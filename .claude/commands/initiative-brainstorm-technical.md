**ROLE**: You are facilitating a technical brainstorming session with a software architect. Focus on **technical architecture**: system integration, data flows, repository changes, dependencies, and implementation constraints. Build upon the existing design specification created in the design phase.

---

**STEP 0: VERIFY BRANCH AND PREREQUISITES**

Verify we're on the correct initiative branch with the design spec:

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Should be on initiative branch
if [[ ! "$CURRENT_BRANCH" =~ ^initiative/ ]]; then
  echo "ERROR: Must be on an initiative branch"
  echo "Current branch: $CURRENT_BRANCH"
  echo ""
  echo "Did you run /initiative-brainstorm-design first?"
  echo "If so, switch to the initiative branch:"
  echo "  git checkout initiative/$ARGUMENTS"
  exit 1
fi

# Check if design spec exists
if [ ! -f "initiatives/_planning/$ARGUMENTS.md" ]; then
  echo "ERROR: Design specification not found"
  echo "Expected: initiatives/_planning/$ARGUMENTS.md"
  echo ""
  echo "Please run /initiative-brainstorm-design first"
  exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "WARNING: You have uncommitted changes"
  echo "Please commit changes before continuing"
  exit 1
fi
```

**STEP 1: REVIEW DESIGN SPECIFICATION**

Read the existing design specification to understand the business context and product requirements:

```bash
# Read the design spec
cat initiatives/_planning/$ARGUMENTS.md
```

Summarize the key points:
- Business goals and user needs
- Functional requirements
- Key workflows and data needs
- External dependencies

**STEP 2: DISCOVER TECHNICAL DOCUMENTATION**

Use the Task tool to launch the `docs-finder` agent to discover technical documentation:
- Repository documentation (which repos might be affected)
- Architecture patterns (how systems integrate)
- Data flow documentation (how data moves)
- Dependency mappings (what depends on what)
- Similar technical implementations

The agent will return relevant technical documentation to review.

**STEP 3: INTERACTIVE TECHNICAL SPECIFICATION**

After reviewing documentation, develop the technical architecture through guided questions. Ask **one question at a time** to explore:

**Architecture Questions:**
- Which repositories will be affected?
- How do systems need to integrate?
- What are the integration points (APIs, databases, events)?
- Will this introduce new services or modify existing ones?
- What's the data flow between systems?
- Are there architectural decisions to make?

**Repository Impact:**
- **mystage-event-sourcing**: Pipeline changes? New scrapers? Data processing?
- **mystage-admin-interface**: Admin tools needed?
- **mystage-app-backend**: Backend API changes?
- **mystage-databases**: Schema changes? New collections?
- **mystage-app**: Mobile app changes?
- **mystage-ff-***: FlutterFlow app updates?

**Data & Storage Questions:**
- What databases are involved? (Firestore, PostgreSQL)
- What collections/tables are affected?
- Are schema changes needed?
- What about data migrations?
- How is data consistency maintained?
- Are there data volume considerations?

**Integration Questions:**
- What APIs need to be created/modified?
- Are there webhook/event integrations?
- What about authentication/authorization?
- How do services discover each other?
- What's the error handling strategy?

**Technology & Implementation:**
- What technologies/libraries are needed?
- Are there new external services to integrate?
- What about Firebase services (Auth, Functions, etc.)?
- Are there cloud resources needed (Cloud Tasks, Pub/Sub, etc.)?
- What deployment considerations exist?

**Performance & Scale:**
- What are the performance requirements?
- Expected data volume and growth?
- Concurrent user considerations?
- Caching strategies needed?
- Background processing requirements?

**Security & Compliance:**
- Authentication requirements?
- Authorization model?
- Data privacy considerations?
- Security vulnerabilities to mitigate?
- Audit logging needed?

**Dependencies:**
- What other initiatives must complete first?
- What initiatives does this enable?
- Are there shared resources/systems?
- What external dependencies exist?

**Risk & Unknowns:**
- What technical risks exist?
- What's not well understood?
- What needs prototyping/proof-of-concept?
- What could cause timeline delays?

**Documentation to reference:**
- `architecture/system-overview.md` - How systems integrate
- `architecture/data-flow.md` - Data movement patterns
- `architecture/dependencies.md` - Cross-repo dependencies
- `repos/[repo-name].md` - Repository details
- Existing initiative plans for patterns

Let's explore this iteratively with one question at a time.

**STEP 4: UPDATE SPECIFICATION WITH TECHNICAL REQUIREMENTS**

Once technical architecture is defined, update the design specification with technical sections.

**4.1: Add technical sections to existing document**

Add the following sections to `initiatives/_planning/$ARGUMENTS.md` (after the design sections):

```markdown
---

## Technical Architecture

**Added**: [Date] - Technical Brainstorming Phase

### Affected Repositories

#### Primary Repositories
- **[repo-name]**: [What changes here]
  - Files/areas affected: [specific paths or modules]
  - Type of work: [new features, refactoring, integration]

#### Secondary Repositories
- **[repo-name]**: [Minor changes]

### Integration Points

#### APIs & Endpoints
- **[Service/API name]**
  - Endpoint: `[HTTP method] /path/to/endpoint`
  - Purpose: [What it does]
  - Authentication: [How secured]
  - Request/Response: [Brief description]

#### Database Integration
- **Database**: [Firestore/PostgreSQL]
- **Collections/Tables**: [Which ones]
- **Operations**: [Create/Read/Update/Delete/Query]
- **Schema Changes**: [If needed]

#### Event Integration
- **Events Published**: [Event names and when triggered]
- **Events Consumed**: [Events listened to]
- **Message Queue**: [Cloud Tasks, Pub/Sub, etc.]

#### External Services
- **[Service name]**: [API, webhook, etc.]
  - Purpose: [What it provides]
  - Integration method: [How we connect]

### Data Architecture

#### Data Models
```typescript
// Key data structures (pseudo-code)
interface EntityName {
  field1: type;
  field2: type;
  // ...
}
```

#### Database Schema
- **Collections/Tables**:
  - `collection_name`: [Purpose]
    - Fields: [field1 (type), field2 (type)]
    - Indexes: [What needs indexing]
    - Relationships: [How it relates to other data]

#### Data Flow
1. [Step 1 of data flow]
2. [Step 2 of data flow]
3. [Step 3 of data flow]

#### Data Migration
- **Migration needed?**: [Yes/No]
- **Migration strategy**: [How to handle existing data]
- **Rollback plan**: [How to undo if needed]

### Technical Dependencies

#### Initiative Dependencies
- **Blocks**: [What initiatives can't start until this completes]
- **Blocked by**: [What initiatives must complete first]
  - [Initiative name]: [Why blocking]
- **Coordination required**: [What initiatives need coordination]
  - [Initiative name]: [What to coordinate]

#### Technology Dependencies
- **New libraries**: [Library name (version)]
- **New services**: [GCP service or external service]
- **Infrastructure**: [Cloud resources needed]

#### Cross-Repository Dependencies
- **Repository A depends on Repository B**: [Why]

### Implementation Approach

#### Architectural Decisions
- **Decision 1**: [Choice made]
  - **Rationale**: [Why this choice]
  - **Alternatives considered**: [What else was considered]
  - **Trade-offs**: [Pros/cons]

#### Technology Choices
- **[Technology/Library]**: [Why chosen]
- **[Pattern/Approach]**: [Why this approach]

#### Phasing Strategy (Technical)
**Phase 1: Foundation**
- [Technical task 1]
- [Technical task 2]

**Phase 2: Integration**
- [Technical task 1]
- [Technical task 2]

**Phase 3: Polish**
- [Technical task 1]
- [Technical task 2]

### Performance Considerations

#### Performance Requirements
- **Response time**: [Target latency]
- **Throughput**: [Requests per second, etc.]
- **Data volume**: [Expected size]

#### Scaling Strategy
- [How system will scale]
- [What resources scale horizontally/vertically]

#### Optimization Opportunities
- [Caching strategies]
- [Query optimization]
- [Background processing]

### Security Architecture

#### Authentication
- [How users authenticate]
- [Token management]

#### Authorization
- [Permission model]
- [Access control]

#### Data Protection
- [Encryption at rest/in transit]
- [PII handling]
- [Data retention]

### Technical Risks

#### High Risk
- **Risk**: [Description]
  - **Impact**: [What could go wrong]
  - **Likelihood**: [High/Medium/Low]
  - **Mitigation**: [How to reduce risk]
  - **Contingency**: [Plan B if mitigation fails]

#### Medium Risk
[Same structure as above]

### Testing Strategy

#### Unit Testing
- [What needs unit tests]
- [Key test scenarios]

#### Integration Testing
- [What integrations need testing]
- [Test environments needed]

#### End-to-End Testing
- [Key user workflows to test]
- [Test data requirements]

### Deployment Strategy

#### Deployment Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

#### Feature Flags
- [Any features that need gradual rollout]

#### Rollback Plan
- [How to rollback if deployment fails]
- [What data needs preserving]

### Monitoring & Observability

#### Metrics to Track
- [Metric 1]: [Why important]
- [Metric 2]: [Why important]

#### Logging Requirements
- [What to log]
- [Log levels and retention]

#### Alerts
- [What conditions trigger alerts]
- [Who gets notified]

### Open Technical Questions

- [ ] [Technical question that needs research]
- [ ] [Decision that needs architect approval]
- [ ] [Question about external service]

---

**Document History:**
- [Original date] - Design specification created
- [Date] - Technical architecture added
```

**4.2: Stage and commit the updates**
```bash
# Add the updated file
git add initiatives/_planning/$ARGUMENTS.md

# Commit with descriptive message
git commit -m "feat(initiative): add technical architecture for $ARGUMENTS

- Affected repositories and integration points
- Data architecture and schema design
- Technical dependencies and risks
- Implementation approach and phasing
- Security, performance, and monitoring considerations"

# Push to the PR
git push
```

**STEP 5: UPDATE DOCUMENTATION**

Use the Task tool to launch the `doc-updater` agent to:
- Update effort estimates if technical complexity affects sizing
- Update dependency mappings
- Update affected repository documentation

Use the Task tool to launch the `architecture-validator` agent to:
- Validate technical architecture completeness
- Check integration patterns are documented
- Verify dependencies are captured

**STEP 6: UPDATE PULL REQUEST**

Update the PR with technical phase completion:

```bash
# Add comment to PR
gh pr comment --body "## ✅ Technical Architecture Phase Complete

Technical architecture has been added to the initiative specification.

### What's Included
- Repository impact analysis
- Integration points and APIs
- Data architecture and schema
- Technical dependencies
- Implementation approach
- Security and performance considerations
- Testing and deployment strategy

### Next Steps
**Implementation Planning**: Run \`/initiative-plan $ARGUMENTS\` to create detailed implementation plan

The plan will break down this initiative into phases, tasks, and subtasks with effort estimates.

### Review Needed
- [ ] Technical architecture review
- [ ] Security review
- [ ] Performance implications review
- [ ] Integration patterns review"
```

**STEP 7: NEXT STEPS GUIDANCE**

Provide clear guidance to the user:

```
✅ TECHNICAL ARCHITECTURE COMPLETE

Branch: initiative/$ARGUMENTS
PR: [PR URL]
Document: initiatives/_planning/$ARGUMENTS.md (updated with technical sections)

INITIATIVE STATUS:
- ✅ Design specification (business & product requirements)
- ✅ Technical architecture (integration & implementation approach)
- ⏳ Implementation planning (next step)

NEXT STEPS:

1. Review the technical architecture
   - Share with engineering team
   - Validate integration approach
   - Confirm technology choices
   - Review security implications

2. Implementation planning (when ready)
   Run: /initiative-plan $ARGUMENTS
   - Break down into phases and tasks
   - Detailed effort estimation
   - Task dependencies and sequencing
   - Updates the same PR

3. Review and merge
   - Complete initiative review (design + technical + plan)
   - Get stakeholder approval
   - Merge PR to main

4. Create issues (after merge)
   Run: /initiative-create-issues $ARGUMENTS
   - Generate GitHub milestone and issues
   - Move initiative to active status
```

---

**Initiative name**: $ARGUMENTS
