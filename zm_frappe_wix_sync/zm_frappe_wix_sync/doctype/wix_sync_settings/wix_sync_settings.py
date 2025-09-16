# -*- coding: utf-8 -*-
# Copyright (c) 2024, ZM Tech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class WixSyncSettings(Document):
    def validate(self):
        # Set default site ID if not provided
        if not self.wix_site_id:
            self.wix_site_id = "a57521a4-3ecd-40b8-852c-462f2af558d2"  # kokofresh site ID

    def on_update(self):
        # Clear connection status on update
        if self.has_value_changed('wix_api_key') or self.has_value_changed('wix_site_id'):
            self.connection_status = ""
            self.last_test_datetime = None
    
    @frappe.whitelist()
    def test_connection(self):
        """
        Test connection method that can be called directly from the DocType
        """
        from zm_frappe_wix_sync.api.wix_sync import test_wix_connection
        return test_wix_connection()
