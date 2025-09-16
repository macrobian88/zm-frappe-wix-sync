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
    For Single DocTypes, create the document if it doesn't exist
    """
    try:
        # For Single DocTypes, the document name is the same as the DocType name
        doctype_name = "Wix Sync Settings"
        
        # Check if the document exists
        if frappe.db.exists(doctype_name, doctype_name):
            return frappe.get_doc(doctype_name, doctype_name)
        else:
            # Create the default Single DocType document if it doesn't exist
            frappe.logger().info("Wix Sync Settings document not found, creating default document")
            
            default_doc = frappe.get_doc({
                "doctype": doctype_name,
                "title": "Wix Sync Configuration",
                "enable_sync": 0,
                "wix_site_id": "a57521a4-3ecd-40b8-852c-462f2af558d2",  # Default kokofresh site ID
                "wix_api_key": "",
                "connection_status": "",
                "last_test_datetime": None
            })
            default_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            
            frappe.logger().info("Created default Wix Sync Settings document")
            return default_doc
            
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
            return {"success": False, "message": "Unable to load Wix sync settings"}
            
        api_key = settings.get("wix_api_key")
        site_id = settings.get("wix_site_id", "a57521a4-3ecd-40b8-852c-462f2af558d2")
        
        if not api_key:
            return {"success": False, "message": "API key not configured. Please set your Wix API key first."}
        
        if not site_id:
            return {"success": False, "message": "Site ID not configured. Please set your Wix Site ID first."}
        
        # Test with a simple API call to get site info instead of creating a product
        # This is less intrusive than creating test products
        url = f"https://www.wixapis.com/site-properties/v4/properties"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "wix-site-id": site_id
        }
        
        # Make a simple GET request to test authentication
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return {
                "success": True, 
                "message": "Connection successful! API key and site ID are valid."
            }
        elif response.status_code == 401:
            return {
                "success": False, 
                "message": "Authentication failed. Please check your API key."
            }
        elif response.status_code == 403:
            return {
                "success": False, 
                "message": "Access denied. Please check your API key permissions and site ID."
            }
        elif response.status_code == 404:
            return {
                "success": False, 
                "message": "Site not found. Please check your site ID."
            }
        else:
            return {
                "success": False, 
                "message": f"Connection test failed with HTTP {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Connection timeout. Please check your internet connection."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Connection error. Please check your internet connection."}
    except Exception as e:
        frappe.log_error(f"Error in test_wix_connection: {str(e)}", "Wix Sync Test Connection")
        return {"success": False, "message": f"Unexpected error: {str(e)}"}


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
