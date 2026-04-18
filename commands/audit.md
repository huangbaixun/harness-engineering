---
description: Perform a health audit on the current project's Harness system, generating a score report and optimization recommendations
---

Execute a Harness health audit:

1. Scan the current project's six-layer Harness status (Memory layer, Rules layer, Skills layer, Agent layer, Hooks layer, Tools layer)
2. Score across seven dimensions: Bootstrap / Task Entry / Validation / Lint Gates / Repo Map / Structured Docs / Decision Records
3. Diagnose common failure modes (CLAUDE.md bloat, insufficient Hook coverage, context pollution, architecture drift, stale documentation)
4. Generate a structured optimization plan (by priority: Immediate action / Complete this month / Continuous improvement)
5. If the user agrees, execute the optimizations directly and submit a PR
