# Installation Guide

## Prerequisites

- Frappe Framework v15.x
- ERPNext v15.x (if using ERPNext)
- Wix API access (API key required)
- Python requests library (included in requirements)

## Installation Steps

### 1. Download and Install the App

```bash
# Navigate to your bench directory
cd /path/to/your/bench

# Get the app from GitHub
bench get-app https://github.com/macrobian88/zm-frappe-wix-sync.git

# Install the app on your site
bench install-app zm_frappe_wix_sync --site your-site-name

# Restart bench
bench restart
```

### 2. Get Wix API Credentials

#### Step 2.1: Create a Wix App (if not already done)
1. Go to [Wix Developers](https://dev.wix.com/)
2. Create a new app or use existing app
3. Note down your App ID

#### Step 2.2: Get API Key
1. In your Wix app dashboard, go to OAuth settings
2. Generate an API key with the following permissions:
   - `WIX_STORES.PRODUCT_CREATE`
   - `SCOPE.STORES.PRODUCT_WRITE`
   - `SCOPE.STORES.CATALOG_WRITE`

#### Step 2.3: Get Site ID
The kokofresh site ID is already configured: `a57521a4-3ecd-40b8-852c-462f2af558d2`

### 3. Configure the App

1. **Login to your Frappe/ERPNext site**

2. **Navigate to Wix Sync Settings:**
   - Go to: **Awesome Bar > "Wix Sync Settings"**
   - Or directly access: `https://your-site.com/app/wix-sync-settings`

3. **Configure Settings:**
   - **Enable Sync**: Check this box to enable automatic syncing
   - **Wix Site ID**: `a57521a4-3ecd-40b8-852c-462f2af558d2` (pre-filled for kokofresh)
   - **Wix API Key**: Enter your API key from Step 2.2

4. **Test Connection:**
   - Click the **"Test Connection"** button
   - Verify the connection is successful
   - If successful, you'll see a test product created in your Wix store

### 4. Usage

#### Automatic Sync
- **Create New Item**: When you create a new Item in ERPNext, it will automatically sync to Wix as a product
- **Check Sync Logs**: Go to **Wix Sync Log** to see sync history and any errors

#### Manual Sync
- **From Item List**: 
  1. Go to **Item List**
  2. Select an item
  3. Click **Menu > "Sync to Wix"**

- **From API**: Use the `manual_sync_item` method programmatically

### 5. Verification

1. **Create a Test Item:**
   ```
   - Item Code: TEST-ITEM-001
   - Item Name: Test Product for Wix Sync
   - Standard Rate: 29.99
   - Description: This is a test product for Wix sync
   ```

2. **Check Results:**
   - Item should automatically sync to Wix
   - Check **Wix Sync Log** for sync status
   - Verify product appears in your Wix store dashboard

### 6. Troubleshooting

#### Common Issues

**1. API Key Invalid**
- Error: "HTTP 401: Unauthorized"
- Solution: Verify API key is correct and has proper permissions

**2. Site ID Invalid**
- Error: "HTTP 403: Forbidden"
- Solution: Ensure site ID matches your Wix site

**3. Missing Required Fields**
- Error: "Missing required field: name"
- Solution: Ensure Item has both item_code and item_name

**4. Connection Timeout**
- Error: "Request timeout"
- Solution: Check internet connection and Wix API status

#### Debugging Steps

1. **Check Error Logs:**
   ```bash
   # From bench directory
   bench logs
   ```

2. **Check Sync Logs:**
   - Navigate to **Wix Sync Log** in your site
   - Look for failed syncs and error messages

3. **Test API Connection:**
   - Use the "Test Connection" button in Wix Sync Settings
   - This creates a test product to verify connectivity

4. **Manual Sync Test:**
   - Try manually syncing an existing item
   - Check if automatic sync is enabled in settings

### 7. Uninstallation

```bash
# Remove the app from site
bench uninstall-app zm_frappe_wix_sync --site your-site-name

# Remove the app from bench (optional)
bench remove-app zm_frappe_wix_sync
```

## Configuration Options

### Wix Sync Settings Fields

| Field | Description | Required |
|-------|-------------|----------|
| Enable Sync | Toggles automatic syncing on/off | No |
| Wix Site ID | Your Wix site identifier | Yes |
| Wix API Key | API key for authentication | Yes |
| Test Connection | Button to test API connectivity | - |
| Connection Status | Shows last test result | Read-only |
| Last Test DateTime | Timestamp of last test | Read-only |

### Document Events Hook

The app hooks into the `Item` doctype's `after_insert` event:
- **Trigger**: When a new Item is created
- **Action**: Automatically syncs to Wix as a product
- **Requirements**: Sync must be enabled in settings

## Support

- **Issues**: [GitHub Issues](https://github.com/macrobian88/zm-frappe-wix-sync/issues)
- **Documentation**: [README.md](https://github.com/macrobian88/zm-frappe-wix-sync)
- **API Reference**: [Wix Stores API](https://dev.wix.com/docs/rest/business-solutions/stores/catalog-v3/products-v3/introduction)
