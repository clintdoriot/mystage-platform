# Facebook Listing Scraper Finalization

## Status
🟢 Active

## Description

Finalize the Facebook events scraper to reliably collect event listings from Facebook. Currently in active development.

## Affected Repositories

- **mystage-event-sourcing** (scraper code)
- **mystage-admin-interface** (management tools)
- **mystage-databases** (credential & proxy storage)

## Key Components

### 1. Core Scraper Development
**Status**: 🟢 Active (being worked on)

### 2. Facebook Account & Proxy Management
**Task**: Add ability to manage FB accounts and proxies in admin tool
**Status**: Planning
**Why**: Need to rotate accounts/proxies to avoid rate limiting and blocks

### 3. Deployment Architecture Decision
**Options**:
- Convert to Docker container
- Add IaC for VM deployment
**Status**: 🔴 Decision needed
**Impact**: Affects deployment strategy and scaling

## Dependencies

- Admin interface: Need UI for managing FB credentials and proxies
- Infrastructure: Docker vs VM decision affects IaC setup
- Firestore: Schema for storing credentials/proxies

## Technical Challenges

- Facebook anti-scraping measures
- Account/proxy rotation strategy
- Rate limiting and detection avoidance
- Maintaining session state

## Estimated Effort

Core scraper: (Active - ongoing)
Admin tools: (TBD)
Deployment: (TBD - depends on Docker vs VM decision)

## Success Criteria

- Reliable scraping of Facebook event listings
- Admin tools for credential/proxy management
- Automated rotation to avoid blocks
- Deployed with proper IaC
- Monitoring and alerting when scraper fails

## Blockers

- Need to decide on Docker vs VM deployment strategy

## Notes

- High priority - Facebook is a major data source
- Anti-scraping measures make this challenging
- May need ongoing maintenance as Facebook changes detection
