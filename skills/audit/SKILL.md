---
name: harness:audit
description: >
  Health check and optimization for existing project Harness setups. Activate when the user mentions
  "check Harness", "optimize CLAUDE.md", "optimize AGENTS.md", "Agent keeps making mistakes",
  "Harness health", "audit Harness", "evaluate AI coding environment", "harness audit",
  "check Agent config", "why won't the Agent follow instructions", "improve Agent effectiveness",
  "add Harness to existing project", or "legacy optimization".
  Also use this Skill when the user complains that Agent behavior deviates from expectations,
  the Agent repeatedly makes the same mistakes, or the project has been around for a while
  but lacks a systematic Harness framework — diagnose and improve.
---

# Harness Health Audit Skill

> This Skill performs a systematic diagnosis of an existing project's Harness framework,
> identifies weak points, and provides concrete optimization recommendations.
> Core principle: **Build constraints around failure modes you have actually observed, not hypothetical ones.**

## Audit Process

### Step 1: Scan Current Harness State

Use an Explore subagent or directly scan the following files and directories:

```bash
# Claude Code config directory
TOOL_DIR=".claude"
MEMORY_FILE=$([ -f "AGENTS.md" ] && echo "AGENTS.md" || echo "CLAUDE.md")
echo "Detected tool config directory: $TOOL_DIR, memory file: $MEMORY_FILE"

# Check each of the six Harness layers
echo "=== 1. Memory Layer ===" && cat "$MEMORY_FILE" 2>/dev/null | wc -l
echo "=== 2. Rules Layer ===" && cat "$TOOL_DIR/settings.json" 2>/dev/null
echo "=== 3. Skills Layer ===" && ls "$TOOL_DIR/skills/" "$TOOL_DIR/commands/" 2>/dev/null
echo "=== 4. Agents Layer ===" && ls "$TOOL_DIR/agents/" 2>/dev/null
echo "=== 5. Hooks Layer ===" && grep -r "hooks" "$TOOL_DIR/settings.json" 2>/dev/null
echo "=== 6. Tools Layer ===" && grep -r "mcpServers" "$TOOL_DIR/settings.json" 2>/dev/null
echo "=== Documentation ===" && ls docs/ 2>/dev/null
echo "=== ADR ===" && ls docs/decisions/ 2>/dev/null
```

### Step 2: Seven-Dimension Health Score

Evaluate and score each dimension (0-3) based on the OpenAI Scorecard framework:

| Dimension | Evaluation Question | 0 Points | 1 Point | 2 Points | 3 Points |
|-----------|-------------------|----------|---------|----------|----------|
| **Bootstrap** | Can the Agent complete first-time setup and self-test without human intervention? | No automation | Partial scripts | Self-test but manual steps required | Fully automated |
| **Task Entry** | Are entry tasks clear and discoverable? | No navigation | CLAUDE.md has a list | Has Commands | Has Skills + Commands |
| **Validation** | Can CI/tests automatically validate Agent output? | No tests | Manual testing | CI has tests | CI + Hooks auto-validate |
| **Lint Gates** | Do format checks run automatically on pre-commit? | No checks | Exists but manual | pre-commit | PostToolUse Hook |
| **Repo Map** | Does the repo have a clear domain architecture diagram? | No docs | README | architecture.md | arch.md with dependency rules |
| **Structured Docs** | Are design docs structured with cross-links? | No docs/ | Exists but scattered | Has structure | Structured + cross-linked |
| **Decision Records** | Are architecture decisions recorded and maintained as ADRs? | No ADR | Exists but outdated | Exists and updated | Exists with deprecation records |

**Score Interpretation**:
- 0-7: RED — Fundamentals missing; recommend using harness:init to build from scratch
- 8-14: YELLOW — Has a foundation but weak; focus on strengthening the lowest-scoring dimensions
- 15-21: GREEN — Good shape; move to fine-tuning and optimization

### Step 3: Identify Failure Modes

Check the following common failure modes and generate a diagnostic report:

**A. Memory File (AGENTS.md / CLAUDE.md) Diagnostics**

```
Checklist:
[ ] Line count exceeds 60? -> Needs trimming
[ ] Contains rules the Agent already follows naturally? -> Remove redundant rules
[ ] Contains vague, unverifiable rules (e.g., "write good code")? -> Replace with specific, verifiable rules
[ ] Contains rules that should be enforced by Hooks but are in the memory file? -> Migrate to Hooks
[ ] Contains outdated rules? -> Delete or flag
[ ] Multiple files with inconsistent content? (AGENTS.md / CLAUDE.md should be in sync)
```

**B. Hook Coverage Diagnostics**

```
Checklist:
[ ] Is there a Stop Hook for quality gates? -> Highest priority
[ ] Is there a PreToolUse Hook to protect sensitive files? -> Security essential
[ ] Is there a PostToolUse Hook for auto-formatting? -> Consistency guarantee
[ ] Are Hooks silent on success? -> Output pollutes context
[ ] Do Hooks use the correct exit code on failure (exit 2)? -> Affects feedback loop
```

**C. Context Health Diagnostics**

```
Checklist:
[ ] Baseline cost (new session) < 20k tokens?
[ ] CLAUDE.md size < 2000 tokens?
[ ] Total MCP tool tokens < 20k?
[ ] Too many MCP Server connections? -> Connect on demand
[ ] Is test output silent on success?
```

**D. Architecture Constraint Diagnostics**

```
Checklist:
[ ] Are there explicit dependency direction rules?
[ ] Are dependency rules automatically validated (Linter / structural tests)?
[ ] Is there an architecture.md documenting module boundaries?
[ ] Are architecture violations caught in CI?
```

**E. Documentation System Diagnostics**

```
Checklist:
[ ] Does architecture.md exist and match the code? -> Check directory structure
[ ] Is the ADR index complete? -> Check decisions/README.md
[ ] Are there ADRs with "deprecated" status? -> This matters
[ ] Is progress tracking using JSON format?
```

### Step 4: Generate Optimization Plan

Sort issues by "frequency x severity" and output a structured optimization plan:

```markdown
## Harness Health Report

### Current Score: XX / 21

### RED — Immediate Action (This Week)
1. [Problem description] -> [Specific fix steps]
2. ...

### YELLOW — Complete This Month
1. [Problem description] -> [Specific fix steps]
2. ...

### GREEN — Continuous Improvement
1. [Problem description] -> [Specific fix steps]
2. ...
```

### Step 5: Execute Optimization

If the user agrees, execute the optimization directly:

1. **Trim CLAUDE.md**: Remove redundant rules, keep core constraints
2. **Add Hooks**: Generate missing Hook scripts based on diagnostics
3. **Establish documentation system**: Create architecture.md, ADR directory
4. **Configure settings.json**: Register Hooks, set permissions
5. **Submit optimization PR**: One commit per fix for easy rollback

### Step 6: Establish Continuous Improvement Cadence

Set up a "weekly Harness maintenance ritual" for the project:

1. **Failure analysis (10 min)** — Review Agent failures from the past week; convert each failure into a Harness improvement
2. **Documentation freshness check (5 min)** — Confirm CLAUDE.md and docs/ contain no stale rules
3. **Cost baseline comparison (5 min)** — Compare this week's vs last week's token usage trends
4. **Harness trimming (as needed)** — As models update, evaluate and remove scaffolding that is no longer necessary

Recommend setting up `/harness:sync-docs` and `/harness:scan-arch` scheduled tasks to automate these checks.

## Validation Framework

During audits, pay special attention to whether both "feedforward + feedback" controls are in place:

**Guides (Feedforward Control)**: Steer the Agent before it acts
- CLAUDE.md architecture conventions -> Computational Guide
- Skills domain knowledge injection -> Inferential Guide

**Sensors (Feedback Control)**: Validate after the Agent acts
- Stop Hook type checking -> Computational Sensor
- Security review Sub-agent -> Inferential Sensor

Principle: Cover 80% of common issues with Computational approaches first, then use Inferential approaches for the remaining 20% that require semantic understanding.
