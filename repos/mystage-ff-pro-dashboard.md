# MyStage Pro Dashboard

## Overview

FlutterFlow-based website for artists, venues, and festival managers to manage their presence and data.

## Technology Stack

- **Platform**: FlutterFlow (considering migration to React)
- **Deployment**: Web
- **Base**: Extends mystage-ff-base-lib

## Purpose

Professional dashboard for:
- **Artists** - Manage artist profiles, performance history, promotional content
- **Venues** - Manage venue information, schedules, bookings
- **Festival Managers** - Manage festival data and lineups

## Development Process

- Built using FlutterFlow visual development platform
- Git is used as **backup only**, not primary development workflow
- Changes typically made through FlutterFlow interface
- **Note**: Discussion of migrating to React instead

## Related Repositories

- **mystage-ff-base-lib** - Base FlutterFlow project this extends (if staying with FF)
- **mystage-app-backend** - Backend functions for dashboard operations
- **mystage-databases** - Database for artist/venue/festival data
- **mystage-event-sourcing** - May consume or supplement scraped data

## Current Status

Active development. Needs better documentation and Claude tooling setup.

## Migration Considerations

- React migration being discussed
- Would require significant re-architecture
- Need to evaluate FlutterFlow limitations vs React benefits

## Notes

- FlutterFlow-based means limited traditional git workflow
- Critical tool for professional users (artists/venues)
- May need more customization than FlutterFlow can provide (hence React discussion)
