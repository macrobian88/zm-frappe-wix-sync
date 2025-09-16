# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2025-09-16

### Fixed
- **Critical Bug Fix**: Fixed "Wix sync settings not found" error during test connection
  - Enhanced `get_wix_sync_settings()` function to auto-create Single DocType document if it doesn't exist
  - Improved test connection functionality with better error handling and validation
  - Fixed Single DocType document creation logic for new installations
  - Better error messages for missing API keys and site IDs

### Improved
- **Test Connection Feature**:
  - Changed to use less intrusive Wix API endpoint (site properties instead of creating test products)
  - Added comprehensive validation before testing connection
  - Improved client-side JavaScript with better error handling and user feedback
  - Added visual indicators for connection status on the form
  - Form now saves automatically before testing to ensure settings persist
  - Clear connection status when API key or site ID changes

### Technical
- Enhanced Single DocType handling in `get_wix_sync_settings()` function
- Added `test_connection()` method to `WixSyncSettings` DocType class
- Improved API error handling with specific HTTP status code responses
- Better logging for debugging Single DocType creation issues
- Enhanced client-side validation and user experience

## [0.0.2] - 2025-09-16

### Fixed
- **Critical Bug Fix**: Fixed "Name of Wix Sync Settings cannot be Wix Sync Settings" error
  - Removed conflicting `autoname` and `naming_rule` fields from Single DocType configuration
  - Single DocTypes now use proper Frappe naming conventions automatically
  - Added migration patch to handle existing installations with problematic document names
  - Made title field editable for better user experience

### Changed
- **Wix Sync Settings DocType**: 
  - Removed `autoname: "field:title"` configuration that caused naming conflicts
  - Removed `naming_rule: "By fieldname"` that was incompatible with Single DocTypes
  - Changed default title from "Wix Sync Settings" to "Wix Sync Configuration"
  - Made title field editable instead of read-only

### Technical
- Added migration patch `zm_frappe_wix_sync.patches.v1_0.fix_wix_sync_settings_naming`
- Improved Single DocType handling according to Frappe framework best practices
- Better error handling for existing installations during upgrade

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
- `GET https://www.wixapis.com/site-properties/v4/properties` - Test connection

### Configuration
- Default Wix Site ID configured for kokofresh: `a57521a4-3ecd-40b8-852c-462f2af558d2`
- Requires Wix API key with product creation permissions
- Settings managed through single DocType interface
