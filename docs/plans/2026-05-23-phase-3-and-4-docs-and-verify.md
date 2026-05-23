# Plan C — Phase 3 (Docs Refresh & Release) + Phase 4 (Verification) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh documentation to the 19-skill topology, restructure `commands/review-pr.md` as a wrapper, bump version to 2.0.0 with CHANGELOG, migrate the legacy codebuddy spec, then run full Phase 4 verification gates and transition F003 to `done`.

**Architecture:** Phase 3 is a sequence of surgical edits to top-level docs + the release artifacts (plugin.json, CHANGELOG.md). Phase 4 is a battery of read-only verification checks plus the final status transitions for F003 and the design spec. No new code or skills are introduced.

**Tech Stack:** Markdown for docs, JSON for plugin.json, git for the file move and version-bump commits, bash for verification grep/JSON checks.

**Source spec:** `docs/specs/2026-05-23-superpowers-integration-design.md`
**Predecessor plans:**
- Plan A — `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` (F001, merged at 5c76cbb)
- Plan B — `docs/plans/2026-05-23-phase-2-vendor-new-skills.md` (F002, merged at 4a8f8cb)

**Pre-existing state (verified at plan-writing time):**
- 18 of 19 skills present under `skills/` — all 13 vendored (Plan A 3 + Plan B 10) + 5 harness-original + `using-harness` = 19. (No new skill files are added in Plan C.)
- `using-harness/SKILL.md` already lists all 19 skills in its catalog (forward-looking when Plan A landed it).
- `features.json`: F001=done, F002=done, F003=proposed. Spec front-matter status=building.
- `docs/architecture.md` (83 lines) still references only the 3-Skill / 5-original era — needs major refresh.
- `README.md` Core Skills table already mentions 9 of the 19 skills (4 renamed forks + 5 originals), but is missing all 10 from Plan B and badge is at v1.10.1 (stale by two versions).
- `CLAUDE.md` is 41 lines — has ample headroom under the ≤60 line constraint.
- `commands/review-pr.md` is currently a 15-line standalone instruction, overlaps with the new `harness:requesting-code-review` + `harness:receiving-code-review` skills (per spec §12).
- `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` still exists in the old (pre-v2.0.0) location.
- `plugin.json` version is `1.11.0`.

---

## Task 3.0: Transition F003 status to `building` (pre-flight)

**Files:**
- Modify: `features.json` (F003 status: proposed → building, technical_notes filename)

- [ ] **Step 1: Update F003 status**

Use Edit with `old_string`:
```
      "id": "F003",
      "name": "superpowers-docs-refresh",
      "priority": 3,
      "status": "proposed",
```
And `new_string`:
```
      "id": "F003",
      "name": "superpowers-docs-refresh",
      "priority": 3,
      "status": "building",
```

- [ ] **Step 2: Replace technical_notes placeholder with the real plan filename**

Use Edit with `old_string`:
```
      "technical_notes": "Plan: docs/plans/<TBD>-phase-3-and-4-docs-and-verify.md (authored after F002 completes)",
```
And `new_string`:
```
      "technical_notes": "Plan: docs/plans/2026-05-23-phase-3-and-4-docs-and-verify.md",
```

- [ ] **Step 3: Validate JSON**

Run: `python3 -m json.tool features.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add features.json
git commit -m "chore(features): transition F003 to building"
```

---

## Task 3.1: Refresh `docs/architecture.md` to 19-skill topology

**Files:**
- Modify: `docs/architecture.md`

The current architecture.md (83 lines) is stuck at the v1.x era. This task replaces it with a v2.0 version that documents the 19-skill topology, the 4-file vendored anatomy, and the relationship between commands and skills.

- [ ] **Step 1: Replace the file content**

Read the existing file first. Then replace its full contents with:

````markdown
# Harness Engineering Plugin — Architecture Diagram

## System Overview

This is an AI Agent Harness plugin that targets Claude Code and provides engineering teams with standardized AI Agent Harness engineering capabilities. As of v2.0.0 it consists of 19 skills under the `harness:` namespace (6 harness-original + 13 vendored from `obra/superpowers` v5.1.0), plus a set of supporting Commands, Hooks, and References.

## Directory Structure

```
harness-engineering-plugin/
├── CLAUDE.md                       ← Project memory file (≤ 60 lines, single source of truth)
├── features.json                   ← Root features.json (dogfood; tracks plugin's own work per ADR-0003)
├── .claude-plugin/
│   └── plugin.json                 ← Claude Code plugin manifest
├── skills/
│   ├── # harness-original (6) — 2-file structure (SKILL.md + evals/evals.json)
│   ├── using-harness/              ← Routing/meta skill (mandatory invocation table for all 19 skills)
│   ├── archive/                    ← Completion archiving and documentation sync
│   ├── audit/                      ← Existing project health check and optimization
│   ├── canary/                     ← Pre-deployment canary planning
│   ├── evolve/                     ← Continuous iterative improvement
│   ├── init/                       ← New project Harness initialization
│   ├── # vendored from superpowers v5.1.0 (13) — 4-file structure
│   ├── brainstorming/              ← Spec authoring (writes to docs/specs/, gated by features.json)
│   ├── dispatching-parallel-agents/← Parallel work dispatch
│   ├── executing-plans/            ← Plan execution (reads from docs/plans/)
│   ├── finishing-a-development-branch/ ← Merge/PR finalization (owns building → done transition)
│   ├── receiving-code-review/      ← Code review reception
│   ├── requesting-code-review/     ← Code review dispatch (PR creation)
│   ├── subagent-driven-development/← Subagent-per-task workflow
│   ├── systematic-debugging/       ← Bug investigation (writes to docs/incidents/)
│   ├── test-driven-development/    ← TDD workflow
│   ├── using-git-worktrees/        ← Worktree-based isolation
│   ├── verification-before-completion/ ← 4-layer completion check
│   ├── writing-plans/              ← Plan authoring (writes to docs/plans/)
│   └── writing-skills/             ← Skill authoring (enforces ADR-0004 + ADR-0009)
├── commands/                       ← Slash commands
│   ├── assign.md                   ← /harness:assign (team feature assignment)
│   ├── audit.md, canary.md, init.md ← Entry points for the matching harness:<name> skills
│   ├── dump.md                     ← /harness:dump (context dump utility)
│   ├── review-pr.md                ← Thin wrapper over harness:requesting-code-review + receiving-code-review
│   ├── scan-arch.md, sync-docs.md  ← Sub-steps invoked by harness:archive
│   ├── scan-entropy.md, trim.md    ← Sub-steps invoked by harness:evolve
├── hooks/                          ← Hook template scripts (silent on success)
│   ├── stop-typecheck.sh, pre-protect-env.sh, post-format.sh
│   ├── stop-commit-progress.sh, post-observe.sh, session-start.sh
├── docs/
│   ├── architecture.md             ← This file
│   ├── decisions/                  ← ADR (Architecture Decision Records)
│   │   ├── 0001 .. 0007 (existing)
│   │   ├── 0008-vendor-superpowers-v5.md       ← v2.0.0: vendor strategy
│   │   └── 0009-harness-delta-sidecar.md       ← v2.0.0: 4-file sidecar convention
│   ├── design/                     ← Design notes
│   ├── plans/                      ← Implementation plans (output of harness:writing-plans)
│   ├── specs/                      ← Design specs (output of harness:brainstorming)
│   ├── incidents/                  ← Debug notes (output of harness:systematic-debugging)
│   └── templates/                  ← Multi-language project templates (typescript / python / go / generic)
├── references/                     ← Reference documents (loaded on demand)
├── scripts/
│   ├── self-test.sh, health-score.py, generate-harness.sh
│   └── sync-superpowers.sh         ← v2.0.0: upstream reconciliation helper (read-only diff report)
└── evals/                          ← Project-level evals (top-level evals.json is the registry)
```

## Vendored skill anatomy (4-file structure per ADR-0009)

Each of the 13 vendored skills contains exactly:

```
skills/<name>/
├── SKILL.md            # superpowers v5.1.0 content verbatim, only 2 allowed edits applied:
│                       #   1. frontmatter `name:` → `harness:<name>`
│                       #   2. pointer line inserted: "> harness local rules: read harness-delta.md"
├── harness-delta.md    # local rules (features.json / ADR / docs / Stop Hook integrations)
├── UPSTREAM.md         # provenance (source SHA, fork date, last-sync date, intentional divergences)
└── evals/evals.json    # ADR-0004 evals validating harness-delta behavior
```

The 6 harness-original skills (`using-harness`, `archive`, `audit`, `canary`, `evolve`, `init`) use a 2-file structure (`SKILL.md` + `evals/evals.json`) — no `harness-delta.md` or `UPSTREAM.md` since there is no upstream to track.

## Skill triggers (abbreviated — see using-harness/SKILL.md for the full mandatory invocation table)

| Trigger | Skill |
|---|---|
| Session start (loaded automatically) | `harness:using-harness` |
| New project Harness setup | `harness:init` |
| Existing project audit | `harness:audit` |
| Pre-deployment planning | `harness:canary` |
| Drift cleanup / "CLAUDE.md too long" | `harness:evolve` |
| Task completion / archive | `harness:archive` |
| Any creative/design task | `harness:brainstorming` |
| Multi-step task before code | `harness:writing-plans` |
| Implementing / fixing bugs | `harness:test-driven-development` |
| Before claiming done | `harness:verification-before-completion` |
| Bug / unexpected behavior | `harness:systematic-debugging` |
| Parallel independent tasks | `harness:dispatching-parallel-agents` |
| Subagent-per-task execution | `harness:subagent-driven-development` |
| Plan execution | `harness:executing-plans` |
| Need isolated workspace | `harness:using-git-worktrees` |
| Asking for code review | `harness:requesting-code-review` |
| Receiving code review | `harness:receiving-code-review` |
| Implementation done; integration | `harness:finishing-a-development-branch` |
| Creating or editing a skill | `harness:writing-skills` |

## Commands → Skills relationship

| Command | Relationship to skills |
|---|---|
| `audit.md`, `canary.md`, `init.md` | Entry point for the matching `harness:<name>` skill |
| `review-pr.md` | Thin wrapper that invokes `harness:requesting-code-review` + `harness:receiving-code-review` |
| `scan-arch.md`, `sync-docs.md` | Sub-steps used inside `harness:archive` |
| `scan-entropy.md`, `trim.md` | Sub-steps used inside `harness:evolve` |
| `assign.md`, `dump.md` | Independent utility commands (no 1:1 skill mapping) |

## Layer Dependency Rules

Allowed dependency direction (references may only flow to the right):

```
references → templates → skills → commands
```

Prohibited:
- Commands must not directly reference references (must go through skills)
- Templates must not reference skills (templates are static resources consumed by skills)
- Hooks are standalone deterministic scripts with no dependency on skills or commands

## Upstream sync workflow

`scripts/sync-superpowers.sh` compares each vendored skill's `UPSTREAM.md` SHA against the currently installed superpowers cache and emits a per-skill diff summary. The script is read-only; it never auto-applies changes. Reconciliation cadence is once per superpowers minor release; each diff is reviewed individually per ADR-0009.
````

- [ ] **Step 2: Verify EOF newline + line count**

```bash
tail -c 1 docs/architecture.md | xxd | head -1
wc -l docs/architecture.md
```
Expected: last byte `0a`. Line count somewhere between 100 and 140 (the new content is larger than the old 83 lines).

- [ ] **Step 3: Commit**

```bash
git add docs/architecture.md
git commit -m "docs(architecture): refresh to 19-skill topology + ADR-0008/0009 conventions"
```

---

## Task 3.2: Update `README.md` Core Skills table + version badge

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Bump version badge**

The badge currently reads `version-v1.10.1-blue`. Use Edit with `old_string`:
```
[![Version](https://img.shields.io/badge/version-v1.10.1-blue)](CHANGELOG.md)
```
And `new_string`:
```
[![Version](https://img.shields.io/badge/version-v2.0.0-blue)](CHANGELOG.md)
```

- [ ] **Step 2: Expand the Core Skills table**

The current `## Core Skills` section has a table that lists 9 skills. Read README.md to find the exact lines. The table currently ends at a row for `harness:verification-before-completion`. Append 10 new rows for the Plan B vendored skills, immediately after that last existing row.

Use Edit with `old_string` set to the existing last row + the trailing blank line + the `---` separator that follows the table. For example, the `old_string` will look something like:

```
| **harness:verification-before-completion** | Before declaring a task complete | 4-layer check (Functional / Quality / Architecture / Integration) |

---
```

And `new_string`:

```
| **harness:verification-before-completion** | Before declaring a task complete | 4-layer check (Functional / Quality / Architecture / Integration) |
| **harness:brainstorming** | New feature / design task | Turns ideas into specs at `docs/specs/`, gates handoff to writing-plans by features.json/ADR linkage |
| **harness:executing-plans** | Plan ready to run | Executes a plan from `docs/plans/` task-by-task, blocks on out-of-scope work |
| **harness:subagent-driven-development** | Plan has independent tasks | Dispatches fresh subagent per task with two-stage review |
| **harness:dispatching-parallel-agents** | 2+ independent parallel tasks | Parallel dispatch respecting layer dependencies + features.json grounding |
| **harness:using-git-worktrees** | Need isolated workspace | Sets up worktree with `feature/<features.json-id>` naming convention |
| **harness:systematic-debugging** | Bug / unexpected behavior | Writes notes to `docs/incidents/`, checks ADR invalidation, prompts canary for prod incidents |
| **harness:receiving-code-review** | Got review feedback | Reconciles rigid-constraint feedback with features.json; arch feedback → ADR |
| **harness:requesting-code-review** | Ready to request review | Pre-review checklist gate (rigid constraints satisfied); PR body includes `feature: <id>` |
| **harness:finishing-a-development-branch** | Implementation complete | Owns `building → done` transition; mandatory `harness:archive` call; canary prompt for deploy-touching changes |
| **harness:writing-skills** | Authoring/editing skills | Enforces ADR-0004 (evals) + ADR-0009 (4-file vs 2-file structure) |

---
```

If the exact trailing separator doesn't match (e.g., different blank-line count), Read the file first, then construct `old_string` based on what's actually there. The key invariant: the 10 new rows must be appended to the existing table, before the `---` that ends the Core Skills section.

- [ ] **Step 3: Verify EOF newline + the badge updated**

```bash
tail -c 1 README.md | xxd | head -1
grep 'version-v2.0.0' README.md
grep -c '^\| \*\*harness:' README.md
```
Expected: last byte `0a`. Badge line shows v2.0.0. The skill-row count is now 19 (or 18 if `harness:using-harness` is documented differently — re-read README if count looks off).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs(readme): bump version badge to v2.0.0 + add 10 vendored skills to Core Skills"
```

---

## Task 3.3: Update `README.zh-CN.md` Core Skills table + version badge

**Files:**
- Modify: `README.zh-CN.md`

Mirror of Task 3.2 in Chinese.

- [ ] **Step 1: Bump version badge**

Same pattern as Task 3.2 Step 1, but in `README.zh-CN.md`. Old version badge → `v2.0.0`.

- [ ] **Step 2: Expand the Chinese Core Skills table**

Read `README.zh-CN.md` to find the `## 核心 Skills`（或类似中文标题）table. Append 10 rows in Chinese:

```
| **harness:brainstorming** | 新功能 / 设计任务 | 把想法落到 `docs/specs/` 的设计 spec，按 features.json/ADR 关联门禁后再交给 writing-plans |
| **harness:executing-plans** | plan 已写、准备执行 | 从 `docs/plans/` 读 plan 一任务一任务执行，遇到 out_of_scope 阻塞 |
| **harness:subagent-driven-development** | 计划含独立任务 | 每任务派发新 subagent，两阶段 review |
| **harness:dispatching-parallel-agents** | 2+ 个独立并行任务 | 并行派发时尊重架构层依赖 + features.json 归属 |
| **harness:using-git-worktrees** | 需要隔离工作区 | 按 `feature/<features.json-id>` 命名约定创建 worktree |
| **harness:systematic-debugging** | 出现 bug / 异常行为 | 调试笔记落 `docs/incidents/`，检查 ADR 假设是否被破坏，生产事故提示 canary |
| **harness:receiving-code-review** | 收到 review 反馈 | 涉及 rigid 约束的反馈与 features.json 对账；架构反馈 → ADR |
| **harness:requesting-code-review** | 准备请评审 | 评审前自检（rigid 约束已满足）；PR 描述含 `feature: <id>` |
| **harness:finishing-a-development-branch** | 实现完成 | 拥有 `building → done` 状态转换；强制调 `harness:archive`；触碰部署面则提示 canary |
| **harness:writing-skills** | 写/改 skill | 强制 ADR-0004（evals）+ ADR-0009（4 文件 vs 2 文件结构） |
```

Insert these rows immediately after the existing last `| **harness:verification-before-completion** | ... |` row, before the trailing `---` separator.

- [ ] **Step 3: Verify EOF newline + skill-row count**

```bash
tail -c 1 README.zh-CN.md | xxd | head -1
grep -c '^\| \*\*harness:' README.zh-CN.md
```

- [ ] **Step 4: Commit**

```bash
git add README.zh-CN.md
git commit -m "docs(readme-zh): bump version badge to v2.0.0 + add 10 vendored skills (Chinese)"
```

---

## Task 3.4: Update `CLAUDE.md` (2 new prohibited rules + 1 ADR pointer)

**Files:**
- Modify: `CLAUDE.md`

Per spec §13 the CLAUDE.md additions are minimal: 2 lines under "Prohibited Practices" and 1 line under "Further Context" pointing to the new ADRs. The hard ≤60-line constraint must hold (currently 41 lines; this task adds 3; final 44).

- [ ] **Step 1: Add 2 prohibited rules**

Use Edit with `old_string`:
```
## Prohibited Practices
- Never hardcode specific project names or team information in templates
- Never generate a CLAUDE.md template exceeding 60 lines
- Never let Hook templates produce output on success
- Never exceed 500 lines in a single Skill file
```
And `new_string`:
```
## Prohibited Practices
- Never hardcode specific project names or team information in templates
- Never generate a CLAUDE.md template exceeding 60 lines
- Never let Hook templates produce output on success
- Never exceed 500 lines in a single Skill file
- Never vendor a superpowers skill without `harness-delta.md`, `UPSTREAM.md`, and `evals/evals.json` (see ADR-0009)
- Never modify a vendored `SKILL.md` body outside the 2 allowed edits (frontmatter `name:` + pointer line)
```

- [ ] **Step 2: Add ADR pointer in Further Context**

Use Edit with `old_string`:
```
- Architecture decision (Claude Code only): docs/decisions/0007-claude-code-only.md
```
And `new_string`:
```
- Architecture decision (Claude Code only): docs/decisions/0007-claude-code-only.md
- Architecture decisions (superpowers vendor strategy): docs/decisions/0008-vendor-superpowers-v5.md + docs/decisions/0009-harness-delta-sidecar.md
```

- [ ] **Step 3: Verify line count is still ≤ 60**

```bash
wc -l CLAUDE.md
```
Expected: 43–45 lines.

- [ ] **Step 4: Verify EOF newline**

```bash
tail -c 1 CLAUDE.md | xxd | head -1
```
Expected: `0a`.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude): add 2 vendor-discipline rules + ADR-0008/0009 pointer"
```

---

## Task 3.5: Rewrite `commands/review-pr.md` as wrapper

**Files:**
- Modify: `commands/review-pr.md`

Per spec §12 the only `commands/` file consolidated by this integration is `review-pr.md` — it overlaps with `harness:requesting-code-review` + `harness:receiving-code-review`. Rewrite as a thin wrapper that invokes those skills.

- [ ] **Step 1: Replace the file content**

Read the current file first. Then replace with:

```markdown
---
description: PR code review — thin wrapper over harness:requesting-code-review + harness:receiving-code-review
---

This command is a thin wrapper. Real review work lives in the two skills below.

## When invoking for the *outbound* side (you authored the PR; asking for review)

Invoke `harness:requesting-code-review`. It enforces the pre-review checklist:
1. All `acceptance_criteria` in `features.json` for the in-progress feature are satisfied
2. No commit touches an item in `features.json` `out_of_scope`
3. No reverse-direction architecture-layer dependency (e.g., `skills/` importing from `commands/`)

The skill drafts the PR body including a `## feature` section referencing the `features.json` id, then creates the PR.

## When invoking for the *inbound* side (you are processing review feedback)

Invoke `harness:receiving-code-review`. It enforces:
- Rigid-constraint feedback → reconcile with `features.json` (accept-and-sync OR explicit reject with rationale; never silent)
- Architectural-change feedback → produce or update an ADR before merge

## Why a wrapper and not direct skill invocation?

This command stays for compatibility with users who already type `/harness:review-pr` and to give a single entry point for "do a PR review" without forcing the user to choose between the two skills. The actual review logic is owned by the two skills; this command must not duplicate that logic.

## Out of scope (intentionally NOT here)

- General code-quality checks unrelated to a PR — those belong in `harness:verification-before-completion`
- Security-focused review — use the project's separate security-review path (not yet a skill in this plugin)
- Architecture audit — that's `harness:audit`
```

- [ ] **Step 2: Verify EOF newline**

```bash
tail -c 1 commands/review-pr.md | xxd | head -1
```
Expected: `0a`.

- [ ] **Step 3: Commit**

```bash
git add commands/review-pr.md
git commit -m "refactor(commands): rewrite review-pr.md as wrapper over requesting/receiving-code-review skills"
```

---

## Task 3.6: Migrate the legacy codebuddy design spec

**Files:**
- Move: `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` → `docs/specs/2026-05-23-remove-codebuddy-design.md`

The integration spec §10 Phase 3 calls for this migration to consolidate all specs under `docs/specs/`. Use `git mv` to preserve history.

- [ ] **Step 1: git mv the file**

```bash
git mv docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md docs/specs/2026-05-23-remove-codebuddy-design.md
```

- [ ] **Step 2: Check whether docs/superpowers/specs/ is now empty (and remove the dir if so)**

```bash
ls docs/superpowers/specs/ 2>/dev/null
```

If empty, also check whether `docs/superpowers/` itself still has anything:

```bash
ls docs/superpowers/ 2>/dev/null
```

If `docs/superpowers/specs/` is empty but `docs/superpowers/` still has other entries (e.g., `plans/`), leave the `specs/` empty directory in place — git doesn't track empty dirs, so it'll disappear from the index automatically.

If `docs/superpowers/` is entirely empty, the directory will not appear in `git status`. No further action needed.

- [ ] **Step 3: Verify history is preserved**

```bash
git log --follow --oneline docs/specs/2026-05-23-remove-codebuddy-design.md | head -3
```
Expected: log shows commits including the original creation under the old path.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md docs/specs/2026-05-23-remove-codebuddy-design.md 2>/dev/null || true
git commit -m "docs(specs): migrate codebuddy design spec from docs/superpowers/specs/ to docs/specs/"
```

---

## Task 3.7: Bump `plugin.json` version to 2.0.0

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Bump version**

Use Edit with `old_string`:
```
  "version": "1.11.0",
```
And `new_string`:
```
  "version": "2.0.0",
```

- [ ] **Step 2: Update the description to reflect v2.0.0 capabilities**

The current description says: `"AI Agent Harness Engineering plugin. Initialize new projects, audit existing harness health, plan with structured triple-format tasks, verify completion with rigid/flexible constraints, and archive specs — all in one install."`

This mentions only the pre-v2.0.0 capability set. Use Edit with `old_string`:
```
  "description": "AI Agent Harness Engineering plugin. Initialize new projects, audit existing harness health, plan with structured triple-format tasks, verify completion with rigid/flexible constraints, and archive specs — all in one install.",
```
And `new_string`:
```
  "description": "AI Agent Harness Engineering plugin. 19 skills under the harness: namespace covering planning, TDD, brainstorming, debugging, code review, worktree isolation, and verification — built on superpowers v5.1.0 with a harness-delta sidecar layer that integrates features.json, ADRs, and project-local docs.",
```

- [ ] **Step 3: Validate JSON**

```bash
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && echo OK
```
Expected: `OK`.

- [ ] **Step 4: Verify version + EOF newline**

```bash
grep '"version"' .claude-plugin/plugin.json
tail -c 1 .claude-plugin/plugin.json | xxd | head -1
```
Expected: version is `"2.0.0"`. Last byte `0a`.

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat(plugin): bump version to 2.0.0 + refresh description for 19-skill topology"
```

---

## Task 3.8: Add CHANGELOG v2.0.0 entry

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Insert the v2.0.0 entry**

Read CHANGELOG.md to confirm the current top-of-file layout. The existing structure is:

```
# Changelog

## v1.11.0 (2026-05-23)
...
```

Use Edit with `old_string`:
```
# Changelog

## v1.11.0 (2026-05-23)
```
And `new_string`:
```
# Changelog

## v2.0.0 (2026-05-23)

**Breaking: superpowers v5.1.0 vendor integration**

- **All 19 skills now under the `harness:` namespace.** End state: 13 vendored from `obra/superpowers` v5.1.0 (each with a `harness-delta.md` + `UPSTREAM.md` + `evals/evals.json` sidecar per ADR-0009) + 6 harness-original.
- **4 forks renamed back to upstream names** (replaces v1.10.0's short-name renames):
  - `harness:plan` → `harness:writing-plans`
  - `harness:tdd` → `harness:test-driven-development`
  - `harness:verify` → `harness:verification-before-completion`
  - `harness:router` → `harness:using-harness` (kept as harness-original; absorbs the upstream `using-superpowers` role)
- **10 new vendored skills:** `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `using-git-worktrees`, `writing-skills`. Each ships with a harness-delta integrating features.json / ADR / docs per spec §7.
- **features.json schema migrated to v2.0** — status enum is now `proposed → building → done` (was `pending` / `in_progress` / `completed`); new optional `spec:` field for back-references to design specs in `docs/specs/`. Top-level `schema_version: "2.0"` declared.
- **New ADRs:**
  - ADR-0008 — "Vendor superpowers v5.1.0" — supersedes the implicit fork strategy embedded in v1.9.x–v1.11.x.
  - ADR-0009 — "harness-delta sidecar 4-file convention" — defines the per-skill anatomy.
- **New directories:**
  - `docs/specs/` — design specs (output of `harness:brainstorming`). Replaces the pre-v2.0.0 default `docs/superpowers/specs/`; existing artifact migrated.
  - `docs/incidents/` — debug notes (output of `harness:systematic-debugging`).
- **Root `features.json` introduced** — this plugin now dogfoods its own conventions per ADR-0003.
- **`scripts/sync-superpowers.sh` added** — read-only upstream reconciliation helper; emits per-skill diff summary against the currently installed superpowers cache. See ADR-0008 §"Implementation".
- **`commands/review-pr.md` rewritten** as a thin wrapper over `harness:requesting-code-review` + `harness:receiving-code-review`. Other commands retained.
- **CLAUDE.md** gains 2 prohibited-practice rules enforcing the vendor discipline (file still ≤ 60 lines).

Migration: Old slash command names (`/harness:plan`, `/harness:tdd`, `/harness:verify`, `/harness:router`) no longer resolve. Use the full upstream names listed above. Existing user projects with their own features.json files using the old status enum will be flagged by `harness:audit` as a hint (back-compatible — new schema fields are optional; old status values still parse but should be migrated).

## v1.11.0 (2026-05-23)
```

- [ ] **Step 2: Verify EOF newline**

```bash
tail -c 1 CHANGELOG.md | xxd | head -1
```
Expected: `0a`.

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): v2.0.0 release notes (superpowers v5.1.0 vendor integration)"
```

---

## Task 4.1: Full verification gate suite

**Files:**
- No files modified — read-only verification.

This task runs the spec §10 Phase 4 verification gates. If any check fails, stop and report rather than blindly fixing — failures here may indicate a real regression that needs review.

- [ ] **Step 1: Grep gate — zero hits for the 4 old short names outside documentary files**

```bash
grep -rE 'harness:(plan|tdd|verify|router)\b' . \
  --include='*.md' --include='*.json' --include='*.sh' --include='*.py' \
  --exclude-dir=.git --exclude-dir=ziLgb4r4 --exclude-dir=node_modules \
  --exclude-dir=docs/superpowers \
  --exclude=CHANGELOG.md \
  | grep -v 'docs/specs/' | grep -v 'docs/plans/' \
  | grep -v 'docs/decisions/0008-' | grep -v 'docs/decisions/0009-' \
  | grep -v 'features.json' \
  || echo "(zero hits — gate passes)"
```
Expected: `(zero hits — gate passes)`. Any other output is a stray reference that must be fixed before continuing.

- [ ] **Step 2: All 14 reorganized skills' evals JSON valid**

```bash
for s in using-harness writing-plans test-driven-development verification-before-completion brainstorming dispatching-parallel-agents executing-plans finishing-a-development-branch receiving-code-review requesting-code-review subagent-driven-development systematic-debugging using-git-worktrees writing-skills; do
  python3 -m json.tool "skills/$s/evals/evals.json" > /dev/null && echo "[$s] OK" || echo "[$s] FAIL"
done
```
Expected: 14 OK lines, 0 FAIL.

- [ ] **Step 3: All 13 vendored skills track upstream cleanly**

```bash
./scripts/sync-superpowers.sh
```
Expected: 13 lines, each `diff-lines=2 last-synced=2026-05-23`. Any skill with diff-lines > 2 indicates an unauthorized edit to SKILL.md body — investigate before proceeding.

- [ ] **Step 4: 5 unchanged harness-original skills present**

```bash
for s in archive audit canary evolve init; do
  test -f "skills/$s/SKILL.md" && echo "[$s] OK" || echo "[$s] MISSING"
done
```
Expected: 5 OK lines.

- [ ] **Step 5: features.json + plugin.json valid; version is 2.0.0**

```bash
python3 -m json.tool features.json > /dev/null && echo "features.json: OK"
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && echo "plugin.json: OK"
grep '"version"' .claude-plugin/plugin.json
```
Expected: both OK; version line shows `"version": "2.0.0"`.

- [ ] **Step 6: CLAUDE.md still ≤ 60 lines**

```bash
wc -l CLAUDE.md
```
Expected: ≤ 60 (after this plan, expected 43–45).

- [ ] **Step 7: 4-file structure intact for all 13 vendored skills**

```bash
for s in writing-plans test-driven-development verification-before-completion brainstorming dispatching-parallel-agents executing-plans finishing-a-development-branch receiving-code-review requesting-code-review subagent-driven-development systematic-debugging using-git-worktrees writing-skills; do
  entries=$(ls "skills/$s/" 2>/dev/null | sort | tr '\n' ' ')
  if [[ "$entries" == "evals harness-delta.md SKILL.md UPSTREAM.md " ]]; then
    echo "[$s] OK"
  else
    echo "[$s] FAIL: got '$entries'"
  fi
done
```
Expected: 13 OK lines.

- [ ] **Step 8: 2-file structure intact for using-harness**

```bash
entries=$(ls skills/using-harness/ | sort | tr '\n' ' ')
[[ "$entries" == "evals SKILL.md " ]] && echo "using-harness: OK (2-file)" || echo "using-harness: FAIL: got '$entries'"
```
Expected: OK.

If all 8 steps pass, report a single summary line and proceed to Task 4.2. If any step fails, stop and surface the failure for the controller / user.

---

## Task 4.2: `harness:init` template references new skill names

**Files:**
- Read-only inspection of `skills/init/SKILL.md` and `docs/templates/<lang>/CLAUDE.md.template`.

`harness:init` is responsible for producing CLAUDE.md and skill stubs for new projects. After the v2.0.0 rename, the template should not refer to old short names.

- [ ] **Step 1: Grep init skill + templates for old short names**

```bash
grep -nE 'harness:(plan|tdd|verify|router)\b' skills/init/SKILL.md docs/templates/*/CLAUDE.md.template 2>/dev/null || echo "(zero hits — templates clean)"
```
Expected: `(zero hits — templates clean)`.

If hits are found, they are stray references that must be fixed — read context to decide whether to update to the new name or leave (methodology mention).

- [ ] **Step 2: Verify the init skill references the new docs conventions**

```bash
grep -nE 'docs/(specs|incidents|plans)/' skills/init/SKILL.md || echo "(init does not mention new docs conventions)"
```

If the init skill doesn't mention `docs/specs/` or `docs/incidents/`, that is a known gap — record it in the report as a follow-up but do NOT fix it as part of Plan C (out of scope; would be a new feature for a future plan).

- [ ] **Step 3: No commit needed if no edits made**

If Step 1 produced hits and fixes are applied, commit with:
```bash
git add skills/init/ docs/templates/
git commit -m "fix(init): remove residual old short names from init template"
```

Otherwise (Step 1 was clean), skip commit and proceed.

---

## Task 4.3: Transition F003 + spec status to `done`; final report

**Files:**
- Modify: `features.json` (F003 building → done)
- Modify: `docs/specs/2026-05-23-superpowers-integration-design.md` (front-matter status building → done)

- [ ] **Step 1: Transition F003 to done**

Use Edit on `features.json` with `old_string`:
```
      "id": "F003",
      "name": "superpowers-docs-refresh",
      "priority": 3,
      "status": "building",
```
And `new_string`:
```
      "id": "F003",
      "name": "superpowers-docs-refresh",
      "priority": 3,
      "status": "done",
```

- [ ] **Step 2: Transition spec status to done**

Use Edit on `docs/specs/2026-05-23-superpowers-integration-design.md` with `old_string`:
```
status: building
features:
```
And `new_string`:
```
status: done
features:
```

- [ ] **Step 3: Verify all 3 features are done**

```bash
python3 -m json.tool features.json > /dev/null && echo "JSON OK"
python3 -c 'import json; d=json.load(open("features.json")); print([(f["id"], f["status"]) for f in d["features"]])'
```
Expected JSON OK; output is `[('F001', 'done'), ('F002', 'done'), ('F003', 'done')]`.

- [ ] **Step 4: Commit**

```bash
git add features.json docs/specs/2026-05-23-superpowers-integration-design.md
git commit -m "chore(features): F003 + integration spec done — superpowers v5.1.0 integration complete"
```

---

## Spec coverage review (Plan C)

This plan implements the following spec sections from `docs/specs/2026-05-23-superpowers-integration-design.md`:

| Spec section | Where in this plan |
|---|---|
| §4 D11 (review-pr wrapper) | Task 3.5 |
| §4 D12 (CLAUDE.md ≤ 60 lines + ADR-9 detail externalized) | Task 3.4 |
| §4 D14 (v1.11.0 → v2.0.0) | Task 3.7 |
| §8 docs/specs migration | Task 3.6 |
| §10 Phase 3 (architecture.md / READMEs / CLAUDE.md / review-pr / plugin.json / CHANGELOG / spec move) | Tasks 3.1–3.8 |
| §10 Phase 4 (grep gate, evals, init template, original skills intact, status to done) | Tasks 4.1–4.3 |
| §14 Versioning + CHANGELOG | Tasks 3.7, 3.8 |
| §15 Dogfooding (F003 lifecycle) | Tasks 3.0 (→ building) and 4.3 (→ done) |
| §17 Risk: stray refs in commands/ and docs/templates/ | Task 4.2 grep |

## Self-review checklist

- [x] **Spec coverage:** all of spec §10 Phase 3 + Phase 4 line items have a Task. ADR-0008/0009 references woven into Task 3.4. F003 + spec status lifecycle closed at Task 4.3.
- [x] **Placeholder scan:** No TBD, TODO, or "fill in later" in this plan. Tasks 3.2 and 3.3 instruct the executor to Read the README files first because the exact surrounding lines may have small variations (the table position is stable but the exact blank-line count around `---` separators is not specified — this is a documented "Read first, then Edit" pattern, not a placeholder).
- [x] **Type consistency:** All skill name references use `harness:<full-name>`. All file paths use the post-Plan-A/B layout (skills/ entries match the actual on-disk names).
- [x] **Phase 4 is read-only by default:** Tasks 4.1 and 4.2 only commit if a real fix is needed (stray reference found). The final status-transition commit (Task 4.3) is the only mandatory Phase 4 commit.
- [x] **No "Similar to Task N" shortcuts.** Task 3.3 (zh-CN README) repeats the content of Task 3.2 in Chinese rather than referring back to it.

## Execution handoff

**Plan complete and saved to `docs/plans/2026-05-23-phase-3-and-4-docs-and-verify.md`.**

Two execution options:

1. **Subagent-Driven (recommended)** — fresh subagent per task, two-stage review. Best for the 11 mostly-surgical tasks here. Each task is small enough that an implementer + spec-review + code-review trio runs quickly.

2. **Inline Execution** — sequential in this session via `harness:executing-plans`. Lower overhead, higher context cost. Reasonable for a plan this size.

After Plan C executes, the integration spec transitions to `done` and all three features (F001/F002/F003) are complete. The natural next step is to push the local main to `origin/main` for review or release (the user explicitly opted not to push during Plans A and B; pushing v2.0.0 is the closing action).

**Which approach?**
