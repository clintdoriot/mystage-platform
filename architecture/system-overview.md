# MyStage Platform Architecture Overview

## Platform Purpose

MyStage connects the music industry ecosystem - fans, artists, venues, and festivals - through automated data aggregation and live interaction tools.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER-FACING LAYER                       │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────┐      │
│  │   App    │  │  Fanex   │  │   Pro Dashboard     │      │
│  │ (Mobile) │  │  (Web)   │  │      (Web)          │      │
│  └────┬─────┘  └────┬─────┘  └──────────┬──────────┘      │
└───────┼─────────────┼───────────────────┼──────────────────┘
        │             │                   │
        └─────────────┴───────────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
   ┌────▼─────────┐         ┌────────▼─────────┐
   │ App Backend  │         │    Firestore     │
   │  Functions   │◄────────┤  (default) DB    │
   └──────────────┘         └──────────────────┘
                                     ▲
                                     │
   ┌──────────────────────────────────────────────────────┐
   │              DATA PIPELINE LAYER                     │
   │  ┌────────────────────────────────────────────┐     │
   │  │       Event Sourcing (Python)              │     │
   │  │  Scrape → Extract → Process → Dedupe       │     │
   │  └─┬──────────────────────────────────────┬───┘     │
   │    │                                      │         │
   │  ┌─▼────────────────┐        ┌───────────▼──────┐  │
   │  │ data-pipeline DB │   →    │  (default) DB    │  │
   │  │  (intermediate)  │        │  (production)    │  │
   │  └──────────────────┘        └──────────────────┘  │
   └──────────────────────────────────────────────────────┘
                      │
                ┌─────▼──────┐
                │   Algolia  │ (search index)
                └────────────┘
                      │
                      ▼
              User-Facing Apps

   ┌──────────────────────────────────────────────────────┐
   │           ADMIN & MANAGEMENT LAYER                   │
   │  ┌────────────────────────────────────────────┐     │
   │  │    Admin Interface (Monorepo)              │     │
   │  │  - Manage data quality                     │     │
   │  │  - Control pipeline operations             │     │
   │  │  - Content moderation                      │     │
   │  └────────────────────────────────────────────┘     │
   │         │                              │             │
   │         ├──────► Firestore             │             │
   │         └──────► Event Sourcing Functions            │
   └──────────────────────────────────────────────────────┘
```

## System Components

### Data Pipeline (mystage-event-sourcing)
**Purpose**: Aggregate and process music industry data
**Language**: Python 3.12 with uv package management
**Architecture**: Monorepo with 11 Firebase Function service groups
**Deployment**: Firebase Functions (30+ functions), Cloud Tasks, Pub/Sub
**AI/ML**: Pydantic-AI for LLM-based extraction
**Data Flow**: URLs → Scrapes → Extractions → Entity Sources → Canonical Entities → Algolia
**Writes to**: Firestore (scraping database), Algolia indexes, Cloud Storage (images)

**Service Groups**: Scheduling, Scraping API, Data Sourcing, Document Processing, Extraction (adapters & agents), Entity Resolution, Entity Source Management, Entity Writers, Image Processing, Data Store Sync

See [mystage-event-sourcing repo](../repos/mystage-event-sourcing.md) for details on integration points and [event-sourcing/docs](https://github.com/mystage/event-sourcing/docs) for implementation details.

### User-Facing Applications

#### Mobile App (mystage-app)
**Purpose**: Fan discovery and engagement
**Platform**: FlutterFlow → iOS/Android
**Reads from**: Firestore (default), Algolia

#### Fanex (mystage-ff-fanex)
**Purpose**: Live performance interaction (tips, requests, chat)
**Platform**: FlutterFlow → Web
**Reads/Writes**: Firestore (default), Stripe

#### Pro Dashboard (mystage-ff-pro-dashboard)
**Purpose**: Artist/venue management tools
**Platform**: FlutterFlow → Web (considering React migration)
**Reads/Writes**: Firestore (default)

#### Base Library (mystage-ff-base-lib)
**Purpose**: Shared components for FlutterFlow apps
**Platform**: FlutterFlow

### Backend Services

#### App Backend (mystage-app-backend)
**Purpose**: Backend functions for user-facing apps
**Language**: TypeScript/JavaScript
**Deployment**: Firebase Functions
**Serves**: App, Fanex, Pro Dashboard

#### Admin Interface (mystage-admin-interface)
**Purpose**: Internal data management and operations with RBAC
**Architecture**: Monorepo (React frontend + Python backend functions - planned)
**Frontend**: React 19 + TypeScript 5 + Vite + MUI (layered hybrid architecture: pages → features → entities → shared)
**Backend**: Python 3.12 + Firebase Functions (admin-api, jobs - planned)
**Testing**: Vitest (unit) + Playwright (E2E)
**Auth**: Firebase Auth with multi-tenancy + role-based access control
**Access**: 3 Firestore databases per environment (main, pipeline, admin), Algolia indices
**Key Features**: Multi-tenant RBAC, audit logging, environment isolation, panel stack system for drill-down navigation

See [mystage-admin-interface repo](../repos/mystage-admin-interface.md) for details on architecture layers and workflows.

### Infrastructure Repositories

#### Firestore (mystage-databases)
**Purpose**: Database rules, indexes, schema definitions
**Deployment**: Applied to GCP Firestore
**Critical**: Source of truth for database structure

#### NFT Exchange (mystage-exchange-nfts)
**Purpose**: NFT sticker exchange (experimental)
**Status**: Architecture decision pending (Firestore vs Postgres)

## Shared Infrastructure

### Databases

#### Firestore: "scraping" database
- **Purpose**: Event-sourcing pipeline and entity data
- **Pipeline collections**: `urls`, `scrapes`, `extractions`, `entity_sources`, `scheduled_tasks`
- **Entity collections**: `evt_venues`, `evt_artists`, `evt_performances`
- **Supporting collections**: `url_images`, `venue_duplicates`
- **Consumers**: Event-sourcing (read/write), all apps (read entities)

#### Firestore: Additional user data
- **Purpose**: User-generated content and application data
- **Data**: User profiles, posts, comments, tips, song requests, chat, profile claims
- **Consumers**: All user-facing apps, admin interface
- **Note**: Database structure/naming TBD - may be same or separate from scraping DB

#### BigQuery (planned)
- **Purpose**: Entity deduplication at scale, analytics
- **Consumers**: Event-sourcing deduplication process

### External Services

#### Algolia
- **Purpose**: Fast search across events/artists/venues
- **Updated by**: Event-sourcing (re-indexing)
- **Consumed by**: All user-facing apps

#### Stripe
- **Purpose**: Payment processing (tips, subscriptions)
- **Integrated with**: App backend, Fanex

#### Firebase Auth
- **Purpose**: User authentication
- **Used by**: All user-facing apps, admin interface

#### GCP/Firebase Platform
- **Functions**: Serverless compute
- **Storage**: File uploads, images
- **Cloud Tasks**: Async job processing (replacing Pub/Sub)

## Integration Patterns

### Data Flow Pattern
```
External Sources
    → Event Sourcing (scrape/extract/process)
    → Firestore data-pipeline
    → Event Sourcing (dedupe/enrich/validate)
    → Firestore (default)
    → Algolia (re-index)
    → User Apps (consume)
```

### Admin Control Pattern
```
Admin Interface
    → Triggers Event Sourcing Functions
    → Pipeline operations execute
    → Results written to Firestore
```

### User Interaction Pattern
```
User App
    → App Backend Functions
    → Firestore (read/write)
    → Response to User
```

### Real-Time Pattern
```
User Action (chat, tip, etc.)
    → Firestore write
    → Firestore real-time listeners
    → Other users see updates
```

## Technology Stack

### Frontend
- **FlutterFlow**: Visual app builder (rapid development)
- **React** (planned): Admin interface, possibly Pro Dashboard

### Backend
- **Python**: Event-sourcing pipeline
- **TypeScript/JavaScript**: Firebase Functions
- **Firebase Functions**: Serverless compute
- **Cloud Tasks**: Async processing (replacing Pub/Sub)

### Data & ML
- **Firestore**: Primary database (NoSQL)
- **BigQuery**: Analytics and deduplication (planned)
- **Pydantic-AI**: LLM orchestration for data extraction
- **Anthropic/OpenAI**: LLM models

### Infrastructure
- **GCP/Firebase**: Cloud platform
- **Terraform/Pulumi** (planned): Infrastructure as Code
- **Docker** (maybe): Containerized services (Facebook scraper)

## Key Architectural Decisions

### Completed
✅ **Firebase/GCP ecosystem**: Integrated services, managed infrastructure
✅ **Firestore as primary DB**: Good for real-time, integrates well with Firebase
✅ **FlutterFlow for rapid development**: Fast iteration on user-facing apps
✅ **LLM-based extraction**: AI for structuring scraped data
✅ **Two-database pattern**: Separate intermediate (data-pipeline) from production (default)

### Pending
🟡 **NFT: Firestore vs Postgres**: Transaction consistency requirements
🟡 **Cloud Tasks migration**: Replace Pub/Sub and document triggers
🟡 **Facebook scraper: Docker vs VM**: Deployment strategy
🟡 **Pro Dashboard: FlutterFlow vs React**: Customization vs rapid development

## Deployment Architecture

### Current State
- Firebase Functions deployed via CLI
- FlutterFlow apps deployed via FlutterFlow platform
- Firestore rules/indexes deployed manually
- Limited CI/CD automation

### Planned Improvements
- Infrastructure as Code (Terraform/Pulumi)
- Automated CI/CD pipelines
- Staging environments
- Comprehensive testing

## Security Architecture

### Authentication
- Firebase Auth for all user apps
- Custom claims for admin roles
- API keys for service-to-service

### Authorization
- Firestore Security Rules control data access
- Backend functions validate all operations
- Role-based access for admin interface

### Data Protection
- HTTPS everywhere
- Firestore encryption at rest
- Stripe handles payment security (PCI compliant)

## Scaling Considerations

### Current Approach
- Firebase auto-scales functions
- Firestore scales automatically
- Algolia handles search load

### Bottlenecks
- Firestore write limits (bulk operations)
- LLM API rate limits (extraction)
- Manual admin operations (needs tooling)

### Mitigation Strategies
- Cloud Tasks for distributed processing
- Batch operations with throttling
- Caching via Algolia
- Early exit optimizations in pipeline

## Cross-Repository Dependencies

### Event Sourcing Depends On
- Firestore (schema and rules)
- BigQuery (deduplication, planned)
- External APIs (enrichment data)

### User Apps Depend On
- Firestore (default) for data
- Algolia for search
- App Backend for operations
- Firebase Auth for authentication

### Admin Interface Depends On
- Firestore (all databases)
- Event Sourcing Functions (trigger operations)
- App Backend (shared operations)

### All Depend On
- mystage-databases (database structure)
- GCP/Firebase platform
- Firebase Auth

## Documentation Boundaries

### This Repo (Platform)
- **High-level architecture** (this document)
- **Integration between repos**
- **Shared infrastructure**
- **Cross-cutting decisions**
- **Initiative planning**

### Individual Repos
- **Implementation details**
- **Internal architecture**
- **API specifications**
- **Code organization**
- **Development workflows**

See [repos/](../repos/) for pointers to individual repository documentation.

## Future Considerations

- GraphQL API layer (unified data access)
- Notification service (comprehensive push/email)
- Chat service architecture (centralized vs embedded)
- Analytics data warehouse
- Machine learning models for matching/recommendations

## Notes

- Architecture is evolving - not everything is built yet
- Some components need refactoring (app-backend organization)
- Moving toward Infrastructure as Code
- Balancing rapid development (FlutterFlow) with customization needs
