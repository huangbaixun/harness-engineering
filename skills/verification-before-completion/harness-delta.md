# harness-delta: verification-before-completion

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

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

### claude-progress.json
Sync the verification outcome to `claude-progress.json` (existing convention) so subsequent sessions see the state.

## Soft hints
- Prefer running the actual feature in a browser/CLI rather than relying on tests alone (per system prompt: type checking is not feature correctness).

## Stop Hook contract
Existing Stop hooks for "claim done without tests" plus this skill's architecture layer check together gate the completion claim.

## Verification (covered by evals)
- with-skill: when an acceptance_criterion is unsatisfied, the skill blocks "ready for finishing" and reports the gap.
- baseline: without the skill, "ready" may be claimed despite gaps.
