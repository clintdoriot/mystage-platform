# CLAUDE.md

This file provides Claude Code with project-specific working instructions for the MyStage platform documentation and planning repository.

## Project Context

Central documentation and planning repository for the entire MyStage platform. Contains cross-project specifications, architecture documentation, initiative planning, effort estimates, and timelines. This is a **documentation repository** - no code implementation happens here.

## Key Commands

**From project root:**
- `ls -la` - List directory contents
- `find . -name "*.md" -type f` - Find all markdown files
- `grep -r "search term" .` - Search across all documentation
- `tree -L 3` - View directory structure (if tree is installed)

**For viewing files:**
- Use Read tool to read markdown files
- Use Glob to find files by pattern
- Use Grep to search file contents

**Note**: This is a documentation repo. No build, test, or deployment commands needed.

## Repository Purpose

This repository is the **single source of truth** for:
- Cross-project specifications and planning
- Platform-wide architecture and integration documentation
- Initiative tracking, effort estimation, and timelines
- Dependency mapping across repositories
- High-level system documentation

**This repository contains documentation ABOUT the platform, not the platform code itself.**

## Documentation Philosophy

- **High-Level Focus**: Platform documentation stays at the integration level - HOW systems connect, not HOW they work internally
- **Cross-Cutting Only**: Only document what spans multiple repositories
- **Living Documentation**: Keep docs current as understanding evolves
- **Lightweight but Useful**: Prefer clear, concise docs over exhaustive detail
- **Clear Boundaries**: Platform = integration, Repos = implementation

See `architecture/README.md` for detailed guidance on what belongs where.

## Project Structure

**Documentation hierarchy:**
- `README.md` - Platform overview and navigation
- `EXECUTIVE-SUMMARY.md` - High-level roadmap and resource requirements (for stakeholders)
- `repos/` - Per-repository documentation (9 active + 3 deprecated)
  - `mystage-event-sourcing.md` - Data pipeline overview
  - `mystage-admin-interface.md` - Admin tools overview
  - `mystage-databases.md` - Database schemas overview
  - `mystage-app-backend.md` - Backend services overview
  - `mystage-app.md`, `mystage-ff-*.md` - FlutterFlow apps
  - `mystage-exchange-nfts.md` - NFT system (preliminary)
- `initiatives/` - Initiative planning and tracking
  - `README.md` - Initiative index with priorities and milestones
  - `effort-estimation.md` - Comprehensive effort estimates (130-173 weeks)
  - `timeline.md` - 10-month implementation plan with Gantt charts
  - `_planning/*.md` - 27 detailed initiative documents
  - `_complete/` - Completed initiatives (historical reference)
  - Active initiatives get their own subdirectories when work begins
- `architecture/` - Platform-wide architecture documentation
  - `README.md` - Documentation boundaries and guidelines
  - `system-overview.md` - Integration-focused system architecture
  - `data-flow.md` - How data moves between systems
  - `dependencies.md` - Cross-repo dependencies and blockers

## Documentation Style

- Use GitHub-flavored Markdown
- Use relative links for internal references
- Include tables for structured data
- Use code blocks with language hints
- Add status indicators (🔴🟡🟢✅⏳)
- Keep headers consistent across similar documents
- Use bullet points for lists, tables for comparisons

## Documentation Agents

Three agents maintain documentation quality and consistency:

- **`docs-finder`** - Discovers existing documentation before creating new content, prevents duplication, enforces documentation boundaries
- **`doc-updater`** - Updates indexes and cross-references after documentation changes, keeps everything in sync
- **`architecture-validator`** - Validates documentation boundaries, completeness, and cross-references before committing

Use these agents proactively:
- **Before starting**: Use `docs-finder` to check for existing docs and ensure proper placement
- **After creating**: Use `doc-updater` to update indexes and establish cross-references
- **Before committing**: Use `architecture-validator` to catch issues early

## Important Rules

- **NEVER** put implementation details in platform docs - those belong in repository docs
- **ALWAYS** focus on integration between systems, not internal implementation
- **ALWAYS** update multiple related docs when making changes (e.g., README, initiative index, timeline)
- **NEVER** commit to timelines without checking dependencies
- **ALWAYS** validate that new initiatives don't duplicate existing ones
- Check existing documentation before creating new files
- Follow git workflow - create feature branches, PR to main
- Keep documentation boundaries clear (see `architecture/README.md`)

## Common Patterns

### When Adding a New Initiative
1. Check `initiatives/_planning/` to ensure it doesn't duplicate existing work
2. Create initiative document in `initiatives/_planning/[initiative-name].md`
3. Update `initiatives/README.md` to add to index
4. Update `initiatives/effort-estimation.md` with effort estimate
5. Update `initiatives/timeline.md` if it affects critical path
6. Update `architecture/dependencies.md` if it has cross-repo dependencies

### When Documenting a Repository
1. Check existing docs in `repos/`
2. Focus on integration points (what databases, what APIs, what other repos)
3. Document technology stack and deployment
4. Link to detailed docs in the actual repository
5. Update platform `README.md` repository index

### When Documenting Architecture
1. Focus on HOW systems integrate, not HOW they work internally
2. Document data flow between systems
3. Show dependencies and integration patterns
4. Reference repository docs for implementation details
5. Keep it high-level and integration-focused

### When Creating Timelines
1. Check `initiatives/effort-estimation.md` for initiative sizes
2. Identify dependencies in `architecture/dependencies.md`
3. Consider resource constraints (team size)
4. Include buffer for unknowns (typically 20%)
5. Show parallel work tracks
6. Update both `timeline.md` and `initiatives/README.md`

## Initiative Workflow

Initiatives move through three stages:

1. **Planning** (`_planning/`) - Scoping, estimation, prioritization
   - `/initiative-brainstorm` creates `_planning/[name].md`
   - `/initiative-plan` creates `_planning/[name]-plan.md`
   - Both files stay in `_planning/` during planning phase

2. **Active** (own subdirectory) - Contains specs, progress tracking, related docs
   - `/initiative-create-issues` moves files to `initiatives/[name]/` subdirectory
   - Creates `initiatives/[name]/issues.md` tracking document
   - Issues created in appropriate GitHub repository
   - Initiative marked as "Active"

3. **Complete** (`_complete/`) - Shipped to production, moved for historical reference
   - Move entire subdirectory: `initiatives/[name]/` → `initiatives/_complete/[name]/`

**Status Indicators:**
- 🔴 Blocked - Cannot proceed due to dependencies
- 🟡 Planning - Needs specification/design
- 🟢 Active - Currently in development
- 🔵 In Review - PR open, awaiting merge
- ⏳ In Progress - Work underway
- ✅ Complete - Shipped to production

## Current Priorities

**High Priority (12 initiatives):**
- Event Sourcing Infrastructure, Database Schema & Tooling
- Facebook Scraper, Entity Deduplication
- Admin Roles, Pipeline Tools, Data Management
- Comprehensive Notification System
- Stripe Integration Fix, Account Deletion
- Platform Documentation (✅ complete)

**See `initiatives/README.md` for full priority breakdown.**

## Key Metrics

- **Total Initiatives**: 27 across 8 categories
- **Total Estimated Effort**: 130-173 weeks
- **Timeline with 3-4 Engineers**: 10 months for high-priority work
- **High-Risk Initiatives**: 4 (Entity Dedup, NFT work)
- **Blocking Dependencies**: Database Schema, Event Sourcing, Stripe Fix

## Cross-References

**Platform Documentation:**
- **For Stakeholders**: Start with `EXECUTIVE-SUMMARY.md`
- **For Engineers**: Start with `architecture/README.md` then `architecture/system-overview.md`
- **For Planning**: Review `initiatives/effort-estimation.md` and `initiatives/timeline.md`
- **For Repo Details**: Check `repos/[repo-name].md`

**External Documentation** (in actual repositories):
- **event-sourcing**: `/Users/clint/Projects/mystage/event-sourcing/docs/`
- **admin-interface**: `/Users/clint/Projects/mystage/admin-interface/docs/`
- **databases**: `/Users/clint/Projects/mystage/databases/` (schema, rules, indexes)

## Documentation Maintenance

### When to Update Platform Docs

**Update Platform Documentation When:**
- Adding a new repository/system to the platform
- Changing how systems integrate or communicate
- Adding/removing shared infrastructure (databases, services)
- Making platform-wide technology decisions
- Changing data flow between systems
- Adding new external service integrations
- Planning new cross-repo initiatives
- Effort estimates or timelines change significantly

**Don't Update Platform Documentation When:**
- Refactoring within a single repository
- Adding features that don't affect integration
- Changing internal APIs (not used by other repos)
- Improving algorithms or implementations
- Fixing bugs in a single repo
- Making changes internal to one system

### Document Update Checklist

When making changes to platform docs:
- [ ] Check if related documents need updates (README, indexes, timeline)
- [ ] Update effort estimates if initiative scope changes
- [ ] Update timeline if critical path is affected
- [ ] Update dependencies if new blockers identified
- [ ] Update architecture docs if integration changes
- [ ] Verify links still work
- [ ] Check for consistency across related docs

## Custom Commands

### Initiative Planning Workflow
- `/initiative-brainstorm [idea]` - Develop initiative specification interactively
- `/initiative-plan [initiative-name]` - Break down initiative into implementation phases
- `/initiative-create-issues [initiative-name]` - Create GitHub milestone and issues

### Issue Management
- `/issue-identify [initiative-name|filter]` - Find next issue to work on
- `/issue-analyze [issue-number]` - Analyze requirements and dependencies in detail

### Quality Assurance
- `/doc-review [path]` - Comprehensive documentation review

**Typical Workflow:**
1. `/initiative-brainstorm [idea]` - Develop specification through guided questions
   - Uses `docs-finder` agent to check for existing initiatives
   - Saves to `initiatives/_planning/[name].md`
   - Uses `doc-updater` agent to update indexes after creation
   - Uses `architecture-validator` agent to validate the spec
2. `/initiative-plan [initiative-name]` - Create detailed implementation plan
   - Uses `docs-finder` agent to discover related documentation
   - Saves to `initiatives/_planning/[name]-plan.md`
   - Uses `doc-updater` agent to update effort estimates and timeline
   - Uses `architecture-validator` agent to validate completeness
3. `/initiative-create-issues [initiative-name]` - Generate trackable issues
   - Asks which repository to create issues in (for multi-repo initiatives)
   - **Moves files** from `_planning/` to `initiatives/[name]/` subdirectory
   - Creates GitHub milestone and issues in chosen repository
   - Creates `initiatives/[name]/issues.md` tracking document
   - Uses `doc-updater` agent to update status and references
   - Uses `architecture-validator` agent to verify everything
4. `/issue-identify` - Find next issue to work on
5. `/issue-analyze [issue-number]` - Clarify requirements before starting
6. Work on documentation/planning
7. `/doc-review [changed-files]` - Review before committing
   - Uses `architecture-validator` agent for comprehensive review

## Common Questions

**Q: Where should detailed implementation docs go?**
A: In the repository itself (e.g., `event-sourcing/docs/`), not in platform docs. Platform docs only cover integration.

**Q: How detailed should initiative documents be?**
A: Enough to understand scope, affected repos, dependencies, and effort. Detailed specs go in the repo when work starts.

**Q: When should an initiative move from _planning to active?**
A: When work begins and you need a workspace for specs, progress tracking, and related artifacts.

**Q: How often should effort estimates be updated?**
A: When scope changes significantly or after completing similar work that provides better data.

**Q: Should we document every repository detail here?**
A: No. Platform docs cover integration points only. Internal details stay in the repo.

## Related Resources

**Platform Documentation:**
- Overview: `README.md`
- Executive Summary: `EXECUTIVE-SUMMARY.md`
- Initiatives Index: `initiatives/README.md`
- Effort Estimates: `initiatives/effort-estimation.md`
- Timeline: `initiatives/timeline.md`
- Architecture Guide: `architecture/README.md`

**Repository Documentation:**
- event-sourcing: `repos/mystage-event-sourcing.md`
- admin-interface: `repos/mystage-admin-interface.md`
- databases: `repos/mystage-databases.md`
- [See `repos/` for complete list]

**External References:**
- event-sourcing repo: `/Users/clint/Projects/mystage/event-sourcing/`
- admin-interface repo: `/Users/clint/Projects/mystage/admin-interface/`
- databases repo: `/Users/clint/Projects/mystage/databases/`

## Notes

- This is **meta-documentation** - documentation about the platform, not code
- Keep it high-level and integration-focused
- Prefer clarity over comprehensiveness
- Update as understanding evolves
- Link to implementation repos for details
- Documentation boundaries matter (see `architecture/README.md`)
