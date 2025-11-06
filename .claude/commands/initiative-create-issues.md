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

### STEP 3: CREATE MILESTONE

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

### STEP 4: CREATE LABELS

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

### STEP 5: GENERATE ISSUES FROM PLAN

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
gh issue create \
  --title "[Issue Title]" \
  --body "[Issue Body]" \
  --milestone "[Milestone Name]" \
  --label "initiative:$ARGUMENTS" \
  --label "[priority-label]" \
  --label "[type-labels]"
```

### STEP 6: LINK DEPENDENCIES

After all issues are created:
1. Go through created issues
2. For each issue with dependencies, add comment:
```bash
gh issue comment [issue-number] --body "Depends on: #[dependency-issue-number]"
```
3. Update dependency issues with "Blocks: #[blocked-issue]" comments

### STEP 7: CREATE ISSUE TRACKING DOCUMENT

Create a tracking document in the initiative directory:
`initiatives/_planning/[initiative-name]-issues.md`

```markdown
# [Initiative Name] - Issue Tracking

**Milestone**: [Milestone Name]
**Created**: [Date]
**Status**: Planning / Active / Complete

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
- [Initiative Spec](initiatives/_planning/[initiative-name].md)
- [Implementation Plan](initiatives/_planning/[initiative-name]-plan.md)

## Progress
- **Total Issues**: [count]
- **Completed**: 0
- **In Progress**: 0
- **Blocked**: 0
- **Open**: [count]
```

### STEP 8: SUMMARY OUTPUT

Provide summary to user:

```
INITIATIVE ISSUES CREATED: [Initiative Name]

MILESTONE: [Milestone Name]
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

TRACKING DOCUMENT: initiatives/_planning/[initiative-name]-issues.md

NEXT STEPS:
1. Review issues for accuracy
2. Assign initial issues to team members
3. Start with: #X - Task 1.1 (no dependencies)
4. Use /issue-identify to find next work
5. Use /issue-analyze before starting each issue
```

### STEP 9: DOCUMENTATION UPDATES

Use the Task tool to launch the `doc-updater` agent to automatically update:
- Add issue tracking link to initiative spec
- Update `initiatives/README.md` with milestone link
- Update initiative status from Planning to Active
- Update `initiatives/timeline.md` if dates are set
- Ensure all cross-references are established

Then use the Task tool to launch the `architecture-validator` agent to verify:
- All documentation is properly cross-referenced
- Issue tracking document is complete
- Initiative status is correctly updated

### STEP 10: VERIFICATION

Verify all issues created correctly:
```bash
# List all issues in milestone
gh issue list --milestone "[Milestone Name]"

# Check labels are applied
gh issue list --label "initiative:$ARGUMENTS"
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
