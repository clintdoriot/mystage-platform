# MyStage Admin Interface

## Overview

Multi-tenant admin interface for managing data across multiple Firebase databases, Algolia indices, and environments. Internal tool with role-based access control for technical and non-technical administrators.

## Architecture

**Monorepo** with npm workspaces containing:
- **Frontend**: React 19 + TypeScript 5 + Vite + MUI (layered hybrid architecture)
- **Backend**: Python 3.12 Firebase Functions (future - admin-api, jobs, shared)

## Technology Stack

### Frontend
- **Framework**: React 19 + TypeScript 5
- **Build**: Vite
- **UI**: MUI Core + MUI X DataGrid
- **State**: TanStack Query (data fetching/caching)
- **Routing**: React Router v6
- **Testing**: Vitest (unit) + Playwright (E2E)
- **Auth**: Firebase Auth with multi-tenancy

### Backend
- **Language**: Python 3.12
- **Package Management**: uv
- **Deployment**: Firebase Functions (planned)
- **Services**: admin-api (privileged ops), jobs (background tasks)

## Frontend Architecture

**Layered hybrid architecture** with unidirectional dependency flow:

```
pages → features → entities → shared
```

**Layers:**
- **app/** - Application shell (guards, layout, providers, theme, routing)
- **pages/** - Route components (thin, coordinate features)
- **features/** - Page workflows (composable building blocks)
- **entities/** - Domain objects (venues, artists, performances, extractions, sources, scrapes)
- **shared/** - Domain-agnostic infrastructure (UI components, hooks, utils, API clients)

## Purpose

### Core Workflows
1. **Data Corrections** - Fix incorrect entity data (venues, artists, performances)
2. **Source Management** - View/manage data pipeline sources
3. **Duplicate Management** - Merge duplicate entities, separate bad merges
4. **User Support** - Respond to user feedback and messages
5. **Data Seeding** - Seed dev environments with production data

### RBAC Roles
- **Customer Support** - User account and feedback management (prod only)
- **Data Admin** - Entity and pipeline data management (prod only)
- **Developer** - Full access to dev environments
- **Super Admin** - Full access to all environments

## Database Access

### Per-Environment Connections
- **Main application database** - Entity data (artists, venues, performances, users, profiles)
- **Data pipeline database** - Pipeline data (urls, scrapes, extractions, entity_sources, scheduled_tasks)
- **Admin database** - Admin data (admin_users, audit_logs, admin_sessions, privileged_operations)

### Environment Isolation
- Separate deployments per environment (admin-dev, admin-prod)
- Each deployment connects to its environment's databases
- Complete isolation via URLs, configs, and service accounts

## Integration Points

**Reads/writes:**
- Firestore (3 databases per environment: main, pipeline, admin)
- Algolia (multiple indices: cities, performances, artists, venues, users, profiles)

**Consumes:**
- **mystage-event-sourcing** - Pipeline data (urls, scrapes, extractions, entity_sources)
- **mystage-databases** - Database rules and schema definitions

**May call:**
- Event-sourcing functions (trigger operations)
- App-backend functions (shared operations)

**Used by:**
- Internal admin team (data quality, corrections, user support)

## Documentation

**Comprehensive docs in repo:**
- `docs/README.md` - Documentation index
- `docs/architecture.md` - Frontend layered architecture
- `docs/spec.md` - Full project specification
- `docs/panel-stack-system.md` - Drill-down navigation system
- `docs/index-*.md` - Code discovery indexes (pages, features, entities, shared-ui, hooks, utils)
- `docs/testing.md` - Testing strategy
- `.claude/CLAUDE.md` - Development instructions

**See repo for implementation details** - the admin-interface repo has extensive documentation about frontend architecture, development patterns, and workflows.

## Current Status

Active development. Well-documented with layered architecture patterns and Claude tooling (commands, agents, documentation agents).

## Key Features

- **Multi-tenant auth** - Firebase Identity Platform multi-tenancy
- **RBAC** - Role-based access control with custom claims
- **Audit logging** - Comprehensive audit trail of admin actions
- **Panel stack system** - Global drill-down navigation for related data
- **Server DataGrid** - Efficient server-side data grid with filtering/sorting
- **Environment switching** - Safe data access across dev/prod environments
