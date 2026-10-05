# ADR 0014: Evidence-based, platform-neutral workflow cleanup

Status: accepted. Date: 2026-10-05. User approved audit repairs in P0/P1/P2 order.

Hooks must perform a configured operation, not imply a guarantee from registration.
No default auto-commit, empty formatter or homemade telemetry. Shared verification
uses argv arrays without a shell; empty configuration is not success. Stop requests
verification once and avoids a retry loop. Explicit verification remains authoritative.

Claude/Codex share bounded state and neutral checkpoint writes. Legacy progress is
read-only. Native compaction does not require an artificial 50% termination rule.
Execution follows the selected workflow without adding duplicate agent pipelines.

Audit findings require observed evidence and status pass/fail/unknown. Universal
60/300-line and 20k-token budgets, model aliases and inventory-based scores are
retired as policy. Repository-specific measured limits may still be justified.
Direct-path protection is an additional narrow guard, not a permissions boundary.

Portable plugin.json is canonical; explicit OpenAI hooks prevent loading Claude
hooks. Legacy platform manifests remain compatibility entries. No upstream skill
body or companion edits beyond the existing permitted namespace/pointer changes.

Sources: https://developers.openai.com/plugins/build/plugins ;
https://code.claude.com/docs/en/hooks ;
https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra .
