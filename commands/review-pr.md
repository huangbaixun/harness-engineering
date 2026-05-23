---
description: PR code review — thin wrapper over harness:requesting-code-review + harness:receiving-code-review
---

This command is a thin wrapper. Real review work lives in the two skills below.

## When invoking for the *outbound* side (you authored the PR; asking for review)

Invoke `harness:requesting-code-review`. It enforces the pre-review checklist:
1. All `acceptance_criteria` in `features.json` for the in-progress feature are satisfied
2. No commit touches an item in `features.json` `out_of_scope`
3. No reverse-direction architecture-layer dependency (e.g., `skills/` importing from `commands/`)

The skill drafts the PR body including a `## feature` section referencing the `features.json` id, then creates the PR.

## When invoking for the *inbound* side (you are processing review feedback)

Invoke `harness:receiving-code-review`. It enforces:
- Rigid-constraint feedback → reconcile with `features.json` (accept-and-sync OR explicit reject with rationale; never silent)
- Architectural-change feedback → produce or update an ADR before merge

## Why a wrapper and not direct skill invocation?

This command stays for compatibility with users who already type `/harness:review-pr` and to give a single entry point for "do a PR review" without forcing the user to choose between the two skills. The actual review logic is owned by the two skills; this command must not duplicate that logic.

## Out of scope (intentionally NOT here)

- General code-quality checks unrelated to a PR — those belong in `harness:verification-before-completion`
- Security-focused review — use the project's separate security-review path (not yet a skill in this plugin)
- Architecture audit — that's `harness:audit`
