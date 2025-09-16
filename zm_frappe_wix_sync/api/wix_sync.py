# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import requests
import json
from frappe.utils import cstr


def sync_item_to_wix(doc, method):
    """
    Sync ERPNext Item to Wix Product when a new item is created
    This function is called via document hooks in hooks.py
    """
    try:
        # Check if sync is enabled
        settings = get_wix_sync_settings()
        if not settings or not settings.get("enable_sync"):
            frappe.log_error("Wix sync is disabled or not configured", "Wix Sync")
            return

        # Get Wix API credentials
        api_key = settings.get("wix_api_key")
        site_id = settings.get("wix_site_id", "a57521a4-3ecd-40b8-852c-462f2af558d2")  # kokofresh site ID
        
        if not api_key:
            frappe.log_error("Wix API key not configured", "Wix Sync")
            return

        # Prepare product data for Wix API
        wix_product_data = prepare_wix_product_data(doc)
        
        # Make API call to Wix
        response = create_wix_product(wix_product_data, api_key, site_id)
        
        if response.get("success"):
            frappe.msgprint(f"Item '{doc.item_name}' successfully synced to Wix", alert=True, indicator="green")
            
            # Log successful sync
            create_sync_log(doc.name, "Success", response.get("wix_product_id"), "")
        else:
            error_msg = response.get("error", "Unknown error occurred")
            frappe.msgprint(f"Failed to sync item to Wix: {error_msg}", alert=True, indicator="red")
            
            # Log failed sync
            create_sync_log(doc.name, "Failed", "", error_msg)
            
    except Exception as e:
        error_msg = f"Exception in Wix sync: {str(e)}"
        frappe.log_error(error_msg, "Wix Sync Error")
        frappe.msgprint(f"Error syncing item to Wix: {str(e)}", alert=True, indicator="red")
        
        # Log failed sync
        create_sync_log(doc.name, "Error", "", error_msg)


def get_wix_sync_settings():
    """
    Get Wix sync settings from the database
    """
    try:
        if frappe.db.exists("Wix Sync Settings", "Wix Sync Settings"):
            return frappe.get_doc("Wix Sync Settings", "Wix Sync Settings")
        else:
            return None
    except Exception as e:
        frappe.log_error(f"Error getting Wix sync settings: {str(e)}", "Wix Sync")
        return None


def prepare_wix_product_data(item_doc):
    """
    Convert ERPNext Item data to Wix Product format according to Wix Stores API v3
    """
    # Get the standard selling rate for the item
    standard_rate = get_item_price(item_doc.name) or "10.00"
    
    # Prepare the product data according to Wix Stores API v3 requirements
    wix_product = {
        "product": {
            "name": item_doc.item_name or item_doc.name,
            "productType": "PHYSICAL",  # Assuming physical products for POC
            "physicalProperties": {},
            "variantsInfo": {
                "variants": [
                    {
                        "price": {
                            "actualPrice": {
                                "amount": str(standard_rate)
                            }
                        },
                        "physicalProperties": {}
                    }
                ]
            }
        }
    }
    
    # Add description if available
    if item_doc.description:
        wix_product["product"]["plainDescription"] = f"<p>{cstr(item_doc.description)}</p>"
    
    # Add SKU if available
    if hasattr(item_doc, 'item_code') and item_doc.item_code:
        wix_product["product"]["variantsInfo"]["variants"][0]["sku"] = item_doc.item_code
    
    # Add fields to return in response for debugging
    wix_product["fields"] = [
        "PLAIN_DESCRIPTION",
        "CURRENCY",
        "VARIANTS_INFO"
    ]
    
    return wix_product


def get_item_price(item_code):
    """
    Get the standard selling rate for an item
    """
    try:
        # Try to get price from Item Price doctype
        price_list = frappe.get_value("Item Price", 
            {"item_code": item_code, "selling": 1}, 
            "price_list_rate")
        
        if price_list:
            return float(price_list)
            
        # If no price list found, try to get from Item doctype
        standard_rate = frappe.get_value("Item", item_code, "standard_rate")
        if standard_rate:
            return float(standard_rate)
            
        # Default fallback price
        return 10.00
        
    except Exception as e:
        frappe.log_error(f"Error getting item price for {item_code}: {str(e)}", "Wix Sync")
        return 10.00


def create_wix_product(product_data, api_key, site_id):
    """
    Make API call to Wix to create a product
    """
    try:
        url = "https://www.wixapis.com/stores/v3/products"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "wix-site-id": site_id
        }
        
        # Make the API request
        response = requests.post(url, 
            json=product_data, 
            headers=headers,
            timeout=30)
        
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            product_id = response_data.get("product", {}).get("id")
            
            return {
                "success": True,
                "wix_product_id": product_id,
                "response": response_data
            }
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            return {
                "success": False,
                "error": error_msg
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout - Wix API did not respond in time"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection error - Could not connect to Wix API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def create_sync_log(item_code, status, wix_product_id="", error_message=""):
    """
    Create a log entry for the sync operation
    """
    try:
        sync_log = frappe.get_doc({
            "doctype": "Wix Sync Log",
            "item_code": item_code,
            "sync_status": status,
            "wix_product_id": wix_product_id,
            "error_message": error_message,
            "sync_datetime": frappe.utils.now()
        })
        sync_log.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"Error creating sync log: {str(e)}", "Wix Sync Log Error")


@frappe.whitelist()
def test_wix_connection():
    """
    Test connection to Wix API - can be called from the UI
    """
    try:
        settings = get_wix_sync_settings()
        if not settings:
            return {"success": False, "message": "Wix sync settings not found"}
            
        api_key = settings.get("wix_api_key")
        site_id = settings.get("wix_site_id", "a57521a4-3ecd-40b8-852c-462f2af558d2")
        
        if not api_key:
            return {"success": False, "message": "API key not configured"}
        
        # Test with a simple product creation (minimal data)
        test_product = {
            "product": {
                "name": "Test Product - Please Delete",
                "productType": "PHYSICAL",
                "physicalProperties": {},
                "variantsInfo": {
                    "variants": [{
                        "price": {
                            "actualPrice": {
                                "amount": "1.00"
                            }
                        },
                        "physicalProperties": {}
                    }]
                }
            }
        }
        
        result = create_wix_product(test_product, api_key, site_id)
        
        if result.get("success"):
            return {
                "success": True, 
                "message": f"Connection successful! Test product created with ID: {result.get('wix_product_id')}"
            }
        else:
            return {
                "success": False, 
                "message": f"Connection failed: {result.get('error')}"
            }
            
    except Exception as e:
        return {"success": False, "message": f"Error testing connection: {str(e)}"}


@frappe.whitelist()
def manual_sync_item(item_code):
    """
    Manually sync an item to Wix - can be called from the UI
    """
    try:
        item_doc = frappe.get_doc("Item", item_code)
        sync_item_to_wix(item_doc, "manual")
        return {"success": True, "message": f"Item {item_code} sync initiated"}
    except Exception as e:
        return {"success": False, "message": f"Error syncing item: {str(e)}"}
