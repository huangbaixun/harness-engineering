# Harness Engineering Plugin

[![Version](https://img.shields.io/badge/version-v1.10.1-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A51.0.0-orange)](https://docs.claude.com)

**Shift your core engineering work from "writing code" to "designing environments where AI agents work reliably."**

Harness Engineering Plugin packages this methodology into ready-to-use Skills, Commands, and Agents -- install and go, no extra configuration needed.

---

## Quick Start

**Step 1: Install**

**Option A -- Marketplace (recommended, auto-updates)**

In a Claude Code conversation:

```
/plugin marketplace add https://raw.githubusercontent.com/huangbaixun/harness-engineering/main/.claude-plugin/marketplace.json
```

After subscribing, select it from the plugin list. Claude Code will prompt you when new versions are available.

**Option B -- Clone from GitHub**

```bash
git clone https://github.com/huangbaixun/harness-engineering.git
claude --plugin-dir ./harness-engineering
```

Good for local evaluation before committing to long-term use.

**Option C -- Official Marketplace (coming soon)**

```bash
# Available after Anthropic review
claude plugins add harness-engineering
```

Or search "Harness Engineering" in Cowork and click install.

**Step 2: Initialize a new project**

In Claude Code, say:

> "Help me initialize this project's Harness"

After initialization, your project gets:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Universal memory layer (<=60 lines), the single source of truth |
| `CLAUDE.md` | 2-line entry point for Claude Code, points to AGENTS.md |
| `init.sh` | Session startup script -- runs tool detection before each new session |
| `.claude/settings.json` | Permission control + Hook registration (incl. SessionStart) |
| `.claude/hooks/session-start.sh` | SessionStart Hook: restores progress context on session start |
| `.claude/hooks/` | Type-check, .env protection, auto-format hooks |
| `.claude/skills/plan/` | Pre-implementation planning Skill (triggers for >30 min or 3+ file tasks) |
| `.claude/skills/tdd/` | TDD Skill (enforced RED->GREEN->REFACTOR cycle) |
| `.claude/skills/verify/` | Pre-completion verification Skill (4-layer check before marking done) |
| `docs/architecture.md` | Architecture diagram -- the agent's spatial awareness doc |
| `docs/claude-progress.json` | Cross-session progress tracking |

Verify readiness: `bash init.sh` -- you should see "Harness ready" on success.

**Step 3: Ongoing benefits**

The SessionStart Hook automatically restores progress context at the start of every session. The harness:plan / harness:tdd / harness:verify workflow Skills engage automatically during implementation, ensuring a complete plan -> implement -> verify loop. Commands let you trigger audits, PR reviews, and entropy scans on demand.

---

## Core Skills

After installation, these Skills trigger automatically based on your intent -- no need to memorize command names. All Skills use the `harness:` namespace:

| Skill | Trigger | What it does |
|-------|---------|-------------|
| **harness:init** | New project / "set up my Harness" | Generates complete 6-layer Harness structure (AGENTS.md + Hooks + templates) |
| **harness:audit** | "Agent keeps making the same mistakes" / legacy project audit | 7-dimension health score + prioritized fix plan |
| **harness:evolve** | "AGENTS.md is too long" / after new model release | Memory file trimming + Hook adaptation + garbage collection |
| **harness:router** | Every scenario (1% rule, loaded each session) | Intent recognition, ensures the right Skill is triggered |
| **harness:plan** | New feature / bug fix (>30 min or 3+ files) | Decomposes into 2-5 min verifiable task blocks with `<action>/<verify>/<done>` triple structure |
| **harness:archive** | Feature completed, ready to archive | Archives specs to `docs/archive/`, checks doc-code consistency, runs architecture health scan |
| **harness:tdd** | Any code writing (bound to 1% rule) | Enforces RED->GREEN->REFACTOR cycle -- tests first, then implementation |
| **harness:verify** | Before declaring a task complete | 4-layer check (Functional / Quality / Architecture / Integration) |

---

## Slash Commands

| Command | Function | Recommended frequency |
|---------|----------|----------------------|
| `/harness:init` | Initialize Harness | Project start |
| `/harness:audit` | Harness health audit | On demand |
| `/harness:assign` | Sprint feature assignment -- auto-calculates dependencies + generates claim script | Sprint start |
| `/harness:review-pr` | Comprehensive PR review (quality + security + architecture) | Every PR |
| `/harness:dump` | Save session progress to claude-progress.json | At ~50% context usage |
| `/harness:sync-docs` | Doc-code consistency check | Daily |
| `/harness:scan-arch` | Architecture health scan | Weekly |
| `/harness:trim` | Trim AGENTS.md to <=60 lines | After new model release |
| `/harness:scan-entropy` | Dead code + duplicate implementation + over-coupling detection | Monthly |

---

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| **security-reviewer** | Opus | Injection vulnerabilities, auth flaws, secret leaks |
| **code-review-agent** | Sonnet | Architecture compliance, maintainability, tech debt |
| **coding-agent** | Sonnet | Long-cycle multi-session coding with cross-session handoff |
| **explore-agent** | Haiku | Codebase exploration, keeps main thread context clean |

---

## Language Templates

`harness:init` supports five tech stacks, automatically selecting the matching template during initialization:

- **TypeScript / Node.js** -- strict mode, pnpm, Jest/Vitest, Biome/ESLint
- **Python** -- type hints, poetry/uv, pytest, mypy/ruff
- **Go** -- go modules, golangci-lint, testing
- **Java** -- JUnit 5 + Mockito + AssertJ, Maven/Gradle, Checkstyle + SpotBugs
- **Generic** -- Language-agnostic Harness skeleton (includes AGENTS.md template)

---

## Platform Compatibility

This plugin supports cross-platform Hooks since v1.9.3:

| Feature | Claude Code | Windows |
|---------|-------------|---------|
| AGENTS.md universal memory | Yes | Yes |
| init.sh auto-detection | Yes | Yes (Git Bash) |
| Skills / Commands | Yes | Yes |
| Hooks (polyglot wrappers) | Yes | Yes (Git Bash / MSYS2) |

**Cross-platform Hook mechanism** (v1.9.3): Each hook script comes in three forms -- `.cmd` (polyglot wrapper, valid for both CMD and bash), extensionless (bash logic), and `.sh` (backward compat). `hooks.json` uses the `${CLAUDE_PLUGIN_ROOT:-.}` path variable, working in both plugin-install and local-dev modes. On Windows, Git for Windows bash is auto-detected; if unavailable, the hook silently succeeds without blocking.

---

## Local Installation Verification

```bash
# Unpack the .skill bundle to a test directory
unzip harness-engineering.skill -d /tmp/harness-test

# Load the plugin
claude --plugin-dir /tmp/harness-test
```

---

## Design Principles

This plugin is fully self-bootstrapped (dogfooding) -- Harness Engineering conventions are used to develop the Harness Engineering Plugin itself:

- `AGENTS.md` <=60 lines, the single source of truth
- `docs/architecture.md` contains explicit dependency rules
- `docs/decisions/` has complete ADR records for every key decision (incl. ADR 0005 tool-agnostic architecture)
- Hook scripts follow the "silent on success, visible on failure" principle
- Skills use `.claude/` paths directly

---

## Methodology References

This plugin is built on the [Harness Engineering Practice Manual](references/HarnessEngineering.md) -- synthesizing first-hand practices from Anthropic, OpenAI, InfoQ, and Hacker News, covering long-cycle task harness design, multi-agent architecture, garbage collection systems, and other core patterns.

v1.9.2 integrated workflow design ideas from [obra/superpowers](https://github.com/obra/superpowers): the writing-plans (pre-implementation planning gate), tdd (enforced RED->GREEN->REFACTOR cycle), and verification (4-layer completion check) Skills are directly inspired by that project's core practices, deeply integrated with Harness's SessionStart Hook and claude-progress.json cross-session memory system to form a complete "plan -> implement -> verify -> remember" loop.

Multi-person collaboration design references the [Team Parallel Development Guide](references/team-parallel-development.md), including features.json parallel field design, Git Worktree isolation, and sprint assignment algorithms.

---

## Contributing

We welcome new Skills, language templates, and Hook script improvements. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

[Chinese documentation / 中文文档](README.zh-CN.md)

---

<details>
<summary>Full file listing</summary>

```
harness-engineering-plugin/
├── AGENTS.md                             <- Universal memory file (single source of truth, <=60 lines)
├── CLAUDE.md                             <- 2-line wrapper (Claude Code)
├── .claude-plugin/
│   └── plugin.json                       <- Claude Code plugin manifest
├── skills/                               <- Unified harness: namespace
│   ├── router/SKILL.md                   harness:router meta-Skill (1% rule)
│   ├── init/SKILL.md                     harness:init project initialization
│   ├── audit/SKILL.md                    harness:audit legacy audit
│   ├── evolve/SKILL.md                   harness:evolve continuous evolution
│   ├── archive/SKILL.md                  harness:archive completion archival
│   ├── plan/SKILL.md                     harness:plan pre-implementation planning
│   ├── tdd/SKILL.md                      harness:tdd TDD workflow
│   └── verify/SKILL.md                   harness:verify pre-completion verification
├── commands/
│   ├── assign.md                <- /harness:assign (team sprint assignment)
│   ├── init.md
│   ├── audit.md
│   ├── review-pr.md
│   ├── dump.md
│   ├── sync-docs.md
│   ├── scan-arch.md
│   ├── trim.md
│   └── scan-entropy.md
├── agents/
│   ├── security-reviewer.md              Opus
│   ├── explore-agent.md                  Haiku
│   ├── code-review-agent.md              Sonnet
│   └── coding-agent.md                   Sonnet
├── hooks/
│   └── hooks.json                        <- Hook registration (${CLAUDE_PLUGIN_ROOT:-.} fallback)
├── scripts/                              <- Each hook in three forms: .cmd / extensionless / .sh
│   ├── session-start{,.cmd,.sh}          <- SessionStart Hook
│   ├── stop-typecheck{,.cmd,.sh}
│   ├── pre-protect-env{,.cmd,.sh}
│   ├── post-format{,.cmd,.sh}
│   ├── stop-commit-progress{,.cmd,.sh}
│   └── post-observe{,.cmd,.sh}
├── docs/
│   ├── architecture.md
│   ├── decisions/                        ADR records (0001-0005)
│   └── templates/                        Five language stack templates (incl. AGENTS.md.template)
├── references/
│   ├── HarnessEngineering.md             Full methodology manual
│   ├── team-parallel-development.md      Team parallel development guide
│   ├── hook-patterns.md
│   └── anti-patterns.md
├── evals/
│   └── evals.json                        Eval index
├── LICENSE
├── CONTRIBUTING.md
└── CHANGELOG.md
```

</details>
