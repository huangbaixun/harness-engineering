# harness-delta: executing-plans

## Upstream
superpowers v6.3.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Before execution begins:
- Locate the `building` feature whose `spec` matches the plan being executed (or whose `technical_notes` references this plan file).
- Extract `acceptance_criteria` as **rigid constraints** — every task in the plan must trace to at least one criterion; do not invent tasks outside that boundary.
- Extract `out_of_scope` — pause execution and ask the user if any task in the plan would touch out-of-scope items.

### Plans directory — Override of upstream default
Plans are read from `docs/plans/YYYY-MM-DD-<topic>-plan.md` (the harness convention), **not** `docs/superpowers/plans/` (the upstream default). This matches `harness:writing-plans` output.

### features.json writes
None directly. Status transitions are owned by the verify → finishing → archive chain.

### ADR
None directly. If executing-plans surfaces an architectural decision that wasn't anticipated during writing-plans, pause execution and escalate to brainstorming + ADR before continuing.

## Soft hints
- Run gates (tests / JSON validation / smoke tests) after each task, not just at the end.
- If a task fails, do not silently retry — report and surface for review.

## Stop Hook contract
Existing Stop hook ("claim done without tests") plus this skill's per-task verification close the loop. The Stop hook trips if a `git commit` is attempted while tests fail or while rigid constraints from features.json are unsatisfied.

## Verification (covered by evals)
- with-skill: when a plan tries to add tasks outside features.json acceptance_criteria, the skill blocks or asks for spec amendment
- with-skill: completion marker only set after all rigid constraints are demonstrably satisfied
- baseline: plan execution may complete with orphan tasks or unsatisfied criteria
