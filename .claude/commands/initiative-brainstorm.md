**STEP 1: DISCOVER EXISTING DOCUMENTATION**

First, use the Task tool to launch the `docs-finder` agent to check for existing documentation:
- Search for similar or related initiatives
- Verify this doesn't duplicate existing work
- Identify related documentation that should be reviewed
- Ensure proper documentation boundaries

The agent will return a list of relevant documentation to review before proceeding.

**STEP 2: INTERACTIVE SPECIFICATION DEVELOPMENT**

After reviewing the docs-finder results, ask me one question at a time so we can develop a thorough, step-by-step specification for this platform initiative. Each question should build on my previous answers, and our end goal is to have a detailed initiative specification that aligns with our platform architecture and existing initiatives.

Key documentation to consider:
- `README.md` - Platform overview and current status
- `architecture/README.md` - Documentation boundaries
- `architecture/system-overview.md` - How systems integrate
- `architecture/data-flow.md` - Data movement between systems
- `architecture/dependencies.md` - Cross-repo dependencies
- `initiatives/README.md` - Existing initiatives and priorities
- `initiatives/effort-estimation.md` - Estimation framework
- `repos/` - Individual repository documentation

Focus areas to explore:
- Which repositories will this initiative affect?
- What integration points between systems will change?
- How does this fit into the existing architecture?
- What are the dependencies on other initiatives?
- What decisions need to be made (e.g., technology choices)?
- What's the estimated effort and complexity?
- What are the success criteria?
- What are the risks and mitigation strategies?
- How does this align with business priorities?
- What documentation will need to be updated?

Let's do this iteratively and dig into every relevant detail. Remember, only one question at a time.

**STEP 3: SAVE AND UPDATE DOCUMENTATION**

Once we are done with the specification:
1. Save the initiative spec as `initiatives/_planning/$INITIATIVE_NAME.md` following the standard template
2. Use the Task tool to launch the `doc-updater` agent to update indexes and cross-references
3. Use the Task tool to launch the `architecture-validator` agent to validate the documentation

The agents will ensure all related documentation is updated and the spec meets quality standards.

---

Here's the initiative idea:

$ARGUMENTS
