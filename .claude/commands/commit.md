Commit the documentation that is currently staged, with a commit message that:

1. uses conventional commit format appropriate to the changed files
2. is concise - don't include unnecessary details on small change sets
3. focuses on what changed functionally, not how it was implemented
4. never mentions tests, TDD, or process details unless those are the primary focus
5. never includes attribution to claude
6. never asks for additional confirmation (running `/commit` IS the permission)

---

## Platform-Specific Commit Patterns

Analyze staged files to determine the appropriate conventional commit type:

### Initiative Documents

**Design specifications** (`initiatives/_planning/[name].md` without `-plan` suffix):
```
feat(initiative): add [initiative-name] design specification
```

**Technical architecture** (`initiatives/_planning/[name].md` with "## Technical Architecture" section):
```
feat(initiative): add technical architecture for [initiative-name]
```

**Implementation plans** (`initiatives/_planning/[name]-plan.md`):
```
feat(initiative): add implementation plan for [initiative-name]
```

**Active initiatives** (`initiatives/[name]/` subdirectories):
```
feat(initiative): update [initiative-name]
```

### Other Documentation

**Repository docs** (`repos/*.md`):
```
docs(repo): update [repo-name] documentation
```

**Architecture docs** (`architecture/*.md`):
```
docs(arch): update [document-name]
```

**Initiative indexes/estimates** (`initiatives/README.md`, `initiatives/effort-estimation.md`, `initiatives/timeline.md`):
```
docs(initiative): update [index|effort estimation|timeline]
```

**Claude config** (`.claude/` files):
```
chore(claude): update [what changed]
```

**General documentation**:
```
docs: update [area]
```

---

## Commit Message Guidelines

- **Be concise**: Short, clear descriptions
- **Focus on WHAT**: Describe the change, not how it was made
- **Be evergreen**: No temporal references like "recently added" or "just updated"
- **Extract initiative names**: Use actual initiative name from file paths when possible
- **Keep it simple**: For small changesets, a one-line message is fine

## Examples

**Good:**
```
feat(initiative): add entity-deduplication design specification
docs(repo): update mystage-admin-api migration guidance
chore(claude): add branch-based workflow commands
docs: update repository index
```

**Avoid:**
```
feat(initiative): add entity-deduplication design specification using TDD and validation
docs: recently updated the repository documentation with new information
feat: improve documentation (add entity dedup stuff) Co-Authored-By: Claude
```

---

**Arguments**: $ARGUMENTS
