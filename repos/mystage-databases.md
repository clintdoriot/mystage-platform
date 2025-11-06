# MyStage Databases

## Overview

Central source of truth for database configuration and schema definitions across the platform. Currently manages Firestore; may include Postgres in the future.

## Current Contents

### Firestore
- **Security Rules** - Access control rules for all Firestore databases
- **Indexes** - Index definitions for query performance
- **Schema Definitions** (planned) - Formal schema documentation

## Databases

### Firestore: "scraping" database
- **Pipeline collections**: `urls`, `scrapes`, `extractions`, `entity_sources`, `scheduled_tasks`, `url_images`
- **Entity collections**: `evt_venues`, `evt_artists`, `evt_performances`
- **Supporting collections**: `venue_duplicates`

### Firestore: Additional databases
- User-generated content and application data
- Admin data (admin_users, audit_logs, etc.)

## Future Plans

- **Schema validation models**: Pydantic (Python) and Zod (TypeScript) models
- **Comprehensive schema documentation**: Definitive source of truth for all database schemas
- **CI/CD**: Automated deployment and validation
- **Postgres** (if needed): Schema, migrations, models for Postgres databases (e.g., NFT system)

## Related Repositories

All repositories depend on database schemas:
- **mystage-event-sourcing** - Primary writer to Firestore databases
- **mystage-admin-interface** - Reads and writes across all databases
- **mystage-app** - Reads production data
- **mystage-app-backend** - Reads and writes for app functionality
- **mystage-ff-fanex** - Reads and writes live performance data
- **mystage-ff-pro-dashboard** - Reads and writes artist/venue data

## Current Status

Active. Contains deployed Firestore rules and indexes. Schema documentation and validation models need to be added.

## Deployment

- Firestore rules and indexes are deployed to GCP/Firebase project
- Future: Postgres migrations and schema deployment

## Notes

- This is a deployed infrastructure repo (not just documentation)
- Changes here affect production databases
- Cross-cutting by nature - all projects depend on these schemas
- Single source of truth for all database structures across the platform
