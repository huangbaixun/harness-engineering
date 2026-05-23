---
date: 2026-05-23
topic: superpowers-integration
type: feature
status: done
features:
  - superpowers-vendor-foundation
  - superpowers-vendor-skills
  - superpowers-docs-refresh
adr:
  - 0008
  - 0009
---

# Integrate superpowers v5.1.0 into harness-engineering

## 1. Context

The harness-engineering plugin (current `v1.11.0`) ships 9 skills under the `harness:` namespace. Four of them (`plan`, `tdd`, `verify`, `router`) were forked from `obra/superpowers` at commit `917e5f5` and renamed in v1.10.0 to shorter triggers. Five (`archive`, `audit`, `canary`, `evolve`, `init`) are harness-original.

Since the fork, superpowers has released v5.1.0 with 14 skills (4 of which correspond to our forks plus 10 new ones). The fork is stale and the naming has diverged.

This spec defines how to:
1. Re-align names with superpowers (revert v1.10.0 short names)
2. Vendor all 14 superpowers v5.1.0 skills into this plugin
3. Localize them with a "harness-delta" layer so they integrate with `features.json`, ADRs, and the existing docs system
4. Preserve all 5 harness-original skills

The end state is **19 skills** under `harness:` namespace, with a clear convention for keeping vendored content in sync with upstream over time.

## 2. Goals

- Naming alignment with superpowers wherever the skill semantics are project-agnostic
- Single-source-of-truth localization: upstream content kept verbatim; harness adaptations live in a sidecar
- All 19 skills satisfy ADR-0004 (skill-creator methodology): each has `evals/evals.json` and passes baseline-vs-with-skill review
- `features.json` ↔ design specs ↔ ADRs form a closed information loop
- Future upstream releases (v5.2, v6, …) have an explicit, low-cost sync workflow

## 3. Non-goals

- Migrating user projects in the wild. v2.0.0 is a clean break; user-side migration is a separate concern handled by `harness:audit`.
- Replacing the `commands/` directory wholesale. Only `review-pr.md` is consolidated; the rest remain as fine-grained tooling entry points.
- Adding GitHub-action automation for upstream sync. Manual periodic reconciliation is sufficient.
- Backfilling missing evals for `archive` and `canary`. Both pre-date this work and lack `evals/` directories, which is a pre-existing ADR-0004 violation. Addressing it is a separate cleanup; not regressed by this work.

## 4. Confirmed decisions (locked through brainstorming)

| # | Decision |
|---|---|
| D1 | Full alignment + full vendor: rename the 4 forks back to upstream names; import all new superpowers skills |
| D2 | Vendor pattern with `harness:` namespace prefix — no dependency on the superpowers plugin |
| D3 | Sidecar `harness-delta.md` plus mandatory `UPSTREAM.md` per vendored skill (SKILL.md keeps upstream content verbatim) |
| D4 | All vendored skills run baseline-vs-with-skill evals per ADR-0004 |
| D5 | Spec `type` is one of `feature` / `adr-proposal` / `exploration`; `type=feature` requires a `features.json` entry before handing off to writing-plans |
| D6 | `features.json` schema gains an optional `spec:` field (back-compatible) |
| D7 | Feature lifecycle status simplified to 3 states: `proposed` → `building` → `done`; spec supersession is tracked via spec front-matter `superseded_by:`, not by a status value |
| D8 | The router/meta skill is named `using-harness` (not the literal upstream `using-superpowers`); it is harness-original, not vendored |
| D9 | Migration is 4 phases (Phase 0 foundations → Phase 1 rename → Phase 2 new vendored → Phase 3 docs/release → Phase 4 verify); implemented as 2–3 sequenced plans |
| D10 | Upstream sync uses manual periodic reconciliation + `scripts/sync-superpowers.sh`, not git submodule |
| D11 | `commands/review-pr.md` becomes a thin wrapper around `requesting-code-review` + `receiving-code-review`; other commands retained |
| D12 | `CLAUDE.md` stays under its 60-line limit; detailed conventions move to ADR-0009 + `references/HarnessEngineering.md` + `docs/architecture.md` |
| D13 | A repo-root `features.json` is added so this plugin dogfoods its own conventions; `docs/templates/<lang>/features.json` continues to serve as initialization template |
| D14 | Version bumps `v1.11.0` → `v2.0.0` (breaking) |

## 5. Target topology (19 skills)

```
skills/
├── # vendored from superpowers v5.1.0 (13 — using-superpowers excluded; see D8)
│   ├── writing-plans/                       (renamed from skills/plan)
│   ├── test-driven-development/             (renamed from skills/tdd)
│   ├── verification-before-completion/      (renamed from skills/verify)
│   ├── brainstorming/                       (new)
│   ├── executing-plans/                     (new)
│   ├── subagent-driven-development/         (new)
│   ├── dispatching-parallel-agents/         (new)
│   ├── using-git-worktrees/                 (new)
│   ├── systematic-debugging/                (new)
│   ├── receiving-code-review/               (new)
│   ├── requesting-code-review/              (new)
│   ├── finishing-a-development-branch/      (new)
│   └── writing-skills/                      (new)
└── # harness-original (6)
    ├── using-harness/                       (renamed from skills/router; plays the same routing/meta role that using-superpowers plays in the superpowers plugin, but with a harness-specific skill catalog)
    ├── archive/
    ├── audit/
    ├── canary/
    ├── evolve/
    └── init/
```

## 6. Vendored skill anatomy (4-file structure)

Each vendored skill directory contains exactly:

```
skills/<name>/
├── SKILL.md           # superpowers v5.1.0 content verbatim, with two minimal edits
├── harness-delta.md   # local rules: features.json / ADR / docs integration
├── UPSTREAM.md        # upstream provenance + last-sync record + intentional divergences
└── evals/
    └── evals.json     # ADR-0004 compliance; with-skill must validate harness-delta behavior
```

### 6.1 Allowed edits to SKILL.md

Only two:

1. `name:` frontmatter field changes from `<upstream-name>` to `harness:<upstream-name>` (to avoid collision with the standalone superpowers plugin)
2. A single pointer line inserted after the frontmatter:

```markdown
> **harness local rules:** Always read [harness-delta.md](./harness-delta.md) before invoking this skill. It defines mandatory integrations with features.json, ADR, and docs.
```

All other content matches superpowers v5.1.0 byte-for-byte.

### 6.2 `harness-delta.md` template

```markdown
# harness-delta: <skill-name>

## Upstream
superpowers v5.1.0 / commit <SHA>

## Hard integrations (must do)
- features.json: <specific reads/writes>
- ADR: <when to produce an ADR, where>
- docs: <output path, naming convention>

## Soft hints
- <advisory items>

## Stop Hook contract
- <hooks that enforce this skill's behavior, if any>

## Verification (covered by evals)
- with-skill should produce X; baseline should not
```

### 6.3 `UPSTREAM.md` template

```markdown
# Upstream provenance: <skill-name>

- **Source:** superpowers v5.1.0
- **Commit SHA:** <SHA>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- <line/section> changed because <reason>

## Upstream changes we deliberately did NOT adopt
- <description + reason>
```

### 6.4 `using-harness` exception

`using-harness` is harness-original (D8). It does not carry `UPSTREAM.md` or `harness-delta.md`; it has only `SKILL.md` + `evals/evals.json`. It may borrow phrasing from upstream `using-superpowers` to keep the "1% rule" discipline consistent, but its skill catalog and mandatory invocation table are harness-specific.

## 7. Per-skill integration matrix (harness-delta summary)

| # | Skill | features.json | ADR | Docs / specs | Stop Hook | Cross-skill |
|---|---|---|---|---|---|---|
| 1 | using-harness (original) | — | — | — | session-start.sh outputs router checklist | Acts as the routing table for all 19 skills |
| 2 | writing-plans | **reads** rigid/flexible constraints; 100% rigid-coverage gate | New architectural decision discovered during planning → write ADR | Plan output to `docs/plans/YYYY-MM-DD-<topic>-plan.md` | Stop hook blocks "implement without a plan" | Hands off to executing-plans |
| 3 | test-driven-development | **reads** `acceptance_criteria` of current in-progress feature as test input source | — | — | Stop hook blocks "claim done without tests" | Bound to using-harness 1% rule |
| 4 | verification-before-completion | does **not** modify features.json status itself. The status remains `building` until the `verify → finishing-a-development-branch → archive` chain completes; only then does the chain transition status to `done` (see §9.4) | — | — | Stop hook runs architecture-layer dependency check (references → templates → skills → commands) | Triggers finishing-a-development-branch |
| 5 | brainstorming | New feature → **writes** entry to features.json with rigid/flexible classification | Conceptual decisions produce an ADR | Spec path **redirected** from `docs/superpowers/specs/` to `docs/specs/YYYY-MM-DD-<topic>-design.md` | — | Mandatory writing-plans handoff |
| 6 | executing-plans | **reads** rigid constraints; must not violate during execution | — | Reads plans from `docs/plans/` | Stop hook integrates with plan-stop | Triggers finishing-a-development-branch at completion |
| 7 | subagent-driven-development | Each subagent task = one features.json entry (no orphan work) | — | — | — | Reads `.claude/agents/` project-specific definitions |
| 8 | dispatching-parallel-agents | Parallel tasks each map to a features.json entry | — | — | — | Must respect architecture layer dependency direction |
| 9 | using-git-worktrees | Worktree branch name = `feature/<features.json-key>` | — | — | — | On worktree merge, triggers `harness:archive` |
| 10 | systematic-debugging | Bug must reference a feature or use `bug:` prefix | If a bug invalidates an ADR assumption, update that ADR's Consequences | Debug notes → `docs/incidents/YYYY-MM-DD-<slug>.md` (**new directory**) | — | Pairs with `harness:canary` rollback in production incidents |
| 11 | receiving-code-review | Review feedback affecting a rigid constraint → write back to features.json or reject with reason | Feedback proposing architectural change → write/update ADR | — | — | — |
| 12 | requesting-code-review | Pre-review check = all rigid constraints satisfied | — | PR description template includes `feature: <key>` line | — | — |
| 13 | finishing-a-development-branch | Sets feature status to `done`; syncs `claude-progress.json` | — | — | — | **Mandatory** call to `harness:archive`; prompts `harness:canary` if deploys touched |
| 14 | writing-skills | — | Enforces ADR-0004 skill-creator methodology | — | — | If new skill is an upstream fork, requires the 4-file vendored structure |

## 8. New docs conventions

- `docs/specs/` — output of brainstorming (replaces upstream default `docs/superpowers/specs/`). The existing artifact under `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` is migrated as part of Phase 3.
- `docs/incidents/` — **new**; output of `systematic-debugging`
- `docs/plans/` — existing; output of writing-plans
- `docs/decisions/` — existing; ADRs

## 9. `docs/specs/` ↔ `features.json` linkage

### 9.1 Spec types (front-matter `type`)

| `type` | Must produce features.json entry? | Must produce ADR? |
|---|---|---|
| `feature` | yes (≥1 entry) | optional |
| `adr-proposal` | no | yes (≥1) |
| `exploration` | no | no |

Gate: brainstorming may not hand off to writing-plans if `type=feature` and no corresponding features.json entries exist; or if `type=adr-proposal` and no ADR file is produced.

### 9.2 Spec front-matter

```yaml
---
date: YYYY-MM-DD
topic: <slug>
type: feature | adr-proposal | exploration
status: proposed | building | done
features: [<key>, ...]   # required when type=feature
adr: [<NNNN>, ...]       # required when type=adr-proposal
superseded_by: <path>    # optional; used in place of a `superseded` status
---
```

### 9.3 features.json entry (new `spec` field)

```json
{
  "key": "superpowers-vendor-foundation",
  "spec": "docs/specs/2026-05-23-superpowers-integration-design.md",
  "rigid": ["..."],
  "flexible": ["..."],
  "acceptance_criteria": ["..."],
  "status": "proposed"
}
```

The `spec` field is **optional** (back-compatible). `harness:init` template populates it by default. `harness:audit` reports its absence as a hint, not an error.

### 9.4 Lifecycle synchronization

| Event | features.json status | spec status |
|---|---|---|
| Brainstorming completes; spec written | new entry, `proposed` | `proposed` |
| Plan approved → execution → verification passes | `building` | `building` |
| Archive completes | `done` | `done` |
| Spec replaced by a new design | (old) entry removed or pointed away | (old) `superseded_by:` set; new spec is `proposed` |

This synchronization table is enforced by `verification-before-completion/harness-delta.md` and `brainstorming/harness-delta.md`.

## 10. Migration phases

### Phase 0 — Foundations

- ADR-0008 "Vendor superpowers v5.1.0" supersedes the existing fork strategy
- ADR-0009 "harness-delta sidecar 4-file convention"
- `features.json` schema migration: `spec` field added; templates updated under `docs/templates/<lang>/features.json`
- New directories `docs/specs/` and `docs/incidents/` (each with a `README.md` describing the convention)
- Repo-root `features.json` introduced (per D13) with initial entries for this integration project

### Phase 1 — Rename the 4 existing forks (breaking)

For each rename, use `git mv` to preserve history:

| From | To |
|---|---|
| `skills/plan/` | `skills/writing-plans/` |
| `skills/tdd/` | `skills/test-driven-development/` |
| `skills/verify/` | `skills/verification-before-completion/` |
| `skills/router/` | `skills/using-harness/` |

For each renamed directory:

1. Replace `SKILL.md` content with superpowers v5.1.0 upstream verbatim (except `using-harness`, which stays harness-original)
2. Update frontmatter `name:` to `harness:<new-name>`
3. Insert the "harness local rules" pointer line (vendored skills only)
4. Extract the existing inline harness-delta content into a new `harness-delta.md`
5. Add `UPSTREAM.md`
6. Author `evals/evals.json` per ADR-0004. Only `skills/router/evals/` currently exists; for that one, port its test cases and rewrite them against the new structure. For `plan`, `tdd`, and `verify`, author fresh evals — these three forks currently lack `evals/` directories.
7. Run with-skill vs baseline evals; pass eval-viewer review

A repo-wide grep gate at the end of Phase 1 must show 0 hits for `harness:plan`, `harness:tdd`, `harness:verify`, `harness:router` outside of `CHANGELOG.md` and the design docs themselves.

### Phase 2 — Vendor the 10 new skills

Each new vendored skill follows the same 4-file structure. The 10 skills can be processed in batches of 3–4, each batch as a single commit with eval-viewer review. `dispatching-parallel-agents` is itself usable for batch parallelism once it lands.

Per-skill checklist:

1. Copy upstream `SKILL.md` from cache
2. Apply the two allowed edits (name + pointer)
3. Author `harness-delta.md` per the integration matrix (Section 7)
4. Author `UPSTREAM.md`
5. Author `evals/evals.json` per ADR-0004
6. Run evals; pass eval-viewer review

### Phase 3 — Docs and release

- `docs/architecture.md` updated to the 19-skill topology, new namespace, vendored vs original distinction
- `README.md` and `README.zh-CN.md` skill catalog updated
- `CLAUDE.md` adds 2 lines under "Prohibited Practices" (no other expansion); detail goes to ADR-0009 and `references/HarnessEngineering.md`
- `commands/review-pr.md` rewritten as a thin wrapper around `requesting-code-review` + `receiving-code-review`
- Existing artifact `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` is moved to `docs/specs/` for consistency
- `plugin.json` version → `2.0.0`
- `CHANGELOG.md` `v2.0.0` entry documents the breaking rename, the 13 new vendored skills, the schema migration, and the new ADRs

### Phase 4 — Verification

- Repo-wide grep gate: 0 hits for the 4 old short names
- All 14 reorganized skills' evals green (13 vendored sidecar-style skills + `using-harness`)
- `harness:init` produces a project template referencing the new skill names only
- `harness:audit` recognizes the new structure
- The 5 unchanged harness-original skills (`archive`, `audit`, `canary`, `evolve`, `init`) verified intact via manual test
- Repo-root `features.json` entries for this integration project transition to `done`

## 11. Upstream sync workflow (post-v2.0.0)

`scripts/sync-superpowers.sh` (new, Phase 0):

- Reads each vendored skill's `UPSTREAM.md` for the recorded upstream commit SHA
- Diffs that SHA against the current cache of superpowers (latest installed version)
- Emits a per-skill report: net new lines, removed lines, file-level diff summary
- Does NOT auto-apply changes

The reconciliation cadence is once per superpowers minor release. Each skill's diff is reviewed individually; accepted changes go through the eval-viewer loop again before commit. The judgment of "accept / skip / extend harness-delta" is intentionally kept human.

## 12. `commands/` disposition

| Command | Action |
|---|---|
| `review-pr.md` | Rewrite as a thin wrapper around the two code-review skills |
| `audit.md` | Keep (entry point for `harness:audit` skill) |
| `canary.md` | Keep (entry point for `harness:canary`) |
| `init.md` | Keep (entry point for `harness:init`) |
| `scan-arch.md` / `sync-docs.md` | Keep (sub-steps of `harness:archive`) |
| `scan-entropy.md` / `trim.md` | Keep (sub-steps of `harness:evolve`) |
| `dump.md` / `assign.md` | Keep (independent utilities) |

The relationship between commands and skills is documented in `docs/architecture.md`.

## 13. CLAUDE.md plan

The only additions to `CLAUDE.md` are 2 lines under "Prohibited Practices":

- "Never vendor a superpowers skill without `harness-delta.md`, `UPSTREAM.md`, and `evals/evals.json`."
- "Never modify a vendored SKILL.md body. Only `name:` frontmatter and the inserted `harness local rules` pointer line may be edited."

Everything else stays in:

- ADR-0009 (the sidecar convention itself)
- `references/HarnessEngineering.md` (rationale and worked examples)
- `docs/architecture.md` (topology, naming, command/skill relationships)

This preserves the documented 60-line limit on CLAUDE.md.

## 14. Versioning

| Component | Before | After |
|---|---|---|
| `plugin.json` version | 1.11.0 | 2.0.0 |
| Skill namespace | `harness:` | `harness:` (unchanged) |
| Slash commands (4 affected) | `/harness:plan`, `/harness:tdd`, `/harness:verify`, `/harness:router` | `/harness:writing-plans`, `/harness:test-driven-development`, `/harness:verification-before-completion`, `/harness:using-harness` |
| Slash commands (10 new) | — | `/harness:brainstorming`, `/harness:executing-plans`, … |

`CHANGELOG.md` `v2.0.0` entry must call out the rename, the new skills, the schema migration, and link both ADRs.

## 15. Dogfooding via root `features.json`

A repo-root `features.json` is introduced in Phase 0 with three entries for this integration project:

| Key | Maps to phases | Initial status |
|---|---|---|
| `superpowers-vendor-foundation` | Phase 0 + Phase 1 | `proposed` |
| `superpowers-vendor-skills` | Phase 2 | `proposed` |
| `superpowers-docs-refresh` | Phase 3 + Phase 4 | `proposed` |

Each entry's `spec` field points back to this design document. ADR-0003 ("dogfooding-harness") is thereby satisfied at the plugin-self level — currently it is not.

## 16. ADRs to write in Phase 0

- **ADR-0008** "Vendor superpowers v5.1.0" — supersedes the previous fork strategy embedded in v1.9.x–v1.10.x; documents the vendor + sidecar choice and rejects the submodule alternative.
- **ADR-0009** "harness-delta sidecar 4-file convention" — defines the per-skill anatomy (SKILL/harness-delta/UPSTREAM/evals) as a first-class structural rule and feeds back into ADR-0004's skill-creator workflow.

## 17. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Existing evals (4 forks have `evals/`) are lost during rename | Phase 1 uses `git mv` and explicitly ports test cases to the new structure |
| `features.json` schema change breaks old user projects | New `spec` field is optional; `harness:audit` reports its absence as a hint, not an error |
| Stray references to old short names (`harness:plan`, etc.) in `commands/` or docs | Phase 1 ends with a grep gate that blocks Phase 2 until clean |
| Recovering harness-delta content from existing inline forks relies on memory | Current forks already carry "@upstream / @harness-delta" preamble blocks — they are the source for the new `harness-delta.md` extraction |
| Phase 2 evals workload (10 new skills × baseline-vs-with-skill) is large | Batch in groups of 3–4 with parallel agents per ADR-0004's accepted pattern |
| Future superpowers releases drift away from this fork | Section 11 sync workflow + `UPSTREAM.md` per-skill record |
| `using-harness` content quality slips below `using-superpowers` upstream | Phase 1 explicitly ports the routing-table discipline; evals validate the 1% rule still triggers |

## 18. Open questions (acknowledged, deferred)

These are not in scope for this design; if they later need a position, treat each as its own brainstorming + ADR:

- Whether `commands/` should eventually be fully replaced by skills (separate ADR if pursued)
- Whether to ever publish harness's vendored skills back upstream as a "harness flavor" of superpowers
- Whether to introduce a CI job that runs `scripts/sync-superpowers.sh` and posts a sync-diff issue automatically

## 19. Implementation handoff

This spec is the input to writing-plans. Expected output is 2–3 sequenced implementation plans:

- Plan A: Phase 0 + Phase 1 (foundations + rename; tightly coupled)
- Plan B: Phase 2 (10 new vendored skills; parallelizable)
- Plan C: Phase 3 + Phase 4 (docs, release, verification)

The exact split is the writing-plans skill's decision.
