# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-01-16

### 🔑 MAJOR FIX: Wix API Key Length Limit Resolved

This release resolves the critical character limit issue preventing users from entering long Wix API keys.

### ✅ **API Key Length Issues Fixed**
- **FIXED**: Removed 140-character limit on `wix_api_key` field
- **UPDATED**: Field type changed from `Password` to `Long Text` (supports 1000+ characters)
- **FIXED**: IST token truncation issues (tokens can be 700+ characters)
- **NEW**: Automatic database migration for existing installations
- **IMPROVED**: Field description updated to clarify long token support

### 🔄 **Database Migration Features**
- **NEW**: Automatic field type migration patch (`migrate_wix_api_key_field.py`)
- **NEW**: Seamless upgrade from Password to Long Text field type
- **NEW**: Database schema update from VARCHAR(140) to TEXT
- **PRESERVED**: Existing API key values maintained during migration
- **AUTOMATED**: Migration runs automatically on `bench migrate`

### 🛠️ **Technical Improvements**
- **UPDATED**: DocType JSON field definition for `wix_api_key`
- **NEW**: Database migration patch with comprehensive error handling
- **IMPROVED**: Field description with IST token information
- **ENHANCED**: Support for tokens up to 1000+ characters

### 📚 **Documentation Updates**
- **UPDATED**: README with API key length fix information
- **NEW**: Migration guide for existing installations
- **NEW**: Troubleshooting section for character limit issues
- **IMPROVED**: Installation instructions with IST token notes

### 🔗 **Backward Compatibility**
- **MAINTAINED**: All existing functionality preserved
- **MAINTAINED**: Existing API keys automatically migrated
- **MAINTAINED**: No configuration changes required
- **SEAMLESS**: Zero-downtime upgrade path

## [2.1.0] - 2025-09-16

### 🔧 MAJOR FIX: Complete Authentication and Sync Overhaul

This release resolves critical authentication issues and implements a robust, production-ready sync system.

### ✅ **Authentication Issues Resolved**
- **FIXED**: Updated to correct site ID: `63a7b738-6d1c-447a-849a-fab973366a06` (Dev Sitex1077548723)  
- **FIXED**: JWT token authentication format now properly handled
- **FIXED**: Updated API endpoints to working Catalog V3 format (`/stores-catalog/v3/`)
- **FIXED**: Resolved Wix Stores app installation requirement (auto-installed via API)
- **FIXED**: Eliminated all "invalid_grant" and 404 authentication errors

### 🚀 **Sync System Improvements**
- **NEW**: Implemented robust `WixSyncManager` class for centralized sync operations
- **NEW**: Enhanced error handling with detailed logging and user feedback
- **FIXED**: Sync log field validation issues (mapped status values correctly)
- **NEW**: Enhanced product data structure optimized for Wix API v3
- **NEW**: Automatic stock quantity and price synchronization
- **NEW**: Support for product weight and SKU mapping

### 🔄 **API Integration Updates**
- **UPDATED**: Switched to working Wix Stores Catalog V3 endpoints
- **IMPROVED**: Authentication headers optimized for JWT tokens
- **NEW**: Comprehensive timeout and error handling (30s timeouts)
- **NEW**: Enhanced connection testing with detailed status reporting
- **NEW**: Automatic retry logic for failed syncs

### ⚡ **Automation Features**
- **NEW**: Automatic sync on item creation (`after_insert` hook)
- **NEW**: Automatic sync on item updates (`on_update` hook)
- **NEW**: Scheduled hourly background sync job to catch missed items
- **NEW**: Manual sync functions for individual and bulk operations

### 🔗 **Backward Compatibility**
- **MAINTAINED**: All existing function signatures preserved  
- **MAINTAINED**: Legacy hooks continue to work seamlessly
- **MAINTAINED**: Seamless upgrade path for existing installations
- **NEW**: Legacy function wrappers for smooth migration

### 🛠️ **Developer Experience**
- **NEW**: Comprehensive error messages and troubleshooting info
- **NEW**: Detailed sync logging with timestamps and error details  
- **NEW**: Connection testing utilities for debugging
- **NEW**: Manual sync operations accessible via API
- **IMPROVED**: Code documentation and inline comments

### 📊 **Monitoring & Logging**
- **NEW**: Enhanced sync log creation with proper status mapping
- **NEW**: Connection status tracking with timestamps
- **NEW**: Failed sync retry mechanism via scheduled jobs
- **NEW**: Success/error count reporting for bulk operations

## [2.0.0] - 2024-XX-XX

### Added
- Initial Wix sync functionality
- Basic authentication with API keys
- Item to product mapping
- Sync logging system

### Fixed  
- Basic connectivity issues
- Initial authentication setup

## [1.0.0] - 2024-XX-XX

### Added
- Initial project setup
- Basic Frappe app structure
- DocType definitions for sync configuration

---

## Migration Guide

### From v2.1.x to v2.2.0

1. **Update to Latest Version:**
   ```bash
   bench get-app --branch main https://github.com/macrobian88/zm-frappe-wix-sync.git
   ```

2. **Run Database Migration:**
   ```bash
   bench --site [your-site] migrate
   ```

3. **Restart Services:**
   ```bash
   bench restart
   ```

4. **Re-enter API Key (if needed):**
   - If you previously couldn't enter your full API key due to character limits
   - Go to Wix Sync Settings and paste your complete IST token
   - The field now supports 1000+ characters

5. **Verify Migration:**
   - Check that your existing API key is still present
   - Test connection to ensure everything works
   - Long IST tokens should now be fully supported

### From v2.0.x to v2.1.0

1. **Update API Configuration:**
   - Your site ID will be automatically updated to the correct value
   - No action required if using the latest API key format

2. **Sync Log Field Fix:**
   - If you encounter sync status validation errors, update the "Sync Status" field options in Customize Form
   - Change from: `Success\nFailed\nError` 
   - To: `Success`, `Failed`, `Error` (separate lines)

3. **Enhanced Features:**
   - Scheduled sync will automatically start working after update
   - No configuration changes required
   - All existing items will be re-synced automatically

4. **Testing:**
   - Use the `test_wix_connection()` function to verify the fix worked
   - Monitor sync logs for successful operations

### Breaking Changes
- None - fully backward compatible

### Dependencies
- No new dependencies added
- Same Python and Frappe version requirements as previous versions

---

## Support

If you encounter any issues after upgrading:

1. **Check Connection**: Use the connection test function
2. **Review Logs**: Check Wix Sync Log entries for detailed error info  
3. **Manual Sync**: Try manually syncing a single item first
4. **Site ID**: Ensure your site ID is correct in settings
5. **API Key Length**: Ensure your full API key is entered (IST tokens can be 700+ chars)

For technical support, create an issue with:
- Your Frappe version
- Error messages from sync logs
- Connection test results
- API key length and format
