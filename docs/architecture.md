# Harness Engineering Plugin — Architecture Diagram

## System Overview

This is an AI Agent Harness plugin that targets Claude Code and provides engineering teams with standardized AI Agent Harness engineering capabilities. As of v2.1.0 it consists of 19 skills under the `harness:` namespace (6 harness-original + 13 vendored from `obra/superpowers` v6.3.0), plus a set of supporting Commands, Hooks, and References.

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
│   ├── # vendored from superpowers v6.3.0 (13) — 4 harness files + upstream companions
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
│   │   ├── 0009-harness-delta-sidecar.md       ← v2.0.0: 4-file sidecar convention
│   │   ├── 0010-meta-skill-session-injection.md
│   │   ├── 0011-features-json-field-ownership.md   ← features.json 字段所有权 / schema 2.1
│   │   └── 0012-features-json-canonical-location.md ← features.json 规范位置为仓库根目录
│   ├── plans/                      ← Implementation plans (output of harness:writing-plans)
│   ├── specs/                      ← Design specs (output of harness:brainstorming)
│   ├── incidents/                  ← Debug notes (output of harness:systematic-debugging)
│   ├── archive/                    ← Archived specs/plans of done features (output of harness:archive)
│   ├── evals/                      ← Eval run records (skill/command eval reports)
│   ├── superpowers/                ← Pre-v2.0.0 legacy location, retained for history
│   └── templates/                  ← Multi-language project templates (typescript / python / go / generic)
├── references/                     ← Reference documents (loaded on demand)
├── scripts/
│   ├── self-test.sh, health-score.py, generate-harness.sh
│   └── sync-superpowers.sh         ← v2.0.0: upstream reconciliation helper (read-only diff report)
└── evals/                          ← Project-level evals (top-level evals.json is the registry)
```

## Vendored skill anatomy (per ADR-0009, as amended 2026-08-22)

Each of the 13 vendored skills contains 4 harness files plus whatever companion files upstream ships alongside that skill:

```
skills/<name>/
├── SKILL.md            # superpowers v6.3.0 content verbatim, only 2 allowed edits applied:
│                       #   1. frontmatter `name:` → `harness:<name>`
│                       #   2. pointer line inserted: "> harness local rules: read harness-delta.md"
├── <companions>        # upstream verbatim, ZERO edits — e.g. visual-companion.md, code-reviewer.md,
│                       #   root-cause-tracing.md, *-prompt.md, scripts/, examples/
├── harness-delta.md    # local rules (features.json / ADR / docs / Stop Hook integrations)
├── UPSTREAM.md         # provenance (source SHA, fork date, last-sync date, divergences, companion inventory)
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

The script compares `SKILL.md` only. After applying a sync, verify the invariants directly: each vendored `SKILL.md` must differ from upstream by exactly the 2 allowed edits, and each companion file must be byte-identical (`cmp`). Last sync: **v5.1.0 → v6.3.0 on 2026-08-22**.
