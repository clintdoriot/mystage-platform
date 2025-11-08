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

### STEP 3: PARSE REPOSITORY AND TEAM ASSIGNMENTS

Parse the implementation plan to extract the **Primary Repository** and **Team** for each task:
- Look for the "REPOSITORY/LOCATION" section in each task
- Extract the "Primary Repository" field
- Extract the "Team" field (Backend, Frontend, or Admin)
- Build a mapping of task → repository + team
- Identify all unique repositories that will have issues created

**Repository Name Normalization:**
Map common variations to full GitHub repo names:
- "event-sourcing" → "clintdoriot/mystage-event-sourcing"
- "admin-interface" → "clintdoriot/mystage-admin-interface"
- "databases" → "clintdoriot/mystage-databases"
- "app-backend" → "clintdoriot/mystage-app-backend"
- "platform" → "clintdoriot/mystage-platform"
- etc.

**Validation:**
- Each task MUST have a Primary Repository specified
- Each task MUST have a Team specified (Backend, Frontend, or Admin)
- If any task is missing repository or team, stop and report the error
- Suggest re-running `/initiative-plan` to fix the issue

**Summary:**
After parsing, show the user a summary:
```
Initiative: [Name]
Total Tasks: [N]

Repositories Affected:
- clintdoriot/mystage-event-sourcing: [N] issues
- clintdoriot/mystage-admin-interface: [N] issues
- clintdoriot/mystage-platform: [N] issues

Teams:
- Backend: [N] issues
- Frontend: [N] issues
- Admin: [N] issues

Project: #3 (@clintdoriot)
All issues will be added to Project #3 with Initiative custom field set
```

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
  "project_number": 3,
  "project_owner": "clintdoriot",
  "issues": [
    {
      "repository": "clintdoriot/mystage-event-sourcing",
      "team": "Backend",
      "priority": "P1 - High",
      "size": "M",
      "title": "Phase 1.1: [Task Name]",
      "body": "## Initiative\n[Initiative Name]\n\n## Description\n[Task description]\n\n## Deliverables\n- [ ] Item 1\n- [ ] Item 2\n\n## Effort\n- Size: M\n- Time: [estimate]\n\n## Related\n- Spec: `initiatives/[name]/[name].md`\n- Plan: `initiatives/[name]/[name]-plan.md`"
    },
    {
      "repository": "clintdoriot/mystage-admin-interface",
      "team": "Admin",
      "priority": "P2 - Medium",
      "size": "S",
      "title": "Phase 1.2: [Task Name]",
      "body": "..."
    }
  ]
}
```

**Key Fields:**
- `initiative`: Initiative name (will be set as custom field "Initiative" in Project #3)
- `repository`: Which repo each issue belongs to
- `team`: Backend, Frontend, or Admin (will be set as custom field "Team" in Project #3)
- `priority`: Optional - P0-Critical, P1-High, P2-Medium, P3-Low (will be set as custom field "Priority")
- `size`: Optional - XS, S, M, L, XL (will be set as custom field "Size")

**Note**: The script will automatically create the issue option for Initiative if it doesn't exist in Project #3. For Priority and Size, they're optional and can be set later manually if not included in the JSON.

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
3. Extract task details (description, deliverables, effort, dependencies, repository, team)
4. Generate issue JSON object with repository and team fields

Save to: `initiatives/$ARGUMENTS/issues.json`

### STEP 6: NO SCRIPT NEEDED

Issues will be created using the shared script at `scripts/create-issues.py`.

**NOTE**: The script currently creates issues and adds them to Project #3, but **does not** automatically set custom fields (Initiative, Team, Priority, Size).

**Custom fields must be:**
1. Configured in Project #3 settings first (Initiative, Team, Priority, Size)
2. Set manually in the Project after issue creation, OR
3. Set via GitHub API (future enhancement to automate this)

The `initiative` and `team` values from issues.json can be used to bulk-set custom fields via API or manually.

### STEP 7: CREATE TRACKING DOCUMENT

Create `initiatives/$ARGUMENTS/issues-tracking.md`:

```markdown
# [Initiative Name] - Issue Tracking

**Milestone**: [Milestone Name]
**Repositories**: [List of all repos with issues]
**Created**: [Date]
**Status**: Active

## Issues File

All issues are defined in: `issues.json`

To create the issues in GitHub:
```bash
python scripts/create-issues.py initiatives/[initiative-name]/issues.json
```

This will:
- Create milestone "[Milestone Name]" in each affected repository
- Create issues in their designated repositories
- Add all issues to GitHub Project #3

## Progress

Track milestones:
- [repo-1]: https://github.com/[repo-1]/milestone
- [repo-2]: https://github.com/[repo-2]/milestone

View all issues in project:
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
   - Create milestone "[Initiative Name]" in each affected repository
   - Create all issues in their designated repositories
   - Add all issues to GitHub Project #3

4. Track progress:
   - View all issues in Project: https://github.com/users/clintdoriot/projects/3
   - View milestones in each repository
```

---

**Arguments**: $ARGUMENTS
