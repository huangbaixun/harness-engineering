---
description: Perform a comprehensive code review of the PR on the current branch
---

Use a subagent to execute the following steps, then summarize:
1. Run `git diff main...HEAD` to get all changes
2. Check code quality (type errors, unused variables, logic flaws)
3. Check security issues (injection, authentication flaws, secret exposure)
4. Verify test coverage (new code must have corresponding tests)
5. Check API documentation updates (all public APIs must have doc comments)
6. Verify architecture constraints (check if dependency direction complies with architecture.md rules)

Output format:
- 🔴 Must fix (blocks merge)
- 🟡 Suggested improvement (optional)
- 🟢 Things done well
