Create a GitHub milestone and issues for an initiative based on the implementation plan. This breaks down an initiative into trackable, assignable issues.

## Command Usage
```
/initiative-create-issues [initiative-name]
```

**Prerequisites:**
- Initiative specification exists: `initiatives/_planning/[initiative-name].md`
- Implementation plan exists: `initiatives/_planning/[initiative-name]-plan.md`
- User confirms they want to create issues

## Process

### STEP 1: VERIFY PREREQUISITES

Check that required documents exist:
```bash
# Check for initiative spec
test -f initiatives/_planning/$ARGUMENTS.md

# Check for implementation plan
test -f initiatives/_planning/$ARGUMENTS-plan.md
```

If either is missing, suggest running:
- `/initiative-brainstorm [initiative-name]` - Create spec
- `/initiative-plan [initiative-name]` - Create plan

### STEP 2: READ IMPLEMENTATION PLAN

Parse the plan document to extract:
- **Initiative Overview**: Summary and scope
- **Phases**: High-level phases (Phase 1, Phase 2, etc.)
- **Tasks**: Individual tasks within each phase (Task 1.1, 1.2, etc.)
- **Dependencies**: Which tasks depend on others
- **Effort Estimates**: Size and time estimates
- **Repositories**: Which repos each task affects

### STEP 3: DETERMINE TARGET REPOSITORY

**For single-repo initiatives:**
- Issues go in the affected repository

**For multi-repo initiatives:**
Ask the user to choose the **primary repository** where most issues should be created:
- List affected repositories from the initiative spec
- Recommend the repository where most implementation work will happen
- Explain that some issues may need to be created in other repos manually

**Example prompt:**
```
This initiative affects multiple repositories:
- mystage-event-sourcing (primary - deduplication logic)
- mystage-admin-interface (secondary - review UI)

I recommend creating issues in: mystage-event-sourcing

Where would you like to create the GitHub milestone and issues?
1. mystage-event-sourcing (recommended)
2. mystage-admin-interface
3. mystage-platform (for cross-cutting planning work)
```

Store the chosen repository for use in later steps.

### STEP 4: MOVE TO ACTIVE SUBDIRECTORY

Before creating issues, move the initiative from planning to active:

**Create subdirectory:**
```bash
mkdir -p initiatives/$ARGUMENTS
```

**Move files:**
```bash
# Move spec
mv initiatives/_planning/$ARGUMENTS.md initiatives/$ARGUMENTS/

# Move plan
mv initiatives/_planning/$ARGUMENTS-plan.md initiatives/$ARGUMENTS/

# Create issues tracking document location
# (will be created in STEP 8)
```

**Update internal references if needed** (links within docs may need updating).

### STEP 5: CREATE MILESTONE

Ask user for milestone details:
- **Milestone Name**: e.g., "Entity Deduplication System" or "Database Schema Tooling"
- **Due Date**: Target completion date (optional)
- **Description**: Brief description of what this milestone delivers

Create milestone:
```bash
gh issue create --milestone "[milestone-name]" --title "[milestone-name]" --body "[description]"
```

Or if you prefer to use the milestone API:
```bash
gh api repos/:owner/:repo/milestones -f title="[milestone-name]" -f description="[description]" -f due_on="[date]"
```

### STEP 6: CREATE LABELS

**Note**: Labels are created in the chosen target repository.


Ensure necessary labels exist:
```bash
# Initiative-specific label
gh label create "initiative:$ARGUMENTS" --description "Issues related to $ARGUMENTS initiative" --color "0366d6" || true

# Standard labels (create if they don't exist)
gh label create "documentation" --description "Documentation updates" --color "d4c5f9" || true
gh label create "planning" --description "Planning and specification work" --color "fbca04" || true
gh label create "architecture" --description "Architecture decisions and documentation" --color "d876e3" || true
gh label create "high-priority" --description "High priority work" --color "d93f0b" || true
gh label create "medium-priority" --description "Medium priority work" --color "fbca04" || true
gh label create "low-priority" --description "Low priority work" --color "0e8a16" || true
```

### STEP 7: GENERATE ISSUES FROM PLAN

**Create issues in the target repository** (determined in STEP 3).


For each task in the implementation plan, create a GitHub issue:

**Issue Title Format:**
```
[Initiative Name] Phase X.Y: [Task Name]
```

**Issue Body Template:**
```markdown
## Initiative
[Initiative Name] - [Brief description]

## Phase/Task
Phase X: [Phase Name]
Task X.Y: [Task Name]

## Description
[Task description from plan]

## Repository/Location
[Which repos or platform areas this affects]

## Deliverables
[List of deliverables from plan]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Dependencies
Depends on: [#issue-number] (if applicable)
Blocks: [Will be filled in after dependent issues created]

## Effort Estimate
- **Size**: [XS/S/M/L/XL]
- **Estimated Time**: [days/weeks]
- **Complexity**: [Low/Medium/High]
- **Risk**: [🟢/🟡/🔴]

## Implementation Approach
[Brief approach from plan]

## Clarifications Needed
[Questions from plan that need answers]

## Documentation to Review
[Relevant docs to read before starting]

---
Part of milestone: [Milestone Name]
Initiative spec: `initiatives/_planning/[initiative-name].md`
Implementation plan: `initiatives/_planning/[initiative-name]-plan.md`
```

**Create each issue:**
```bash
# Change to target repository directory first (if not platform repo)
cd /Users/clint/Projects/mystage/[target-repo]

gh issue create \
  --title "[Issue Title]" \
  --body "[Issue Body]" \
  --milestone "[Milestone Name]" \
  --label "initiative:$ARGUMENTS" \
  --label "[priority-label]" \
  --label "[type-labels]"
```

**For multi-repo initiatives:**
- Create most issues in primary repo
- Note in tracking document which issues belong in other repos
- User can create those issues manually or you can help create them in other repos

### STEP 8: LINK DEPENDENCIES

After all issues are created:
1. Go through created issues
2. For each issue with dependencies, add comment:
```bash
gh issue comment [issue-number] --body "Depends on: #[dependency-issue-number]"
```
3. Update dependency issues with "Blocks: #[blocked-issue]" comments

### STEP 9: CREATE ISSUE TRACKING DOCUMENT

Create a tracking document in the initiative subdirectory:
`initiatives/[initiative-name]/issues.md`

**Note**: Initiative is now in its own subdirectory since it's active.

```markdown
# [Initiative Name] - Issue Tracking

**Milestone**: [Milestone Name]
**Repository**: [Target repository name]
**Created**: [Date]
**Status**: Active

## Issues by Phase

### Phase 1: [Phase Name]
- [ ] #X - Task 1.1: [Task Name] (Status: Open, Priority: High)
- [ ] #Y - Task 1.2: [Task Name] (Status: Open, Priority: High)

### Phase 2: [Phase Name]
- [ ] #Z - Task 2.1: [Task Name] (Status: Open, Priority: Medium)

## Dependency Graph

```
#X → #Y → #Z
     ↓
    #A → #B
```

## Quick Links
- [Milestone on GitHub]([url])
- [Initiative Spec]([initiative-name].md)
- [Implementation Plan]([initiative-name]-plan.md)

## Notes
- **Repository**: Most issues created in [target-repo]
- **Multi-repo**: [If applicable, list issues that should be created in other repos]

## Progress
- **Total Issues**: [count]
- **Completed**: 0
- **In Progress**: 0
- **Blocked**: 0
- **Open**: [count]
```

### STEP 10: SUMMARY OUTPUT

Provide summary to user:

```
INITIATIVE ISSUES CREATED: [Initiative Name]

MOVED TO ACTIVE:
- initiatives/[initiative-name]/[initiative-name].md (spec)
- initiatives/[initiative-name]/[initiative-name]-plan.md (plan)
- initiatives/[initiative-name]/issues.md (tracking)

MILESTONE: [Milestone Name]
- Repository: [target-repo]
- URL: [milestone-url]
- Due Date: [date]

ISSUES CREATED:
Phase 1: [Phase Name]
  ✓ #X - Task 1.1: [Task Name] (Priority: High, Size: M)
  ✓ #Y - Task 1.2: [Task Name] (Priority: High, Size: L)

Phase 2: [Phase Name]
  ✓ #Z - Task 2.1: [Task Name] (Priority: Medium, Size: M)

TOTAL: [count] issues created

DEPENDENCIES LINKED:
- #Y depends on #X
- #Z depends on #Y

LABELS APPLIED:
- initiative:[initiative-name]
- [priority labels]
- [type labels]

TRACKING DOCUMENT: initiatives/[initiative-name]/issues.md

GITHUB REPOSITORY: [target-repo-name]

NEXT STEPS:
1. Review issues for accuracy
2. Assign initial issues to team members
3. Start with: #X - Task 1.1 (no dependencies)
4. Use /issue-identify to find next work
5. Use /issue-analyze before starting each issue
```

### STEP 11: DOCUMENTATION UPDATES

Use the Task tool to launch the `doc-updater` agent to automatically update:
- Update `initiatives/README.md`:
  - Move initiative from `_planning/` reference to active subdirectory
  - Update status from Planning to Active
  - Add milestone link
- Update `initiatives/timeline.md` if dates are set
- Ensure all cross-references point to new subdirectory location

Then use the Task tool to launch the `architecture-validator` agent to verify:
- All documentation is properly cross-referenced
- Issue tracking document is complete
- Initiative status is correctly updated
- File moves were successful

### STEP 12: VERIFICATION

Verify all issues created correctly:
```bash
# Change to target repository
cd /Users/clint/Projects/mystage/[target-repo]

# List all issues in milestone
gh issue list --milestone "[Milestone Name]"

# Check labels are applied
gh issue list --label "initiative:$ARGUMENTS"
```

Verify file moves:
```bash
# Verify subdirectory exists
ls -la initiatives/[initiative-name]/

# Verify files moved
test -f initiatives/[initiative-name]/[initiative-name].md
test -f initiatives/[initiative-name]/[initiative-name]-plan.md
test -f initiatives/[initiative-name]/issues.md
```

## Options

**Dry Run Mode:**
Add `--dry-run` to preview issues without creating:
```
/initiative-create-issues [initiative-name] --dry-run
```

**Custom Milestone Name:**
Specify milestone name explicitly:
```
/initiative-create-issues [initiative-name] --milestone "Custom Milestone Name"
```

## Notes

- Issues are created in order (Phase 1.1, 1.2, etc.)
- Dependencies are linked after all issues exist
- Labels help filter and organize work
- Tracking document makes progress visible
- Issues can be refined after creation based on learnings
