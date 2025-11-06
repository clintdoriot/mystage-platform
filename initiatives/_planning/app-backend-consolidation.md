# App Backend Consolidation

## Status
🟡 Planning - Decision needed

## Description

Consider merging mystage-app-backend into mystage-admin-interface (or another repo) to consolidate backend functions.

## Affected Repositories

- **mystage-app-backend** (might be merged)
- **mystage-admin-interface** (potential target)
- All consuming apps (need to update references)

## Problem Statement

mystage-app-backend is described as "random backend functions" which suggests:
- Unclear boundaries with other backend repos
- Possible duplication with admin-interface or event-sourcing
- Maintenance overhead of separate repo
- Unclear ownership

## Options

### Option 1: Merge into Admin Interface
**Pros**:
- Consolidate similar monorepo structure
- Shared tooling and deployment
- Clearer organization

**Cons**:
- Admin interface might not be the right home
- Functions serve different purposes
- Larger monorepo to manage

### Option 2: Merge into Event Sourcing
**Pros**:
- Functions might be pipeline-related
- GCP project consolidation

**Cons**:
- Event sourcing is already large
- May mix concerns

### Option 3: Keep Separate
**Pros**:
- Clear separation
- Independent deployment

**Cons**:
- "Random functions" suggests poor organization
- Maintenance overhead

### Option 4: Reorganize Functions
- Move functions to their proper homes
- Deprecate app-backend repo
- Each function goes where it belongs

## Dependencies

Need to audit:
1. What functions exist in app-backend?
2. What are they used for?
3. Where should they logically live?
4. Are there duplicates with other repos?

## Effort Estimate

Audit: 2-3 days
Decision and planning: 1-2 days
Migration: 1-3 weeks (depends on decision)
Testing and deployment: 1 week
Documentation: 3-5 days

## Success Criteria

- Clear organization of backend functions
- Reduced maintenance overhead
- Better developer experience
- No service disruption

## Priority

Medium - Important for long-term maintainability

## Next Steps

1. Audit app-backend functions
2. Map functions to their purpose and consumers
3. Decide on organization strategy
4. Create migration plan if consolidating
5. Add documentation and tooling regardless of decision

## Notes

- This is an architectural decision that affects all projects
- Don't rush - get it right
- May reveal need for better function organization across all repos
