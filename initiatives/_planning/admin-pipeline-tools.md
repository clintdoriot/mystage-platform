# Admin Interface: Pipeline Management Tools

## Status
🟡 Planning / 🟢 Active (mixed)

## Description

Build comprehensive admin tools to manage and monitor the event-sourcing data pipeline.

## Affected Repositories

- **mystage-admin-interface** (UI and frontend functions)
- **mystage-event-sourcing** (backend functions to be called)
- **mystage-databases** (pipeline data storage)

## Key Components

### 1. Entity Merging Tools
**Status**: 🟢 Active - Finish implementation
**Purpose**: Allow admin team to review and merge duplicate entities

### 2. Entity Data Modification
**Status**: 🟡 Planning
**Purpose**: Edit entity data directly when scraping/extraction fails

### 3. Pipeline Data Tables
**Status**: 🟡 Planning
**Tables needed**:
- URLs (sources being scraped)
- Scrapes (raw scrape data)
- Extractions (extracted structured data)
- Entity sources (mapping entities to sources)
- URL images (image processing pipeline)

### 4. Infrastructure Management
**Status**: 🟡 Planning
**Tools needed**:
- Proxy list management
- FB scrape credentials management

### 5. Task Scheduling Tools
**Status**: 🟡 Planning
**Purpose**: Manage scheduled scraping tasks
**Dependencies**: Event-sourcing Cloud Tasks migration

## Dependencies

- Event-sourcing: Convert admin functions to Cloud Functions (callable from admin UI)
- Event-sourcing: Cloud Tasks migration
- Entity deduplication: Merge backend functions
- Firestore: Schema for pipeline data

## User Stories

As an admin, I need to:
- See all URLs being scraped and their status
- View raw scrape data and extractions for debugging
- Manually trigger scraping for specific URLs
- Edit entity data when automated extraction is wrong
- Manage proxy rotation for scraping
- Add/remove Facebook credentials
- Review and merge duplicate entities
- Monitor scraping task schedule

## Estimated Effort

Entity merging: (Active - needs completion estimate)
Data tables: (TBD)
Infrastructure tools: (TBD)
Task management: (TBD - depends on Cloud Tasks migration)

## Success Criteria

- Admin team can fully manage pipeline without touching code
- Visibility into all pipeline stages
- Can debug scraping issues through UI
- Can manually correct data quality issues
- Reduced time to resolve pipeline problems

## Priority

High - Admin team currently lacks tools to manage pipeline effectively

## Notes

- This unlocks admin team productivity
- Two-way dependency with event-sourcing infrastructure work
- Start with most painful gaps (entity merging, URL management)
