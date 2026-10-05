# harness-delta: verification-before-completion

## Upstream
superpowers v6.4.2 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Locate the current `building` feature. Verify each `acceptance_criterion` has been demonstrably satisfied (test passing, behavior observable).

### features.json writes
This skill does **not** transition `status` to `done`. The transition `building → done` is owned by the `verification-before-completion → finishing-a-development-branch → archive` chain. This skill emits a "verified" outcome that the chain consumes; it does not edit features.json directly.

### Architecture layer dependency check
Before declaring verification passed, run the architecture layer check (manually or via `commands/scan-arch.md`). The convention is:
`references → templates → skills → commands`. Any reverse-direction dependency must be flagged.

### ADR
If verification reveals an ADR assumption is broken, update that ADR's Consequences section (do not silently work around it). Cross-link the affected ADR from the verification report.

### Neutral progress
Sync the verification outcome to the configured neutral progress file (`docs/harness-progress.json` by default; legacy files are read-only) (existing convention) so subsequent sessions see the state.

## Soft hints
- Prefer running the actual feature in a browser/CLI rather than relying on tests alone (per system prompt: type checking is not feature correctness).

## Stop Hook contract
A configured Stop verifier supplies command feedback only. It does not enforce acceptance criteria, intercept commits or certify completion; explicit inspected evidence remains required.

## Verification (covered by evals)
- with-skill: when an acceptance_criterion is unsatisfied, the skill blocks "ready for finishing" and reports the gap.
- baseline: without the skill, "ready" may be claimed despite gaps.

## Codex and GPT-6 workflow adapter

Read `references/platforms/codex.md` from the runtime root when running on Codex; map tools to the actual host and preserve native permissions. Long-running workflow policy is in `references/gpt6-workflows.md`, loaded only when relevant. The user's existing approval and scope remain authoritative; do not repeat approval gates already satisfied. Native execution records a checkpoint, runs all approved tasks, and gets one final independent review. Planning records interfaces and checkable decisions rather than implementing the product during planning. Do not change models or global configuration implicitly.
