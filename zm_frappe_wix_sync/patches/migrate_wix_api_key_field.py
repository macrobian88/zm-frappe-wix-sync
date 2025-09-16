#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch to migrate wix_api_key field from Password to Long Text
This patch handles the database schema migration for existing installations
"""
import frappe


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
        try:
            wix_api_key_field = frappe.db.get_value("DocField", 
                {"parent": "Wix Sync Settings", "fieldname": "wix_api_key"}, 
                ["fieldtype", "name"], as_dict=True)
        except:
            print("wix_api_key field not found in DocField, skipping patch")
            return
        
        if not wix_api_key_field:
            print("wix_api_key field not found, skipping patch")
            return
        
        # Check if the field is currently a Password type
        if wix_api_key_field.fieldtype == "Password":
            print("Migrating wix_api_key field from Password to Long Text...")
            
            # Update the field type in the DocField table
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
            table_exists = frappe.db.sql(f"""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = '{frappe.conf.db_name}' 
                AND TABLE_NAME = '{table_name}'
            """)
            
            if table_exists and table_exists[0][0] > 0:
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
            
            # Commit the changes
            frappe.db.commit()
            
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
        frappe.log_error("Wix API Key Migration Error", str(e))
        pass
