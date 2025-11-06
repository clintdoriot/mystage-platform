# MyStage Platform Documentation

This repository contains cross-project documentation, specifications, and planning for the MyStage platform.

## Quick Start

**New here?** Start with the [Executive Summary](EXECUTIVE-SUMMARY.md) for a high-level overview of the platform, current state, and 10-month roadmap.

**Looking for specific information?**
- 📊 **Planning & Roadmap**: See [initiatives/](initiatives/) for all 27 initiatives, effort estimates, and timeline
- 🏗️ **Architecture**: See [architecture/](architecture/) for how systems integrate and data flows
- 📦 **Repository Details**: See [repos/](repos/) for documentation on each of the 9 active repos

## Purpose

- Central location for specifications that span multiple repositories
- Platform-wide architecture documentation
- Initiative tracking and timelines (27 initiatives documented)
- Shared data models and contracts
- Cross-cutting technical decisions

## Current Status

✅ **Platform Documentation & Planning Initiative Complete**

This repository now contains:
- **12 repository documentation files** (9 active + 3 deprecated)
- **27 detailed initiative documents** across all areas (infrastructure, data, admin, user features, NFT)
- **Comprehensive effort estimates** (130-173 weeks total, sized and prioritized)
- **10-month implementation timeline** with quarterly milestones and resource requirements
- **Architecture documentation** focused on integration between systems
- **Dependency mapping** showing critical paths and blockers

See [initiatives/platform-planning.md](initiatives/_planning/platform-planning.md) for full details on what was accomplished.

## Repository Index

### Active Projects

#### Core Infrastructure

- **[mystage-event-sourcing](repos/mystage-event-sourcing.md)** - Data pipeline for sourcing music industry data on performances, artists and venues. Python, Firebase, GCP project with many Firebase functions. Scrapes websites, analyzes data, produces comprehensive data on local events, venues and musicians. Intermediate data stored in data-pipeline database, final results in "(default)" database, re-indexed in Algolia.

- **[mystage-databases](repos/mystage-databases.md)** - Firestore rules and indexes. Should eventually contain schema definitions.

- **[mystage-app-backend](repos/mystage-app-backend.md)** - Backend functions needed by the front end app, fanex, and pro-dashboard.

#### User-Facing Applications

- **[mystage-app](repos/mystage-app.md)** - FlutterFlow-based mobile app for iOS and Android. Primary distribution channel for fans. Not typically managed through git (git is backup only).

- **[mystage-ff-fanex](repos/mystage-ff-fanex.md)** - FlutterFlow-based website for live performances (tipping, song requests, chat). Not typically managed through git (git is backup only).

- **[mystage-ff-pro-dashboard](repos/mystage-ff-pro-dashboard.md)** - FlutterFlow-based website for artists, venues, and festival managers to manage their data. Not typically managed through git (git is backup only). Some discussion of migrating to React.

- **[mystage-ff-base-lib](repos/mystage-ff-base-lib.md)** - FlutterFlow base project used by other FlutterFlow projects.

#### Internal Tools

- **[mystage-admin-interface](repos/mystage-admin-interface.md)** - Admin interface for internal team to manage all data across the project. Monorepo containing frontend and backend functions specific to admin site. May need to call functions from event-sourcing or app-backend repos.

#### Experimental

- **[mystage-exchange-nfts](repos/mystage-exchange-nfts.md)** - Preliminary attempt at implementing NFT-based sticker exchange for the app and dashboard.

### Deprecated Projects

These repos are listed for reference but are no longer actively developed:

- **mystage-admin-api** - Old repo for admin functions, never fully utilized. Now deprecated, though may contain useful geolocation services that could be migrated.
- **mystage-resume-monorepo** - Resume management system based on similar tech stack to admin-interface, but evolved into its own project.
- **mystage-resume-processing** - Preliminary resume management system, being migrated to monorepo.

## Directory Structure

```
platform/
├── README.md                    # This file
├── repos/                       # Per-repository documentation
│   ├── mystage-event-sourcing/  # Complex repos get folders
│   └── mystage-*.md             # Simple repos get single files
├── initiatives/                 # Cross-cutting initiatives and planning
└── architecture/                # Platform-wide architecture docs
```

## How to Use This Repository

### For Writing Specs
When writing a specification that touches multiple repositories, create it in `initiatives/` and reference the relevant repo docs.

### For Architecture Decisions
Platform-wide architectural decisions and data flows should be documented in `architecture/`. This covers **integration between systems**, not implementation within systems. See [architecture/README.md](architecture/README.md) for guidance on what belongs in platform architecture vs repository architecture.

### For Repo-Specific Details
Individual repository details, internal architecture, and implementation specifics belong in the respective repositories (pointed to from `repos/`).

## Getting Started

### For Executives / Product Managers
1. Read [EXECUTIVE-SUMMARY.md](EXECUTIVE-SUMMARY.md) - High-level overview, roadmap, resource requirements
2. Review [initiatives/README.md](initiatives/README.md) - Initiative index with priorities
3. Check [initiatives/timeline.md](initiatives/timeline.md) - Detailed timeline with milestones

### For Engineers / Technical Leads
1. Read [architecture/README.md](architecture/README.md) - Understand documentation boundaries
2. Review [architecture/system-overview.md](architecture/system-overview.md) - How systems integrate
3. Check [architecture/data-flow.md](architecture/data-flow.md) - How data moves through the platform
4. Dive into specific `repos/*.md` for implementation details

### For Project Planning
1. Review [initiatives/effort-estimation.md](initiatives/effort-estimation.md) - Comprehensive effort estimates
2. Check [initiatives/timeline.md](initiatives/timeline.md) - Timeline with dependencies
3. Review individual initiative docs in `initiatives/_planning/*.md` for detailed requirements
