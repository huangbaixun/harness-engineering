# Anthropic Marketplace Submission Materials

> Submission URL: https://claude.ai/settings/plugins/submit  
> Version: v1.10.1  
> Preparation date: 2026-04-18

---

## 1. Basic Information

| Field | Value |
|-------|-------|
| **Plugin Name** | harness-engineering |
| **Display Name** | Harness Engineering |
| **Version** | 1.10.1 |
| **Author / Organization** | Harness Engineering |
| **Repository URL** | https://github.com/huangbaixun/harness-engineering |
| **Homepage URL** | https://github.com/huangbaixun/harness-engineering |
| **License** | MIT |
| **Category** | Engineering / Developer Tools |

---

## 2. Short Description (120 characters max)

```
AI Agent Harness Engineering: init, audit, team sprint allocation. Built for Claude Code — install and go.
```

---

## 3. Long Description (Markdown)

```markdown
## What is Harness Engineering?

Harness Engineering transforms how your team works with AI agents — shifting the focus from "writing code" to "designing environments where AI agents work reliably."

Instead of hoping Claude remembers your conventions, you encode them into a structured **6-layer Harness**: Memory (AGENTS.md), Rules (settings.json), Skills, Agents, Hooks, and MCP Tools.

## What This Plugin Does

Install once, and your projects get:

- **`harness:init`** — Bootstraps a complete AI agent harness for any new project in minutes. Generates AGENTS.md, init.sh, hooks (type-check, .env protection, auto-format), and architecture docs. Supports TypeScript, Python, Go, Java, and generic stacks.

- **`harness:audit`** — Scores your existing project's harness health across 7 dimensions. Pinpoints weak spots and generates a prioritized fix plan.

- **`harness:evolve`** — Runs periodic garbage collection on your harness: trims bloated AGENTS.md files, removes stale rules, adapts hooks to new model capabilities.

- **`harness:archive`** — *(New in v1.10.0)* Automated completion archival and doc sync. When a feature is done, archives specs to `docs/archive/` (preserving git history), checks doc-code consistency, runs a lightweight architecture health scan, and generates a structured archive report.

- **`harness:plan`** — *(Enhanced in v1.10.0)* Now enforces `<action>/<verify>/<done>` triple structure for every task. Reads `rigid` vs `flexible` constraints from `features.json` — rigid items (acceptance criteria, forbidden patterns) must map to tasks; flexible items (technical notes) are advisory. Ensures 100% rigid constraint coverage before execution begins.

- **`/harness:assign`** — Sprint planning for AI-assisted teams. Analyzes your `features.json` dependency graph, calculates critical path, and generates a `sprint-kickoff.sh` with per-member task assignments that minimize file conflicts and maximize parallel execution.

## Key Design Principles

- **Built for Claude Code**: Uses `.claude/` as the standard configuration directory
- **AGENTS.md as single source of truth**: One universal memory file, two 2-line wrappers for each tool
- **60-line rule**: Based on ETH Zurich research showing performance degrades with oversized memory files
- **Hooks over instructions**: Critical constraints enforced deterministically via hooks, not model judgment

## Quick Start

After installing, just say:

> "Help me initialize this project's Harness"

The `harness:init` skill auto-triggers and walks you through setup.
```

---

## 4. Keywords / Tags

```
harness, agent-engineering, devops, team, sprint, claude-code, hooks, memory, ai-engineering
```

---

## 5. Target Audience

- **Engineering teams**: Looking to standardize AI agent workflows across multiple projects
- **Full-stack engineers**: Using Claude Code for day-to-day development
- **Tech leads**: Coordinating sprint planning for multi-developer AI-assisted projects
- **Platform engineers**: Establishing AI engineering standards and constraint systems for their teams

---

## 6. Skills Overview (for Marketplace Display)

| Skill / Command | Trigger Scenario | Core Functionality |
|----------------|-----------------|-------------------|
| `harness:init` | New project setup | Generates full 6-layer Harness structure |
| `harness:audit` | Existing project audit | 7-dimension health score + prioritized fix plan |
| `harness:evolve` | Ongoing optimization | AGENTS.md trimming + hook adaptation |
| `harness:archive` | Post-feature archival | Spec archival + doc sync + architecture health check |
| `harness:canary` | Pre-deployment planning | Risk-scored canary runbook with staged rollout + rollback triggers |
| `harness:router` | Meta-skill (1% rule) | Intent recognition, auto-routes to the correct skill |
| `/harness:assign` | Sprint kickoff | Dependency graph analysis + optimal owner assignment |
| `/harness:review-pr` | Every PR | Quality + security + architecture review |
| `/harness:dump` | At 50% context usage | Cross-session progress persistence |
| `/harness:scan-arch` | Weekly | Architecture health scan |

---

## 7. Screenshot Descriptions

The following screenshots should be prepared for submission:

1. **harness:init output**: Shows the generated file tree after initialization (AGENTS.md, init.sh, hooks/)
2. **init.sh output**: Shows the Harness readiness check output after running `bash init.sh` (tool detection, progress display)
3. **harness:audit health report**: Shows the 7-dimension scoring table and prioritized fix plan
4. **/harness:assign results**: Shows the sprint allocation table and a snippet of the generated sprint-kickoff.sh
5. **AGENTS.md vs CLAUDE.md comparison**: Demonstrates the tool-agnostic architecture with both files

---

## 8. Technical Compatibility

| Environment | Support Status |
|-------------|---------------|
| Claude Code >= 1.0.0 | Fully supported |
| Cowork (Anthropic Desktop) | Supported (skill triggering) |
| TypeScript / Node.js projects | Dedicated template |
| Python projects | Dedicated template |
| Go projects | Dedicated template |
| Java projects | Dedicated template |
| Other languages | Generic template |

---

## 9. Privacy and Security Statement

- This plugin **does not collect any user data** and makes no network requests
- The `team_name` and `default_tech_stack` fields in `userConfig` are used locally only and stored securely by Claude Code
- All hook scripts are local shell scripts with fully auditable source code: [scripts/](../scripts/)
- No third-party MCP dependencies

---

## 10. Submission Checklist

Confirm before submitting:

- [x] `plugin.json` includes `name`, `version`, `homepage`, `repository`, `license`
- [x] `skills/`, `commands/`, `agents/`, `hooks/` are all in the plugin root directory
- [x] All internal plugin paths use `${CLAUDE_PLUGIN_ROOT}` instead of hardcoded absolute paths
- [x] `SKILL.md` contains valid YAML frontmatter (`name`, `description`)
- [x] Skills do not conflict with common tool names when used without the plugin prefix
- [x] LICENSE file is present (MIT)
- [x] README.md includes quick-start instructions
- [x] CHANGELOG.md documents version history
- [x] Plugin loading verified locally (`bash init.sh` output is normal)
