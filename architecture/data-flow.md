# MyStage Platform Data Flow

## Overview

This document describes how data flows through the MyStage platform, from data sourcing through to user consumption.

## Primary Data Pipeline (Event Sourcing)

### Complete Pipeline Flow

```
External Sources (Yelp, Google Maps, Bandsintown, etc.)
    ↓ [1. Scraping via Firebase Functions]
urls → scrapes (raw HTML/JSON)
    ↓ [2. LLM Extraction via Pydantic-AI]
extractions (structured data)
    ↓ [3. Entity Resolution]
entity_sources (individual source contributions)
    ↓ [4. Entity Merging]
evt_venues, evt_artists, evt_performances (canonical entities)
    ↓ [5. Synchronization]
Algolia search indexes
    ↓ [6. Consumption]
User-Facing Apps
```

**All pipeline and entity data stored in**: Firestore (scraping database)

### Pipeline Stages Detail

#### 1. Scraping
- **Service Groups**: functions-scheduling, functions-sourcing, functions-scrapestorm
- **Input**: URLs from multiple sources
- **Output**: Raw scraped data in `scrapes` collection
- **Sources**: Yelp (via Apify), Google Maps (via Apify + direct), Bandsintown

#### 2. Extraction
- **Service Groups**: functions-doc-processors, functions-extraction-adapters, functions-extraction-agents
- **Input**: Scrapes
- **Output**: Structured data in `extractions` collection
- **Method**: LLM-based extraction using Pydantic-AI
- **Handles**: Both structured sources (adapters) and unstructured sources (AI agents)

#### 3. Entity Resolution
- **Service Group**: functions-entity-resolution
- **Input**: Extractions
- **Output**: Resolved entity IDs published to entity-source-mgmt
- **Purpose**: Match extractions to existing entities or create new entity IDs

#### 4. Entity Source Management & Merging
- **Service Groups**: functions-entity-source-mgmt, functions-entity-writers
- **Input**: Resolved entity IDs + extraction data
- **Process**:
  - Create/update `entity_sources` (individual source contributions)
  - Merge multiple sources into canonical entities
- **Output**: Canonical entities in `evt_venues`, `evt_artists`, `evt_performances`
- **Method**: AI-powered merging with conflict resolution based on source priority

#### 5. Search Synchronization
- **Service Group**: functions-sync-data-stores
- **Input**: Entity write events from Firestore
- **Output**: Updated Algolia indexes (venues, artists, performances)
- **Purpose**: Keep search indexes in sync with canonical entities

#### 6. User Consumption

```
User-Facing Apps
    ↓ [search]
Algolia Indexes (fast search)
    ↓ [details]
Firestore (full entity data)
```

**Consumer Apps**:
- Mobile app (iOS/Android)
- Fanex website
- Pro dashboard

## Admin Data Flow

### Manual Data Management

```
Admin Interface (React + TypeScript)
    ↓ [CRUD operations with RBAC]
Three Firestore Databases:
  - Main database (entities, users, profiles)
  - Pipeline database (urls, scrapes, extractions, entity_sources)
  - Admin database (admin_users, audit_logs, privileged_operations)
    ↓ [re-indexing]
Algolia (multiple indices)
    ↓
User-Facing Apps
```

**Purpose**:
- Correct scraping errors and entity data
- Add missing data
- Merge duplicate entities (venues, artists, performances)
- Separate bad merges
- User account management and support
- Moderate content

**RBAC**: Role-based access control with multi-tenancy
- Customer Support: User/profile management only
- Data Admin: Entity and pipeline data
- Developer: Full access (dev only)
- Super Admin: Full access (all environments)

### Admin Pipeline Control

```
Admin Interface
    ↓ [trigger operations]
Event Sourcing Functions (Cloud Functions)
    ↓ [execute]
Data Pipeline
```

**Purpose**:
- Trigger manual scraping
- Execute entity merges
- Manage scraping tasks
- View/manage pipeline data (urls, scrapes, extractions, entity_sources)

## User-Generated Data Flow

### Profile Claims

```
User (Pro Dashboard/App)
    ↓ [submit claim]
Firestore: claim requests
    ↓ [review]
Admin Interface
    ↓ [approve]
Firestore: user profiles with ownership
```

### Live Performance Data (Fanex)

```
Fan (Fanex) → Firestore: tips, song requests, chat
    ↓ [real-time]
Performer (Fanex/Pro Dashboard)
```

**Features**:
- Tips (payment via Stripe)
- Song requests
- Chat messages

### Posts & Comments

```
User (App)
    ↓ [create content]
Firestore: posts/comments
    ↓ [flagged]
Admin Interface (moderation)
    ↓ [action]
Firestore: content status updated
```

## Payment Data Flow

### Tipping Flow

```
Fan (Fanex)
    ↓ [payment]
Stripe
    ↓ [webhook]
App Backend Functions
    ↓ [record]
Firestore: transaction records
    ↓ [notification]
Performer
```

### Subscription/Premium (Future?)

```
User (App/Pro Dashboard)
    ↓ [subscribe]
Stripe
    ↓ [webhook]
App Backend Functions
    ↓ [update]
Firestore: user subscription status
```

## NFT Data Flow (Planned - Architecture TBD)

### Option A: Firestore-Based

```
Creator (Pro Dashboard)
    ↓ [create NFT]
NFT Backend (Firestore)
    ↓ [mint]
Blockchain
    ↓ [ownership record]
Firestore: NFT ownership
    ↓ [display]
User (App - collection view)
```

### Option B: Postgres-Based

```
Creator (Pro Dashboard)
    ↓ [create NFT]
NFT Backend (Postgres)
    ↓ [mint]
Blockchain
    ↓ [ownership record]
Postgres: NFT ownership
    ↓ [display]
User (App - collection view)
```

**Decision needed**: See [NFT Architecture](../initiatives/nft-architecture.md)

## Notification Data Flow (Planned)

```
Triggering Event (any source)
    ↓ [create notification]
Notification Service (App Backend)
    ↓ [store]
Firestore: notifications
    ↓ [deliver]
Firebase Cloud Messaging / Email / etc.
    ↓ [receive]
User (App/Dashboard)
```

**Triggers**:
- New events from followed artists
- Chat messages
- Tips received
- Profile claims approved
- Content moderation actions

## Chat Data Flow (Existing? TBD)

```
User A (App/Fanex/Dashboard)
    ↓ [send message]
Backend Chat Service
    ↓ [store & broadcast]
Firestore: chat messages
    ↓ [real-time listener]
User B (App/Fanex/Dashboard)
```

## Data Stores Summary

### Firestore Databases

**Main database: "scraping"** (GCP project database)
   - **Pipeline collections**: `urls`, `scrapes`, `extractions`, `entity_sources`, `scheduled_tasks`, `url_images`
   - **Entity collections**: `evt_venues`, `evt_artists`, `evt_performances`
   - **Supporting collections**: `venue_duplicates`, other data
   - **Consumers**: Event-sourcing pipeline (read/write), all apps (read entities)
   - **Note**: Event-sourcing manages the entire pipeline within this database

**Additional user data** (stored in Firestore, database TBD):
   - User profiles, authentication data
   - User-generated content (posts, comments)
   - Live performance data (tips, song requests, chat from fanex)
   - Profile claims
   - Admin data

### External Data Stores

1. **Algolia**
   - **Purpose**: Fast search indexing
   - **Indexes**: venues, artists, performances
   - **Updated by**: Event-sourcing sync functions
   - **Consumed by**: All user-facing apps (search)

2. **BigQuery** (planned)
   - **Purpose**: Entity deduplication at scale
   - **Contents**: Entity matching data, analytics
   - **Consumers**: Event-sourcing deduplication process

3. **Cloud Storage**
   - **Purpose**: Image storage and CDN
   - **Contents**: Optimized images for venues, artists, performances
   - **Updated by**: Event-sourcing image processing functions

4. **Postgres** (maybe - NFT system)
   - **Purpose**: NFT transactions and ownership (if Postgres chosen)
   - **Contents**: NFT metadata, ownership records, transactions
   - **Consumers**: NFT system
   - **Status**: Architecture decision pending

## Data Quality Loop

```
External Sources
    ↓ [scraping & extraction]
Firestore: data-pipeline
    ↓ [processing]
Firestore: (default)
    ↓ [admin review]
Admin Interface
    ↓ [corrections]
Firestore: (default)
    ↓ [feedback loop]
Extraction Improvements (prompts updated)
```

**Purpose**: Continuous improvement of data quality

## Key Integration Points

### Repository Interactions

```
mystage-databases (rules & schema)
    ↑ read/write
mystage-event-sourcing (pipeline)
    ↓ produces data
mystage-databases (default database)
    ↑ read/write
mystage-admin-interface (management) + mystage-app-backend (APIs)
    ↑ read
mystage-app + mystage-ff-* (user apps)
```

### External Service Integration

- **GCP**: Firebase Functions, Cloud Tasks, BigQuery
- **Algolia**: Search indexing
- **Stripe**: Payment processing
- **Blockchain**: NFT minting (future)
- **External APIs**: Data enrichment (Google Places, social media, etc.)

## Performance Considerations

### Write Path
- Event-sourcing does bulk writes to Firestore
- Need to optimize for Firestore write limits
- Cloud Tasks for distributed processing

### Read Path
- Algolia for search (performance)
- Firestore direct reads for detail pages
- Caching strategy TBD

### Real-Time Features
- Firestore real-time listeners for chat
- Firestore real-time listeners for live performance features (fanex)

## Security Considerations

### Data Access
- Firestore Security Rules enforce access control
- Admin interface has elevated permissions
- User apps have limited read access
- Write operations go through backend functions

### Payment Security
- Stripe handles payment processing (PCI compliance)
- Webhook verification required
- Transaction records in Firestore

### Content Moderation
- Admin review of flagged content
- Automated screening (future)
- User reporting system

## Notes

- This architecture is current state + planned features
- Some components (chat, notifications) may already exist but need documentation
- NFT architecture is undecided
- Data flow will evolve as new features are added
