# harness-delta: writing-plans

## Upstream
superpowers v6.3.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Before producing the plan, read `features.json` (project root preferred; fall back to `docs/templates/generic/features.json.template` for new projects):
- Identify the current in-progress feature (status=`building`) or the next `proposed` feature.
- Extract `acceptance_criteria` as **rigid constraints** — every plan task must trace back to at least one criterion.
- Extract `out_of_scope` — every plan task must NOT touch items here.
- `description` and `technical_notes` provide context but are not constraints.

### features.json writes
Do NOT change `status` here. Status transitions are owned by other skills (see §9.4 of the integration spec). This skill only reads.

### ADR
If, during planning, a new architectural decision surfaces (vendor-vs-build, naming conventions, schema changes, etc.), pause planning and produce an ADR draft in `docs/decisions/NNNN-<slug>.md`. The plan then references the ADR.

### docs / spec linkage
**Override of upstream default.** Plan output goes to `docs/plans/YYYY-MM-DD-<topic>-plan.md` (the harness convention), not `docs/superpowers/plans/` (the upstream default in SKILL.md). This is intentional per the integration spec §8 — `docs/plans/` is the canonical location in this plugin.

The plan must name its source spec in the upstream **`Spec:`** field (added in v6.3.0), pointing at the `docs/specs/` file the plan implements. Do not use a bespoke front-matter key — `harness:subagent-driven-development` reads the upstream field to resolve plan conflicts against the design.

### 100% rigid coverage gate
At the end of plan authoring, verify every entry in `acceptance_criteria` has at least one corresponding task. List any orphan criteria and either add tasks or push back to brainstorming.

### Global Constraints section carries the project rules (new in v6.3.0)
v6.3.0 added a **Global Constraints** block to the plan template, holding project-wide requirements copied verbatim from the spec. In this repo that block must carry, at minimum, the constraints from CLAUDE.md that plan tasks routinely trip over: the `references → templates → skills → commands` dependency direction, the ≤60-line CLAUDE.md template limit, the "hooks are silent on success" rule, and the `{{PLACEHOLDER}}` format. A task's requirements implicitly include this block, so anything omitted here is effectively unenforced.

## Soft hints
- Prefer fewer larger tasks if they remain reviewable (≤20 substeps each); otherwise split. v6.3.0's **Task Right-Sizing** section is the upstream statement of the same idea — a task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate.
- v6.3.0 also added an **Interfaces** block per task (consumes / produces, with exact signatures). Fill it — SDD implementers see only their own task and learn neighbouring names from that block.
- Frequent commits within a task are encouraged.

## Stop Hook contract
None directly. Downstream `harness:executing-plans` and `harness:verification-before-completion` carry the Stop Hook integrations.

## Verification (covered by evals)
- with-skill: when features.json has an in-progress feature, the plan output references each entry in that feature's `acceptance_criteria` (verbatim or paraphrased per eval #1 assertion).
- baseline: without the skill, plan output may diverge from `acceptance_criteria` or invent unrelated tasks.
