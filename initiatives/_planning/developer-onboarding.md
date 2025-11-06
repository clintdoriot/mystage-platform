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

### 1. Platform Overview
- System architecture
- Repository relationships
- Data flow diagrams
- Technology stack summary

### 2. Development Environment Setup
- Required tools and services
- Firebase project access
- GCP configuration
- Local development setup
- Environment variables and secrets

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

Initial version: 1-2 weeks
Ongoing maintenance: continuous

Breakdown:
- Platform overview: 2-3 days
- Environment setup: 2-3 days
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

Suggested location: `platform/docs/developer-onboarding/`
- README.md (start here)
- architecture-overview.md
- environment-setup.md
- repo-guides/ (folder)
- common-tasks/ (folder)
- access-credentials.md
- development-standards.md

## Related Initiatives

- [Platform Documentation & Planning](platform-planning.md) (current work)

## Notes

- This is a living document that needs updates as platform evolves
- Consider video walkthroughs for complex setup
- Create templates for common tasks
- Include troubleshooting section
- Link to Claude tools and commands documentation
