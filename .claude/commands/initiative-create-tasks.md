Create Asana tasks for an initiative based on the implementation plan. This creates tasks directly in Asana via the MCP integration.

## Command Usage
```
/initiative-create-tasks [initiative-name]
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
  echo "4. Run: /initiative-create-tasks $ARGUMENTS"
  echo ""
  echo "WHY: Initiative files must be on main before creating tasks"
  echo "     Tasks will reference the merged specification and plan"
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

Parse the plan document (`initiatives/_planning/$ARGUMENTS-plan.md`) to extract:
- **Initiative Overview**: Summary and scope
- **Phases**: High-level phases (Phase 1, Phase 2, etc.)
- **Tasks**: Individual tasks within each phase (Task 1.1, 1.2, etc.)
- **Task Details**: For each task, extract:
  - Task name/title
  - Description and scope
  - Primary Project (which Asana project)
  - Repository (which repos affected)
  - Priority (High/Medium/Low)
  - Estimated Hours
  - Deliverables
  - Dependencies
  - Acceptance criteria

### STEP 3: PARSE PROJECT ASSIGNMENTS

Parse the implementation plan to extract the **Primary Project** for each task:
- Look for the "PROJECT/REPOSITORY" section in each task
- Extract the "Primary Project" field
- Extract "Repository" field
- Extract "Priority" and "Estimated Hours"
- Build a mapping of task → Asana project

**Project Name to ID Mapping:**
Map project names to Asana project GIDs:
- "-MS D Data Pipeline" → 1209042780967623
- "-MS D 1.3 Sprint" → 1208479363218703
- "-MS D Pro Dashboard" → 1209189575962477
- "-MS D Fan Experience App" → 1208791609685501
- "-MS D Admin Portal" → 1208833533751404

**Validation:**
- Each task MUST have a Primary Project specified
- Each task MUST have Repository specified
- If any task is missing required fields, stop and report the error
- Suggest re-running `/initiative-plan` to fix the issue

**Summary:**
After parsing, show the user a summary:
```
Initiative: [Name]
Total Tasks: [N]

Asana Projects:
- -MS D Data Pipeline: [N] tasks
- -MS D Admin Portal: [N] tasks
- -MS D 1.3 Sprint: [N] tasks

Repositories:
- mystage-databases: [N] tasks
- mystage-admin-interface: [N] tasks
- mystage-event-sourcing: [N] tasks
```

### STEP 4: MOVE TO ACTIVE SUBDIRECTORY

Before creating tasks, move the initiative from planning to active:

```bash
# Create subdirectory
mkdir -p initiatives/$ARGUMENTS

# Move files
mv initiatives/_planning/$ARGUMENTS.md initiatives/$ARGUMENTS/
mv initiatives/_planning/$ARGUMENTS-plan.md initiatives/$ARGUMENTS/

echo "Moved initiative to: initiatives/$ARGUMENTS/"
```

### STEP 5: CREATE ASANA TASKS

For each task in the implementation plan, create an Asana task using the MCP integration.

**For each task:**

1. **Map project name to GID** using the mapping above
2. **Prepare task name** using format: `[[initiative-name] X.Y] [Task Name]`
   - Example: `[notification-system 1.1] Design Firestore Schema & Indexes`
   - This embeds the initiative name and task number in the task name itself

3. **Extract ALL task details from the plan** including:
   - SCOPE OF WORK section (complete description)
   - REPOSITORY/LOCATION (primary repo, team, also affects)
   - EXPECTED OUTPUTS (deliverables and acceptance criteria)
   - PREREQUISITES (dependencies and required decisions)
   - CLARIFICATION NEEDED (questions to answer before starting)
   - IMPLEMENTATION APPROACH (research/design/implementation/review phases)
   - ACCEPTANCE CRITERIA (checklist items)
   - EFFORT ESTIMATE (size, time, complexity, risk)

4. **Prepare comprehensive task description** in markdown format:
   ```markdown
   ## Scope of Work
   [Copy SCOPE OF WORK section from plan - the complete task description]

   ## Repository
   **Primary Repository**: [repo-name]
   **Team**: [team-name]
   **Also Affects**: [other repos if any]

   ## Expected Outputs

   **Deliverables:**
   [Copy complete deliverables list from plan]

   **Acceptance Criteria:**
   [Copy acceptance criteria from EXPECTED OUTPUTS section]

   ## Prerequisites

   **Dependencies from previous tasks:**
   [List dependencies - reference other task numbers]

   **Required decisions:**
   [Copy required decisions from plan]

   ## Clarification Needed
   [Copy CLARIFICATION NEEDED section from plan if present]

   ## Implementation Approach

   [Copy complete IMPLEMENTATION APPROACH section from plan, including:
   - Research phase
   - Design phase
   - Implementation phase
   - Review phase]

   ## Acceptance Criteria Checklist
   [Copy complete checklist from ACCEPTANCE CRITERIA section]

   ## Effort Estimate
   - **Size**: [XS/S/M/L/XL]
   - **Estimated Time**: [hours]
   - **Complexity**: [Low/Medium/High]
   - **Risk**: [🟢/🟡/🔴] [Risk description]
   - **Priority**: [High/Medium/Low]

   ## Related Documentation
   - Initiative spec: `initiatives/[name]/[name].md`
   - Implementation plan: `initiatives/[name]/[name]-plan.md`
   ```

   **IMPORTANT**: The task description should be comprehensive enough that an engineer can implement the task WITHOUT needing to read the full initiative spec or plan. Include ALL relevant schemas, configuration examples, implementation patterns, and technical details from the plan.

5. **Create the task** using `mcp__asana__asana_create_task`:
   - `name`: "[[initiative-name] X.Y] [Task Name]"
   - `project_id`: [Asana project GID from mapping]
   - `notes`: [Formatted description from above]

5. **Note about custom fields:**
   - Custom fields cannot be set via the current MCP integration during task creation
   - After all tasks are created, provide instructions for manually setting:
     - Priority custom field (High/Medium/Low)
     - Est. Hours custom field (number)

6. **Track created tasks:**
   - Store task GID, title, and project in memory
   - Will be used to generate tracking document

**Error Handling:**
- If task creation fails, log the error and continue with remaining tasks
- Report all failures at the end
- Provide option to retry failed tasks

### STEP 6: CREATE REFERENCE DOCUMENT

Create `initiatives/$ARGUMENTS/tasks-reference.md` as a simple reference to the created Asana tasks:

```markdown
# [Initiative Name] - Asana Tasks Reference

**Initiative**: [initiative-name]
**Created**: [Date]
**Total Tasks**: [N]

All tasks follow the naming convention: `[[initiative-name] X.Y] [Task Name]`

**To find all tasks:** Search Asana for `[[initiative-name]`

## Tasks by Project

### -MS D Data Pipeline ([N] tasks)
- [[initiative-name] 1.1] [Task Name] - [Asana URL] (GID: [gid])
- [[initiative-name] 1.2] [Task Name] - [Asana URL] (GID: [gid])

### -MS D Admin Portal ([N] tasks)
- [[initiative-name] 2.1] [Task Name] - [Asana URL] (GID: [gid])
- [[initiative-name] 2.2] [Task Name] - [Asana URL] (GID: [gid])

## Tasks by Repository

**mystage-databases**: Task 1.1, Task 2.3
**mystage-admin-interface**: Task 1.2, Task 3.1
**mystage-event-sourcing**: Task 1.1, Task 2.1

## Manual Setup Required

Due to MCP integration limitations, manually set these custom fields in Asana:

| Task | Priority | Est. Hours | Repository |
|------|----------|------------|------------|
| [[initiative-name] 1.1] [Name] | High | 8 | mystage-databases, mystage-event-sourcing |
| [[initiative-name] 1.2] [Name] | Medium | 16 | mystage-admin-interface |

Values are also documented in each task's description field.
```

### STEP 7: PROVIDE NEXT STEPS

Show the user what was created and how to proceed:

```
✅ INITIATIVE TASKS CREATED

Created files:
- initiatives/$ARGUMENTS/$ARGUMENTS.md (moved from _planning)
- initiatives/$ARGUMENTS/$ARGUMENTS-plan.md (moved from _planning)
- initiatives/$ARGUMENTS/tasks-reference.md (task reference)

Asana Tasks Created: [N]
- -MS D Data Pipeline: [N] tasks
- -MS D Admin Portal: [N] tasks
- -MS D 1.3 Sprint: [N] tasks
- [etc.]

NEXT STEPS:

1. Set custom fields in Asana:
   See initiatives/$ARGUMENTS/tasks-reference.md for the table of Priority and Est. Hours
   values to set manually in Asana (MCP limitations prevent automatic setting).

2. Organize tasks in Asana:
   - Tasks created in default "Backlog" section
   - Move to "Ready" when ready to start
   - Track progress through normal Asana workflow

3. Find all initiative tasks:
   Search Asana for `[[initiative-name]` to see all tasks across projects

4. Commit the reference document:
   git add initiatives/$ARGUMENTS/
   git commit -m "feat(initiative): create Asana tasks for $ARGUMENTS"
```

---

**Arguments**: $ARGUMENTS
