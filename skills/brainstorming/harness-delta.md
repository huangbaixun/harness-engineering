# harness-delta: brainstorming

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Spec output path — Override of upstream default
Brainstorming spec output goes to `docs/specs/YYYY-MM-DD-<topic>-design.md` (the harness convention), **not** `docs/superpowers/specs/` (the upstream default in SKILL.md). This is intentional per the integration spec §8 — `docs/specs/` is the canonical location in this plugin.

### Spec front-matter is mandatory
Every spec produced by this skill must include the front-matter declared in `docs/specs/README.md`:

```yaml
---
date: YYYY-MM-DD
topic: <slug>
type: feature | adr-proposal | exploration
status: proposed | building | done
features: [<features.json-id>, ...]   # required when type=feature
adr: [<NNNN>, ...]                    # required when type=adr-proposal
superseded_by: <path>                 # optional
---
```

### features.json writes (only when type=feature)
When the spec's `type` is `feature`, this skill must append one entry per feature to `features.json`:
- `id`, `name`, `priority`, `status: "proposed"`, `spec: <path-to-this-spec>`, `description`, `acceptance_criteria`, `out_of_scope`, `dependencies`, `technical_notes`, `related_files`
- The new entry's `spec:` field MUST point back to the spec file being authored (back-reference)

### ADR writes (only when type=adr-proposal)
When the spec's `type` is `adr-proposal`, this skill must produce one or more ADRs under `docs/decisions/NNNN-<slug>.md` before transitioning to writing-plans.

### Gate to writing-plans handoff
- type=feature without a corresponding features.json entry → **blocked**, must add entry or change type
- type=adr-proposal without a corresponding ADR file → **blocked**, must produce ADR or change type
- type=exploration → can hand off without features.json or ADR (or end without writing-plans at all)

## Soft hints
- Use the brainstorming sections incrementally; do not present the full design in one shot.
- Visual companion is opt-in per spec §6.

## Stop Hook contract
None directly; writing-plans is the next mandatory step after brainstorming completes (forced exit at the workflow level via `harness:using-harness` 1% rule).

## Verification (covered by evals)
- with-skill: type=feature → entry appears in `features.json` before writing-plans handoff
- with-skill: type=adr-proposal → ADR file appears in `docs/decisions/` before writing-plans handoff
- baseline: spec may dangle without features.json sync or ADR
