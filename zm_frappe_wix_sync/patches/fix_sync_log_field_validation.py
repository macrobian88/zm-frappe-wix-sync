# Fix Wix Sync Log field validation issue
# This patch fixes the malformed sync_status field options

import frappe

def execute():
    """
    Fix the sync_status field options in Wix Sync Log DocType
    Changes from "Success\\nFailed\\nError" to proper newline format
    """
    try:
        # Check if the DocType exists
        if not frappe.db.exists("DocType", "Wix Sync Log"):
            return
            
        # Get the DocType
        doc = frappe.get_doc("DocType", "Wix Sync Log")
        
        # Find the sync_status field
        for field in doc.fields:
            if field.fieldname == "sync_status":
                # Fix the malformed options
                if field.options == "Success\\\\nFailed\\\\nError":
                    field.options = "Success\nFailed\nError"
                    doc.save()
                    frappe.db.commit()
                    
                    print("✅ Fixed Wix Sync Log sync_status field options")
                    
                    # Clear cache to ensure changes take effect
                    frappe.clear_cache(doctype="Wix Sync Log")
                    
                    # Rebuild DocType to apply changes
                    frappe.reload_doctype("Wix Sync Log")
                    
                    break
        else:
            print("ℹ️ sync_status field not found or already fixed")
            
    except Exception as e:
        print(f"⚠️ Error fixing Wix Sync Log field: {str(e)}")
        # Don't raise exception as this is a non-critical patch
