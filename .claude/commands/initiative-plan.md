**CRITICAL INSTRUCTION: THINK DEEPLY AND SYSTEMATICALLY**
You must spend significant mental effort breaking down the initiative. Take your time to understand the full scope, identify logical boundaries, and create a hierarchical structure that ensures nothing is missed.

**STEP 0: VERIFY BRANCH AND PREREQUISITES**

Verify we're on the correct initiative branch with both design and technical specs:

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Should be on initiative branch
if [[ ! "$CURRENT_BRANCH" =~ ^initiative/ ]]; then
  echo "ERROR: Must be on an initiative branch"
  echo "Current branch: $CURRENT_BRANCH"
  echo ""
  echo "Please switch to the initiative branch:"
  echo "  git checkout initiative/$ARGUMENTS"
  exit 1
fi

# Check if initiative spec exists
if [ ! -f "initiatives/_planning/$ARGUMENTS.md" ]; then
  echo "ERROR: Initiative specification not found"
  echo "Expected: initiatives/_planning/$ARGUMENTS.md"
  echo ""
  echo "Please run /initiative-brainstorm-design and /initiative-brainstorm-technical first"
  exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "WARNING: You have uncommitted changes"
  echo "Please commit changes before continuing"
  exit 1
fi
```

**STEP 1: DOCUMENTATION DISCOVERY**

First, use the Task tool to launch the `docs-finder` agent to discover existing documentation:
- Locate the initiative specification (`initiatives/_planning/$ARGUMENTS.md`)
- Find related initiatives and coordination points
- Identify affected repositories and their documentation
- Check for existing architecture patterns
- Review dependency relationships

The agent will return a list of relevant documentation to review.

After receiving the docs-finder results, review these key documents:
- Initiative specification (if exists)
- Architecture documentation (system-overview.md, dependencies.md)
- Repository documentation for affected repos
- Effort estimation framework

**STEP 2: INITIATIVE SPECIFICATION ANALYSIS**
Read the initiative specification from `initiatives/_planning/$ARGUMENTS.md`. If it doesn't exist, ask the user to run `/initiative-brainstorm` first.

Analyze the initiative spec thoroughly to understand:
- Core business requirements and platform impact
- Technical constraints and dependencies
- Integration points between systems/repos
- Affected repositories and their roles
- Success criteria and acceptance conditions
- Risks and mitigation strategies
- Potential blockers and decision points

**STEP 3: HIERARCHICAL INITIATIVE BREAKDOWN**

Create a three-tier hierarchy:

**3.1 HIGH-LEVEL PHASES**
Break the initiative into 3-5 major phases that represent logical completion milestones:
- Each phase should deliver demonstrable value or unblock work
- Phases should build upon each other logically
- Each phase should represent a natural checkpoint
- Consider: Planning/Design → Foundation → Implementation → Integration → Validation

**3.2 PHASE TASKS**
For each phase, identify 3-8 concrete tasks:
- Each task should be repo-specific or cross-cutting work
- Tasks within a phase should be ordered by dependencies
- Each task should have clear deliverables (specs, code, tests, docs)
- Tasks should map to GitHub issues that can be assigned

**3.3 TASK SUBTASKS**
For each task, break down into specific subtasks:
- Research and analysis needed
- Design decisions required
- Implementation work (if code is involved)
- Testing requirements
- Documentation updates
- Review and approval needed

**STEP 4: INDIVIDUAL TASK DESCRIPTIONS**
Create a detailed description for each task using this template:

```
## Task [Phase.Task]: [Descriptive Task Name]

### SCOPE OF WORK
[Clear description of what will be accomplished in this task]

### REPOSITORY/LOCATION
[Which repo(s) this affects, or if it's platform-level documentation]

### EXPECTED OUTPUTS
**Deliverables:**
- [Specific files, specs, or artifacts to be created/modified]
- [Documentation that will be updated]
- [Decisions that will be documented]

**Acceptance Criteria:**
- [Specific criteria for task completion]
- [What can be demonstrated or verified]

### PREREQUISITES
**Dependencies from previous tasks:**
- [What must be completed before this task can begin]
- [Specific documents, decisions, or implementations needed]

**Required decisions:**
- [Any architectural or technical decisions needed before starting]
- [Business priorities or requirements to clarify]

### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. [Specific question about requirements or approach]
2. [Any ambiguous integration points or dependencies]
3. [Technical decisions that need stakeholder input]

### IMPLEMENTATION APPROACH
[Brief outline of how this task will be approached]
- Research phase: [What to investigate]
- Design phase: [What to design or specify]
- Implementation phase: [What to build or document]
- Review phase: [What to validate]

### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] [Specific testable or demonstrable criteria]
- [ ] [All deliverables created and reviewed]
- [ ] [Documentation updated]
- [ ] [Integration verified (if applicable)]
- [ ] [Stakeholder approval obtained (if needed)]

### EFFORT ESTIMATE
- **Size**: [XS/S/M/L/XL based on effort-estimation.md framework]
- **Estimated Time**: [Days or weeks]
- **Complexity**: [Low/Medium/High]
- **Risk**: [🟢 Low / 🟡 Medium / 🔴 High]
```

**STEP 5: CROSS-INITIATIVE DEPENDENCIES**

Identify and document dependencies on other initiatives:
- Which initiatives must complete before this can start?
- Which initiatives does this initiative unblock?
- Are there any parallel initiatives that need coordination?
- What shared resources or decisions are required?

**STEP 6: OUTPUT STRUCTURE**

Store the plan in `initiatives/_planning/$ARGUMENTS-plan.md` with clear phase/task/subtask hierarchy.

**Note**: The plan will stay in `_planning/` until issues are created. When you run `/initiative-create-issues`, both the spec and plan will be moved to `initiatives/[initiative-name]/` subdirectory (marking it as active).

**Plan structure:**
```
# Initiative Implementation Plan: [Initiative Name]

## Overview
[Brief description of the initiative and its scope]

## Dependencies
### Blocking Dependencies
- [Initiatives that must complete first]

### Unblocks
- [Initiatives this will enable]

### Coordination Required
- [Initiatives that need parallel coordination]

## Phase 1: [Phase Name]
### Task 1.1: [Task Name]
[Task description using template above]

### Task 1.2: [Task Name]
[Task description using template above]

## Phase 2: [Phase Name]
### Task 2.1: [Task Name]
[Task description using template above]

## Risk Mitigation
[Key risks and mitigation strategies]

## Success Metrics
[How to measure successful completion]
```

**STEP 7: COMMIT IMPLEMENTATION PLAN**

After creating the plan document:

```bash
# Add the new plan file
git add initiatives/_planning/$ARGUMENTS-plan.md

# Commit with descriptive message
git commit -m "feat(initiative): add implementation plan for $ARGUMENTS

- Hierarchical breakdown into phases and tasks
- Detailed effort estimates and dependencies
- Risk mitigation strategies
- Success metrics and acceptance criteria"

# Push to the PR
git push
```

**STEP 8: UPDATE PLATFORM DOCUMENTATION**

After creating the plan, use the Task tool to launch the `doc-updater` agent:
- The agent will update `initiatives/effort-estimation.md` if needed
- The agent will update `initiatives/timeline.md` if critical path affected
- The agent will update `architecture/dependencies.md` if new dependencies identified
- The agent will update initiative status in `initiatives/README.md`

Then use the Task tool to launch the `architecture-validator` agent to validate:
- Documentation boundaries are respected
- Cross-references are complete
- All required sections are present
- No duplication exists

**STEP 9: UPDATE PULL REQUEST**

Update the PR with planning phase completion:

```bash
# Add comment to PR
gh pr comment --body "## ✅ Implementation Planning Phase Complete

Implementation plan has been created with detailed breakdown of phases, tasks, and effort estimates.

### What's Included
- Hierarchical task breakdown (phases → tasks → subtasks)
- Effort estimates and sizing
- Task dependencies and sequencing
- Risk mitigation strategies
- Success metrics and acceptance criteria
- Repository-specific implementation details

### Initiative Complete
- ✅ Design specification (business & product requirements)
- ✅ Technical architecture (integration & implementation approach)
- ✅ Implementation plan (phases, tasks, effort estimates)

### Ready for Review
This initiative is now ready for final review and approval:
- [ ] Product/business review
- [ ] Technical architecture review
- [ ] Effort estimation review
- [ ] Priority confirmation

### After Merge
Once this PR is merged to main, create GitHub issues with:
\`\`\`
/initiative-create-issues $ARGUMENTS
\`\`\`

This will:
- Move initiative to active status
- Create GitHub milestone
- Generate issues from the plan
- Set up issue tracking"
```

**STEP 10: NEXT STEPS GUIDANCE**

Provide clear guidance to the user:

```
✅ IMPLEMENTATION PLAN COMPLETE

Branch: initiative/$ARGUMENTS
PR: [PR URL]
Documents:
- initiatives/_planning/$ARGUMENTS.md (design + technical specs)
- initiatives/_planning/$ARGUMENTS-plan.md (implementation plan)

INITIATIVE STATUS:
- ✅ Design specification (business & product requirements)
- ✅ Technical architecture (integration & implementation approach)
- ✅ Implementation plan (phases, tasks, effort estimates)

READY FOR REVIEW AND MERGE:

1. Review the complete initiative
   - Design specification
   - Technical architecture
   - Implementation plan
   - Effort estimates

2. Get stakeholder approvals
   - Product/business stakeholders
   - Technical architects
   - Engineering leads

3. Merge the PR
   - All phases complete
   - Reviews approved
   - Merge to main branch

4. Create GitHub issues (after merge)
   Run: /initiative-create-issues $ARGUMENTS
   - Must be run from main branch (after PR merge)
   - Creates GitHub milestone
   - Generates issues from plan
   - Moves initiative to active subdirectory
   - Sets up issue tracking
```

**CRITICAL FINAL INSTRUCTION:**
Before completing your planning:
1. Review the entire breakdown for logical flow and dependencies
2. Ensure no work is missed or duplicated across tasks
3. Verify each task is appropriately sized with clear deliverables
4. Confirm cross-repo coordination is explicitly called out
5. Double-check that documentation updates are included
6. Ensure risks and decision points are identified
7. Verify alignment with platform architecture boundaries

Initiative name: $ARGUMENTS
