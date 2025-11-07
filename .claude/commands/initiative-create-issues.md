Create a GitHub milestone and issues for an initiative based on the implementation plan. This generates a JSON file with all issues and a Python script to create them in batch.

## Command Usage
```
/initiative-create-issues [initiative-name]
```

**Prerequisites:**
- Initiative PR has been merged to main
- Initiative specification exists: `initiatives/_planning/[initiative-name].md`
- Implementation plan exists: `initiatives/_planning/[initiative-name]-plan.md`

**CRITICAL**: This command must be run from the main branch after the initiative PR has been merged.

## Process

### STEP 0: VERIFY ON MAIN BRANCH

This command must only run on main branch after the initiative PR is merged:

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Must be on main
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "ERROR: This command must be run from the main branch"
  echo "Current branch: $CURRENT_BRANCH"
  echo ""
  echo "WORKFLOW:"
  echo "1. Ensure initiative PR is approved and merged"
  echo "2. Switch to main: git checkout main"
  echo "3. Pull latest: git pull origin main"
  echo "4. Run: /initiative-create-issues $ARGUMENTS"
  echo ""
  echo "WHY: Initiative files must be on main before creating issues"
  echo "     Issues will reference the merged specification and plan"
  exit 1
fi

# Ensure main is up to date
git pull origin main
```

### STEP 1: VERIFY PREREQUISITES

Check that required documents exist on main branch:
```bash
# Check for initiative spec
test -f initiatives/_planning/$ARGUMENTS.md

# Check for implementation plan
test -f initiatives/_planning/$ARGUMENTS-plan.md
```

If either is missing, suggest running:
- `/initiative-brainstorm-design [initiative-name]` - Create design spec
- `/initiative-brainstorm-technical [initiative-name]` - Add technical architecture
- `/initiative-plan [initiative-name]` - Create implementation plan

### STEP 2: READ IMPLEMENTATION PLAN

Parse the plan document to extract:
- **Initiative Overview**: Summary and scope
- **Phases**: High-level phases (Phase 1, Phase 2, etc.)
- **Tasks**: Individual tasks within each phase (Task 1.1, 1.2, etc.)
- **Subtasks**: Implementation details under each task
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

```bash
# Create subdirectory
mkdir -p initiatives/$ARGUMENTS

# Move files
mv initiatives/_planning/$ARGUMENTS.md initiatives/$ARGUMENTS/
mv initiatives/_planning/$ARGUMENTS-plan.md initiatives/$ARGUMENTS/

echo "Moved initiative to: initiatives/$ARGUMENTS/"
```

### STEP 5: GENERATE ISSUES JSON

Create `initiatives/$ARGUMENTS/issues.json` with all issues from the implementation plan.

**JSON Structure:**
```json
{
  "initiative": "[Initiative Name]",
  "milestone": "[Initiative Name]",
  "target_repo": "[repo-name]",
  "project_number": 3,
  "project_owner": "clintdoriot",
  "issues": [
    {
      "title": "Phase 1.1: [Task Name]",
      "body": "## Initiative\n[Initiative Name]\n\n## Description\n[Task description]\n\n## Deliverables\n- [ ] Item 1\n- [ ] Item 2\n\n## Effort\n- Size: [S/M/L]\n- Time: [estimate]\n\n## Related\n- Spec: `initiatives/[name]/[name].md`\n- Plan: `initiatives/[name]/[name]-plan.md`"
    }
  ]
}
```

**Issue Title Format:**
```
Phase X.Y: [Task Name]
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
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

## Dependencies
[List any task dependencies]

## Effort Estimate
- **Size**: [XS/S/M/L/XL]
- **Estimated Time**: [days/weeks]
- **Complexity**: [Low/Medium/High]

## Implementation Notes
[Any important implementation details from plan]

## Related Documentation
- Initiative spec: `initiatives/[name]/[name].md`
- Implementation plan: `initiatives/[name]/[name]-plan.md`
```

**Generate one issue per task** in the implementation plan. Parse the plan systematically:
1. Identify all phases
2. For each phase, identify all tasks
3. Extract task details (description, deliverables, effort, dependencies)
4. Generate issue JSON object

Save to: `initiatives/$ARGUMENTS/issues.json`

### STEP 6: NO SCRIPT NEEDED

Issues will be created using the shared script at `scripts/create-issues.py`.

### STEP 7: CREATE TRACKING DOCUMENT

Create `initiatives/$ARGUMENTS/issues-tracking.md`:

```markdown
# [Initiative Name] - Issue Tracking

**Milestone**: [Milestone Name]
**Repository**: [target-repo]
**Created**: [Date]
**Status**: Active

## Issues File

All issues are defined in: `issues.json`

To create the issues in GitHub:
```bash
python scripts/create-issues.py initiatives/[initiative-name]/issues.json
```

## Progress

Track milestone progress at:
https://github.com/[target-repo]/milestone

View in project:
https://github.com/users/clintdoriot/projects/3

## Notes

- Issues created from implementation plan
- All issues added to milestone: [Milestone Name]
- All issues added to GitHub Project #3
```

### STEP 8: PROVIDE NEXT STEPS

Show the user what was created and how to proceed:

```
✅ INITIATIVE SETUP COMPLETE

Created files:
- initiatives/$ARGUMENTS/$ARGUMENTS.md (moved from _planning)
- initiatives/$ARGUMENTS/$ARGUMENTS-plan.md (moved from _planning)
- initiatives/$ARGUMENTS/issues.json (generated)
- initiatives/$ARGUMENTS/issues-tracking.md (tracking doc)

NEXT STEPS:

1. Review the issues:
   cat initiatives/$ARGUMENTS/issues.json

2. Edit if needed:
   - Adjust issue titles
   - Refine descriptions
   - Add/remove issues

3. Create the GitHub issues:
   python scripts/create-issues.py initiatives/$ARGUMENTS/issues.json

   This will:
   - Ask for confirmation once
   - Create milestone in [target-repo]
   - Create all issues from issues.json in batch
   - Add issues to GitHub Project #3

4. Track progress:
   - Milestone: https://github.com/[target-repo]/milestone
   - Project: https://github.com/users/clintdoriot/projects/3
```

---

**Arguments**: $ARGUMENTS
