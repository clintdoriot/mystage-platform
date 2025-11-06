# MyStage Platform Initiatives

## Overview

This directory contains documentation for all active and planned initiatives across the MyStage platform. Initiatives are organized by primary focus area but many have cross-cutting concerns.

## Workflow

Initiatives move through three stages:

### 1. Planning (`_planning/`)
New initiatives start here during the planning phase. These are being:
- Scoped and defined (via `/initiative-brainstorm`)
- Implementation planned (via `/initiative-plan`)
- Estimated for effort
- Analyzed for dependencies
- Prioritized against other work

Files stay in `_planning/` until issues are created:
- `_planning/[initiative-name].md` - Initiative specification
- `_planning/[initiative-name]-plan.md` - Implementation plan

### 2. Active (`<initiative-name>/`)
Once issues are created (via `/initiative-create-issues`), the initiative moves to its own subdirectory:
- Files moved: `_planning/[name].md` and `_planning/[name]-plan.md` → `initiatives/[name]/`
- New file created: `initiatives/[name]/issues.md` - Issue tracking document
- GitHub milestone created in appropriate repository
- Initiative marked as "Active"

Example: `initiatives/entity-deduplication/`
- `entity-deduplication.md` - Spec
- `entity-deduplication-plan.md` - Implementation plan
- `issues.md` - Issue tracking

### 3. Complete (`_complete/`)
When an initiative is shipped to production and closed, the entire subdirectory moves to `_complete/`:
- `initiatives/[name]/` → `initiatives/_complete/[name]/`
- Preserves all history and tracking documents

**Note**: All initiatives below are currently in the planning phase (`_planning/`).

## Initiative Categories

### Infrastructure & Technical Debt
- [Event Sourcing Infrastructure Modernization](_planning/event-sourcing-infrastructure.md)
- [App Backend Consolidation](_planning/app-backend-consolidation.md)
- [Database Schema & Tooling](_planning/database-schema-tooling.md)

### Data Pipeline & Quality
- [Facebook Scraper Finalization](_planning/facebook-scraper.md)
- [Entity Deduplication System](_planning/entity-deduplication.md)
- [Data Enrichment Pipeline](_planning/data-enrichment.md)
- [Dynamic Scraping System](_planning/dynamic-scraping.md)
- [Extraction Improvements](_planning/extraction-improvements.md)
- [Pipeline Performance Optimization](_planning/pipeline-optimization.md)

### Admin & Internal Tools
- [Admin Interface: Roles & Access Control](_planning/admin-roles-access.md)
- [Admin Interface: Pipeline Management Tools](_planning/admin-pipeline-tools.md)
- [Admin Interface: Content Moderation](_planning/admin-content-moderation.md)
- [Admin Interface: Data Management](_planning/admin-data-management.md)

### User-Facing Features
- [Comprehensive Notification System](_planning/notification-system.md)
- [Chat System Integration](_planning/chat-integration.md)
- [Stripe Payment Integration Fix](_planning/stripe-integration.md)
- [Profile Onboarding Workflows](_planning/profile-onboarding.md)

### NFT Sticker Exchange
- [NFT Exchange: Architecture & Design](_planning/nft-architecture.md)
- [NFT Exchange: Backend & APIs](_planning/nft-backend.md)
- [NFT Exchange: Admin Tools](_planning/nft-admin.md)
- [NFT Exchange: Security & Minting](_planning/nft-security.md)

### Platform & Process
- [Platform Documentation & Planning](_planning/platform-planning.md) *(current initiative)*
- [Developer Onboarding](_planning/developer-onboarding.md)

### In-Flight Work
- [Go High Level Integration](_planning/go-high-level-integration.md)
- [Follower Sync](_planning/follower-sync.md)
- [Account Deletion](_planning/account-deletion.md)
- [Profile Claim Management](_planning/profile-claim-management.md)

## Planning Documents

### [Effort Estimation](effort-estimation.md)
Comprehensive effort estimates for all 27 initiatives including:
- Size estimates (S/M/L/XL with week ranges)
- Complexity and risk assessments
- Priority rankings
- Detailed effort breakdowns by initiative

**Key Metrics**:
- **Total Estimated Effort**: 130-173 weeks across all initiatives
- **High Priority**: 12 initiatives requiring immediate attention
- **High Risk**: 4 initiatives needing extra planning and mitigation

### [Timeline & Milestones](timeline.md)
Detailed 10-month timeline with quarterly milestones:
- **Q1 (Months 1-3)**: Foundation - Database schema, Event sourcing, Critical fixes
- **Q2 (Months 4-6)**: Data Quality - Deduplication, Admin tools, Pipeline optimization
- **Q3 (Months 7-9)**: User Features - Notifications, Chat, Onboarding
- **Q4 (Months 10-12)**: Scale & Polish - Platform optimization, Developer experience

Includes resource requirements, risk mitigation strategies, and parallel work optimization.

## Priority Summary

See [effort-estimation.md](effort-estimation.md#by-priority) for complete analysis.

### High Priority (12 initiatives)
Foundation and critical business needs:
- Event Sourcing Infrastructure, Database Schema & Tooling
- Facebook Scraper, Entity Deduplication
- Admin Roles, Pipeline Tools, Data Management
- Comprehensive Notification System
- Stripe Integration Fix, Account Deletion
- Platform Documentation (current, nearly complete)

### Medium-High Priority (2 initiatives)
- Chat System Integration, App Backend Consolidation

### Medium Priority (8 initiatives)
- Data Enrichment, Dynamic Scraping, Extraction Improvements
- Admin Content Moderation, Profile Onboarding
- Developer Onboarding, Follower Sync, Profile Claim Management

### To Be Determined (4 initiatives)
All NFT initiatives - depends on business priority and architecture decision

## Dependencies

See [timeline.md](timeline.md#critical-path) for complete dependency analysis.

### Foundation (Blocking Everything)
- **Database Schema & Tooling** - Blocks all data-related work
- **Event Sourcing Infrastructure** - Blocks data quality improvements
- **Stripe Integration Fix** - Blocks revenue (critical)

### Data Quality Track
- **Facebook Scraper** → Expands data coverage
- **Entity Deduplication** → Requires admin tools, improves data quality
- **Data Enrichment** → Requires event sourcing infrastructure

### Admin Tools Track
- **Admin Roles & Access** → Required for other admin features
- **Admin Data Management** → Required for entity deduplication
- **Admin Pipeline Tools** → Required for pipeline operations

### User Features Track
- **Notification System** → Blocks chat integration
- **Chat Integration** → Requires notifications (soft dependency)

### NFT Track (Conditional)
- **NFT Architecture Decision** → Blocks all other NFT work
- May require **Database Schema (Postgres)** depending on architecture choice

## Timeline Overview

See [timeline.md](timeline.md) for detailed Gantt charts and weekly breakdown.

### Milestones

| Milestone | Target | Key Deliverables |
|-----------|--------|------------------|
| **M1: Foundation Complete** | Month 3 | Database schema, Event sourcing modernized, Critical fixes |
| **M2: Data Quality Platform** | Month 6 | Deduplication live, Admin tools complete, Pipeline optimized |
| **M3: Enhanced User Experience** | Month 9 | Notifications, Chat, Onboarding, Backend consolidated |
| **M4: Production Ready Platform** | Month 10 | Developer experience, Monitoring, Documentation complete |
| **M5: NFT Platform** (optional) | Month 16 | NFT exchange operational (if prioritized) |

### Current Status
- **Platform Documentation & Planning**: ⏳ In Progress (Week 4 of 4)
- **In-Flight Work**: 🟡 Need assessment (Go High Level, Follower Sync, Account Deletion, Profile Claim)
- **Next Up**: Database Schema & Tooling, Stripe Fix (Week 2)

## Status Legend

- 🔴 **Blocked** - Cannot proceed due to dependencies
- 🟡 **Planning** - Needs specification/design
- 🟢 **Active** - Currently in development
- 🔵 **In Review** - PR open, awaiting merge
- ⚪ **Planned** - Scheduled but not started
- ✅ **Complete** - Shipped to production
