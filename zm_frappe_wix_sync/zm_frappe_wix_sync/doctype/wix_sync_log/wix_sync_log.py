# -*- coding: utf-8 -*-
# Copyright (c) 2024, ZM Tech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class WixSyncLog(Document):
    def validate(self):
        if not self.sync_datetime:
            self.sync_datetime = frappe.utils.now()
