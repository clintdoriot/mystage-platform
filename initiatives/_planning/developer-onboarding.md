# Developer Onboarding Documentation

## Status
🟡 Planning

## Description

Create comprehensive developer onboarding documentation for new team members joining the MyStage projects.

## Affected Repositories

- **mystage-platform** (this repo - onboarding docs)
- All other repos (will need documentation updates)

## Purpose

Enable new developers to:
- Understand the platform architecture
- Set up development environments quickly
- Navigate the codebase effectively
- Follow development workflows
- Access necessary tools and services

## Key Components

### 0. Automated Setup Tooling
**Scripts per repository** (`scripts/setup-env.sh` or similar):
- Fetch environment variables from GCP Secret Manager
- Generate `.env` files automatically
- Validate required secrets are present
- Set up Firebase project configuration
- Install dependencies using appropriate package manager

**Shared pattern documentation** (in platform repo):
- Template script for GCP Secret Manager integration
- Secret naming conventions across repos
- Authentication patterns (gcloud auth)
- Error handling and troubleshooting

### 1. Platform Overview
- System architecture
- Repository relationships
- Data flow diagrams
- Technology stack summary

### 2. Development Environment Setup
- Required tools and services (uv, Firebase CLI, Node, etc.)
- Firebase project access
- GCP configuration
- Local development setup
- **Environment variables and secrets**:
  - **Automated .env generation** from GCP Secret Manager
  - Scripts in each repo (`scripts/setup-env.sh` or similar)
  - Shared pattern/template documented in platform
  - Secret naming conventions
  - Troubleshooting common issues
- **Onboarding checklist** (step-by-step setup verification)

### 3. Repository-Specific Guides
For each repo:
- Purpose and scope
- Setup instructions
- Development workflow
- Testing approach
- Deployment process

### 4. Common Tasks
- How to add a new scraper
- How to modify extraction prompts
- How to add admin UI features
- How to deploy functions
- How to debug pipeline issues

### 5. Access & Credentials
- Firebase project access
- GCP permissions
- Algolia access
- GitHub access
- Stripe dashboard (if applicable)
- Third-party services

### 6. Development Standards
- Code style guidelines
- Testing requirements
- Git workflow
- PR process
- Claude tooling usage

## Dependencies

- Platform documentation (ongoing)
- Architecture documentation
- Per-repo documentation improvements

## Estimated Effort

Initial version: 2-3 weeks
Ongoing maintenance: continuous

Breakdown:
- **Automated setup tooling**: 3-5 days
  - GCP Secret Manager integration pattern: 1 day
  - Script templates and examples: 1 day
  - Per-repo setup scripts: 1-3 days (depends on number of repos)
  - Testing and validation: 1 day
- **Onboarding checklist**: 1-2 days
- Platform overview: 2-3 days
- Environment setup documentation: 2-3 days
- Per-repo guides: 1-2 days each
- Common tasks: 2-3 days
- Access documentation: 1 day
- Review and polish: 2-3 days

## Success Criteria

- New developer can set up environment in < 1 day
- Clear understanding of architecture in < 2 days
- Can make first contribution in < 1 week
- Documentation is discoverable and searchable
- Feedback from new developers is positive

## Priority

High - Currently blocking efficient team scaling

## Structure

### Platform Documentation
**Location**: `platform/docs/developer-onboarding/`
- README.md (start here with onboarding checklist)
- architecture-overview.md
- environment-setup.md (includes GCP Secret Manager pattern)
- repo-guides/ (folder with per-repo setup)
- common-tasks/ (folder)
- access-credentials.md
- development-standards.md
- troubleshooting.md

### Per-Repository Tooling
**Location**: Each repo's `scripts/` directory
- `scripts/setup-env.sh` (or `.py`) - Fetch secrets and generate .env
- `scripts/validate-env.sh` - Verify environment is correctly set up
- `scripts/README.md` - Document available setup scripts

**Repositories needing setup scripts**:
- mystage-event-sourcing
- mystage-admin-interface
- mystage-app-backend
- mystage-databases (for deployment scripts)

**Example script structure**:
```bash
#!/bin/bash
# scripts/setup-env.sh
# Fetches environment variables from GCP Secret Manager and generates .env file

# 1. Check gcloud auth
# 2. Fetch secrets from Secret Manager
# 3. Generate .env.development.local or appropriate file
# 4. Validate required variables present
# 5. Output success/next steps
```

## Related Initiatives

- [Platform Documentation & Planning](platform-planning.md) (current work)

## Notes

- This is a living document that needs updates as platform evolves
- Consider video walkthroughs for complex setup
- Create templates for common tasks
- Include troubleshooting section
- Link to Claude tools and commands documentation
