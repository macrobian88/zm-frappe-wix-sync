# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2024-01-01

### Added
- Initial release of ZM Frappe Wix Sync
- Automatic ERPNext Item to Wix Product synchronization
- Wix Sync Settings DocType for configuration management
- Wix Sync Log DocType for tracking sync operations
- Support for Wix Stores Catalog V3 API
- Manual sync functionality from Item List view
- Connection testing functionality
- Comprehensive error handling and logging
- POC implementation focusing on product creation only

### Features
- **Automatic Sync**: Items created in ERPNext automatically sync to Wix
- **Manual Sync**: Option to manually sync existing items
- **Settings Management**: Easy configuration through Frappe interface
- **Logging**: Complete audit trail of all sync operations
- **Error Handling**: Robust error handling with detailed error messages
- **Test Connection**: Built-in connection testing to verify API setup

### Technical Details
- Compatible with Frappe Framework v15.x
- Uses Wix Stores Catalog V3 API endpoints
- Implements document event hooks for real-time sync
- Includes client-side JavaScript for enhanced UX
- Follows Frappe app development best practices

### Known Limitations
- One-way sync only (ERPNext → Wix)
- Product creation only (no updates or deletions)
- Limited to physical products
- POC version with basic feature set

### API Endpoints Used
- `POST https://www.wixapis.com/stores/v3/products` - Create products in Wix

### Configuration
- Default Wix Site ID configured for kokofresh: `a57521a4-3ecd-40b8-852c-462f2af558d2`
- Requires Wix API key with product creation permissions
- Settings managed through single DocType interface
