# Harness Engineering Plugin — Architecture Diagram

## System Overview

This is an AI Agent Harness plugin that supports Claude Code and provides engineering teams with standardized AI Agent Harness engineering capabilities. It consists of three core Skills along with a set of supporting Commands, Hooks, and References.

**Tool-agnostic design**: `AGENTS.md` serves as the cross-tool universal memory file; `CLAUDE.md` is a 2-line wrapper; Skills use the `$TOOL_DIR` variable instead of hardcoded paths.

## Directory Structure

```
harness-engineering-plugin/
├── AGENTS.md                       ← Universal memory file (< 60 lines, single source of truth across tools)
├── CLAUDE.md                       ← 2-line wrapper → AGENTS.md (for Claude Code users)
├── .claude-plugin/
│   └── plugin.json                 ← Claude Code plugin manifest
├── skills/                         ← Skills (universal, $TOOL_DIR agnostic)
│   ├── init/               ← New project Harness initialization
│   │   └── SKILL.md
│   ├── audit/              ← Existing project health check and optimization
│   │   └── SKILL.md
│   └── evolve/             ← Continuous iterative improvement
│       └── SKILL.md
├── commands/                       ← Slash Commands (universal)
│   ├── assign.md          ← /harness:assign (team feature assignment)
│   ├── init.md
│   ├── audit.md
│   ├── review-pr.md
│   ├── dump.md
│   ├── sync-docs.md
│   ├── scan-arch.md
│   └── trim.md
├── hooks/                          ← Hook template scripts (universal)
│   ├── stop-typecheck.sh
│   ├── pre-protect-env.sh
│   ├── post-format.sh
│   ├── stop-commit-progress.sh
│   └── post-observe.sh
├── docs/
│   ├── architecture.md             ← This file
│   ├── decisions/                  ← ADR (Architecture Decision Records)
│   │   ├── README.md
│   │   ├── 0001-skill-based-architecture.md
│   │   ├── 0002-multi-language-templates.md
│   │   ├── 0003-dogfooding-harness.md
│   │   ├── 0004-skill-creator-methodology.md
│   │   └── 0005-tool-agnostic-agents-md.md  ← Tool-agnostic architecture decision
│   ├── design/
│   │   └── skill-interaction-flow.md
│   └── templates/                  ← Multi-language project templates
│       ├── typescript/
│       ├── python/
│       ├── go/
│       └── generic/                ← Language-agnostic generic templates (includes AGENTS.md.template)
├── references/                     ← Reference documents (loaded on demand)
│   ├── harness-engineering-handbook.md
│   ├── hook-patterns.md
│   ├── anti-patterns.md
│   └── team-parallel-development.md ← Multi-person collaboration and features.json team design
└── scripts/                        ← Helper scripts
    ├── self-test.sh
    ├── health-score.py
    └── generate-harness.sh
```

## Core Skill Responsibilities

| Skill | Trigger Scenario | Input | Output |
|-------|-----------------|-------|--------|
| **harness:init** | Setting up Harness for a new project from scratch | Tech stack info, project description | AGENTS.md + Hooks + docs/ + $TOOL_DIR/settings.json |
| **harness:audit** | Evaluating and optimizing an existing project | Existing codebase | Health report + optimization recommendations + fix PR |
| **harness:evolve** | Continuous iterative improvement | Failure logs, model updates | Harness simplification/enhancement suggestions + automated maintenance |

## Layer Dependency Rules

Allowed dependency direction (references may only flow to the right):

```
references → templates → skills → commands
```

Prohibited:
- Commands must not directly reference references (must go through skills)
- Templates must not reference skills (templates are static resources consumed by skills)
- Hooks are standalone deterministic scripts with no dependency on skills or commands
