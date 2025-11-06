# Initiative Dependencies Map

## Overview

This document maps dependencies between initiatives to help with prioritization and planning.

## Critical Blocking Dependencies

### NFT Architecture Decision Blocks Everything NFT-Related

The **[NFT Architecture Decision](../initiatives/nft-architecture.md)** (Firestore vs Postgres) is a critical blocking dependency for:

- ❌ [NFT Backend & APIs](../initiatives/nft-backend.md)
- ❌ [NFT Admin Tools](../initiatives/nft-admin.md)
- ❌ [NFT Security & Minting](../initiatives/nft-security.md)
- ⚠️ [Profile Onboarding](../initiatives/profile-onboarding.md) (NFT creator workflows)
- ⚠️ [Admin Data Management](../initiatives/admin-data-management.md) (NFT management)

**Impact**: All NFT work is stalled until this decision is made.

### Event Sourcing Infrastructure ↔ Admin Pipeline Tools

Two-way dependency between:
- **[Event Sourcing Infrastructure](../initiatives/event-sourcing-infrastructure.md)** needs to convert admin functions to Cloud Functions
- **[Admin Pipeline Tools](../initiatives/admin-pipeline-tools.md)** needs those functions to be callable from UI

**Resolution**: Need to coordinate these initiatives or sequence them properly.

## Dependency Chains

### Entity Management Chain

```
Entity Deduplication
    ↓ (provides merge functions)
Admin Pipeline Tools (merge UI)
    ↓ (provides feedback)
Extraction Improvements
    ↓ (better extraction reduces duplicates)
Entity Deduplication
```

This is a cycle - they reinforce each other.

### Data Quality Chain

```
Event Sourcing Infrastructure
    ↓ (provides reliable pipeline)
Pipeline Optimization
    ↓ (faster processing)
Data Enrichment
    ↓ (complete data)
Entity Deduplication
    ↓ (clean data)
User-Facing Apps (better UX)
```

### Profile Management Chain

```
Profile Claim Management
    ↓ (enables claiming)
Profile Onboarding
    ↓ (specialized workflows)
NFT Architecture Decision
    ↓ (enables NFT features)
NFT Backend & Admin
    ↓ (sticker creation)
Profile Onboarding (NFT creators)
```

### Payment & Monetization Chain

```
Stripe Integration Fix
    ↓ (enables payments)
NFT System
    ↓ (NFT purchases)
Profile Onboarding (verified creators)
```

## Cross-Cutting Dependencies

### Notification System

**Depends on**:
- Firestore schema definition
- Backend infrastructure
- Integration points in all apps

**Blocks** (or makes better):
- Chat integration (chat notifications)
- Profile claim management (approval notifications)
- Admin content moderation (moderation notifications)
- Any user-facing feature that needs notifications

### Chat Integration

**Depends on**:
- Backend chat service (exists or needs building?)
- Notification system integration
- Firestore schema

**Enables**:
- Pro dashboard features
- Admin support capabilities
- Content moderation needs

### Firestore Schema & Tooling

**Affects**:
- Literally every other initiative
- Foundation for all database work

**Provides**:
- Schema documentation
- Type safety
- Deployment automation

### Admin Roles & Access Control

**Enables**:
- All admin interface features
- Secure access to tools
- Content moderation
- Developer onboarding

## Repository-Level Dependencies

### mystage-databases

**Consumed by**: All projects
**Provides**: Database structure and rules
**Blocks**: Any feature requiring new schema

### mystage-event-sourcing

**Consumes**: Firestore schemas
**Provides**: Core data (events, artists, venues)
**Blocks**: User-facing apps (without data, they're empty)

### mystage-admin-interface

**Consumes**: Event-sourcing functions, Firestore data
**Provides**: Data management capabilities
**Enables**: Manual data correction, admin operations

### mystage-app-backend

**Status**: Unclear boundaries
**Needs**: Consolidation decision or better organization
**Affects**: All user-facing apps

## Priority Implications

### Must Do First (Unblock Others)

1. **NFT Architecture Decision** - Blocks entire NFT feature set
2. **Firestore Schema Documentation** - Needed by everything
3. **Event Sourcing Infrastructure** - Foundation for pipeline work
4. **Admin Roles & Access** - Needed before rolling out admin tools
5. **Stripe Integration Fix** - Revenue blocker

### High Value (Impact Multiple Areas)

1. **Notification System** - Affects user engagement across all apps
2. **Entity Deduplication** - Critical data quality issue
3. **Admin Pipeline Tools** - Unlocks admin team productivity
4. **Pipeline Optimization** - Cost and performance improvements

### Can Wait / Lower Priority

1. **Dynamic Scraping** - Nice to have, not critical
2. **NFT System** (entire thing) - Experimental, market unclear
3. **Exchange NFTs** - Depends on NFT decision + validation

## Suggested Sequencing

### Phase 1: Foundation (Unblock Others)
1. Firestore schema documentation
2. Admin roles & access control
3. Stripe integration fix
4. Event sourcing infrastructure (Cloud Tasks, IaC)

### Phase 2: Core Features (High Value)
1. Entity deduplication system
2. Admin pipeline tools
3. Notification system (basic)
4. Pipeline optimization

### Phase 3: Refinement
1. Extraction improvements (ongoing)
2. Data enrichment
3. Profile claim completion
4. Chat integration

### Phase 4: Advanced Features (After Validation)
1. NFT architecture decision
2. NFT implementation (if proceeding)
3. Dynamic scraping
4. Profile onboarding enhancements

## Decision Points

### Critical Decisions Needed

1. **NFT: Firestore vs Postgres?** - Blocks all NFT work
2. **App Backend: Consolidate or keep separate?** - Affects architecture
3. **NFT: Proceed or pivot?** - Market validation needed
4. **Facebook Scraper: Docker vs VM?** - Affects deployment

### Nice-to-Have Decisions

1. Chat system: Build new or integrate existing?
2. Notification system: Third-party or custom?
3. Dynamic scraping: Pursue or defer?

## Notes

- Many initiatives have circular dependencies (improvement cycles)
- Cross-cutting features (notifications, chat) affect prioritization
- Some "in-flight" PRs should be completed quickly (low hanging fruit)
- Foundation work (Firestore, infrastructure) unlocks many other initiatives
