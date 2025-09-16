# -*- coding: utf-8 -*-
# Copyright (c) 2024, ZM Tech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute():
    """
    Fix Wix Sync Settings Single DocType naming issues.
    
    This patch handles installations where the Wix Sync Settings document
    was created with an incorrect name (auto-generated instead of using
    the proper Single DocType naming convention).
    """
    try:
        doctype_name = "Wix Sync Settings"
        
        # Check if we already have a properly named document
        if frappe.db.exists(doctype_name, doctype_name):
            frappe.logger().info("Wix Sync Settings already has correct naming")
            
            # Clean up any duplicate documents with incorrect names
            incorrect_docs = frappe.get_all(doctype_name, 
                                          filters={"name": ["!=", doctype_name]})
            
            if incorrect_docs:
                frappe.logger().info(f"Found {len(incorrect_docs)} incorrectly named documents to clean up")
                for doc_info in incorrect_docs:
                    try:
                        frappe.delete_doc(doctype_name, doc_info.name, force=True)
                        frappe.logger().info(f"Deleted duplicate Wix Sync Settings: {doc_info.name}")
                    except Exception as e:
                        frappe.logger().error(f"Error deleting duplicate document {doc_info.name}: {str(e)}")
                        
            frappe.db.commit()
            return
        
        # Look for any Wix Sync Settings documents
        existing_docs = frappe.get_all(doctype_name, limit=1)
        
        if existing_docs:
            incorrect_name = existing_docs[0].name
            frappe.logger().info(f"Found Wix Sync Settings with incorrect name: {incorrect_name}")
            
            # Get the document data
            old_doc = frappe.get_doc(doctype_name, incorrect_name)
            
            # Create new document with proper naming
            new_doc = frappe.get_doc({
                "doctype": doctype_name,
                "name": doctype_name,
                "title": old_doc.get("title", "Wix Sync Configuration"),
                "enable_sync": old_doc.get("enable_sync", 0),
                "wix_site_id": old_doc.get("wix_site_id", "a57521a4-3ecd-40b8-852c-462f2af558d2"),
                "wix_api_key": old_doc.get("wix_api_key", ""),
                "connection_status": old_doc.get("connection_status", ""),
                "last_test_datetime": old_doc.get("last_test_datetime")
            })
            
            # Set flags to bypass naming series
            new_doc.flags.ignore_naming_series = True
            new_doc.insert(ignore_permissions=True)
            
            # Delete the old document
            frappe.delete_doc(doctype_name, incorrect_name, force=True)
            
            frappe.logger().info(f"Successfully migrated Wix Sync Settings from '{incorrect_name}' to '{doctype_name}'")
            
        else:
            # No document exists, create a default one
            frappe.logger().info("No Wix Sync Settings found, creating default document")
            
            default_doc = frappe.get_doc({
                "doctype": doctype_name,
                "name": doctype_name,
                "title": "Wix Sync Configuration",
                "enable_sync": 0,
                "wix_site_id": "a57521a4-3ecd-40b8-852c-462f2af558d2",
                "wix_api_key": "",
                "connection_status": "Ready for configuration",
                "last_test_datetime": None
            })
            
            default_doc.flags.ignore_naming_series = True
            default_doc.insert(ignore_permissions=True)
            
            frappe.logger().info("Created default Wix Sync Settings document")
        
        frappe.db.commit()
        frappe.logger().info("Wix Sync Settings Single DocType naming migration completed successfully")
        
    except Exception as e:
        frappe.logger().error(f"Error during Wix Sync Settings naming migration: {str(e)}")
        frappe.db.rollback()
        raise
