# Entity Deduplication System

## Status
🟡 Planning / 🟢 Active (mixed)

## Description

Comprehensive system to identify and merge duplicate entities (venues, artists, performances) across multiple data sources. Critical for data quality.

## Affected Repositories

- **mystage-event-sourcing** (deduplication logic, BigQuery integration)
- **mystage-admin-interface** (merge UI and tools)
- **mystage-databases** (entity data, merge operations)

## Key Components

### 1. BigQuery-Based Entity Deduplication
**Tasks**:
- Document the deduplication approach
- Test BigQuery deduplication queries
- Set up IaC for BigQuery infrastructure
**Status**: 🟡 Planning
**Why**: BigQuery provides powerful matching capabilities at scale

### 2. Backend Merge Functions
**Tasks**:
- Finalize backend functions to merge entities
- Handle all edge cases (references, relationships, etc.)
- Ensure data integrity during merge
**Status**: Active
**Reference**: See `venue-merge-issue-order.txt` in `/Users/clint/Projects/mystage`

### 3. Admin UI for Entity Merging
**Tasks**:
- Finish entity merging tools in admin interface
- Add support for modifying entity data
- Review and approve suggested matches
**Status**: 🟡 Planning
**Dependencies**: Backend merge functions

### 4. Multi-Stage Entity Resolution & Data Enrichment
**Description**: Iterative (possibly agentic) approach to:
- Match data with existing entities first (avoid costly enrichment)
- Only enrich when necessary to improve entity resolution
- May require multiple passes
**Status**: 🟡 Planning
**Why**: Enrichment is expensive - optimize by matching first

## Dependencies

- BigQuery IaC setup
- Admin interface merge UI
- Data enrichment pipeline (for new entities)
- Firestore schema for tracking merge operations

## Technical Challenges

- Matching accuracy (false positives vs false negatives)
- Handling conflicts during merge (which data to keep?)
- Maintaining referential integrity
- Performance at scale
- Cost optimization (BigQuery queries, API enrichment calls)

## Estimated Effort

BigQuery setup & documentation: (TBD)
Backend merge functions: (Active - needs completion estimate)
Admin UI: (TBD - depends on backend completion)
Multi-stage resolution: (TBD - complex, may be later phase)

## Success Criteria

- BigQuery deduplication system operational
- Admin team can review and merge duplicates via UI
- Merge operations maintain data integrity
- Reduced duplicate entities in production
- Cost-effective enrichment strategy

## Reference Documents

- `/Users/clint/Projects/mystage/venue-merge-issue-order.txt`

## Notes

- This is critical for data quality
- Affects user experience (seeing duplicate venues/artists)
- Multi-stage resolution is advanced feature - may phase after basic merge
- Need to balance automation with human review
