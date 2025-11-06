# Platform Architecture Documentation

## Purpose

This directory contains **high-level, cross-cutting architecture documentation** for the MyStage platform. These docs focus on how systems integrate, not how they're implemented internally.

## What Belongs Here

### ✅ Include in Platform Architecture
- **System integration**: How repositories interact with each other
- **Data flow**: How data moves between systems (repos, databases, services)
- **Shared infrastructure**: Databases, external services, platform services
- **Cross-cutting patterns**: Authentication, authorization, real-time communication
- **Platform-wide decisions**: Technology stack, deployment strategy
- **Integration contracts**: What each system expects from others
- **Cross-repo dependencies**: Which repos depend on which

**Audience**: Anyone who needs to understand how the whole platform fits together

### ❌ Don't Include in Platform Architecture
- **Internal implementation**: How a single repo is structured internally
- **Code organization**: Directory structure, module layout within a repo
- **Detailed APIs**: Specific endpoint definitions (those go in the repo)
- **Component architecture**: How components within a system interact
- **Development workflows**: How to develop in a specific repo
- **Detailed algorithms**: How extraction/deduplication/etc. work internally

**These belong in**: Individual repository documentation

## Documents in This Directory

### [system-overview.md](system-overview.md)
**High-level system architecture** showing:
- Major components (repositories) and their purposes
- How components integrate
- Shared infrastructure (Firestore, Algolia, Stripe, etc.)
- Technology stack choices
- Key architectural decisions
- Deployment architecture

**Read this first** if you're new to the platform.

### [data-flow.md](data-flow.md)
**How data moves through the platform**:
- Primary data pipeline (scraping → processing → consumption)
- Admin data flows (management and control)
- User-generated data flows (posts, claims, tips)
- Payment flows (Stripe integration)
- Planned flows (notifications, chat, NFT)

**Read this** to understand data lifecycle and integration points.

### [dependencies.md](dependencies.md)
**Initiative dependencies and relationships**:
- What initiatives block others
- Critical decision points
- Suggested sequencing
- Cross-cutting dependencies

**Read this** when prioritizing work and planning implementation order.

## Documentation Boundaries

### Example: Event Sourcing Pipeline

**Platform Architecture** (this directory) documents:
```
External Sources → Event Sourcing → data-pipeline DB →
Event Sourcing → (default) DB → Algolia → User Apps
```
- What databases it writes to
- What other systems consume its data
- High-level: "scrapes, extracts, deduplicates, enriches"

**Event Sourcing Repo** documents:
```
Scraper → Extractor → Validator → Deduplicator → Enricher
    ↓         ↓           ↓            ↓            ↓
  [Internal architecture, components, APIs, algorithms]
```
- How scraping works internally
- Extraction pipeline stages
- Deduplication algorithm
- How to add a new scraper
- API specifications

### Example: Admin Interface

**Platform Architecture** documents:
```
Admin Interface ─calls─> Event Sourcing Functions
Admin Interface ─reads/writes─> Firestore (all DBs)
Admin Interface <─authenticates via─ Firebase Auth
```
- Integration with event-sourcing
- Database access patterns
- Authentication/authorization approach

**Admin Interface Repo** documents:
```
Frontend (React?) ↔ Backend Functions ↔ Firestore
     │                    │
  [Components]      [API Endpoints]
  [Routing]         [Business Logic]
  [State Mgmt]      [Data Access]
```
- Monorepo structure (frontend + backend)
- Component architecture
- API endpoint specifications
- How to add a new admin page

## When to Update These Docs

### Update Platform Architecture When:
- Adding a new repository/system
- Changing how systems integrate
- Adding/removing shared infrastructure (databases, services)
- Making platform-wide technology decisions
- Changing data flow between systems
- Adding new external service integrations

### Don't Update Platform Architecture When:
- Refactoring within a single repo
- Adding features that don't affect integration
- Changing internal APIs (not used by other repos)
- Improving algorithms or implementations
- Fixing bugs

## Related Documentation

- **[../repos/](../repos/)** - Pointers to individual repository documentation
- **[../initiatives/](../initiatives/)** - Initiative planning and tracking
- **[../README.md](../README.md)** - Platform documentation overview

## Keeping Docs High-Level

**Good platform architecture doc:**
> "Event sourcing writes processed data to Firestore (default) database, which is then indexed to Algolia. User-facing apps read from both Algolia (search) and Firestore (details)."

**Too detailed for platform (belongs in repo):**
> "The extraction service uses pydantic-ai to orchestrate LLM calls. It makes 3 passes: first for basic info, second for structured details, third for validation. Each pass uses a different prompt template stored in prompts/..."

**Rule of thumb**: If it's about HOW systems interact, it belongs here. If it's about HOW a system works internally, it belongs in that repo.

## Questions?

If you're unsure whether something belongs in platform architecture or repo documentation, ask:

1. **Does this affect multiple repos?** → Platform architecture
2. **Is this an integration point?** → Platform architecture
3. **Is this about internal implementation?** → Repository docs
4. **Would this help someone understand the whole platform?** → Platform architecture
5. **Would this help someone work in a specific repo?** → Repository docs
