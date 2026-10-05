# harness-delta: executing-plans

## Upstream
superpowers v6.4.2 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Before execution begins:
- Locate the `building` feature whose `spec` matches the plan being executed (or whose `technical_notes` references this plan file).
- Extract `acceptance_criteria` as **rigid constraints** — every task in the plan must trace to at least one criterion; do not invent tasks outside that boundary.
- Extract `out_of_scope` — pause execution and ask the user if any task in the plan would touch out-of-scope items.

### Plans directory — Override of upstream default
Plans are read from `docs/plans/YYYY-MM-DD-<topic>-plan.md` (the harness convention), **not** `docs/superpowers/plans/` (the upstream default). This matches `harness:writing-plans` output.

### features.json writes
None directly. Status transitions follow the selected verified integration workflow; do not mark done before its completion requirements.

### ADR
None directly. If executing-plans surfaces an architectural decision that wasn't anticipated during writing-plans, pause execution and escalate to brainstorming + ADR before continuing.

## Soft hints
- Run gates (tests / JSON validation / smoke tests) after each task, not just at the end.
- Fix routine local failures within the approved scope; surface unresolved blockers and new decisions.

## Stop Hook contract
Configured Stop verification is an additional feedback mechanism. It does not intercept git commit, enforce acceptance criteria or replace explicit verification. An unconfigured check is unknown, never passed.

## Verification (covered by evals)
- with-skill: when a plan tries to add tasks outside features.json acceptance_criteria, the skill blocks or asks for spec amendment
- with-skill: completion marker only set after all rigid constraints are demonstrably satisfied
- baseline: plan execution may complete with orphan tasks or unsatisfied criteria

## Codex and GPT-6 workflow adapter

Read `references/platforms/codex.md` from the runtime root when running on Codex; map tools to the actual host and preserve native permissions. Long-running workflow policy is in `references/gpt6-workflows.md`, loaded only when relevant. The user's existing approval and scope remain authoritative; do not repeat approval gates already satisfied. Native execution records a checkpoint, runs all approved tasks, and gets one final independent review. Planning records interfaces and checkable decisions rather than implementing the product during planning. Do not change models or global configuration implicitly.
