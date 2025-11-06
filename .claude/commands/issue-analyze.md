Analyze a GitHub issue in detail to understand requirements, dependencies, and clarify any ambiguities before starting work.

## Command Usage
```
/issue-analyze [issue-number]
```

If no issue number is provided, will analyze the most recently identified issue from `/issue-identify`.

## Analysis Process

### 1. Fetch Issue Details
```bash
gh issue view [issue-number] --json title,body,labels,assignees,milestone,state,url,comments
```

Extract key information:
- **Title and Description**: What needs to be done
- **Initiative**: Which initiative this belongs to
- **Phase/Task ID**: Where in the implementation plan
- **Repository**: Which repos are affected
- **Dependencies**: What must be complete first
- **Blocks**: What this unblocks
- **Labels**: Priority, type, status
- **Comments**: Additional context or clarifications

### 2. Review Related Documentation

Before analyzing, read relevant platform documentation:

**For initiative-related issues:**
- `initiatives/_planning/[initiative-name].md` - Initiative specification
- `initiatives/_planning/[initiative-name]-plan.md` - Implementation plan (if exists)
- `initiatives/effort-estimation.md` - Sizing framework
- `architecture/dependencies.md` - Cross-initiative dependencies

**For repository documentation issues:**
- `repos/[repo-name].md` - Current repo documentation
- `architecture/system-overview.md` - Integration patterns
- `architecture/data-flow.md` - Data movement

**For architecture issues:**
- `architecture/README.md` - Documentation boundaries
- `architecture/system-overview.md` - Current architecture
- Related repo docs for affected systems

### 3. Dependency Analysis

**Check dependencies:**
1. Read `Depends on: #X` from issue body
2. For each dependency, check if it's closed: `gh issue view #X --json state`
3. If any are open, list them and suggest working on dependencies first
4. Check if this issue blocks others (priority indicator)

**Identify implicit dependencies:**
- Does this require architecture decisions?
- Are there related initiatives that should coordinate?
- Does documentation exist for prerequisites?
- Are there external factors (decisions, approvals)?

### 4. Scope Clarification

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

### 5. Requirements Clarification

**Ask clarifying questions if needed:**

**For planning/spec issues:**
- What business problem does this solve?
- What are the success criteria?
- Who are the stakeholders to consult?
- What's the priority relative to other work?
- What decisions must be made?

**For documentation issues:**
- What's the target audience?
- What level of detail is appropriate?
- What related docs need updating?
- Are there examples or diagrams needed?

**For architecture issues:**
- Which systems/repos are affected?
- What integration patterns are involved?
- What are the constraints or requirements?
- Are there alternative approaches to consider?

### 6. Effort Validation

Compare issue scope to effort framework:
- Does the described work match the size estimate?
- Are there hidden complexities?
- Should this be broken into smaller issues?
- Is the timeline realistic?

### 7. Risk Assessment

Identify risks and challenges:
- **Dependency risks**: Other work blocking this
- **Decision risks**: Unclear requirements or priorities
- **Coordination risks**: Multiple stakeholders or repos
- **Technical risks**: Architectural uncertainties
- **Timeline risks**: External dependencies or approvals

### 8. Output Format

```
ISSUE ANALYSIS: #[number] - [title]

## Summary
[Brief description of what this issue accomplishes]

## Initiative Context
- Initiative: [initiative name]
- Phase/Task: [Phase X.Y]
- Priority: [High/Medium/Low]
- Repository: [affected repos]

## Dependencies
### Blocking This Issue:
- [ ] #X - [title] (Status: [open/closed])
- [ ] [Decision/approval needed]

### This Issue Blocks:
- #Y - [title]
- #Z - [title]

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

From issue:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

Additional verification:
- [ ] Related docs updated
- [ ] Cross-references working
- [ ] Documentation boundaries respected

## Effort Assessment

**Estimated Size**: [XS/S/M/L/XL]
**Estimated Time**: [hours/days]
**Complexity**: [Low/Medium/High]
**Risk**: [🟢 Low / 🟡 Medium / 🔴 High]

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
- [✓/✗] All dependencies closed
- [✓/✗] Requirements clear
- [✓/✗] Scope well-defined
- [✓/✗] No major blockers

**Recommendation:**
[Start immediately / Address clarifications first / Wait for dependencies]

## Next Steps

[Clear actionable next steps to begin work on this issue]
```

### 9. Interactive Clarification

If requirements are unclear:
1. Identify specific ambiguities
2. Ask targeted questions (one at a time if needed)
3. Document answers for reference
4. Update issue with clarifications if helpful

### 10. Follow-Up Actions

After analysis, offer to:
- Start working on the issue if ready
- Update issue with clarifications
- Create dependency issues if needed
- Suggest alternative sequencing if better approach exists
