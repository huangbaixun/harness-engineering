# harness-delta: receiving-code-review

## Upstream
superpowers v6.4.2 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reconciliation for rigid-constraint feedback
When review feedback proposes a change that touches a **rigid constraint** (an `acceptance_criterion` or `out_of_scope` declaration in `features.json` for the current feature):
- **Option A — accept the change**: update `features.json` to reflect the new constraint AND apply the code change. The constraint update must be committed separately (or as part of the same commit if atomic) with a message explaining the trade-off.
- **Option B — reject the change**: explicitly document the rejection in the PR conversation, citing the existing rigid constraint and why it must hold. Do not silently ignore.

Silent acceptance (apply code change without features.json sync) and silent rejection (close discussion without rationale) are both **prohibited**.

### ADR for architectural-change feedback
If review feedback proposes an architectural change (new dependency, layer-direction reversal, new external service, framework choice), pause acceptance and produce an ADR:
- Either a new ADR if it's a net-new decision, OR
- An update to an existing ADR's `Consequences` section if it modifies a prior decision's assumptions

The PR cannot merge until the ADR is written and reviewed.

### docs
None directly.

## Soft hints
- Prefer applying feedback in the same PR over deferring to a follow-up, unless the change is genuinely out of scope.
- Quote the reviewer's exact words when responding to avoid misinterpretation.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: rigid-constraint feedback → features.json updated OR explicit rejection logged
- with-skill: architectural feedback → ADR produced or updated before merge
- baseline: feedback may be applied without features.json or ADR sync

## Codex and GPT-6 workflow adapter

Read `references/platforms/codex.md` from the runtime root when running on Codex; map tools to the actual host and preserve native permissions. Long-running workflow policy is in `references/gpt6-workflows.md`, loaded only when relevant. The user's existing approval and scope remain authoritative; do not repeat approval gates already satisfied. Native execution records a checkpoint, runs all approved tasks, and gets one final independent review. Planning records interfaces and checkable decisions rather than implementing the product during planning. Do not change models or global configuration implicitly.
