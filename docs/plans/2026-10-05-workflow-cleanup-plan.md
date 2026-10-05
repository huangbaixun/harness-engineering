# Harness workflow cleanup — approved Native execution

User approved the preceding audit and P0 → P1 → P2 order. Scope: framework only;
no consuming-product changes, deployment, credentials, global configuration or Issue calls.

1. P0: remove default auto-commit, empty formatting and telemetry hooks; replace
   empty checks with a shared argv-based verifier and Claude protocol adapter.
   Regressions must preserve unrelated staged changes and reject empty checks.
2. P1: bounded shared session context, neutral explicit checkpoints, native
   compaction, scoped execution/review; narrow direct-path protection with valid
   stdin parsing, without claiming a shell/security boundary.
3. P2: outcome-based audit/evolution, retire universal line/token scores and fixed
   model selection, canonical portable manifest with explicit Codex hook override;
   retain compatibility manifests, upstream bytes, licenses and opt-in Issue sync.

Validation: baseline offline suite (14/14 files passed); meaningful regressions,
paired old/new skill evaluations and human-review artifact, full offline suite,
upstream provenance check, final independent review. Measurements unavailable
from the host remain unknown. Live hook trust/loading is a separate validation gap.
