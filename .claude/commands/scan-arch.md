---
description: Run an architecture health scan to check for dependency violations, oversized modules, and missing tests
---

Execute an architecture health scan:

1. Check dependency direction violations (per the dependency rules defined in architecture.md)
2. Identify oversized files (source files exceeding 300 lines)
3. Find new files missing corresponding tests (added in the last 7 days)
4. Detect circular dependencies
5. Assess module coupling (which modules are referenced by more than 3 other modules)

Generate a consolidated architecture health report and update docs/quality.md (if it exists).
Provide specific fix recommendations for the most severe issues.
