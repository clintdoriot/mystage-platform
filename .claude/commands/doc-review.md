# Documentation Review & Quality Assurance

Perform a thorough documentation review of the specified files or directories, checking for completeness, accuracy, consistency, and adherence to platform documentation standards.

**This command uses the `architecture-validator` agent to perform the review.**

## Command Usage
```
/doc-review [path/to/file-or-directory]
/doc-review --base <branch-name>
/doc-review <base-branch>..<compare-branch>
```

**Modes:**
- `[path]` - Review specific documentation files/directories
- `--base <branch>` - Review documentation changes vs specified base branch (default: main)
- `<base>..<compare>` - Review documentation changes between two branches
- No arguments - Review all changed documentation files

## Review Process

**STEP 1: LAUNCH ARCHITECTURE VALIDATOR AGENT**

Use the Task tool to launch the `architecture-validator` agent with the specified path or git comparison. The agent will perform all the checks below and return a comprehensive validation report.

**STEP 2: REVIEW AGENT REPORT**

The agent will check the following areas:

### 1. Git Integration

When using branch comparison modes:
1. **Identify Changed Docs**: `git diff --name-only <base>..<compare> -- '*.md'`
2. **Analyze Doc Diffs**: Focus on modified sections
3. **Context Awareness**: Understand what changed vs what stayed
4. **Consistency Check**: Ensure related docs are updated together

### 2. Documentation Quality

- [ ] **Clarity & Readability**
  - [ ] Clear, concise language
  - [ ] Proper heading hierarchy (H1 → H2 → H3)
  - [ ] Logical information flow
  - [ ] Appropriate use of lists, tables, code blocks
  - [ ] No jargon without explanation
  - [ ] Spelling and grammar

- [ ] **Accuracy**
  - [ ] Technical details are correct
  - [ ] Repository references are accurate
  - [ ] Integration descriptions match reality
  - [ ] Effort estimates align with framework
  - [ ] Dependencies are correctly stated
  - [ ] Status indicators are current

- [ ] **Completeness**
  - [ ] All required sections present
  - [ ] No TODO or placeholder sections
  - [ ] Examples provided where helpful
  - [ ] Links to related docs included
  - [ ] Success criteria defined
  - [ ] Risks and mitigations documented

- [ ] **Consistency**
  - [ ] Follows standard template for document type
  - [ ] Terminology consistent across docs
  - [ ] Formatting matches platform style
  - [ ] Status indicators used correctly (🔴🟡🟢✅⏳)
  - [ ] Similar initiatives documented similarly

### 3. Platform-Specific Checks

- [ ] **Documentation Boundaries** (see `architecture/README.md`)
  - [ ] Platform docs stay at integration level
  - [ ] Implementation details deferred to repo docs
  - [ ] Clear distinction between platform and repo concerns
  - [ ] No over-documentation of internal details

- [ ] **Cross-References**
  - [ ] Links to related initiatives work
  - [ ] Repository references are accurate
  - [ ] Architecture docs referenced appropriately
  - [ ] Effort estimates link correctly
  - [ ] Timeline references are current

- [ ] **Initiative Documentation**
  - [ ] Affected repositories clearly listed
  - [ ] Dependencies identified
  - [ ] Effort estimate provided
  - [ ] Priority assigned
  - [ ] Status indicator present
  - [ ] Success criteria defined
  - [ ] Risks documented

- [ ] **Repository Documentation**
  - [ ] Technology stack documented
  - [ ] Integration points identified
  - [ ] Database usage described
  - [ ] Deployment approach mentioned
  - [ ] Links to actual repo docs

- [ ] **Architecture Documentation**
  - [ ] Focuses on HOW systems integrate
  - [ ] Data flow clearly described
  - [ ] Dependencies mapped
  - [ ] Integration patterns documented
  - [ ] No implementation details

### 4. Related Documentation Updates

- [ ] **When initiative docs change:**
  - [ ] `initiatives/README.md` updated with new initiative
  - [ ] `initiatives/effort-estimation.md` includes sizing
  - [ ] `initiatives/timeline.md` reflects timeline impact
  - [ ] `architecture/dependencies.md` shows dependencies

- [ ] **When architecture changes:**
  - [ ] Related repo docs updated
  - [ ] Initiative docs reflect new integration patterns
  - [ ] Data flow diagrams updated
  - [ ] System overview reflects changes

- [ ] **When repos added/changed:**
  - [ ] Main `README.md` repository index updated
  - [ ] New repo doc created in `repos/`
  - [ ] Architecture docs show integration
  - [ ] Related initiatives updated

## Agent Output Format

The `architecture-validator` agent will return a structured report:

```
DOCUMENTATION REVIEW: [file-path] (vs [base-branch])

## Analysis Summary
[Overall assessment of documentation quality and completeness]

## Changed Files Summary
- Added: [list of new documentation files]
- Modified: [list of changed documentation files]
- Deleted: [list of removed documentation files]

## Critical Issues (🔴)
- [ ] [Issue description]
  - Impact: [High/Medium/Low]
  - Location: [file:line or section]
  - Recommendation: [How to fix]
  - Example:
    ```markdown
    # Before
    [problematic content]

    # After
    [corrected content]
    ```

## Warnings (🟠)
- [ ] [Issue description]
  - Impact: [High/Medium/Low]
  - Location: [file:section]
  - Suggestion: [Recommended improvement]

## Suggestions (🔵)
- [ ] [Optional improvement]
  - Benefit: [Why this would be valuable]
  - Effort: [Low/Medium/High]

## Accuracy Issues
- [ ] [Inaccurate information]
  - Current: [What it says now]
  - Should be: [Correct information]
  - Source: [Where to verify]

## Completeness Gaps
- [ ] [Missing information]
  - Section: [Where it should go]
  - Content needed: [What's missing]
  - Importance: [Why it matters]

## Consistency Issues
- [ ] [Inconsistency found]
  - Location: [Where found]
  - Conflicts with: [Other doc or standard]
  - Resolution: [How to make consistent]

## Cross-Reference Issues
- [ ] [Broken or missing link]
  - Link: [The problematic reference]
  - Should link to: [Correct target]
  - Fix: [How to correct]

## Related Documentation Updates Needed
- [ ] [Other docs that should be updated]
  - File: [Path to related doc]
  - Change needed: [What to update]
  - Reason: [Why it needs updating]

## Platform Boundary Violations
- [ ] [Implementation detail in platform docs]
  - Location: [Where found]
  - Issue: [What doesn't belong]
  - Should go: [Where it belongs instead]

## Documentation Standards
- [ ] [Standard not followed]
  - Standard: [Which guideline]
  - Location: [Where violation occurs]
  - Fix: [How to comply]
```

## Usage Examples

### Review a specific documentation file
```
/doc-review initiatives/_planning/entity-deduplication.md
```

### Review all changed documentation vs main
```
/doc-review
```

### Review changes vs specific base branch
```
/doc-review --base dev
```

### Review changes between branches
```
/doc-review main..feature/nft-planning
```

### Review entire directory
```
/doc-review architecture/
```

## Documentation Standards Checklist

### Initiative Documents
- [ ] Status indicator present (🔴🟡🟢✅⏳)
- [ ] Description section
- [ ] Affected Repositories section
- [ ] Dependencies documented
- [ ] Estimated Effort provided
- [ ] Priority assigned
- [ ] Success Criteria defined

### Repository Documents
- [ ] Overview/Purpose
- [ ] Technology Stack
- [ ] Integration points (what it connects to)
- [ ] Database usage
- [ ] Deployment approach
- [ ] Link to actual repository docs

### Architecture Documents
- [ ] Focus on integration, not implementation
- [ ] Clear diagrams or flows where helpful
- [ ] Cross-references to repo docs
- [ ] Dependencies clearly stated
- [ ] System boundaries respected

### Effort Estimation Documents
- [ ] Size scale defined (XS/S/M/L/XL/XXL)
- [ ] Complexity factors listed
- [ ] Risk assessment included
- [ ] Dependencies noted
- [ ] Priority assigned

### Timeline Documents
- [ ] Milestones defined
- [ ] Dependencies shown
- [ ] Resource requirements stated
- [ ] Risk mitigation included
- [ ] Parallel work identified

## Integration

This command can be used:
- Before committing documentation changes
- During pull request reviews
- When planning new initiatives
- To audit documentation quality
- To ensure consistency across platform docs

## Exit Codes
- `0`: No issues found or only suggestions
- `1`: Warnings found (should be addressed)
- `2`: Critical issues found (must be fixed)
- `3`: Error during analysis
