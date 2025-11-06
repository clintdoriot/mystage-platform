# MyStage Admin API (Deprecated)

## Status
⚠️ **DEPRECATED** - Migrate to mystage-admin-interface

## Overview

Legacy repository for admin-related backend functions. Never fully utilized in production. Being replaced by the more comprehensive mystage-admin-interface monorepo which includes both frontend and backend.

## Why Deprecated

- **Limited functionality**: Only partially implemented admin functions
- **Better alternative**: mystage-admin-interface provides complete admin solution (frontend + backend)
- **Architectural evolution**: Moved to monorepo pattern for better admin tool organization
- **Maintenance burden**: Reduces number of repositories to maintain

## Current Contents

### Potentially Useful Services
- **Geolocation services** - May contain location-based functionality worth migrating
- Some admin utility functions

### What Not to Use
- Authentication/authorization patterns (use mystage-admin-interface RBAC instead)
- Database access patterns (use mystage-admin-interface multi-database approach)
- API structure (use mystage-admin-interface backend functions)

## Technology Stack

- **Backend**: Python + Firebase Functions
- **Database**: Firestore (likely single database, not multi-database approach)
- **Authentication**: Firebase Auth (older patterns)

## Migration Path

### To: mystage-admin-interface

**What to migrate:**
1. **Geolocation services** - Evaluate and port useful geolocation functionality
2. **Utility functions** - Review for any reusable admin utilities
3. **Business logic** - Extract any valuable admin-specific logic

**What NOT to migrate:**
- Infrastructure/deployment patterns (use new monorepo structure)
- Authentication/authorization (use new RBAC system)
- Database access (use new multi-database approach)

**Migration process:**
1. Audit mystage-admin-api for valuable functionality
2. Identify geolocation services and utilities to preserve
3. Reimplement in mystage-admin-interface following new patterns:
   - Place in `functions/admin-api/` (for backend)
   - Follow RBAC patterns
   - Use multi-database connections
4. Test thoroughly in mystage-admin-interface
5. Archive mystage-admin-api repository

## Related Repositories

- **mystage-admin-interface** - Replacement repository (monorepo with frontend + backend)
- **mystage-event-sourcing** - May have some overlapping admin functions
- **mystage-app-backend** - Another backend functions repo (separate from admin)

## Deployment

**Status**: No longer deployed
**Previous deployment**: GCP/Firebase project (likely same project as other functions)

## Integration Points

### Historical Integrations
- Firestore (admin database or shared databases)
- Firebase Auth
- Possibly called from admin interfaces or internal tools

### Current State
- Not integrated with current admin-interface
- Functions likely not in use
- May have been used for one-off admin tasks

## Notes

- **Archive candidate**: Once geolocation services are evaluated/migrated, this repo can be archived
- **Low priority**: Migration is not urgent unless specific functionality is needed
- **Reference only**: Good to keep for historical context, but don't base new work on it
- **Audit first**: Before archiving, thoroughly audit for any hidden valuable functionality

## Recommendations

1. **Short-term**: Leave as-is, reference only
2. **Audit phase**: Create initiative to audit geolocation services and utilities
3. **Migration phase**: Extract valuable functionality to mystage-admin-interface
4. **Archive phase**: Once valuable functionality extracted, archive the repository

## Migration Initiative

See: `initiatives/_planning/admin-api-migration.md` (if created)

This would be a small initiative to:
- Audit mystage-admin-api for valuable services (especially geolocation)
- Migrate useful functionality to mystage-admin-interface
- Archive mystage-admin-api repository
- Estimated effort: S-M (1-3 weeks)
