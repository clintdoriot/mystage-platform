# MyStage Event Sourcing

## Overview

Data pipeline for sourcing music industry data on performances, artists, and venues. A monorepo containing 11 service groups deployed as Firebase Functions, plus shared Python packages.

## Technology Stack

- **Language**: Python 3.12
- **Package Management**: uv
- **Cloud Platform**: GCP/Firebase
- **Functions**: Firebase Functions (11 service groups, 30+ functions)
- **Database**: Firestore (scraping database)
- **Search**: Algolia
- **Messaging**: Pub/Sub, Cloud Tasks
- **AI/ML**: Pydantic-AI for LLM-based extraction

## Purpose

Automated data pipeline that:
- Scrapes music industry websites (Yelp, Google Maps, Bandsintown, etc.)
- Extracts structured data using LLM agents
- Resolves and deduplicates entities
- Merges data from multiple sources
- Synchronizes to Algolia for search

## High-Level Data Flow

```
URLs → Scrapes → Extractions → Entity Sources →
Entity Resolution → Canonical Entities → Algolia
```

**Key stages:**
1. **Scheduling**: Orchestrate scraping tasks
2. **Scraping**: Collect data from external sources
3. **Extraction**: Transform raw data to structured format (LLM-based)
4. **Entity Resolution**: Match entities across sources
5. **Source Management**: Store individual source contributions
6. **Entity Merging**: Combine sources into canonical entities
7. **Synchronization**: Update Algolia search indexes

## Monorepo Structure

```
event-sourcing/
├── services/               # 11 Firebase Function service groups
│   ├── functions-scheduling/
│   ├── functions-sourcing/
│   ├── functions-extraction-agents/
│   └── ... (8 more)
├── packages/               # Shared Python packages
│   ├── mystage-core/      # Models, utilities
│   └── mystage-agents/    # Agent utilities
├── admin/                  # Admin scripts for data management
└── docs/                   # Comprehensive documentation
```

## Service Groups (11 total)

1. **functions-scheduling** - Task orchestration
2. **functions-scrapestorm** - Scraping API
3. **functions-sourcing** - Data scraping from sources
4. **functions-doc-processors** - Document routing
5. **functions-extraction-adapters** - Data transformation
6. **functions-extraction-agents** - LLM extraction
7. **functions-entity-resolution** - Entity matching
8. **functions-entity-source-mgmt** - Source management
9. **functions-entity-writers** - Entity merging
10. **functions-img-processing** - Image optimization
11. **functions-sync-data-stores** - Algolia sync

## Key Collections (Firestore)

**Pipeline collections:**
- `urls`, `scrapes`, `extractions`, `entity_sources`, `scheduled_tasks`

**Entity collections:**
- `evt_venues`, `evt_artists`, `evt_performances`

**Supporting collections:**
- `url_images`, `venue_duplicates`

## Integration Points

**Writes to:**
- Firestore (scraping database) - All pipeline and entity data
- Algolia - Search indexes for venues, artists, performances
- Cloud Storage - Images via CDN

**Consumed by:**
- **mystage-admin-interface** - Calls functions, reads/writes Firestore
- **mystage-app** - Reads entities from Firestore/Algolia
- **mystage-ff-fanex** - Reads entities
- **mystage-ff-pro-dashboard** - Reads entities

**Depends on:**
- **mystage-databases** - Database rules and schema definitions
- External APIs - Google Places, social media (for enrichment)

## Documentation

**Comprehensive docs in repo:**
- `docs/README.md` - Documentation index
- `docs/pipeline.md` - Complete pipeline architecture
- `docs/data_model.md` - Collections and relationships
- `docs/project_structure.md` - Monorepo organization
- `docs/testing.md` - Testing philosophy
- `.claude/CLAUDE.md` - Development instructions

**See repo for implementation details** - the event-sourcing repo has extensive documentation about internal architecture, service design, and development workflows.

## Current Status

Active development. Well-documented with extensive Claude tooling (commands, agents). Mature codebase with established patterns.
