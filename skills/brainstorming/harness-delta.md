# harness-delta: brainstorming

## Upstream
superpowers v6.3.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Path classification decides which gates fire (new in v6.3.0)
Upstream v6.3.0 replaced the single "always write a spec" flow with three paths — **spike**, **bounded**, **architectural**. The harness gates below are scoped accordingly:

| Upstream path | Spec file written? | harness gates that apply |
|---|---|---|
| **spike** | no | None of the spec/features.json/ADR gates. Report the finding; if the spike's answer turns into work, re-classify and the gates apply to that new task. |
| **bounded** | no | No spec file, so no front-matter or features.json/ADR gate. **But** if the change touches a `features.json` `out_of_scope` entry, or reverses the `references → templates → skills → commands` dependency direction, the task is not bounded — upgrade to architectural. |
| **architectural** | yes | All gates below apply in full. |

The upgrade ratchet is one-way and it is a harness rule too: discovering a features.json or ADR obligation mid-task upgrades the path. Never downgrade to skip a gate.

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

### Gate to writing-plans handoff (architectural path only)
- type=feature without a corresponding features.json entry → **blocked**, must add entry or change type
- type=adr-proposal without a corresponding ADR file → **blocked**, must produce ADR or change type
- type=exploration → can hand off without features.json or ADR (or end without writing-plans at all)

## Soft hints
- Use the brainstorming sections incrementally; do not present the full design in one shot.
- Visual companion is opt-in per spec §6. v6.3.0 made the offer **just-in-time** rather than upfront —
  do not offer it before a question actually needs showing.
- The `scripts/` companion (visual companion server) is now vendored; it was missing before this sync.

## Stop Hook contract
None directly; writing-plans is the next mandatory step after brainstorming completes (forced exit at the workflow level via `harness:using-harness` 1% rule).

## Verification (covered by evals)
- with-skill: type=feature → entry appears in `features.json` before writing-plans handoff
- with-skill: type=adr-proposal → ADR file appears in `docs/decisions/` before writing-plans handoff
- baseline: spec may dangle without features.json sync or ADR
