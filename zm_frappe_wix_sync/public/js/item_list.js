frappe.listview_settings['Item'] = {
    add_fields: ['item_code', 'item_name', 'item_group'],
    onload: function(listview) {
        // Add custom button for manual Wix sync
        listview.page.add_menu_item(__('Sync to Wix'), function() {
            var selected = listview.get_checked_items();
            if (selected.length === 0) {
                frappe.msgprint(__('Please select at least one item'));
                return;
            }
            
            if (selected.length > 1) {
                frappe.msgprint(__('Please select only one item at a time for sync'));
                return;
            }
            
            var item_code = selected[0].item_code;
            
            frappe.call({
                method: 'zm_frappe_wix_sync.api.wix_sync.manual_sync_item',
                args: {
                    item_code: item_code
                },
                freeze: true,
                freeze_message: __('Syncing item to Wix...'),
                callback: function(response) {
                    var result = response.message;
                    if (result.success) {
                        frappe.show_alert({
                            message: __(result.message),
                            indicator: 'green'
                        });
                        listview.refresh();
                    } else {
                        frappe.show_alert({
                            message: __(result.message),
                            indicator: 'red'
                        });
                    }
                }
            });
        });
    }
};
