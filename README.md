# Harness Engineering Plugin

[![Version](https://img.shields.io/badge/version-v2.4.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A51.0.0-orange)](https://docs.claude.com)

**Shift your core engineering work from "writing code" to "designing environments where AI agents work reliably."**

Harness Engineering Plugin packages this methodology into ready-to-use Skills, Commands, and Agents -- install workflow skills, then configure the project checks that actually apply.

## Codex local quick start (v2.4.0)

Requires Python 3.10+; local development/tests use only standard libraries. From this repository, preview and adopt a project:

```bash
python3 scripts/harness_init.py --tool codex --project ../my-project --dry-run --adopt-existing
python3 scripts/harness_init.py --tool codex --project ../my-project --adopt-existing
```

Project delivery installs 19 skills in `.agents/skills/<name>` and supporting resources in `.agents/harness`. Existing project rules remain outside the managed AGENTS block. Conflicting resources/configuration are reported before writes; review updates rather than overwriting existing settings. GitHub sync and automatic commits are disabled. Configure verification as argv arrays in `.harness/config.json`, then run:

```bash
python3 .agents/harness/scripts/codex_hook.py verify --project .
python3 .agents/harness/scripts/harness_state.py checkpoint --project . --task F001 --next-action "run checks"
```

Alternatively use `--delivery plugin` and load this checkout through Codex's native local plugin flow; do not also install project skills. Root `plugin.json` explicitly selects `hooks/codex.json` through `extensions.com.openai`; the legacy Codex manifest remains a fallback. Review hook trust with `/hooks`. Project-only skills do not activate hooks; no global configuration is written. See [platform matrix](docs/platform-capabilities.md), [Codex adapter](references/platforms/codex.md) and [GPT-6 workflow guidance](references/gpt6-workflows.md). Named command/agent files are Claude-specific; model selection stays with the host/user.

To uninstall project delivery, review and remove the generated `.agents/harness`, `.agents/skills/<name>`, managed AGENTS block and `.harness/config.json`; retain your own rules/features/progress. Uninstall plugin delivery through the host plugin UI. Legacy `docs/claude-progress.json` is read-only fallback; new checkpoints use `docs/harness-progress.json`.

Validation: `python3 scripts/validate.py`. Actual measurements and unverified host capabilities are listed in [evaluation](docs/evals/2026-10-05-codex-adaptation-report.md).

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

Preview offline Claude adoption from this repository:

```bash
python3 scripts/harness_init.py --tool claude --project ../my-project --adopt-existing --dry-run
python3 scripts/harness_init.py --tool claude --project ../my-project --adopt-existing
```

It creates/updates the managed CLAUDE.md block, `.harness/config.json`, root
features.json if absent, `.claude/harness` resources and `.claude/skills`. Existing
settings and permissions remain untouched; no hooks or global configuration are
activated. Plugin delivery uses `--delivery plugin` instead and copies no skill tree.

Discover the actual project commands and configure verification_commands as argv
arrays, then execute `python3 .claude/harness/scripts/harness_runtime.py verify
--project .`. Empty checks are not a readiness signal. Save neutral progress through
the checkpoint helper when needed. Design/docs templates are available on demand;
the initializer does not manufacture project architecture, ADRs or test results.

Trusted plugin SessionStart emits bounded state; workflows are selected by relevant
task intent. Local adapter fixtures do not prove actual native lifecycle execution.

---

## Workflow cleanup (2.4.0)

Portable root `plugin.json` is canonical. `extensions.com.openai.hooks` explicitly
selects `hooks/codex.json`; `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`
remain compatibility entries. Native hooks still require host trust.

Both hosts share bounded context, argv verification and neutral checkpoint logic.
The offline initializer now accepts `--tool claude` as well as `--tool codex`; Claude
project delivery uses `.claude/harness` and `.claude/skills`. Existing settings and
permissions are preserved; hooks are not implicitly activated by project adoption.

Retired defaults: auto-commit progress, empty auto-format and homemade telemetry.
`stop-commit-progress` / `post-format` remain warning-only compatibility stubs.
`stop-typecheck` now runs real configured checks, using event JSON on stdin.
Empty verification is not success. Direct-file protection parses stdin without jq,
allows `.env.example` / `.env.sample` / `.env.template`, checks resolved aliases,
and supplements native permissions without parsing or securing Bash commands.

Optional observe reads native stdin events and requires `telemetry_enabled: true`;
it stores sanitized event metadata in `.harness/telemetry.jsonl`. Token/cost/duration
remain unknown. Issue sync remains separately opt-in through features.json.github;
the initializer never enables it. Explicit checkpoints never commit.

No universal 60/300-line, 20k-token, 50%-context or fixed model-alias policy remains.
Audits assess actual enforcement and observed outcomes. Existing installs must
review and remove retired hook registrations; this initializer deliberately refuses
to overwrite an older runtime/configuration silently. See
[ADR 0014](docs/decisions/0014-evidence-based-workflow-cleanup.md).

## Core Skills

After installation, these Skills trigger automatically based on your intent -- no need to memorize command names. All Skills use the `harness:` namespace:

| Skill | Trigger | What it does |
|-------|---------|-------------|
| **harness:init** | New project / "set up my Harness" | Conflict-first offline adoption for the actual host |
| **harness:audit** | "Agent keeps making the same mistakes" / legacy project audit | Evidence-backed pass/fail/unknown findings + prioritized repairs |
| **harness:evolve** | "CLAUDE.md is too long" / after new model release | Memory file trimming + Hook adaptation + garbage collection |
| **harness:using-harness** | Relevant workflow routing | Intent recognition, ensures the right Skill is triggered |
| **harness:writing-plans** | An agreed change requiring a plan | Records interfaces, decisions and checkable implementation tasks |
| **harness:canary** | Ready to deploy / release planning | Risk-scored canary deployment runbook with staged rollout, rollback triggers, observability checklists |
| **harness:archive** | Feature completed, ready to archive | Archives specs to `docs/archive/`, checks doc-code consistency, runs architecture health scan |
| **harness:test-driven-development** | Behavioral implementation | Enforces RED->GREEN->REFACTOR cycle -- tests first, then implementation |
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

## Slash Commands

| Command | Function | Recommended frequency |
|---------|----------|----------------------|
| `/harness:init` | Initialize Harness | Project start |
| `/harness:audit` | Harness health audit | On demand |
| `/harness:assign` | Sprint feature assignment -- auto-calculates dependencies + generates claim script | Sprint start |
| `/harness:canary` | Generate canary deployment runbook with risk assessment | Pre-deploy |
| `/harness:review-pr` | Comprehensive PR review (quality + security + architecture) | Every PR |
| `/harness:dump` | Save session progress to harness-progress.json | When a useful checkpoint is needed |
| `/harness:sync-docs` | Doc-code consistency check | Daily |
| `/harness:scan-arch` | Architecture health scan | Weekly |
| `/harness:trim` | Trim CLAUDE.md to focused instructions | After new model release |
| `/harness:scan-entropy` | Dead code + duplicate implementation + over-coupling detection | Monthly |

---

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| **security-reviewer** | Host/user default | Injection vulnerabilities, auth flaws, secret leaks |
| **code-review-agent** | Host/user default | Architecture compliance, maintainability, tech debt |
| **coding-agent** | Host/user default | Long-cycle multi-session coding with cross-session handoff |
| **explore-agent** | Host/user default | Codebase exploration, keeps main thread context clean |

---

## Language Templates

`harness:init` supports five tech stacks, automatically selecting the matching template during initialization:

- **TypeScript / Node.js** -- strict mode, pnpm, Jest/Vitest, Biome/ESLint
- **Python** -- type hints, poetry/uv, pytest, mypy/ruff
- **Go** -- go modules, golangci-lint, testing
- **Java** -- JUnit 5 + Mockito + AssertJ, Maven/Gradle, Checkstyle + SpotBugs
- **Generic** -- Language-agnostic Harness skeleton

---

## Platform Compatibility

This plugin supports cross-platform Hooks since v1.9.3:

| Feature | Claude Code | Windows |
|---------|-------------|---------|
| init.sh auto-detection | Yes | Yes (Git Bash) |
| Skills / Commands | Yes | Yes |
| Hooks (polyglot wrappers) | Yes | Yes (Git Bash / MSYS2) |

**Cross-platform Hook mechanism** (v1.9.3): Each hook script comes in three forms -- `.cmd` (polyglot wrapper, valid for both CMD and bash), extensionless (bash logic), and `.sh` (backward compat). `hooks.json` uses the `${CLAUDE_PLUGIN_ROOT:-.}` path variable, working in both plugin-install and local-dev modes. On Windows the compatibility wrappers require Git Bash / MSYS2; if unavailable, verification cannot be claimed. Windows runtime execution is not validated by the local macOS suite.

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

- `CLAUDE.md` focused instructions, the single source of truth
- `docs/architecture.md` contains explicit dependency rules
- `docs/decisions/` has complete ADR records for every key decision (ADR 0013 supersedes the ADR 0007 Claude-only constraint)
- Hook scripts follow the "silent on success, visible on failure" principle
- Platform adapters select host paths; shared skills remain platform-neutral

---

## Methodology References

This plugin is built on the [Harness Engineering Practice Manual](references/HarnessEngineering.md) -- synthesizing first-hand practices from Anthropic, OpenAI, InfoQ, and Hacker News, covering long-cycle task harness design, multi-agent architecture, garbage collection systems, and other core patterns.

v1.9.2 integrated workflow design ideas from [obra/superpowers](https://github.com/obra/superpowers): the writing-plans (pre-implementation planning gate), test-driven-development (enforced RED->GREEN->REFACTOR cycle), and verification-before-completion (4-layer completion check) Skills are directly inspired by that project's core practices, deeply integrated with Harness's SessionStart Hook and harness-progress.json cross-session memory system to form a complete "plan -> implement -> verify -> remember" loop.

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
├── CLAUDE.md                             <- Project memory file (single source of truth, focused instructions)
├── .claude-plugin/
│   └── plugin.json                       <- Claude Code plugin manifest
├── skills/                               <- Unified harness: namespace
│   ├── using-harness/SKILL.md            harness:using-harness relevant workflow routing
│   ├── init/SKILL.md                     harness:init project initialization
│   ├── audit/SKILL.md                    harness:audit legacy audit
│   ├── evolve/SKILL.md                   harness:evolve continuous evolution
│   ├── archive/SKILL.md                  harness:archive completion archival
│   ├── canary/SKILL.md                   harness:canary deployment runbook
│   ├── writing-plans/SKILL.md            harness:writing-plans pre-implementation planning
│   ├── test-driven-development/SKILL.md  harness:test-driven-development TDD workflow
│   └── verification-before-completion/SKILL.md  harness:verification-before-completion pre-completion verification
├── commands/
│   ├── assign.md                <- /harness:assign (team sprint assignment)
│   ├── canary.md                <- /harness:canary (deployment runbook)
│   ├── init.md
│   ├── audit.md
│   ├── review-pr.md
│   ├── dump.md
│   ├── sync-docs.md
│   ├── scan-arch.md
│   ├── trim.md
│   └── scan-entropy.md
├── agents/
│   ├── security-reviewer.md              host/user default
│   ├── explore-agent.md                  host/user default
│   ├── code-review-agent.md              host/user default
│   └── coding-agent.md                   host/user default
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
│   ├── decisions/                        ADR records (0001-0007)
│   └── templates/                        Five language stack templates
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
