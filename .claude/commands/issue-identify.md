Identify the next GitHub issue to work on for the MyStage platform documentation and planning. Can filter by initiative, milestone, or work with all open issues.

## Command Usage
```
/issue-identify [initiative-name|milestone-name|label]
```
Where the argument can be:
- An initiative name (e.g., `entity-deduplication`, `database-schema`) - will search by `initiative:[name]` label
- A milestone name (e.g., `Q1 Foundation`, `Phase 1: Foundation`) - will search by milestone
- Any other label (e.g., `documentation`, `planning`, `architecture`, `high-priority`)
- Empty to show all open issues

## Steps

**STEP 1: DETERMINE FILTER TYPE**
- If argument contains spaces or version numbers, treat as milestone name
- If argument starts with known prefixes or common labels, use as direct label
- If argument looks like an initiative name (hyphenated), construct label: `initiative:[argument]`
- If no argument provided, show all open issues

**STEP 2: FETCH ISSUES**
List open GitHub issues with the appropriate filter:
```bash
# For initiative label:
gh issue list --state open --label "initiative:[initiative-name]" --limit 20

# For milestone:
gh issue list --state open --milestone "[milestone-name]" --limit 20

# For all issues:
gh issue list --state open --limit 20
```

**STEP 3: ANALYZE ISSUE DEPENDENCIES**
For each issue, check the issue body for:
- **Dependencies**: "Depends on: #X" - skip if dependency is still open
- **Blocking**: "Blocks: #Y" - prioritize issues that unblock others
- **Phase/Task ID**: Look for "Phase.Task" to understand implementation order
- **Initiative**: Which initiative this belongs to
- **Repository**: Which repo(s) this affects
- **Labels**: Check for `blocked`, `in-progress`, `ready`, `high-priority`, `documentation`, `planning`

**STEP 4: PRIORITIZE ISSUES**
Rank issues considering:
1. **Unblocked**: No open dependencies
2. **Implementation Order**: Earlier phase/task numbers first
3. **Unassigned**: Available to work on immediately
4. **Priority**: High-priority initiatives first
5. **Foundation First**: Planning and architecture before implementation-focused docs
6. **Smaller Scope**: Prefer focused, single-purpose issues
7. **Unblocks Others**: Issues that have other issues depending on them

**STEP 5: DISPLAY RESULTS**
For each relevant issue, show:
```
Issue #123: [Entity Deduplication] Task 1.1: Create Initiative Specification
Labels: [initiative:entity-deduplication] [documentation] [planning] [high-priority]
Assignee: unassigned
Dependencies: None
Blocks: Issues #124, #125
Repository: mystage-event-sourcing, mystage-admin-interface
Preview: Create detailed initiative specification for entity deduplication...
Phase/Task: Phase 1.1
```

**STEP 6: MAKE RECOMMENDATION**
Present the best next task:
```
RECOMMENDED NEXT ISSUE:
Issue #123: [Entity Deduplication] Task 1.1: Create Initiative Specification
Reason: Foundation documentation with no dependencies, unblocks 2 other issues

IMPLEMENTATION ORDER:
Next up after #123:
- Issue #124: Task 1.2: Architecture Design (depends on #123)
- Issue #125: Task 1.3: Effort Estimation (depends on #123)

OTHER OPTIONS:
Issue #126: [Database Schema] Task 2.1: Schema Documentation - Available but different initiative
```

**STEP 7: PLATFORM CONTEXT**
Consider platform documentation priorities when analyzing:
- **Planning docs first**: Initiatives and specs enable implementation work
- **Architecture clarity**: System integration docs help all repos
- **Dependencies early**: Identify blockers before work starts
- **Initiative sequencing**: Complete related docs together
- **Cross-cutting first**: Platform-wide decisions before repo-specific work

**STEP 8: NO MATCHES HANDLING**
If no issues match the filter:
- Check if initiative exists: `gh issue list --search "initiative:[initiative-name] in:labels"`
- Suggest available initiatives: `gh label list | grep "initiative:"`
- Offer to show all open issues instead

**STEP 9: FOLLOW-UP**
Ask if the user wants to:
- Analyze the recommended issue in detail
- Start working on the issue immediately
- See related documentation that should be reviewed first
