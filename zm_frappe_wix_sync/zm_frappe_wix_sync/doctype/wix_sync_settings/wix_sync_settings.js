frappe.ui.form.on('Wix Sync Settings', {
    test_connection: function(frm) {
        // Validate required fields before testing
        if (!frm.doc.wix_api_key) {
            frappe.msgprint({
                title: __('Missing API Key'),
                message: __('Please set the Wix API Key first'),
                indicator: 'red'
            });
            return;
        }
        
        if (!frm.doc.wix_site_id) {
            frappe.msgprint({
                title: __('Missing Site ID'),
                message: __('Please set the Wix Site ID first'),
                indicator: 'red'
            });
            return;
        }
        
        // Save the form first to ensure settings are persisted
        frm.save().then(() => {
            // Call the test connection API
            frm.call({
                method: 'zm_frappe_wix_sync.api.wix_sync.test_wix_connection',
                freeze: true,
                freeze_message: __('Testing connection to Wix...'),
                callback: function(response) {
                    if (response && response.message) {
                        var result = response.message;
                        
                        // Update the connection status fields
                        frm.set_value('last_test_datetime', frappe.datetime.now_datetime());
                        
                        if (result.success) {
                            frm.set_value('connection_status', 'Success: ' + result.message);
                            frappe.show_alert({
                                message: __('Connection Test Successful!'),
                                indicator: 'green'
                            });
                            
                            // Show success message
                            frappe.msgprint({
                                title: __('Connection Successful'),
                                message: result.message,
                                indicator: 'green'
                            });
                        } else {
                            frm.set_value('connection_status', 'Failed: ' + result.message);
                            frappe.show_alert({
                                message: __('Connection Test Failed'),
                                indicator: 'red'
                            });
                            
                            // Show error message
                            frappe.msgprint({
                                title: __('Connection Failed'),
                                message: result.message,
                                indicator: 'red'
                            });
                        }
                        
                        // Save the updated status
                        frm.save();
                    } else {
                        // Handle unexpected response format
                        frm.set_value('connection_status', 'Error: Unexpected response format');
                        frm.set_value('last_test_datetime', frappe.datetime.now_datetime());
                        
                        frappe.msgprint({
                            title: __('Connection Test Error'),
                            message: __('Received unexpected response from server'),
                            indicator: 'red'
                        });
                        
                        frm.save();
                    }
                },
                error: function(xhr, status, error) {
                    // Handle API call errors
                    let error_message = 'Unknown error occurred';
                    
                    if (xhr && xhr.responseJSON && xhr.responseJSON.message) {
                        error_message = xhr.responseJSON.message;
                    } else if (error) {
                        error_message = error;
                    }
                    
                    frm.set_value('connection_status', 'Error: ' + error_message);
                    frm.set_value('last_test_datetime', frappe.datetime.now_datetime());
                    
                    frappe.show_alert({
                        message: __('Connection Test Failed'),
                        indicator: 'red'
                    });
                    
                    frappe.msgprint({
                        title: __('Connection Test Error'),
                        message: error_message,
                        indicator: 'red'
                    });
                    
                    frm.save();
                }
            });
        }).catch((error) => {
            // Handle form save errors
            frappe.msgprint({
                title: __('Save Error'),
                message: __('Could not save the settings. Please try again.'),
                indicator: 'red'
            });
        });
    },
    
    refresh: function(frm) {
        // Add custom styling or additional functionality on form refresh
        if (frm.doc.connection_status) {
            // Add visual indicators based on connection status
            if (frm.doc.connection_status.startsWith('Success')) {
                frm.dashboard.set_headline_alert(
                    '<div class="text-success">Last connection test was successful</div>'
                );
            } else if (frm.doc.connection_status.startsWith('Failed') || frm.doc.connection_status.startsWith('Error')) {
                frm.dashboard.set_headline_alert(
                    '<div class="text-danger">Last connection test failed</div>'
                );
            }
        }
    },
    
    wix_api_key: function(frm) {
        // Clear connection status when API key changes
        if (frm.doc.connection_status) {
            frm.set_value('connection_status', '');
            frm.set_value('last_test_datetime', '');
        }
    },
    
    wix_site_id: function(frm) {
        // Clear connection status when site ID changes
        if (frm.doc.connection_status) {
            frm.set_value('connection_status', '');
            frm.set_value('last_test_datetime', '');
        }
    }
});
