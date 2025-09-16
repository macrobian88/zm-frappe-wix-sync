# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

app_name = "zm_frappe_wix_sync"
app_title = "ZM Frappe Wix Sync"
app_publisher = "ZM Tech"
app_description = "A Frappe app to sync ERPNext items with Wix products"
app_icon = "octicon octicon-sync"
app_color = "grey"
app_email = "tech@zmtech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zm_frappe_wix_sync/css/zm_frappe_wix_sync.css"
# app_include_js = "/assets/zm_frappe_wix_sync/js/zm_frappe_wix_sync.js"

# include js, css files in header of web template
# web_include_css = "/assets/zm_frappe_wix_sync/css/zm_frappe_wix_sync.css"
# web_include_js = "/assets/zm_frappe_wix_sync/js/zm_frappe_wix_sync.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "zm_frappe_wix_sync/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {"Item" : "public/js/item_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "zm_frappe_wix_sync.install.before_install"
# after_install = "zm_frappe_wix_sync.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "zm_frappe_wix_sync.uninstall.before_uninstall"
# after_uninstall = "zm_frappe_wix_sync.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zm_frappe_wix_sync.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Item": {
        "after_insert": "zm_frappe_wix_sync.api.wix_sync.sync_item_to_wix"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"zm_frappe_wix_sync.tasks.all"
# 	],
# 	"daily": [
# 		"zm_frappe_wix_sync.tasks.daily"
# 	],
# 	"hourly": [
# 		"zm_frappe_wix_sync.tasks.hourly"
# 	],
# 	"weekly": [
# 		"zm_frappe_wix_sync.tasks.weekly"
# 	]
# 	"monthly": [
# 		"zm_frappe_wix_sync.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "zm_frappe_wix_sync.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "zm_frappe_wix_sync.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "zm_frappe_wix_sync.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"zm_frappe_wix_sync.auth.validate"
# ]
