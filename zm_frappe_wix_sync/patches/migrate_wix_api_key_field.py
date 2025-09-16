#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch to migrate wix_api_key field from Password to Long Text
This patch handles the database schema migration for existing installations
"""
import frappe
from frappe.model import rename_field


def execute():
    """
    Execute the database migration for wix_api_key field type change
    """
    try:
        # Check if the DocType exists
        if not frappe.db.exists("DocType", "Wix Sync Settings"):
            print("Wix Sync Settings DocType not found, skipping patch")
            return
        
        # Get the current field definition
        wix_sync_settings_meta = frappe.get_meta("Wix Sync Settings")
        wix_api_key_field = None
        
        for field in wix_sync_settings_meta.fields:
            if field.fieldname == "wix_api_key":
                wix_api_key_field = field
                break
        
        if not wix_api_key_field:
            print("wix_api_key field not found, skipping patch")
            return
        
        # Check if the field is currently a Password type
        if wix_api_key_field.fieldtype == "Password":
            print("Migrating wix_api_key field from Password to Long Text...")
            
            # Update the field type in the database
            frappe.db.sql("""
                UPDATE `tabDocField` 
                SET fieldtype = 'Long Text', 
                    length = NULL,
                    description = 'Your Wix API Key for authentication (supports up to 1000 characters for IST tokens)'
                WHERE parent = 'Wix Sync Settings' 
                AND fieldname = 'wix_api_key'
            """)
            
            # Update the table schema to allow longer text
            # Since we're changing from VARCHAR(140) to TEXT, we need to alter the table
            table_name = "tabWix Sync Settings"
            
            # Check if the table exists
            if frappe.db.exists_table(table_name):
                # Get current column type
                current_type = frappe.db.sql(f"""
                    SELECT COLUMN_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = '{frappe.conf.db_name}' 
                    AND TABLE_NAME = '{table_name}' 
                    AND COLUMN_NAME = 'wix_api_key'
                """)
                
                if current_type and 'varchar' in current_type[0][0].lower():
                    # Alter the column to TEXT type
                    frappe.db.sql(f"""
                        ALTER TABLE `{table_name}` 
                        MODIFY COLUMN `wix_api_key` TEXT
                    """)
                    print(f"Successfully altered {table_name}.wix_api_key to TEXT type")
            
            # Clear cache to reload the updated metadata
            frappe.clear_cache()
            
            print("wix_api_key field migration completed successfully")
            
        elif wix_api_key_field.fieldtype == "Long Text":
            print("wix_api_key field is already Long Text type, skipping migration")
            
        else:
            print(f"wix_api_key field has unexpected type: {wix_api_key_field.fieldtype}")
            
    except Exception as e:
        print(f"Error during wix_api_key field migration: {str(e)}")
        # Don't raise the exception as patches should be fault-tolerant
        pass
