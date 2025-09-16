# -*- coding: utf-8 -*-
# Copyright (c) 2024, ZM Tech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute():
    """
    Fix naming issue with Wix Sync Settings Single DocType.
    
    This patch handles the migration from the old naming system that caused
    conflicts with Single DocTypes having the same name as the document name.
    """
    try:
        # Check if any Wix Sync Settings documents exist with problematic names
        existing_docs = frappe.get_all('Wix Sync Settings', 
                                     fields=['name', 'title'], 
                                     filters={'name': ['!=', 'Wix Sync Settings']})
        
        if existing_docs:
            frappe.logger().info(f"Found {len(existing_docs)} Wix Sync Settings documents to migrate")
            
            # For each document with a problematic name, rename it
            for doc_info in existing_docs:
                old_name = doc_info.get('name')
                
                # Get the full document
                doc = frappe.get_doc('Wix Sync Settings', old_name)
                
                # Delete the old document
                frappe.delete_doc('Wix Sync Settings', old_name, force=1)
                
                # Create a new document with the correct Single DocType behavior
                # For Single DocTypes, the name should be the same as the DocType
                new_doc = frappe.get_doc({
                    'doctype': 'Wix Sync Settings',
                    'title': doc.get('title', 'Wix Sync Configuration'),
                    'enable_sync': doc.get('enable_sync', 0),
                    'wix_site_id': doc.get('wix_site_id', ''),
                    'wix_api_key': doc.get('wix_api_key', ''),
                    'connection_status': doc.get('connection_status', ''),
                    'last_test_datetime': doc.get('last_test_datetime')
                })
                new_doc.insert()
                
                frappe.logger().info(f"Migrated Wix Sync Settings document from '{old_name}' to 'Wix Sync Settings'")
        
        # Ensure the Single DocType document exists with correct name
        if not frappe.db.exists('Wix Sync Settings', 'Wix Sync Settings'):
            # Create the default Single DocType document
            default_doc = frappe.get_doc({
                'doctype': 'Wix Sync Settings',
                'title': 'Wix Sync Configuration',
                'enable_sync': 0,
                'wix_site_id': 'a57521a4-3ecd-40b8-852c-462f2af558d2',  # Default kokofresh site ID
                'wix_api_key': '',
                'connection_status': '',
                'last_test_datetime': None
            })
            default_doc.insert()
            frappe.logger().info("Created default Wix Sync Settings document")
            
        frappe.db.commit()
        frappe.logger().info("Successfully completed Wix Sync Settings naming fix migration")
        
    except Exception as e:
        frappe.logger().error(f"Error during Wix Sync Settings naming migration: {str(e)}")
        frappe.db.rollback()
        raise
