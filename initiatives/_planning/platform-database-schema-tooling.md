# Database Schema & Tooling

## Status
🟡 Planning

## Description

Add comprehensive documentation, tooling, and CI/CD to the mystage-databases repository for all database schemas (Firestore and potentially Postgres).

## Affected Repositories

- **mystage-databases** (primary)
- All repos that use databases (for schema awareness)

## Key Components

### 1. Schema Documentation
**Purpose**: Definitive source of truth for all database schemas
**Contents**:
- All collections/tables and their structure
- Field types and validation rules
- Indexes and their purpose
- Relationships between collections/tables
- Data migration history

**Databases**:
- Firestore collections (urls, scrapes, extractions, evt_venues, evt_artists, evt_performances, etc.)
- Postgres tables (if/when added for NFT system or other features)

### 2. Schema Validation
**Future**: Pydantic models (Python) and Zod schemas (TypeScript)
**Purpose**: Runtime validation, type safety, code generation
**Supports**: Both Firestore and Postgres schemas

### 3. Tooling
**Additions**:
- Schema linting
- Migration tools (Firestore and Postgres)
- Documentation generation
- Validation scripts

### 4. CI/CD Pipeline
**Capabilities**:
- Automated deployment of Firestore rules and indexes
- Automated deployment of Postgres migrations
- Schema validation on PRs
- Documentation publishing
- Breaking change detection

## Benefits

- Single source of truth for all database structures
- Type safety across all projects
- Automated deployment
- Easier onboarding for developers
- Catch schema issues early

## Technical Components

**Firestore**:
- Security rules
- Index definitions
- Schema documentation (Markdown, JSON schema)
- Deployment scripts

**Postgres** (future):
- Migration files (Alembic, Flyway, etc.)
- Schema DDL
- Connection configuration

**Shared**:
- Pydantic/Zod models
- CI/CD (GitHub Actions)
- Validation tooling
- Code generation

## Dependencies

- Need to audit current Firestore schema comprehensively
- CI/CD infrastructure setup
- Decision on Postgres (NFT architecture)

## Estimated Effort

Firestore schema documentation: 2-3 weeks
CI/CD setup: 1 week
Tooling development: 1-2 weeks
Pydantic/Zod generation: 2-3 weeks (future)
Postgres setup (if needed): 1-2 weeks

## Success Criteria

- Complete schema documentation exists for all databases
- Rules and indexes deploy automatically (Firestore)
- Migrations deploy automatically (Postgres, if added)
- Breaking changes caught in PR review
- Developers can easily understand all database structures
- Type-safe database access (with code generation)

## Priority

Medium-High - Foundation for data consistency

## Phasing

**Phase 1**: Firestore documentation and CI/CD
**Phase 2**: Schema validation tooling
**Phase 3**: Code generation (Pydantic, Zod)
**Phase 4**: Postgres integration (if NFT proceeds)

## Notes

- This makes databases repo truly the "source of truth" for ALL database schemas
- Benefits all projects across the platform
- Future-proof for adding Postgres or other databases
- Consider tools like firebase-schema-generator for Firestore
- Consider Alembic or Flyway for Postgres migrations
