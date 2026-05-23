# harness-delta: writing-plans

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

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
Plan output: `docs/plans/YYYY-MM-DD-<topic>-plan.md`. The plan front-matter (or first paragraph) must reference the source spec under `docs/specs/`.

### 100% rigid coverage gate
At the end of plan authoring, verify every entry in `acceptance_criteria` has at least one corresponding task. List any orphan criteria and either add tasks or push back to brainstorming.

## Soft hints
- Prefer fewer larger tasks if they remain reviewable (≤20 substeps each); otherwise split.
- Frequent commits within a task are encouraged.

## Stop Hook contract
None directly. Downstream `harness:executing-plans` and `harness:verification-before-completion` carry the Stop Hook integrations.

## Verification (covered by evals)
- with-skill: when features.json has an in-progress feature, the plan output references that feature's `acceptance_criteria` line-for-line.
- baseline: without the skill, plan output may diverge from `acceptance_criteria` or invent unrelated tasks.
