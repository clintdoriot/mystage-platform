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
  - `_planning/*.md` - 28 detailed initiative documents
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
- **ALWAYS** work on feature branches - **NEVER** commit directly to main
- **NEVER** create git commits without user running `/commit` command
- Keep documentation boundaries clear (see `architecture/README.md`)

## Git Workflow

**CRITICAL**: All documentation work happens on feature branches. Direct commits to main are not allowed.

### Branch-Based Workflow

**Branch Naming Convention:**
- Initiative planning: `initiative/[initiative-name]`
- Documentation updates: `docs/[description]`
- Repository docs: `repo/[repo-name]`
- Architecture changes: `arch/[description]`

**Example:**
```bash
git checkout -b initiative/entity-deduplication
# Make changes...
git add .
git commit -m "feat: add entity deduplication initiative design spec"
git push -u origin initiative/entity-deduplication
gh pr create --title "Initiative: Entity Deduplication System"
```

### Initiative Planning Workflow with Branches

The initiative planning workflow creates a single PR that evolves through multiple stages:

1. **Design Brainstorm** (creates branch + PR)
   - `/initiative-brainstorm-design [idea]` - Non-technical design specification
   - Creates feature branch `initiative/[name]`
   - Creates initial design document
   - Opens PR for review

2. **Technical Brainstorm** (adds to PR)
   - `/initiative-brainstorm-technical [initiative-name]` - Technical architecture
   - Works within existing branch
   - Adds technical requirements to design document
   - Updates PR

3. **Planning** (adds to PR)
   - `/initiative-plan [initiative-name]` - Implementation breakdown
   - Works within existing branch
   - Creates plan document
   - Updates PR with plan

4. **Review and Merge** (manual)
   - Team reviews the complete initiative (design + technical + plan)
   - Merge PR to main when approved

5. **Issue Creation** (after merge)
   - `/initiative-create-issues [initiative-name]` - Generate GitHub issues
   - **Must be on main branch** (after PR is merged)
   - Moves files from `_planning/` to active subdirectory
   - Creates issues in appropriate repository

### Branch Verification

All commands that modify documentation **must** verify they are on a feature branch (not main):

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# If on main, either create a branch or abort
if [ "$CURRENT_BRANCH" = "main" ]; then
  echo "ERROR: Cannot modify documentation on main branch"
  echo "Please create a feature branch first:"
  echo "  git checkout -b initiative/[name]"
  exit 1
fi
```

### PR Management

**Opening PRs:**
```bash
gh pr create \
  --title "[Type]: [Description]" \
  --body "$(cat <<'EOF'
## Changes
- Added/updated [description]

## Documentation Updates
- [ ] Updated indexes
- [ ] Validated cross-references
- [ ] Ran doc-review

## Related
- Initiative: [name]
- Affected repos: [list]
EOF
)"
```

**PR Types:**
- `Initiative: [Name]` - Initiative planning documents
- `Docs: [Description]` - General documentation updates
- `Repo: [Name]` - Repository documentation
- `Arch: [Description]` - Architecture documentation

### When to Work on Main

**ONLY these scenarios allow main branch work:**
- `/initiative-create-issues` - After initiative PR is merged
- Emergency documentation fixes (with explicit approval)

### Committing Changes

**CRITICAL RULE: NEVER commit without the user running `/commit`**

Claude should **NEVER**:
- Run `git commit` directly via Bash tool
- Commit as part of any other command workflow
- Commit automatically after file changes
- Commit without explicit `/commit` command from user

The **ONLY** way to create commits is:
```bash
# User stages files
git add [files]

# User runs commit command
/commit
```

**The `/commit` command:**
- Analyzes staged changes
- Generates appropriate conventional commit message
- Shows the commit message to user
- Creates the commit immediately (running `/commit` IS the permission)

**Why this matters:**
- User controls exactly when commits happen
- Ensures proper commit message format
- Maintains clean git history
- Prevents accidental or premature commits

**If you need to suggest committing:**
- Tell the user: "You can commit these changes with `/commit`"
- Never run git commit yourself
- Never ask permission to commit (running `/commit` is the permission)

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

- **Total Initiatives**: 28 across 8 categories
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
- `/initiative-brainstorm-design [idea]` - Create non-technical design specification (designers/PMs)
- `/initiative-brainstorm-technical [initiative-name]` - Add technical architecture requirements (architects)
- `/initiative-plan [initiative-name]` - Break down initiative into implementation phases
- `/initiative-create-issues [initiative-name]` - Create GitHub milestone and issues (after PR merge)

### Issue Management
- `/issue-identify [initiative-name|filter]` - Find next issue to work on
- `/issue-analyze [issue-number]` - Analyze requirements and dependencies in detail

### Quality Assurance
- `/doc-review [path]` - Comprehensive documentation review

### Git Workflow
- `/commit` - Create commit with properly formatted conventional commit message
  - **CRITICAL**: This is the ONLY way Claude should create commits
  - Analyzes staged changes and generates appropriate message
  - Running this command IS the user's permission to commit
  - Commits immediately without additional confirmation

**Typical Workflow (Branch-Based):**

1. **Design Phase** - `/initiative-brainstorm-design [idea]`
   - Non-technical specification for designers/product managers
   - Uses `docs-finder` agent to check for existing initiatives
   - Creates feature branch `initiative/[name]`
   - Saves to `initiatives/_planning/[name].md`
   - Uses `doc-updater` agent to update indexes after creation
   - Uses `architecture-validator` agent to validate the spec
   - Opens PR for the initiative

2. **Technical Phase** - `/initiative-brainstorm-technical [initiative-name]`
   - Technical architecture for software architects
   - Works within existing initiative branch
   - Uses `docs-finder` agent to discover related documentation
   - Adds technical requirements to `initiatives/_planning/[name].md`
   - Uses `doc-updater` agent to update indexes
   - Uses `architecture-validator` agent to validate technical spec
   - Updates PR with technical additions

3. **Planning Phase** - `/initiative-plan [initiative-name]`
   - Detailed implementation breakdown
   - Works within existing initiative branch
   - Uses `docs-finder` agent to discover related documentation
   - Saves to `initiatives/_planning/[name]-plan.md`
   - Uses `doc-updater` agent to update effort estimates and timeline
   - Uses `architecture-validator` agent to validate completeness
   - Updates PR with implementation plan

4. **Review and Merge** (Manual)
   - Team reviews complete initiative (design + technical + plan)
   - Approve and merge PR to main
   - Initiative documents now on main branch in `_planning/`

5. **Issue Creation** - `/initiative-create-issues [initiative-name]`
   - **Must run on main branch** (after PR merge)
   - Asks which repository to create issues in (for multi-repo initiatives)
   - **Moves files** from `_planning/` to `initiatives/[name]/` subdirectory
   - Creates GitHub milestone and issues in chosen repository
   - Creates `initiatives/[name]/issues.md` tracking document
   - Uses `doc-updater` agent to update status and references
   - Uses `architecture-validator` agent to verify everything

6. **Development Workflow:**
   - `/issue-identify` - Find next issue to work on
   - `/issue-analyze [issue-number]` - Clarify requirements before starting
   - Work on implementation in appropriate repository
   - `/doc-review [changed-files]` - Review docs before committing (uses `architecture-validator`)

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
