# ZM Frappe Wix Sync

A Frappe v15 custom module app that syncs ERPNext items with Wix products for the kokofresh website.

## Features

- **Product Sync**: Automatically syncs ERPNext Item creation with Wix Product creation
- **Real-time Integration**: Uses Frappe hooks to trigger Wix API calls when items are created
- **Configurable Settings**: Easy setup through Frappe settings doctype
- **Error Handling**: Comprehensive logging and error handling for sync operations

## Installation

1. Get the app:
```bash
bench get-app https://github.com/macrobian88/zm-frappe-wix-sync.git
```

2. Install on your site:
```bash
bench install-app zm_frappe_wix_sync
```

3. Configure your Wix API credentials in the Wix Sync Settings doctype

## Configuration

After installation, navigate to:
**Settings > Wix Sync Settings**

Configure the following:
- **Wix Site ID**: Your Wix site ID (kokofresh site ID)
- **API Key**: Your Wix API key
- **Enable Sync**: Toggle to enable/disable automatic syncing

## How it Works

When a new Item is created in ERPNext:
1. The app listens for the `after_insert` event via Frappe hooks
2. Extracts item details (name, description, price, etc.)
3. Formats the data according to Wix Stores API v3 requirements
4. Makes API call to create product in Wix
5. Logs the sync status and any errors

## API Reference

Uses Wix Stores Catalog V3 API:
- **Endpoint**: `POST https://www.wixapis.com/stores/v3/products`
- **Authentication**: Bearer token
- **Required Fields**: name, productType, variantsInfo, physicalProperties

## Development

This is a POC (Proof of Concept) focusing on:
- One-way sync from ERPNext to Wix
- Product creation only
- Simple error handling and logging

## Support

For issues and questions, please open an issue on the GitHub repository.

## License

MIT License
