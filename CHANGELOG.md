# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Same Python and Frappe version requirements as v2.0.x

---

## Support

If you encounter any issues after upgrading:

1. **Check Connection**: Use the connection test function
2. **Review Logs**: Check Wix Sync Log entries for detailed error info  
3. **Manual Sync**: Try manually syncing a single item first
4. **Site ID**: Ensure your site ID is correct in settings

For technical support, create an issue with:
- Your Frappe version
- Error messages from sync logs
- Connection test results
