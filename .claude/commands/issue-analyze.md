Analyze an Asana task in detail to understand requirements, dependencies, and clarify any ambiguities before starting work.

## Command Usage
```
/issue-analyze [task-gid]
```

If no task GID is provided, will analyze the most recently identified task from `/issue-identify`.

## Analysis Process

### 1. Fetch Task Details

Use Asana MCP integration to get full task details:
```
mcp__asana__asana_get_task:
- task_id: [task-gid]
- opt_fields: "name,notes,tags.name,custom_fields,projects.name,memberships.section.name,due_on,assignee.name,followers.name,dependencies,dependents"
```

Extract key information:
- **Name**: Task title (often includes Phase X.Y prefix)
- **Description (notes)**: Full task details
- **Project**: Which Asana project/team owns this
- **Section**: Current workflow status (Backlog/Ready/In Progress/etc.)
- **Tags**: Initiative and repository tags
- **Custom Fields**: Priority, Est. Hours, % Complete
- **Due Date**: If set
- **Assignee**: Who owns this task
- **Dependencies**: What must be complete first (if supported by Asana)
- **Dependents**: What this unblocks (if supported by Asana)

### 2. Parse Task Description

The task description should follow this format (from `/initiative-create-issues`):
```markdown
## Initiative
[Initiative Name] - [Brief description]

## Phase/Task
Phase X: [Phase Name]
Task X.Y: [Task Name]

## Description
[Task description]

## Deliverables
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

## Dependencies
[List any task dependencies]

## Effort Estimate
- **Priority**: [High/Medium/Low]
- **Estimated Hours**: [hours]
- **Complexity**: [Low/Medium/High]

## Implementation Notes
[Important implementation details]

## Related Documentation
- Initiative spec: `initiatives/[name]/[name].md`
- Implementation plan: `initiatives/[name]/[name]-plan.md`
```

Parse each section to extract structured information.

### 3. Review Related Documentation

Before analyzing, read relevant platform documentation:

**Extract initiative name from tags or description, then read:**
- `initiatives/[initiative-name]/[initiative-name].md` - Initiative specification
- `initiatives/[initiative-name]/[initiative-name]-plan.md` - Full implementation plan
- `initiatives/[initiative-name]/tasks-tracking.md` - Task tracking document

**For repository-specific work:**
- `repos/[repo-name].md` - Current repo documentation (extract repo from tags)
- `architecture/system-overview.md` - Integration patterns
- `architecture/data-flow.md` - Data movement between systems

**For architecture work:**
- `architecture/README.md` - Documentation boundaries
- `architecture/system-overview.md` - Current architecture
- Related repo docs for affected systems

### 4. Dependency Analysis

**Check explicit dependencies:**
1. Look for "Dependencies" section in task description
2. Parse task references (Phase X.Y format or Asana task links)
3. For each dependency, check if it's in "Done" section
4. Flag any blocking dependencies that aren't complete

**Identify implicit dependencies:**
- Does this require architecture decisions not yet made?
- Are there related tasks in other projects that should coordinate?
- Does prerequisite documentation exist?
- Are there external factors (stakeholder decisions, approvals)?

**Check what this unblocks:**
- Look at related tasks in the same initiative (same initiative tag)
- Find tasks with higher phase/task numbers
- Prioritize if this task is blocking other work

### 5. Scope Clarification

**Deliverables Analysis:**
- What files/documents will be created or modified?
- What decisions need to be made and documented?
- What research or analysis is required?
- What cross-references need updating?

**Boundary Verification:**
- Is this appropriate for platform docs vs repo docs?
- Does it respect documentation boundaries?
- Are integration vs implementation concerns clear?
- Is the scope well-defined and focused?

### 6. Requirements Clarification

**Ask clarifying questions if needed:**

**For planning/spec tasks:**
- What business problem does this solve?
- What are the success criteria?
- Who are the stakeholders to consult?
- What's the priority relative to other work?
- What decisions must be made?

**For documentation tasks:**
- What's the target audience?
- What level of detail is appropriate?
- What related docs need updating?
- Are there examples or diagrams needed?

**For implementation tasks:**
- Which repositories will be modified?
- What integration points are affected?
- What are the constraints or requirements?
- Are there alternative approaches to consider?

### 7. Effort Validation

Compare task details to effort estimate:
- Does the described work match the estimated hours?
- Are there hidden complexities not accounted for?
- Should this be broken into smaller tasks?
- Is the timeline realistic given dependencies?

### 8. Risk Assessment

Identify risks and challenges:
- **Dependency risks**: Other work blocking this
- **Decision risks**: Unclear requirements or priorities
- **Coordination risks**: Multiple stakeholders, projects, or repos
- **Technical risks**: Architectural uncertainties
- **Timeline risks**: External dependencies or approvals

### 9. Output Format

```
TASK ANALYSIS: [Task Name]

## Summary
[Brief description of what this task accomplishes]

## Task Details
- **Asana GID**: [gid]
- **Project**: -MS D [Project Name]
- **Section**: [Backlog/Ready/In Progress/etc.]
- **Initiative**: #[initiative-name]
- **Repository Tags**: #[repo1], #[repo2]
- **Priority**: [High/Medium/Low]
- **Estimated Hours**: [number]
- **Due Date**: [date or "Not set"]
- **Assignee**: [name]
- **View in Asana**: [url]

## Initiative Context
- Initiative: [initiative name]
- Phase/Task: [Phase X.Y]
- Related Tasks: [count] tasks in this initiative
- Completion: [X/Y tasks complete]

## Dependencies

### Blocking This Task:
- [ ] Phase X.Y: [title] (Status: [section])
- [ ] [Decision/approval needed]

### This Task Blocks:
- Phase X.Y: [title]
- Phase X.Z: [title]

### Implicit Dependencies:
- [Architecture decision needed]
- [Coordination with other initiative]

## Scope & Deliverables

**Will Create/Modify:**
- `[file-path]` - [purpose]
- `[file-path]` - [purpose]

**Related Docs to Update:**
- `[file-path]` - [what to update]

**Decisions to Document:**
- [Decision point 1]
- [Decision point 2]

## Requirements

**Clear Requirements:**
- [Requirement 1]
- [Requirement 2]

**Clarifications Needed:**
1. [Question about requirement or approach]
2. [Ambiguity to resolve]
3. [Decision point that needs input]

## Acceptance Criteria

From task description:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

Additional verification:
- [ ] Related docs updated
- [ ] Cross-references working
- [ ] Documentation boundaries respected
- [ ] Task moved to "Done" section

## Effort Assessment

**Estimated Hours**: [from custom field]
**Priority**: [from custom field]
**Complexity**: [from task description]

**Effort Notes:**
- [Factor affecting effort]
- [Consideration for timeline]

## Risks & Challenges

**High Risk** 🔴:
- [Risk description]
  - Mitigation: [how to address]

**Medium Risk** 🟡:
- [Risk description]
  - Mitigation: [how to address]

## Approach Recommendation

**Suggested approach:**
1. [First step]
2. [Second step]
3. [Third step]

**Documentation to review before starting:**
- `[file-path]` - [why relevant]
- `[file-path]` - [why relevant]

**Stakeholders to consult:**
- [Person/role] - [what to clarify]

## Ready to Start?

**Prerequisites Complete:**
- [✓/✗] All dependencies in "Done" section
- [✓/✗] Requirements clear
- [✓/✗] Scope well-defined
- [✓/✗] No major blockers
- [✓/✗] Task in "Ready" or "In Progress" section

**Current Status:**
- Section: [current section]
- [Recommendation: Start immediately / Move to Ready first / Address clarifications / Wait for dependencies]

## Next Steps

**To begin work:**
1. [If not already] Move task to "In Progress" section in Asana
2. [First concrete action to take]
3. [Second action]

**When complete:**
1. Verify all acceptance criteria met
2. Update related documentation
3. Move task to "In Review" section
4. Request review from [stakeholder]
5. After approval, move to "Done"
```

### 10. Interactive Clarification

If requirements are unclear:
1. Identify specific ambiguities
2. Ask targeted questions (one at a time if needed)
3. Document answers for reference
4. Offer to update task description in Asana with clarifications

### 11. Follow-Up Actions

After analysis, offer to:
- Start working on the task if ready
- Move task to "Ready" section if dependencies are met
- Update task description with clarifications
- Identify and create dependency tasks if needed
- Suggest alternative sequencing if better approach exists
- Review related documentation before starting
