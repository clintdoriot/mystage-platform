# Event Sourcing Infrastructure Modernization

## Status
🟡 Planning / 🟢 Active (mixed)

## Description

Major infrastructure overhaul of the event-sourcing data pipeline to improve reliability, scalability, and maintainability.

## Affected Repositories

- **mystage-event-sourcing** (primary)
- **mystage-admin-interface** (tooling integration)
- **mystage-databases** (may need schema changes)

## Key Components

### 1. Convert Pub/Sub & Document Triggers to Cloud Tasks
**Why**: Better control, retry logic, and task management
**Status**: Planning

### 2. Convert Admin Directory to Cloud Functions
**Why**: Allow admin interface to trigger pipeline operations
**Status**: Planning
**Dependencies**: Admin pipeline tools

### 3. Infrastructure as Code (IaC)
**Components**:
- BigQuery setup for entity deduplication
- VM deployment for Facebook scraper (or Docker?)
**Status**: Planning

### 4. Custom Task Scheduler → Cloud Tasks
**Why**: Better integration with Cloud ecosystem, UI management
**Status**: Planning

### 5. Logfire Dashboard
**Why**: Catch service failures and monitoring
**Status**: Planning

### 6. Pydantic-AI Update
**Task**: Update to latest version, fix all pipeline errors
**Status**: Active

### 7. Testing Infrastructure
**Task**: Finish pydantic/deep evals, get all evals working fully
**Status**: Active

## Dependencies

- Admin Interface pipeline management tools (two-way dependency)
- Firestore schema updates
- BigQuery IaC setup

## Technical Decisions Needed

- Docker vs VM deployment for Facebook scraper
- IaC tool choice (Terraform, Pulumi, etc.)
- Migration strategy for existing triggers

## Estimated Effort

(To be determined after detailed analysis)

## Success Criteria

- All pub/sub triggers converted to Cloud Tasks
- Admin functions callable from admin interface
- IaC in place for all infrastructure
- Logfire dashboard operational
- All tests passing with latest pydantic-ai

## Notes

- This is foundational work that will make future improvements easier
- Some components are active, others need specs
- Large effort - consider phasing
