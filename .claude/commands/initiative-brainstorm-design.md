**ROLE**: You are facilitating a design brainstorming session with a designer or product manager. Focus on **non-technical** aspects: business goals, user needs, product requirements, and desired outcomes. Avoid technical architecture discussions - those happen in the technical brainstorming phase.

---

**STEP 0: VERIFY GIT STATUS**

Before starting, verify we're ready to create a new initiative branch:

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Should be on main to start new initiative
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "WARNING: Not on main branch. Current branch: $CURRENT_BRANCH"
  echo "Do you want to:"
  echo "  1. Switch to main and start fresh"
  echo "  2. Continue on current branch"
  echo "  3. Abort"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "WARNING: You have uncommitted changes"
  echo "Please commit or stash changes before starting new initiative"
  exit 1
fi
```

**STEP 1: DISCOVER EXISTING DOCUMENTATION**

Use the Task tool to launch the `docs-finder` agent to check for existing documentation:
- Search for similar or related initiatives
- Verify this doesn't duplicate existing work
- Identify related documentation that should be reviewed
- Check if similar functionality exists in any repository

The agent will return a list of relevant documentation to review before proceeding.

**STEP 2: INTERACTIVE DESIGN SPECIFICATION**

After reviewing the docs-finder results, develop a non-technical design specification through guided questions. Ask **one question at a time** to explore:

**Business & Product Questions:**
- What business problem does this solve?
- Who are the primary users/stakeholders?
- What's the expected business impact?
- How does this align with product strategy?
- What are the success metrics?
- What's the priority relative to other initiatives?

**User Experience Questions:**
- What user pain points does this address?
- What user workflows will be affected?
- What's the ideal user experience?
- Are there accessibility considerations?
- What platforms/devices are involved? (web, mobile, admin tools)

**Functional Requirements:**
- What specific features or capabilities are needed?
- What data will users interact with?
- What actions can users take?
- Are there different user roles with different needs?
- What notifications or communications are needed?

**Scope & Constraints:**
- What's included in scope vs. out of scope?
- Are there time constraints or deadlines?
- What's the minimum viable version?
- What can be done in phases?
- Are there external dependencies (3rd party services, APIs)?

**Risk & Considerations:**
- What are the biggest risks or unknowns?
- Are there compliance or legal considerations?
- What happens if this initiative doesn't happen?
- Are there alternative approaches to consider?

**Documentation to reference:**
- `README.md` - Platform overview and current status
- `initiatives/README.md` - Existing initiatives and priorities
- `initiatives/effort-estimation.md` - Priority framework
- `repos/` - What repositories/systems exist

**IMPORTANT**: Keep questions **non-technical**. Focus on WHAT we're building and WHY, not HOW we'll build it. Technical architecture comes in the next phase.

Let's explore this iteratively with one question at a time.

**STEP 3: CREATE BRANCH AND SAVE SPECIFICATION**

Once the design specification is complete:

**3.1: Determine initiative name**
- Convert the initiative idea into a short, kebab-case name
- Example: "Entity Deduplication System" → "entity-deduplication"
- Store as: `$INITIATIVE_NAME`

**3.2: Create feature branch**
```bash
# Create and switch to initiative branch
git checkout -b initiative/$INITIATIVE_NAME

# Verify branch creation
git branch --show-current
```

**3.3: Create design specification document**

Save the specification as `initiatives/_planning/$INITIATIVE_NAME.md` following this template:

```markdown
# [Initiative Name]

**Status**: 🟡 Planning - Design Phase
**Created**: [Date]
**Last Updated**: [Date]
**Priority**: [High/Medium/Low - TBD]
**Phase**: Design Specification

## Business Context

### Problem Statement
[What business problem are we solving?]

### Business Goals
- [Goal 1]
- [Goal 2]
- [Goal 3]

### Success Metrics
- [Metric 1: how we'll measure success]
- [Metric 2]
- [Metric 3]

### Target Users
- **Primary Users**: [Who]
- **Secondary Users**: [Who]
- **Stakeholders**: [Who]

### Business Impact
[Expected impact on business/users/platform]

## Product Requirements

### Functional Requirements

#### [Feature Area 1]
**What it does:**
[Non-technical description of functionality]

**User value:**
[How this helps users]

**Must have:**
- [Required capability 1]
- [Required capability 2]

**Nice to have:**
- [Optional capability 1]
- [Optional capability 2]

#### [Feature Area 2]
[Same structure as above]

### User Experience Requirements

**Key User Workflows:**
1. [Workflow 1]
   - User starts from: [context]
   - User needs to: [action]
   - Expected outcome: [result]

2. [Workflow 2]
   [Same structure]

**Platform Touchpoints:**
- [ ] Web application
- [ ] Mobile app (iOS/Android)
- [ ] Admin interface
- [ ] Email/notifications
- [ ] API access

**Accessibility & Usability:**
- [Considerations for accessibility]
- [Usability requirements]
- [Performance expectations from user perspective]

### Data Requirements

**What data do users need?**
- [Data type 1] - [Why needed]
- [Data type 2] - [Why needed]

**What data do users create/modify?**
- [Data type 1] - [How used]
- [Data type 2] - [How used]

### External Dependencies

**Third-Party Services:**
- [Service name] - [What it provides]

**External APIs:**
- [API name] - [What it provides]

**Other Dependencies:**
- [Dependency] - [Why needed]

## Scope & Phasing

### In Scope (MVP)
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Out of Scope (Future)
- [Feature that will come later]
- [Feature that's explicitly excluded]

### Phasing Strategy
**Phase 1**: [What gets built first]
**Phase 2**: [What comes next]
**Phase 3**: [Future enhancements]

## Risks & Considerations

### Business Risks
- **Risk**: [Description]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [How to address]

### User Experience Risks
- **Risk**: [Description]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [How to address]

### Compliance & Legal
- [Any regulatory considerations]
- [Privacy considerations]
- [Data retention requirements]

## Priority & Timeline

### Priority Justification
[Why this initiative is High/Medium/Low priority]

### Time Sensitivity
- **Deadline**: [If any]
- **Business driver**: [What's driving timeline]

### Dependencies on Other Initiatives
- **Blocks**: [What this enables]
- **Blocked by**: [What must complete first]
- **Related**: [What should be coordinated]

## Next Steps

- [ ] Technical brainstorming session (add architecture requirements)
- [ ] Implementation planning
- [ ] Effort estimation
- [ ] Approval & prioritization

## Open Questions

### Design Questions
- [ ] [Question that needs product decision]

### Business Questions
- [ ] [Question that needs business stakeholder input]

---

**Document History:**
- [Date] - Design specification created
```

**3.4: Stage and commit the specification**
```bash
# Add the new file
git add initiatives/_planning/$INITIATIVE_NAME.md

# Commit with descriptive message
git commit -m "feat(initiative): add $INITIATIVE_NAME design specification

- Business context and problem statement
- Product requirements and user workflows
- Scope and phasing strategy
- Risks and considerations
- Priority justification"
```

**STEP 4: UPDATE DOCUMENTATION**

Use the Task tool to launch the `doc-updater` agent to:
- Add initiative to `initiatives/README.md` (under appropriate category)
- Update any relevant indexes
- Establish cross-references

Use the Task tool to launch the `architecture-validator` agent to:
- Validate the design specification is complete
- Check that it doesn't duplicate existing initiatives
- Verify proper documentation boundaries

**STEP 5: CREATE PULL REQUEST**

Push the branch and create a PR for review:

```bash
# Push the new branch
git push -u origin initiative/$INITIATIVE_NAME

# Create PR with gh CLI
gh pr create \
  --title "Initiative: $INITIATIVE_NAME" \
  --body "$(cat <<'EOF'
## Initiative Design Specification

This PR contains the design specification for the **$INITIATIVE_NAME** initiative.

### What's Included
- ✅ Business context and problem statement
- ✅ Product requirements and functional specifications
- ✅ User experience requirements and workflows
- ✅ Scope definition and phasing strategy
- ✅ Risk assessment and mitigation

### Next Steps
1. **Review design specification** - Product/business stakeholders review
2. **Technical brainstorming** - Architect adds technical requirements (on this branch)
3. **Implementation planning** - Create detailed implementation plan (on this branch)
4. **Merge** - After all phases complete and approved
5. **Issue creation** - Generate GitHub issues (after merge to main)

### Documentation Updates
- [x] Added to initiatives/_planning/
- [x] Updated initiatives/README.md index
- [x] Ran docs-finder to check for duplicates
- [x] Ran architecture-validator

### Related
- Initiative spec: \`initiatives/_planning/$INITIATIVE_NAME.md\`
- Design phase only - technical phase pending

---
**Status**: 🟡 Design phase complete, awaiting technical brainstorming
EOF
)"
```

**STEP 6: NEXT STEPS GUIDANCE**

Provide clear guidance to the user:

```
✅ DESIGN SPECIFICATION COMPLETE

Branch: initiative/$INITIATIVE_NAME
PR: [URL from gh pr create]
Document: initiatives/_planning/$INITIATIVE_NAME.md

NEXT STEPS:

1. Review the design specification
   - Share PR with stakeholders
   - Gather feedback on product requirements
   - Confirm business priorities

2. Technical brainstorming (when ready)
   Run: /initiative-brainstorm-technical $INITIATIVE_NAME
   - Software architect adds technical requirements
   - Identifies affected repositories
   - Documents integration points
   - Updates the same PR

3. Implementation planning (after technical)
   Run: /initiative-plan $INITIATIVE_NAME
   - Break down into phases and tasks
   - Effort estimation
   - Updates the same PR

4. Review and merge
   - Team reviews complete initiative
   - Merge PR to main

5. Create issues (after merge)
   Run: /initiative-create-issues $INITIATIVE_NAME
   - Generate GitHub issues
   - Move to active subdirectory
```

---

**Initiative idea**: $ARGUMENTS
