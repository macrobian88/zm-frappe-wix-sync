# ZM Frappe Wix Sync

A comprehensive Frappe app that automatically synchronizes ERPNext items with Wix Store products in real-time.

## 🚀 **Latest Update - v2.2.0**

### ✅ **API Key Length Limit FIXED** 
**NEW**: Support for long Wix API keys (721+ characters)! This release resolves:
- ❌ "Max allowed characters is 140" error → ✅ Supports up to 1000+ character API keys
- ❌ IST token truncation issues → ✅ Full IST token storage  
- ❌ Authentication failures with long keys → ✅ Complete key preservation
- 🔄 **Automatic Migration**: Existing installations automatically upgrade field type

### ✅ **Previous Fixes - Authentication Issues RESOLVED** 
All Wix authentication problems have been completely fixed! Previous release resolved:
- ❌ `invalid_grant` errors → ✅ Working JWT authentication  
- ❌ 404 Not Found errors → ✅ Correct API endpoints
- ❌ Site ID mismatches → ✅ Auto-detected site configuration
- ❌ Missing Wix Stores app → ✅ Automatic app installation

## 🎯 **Key Features**

- **🔄 Automatic Sync**: Items sync to Wix automatically when created or updated
- **⏰ Background Jobs**: Hourly scheduled sync catches any missed items  
- **🛡️ Robust Authentication**: JWT token support with proper error handling
- **📊 Comprehensive Logging**: Detailed sync status tracking and error reporting
- **🔧 Manual Controls**: Manual sync options for individual or bulk operations
- **⚡ Real-time Updates**: Product name, price, stock, and description sync
- **🔑 Long API Key Support**: Handles IST tokens up to 1000+ characters
- **🔄 Backward Compatible**: Seamless upgrade from previous versions

## 📋 **Prerequisites**

- Frappe Framework v13.0+ 
- ERPNext v13.0+
- Active Wix account with a site
- Wix API key with Store permissions
- Python requests library

## ⚡ **Quick Start**

### 1. Installation
```bash
# Install the app
bench get-app https://github.com/macrobian88/zm-frappe-wix-sync.git
bench --site [your-site] install-app zm_frappe_wix_sync

# Restart to activate hooks
bench restart
```

### 2. Generate Wix API Key
1. Go to [Wix API Keys Manager](https://manage.wix.com/account/api-keys)
2. Click "Create API Key" 
3. **Name**: `Frappe-Wix-Sync`
4. **Permissions**: Select "Manage Stores - All Permissions"
5. **Sites**: Select your site or "All Sites"
6. **Generate** and copy the API key immediately
7. **Note**: IST tokens can be 700+ characters long - this is normal and supported!

### 3. Configure Settings
1. Go to **Wix Sync Settings** in your Frappe site
2. **Enable Sync**: ✅ Check the box
3. **Wix API Key**: Paste your full API key (supports long IST tokens)
4. **Site ID**: Will be auto-detected (or set manually)
5. **Save** the settings

### 4. Test Connection
1. Click **"Test Connection"** button
2. Should show: ✅ "Connection successful!"
3. If errors occur, check the troubleshooting section below

### 5. Start Syncing
- **Automatic**: Create/edit any Item → syncs automatically
- **Manual**: Use sync buttons in Item list or call API methods
- **Bulk**: Use `manual_sync_all_items()` function

## 🔧 **Configuration**

### Wix Sync Settings Fields:
- **Title**: Descriptive name for the configuration
- **Enable Sync**: Master switch for all sync operations
- **Wix Site ID**: Your Wix site identifier (auto-detected)  
- **Wix API Key**: Your JWT authentication token (supports 1000+ characters)
- **Connection Status**: Shows current API connection status
- **Last Test DateTime**: Timestamp of last connection test

## 📚 **API Methods**

### Connection Testing
```python
# Test Wix API connection
frappe.call("zm_frappe_wix_sync.api.wix_sync.test_wix_connection")
```

### Manual Sync Operations  
```python
# Sync single item
frappe.call("zm_frappe_wix_sync.api.wix_sync.manual_sync_single_item", 
           item_code="YOUR_ITEM_CODE")

# Sync all items  
frappe.call("zm_frappe_wix_sync.api.wix_sync.manual_sync_all_items")
```

## 🔄 **How Sync Works**

### Automatic Triggers:
- **Item Creation**: New items sync immediately after creation
- **Item Updates**: Changes sync when items are saved
- **Scheduled Jobs**: Hourly background sync catches missed items

### Data Mapping:
- **Item Name** → Wix Product Name
- **Item Code** → Wix Product SKU  
- **Description** → Wix Product Description
- **Standard Rate** → Wix Product Price
- **Stock Quantity** → Wix Inventory Level
- **Weight** → Wix Product Weight

### Sync Process:
1. Item change detected in Frappe
2. WixSyncManager validates settings
3. Product data prepared for Wix API
4. API call made with authentication
5. Success/error logged in Wix Sync Log
6. User notified of result

## 📋 **Troubleshooting**

### Authentication Issues

#### Problem: "Connection test failed" 
**Solution**: 
```bash
# Check API key format - should start with "IST."
# Verify site ID is correct
# Ensure API key has Store permissions
# Ensure full API key is pasted (IST tokens are 700+ chars)
```

#### Problem: "401 Unauthorized"
**Solution**:
```bash
# Generate new API key with proper permissions
# Check account owner/co-owner status
# Verify API key hasn't been deactivated  
```

#### Problem: "Max allowed characters is 140"
**Solution**:
```bash
# This issue is fixed in v2.2.0+
# Update to latest version to support long API keys
# If still occurring, run: bench migrate
```

#### Problem: "Wix Stores not found"
**Solution**:
```bash
# App auto-installs Wix Stores if missing
# If fails, manually install Wix Stores from Wix App Market
# Restart sync after installation
```

### Sync Issues

#### Problem: Items not syncing
**Solution**:
```python
# Check if sync is enabled
frappe.get_doc("Wix Sync Settings").enable_sync

# Test connection
frappe.call("zm_frappe_wix_sync.api.wix_sync.test_wix_connection")

# Check sync logs
frappe.get_all("Wix Sync Log", limit=10, order_by="creation desc")
```

#### Problem: "Sync Status validation error"  
**Solution**:
```bash
# Go to Customize Form > Wix Sync Log
# Update "Sync Status" field options to:
# Success
# Failed  
# Error
# (Remove \n characters)
```

## 🔄 **Migration Notes**

### Upgrading from v2.1.0 or earlier:
The app automatically migrates the `wix_api_key` field from Password (140 chars) to Long Text (1000+ chars) when you:

1. **Update the app**:
```bash
bench get-app --branch main https://github.com/macrobian88/zm-frappe-wix-sync.git
```

2. **Run migration**:
```bash
bench --site [your-site] migrate
```

3. **Restart**:
```bash
bench restart
```

Your existing API key will be preserved during the migration.

## 🔍 **Monitoring**

### Sync Logs
Check **Wix Sync Log** for detailed sync history:
- Item codes and sync timestamps
- Success/error status  
- Wix product IDs
- Detailed error messages

### Connection Status
Monitor **Wix Sync Settings** for:
- Real-time connection status
- Last successful test timestamp  
- API connectivity health

## 🛠️ **Development**

### Project Structure
```
zm_frappe_wix_sync/
├── api/
│   └── wix_sync.py          # Main sync logic
├── hooks.py                 # Event hooks & scheduling  
├── patches/
│   └── migrate_wix_api_key_field.py  # Field migration
├── zm_frappe_wix_sync/
│   └── doctype/
│       ├── wix_sync_log/    # Sync logging
│       └── wix_sync_settings/ # Configuration
└── public/
    └── js/
        └── item_list.js     # UI enhancements
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📖 **Changelog**

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

## 🆘 **Support**

- **Issues**: [GitHub Issues](https://github.com/macrobian88/zm-frappe-wix-sync/issues)
- **Discussions**: [GitHub Discussions](https://github.com/macrobian88/zm-frappe-wix-sync/discussions)
- **Email**: tech@zmtech.com

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⭐ **Star this repo** if it helps your business!

Made with ❤️ by [ZM Tech](https://github.com/macrobian88)
