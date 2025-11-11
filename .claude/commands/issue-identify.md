Identify the next Asana task to work on for the MyStage platform. Can filter by initiative tag, project, or work with all open tasks.

## Command Usage
```
/issue-identify [initiative-name|project-name]
```
Where the argument can be:
- An initiative name (e.g., `notification-system`, `entity-deduplication`) - will search by `#initiative-name` tag
- A project name (e.g., `Admin Portal`, `Data Pipeline`) - will search in that project
- Empty to show all incomplete tasks assigned to you

## Steps

### STEP 1: DETERMINE FILTER TYPE

Analyze the argument to determine how to search:
- If argument contains hyphens (e.g., "notification-system"), treat as initiative tag: `#[argument]`
- If argument matches a project name (e.g., "Admin Portal"), search that specific project
- If no argument provided, show all your incomplete tasks across all projects

### STEP 2: FETCH ASANA TASKS

Use the Asana MCP integration to fetch tasks:

**For initiative tag search:**
```
Use mcp__asana__asana_search_tasks:
- workspace: 426521350405896
- assignee_any: "me"
- completed: false
- text: "#[initiative-name]"
- opt_fields: "name,due_on,projects.name,tags.name,custom_fields,memberships.section.name"
```

**For project-based search:**
First get project sections to understand workflow, then get tasks:
```
1. Get project sections with mcp__asana__asana_get_project_sections
2. Get tasks with mcp__asana__asana_get_tasks for that project
```

**For all tasks (no filter):**
```
Use mcp__asana__asana_search_tasks:
- workspace: 426521350405896
- assignee_any: "me"
- completed: false
- opt_fields: "name,due_on,projects.name,tags.name,custom_fields,memberships.section.name"
```

### STEP 3: ANALYZE TASK DETAILS

For each task returned, extract:
- **Name**: Task title
- **Project**: Which Asana project it's in
- **Section**: Which workflow section (Backlog, Ready, In Progress, In Review, Done)
- **Tags**: Initiative and repository tags
- **Custom Fields**: Priority, Est. Hours, % Complete
- **Due Date**: If set
- **Assignee**: Who it's assigned to

### STEP 4: PRIORITIZE TASKS

Rank tasks considering:

**Primary Factors:**
1. **Section Status**:
   - "Ready" section tasks are highest priority (ready to start)
   - "In Progress" tasks (if you have any, finish those first)
   - "Backlog" tasks (not yet ready)
   - Skip "In Review" or "Done" sections

2. **Priority Custom Field**:
   - High priority first
   - Medium priority second
   - Low priority last

3. **Implementation Order**:
   - Look for "Phase X.Y" in task name
   - Earlier phase numbers first (Phase 1 before Phase 2)
   - Earlier task numbers first (Task 1.1 before Task 1.2)

4. **Dependencies**:
   - Check task description for "Dependencies" section
   - Prefer tasks with no blocking dependencies
   - Prioritize tasks that unblock other work

5. **Due Dates**:
   - Tasks with earlier due dates prioritized
   - Overdue tasks flagged

**Secondary Factors:**
6. **Estimated Hours**: Smaller tasks for quick wins
7. **Project Context**: Group related work together

### STEP 5: DISPLAY RESULTS

For each relevant task, show:
```
Task: [Task Name]
Project: -MS D Admin Portal
Section: Ready
Tags: #notification-system, #mystage-admin-interface
Priority: High
Est. Hours: 8
Due: 2025-11-15
Phase/Task: Phase 1.1
Asana URL: [url]
Preview: [First 100 chars of description]
```

### STEP 6: MAKE RECOMMENDATION

Present the best next task:
```
RECOMMENDED NEXT TASK:

Task: Phase 1.1: Add notification preferences table
Project: -MS D Data Pipeline
Section: Ready
Priority: High
Est. Hours: 8
Tags: #notification-system, #mystage-databases
Reason: High priority, in Ready section, no blocking dependencies, earliest phase

View in Asana: [url]

NEXT UP (In Order):
1. Phase 1.2: Build notification preferences UI - Blocked by Phase 1.1
2. Phase 1.3: Create notification API endpoints - Blocked by Phase 1.1

OTHER READY TASKS (Different Initiatives):
- [Entity Deduplication] Phase 2.1: Schema Analysis - Ready, Medium priority
```

### STEP 7: WORKFLOW CONTEXT

Provide context about task workflow:
- **Backlog**: Not yet ready to start (missing dependencies, unclear requirements)
- **Ready**: All dependencies met, requirements clear, ready to begin
- **In Progress**: Currently being worked on
- **In Review**: Awaiting code review or approval
- **Done**: Completed and verified

Suggest moving tasks between sections as appropriate.

### STEP 8: NO MATCHES HANDLING

If no tasks match the filter:
- Check if initiative tag exists: search for the tag name
- Suggest available initiatives: show common tags
- Offer to show all open tasks instead
- Check if all tasks for that initiative are complete

### STEP 9: FOLLOW-UP

Ask if the user wants to:
- Analyze the recommended task in detail (use `/issue-analyze`)
- Start working on the task immediately
- Move a task from Backlog to Ready
- See related documentation to review first
- Filter by a different initiative or project
