# Plan A — Phase 0 (Foundations) + Phase 1 (Rename 4 Forks) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the foundations (ADRs, schema migration, scripts, new docs directories, root features.json) and rename the 4 existing superpowers forks to their upstream names with the 4-file vendored structure.

**Architecture:** Two coupled sub-phases. Phase 0 establishes durable conventions (ADR-0008, ADR-0009) and infrastructure (schema, root features.json, sync script, new docs dirs) that Phase 1 depends on. Phase 1 then `git mv`-renames the 4 forks (`router`/`plan`/`tdd`/`verify` → `using-harness`/`writing-plans`/`test-driven-development`/`verification-before-completion`) and populates each with the 4-file structure (SKILL.md / harness-delta.md / UPSTREAM.md / evals/evals.json), except `using-harness` which is harness-original and uses a 2-file structure (SKILL.md / evals/evals.json).

**Tech Stack:** Markdown for ADRs and skill files, JSON for features.json and evals, Bash for sync script, git for renames and commits.

**Spec gap noted:** The current `docs/templates/generic/features.json.template` uses `status: "pending"` and an `id` field, not matching the spec §9.3 example. Per D7 (3-state status) and D6 (add `spec:` field), Task 0.4 migrates the template schema explicitly: status enum `pending → proposed`, `in_progress → building`, `completed → done`; adds optional `spec:` field. The `id` field is **kept** as the entry key — the spec's `key` was illustrative. The `rigid`/`flexible` classification mentioned in the spec lives in `harness:writing-plans`' `harness-delta.md` as a skill-side convention, not as new schema fields.

**Source spec:** `docs/specs/2026-05-23-superpowers-integration-design.md`

**Upstream cache base** (path used by Phase 1 tasks to copy SKILL.md content from): `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/<name>/SKILL.md`. If your machine has a different superpowers cache path, locate it via `find ~/.claude -type d -name 'superpowers' -path '*/5.1.0/*'`.

**Upstream SHA capture** (one-time, used by Tasks 1.2/1.3/1.4 to fill UPSTREAM.md's `Commit SHA:` line):

```bash
UPSTREAM_BASE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0"
UPSTREAM_SHA="$(git -C "$UPSTREAM_BASE" rev-parse HEAD 2>/dev/null || echo 'v5.1.0')"
echo "$UPSTREAM_SHA"
```

Record the printed value. The Phase 1 tasks substitute it into their UPSTREAM.md files as the literal SHA — do not write the instructional text into the file.

---

## Task 0.1: Write ADR-0008 "Vendor superpowers v5.1.0"

**Files:**
- Create: `docs/decisions/0008-vendor-superpowers-v5.md`

- [ ] **Step 1: Write the ADR**

Create `docs/decisions/0008-vendor-superpowers-v5.md` with this content:

```markdown
# ADR-0008: Vendor superpowers v5.1.0 into harness-engineering

## Status
Accepted — 2026-05-23

## Supersedes
The implicit fork strategy embedded in v1.9.x–v1.11.x, where four skills (`plan`, `tdd`, `verify`, `router`) were forked from `obra/superpowers @ 917e5f5` and renamed for shorter triggers.

## Context
The harness-engineering plugin diverged from `obra/superpowers` at commit `917e5f5`. Since then upstream released v5.1.0 with 14 skills — 4 corresponding to our forks plus 10 new ones (`brainstorming`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees`, `systematic-debugging`, `receiving-code-review`, `requesting-code-review`, `finishing-a-development-branch`, `writing-skills`).

The fork is stale, naming is divergent, and a per-skill maintenance contract for ongoing sync is missing.

## Decision
Vendor all 14 superpowers v5.1.0 skills into this plugin (13 with sidecar structure; `using-harness` as harness-original — see Section 4). End state: 19 skills under the `harness:` namespace.

## Considered alternatives
1. **Depend on the superpowers plugin** — rejected: introduces a runtime dependency on a separately-installed plugin and prevents harness from carrying its own localized rules.
2. **Git submodule of upstream** — rejected: automated sync conflicts with ADR-0004's requirement that each skill change go through the skill-creator eval loop. Each upstream diff is a judgment call, not a mechanical apply.
3. **Keep only the 4 existing forks; do not import the 10 new ones** — rejected: misses real capability (brainstorming, executing-plans, writing-skills are first-class needs of this plugin's workflow).

## Consequences
**Positive:**
- Single-source-of-truth: harness owns its skills regardless of upstream plugin availability
- Naming aligned with superpowers (same patterns, discoverable)
- Future sync is explicit and reviewable per ADR-0004

**Negative:**
- Breaking change: 4 old slash command names (`/harness:plan` etc.) are replaced
- Maintenance burden: each upstream release requires per-skill reconciliation

## Implementation
See `docs/specs/2026-05-23-superpowers-integration-design.md` (covers all phases) and `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` (Phase 0 + Phase 1 execution).

## Related
- ADR-0004 (skill-creator methodology) — applies to all 14 reorganized skills' evals
- ADR-0009 (harness-delta sidecar 4-file convention) — sibling decision establishing per-skill structure
- ADR-0007 (Claude Code only) — namespace context
```

- [ ] **Step 2: Verify the file was created**

Run: `test -f docs/decisions/0008-vendor-superpowers-v5.md && wc -l docs/decisions/0008-vendor-superpowers-v5.md`
Expected: line count > 30

- [ ] **Step 3: Commit**

```bash
git add docs/decisions/0008-vendor-superpowers-v5.md
git commit -m "docs(adr): add ADR-0008 vendor superpowers v5.1.0"
```

---

## Task 0.2: Write ADR-0009 "harness-delta sidecar 4-file convention"

**Files:**
- Create: `docs/decisions/0009-harness-delta-sidecar.md`

- [ ] **Step 1: Write the ADR**

Create `docs/decisions/0009-harness-delta-sidecar.md` with this content:

```markdown
# ADR-0009: harness-delta sidecar 4-file convention for vendored skills

## Status
Accepted — 2026-05-23

## Context
ADR-0008 commits to vendoring 13 superpowers skills with local rules layered on top (integration with `features.json`, ADRs, docs). The structural question is *where* those local rules live without polluting upstream content.

Three patterns were considered during brainstorming (recorded in `docs/specs/2026-05-23-superpowers-integration-design.md` §2):

1. **Inline delta** in `SKILL.md` (the pattern used by the previous v1.x forks)
2. **Sidecar delta file** alongside an unmodified upstream `SKILL.md`
3. **Wrapper skill** that calls the upstream skill and adds checks

## Decision
Each vendored skill directory contains exactly four files:

```
skills/<name>/
├── SKILL.md           # superpowers v5.1.0 content verbatim, only frontmatter `name` changed + one pointer line inserted
├── harness-delta.md   # harness-specific integrations (features.json / ADR / docs / Stop Hook contract)
├── UPSTREAM.md        # provenance: source commit SHA, last-sync date, intentional divergences
└── evals/
    └── evals.json     # per ADR-0004; tests that harness-delta behavior takes effect
```

`using-harness` is **exempt** (harness-original skill, no upstream); it has 2 files: `SKILL.md` + `evals/evals.json`.

## Allowed edits to vendored `SKILL.md`
Only two:
1. `name:` frontmatter field becomes `harness:<upstream-name>`
2. One pointer line inserted after the frontmatter:
   > **harness local rules:** Always read [harness-delta.md](./harness-delta.md) before invoking this skill. It defines mandatory integrations with features.json, ADR, and docs.

All other content is byte-for-byte upstream.

## Considered alternatives
- **Inline delta** — rejected: makes upstream sync diff noisy and error-prone
- **Wrapper skill** — rejected: duplicates 99% of content; two "session-start" meta skills conflict

## Consequences
**Positive:**
- Upstream diffs stay clean — sync workflow (Section 11 of integration spec) becomes mechanical
- Local rules are independently editable and lint-able
- Provenance per skill is explicit (UPSTREAM.md)

**Negative:**
- Agents must load two files per skill invocation
- Discipline required: SKILL.md body must never be edited outside the two allowed changes

## Implementation
Phase 1 of `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` applies this convention to the 4 renamed forks. Phase 2 (separate plan) applies it to the 10 new vendored skills.

## Related
- ADR-0004 (skill-creator methodology)
- ADR-0008 (vendor superpowers v5.1.0)
```

- [ ] **Step 2: Verify the file**

Run: `test -f docs/decisions/0009-harness-delta-sidecar.md && head -5 docs/decisions/0009-harness-delta-sidecar.md`
Expected: heading `# ADR-0009: ...` visible

- [ ] **Step 3: Commit**

```bash
git add docs/decisions/0009-harness-delta-sidecar.md
git commit -m "docs(adr): add ADR-0009 harness-delta sidecar 4-file convention"
```

---

## Task 0.3: Update ADR index

**Files:**
- Modify: `docs/decisions/README.md`

- [ ] **Step 1: Append two new rows to the table**

Read `docs/decisions/README.md`, then use the Edit tool with this `old_string`:

```
| 0007 | Claude Code Only — 移除工具无关兼容层 | 已采纳 | 2026-05-23 |
```

And this `new_string`:

```
| 0007 | Claude Code Only — 移除工具无关兼容层 | 已采纳 | 2026-05-23 |
| 0008 | Vendor superpowers v5.1.0 | 已采纳 | 2026-05-23 |
| 0009 | harness-delta sidecar 4 文件结构约定 | 已采纳 | 2026-05-23 |
```

- [ ] **Step 2: Verify both rows present**

Run: `grep -c '^| 000[89] |' docs/decisions/README.md`
Expected: `2`

- [ ] **Step 3: Commit**

```bash
git add docs/decisions/README.md
git commit -m "docs(adr): index ADR-0008 and ADR-0009"
```

---

## Task 0.4: Migrate features.json template schema

**Files:**
- Modify: `docs/templates/generic/features.json.template`

**Schema migration:**
- Status enum: `pending → proposed`, `in_progress → building`, `completed → done`
- New optional field on each entry: `"spec": "<path-to-spec-md>"` or omit
- Add a top-level `"schema_version": "2.0"` field

- [ ] **Step 1: Write the new template**

Read the existing `docs/templates/generic/features.json.template`, then replace its contents with:

```json
{
  "schema_version": "2.0",
  "version": "1.0",
  "product": "{{PROJECT_NAME}}",
  "last_updated": "{{TIMESTAMP}}",
  "updated_by": "{{AUTHOR}}",

  "features": [
    {
      "id": "F001",
      "name": "{{FEATURE_NAME}}",
      "priority": 1,
      "status": "proposed",
      "spec": "",
      "description": "{{FEATURE_DESCRIPTION}}",
      "acceptance_criteria": [
        "{{CRITERION_1}}",
        "{{CRITERION_2}}"
      ],
      "out_of_scope": [],
      "dependencies": [],
      "technical_notes": "",
      "related_files": []
    }
  ],

  "constraints": {
    "implementation_order": "严格按 priority 顺序，有 dependency 的特性必须等依赖完成",
    "code_state_rule": "每个特性完成后代码必须可合并（测试全通过、无 TODO、有基本注释）",
    "scope_rule": "out_of_scope 的内容不实现，即使很简单。需求变更必须先更新本文件",
    "status_lifecycle": "proposed → building → done。proposed = 已 brainstorm 但未 plan；building = plan 已批准、execute/verify 进行中；done = archive 完成"
  }
}
```

- [ ] **Step 2: Validate JSON**

Run: `python3 -m json.tool docs/templates/generic/features.json.template > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add docs/templates/generic/features.json.template
git commit -m "feat(templates): migrate features.json to schema 2.0 (3-state status + spec field)"
```

---

## Task 0.5: Create `docs/specs/` directory with README

**Files:**
- Create: `docs/specs/README.md`
- Existing (moved later in Phase 3): `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` (left alone for now)
- Already present: `docs/specs/2026-05-23-superpowers-integration-design.md` (the spec itself)

- [ ] **Step 1: Write the README**

Create `docs/specs/README.md`:

```markdown
# docs/specs/

This directory holds design specs produced by `harness:brainstorming`.

## Convention
- Filename: `YYYY-MM-DD-<topic>-design.md`
- Front-matter (required):

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

## Spec ↔ features.json linkage
- `type: feature` requires one or more entries in `features.json`, each with a `spec:` pointer back to this file (back-reference).
- `type: adr-proposal` requires one or more ADR files under `docs/decisions/`.
- `type: exploration` may dangle as historical record.

## Migration note
Earlier specs under `docs/superpowers/specs/` (pre-v2.0.0 default location) are migrated here in Phase 3 of the superpowers integration project. New specs always land in `docs/specs/`.
```

- [ ] **Step 2: Verify**

Run: `test -f docs/specs/README.md && grep -q 'type: feature' docs/specs/README.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add docs/specs/README.md
git commit -m "docs(specs): establish docs/specs/ directory with linkage README"
```

---

## Task 0.6: Create `docs/incidents/` directory with README

**Files:**
- Create: `docs/incidents/README.md`

- [ ] **Step 1: Write the README**

Create `docs/incidents/README.md`:

```markdown
# docs/incidents/

This directory holds debug notes produced by `harness:systematic-debugging`.

## Convention
- Filename: `YYYY-MM-DD-<slug>.md`
- Each incident note should record:
  - Symptom observed
  - Reproduction steps
  - Root cause (or hypothesis if unresolved)
  - Fix applied (or escalation path if still open)
  - Whether the incident invalidated any ADR assumption — if so, link the affected ADR and update its **Consequences** section

## Cross-skill triggers
- Production incidents may invoke `harness:canary` rollback procedures.
- Incidents tied to a `features.json` entry should set that entry's status or link back via `related_files`.
```

- [ ] **Step 2: Verify**

Run: `test -f docs/incidents/README.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add docs/incidents/README.md
git commit -m "docs(incidents): establish docs/incidents/ directory"
```

---

## Task 0.7: Create repo-root `features.json` (dogfood entries)

**Files:**
- Create: `/features.json` (repo root)

- [ ] **Step 1: Write the file**

Create `features.json` at the repo root:

```json
{
  "schema_version": "2.0",
  "version": "1.0",
  "product": "harness-engineering",
  "last_updated": "2026-05-23",
  "updated_by": "huangbaixun",

  "features": [
    {
      "id": "F001",
      "name": "superpowers-vendor-foundation",
      "priority": 1,
      "status": "proposed",
      "spec": "docs/specs/2026-05-23-superpowers-integration-design.md",
      "description": "Phase 0 + Phase 1 of the superpowers integration: ADRs, schema migration, sync script, new docs dirs, and rename the 4 existing forks (router/plan/tdd/verify) to upstream names.",
      "acceptance_criteria": [
        "ADR-0008 and ADR-0009 committed and indexed",
        "features.json schema migrated to 2.0; status enum is proposed/building/done",
        "docs/specs/ and docs/incidents/ exist with READMEs",
        "scripts/sync-superpowers.sh exists and is executable",
        "skills/{using-harness,writing-plans,test-driven-development,verification-before-completion}/ exist with the 4-file structure (2-file for using-harness)",
        "Repo-wide grep shows 0 hits for old short names (harness:plan, harness:tdd, harness:verify, harness:router) outside CHANGELOG.md and existing design docs"
      ],
      "out_of_scope": [
        "Phase 2 (10 new vendored skills)",
        "Phase 3/4 (docs refresh + verification)"
      ],
      "dependencies": [],
      "technical_notes": "Plan: docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md",
      "related_files": [
        "docs/decisions/0008-vendor-superpowers-v5.md",
        "docs/decisions/0009-harness-delta-sidecar.md",
        "docs/templates/generic/features.json.template",
        "scripts/sync-superpowers.sh"
      ]
    },
    {
      "id": "F002",
      "name": "superpowers-vendor-skills",
      "priority": 2,
      "status": "proposed",
      "spec": "docs/specs/2026-05-23-superpowers-integration-design.md",
      "description": "Phase 2: vendor 10 new superpowers skills (brainstorming, executing-plans, subagent-driven-development, dispatching-parallel-agents, using-git-worktrees, systematic-debugging, receiving-code-review, requesting-code-review, finishing-a-development-branch, writing-skills) with the 4-file sidecar structure and ADR-0004 evals each.",
      "acceptance_criteria": [
        "10 new skill directories under skills/ each with SKILL.md, harness-delta.md, UPSTREAM.md, evals/evals.json",
        "All 10 evals pass with-skill vs baseline review per ADR-0004"
      ],
      "out_of_scope": [
        "Renaming the 4 existing forks (handled in F001)"
      ],
      "dependencies": ["F001"],
      "technical_notes": "Plan: docs/plans/<TBD>-phase-2-vendor-new-skills.md (authored after F001 completes)",
      "related_files": []
    },
    {
      "id": "F003",
      "name": "superpowers-docs-refresh",
      "priority": 3,
      "status": "proposed",
      "spec": "docs/specs/2026-05-23-superpowers-integration-design.md",
      "description": "Phase 3 + 4: update architecture.md, READMEs, CLAUDE.md (≤60 lines), rewrite commands/review-pr.md as wrapper, bump version to 2.0.0, write CHANGELOG, then run verification (grep gate, evals, init-template, audit).",
      "acceptance_criteria": [
        "docs/architecture.md reflects 19-skill topology",
        "CLAUDE.md still ≤60 lines",
        "plugin.json version = 2.0.0",
        "CHANGELOG v2.0.0 entry references both ADRs and the schema migration",
        "Repo-wide verification gates from spec §10 Phase 4 all pass"
      ],
      "out_of_scope": [],
      "dependencies": ["F001", "F002"],
      "technical_notes": "Plan: docs/plans/<TBD>-phase-3-and-4-docs-and-verify.md (authored after F002 completes)",
      "related_files": []
    }
  ],

  "constraints": {
    "implementation_order": "F001 → F002 → F003. F002 cannot start until F001 grep gate passes. F003 cannot start until F002 evals all pass.",
    "code_state_rule": "Each feature transitions proposed → building → done. The transition to done occurs only after the corresponding plan's verification step passes.",
    "scope_rule": "Out-of-scope items are tracked under their respective features; do not pull them forward.",
    "status_lifecycle": "proposed → building → done"
  }
}
```

- [ ] **Step 2: Validate JSON**

Run: `python3 -m json.tool features.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 3: Update F001 status to `building`**

Use Edit tool to change `"id": "F001"`'s `"status": "proposed"` to `"status": "building"` (because this Plan A is executing now — F001 is actively being built).

- [ ] **Step 4: Re-validate JSON**

Run: `python3 -m json.tool features.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add features.json
git commit -m "feat: add root features.json (dogfood superpowers integration project)"
```

---

## Task 0.8: Create `scripts/sync-superpowers.sh`

**Files:**
- Create: `scripts/sync-superpowers.sh`

- [ ] **Step 1: Write the script**

Create `scripts/sync-superpowers.sh` (executable):

```bash
#!/usr/bin/env bash
# scripts/sync-superpowers.sh
# Periodic reconciliation helper for vendored superpowers skills.
# Reads each skill's UPSTREAM.md, compares its recorded commit SHA against
# the currently installed superpowers cache, and emits a diff summary.
# Does NOT auto-apply changes. See docs/specs/2026-05-23-superpowers-integration-design.md §11.

set -euo pipefail

CACHE_BASE="${CACHE_BASE:-$HOME/.claude/plugins/cache/claude-plugins-official/superpowers}"
SKILLS_DIR="${SKILLS_DIR:-skills}"

# Locate latest installed superpowers version
if [[ ! -d "$CACHE_BASE" ]]; then
  echo "[sync-superpowers] superpowers cache not found at $CACHE_BASE" >&2
  exit 1
fi

LATEST_VERSION="$(ls -1 "$CACHE_BASE" | sort -V | tail -1)"
LATEST_PATH="$CACHE_BASE/$LATEST_VERSION/skills"

if [[ ! -d "$LATEST_PATH" ]]; then
  echo "[sync-superpowers] no skills found at $LATEST_PATH" >&2
  exit 1
fi

echo "Comparing vendored skills against superpowers $LATEST_VERSION"
echo "==============================================================="

found_any=0
for upstream_path in "$LATEST_PATH"/*/; do
  upstream_name="$(basename "$upstream_path")"
  vendored_path="$SKILLS_DIR/$upstream_name"

  if [[ ! -d "$vendored_path" ]]; then
    # Skip skills we deliberately do not vendor (e.g., using-superpowers)
    continue
  fi
  found_any=1

  upstream_skill_md="$upstream_path/SKILL.md"
  vendored_skill_md="$vendored_path/SKILL.md"

  if [[ ! -f "$upstream_skill_md" || ! -f "$vendored_skill_md" ]]; then
    echo "[$upstream_name] missing SKILL.md (upstream or vendored)"
    continue
  fi

  # Compare upstream SKILL.md to vendored SKILL.md (ignoring the two allowed edits)
  # The allowed edits: (1) name: line in frontmatter, (2) "harness local rules" pointer line
  # diff exits 1 when files differ (normal case) — absorb with || true so set -e doesn't kill us
  diff_lines="$( (diff <(grep -v -E '^name:|harness local rules' "$upstream_skill_md") \
                       <(grep -v -E '^name:|harness local rules' "$vendored_skill_md") \
               || true) | wc -l | tr -d ' ')"

  upstream_md="$vendored_path/UPSTREAM.md"
  if [[ -f "$upstream_md" ]]; then
    # grep exits 1 when no match (transitional state) — absorb with || true, default below
    last_synced="$(grep -E '^- \*\*Last synced:\*\*' "$upstream_md" | sed 's/^- \*\*Last synced:\*\* //' || true)"
    if [[ -z "$last_synced" ]]; then
      last_synced="(not recorded)"
    fi
  else
    last_synced="(UPSTREAM.md missing)"
  fi

  echo "[$upstream_name] diff-lines=$diff_lines  last-synced=$last_synced"
done

if [[ $found_any -eq 0 ]]; then
  echo "(no vendored skills found)"
fi

echo "==============================================================="
echo "Done. Review per-skill diffs manually before applying changes."
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x scripts/sync-superpowers.sh
```

- [ ] **Step 3: Smoke-test the script (will report empty since vendored skills not yet renamed)**

```bash
./scripts/sync-superpowers.sh
```

Expected: it runs without error, prints either per-skill rows or "(no vendored skills found)" since renames haven't happened yet.

- [ ] **Step 4: Commit**

```bash
git add scripts/sync-superpowers.sh
git commit -m "feat(scripts): add sync-superpowers.sh for upstream reconciliation"
```

---

## Task 1.1: Rename `skills/router/` → `skills/using-harness/`

**Files:**
- Move via git mv: `skills/router/` → `skills/using-harness/`
- Modify: `skills/using-harness/SKILL.md` (name field + content refresh)
- Modify: `skills/using-harness/evals/evals.json` (skill_name field)

**Note:** `using-harness` is harness-original, NOT vendored. It uses the **2-file structure** (`SKILL.md` + `evals/evals.json`), no `harness-delta.md` or `UPSTREAM.md`.

- [ ] **Step 1: git mv the directory**

```bash
git mv skills/router skills/using-harness
```

- [ ] **Step 2: Verify the move**

Run: `test -d skills/using-harness && test -f skills/using-harness/SKILL.md && test -f skills/using-harness/evals/evals.json && echo OK`
Expected: `OK`

- [ ] **Step 3: Update SKILL.md content**

Read `skills/using-harness/SKILL.md` (formerly `skills/router/SKILL.md`). Replace its full contents with:

```markdown
---
name: harness:using-harness
description: >
  Mandatory routing/meta skill for the harness-engineering plugin. Loads at every session start
  and enforces the "1% rule" — if there's even a 1% chance a harness skill applies, invoke it.
  Routes between 19 skills (13 vendored from superpowers v5.1.0 + 6 harness-original).
---

# harness:using-harness — Harness Engineering Meta Skill

> This skill is loaded at the start of every session to ensure harness-engineering capabilities
> are properly activated. Inspired by the `using-superpowers` forced-trigger pattern from
> `obra/superpowers`, but with the harness skill catalog and mandatory invocation table.

## Core Rule: Mandatory Skill Invocation

If there is even a 1% chance one of the skills below applies, **you must invoke it** — you have no discretion.

## Skill catalog

### Vendored from superpowers v5.1.0 (13)
| Trigger | Skill |
|---|---|
| Planning a multi-step task before touching code | `harness:writing-plans` |
| Implementing a feature or fixing a bug | `harness:test-driven-development` |
| About to claim work is complete | `harness:verification-before-completion` |
| Any creative/design task (new feature, modify behavior) | `harness:brainstorming` |
| Executing a written plan task-by-task | `harness:executing-plans` |
| Executing a plan via fresh subagent per task | `harness:subagent-driven-development` |
| 2+ independent parallel tasks | `harness:dispatching-parallel-agents` |
| Need an isolated workspace | `harness:using-git-worktrees` |
| Any bug, test failure, or unexpected behavior | `harness:systematic-debugging` |
| Receiving code review feedback | `harness:receiving-code-review` |
| Asking for code review | `harness:requesting-code-review` |
| Implementation complete; integrating the work | `harness:finishing-a-development-branch` |
| Creating or editing a skill | `harness:writing-skills` |

### Harness-original (6)
| Trigger | Skill |
|---|---|
| (this skill itself) | `harness:using-harness` |
| Task completion / archiving | `harness:archive` |
| Health check on existing project Harness setup | `harness:audit` |
| Pre-production deploy planning | `harness:canary` |
| Garbage collection / drift cleanup | `harness:evolve` |
| New project initialization | `harness:init` |

## Hard rules
- Invoke the relevant skill **before** any response or action (including clarifying questions).
- Never rationalize skipping a skill ("this is simple", "I remember this", "the skill is overkill").
- When the user explicitly types `/<skill>`, invoke it immediately.

## Cross-skill handoffs
- `harness:brainstorming` → must hand off to `harness:writing-plans` (terminal state for brainstorming).
- `harness:writing-plans` → hands off to `harness:executing-plans` or `harness:subagent-driven-development`.
- `harness:verification-before-completion` → triggers `harness:finishing-a-development-branch` → which must call `harness:archive`.
```

- [ ] **Step 4: Update `skills/using-harness/evals/evals.json`**

Read it, then update the top-level `"skill_name"` field. Use Edit with `old_string`:
```
  "skill_name": "harness:router",
```
And `new_string`:
```
  "skill_name": "harness:using-harness",
```

- [ ] **Step 5: Validate evals JSON**

Run: `python3 -m json.tool skills/using-harness/evals/evals.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 6: Verify the 2-file structure (no harness-delta.md or UPSTREAM.md)**

Run: `ls skills/using-harness/ | sort`
Expected exactly: `SKILL.md` and `evals` (a directory)

- [ ] **Step 7: Commit**

```bash
git add skills/using-harness/
git commit -m "refactor(skills): rename router to using-harness; update catalog for 19-skill topology"
```

---

## Task 1.2: Rename `skills/plan/` → `skills/writing-plans/` (vendor structure)

**Files:**
- Move via git mv: `skills/plan/` → `skills/writing-plans/`
- Replace: `skills/writing-plans/SKILL.md` (upstream content + 2 allowed edits)
- Create: `skills/writing-plans/harness-delta.md`
- Create: `skills/writing-plans/UPSTREAM.md`
- Create: `skills/writing-plans/evals/evals.json` (fresh — no existing evals to port)

- [ ] **Step 1: git mv the directory**

```bash
git mv skills/plan skills/writing-plans
```

- [ ] **Step 2: Replace SKILL.md with upstream content + 2 edits**

Copy upstream content:

```bash
UPSTREAM=~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-plans/SKILL.md
cp "$UPSTREAM" skills/writing-plans/SKILL.md
```

Then apply the 2 allowed edits using Edit tool:

**Edit 1 (frontmatter `name:`):**
Read the file, find the `name:` line in frontmatter (will be `name: writing-plans`), change to:
```
name: harness:writing-plans
```

**Edit 2 (pointer line):**
Use Edit with `old_string`:
```
---

# Writing Plans
```
And `new_string`:
```
---

> **harness local rules:** Always read [harness-delta.md](./harness-delta.md) before invoking this skill. It defines mandatory integrations with features.json, ADR, and docs.

# Writing Plans
```

(If the heading isn't exactly `# Writing Plans`, adjust to match the upstream H1; the goal is to insert the pointer line between the frontmatter `---` and the first H1.)

- [ ] **Step 3: Create harness-delta.md**

Create `skills/writing-plans/harness-delta.md`:

```markdown
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
```

- [ ] **Step 4: Create UPSTREAM.md**

Create `skills/writing-plans/UPSTREAM.md`:

```markdown
# Upstream provenance: writing-plans

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:writing-plans` (was `writing-plans`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

The directory `skills/writing-plans/evals/` may or may not exist (the old `skills/plan/` did NOT have evals). Create it:

```bash
mkdir -p skills/writing-plans/evals
```

Then create `skills/writing-plans/evals/evals.json`:

```json
{
  "skill_name": "harness:writing-plans",
  "evals": [
    {
      "id": 1,
      "eval_name": "features-json-rigid-coverage",
      "type": "behavior",
      "rule_under_test": "Plan output must reference every acceptance_criterion of the in-progress feature",
      "prompt": "Read features.json. The feature 'add-pagination' is status=proposed with acceptance_criteria: ['paginate API at 50 per page', 'preserve sort order', 'expose total count header']. Write an implementation plan.",
      "expected_output": "Plan tasks collectively cover all three criteria; no criterion is orphaned. The plan does not include tasks unrelated to these three criteria.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "every criterion has at least one task",
          "check": "Each of the three acceptance_criteria strings appears (verbatim or paraphrased) in at least one task's description or test step."
        },
        {
          "name": "no orphan tasks",
          "check": "Every task in the plan can be tied back to at least one of the three criteria."
        },
        {
          "name": "spec linkage stated",
          "check": "Plan header references the source spec or feature key."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "out-of-scope-not-touched",
      "type": "pressure",
      "rule_under_test": "Plan must not include tasks for items declared out_of_scope in features.json",
      "prompt": "features.json has feature 'add-pagination' with out_of_scope: ['cursor-based pagination']. User says: 'and while you're at it, support cursor pagination too — should be easy'. Write the plan.",
      "expected_output": "Plan respects out_of_scope: no cursor pagination tasks. Skill pushes back, citing features.json.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "no cursor pagination tasks",
          "check": "Plan contains zero tasks implementing cursor-based pagination."
        },
        {
          "name": "explicit push-back",
          "check": "Plan or accompanying message explicitly references features.json out_of_scope and asks the user to update features.json first if scope must change."
        }
      ]
    },
    {
      "id": 3,
      "eval_name": "adr-trigger-on-architectural-decision",
      "type": "behavior",
      "rule_under_test": "When planning surfaces an architectural decision, produce an ADR draft before finalizing the plan",
      "prompt": "Plan a new feature 'background job queue'. The spec doesn't specify whether to use SQS, Redis Streams, or a custom in-process queue.",
      "expected_output": "Skill pauses planning, drafts an ADR proposing the queue choice (under docs/decisions/), presents trade-offs, and only then finalizes the plan referencing the ADR.",
      "files": [],
      "assertions": [
        {
          "name": "ADR draft produced",
          "check": "Output includes a draft ADR file path under docs/decisions/ with the standard ADR structure (Context / Decision / Consequences)."
        },
        {
          "name": "plan references the ADR",
          "check": "The plan body references the ADR by number."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate evals JSON**

Run: `python3 -m json.tool skills/writing-plans/evals/evals.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 7: Verify the 4-file structure**

Run: `ls skills/writing-plans/ | sort`
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`

- [ ] **Step 8: Commit**

```bash
git add skills/writing-plans/
git commit -m "refactor(skills): rename plan to writing-plans; vendor v5.1.0 + sidecar"
```

---

## Task 1.3: Rename `skills/tdd/` → `skills/test-driven-development/` (vendor structure)

**Files:**
- Move via git mv: `skills/tdd/` → `skills/test-driven-development/`
- Replace: `skills/test-driven-development/SKILL.md`
- Create: `skills/test-driven-development/harness-delta.md`
- Create: `skills/test-driven-development/UPSTREAM.md`
- Create: `skills/test-driven-development/evals/evals.json` (fresh)

- [ ] **Step 1: git mv**

```bash
git mv skills/tdd skills/test-driven-development
```

- [ ] **Step 2: Replace SKILL.md with upstream + 2 edits**

```bash
UPSTREAM=~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/test-driven-development/SKILL.md
cp "$UPSTREAM" skills/test-driven-development/SKILL.md
```

Edit frontmatter `name:` to `harness:test-driven-development`.

Edit to insert the pointer line between the frontmatter `---` and the first H1, same pattern as Task 1.2 Step 2.

- [ ] **Step 3: Create harness-delta.md**

Create `skills/test-driven-development/harness-delta.md`:

```markdown
# harness-delta: test-driven-development

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Locate the current in-progress feature (status=`building`) in `features.json`. Use its `acceptance_criteria` array as the **test input source**:
- Each criterion should map to at least one test case.
- Test names should reference the criterion (e.g., `test_pagination_at_50_per_page` for criterion "paginate API at 50 per page").

### features.json writes
None. This skill does not modify features.json.

### ADR
None directly.

### Binding to using-harness 1% rule
This skill is one of the mandatory invocation targets in `harness:using-harness`. Any user message that suggests writing code, fixing bugs, or implementing features triggers it.

## Soft hints
- Prefer integration tests over unit tests when integration coverage is unclear; ADR-0004's "integration-first" stance applies.

## Stop Hook contract
The session's Stop hook blocks "claim done without tests" (existing infrastructure). This skill plus that hook close the loop.

## Verification (covered by evals)
- with-skill: when features.json has a `building` feature, the first test written cites the specific `acceptance_criterion` by content.
- baseline: without the skill, tests may be written but won't trace to the criteria.
```

- [ ] **Step 4: Create UPSTREAM.md**

Same template as Task 1.2 Step 4, substituting skill name:

```markdown
# Upstream provenance: test-driven-development

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>

- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:test-driven-development`
- Pointer line to `harness-delta.md` after frontmatter

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```bash
mkdir -p skills/test-driven-development/evals
```

Then write `skills/test-driven-development/evals/evals.json`:

```json
{
  "skill_name": "harness:test-driven-development",
  "evals": [
    {
      "id": 1,
      "eval_name": "tests-map-to-acceptance-criteria",
      "type": "behavior",
      "rule_under_test": "Each test case must trace to at least one acceptance_criterion of the current feature",
      "prompt": "features.json shows feature 'rate-limit-api' status=building with acceptance_criteria: ['rejects 6th request in same second', 'returns 429 status', 'sets Retry-After header']. Write tests for this feature.",
      "expected_output": "Three or more tests, each named to reflect one of the three criteria; the test names and assertions visibly correspond to the criteria.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "test count >= criterion count",
          "check": "At least one test per acceptance_criterion."
        },
        {
          "name": "test names reference criteria",
          "check": "Each test name or docstring references the corresponding criterion text."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "no-implementation-before-test",
      "type": "pressure",
      "rule_under_test": "Skill must enforce write-failing-test-first, regardless of user pressure",
      "prompt": "I already know how to implement this rate limiter. Just write the implementation, I'll add tests later. Be efficient.",
      "expected_output": "Skill refuses to skip the test-first step and explains why (TDD discipline is rigid, not flexible).",
      "files": [],
      "assertions": [
        {
          "name": "refuses to skip",
          "check": "Output does not produce implementation code without first producing failing tests."
        },
        {
          "name": "cites rigidity",
          "check": "Output explicitly references the test-first discipline being non-negotiable."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON**

Run: `python3 -m json.tool skills/test-driven-development/evals/evals.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 7: Verify 4-file structure**

Run: `ls skills/test-driven-development/ | sort`
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`

- [ ] **Step 8: Commit**

```bash
git add skills/test-driven-development/
git commit -m "refactor(skills): rename tdd to test-driven-development; vendor v5.1.0 + sidecar"
```

---

## Task 1.4: Rename `skills/verify/` → `skills/verification-before-completion/` (vendor structure)

**Files:**
- Move via git mv: `skills/verify/` → `skills/verification-before-completion/`
- Replace: `skills/verification-before-completion/SKILL.md`
- Create: `skills/verification-before-completion/harness-delta.md`
- Create: `skills/verification-before-completion/UPSTREAM.md`
- Create: `skills/verification-before-completion/evals/evals.json` (fresh)

- [ ] **Step 1: git mv**

```bash
git mv skills/verify skills/verification-before-completion
```

- [ ] **Step 2: Replace SKILL.md with upstream + 2 edits**

```bash
UPSTREAM=~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/verification-before-completion/SKILL.md
cp "$UPSTREAM" skills/verification-before-completion/SKILL.md
```

Apply the 2 edits as in Task 1.2 Step 2.

- [ ] **Step 3: Create harness-delta.md**

Create `skills/verification-before-completion/harness-delta.md`:

```markdown
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
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: verification-before-completion

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>

- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:verification-before-completion`
- Pointer line to `harness-delta.md` after frontmatter

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```bash
mkdir -p skills/verification-before-completion/evals
```

Then `skills/verification-before-completion/evals/evals.json`:

```json
{
  "skill_name": "harness:verification-before-completion",
  "evals": [
    {
      "id": 1,
      "eval_name": "block-on-unsatisfied-criterion",
      "type": "behavior",
      "rule_under_test": "Skill must block 'verified' if any acceptance_criterion is unsatisfied",
      "prompt": "features.json has feature 'rate-limit-api' status=building with acceptance_criteria: ['rejects 6th request', 'returns 429', 'sets Retry-After']. Tests show 2 criteria passing, 1 failing (Retry-After header missing). User asks: 'verify this is done'.",
      "expected_output": "Skill reports: NOT verified. The 'Retry-After header' criterion is unsatisfied. Lists the specific gap. Does NOT trigger finishing-a-development-branch.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "blocks verification",
          "check": "Output explicitly states verification did not pass."
        },
        {
          "name": "names the specific gap",
          "check": "Output cites 'Retry-After header' as the failing criterion."
        },
        {
          "name": "does not advance status",
          "check": "Output does not call finishing-a-development-branch and does not transition status to done."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "architecture-layer-violation-detection",
      "type": "behavior",
      "rule_under_test": "Skill must flag reverse-direction layer dependencies",
      "prompt": "A new commit imports from `commands/audit.md` content inside `skills/audit/SKILL.md`. The dependency direction in this project is references → templates → skills → commands; commands may depend on skills, not vice versa. Run verification.",
      "expected_output": "Skill flags the violation: skills/audit/SKILL.md depending on commands/audit.md reverses the layer order. Verification does not pass.",
      "files": [],
      "assertions": [
        {
          "name": "violation detected",
          "check": "Output identifies the reverse-direction dependency by file path."
        },
        {
          "name": "blocks completion",
          "check": "Output does not allow status transition to done."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON**

Run: `python3 -m json.tool skills/verification-before-completion/evals/evals.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 7: Verify 4-file structure**

Run: `ls skills/verification-before-completion/ | sort`
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`

- [ ] **Step 8: Commit**

```bash
git add skills/verification-before-completion/
git commit -m "refactor(skills): rename verify to verification-before-completion; vendor v5.1.0 + sidecar"
```

---

## Task 1.5: Repo-wide grep gate

**Goal:** Ensure no stray references to old short names (`harness:plan`, `harness:tdd`, `harness:verify`, `harness:router`) remain in code/docs/templates. References inside `CHANGELOG.md` (historical record) and `docs/specs/*.md` (the integration spec itself documents old names) are allowed.

- [ ] **Step 1: Run the grep**

```bash
grep -rE 'harness:(plan|tdd|verify|router)\b' . \
  --include='*.md' \
  --include='*.json' \
  --include='*.sh' \
  --include='*.py' \
  --exclude-dir=.git \
  --exclude=CHANGELOG.md \
  --exclude-dir=ziLgb4r4 \
  | grep -v 'docs/specs/'
```

Expected: zero output. If non-zero output, each line is a stray reference that must be updated.

- [ ] **Step 2: Fix any stray references**

For each line returned above:
1. Read the file
2. Replace the old short name with the new full name:
   - `harness:plan` → `harness:writing-plans`
   - `harness:tdd` → `harness:test-driven-development`
   - `harness:verify` → `harness:verification-before-completion`
   - `harness:router` → `harness:using-harness`
3. Commit each fix with message `fix(refs): update stray <old> → <new> reference in <file>`

- [ ] **Step 3: Re-run the grep**

```bash
grep -rE 'harness:(plan|tdd|verify|router)\b' . \
  --include='*.md' \
  --include='*.json' \
  --include='*.sh' \
  --include='*.py' \
  --exclude-dir=.git \
  --exclude=CHANGELOG.md \
  --exclude-dir=ziLgb4r4 \
  | grep -v 'docs/specs/'
```

Expected: zero output.

- [ ] **Step 4: Transition F001 status to `done` in `features.json`**

Open root `features.json`. Change F001's `"status": "building"` to `"status": "done"`.

Run: `python3 -m json.tool features.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 5: Commit the status transition**

```bash
git add features.json
git commit -m "chore(features): F001 superpowers-vendor-foundation done"
```

---

## Spec coverage review (Plan A only)

This plan implements the following spec sections:

| Spec section | Where in this plan |
|---|---|
| §4 D1 (full alignment + vendor) | Tasks 1.2–1.4 rename to upstream names |
| §4 D2 (vendor pattern, no plugin dep) | Tasks 1.2–1.4 copy upstream content into our tree |
| §4 D3 (4-file sidecar) | Tasks 1.2–1.4 produce SKILL/harness-delta/UPSTREAM/evals; Task 1.1 uses 2-file structure (exception per D8) |
| §4 D4 (ADR-0004 evals) | Tasks 1.1 Step 4, 1.2 Step 5, 1.3 Step 5, 1.4 Step 5 |
| §4 D6 (spec field) | Task 0.4 adds optional `spec:` field |
| §4 D7 (3-state status) | Task 0.4 migrates enum |
| §4 D8 (using-harness name) | Task 1.1 |
| §4 D10 (sync workflow) | Task 0.8 |
| §4 D12 (CLAUDE.md ≤60 lines) | Deferred to Plan C |
| §4 D13 (root features.json) | Task 0.7 |
| §4 D14 (v2.0.0 version bump) | Deferred to Plan C |
| §10 Phase 0 | Tasks 0.1–0.8 |
| §10 Phase 1 | Tasks 1.1–1.5 |
| §10 Phase 2 (10 new vendored) | Deferred to **Plan B** (separate plan, authored after this one) |
| §10 Phase 3/4 | Deferred to **Plan C** |
| §16 ADRs | Tasks 0.1, 0.2 |

Items deferred to Plan B and Plan C are intentional — they belong to F002 and F003 respectively (see root `features.json` dependencies).

---

## Self-review checklist (executed before plan publishes)

- [x] **Spec coverage:** every locked decision (D1–D14) either has a Plan A task or is explicitly deferred to Plan B/C
- [x] **Placeholder scan:** no `TBD`, `TODO`, "fill in later"; the commit SHA placeholder in UPSTREAM.md files is intentional — Step 1 of each task instructs how to record it
- [x] **Type consistency:** skill names use `harness:<full-upstream-name>` consistently in all SKILL.md frontmatter, evals.json `skill_name`, and cross-references
- [x] **Schema consistency:** `status` enum is `proposed/building/done` everywhere; `spec:` field added to template and root features.json
- [x] **Grep gate:** Task 1.5 explicitly enforces zero stray old-name references

---

## Execution handoff

**Plan complete and saved to `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md`.**

Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Best for plans this size (~13 tasks, ~70 substeps).

2. **Inline Execution** — Execute tasks in this session using `executing-plans`, batch with checkpoints. Larger context cost but you see each step.

After Plan A executes and F001 transitions to `done`, the next session should invoke `harness:writing-plans` again to author Plan B (Phase 2, 10 new vendored skills).

**Which approach?**
