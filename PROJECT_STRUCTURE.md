# Project Structure

This document outlines the complete structure of the zm-frappe-wix-sync Frappe app.

```
zm-frappe-wix-sync/
├── README.md                           # Main documentation
├── INSTALL.md                          # Installation guide
├── CHANGELOG.md                        # Version history
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
├── setup.py                            # Setup configuration
├── pyproject.toml                      # Modern Python packaging
├── MANIFEST.in                         # Package manifest
│
└── zm_frappe_wix_sync/                 # Main app directory
    ├── __init__.py                     # App version
    ├── hooks.py                        # Frappe hooks configuration
    ├── modules.txt                     # Module definition
    ├── patches.txt                     # Database patches
    │
    ├── api/                            # API modules
    │   ├── __init__.py
    │   └── wix_sync.py                 # Main Wix synchronization logic
    │
    ├── public/                         # Static assets
    │   ├── css/
    │   │   └── .gitkeep
    │   └── js/
    │       └── item_list.js            # Custom Item list view
    │
    ├── templates/                      # Jinja templates
    │   ├── __init__.py
    │   ├── includes/                   # Template includes
    │   └── pages/                      # Web pages
    │       └── __init__.py
    │
    └── zm_frappe_wix_sync/             # Module directory
        ├── __init__.py
        └── doctype/                    # DocType definitions
            ├── __init__.py
            ├── wix_sync_settings/      # Settings DocType
            │   ├── __init__.py
            │   ├── wix_sync_settings.json      # DocType definition
            │   ├── wix_sync_settings.py        # Controller
            │   └── wix_sync_settings.js        # Client script
            └── wix_sync_log/           # Log DocType
                ├── __init__.py
                ├── wix_sync_log.json   # DocType definition
                └── wix_sync_log.py     # Controller
```

## Key Components

### 1. Core Files
- **hooks.py**: Defines document events and includes custom JS
- **wix_sync.py**: Main synchronization logic and API integration
- **requirements.txt**: Python dependencies (frappe>=15.0.0, requests>=2.31.0)

### 2. DocTypes
- **Wix Sync Settings**: Single DocType for configuration
- **Wix Sync Log**: Tracks all synchronization attempts

### 3. API Integration
- Uses Wix Stores Catalog V3 API
- Endpoint: `POST https://www.wixapis.com/stores/v3/products`
- Supports kokofresh site ID: `a57521a4-3ecd-40b8-852c-462f2af558d2`

### 4. Features
- **Automatic Sync**: Items created in ERPNext automatically sync to Wix
- **Manual Sync**: Button in Item List for manual synchronization
- **Connection Testing**: Built-in API connectivity testing
- **Error Logging**: Complete audit trail of sync operations
- **Settings Management**: Easy configuration through Frappe interface

### 5. Hooks Configuration
```python
doc_events = {
    "Item": {
        "after_insert": "zm_frappe_wix_sync.api.wix_sync.sync_item_to_wix"
    }
}

doctype_list_js = {
    "Item": "public/js/item_list.js"
}
```

### 6. Installation Commands
```bash
# Get app
bench get-app https://github.com/macrobian88/zm-frappe-wix-sync.git

# Install on site
bench install-app zm_frappe_wix_sync --site your-site-name

# Restart
bench restart
```

## Development Notes

### POC Limitations
- One-way sync only (ERPNext → Wix)
- Product creation only (no updates/deletions)
- Physical products only
- Basic error handling

### Future Enhancements
- Bi-directional sync
- Product updates and deletions
- Digital product support
- Bulk sync operations
- Advanced error recovery
- Webhook integration
- Image sync support

### Technical Specifications
- **Framework**: Frappe Framework v15.x
- **API**: Wix Stores Catalog V3
- **Authentication**: Bearer token
- **Dependencies**: requests library for HTTP calls
- **Error Handling**: Try-catch with detailed logging
- **Data Format**: JSON payloads matching Wix API schema

## Usage Workflow

1. **Configuration**: Set API key and site ID in Wix Sync Settings
2. **Test Connection**: Verify API connectivity
3. **Create Items**: New ERPNext items automatically sync to Wix
4. **Monitor Logs**: Check Wix Sync Log for sync status
5. **Manual Sync**: Use Item List menu for existing items

This structure provides a solid foundation for ERPNext-Wix integration with room for future enhancements.
