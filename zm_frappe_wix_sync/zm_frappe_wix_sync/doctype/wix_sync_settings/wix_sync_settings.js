frappe.ui.form.on('Wix Sync Settings', {
    test_connection: function(frm) {
        if (!frm.doc.wix_api_key) {
            frappe.msgprint(__('Please set the Wix API Key first'));
            return;
        }
        
        frm.call({
            method: 'zm_frappe_wix_sync.api.wix_sync.test_wix_connection',
            freeze: true,
            freeze_message: __('Testing connection to Wix...'),
            callback: function(response) {
                var result = response.message;
                if (result.success) {
                    frm.set_value('connection_status', 'Success: ' + result.message);
                    frm.set_value('last_test_datetime', frappe.datetime.now_datetime());
                    frappe.show_alert({
                        message: __('Connection successful!'),
                        indicator: 'green'
                    });
                } else {
                    frm.set_value('connection_status', 'Failed: ' + result.message);
                    frm.set_value('last_test_datetime', frappe.datetime.now_datetime());
                    frappe.show_alert({
                        message: __('Connection failed: ' + result.message),
                        indicator: 'red'
                    });
                }
                frm.save();
            }
        });
    }
});
