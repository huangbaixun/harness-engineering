---
description: Check consistency between documentation and code, generate fix recommendations when drift is detected
---

Use a subagent to execute the following checks:

1. Scan the directory structure description in docs/architecture.md
   Compare with the actual directory structure to find inconsistencies

2. Check each rule in CLAUDE.md
   Verify in the codebase whether it still applies
   - Does the error pattern the rule addresses still exist?
   - Has the rule been superseded by another mechanism (Hook/Linter), making the text version redundant?

3. Check ADRs with "Accepted" status in docs/decisions/
   Verify whether the corresponding technology choices are still in use

For each detected drift, generate a specific fix recommendation.
If the user agrees, apply the fixes directly and commit.
