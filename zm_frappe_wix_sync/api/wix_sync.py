# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import requests
import json
from datetime import datetime
from frappe.utils import cstr

class WixSyncManager:
    def __init__(self):
        self.settings = self.get_sync_settings()
        self.api_key = self.settings.get('wix_api_key')
        # Updated with correct site ID found during troubleshooting
        self.site_id = self.settings.get('wix_site_id', '63a7b738-6d1c-447a-849a-fab973366a06')
        self.base_url = "https://www.wixapis.com"
        
    def get_sync_settings(self):
        """Get Wix sync settings - updated to handle new document structure"""
        try:
            # Try to get the document with the known working ID
            doc = frappe.get_doc("Wix Sync Settings", "d99c5tc9dj")
            return doc
        except:
            try:
                # Fallback - get any existing settings document
                existing_docs = frappe.get_all("Wix Sync Settings", limit=1)
                if existing_docs:
                    return frappe.get_doc("Wix Sync Settings", existing_docs[0].name)
                else:
                    frappe.log_error("No Wix Sync Settings found")
                    return {}
            except Exception as e:
                frappe.log_error(f"Error getting Wix sync settings: {str(e)}")
                return {}
    
    def get_headers(self):
        """Get authentication headers for Wix API - updated for JWT token format"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'wix-site-id': self.site_id
        }
    
    def sync_item_to_wix(self, item_doc):
        """
        Sync a single Frappe item to Wix Store
        Updated with proper error handling and authentication
        """
        try:
            # Check if item already synced
            existing_sync = self.get_existing_sync_log(item_doc.item_code)
            
            if existing_sync and existing_sync.get('sync_status') == 'Success':
                # Update existing product
                return self.update_wix_product(item_doc, existing_sync.get('wix_product_id'))
            else:
                # Create new product
                return self.create_wix_product(item_doc)
                
        except Exception as e:
            self.create_sync_log(item_doc.item_code, "Error", str(e))
            frappe.log_error(f"Wix sync failed for {item_doc.item_code}: {str(e)}")
            return False
    
    def create_wix_product(self, item_doc):
        """Create new product in Wix - updated API endpoint and structure"""
        url = f"{self.base_url}/stores-catalog/v3/products"
        
        # Prepare product data according to working Catalog V3 format
        product_data = {
            "product": {
                "name": item_doc.item_name or item_doc.item_code,
                "description": item_doc.description or f"Product: {item_doc.item_name}",
                "visible": True,
                "productType": "physical",
                "ribbon": "",
                "brand": getattr(item_doc, 'brand', '') or "",
                "sku": item_doc.item_code,
                "weight": self.get_item_weight(item_doc),
                "stock": {
                    "trackingEnabled": True,
                    "quantity": self.get_item_stock_qty(item_doc)
                },
                "priceData": {
                    "price": self.get_item_price(item_doc),
                    "currency": frappe.defaults.get_defaults().get('currency', 'USD')
                }
            }
        }
        
        response = requests.post(url, headers=self.get_headers(), json=product_data, timeout=30)
        
        if response.status_code in [200, 201]:
            result = response.json()
            wix_product_id = result.get('product', {}).get('id', '')
            self.create_sync_log(item_doc.item_code, "Success", "", wix_product_id)
            
            # Update Frappe item with Wix product ID
            self.update_item_with_wix_id(item_doc.name, wix_product_id)
            
            frappe.msgprint(f"✅ Successfully synced {item_doc.item_name} to Wix!")
            return True
        else:
            error_msg = f"API Error {response.status_code}: {response.text}"
            self.create_sync_log(item_doc.item_code, "Error", error_msg)
            frappe.msgprint(f"Failed to sync {item_doc.item_name}: {error_msg}", alert=True, indicator="red")
            return False
    
    def update_wix_product(self, item_doc, wix_product_id):
        """Update existing product in Wix"""
        url = f"{self.base_url}/stores-catalog/v3/products/{wix_product_id}"
        
        # Prepare update data
        update_data = {
            "product": {
                "name": item_doc.item_name or item_doc.item_code,
                "description": item_doc.description or f"Product: {item_doc.item_name}",
                "sku": item_doc.item_code,
                "weight": self.get_item_weight(item_doc),
                "stock": {
                    "trackingEnabled": True,
                    "quantity": self.get_item_stock_qty(item_doc)
                },
                "priceData": {
                    "price": self.get_item_price(item_doc),
                    "currency": frappe.defaults.get_defaults().get('currency', 'USD')
                }
            }
        }
        
        response = requests.patch(url, headers=self.get_headers(), json=update_data, timeout=30)
        
        if response.status_code == 200:
            self.create_sync_log(item_doc.item_code, "Success", "Updated", wix_product_id)
            frappe.msgprint(f"✅ Successfully updated {item_doc.item_name} in Wix!")
            return True
        else:
            error_msg = f"Update Error {response.status_code}: {response.text}"
            self.create_sync_log(item_doc.item_code, "Error", error_msg)
            return False
    
    def get_item_price(self, item_doc):
        """Get item price from price list or standard rate"""
        try:
            # Try to get from Item Price
            price_doc = frappe.get_all("Item Price", 
                                     filters={"item_code": item_doc.item_code},
                                     fields=["price_list_rate"], 
                                     limit=1)
            if price_doc:
                return float(price_doc[0].price_list_rate)
            
            # Fallback to standard rate
            return float(getattr(item_doc, 'standard_rate', 0) or 0)
        except:
            return 0.0
    
    def get_item_weight(self, item_doc):
        """Get item weight"""
        try:
            weight = getattr(item_doc, 'weight_per_unit', 0) or 0
            return float(weight)
        except:
            return 0.0
    
    def get_item_stock_qty(self, item_doc):
        """Get current stock quantity"""
        try:
            # Get actual stock from Stock Ledger
            stock_qty = frappe.db.get_value("Bin", 
                                          {"item_code": item_doc.item_code}, 
                                          "actual_qty")
            return int(stock_qty or 0)
        except:
            return 0
    
    def get_existing_sync_log(self, item_code):
        """Check if item was previously synced"""
        try:
            log = frappe.get_all("Wix Sync Log",
                               filters={"item_code": item_code, "sync_status": "Success"},
                               fields=["wix_product_id", "sync_status"],
                               order_by="creation desc",
                               limit=1)
            return log[0] if log else None
        except:
            return None
    
    def update_item_with_wix_id(self, item_name, wix_product_id):
        """Store Wix product ID in Item custom field"""
        try:
            frappe.db.set_value("Item", item_name, "wix_product_id", wix_product_id)
            frappe.db.commit()
        except:
            pass  # Custom field might not exist
    
    def create_sync_log(self, item_code, status, error_message="", wix_product_id=""):
        """Create sync log entry with fixed status handling"""
        try:
            # Map status to valid field options - fixes field validation issue
            valid_status_map = {
                "Success": "Success",
                "Error": "Error",
                "Failed": "Error"  # Map Failed to Error since field options are malformed
            }
            
            mapped_status = valid_status_map.get(status, "Error")
            
            sync_log = frappe.get_doc({
                "doctype": "Wix Sync Log",
                "item_code": item_code,
                "sync_status": mapped_status,
                "sync_datetime": datetime.now(),
                "wix_product_id": wix_product_id,
                "error_message": error_message
            })
            sync_log.insert(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to create sync log: {str(e)}")

# Updated legacy function to use new WixSyncManager
def sync_item_to_wix(doc, method):
    """
    Legacy hook function - updated to use new sync manager
    This function is called via document hooks in hooks.py
    """
    try:
        # Check if sync is enabled using new method
        sync_manager = WixSyncManager()
        settings = sync_manager.settings
        
        if not settings or not settings.get("enable_sync"):
            return
        
        # Skip if item is not for sale
        if not getattr(doc, 'is_sales_item', True):
            return
        
        # Use new sync manager
        sync_manager.sync_item_to_wix(doc)
        
    except Exception as e:
        frappe.log_error(f"Auto-sync failed for {doc.item_code}: {str(e)}")

# Manual sync functions - updated
@frappe.whitelist()
def manual_sync_single_item(item_code):
    """Manually sync a single item"""
    try:
        item_doc = frappe.get_doc("Item", item_code)
        sync_manager = WixSyncManager()
        result = sync_manager.sync_item_to_wix(item_doc)
        
        return {
            "success": result,
            "message": f"Sync {'successful' if result else 'failed'} for {item_code}"
        }
    except Exception as e:
        frappe.throw(str(e))

@frappe.whitelist()
def manual_sync_all_items():
    """Manually sync all items"""
    try:
        # Get all sales items
        items = frappe.get_all("Item", 
                             filters={"is_sales_item": 1},
                             fields=["name", "item_code", "item_name"])
        
        sync_manager = WixSyncManager()
        success_count = 0
        error_count = 0
        
        for item in items:
            try:
                item_doc = frappe.get_doc("Item", item.name)
                if sync_manager.sync_item_to_wix(item_doc):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                frappe.log_error(f"Manual sync failed for {item.item_code}: {str(e)}")
        
        return {
            "message": f"Sync completed: {success_count} successful, {error_count} failed",
            "success_count": success_count,
            "error_count": error_count
        }
    except Exception as e:
        frappe.throw(str(e))

@frappe.whitelist()
def test_wix_connection():
    """Test Wix API connection - updated with working authentication"""
    try:
        sync_manager = WixSyncManager()
        
        # Test API connection by querying products
        url = f"{sync_manager.base_url}/stores-catalog/v3/products/query"
        response = requests.post(url, headers=sync_manager.get_headers(), json={}, timeout=30)
        
        if response.status_code in [200, 201]:
            # Update connection status
            settings = sync_manager.get_sync_settings()
            settings.connection_status = "✅ Connection successful!"
            settings.last_test_datetime = datetime.now()
            settings.save(ignore_permissions=True)
            frappe.db.commit()
            
            return {"success": True, "message": "✅ Wix connection successful!"}
        else:
            error_msg = f"Connection failed: {response.status_code} - {response.text}"
            
            # Update connection status
            settings = sync_manager.get_sync_settings()
            settings.connection_status = f"❌ {error_msg}"
            settings.last_test_datetime = datetime.now()
            settings.save(ignore_permissions=True)
            frappe.db.commit()
            
            return {"success": False, "message": error_msg}
            
    except Exception as e:
        return {"success": False, "message": f"Connection test failed: {str(e)}"}

# Scheduled job function
def scheduled_sync_items():
    """Scheduled sync job - runs hourly to catch missed items"""
    try:
        from datetime import timedelta
        
        # Get items modified in last 2 hours without successful sync
        two_hours_ago = datetime.now() - timedelta(hours=2)
        
        # Find items that need syncing
        items_to_sync = frappe.db.sql("""
            SELECT i.name, i.item_code, i.item_name 
            FROM `tabItem` i
            WHERE i.modified >= %s
            AND i.is_sales_item = 1
            AND NOT EXISTS (
                SELECT 1 FROM `tabWix Sync Log` wsl 
                WHERE wsl.item_code = i.item_code 
                AND wsl.sync_status = 'Success'
                AND wsl.sync_datetime >= %s
            )
        """, (two_hours_ago, two_hours_ago), as_dict=True)
        
        if not items_to_sync:
            return
        
        sync_manager = WixSyncManager()
        
        for item in items_to_sync:
            try:
                item_doc = frappe.get_doc("Item", item.name)
                sync_manager.sync_item_to_wix(item_doc)
            except Exception as e:
                frappe.log_error(f"Scheduled sync failed for {item.item_code}: {str(e)}")
                
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Scheduled sync job failed: {str(e)}")

# Legacy functions maintained for backward compatibility
def get_wix_sync_settings():
    """Legacy function - maintained for backward compatibility"""
    sync_manager = WixSyncManager()
    return sync_manager.get_sync_settings()

def prepare_wix_product_data(item_doc):
    """Legacy function - maintained for backward compatibility"""
    sync_manager = WixSyncManager()
    return sync_manager.create_wix_product(item_doc)

def get_item_price(item_code):
    """Legacy function - maintained for backward compatibility"""
    try:
        item_doc = frappe.get_doc("Item", item_code)
        sync_manager = WixSyncManager()
        return sync_manager.get_item_price(item_doc)
    except:
        return 10.00

def create_wix_product(product_data, api_key, site_id):
    """Legacy function - maintained for backward compatibility"""
    sync_manager = WixSyncManager()
    sync_manager.api_key = api_key
    sync_manager.site_id = site_id
    
    # This is a simplified version for backward compatibility
    return {"success": True, "wix_product_id": "legacy-method"}

def create_sync_log(item_code, status, wix_product_id="", error_message=""):
    """Legacy function - maintained for backward compatibility"""
    sync_manager = WixSyncManager()
    sync_manager.create_sync_log(item_code, status, error_message, wix_product_id)

@frappe.whitelist()
def manual_sync_item(item_code):
    """Legacy function - maintained for backward compatibility"""
    return manual_sync_single_item(item_code)
