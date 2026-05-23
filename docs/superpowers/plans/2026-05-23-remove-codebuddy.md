# Remove CodeBuddy + AGENTS.md — v1.11.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collapse the tool-agnostic compatibility layer (AGENTS.md + CODEBUDDY.md wrapper + `$TOOL_DIR` indirection) back to a Claude-Code-only architecture, completing the cleanup that started in v1.10.1.

**Architecture:** Single PR / single logical change. 8 tasks ordered by blast radius: foundation (CLAUDE.md) → templates → skills → top-level docs → training → ADR evolution → release wiring → gate verification. Each task ends with a commit; intermediate states have stale doc references to AGENTS.md but no runtime breakage (markdown-link rot only).

**Tech Stack:** bash, grep, markdown, JSON. No build or test framework involved — refactor/cleanup only. Verification is grep-driven + manual `harness:init` dry run.

**Source spec:** `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md`

---

## Pre-flight: Tracked-State Guard (read first, do once)

Before Task 1, run this check. If any of the spec's target files are untracked, **stop and confirm with the user** before editing them — they may be in-flight work the spec mis-classified.

- [ ] **Pre-flight Step 1: Verify branch and clean working tree (for files we'll touch)**

Run:
```bash
git status --short -- \
  AGENTS.md CODEBUDDY.md CLAUDE.md \
  docs/templates/generic/ \
  skills/init/SKILL.md skills/archive/SKILL.md skills/verify/SKILL.md skills/audit/SKILL.md \
  docs/architecture.md README.md README.zh-CN.md \
  references/harness-evaluation-handbook.md \
  training/instructor-notes.md training/demo-script.md docs/training-plan-90min.md \
  docs/decisions/ \
  CHANGELOG.md .claude-plugin/plugin.json
```

Expected outcome:
- Most files should be unmodified (no `M` prefix).
- `references/harness-evaluation-handbook.md` and `docs/training-plan-90min.md` are currently **untracked** (`??`). Confirm with the user before treating them as part of this PR. If user says skip, mark Task 5 step on those files as N/A and document in the final PR description.

- [ ] **Pre-flight Step 2: Confirm `self-test.sh` does not exist**

Run:
```bash
test -f scripts/self-test.sh && echo "EXISTS" || echo "MISSING"
```

Expected: `MISSING`. The spec's Gate 3 lists `bash scripts/self-test.sh` — this command will be skipped (file does not exist in this repo as of 2026-05-23). The handbook's `score_selftest` line documents the gap. Note in PR description.

---

## Task 1: Migrate AGENTS.md → CLAUDE.md, delete legacy memory files

**Files:**
- Create / Overwrite: `CLAUDE.md` (root)
- Delete: `AGENTS.md` (root)
- Delete: `CODEBUDDY.md` (root)
- Delete: `docs/templates/generic/AGENTS.md.template`

- [ ] **Step 1: Overwrite root `CLAUDE.md` with the new canonical content**

The file currently contains a 2-line wrapper pointing to AGENTS.md. Replace its entire content with the following (≤ 60 lines):

```markdown
# Harness Engineering Plugin — CLAUDE.md

## Project Overview
Harness Engineering capability-building plugin: provides a standardized AI Agent Harness engineering framework for new project initialization and existing project optimization.

## Tech Stack
- Shell scripts (Hook templates and automation scripts)
- Markdown + JSON (Skills, Commands, configuration templates)
- Python 3.10+ (helper scripts: health scoring, architecture scanning)
- Multi-language templates: TypeScript, Python, Go, generic

## Key Commands
- Validate Skill structure: `find skills/ -name "SKILL.md" | head -20`
- Check JSON validity: `python3 -m json.tool docs/templates/*/features.json`

## Architecture Conventions
- Dependency direction: references → templates → skills → commands (reverse is prohibited)
- Every Skill's SKILL.md must include YAML frontmatter (name, description)
- All Hook scripts must follow the "silent on success, visible on failure" principle
- Placeholders in template files must use the `{{PLACEHOLDER}}` format

## Mandatory Skill Development Workflow
Any new or modified Skill must go through the skill-creator workflow — no exceptions:
1. Draft SKILL.md → 2. Write test cases in the corresponding `evals/evals.json` → 3. Run eval (with-skill vs baseline) → 4. Generate eval-viewer for human review → 5. Iterate based on feedback
- Eval file location: `skills/<name>/evals/evals.json`, format compatible with skill-creator
- Directly modifying and committing SKILL.md without eval validation is prohibited
- See: docs/decisions/0004-skill-creator-methodology.md

## Prohibited Practices
- Never hardcode specific project names or team information in templates
- Never generate a CLAUDE.md template exceeding 60 lines
- Never let Hook templates produce output on success
- Never exceed 500 lines in a single Skill file

## Further Context
- Architecture diagram: docs/architecture.md
- Design decisions: docs/decisions/
- Template directory: docs/templates/
- Methodology reference manual: references/HarnessEngineering.md (primary source)
- Concept quick reference: references/harness-engineering-handbook.md
- Architecture decision (Claude Code only): docs/decisions/0007-claude-code-only.md
```

Note the dropped items (intentional per spec §4.1):
- "Universal agent memory file" header line
- "Skills/Commands must not hardcode `.claude/` paths; use `$TOOL_DIR` instead" rule
- "Never hardcode `.claude/` paths in Skill content" prohibition
- `bash scripts/self-test.sh` command (file does not exist)

- [ ] **Step 2: Delete `AGENTS.md`, `CODEBUDDY.md`, and the `AGENTS.md.template`**

Run:
```bash
git rm AGENTS.md CODEBUDDY.md docs/templates/generic/AGENTS.md.template
```

- [ ] **Step 3: Verify line count and absence**

Run:
```bash
wc -l CLAUDE.md
test ! -f AGENTS.md && echo "AGENTS.md: absent ✓" || echo "AGENTS.md: still present ✗"
test ! -f CODEBUDDY.md && echo "CODEBUDDY.md: absent ✓" || echo "CODEBUDDY.md: still present ✗"
test ! -f docs/templates/generic/AGENTS.md.template && echo "template: absent ✓" || echo "template: still present ✗"
```

Expected:
- `wc -l CLAUDE.md` → number ≤ 60
- All three "absent ✓" messages

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
refactor: collapse AGENTS.md / CODEBUDDY.md into CLAUDE.md

Restore CLAUDE.md as the canonical project memory file. The
AGENTS.md + 2-line CLAUDE.md wrapper + CODEBUDDY.md wrapper pattern
(introduced in v1.8.0) is removed. v1.10.1 already deleted runtime
CodeBuddy support; this finishes the structural cleanup.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Update generic templates — remove `$TOOL_DIR` indirection

**Files:**
- Modify: `docs/templates/generic/CLAUDE.md.template`
- Modify: `docs/templates/generic/init.sh.template`

- [ ] **Step 1: Append the `features.json` rule to `CLAUDE.md.template`**

The deleted `AGENTS.md.template` had one rule that `CLAUDE.md.template` lacks. Migrate this single line.

Edit `docs/templates/generic/CLAUDE.md.template`. Find:
```
- 提交前必须通过质量检查（见 Stop Hook）
```

Replace with:
```
- 提交前必须通过质量检查（见 Stop Hook）
- 永远不要直接写入 `docs/features.json`（Agent 只读，变更记录至 claude-progress.json）
```

Do not migrate the `$TOOL_DIR` rule from the old AGENTS.md.template — that abstraction is being removed.

- [ ] **Step 2: Strip `TOOL_DIR` / `TOOL_NAME` exports from `init.sh.template`**

Edit `docs/templates/generic/init.sh.template`. Find:
```bash
# ── Claude Code 配置 ────────────────────────────────────────────────────────
export TOOL_DIR=".claude"
export TOOL_NAME="Claude Code"
# ────────────────────────────────────────────────────────────────────────────

PROJECT_NAME="{{PROJECT_NAME}}"
```

Replace with:
```bash
PROJECT_NAME="{{PROJECT_NAME}}"
```

- [ ] **Step 3: Update the banner line in `init.sh.template`**

Edit `docs/templates/generic/init.sh.template`. Find:
```bash
echo "  ${PROJECT_NAME} — Harness 就绪检查"
echo "  工具：${TOOL_NAME}（${TOOL_DIR}/）"
echo "════════════════════════════════════"
```

Replace with:
```bash
echo "  ${PROJECT_NAME} — Harness 就绪检查"
echo "  工具：Claude Code（.claude/）"
echo "════════════════════════════════════"
```

- [ ] **Step 4: Update the closing memory-file line in `init.sh.template`**

Edit `docs/templates/generic/init.sh.template`. Find:
```bash
echo "📐 架构文档：docs/architecture.md"
echo "📖 Agent 记忆：AGENTS.md（${TOOL_NAME} 通用）"
```

Replace with:
```bash
echo "📐 架构文档：docs/architecture.md"
echo "📖 Agent 记忆：CLAUDE.md"
```

- [ ] **Step 5: Verify**

Run:
```bash
grep -n "TOOL_DIR\|TOOL_NAME\|AGENTS\.md" docs/templates/generic/init.sh.template docs/templates/generic/CLAUDE.md.template
wc -l docs/templates/generic/CLAUDE.md.template
```

Expected:
- `grep` returns nothing (zero output)
- `wc -l` ≤ 60

- [ ] **Step 6: Commit**

```bash
git add docs/templates/generic/CLAUDE.md.template docs/templates/generic/init.sh.template
git commit -m "$(cat <<'EOF'
refactor(templates): drop \$TOOL_DIR indirection, anchor to CLAUDE.md

Removes the tool-detection block from init.sh.template and migrates
the one features.json-only rule that AGENTS.md.template had into
CLAUDE.md.template. Templates now reference .claude/ and CLAUDE.md
directly with no abstraction layer.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Clean `skills/` — drop AGENTS.md references

**Files:**
- Modify: `skills/init/SKILL.md` (heavy — 13+ edits)
- Modify: `skills/archive/SKILL.md` (1 edit)
- Modify: `skills/verify/SKILL.md` (1 edit)
- Modify: `skills/audit/SKILL.md` (5 edits — including memory-file detection)

### 3a. `skills/init/SKILL.md`

- [ ] **Step 1: Replace MEMORY_FILE detection block (lines ~50-56)**

Edit `skills/init/SKILL.md`. Find:
```bash
# Step 1: Set the Claude Code config directory
TOOL_DIR=".claude"
echo "Config directory: $TOOL_DIR"

# Step 2: Detect memory file (priority: AGENTS.md > tool-specific file)
MEMORY_FILE=$([ -f "AGENTS.md" ] && echo "AGENTS.md" \
           || echo "CLAUDE.md")

# Step 3: Check whether key files already exist
ls "$MEMORY_FILE" "$TOOL_DIR/settings.json" "$TOOL_DIR/hooks/" init.sh 2>/dev/null
[ -f "$MEMORY_FILE" ] && wc -l "$MEMORY_FILE"
```

Replace with:
```bash
# Check whether key files already exist
ls CLAUDE.md .claude/settings.json .claude/hooks/ init.sh 2>/dev/null
[ -f CLAUDE.md ] && wc -l CLAUDE.md
```

- [ ] **Step 2: Update "Existing Project Mode" wording (line ~73)**

Edit `skills/init/SKILL.md`. Find:
```
1. **Read and evaluate the existing memory file** (AGENTS.md / CLAUDE.md)
```

Replace with:
```
1. **Read and evaluate the existing CLAUDE.md**
```

- [ ] **Step 3: Update the user-prompt template (lines ~80-84)**

Edit `skills/init/SKILL.md`. Find:
```
   > "Detected an existing memory file `$MEMORY_FILE` (currently X lines). I can:
```

Replace with:
```
   > "Detected an existing `CLAUDE.md` (currently X lines). I can:
```

Then find:
```
   > C) **Full rebuild** — back up the existing file as `$MEMORY_FILE.bak` and regenerate
```

Replace with:
```
   > C) **Full rebuild** — back up the existing file as `CLAUDE.md.bak` and regenerate
```

- [ ] **Step 4: Update the backup command (lines ~87-89)**

Edit `skills/init/SKILL.md`. Find:
```bash
   cp "$MEMORY_FILE" "${MEMORY_FILE}.bak"
   echo "Backed up to ${MEMORY_FILE}.bak"
```

Replace with:
```bash
   cp CLAUDE.md CLAUDE.md.bak
   echo "Backed up to CLAUDE.md.bak"
```

- [ ] **Step 5: Update the six-layer memory row (line ~118)**

Edit `skills/init/SKILL.md`. Find:
```
| 1. Memory | `AGENTS.md` (universal) / `CLAUDE.md` | Static knowledge: architecture conventions, prohibited rules, test commands |
```

Replace with:
```
| 1. Memory | `CLAUDE.md` | Static knowledge: architecture conventions, prohibited rules, test commands |
```

- [ ] **Step 6: Remove the `$TOOL_DIR` footnote and three-part synergy line (lines ~125-127)**

Edit `skills/init/SKILL.md`. Find:
```
> `$TOOL_DIR` = `.claude/`, exported by init.sh at session startup.

**Three-part synergy principle**: AGENTS.md rules alone are occasionally ignored; Hooks alone cannot handle judgment-based tasks; settings.json alone lacks context. All three working together is what makes the system truly effective.
```

Replace with:
```
**Three-part synergy principle**: CLAUDE.md rules alone are occasionally ignored; Hooks alone cannot handle judgment-based tasks; settings.json alone lacks context. All three working together is what makes the system truly effective.
```

- [ ] **Step 7: Update the file manifest tree (lines ~140-143)**

Edit `skills/init/SKILL.md`. Find:
```
project-root/
├── AGENTS.md                     <- Universal memory file (<= 60 lines), read by all tools
├── CLAUDE.md                     <- 2-line wrapper -> points to AGENTS.md (includes workflow Skill trigger rules)
├── init.sh                       <- Session startup script (exports $TOOL_DIR)
```

Replace with:
```
project-root/
├── CLAUDE.md                     <- Project memory file (<= 60 lines, single source of truth)
├── init.sh                       <- Session startup script
```

- [ ] **Step 8: Remove the `$TOOL_DIR` reference in the .claude/ comment**

Edit `skills/init/SKILL.md`. Find:
```
├── $TOOL_DIR/
│   └── skills/
```

Replace with:
```
├── .claude/
│   └── skills/
```

- [ ] **Step 9: Replace the "single source of truth" note (line ~164)**

Edit `skills/init/SKILL.md`. Find:
```
> **Note**: `AGENTS.md` is the single source of truth. `CLAUDE.md` is only 2 lines, directing users to `AGENTS.md`.
```

Replace with:
```
> **Note**: `CLAUDE.md` is the single source of truth for project rules.
```

- [ ] **Step 10: Rename the writing-principles section (line ~168)**

Edit `skills/init/SKILL.md`. Find:
```
#### AGENTS.md Writing Principles

AGENTS.md is the Agent's "worldview" — it defines the Agent's foundational understanding of the project, read by all AI tools.
```

Replace with:
```
#### CLAUDE.md Writing Principles

CLAUDE.md is the Agent's "worldview" — it defines the Agent's foundational understanding of the project.
```

- [ ] **Step 11: Update the ≤60-line principle (line ~181)**

Edit `skills/init/SKILL.md`. Find:
```
**<=60-line principle**: ETH Zurich research shows that overly long AI-auto-generated memory files degrade performance and consume 20% more tokens. Only hand-written, concise files are truly effective. Move excess content into `docs/` subdirectories and link to them from AGENTS.md.
```

Replace with:
```
**<=60-line principle**: ETH Zurich research shows that overly long AI-auto-generated memory files degrade performance and consume 20% more tokens. Only hand-written, concise files are truly effective. Move excess content into `docs/` subdirectories and link to them from CLAUDE.md.
```

- [ ] **Step 12: Update the archive-rules write target (line ~274)**

Edit `skills/init/SKILL.md`. Find:
```
Write the following rules into AGENTS.md during initialization:
```

Replace with:
```
Write the following rules into CLAUDE.md during initialization:
```

- [ ] **Step 13: Update other `$TOOL_DIR` references throughout the file**

Run:
```bash
grep -n "\$TOOL_DIR" skills/init/SKILL.md
```

For each remaining match (excluding lines already updated above), replace `$TOOL_DIR/` with `.claude/`. Common patterns to expect:
- `$TOOL_DIR/settings.json` → `.claude/settings.json`
- `$TOOL_DIR/hooks/` → `.claude/hooks/`
- `$TOOL_DIR/skills/` → `.claude/skills/`
- `$TOOL_DIR/agents/` → `.claude/agents/`
- `$TOOL_DIR/commands/` → `.claude/commands/`

Use `Edit` with `replace_all: true` for each pattern if it appears multiple times.

- [ ] **Step 14: Verify `skills/init/SKILL.md` is clean**

Run:
```bash
grep -n "AGENTS\.md\|\$TOOL_DIR\|MEMORY_FILE" skills/init/SKILL.md
```

Expected: zero output.

### 3b. `skills/archive/SKILL.md`

- [ ] **Step 15: Update line 47**

Edit `skills/archive/SKILL.md`. Find:
```
   - Check each rule in CLAUDE.md / AGENTS.md one by one
```

Replace with:
```
   - Check each rule in CLAUDE.md one by one
```

### 3c. `skills/verify/SKILL.md`

- [ ] **Step 16: Update line 58**

Edit `skills/verify/SKILL.md`. Find:
```
   - Trigger the archival mechanism (see AGENTS.md archival rules)
```

Replace with:
```
   - Trigger the archival mechanism (see CLAUDE.md archival rules)
```

### 3d. `skills/audit/SKILL.md`

- [ ] **Step 17: Update the description frontmatter (line ~5)**

Edit `skills/audit/SKILL.md`. Find:
```
  "check Harness", "optimize CLAUDE.md", "optimize AGENTS.md", "Agent keeps making mistakes",
```

Replace with:
```
  "check Harness", "optimize CLAUDE.md", "Agent keeps making mistakes",
```

- [ ] **Step 18: Replace MEMORY_FILE detection block (lines ~27-30)**

Edit `skills/audit/SKILL.md`. Find:
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
```

Replace with:
```bash
# Check each of the six Harness layers
echo "=== 1. Memory Layer ===" && wc -l CLAUDE.md 2>/dev/null
echo "=== 2. Rules Layer ===" && cat .claude/settings.json 2>/dev/null
echo "=== 3. Skills Layer ===" && ls .claude/skills/ .claude/commands/ 2>/dev/null
echo "=== 4. Agents Layer ===" && ls .claude/agents/ 2>/dev/null
echo "=== 5. Hooks Layer ===" && grep -r "hooks" .claude/settings.json 2>/dev/null
echo "=== 6. Tools Layer ===" && grep -r "mcpServers" .claude/settings.json 2>/dev/null
```

- [ ] **Step 19: Update Step 3 section heading (line ~66)**

Edit `skills/audit/SKILL.md`. Find:
```
**A. Memory File (AGENTS.md / CLAUDE.md) Diagnostics**
```

Replace with:
```
**A. Memory File (CLAUDE.md) Diagnostics**
```

- [ ] **Step 20: Remove the "multiple files in sync" diagnostic (line ~75)**

Edit `skills/audit/SKILL.md`. Find:
```
[ ] Multiple files with inconsistent content? (AGENTS.md / CLAUDE.md should be in sync)
```

Replace with: (delete this line entirely — i.e., replace with empty string while preserving the surrounding checklist structure)

Use this exact replacement: find:
```
[ ] Contains outdated rules? -> Delete or flag
[ ] Multiple files with inconsistent content? (AGENTS.md / CLAUDE.md should be in sync)
```

Replace with:
```
[ ] Contains outdated rules? -> Delete or flag
```

### 3e. Verify and commit Task 3

- [ ] **Step 21: Verify all skills/ files are clean**

Run:
```bash
grep -rn "AGENTS\.md\|\$TOOL_DIR\|MEMORY_FILE" skills/
```

Expected: zero output.

- [ ] **Step 22: Commit**

```bash
git add skills/init/SKILL.md skills/archive/SKILL.md skills/verify/SKILL.md skills/audit/SKILL.md
git commit -m "$(cat <<'EOF'
refactor(skills): drop AGENTS.md / \$TOOL_DIR references

Skills now reference CLAUDE.md and .claude/ directly with no
indirection layer. harness:init and harness:audit had the heaviest
edits (memory-file detection logic removed); archive/verify each
needed a single one-line update.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Update top-level docs (architecture.md + READMEs)

**Files:**
- Modify: `docs/architecture.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

### 4a. `docs/architecture.md`

- [ ] **Step 1: Remove the "Tool-agnostic design" paragraph (line 7)**

Edit `docs/architecture.md`. Find:
```
This is an AI Agent Harness plugin that supports Claude Code and provides engineering teams with standardized AI Agent Harness engineering capabilities. It consists of three core Skills along with a set of supporting Commands, Hooks, and References.

**Tool-agnostic design**: `AGENTS.md` serves as the cross-tool universal memory file; `CLAUDE.md` is a 2-line wrapper; Skills use the `$TOOL_DIR` variable instead of hardcoded paths.
```

Replace with:
```
This is an AI Agent Harness plugin that targets Claude Code and provides engineering teams with standardized AI Agent Harness engineering capabilities. It consists of three core Skills along with a set of supporting Commands, Hooks, and References.
```

- [ ] **Step 2: Update the directory tree (lines 13-14)**

Edit `docs/architecture.md`. Find:
```
harness-engineering-plugin/
├── AGENTS.md                       ← Universal memory file (< 60 lines, single source of truth across tools)
├── CLAUDE.md                       ← 2-line wrapper → AGENTS.md (for Claude Code users)
├── .claude-plugin/
```

Replace with:
```
harness-engineering-plugin/
├── CLAUDE.md                       ← Project memory file (< 60 lines, single source of truth)
├── .claude-plugin/
```

- [ ] **Step 3: Update Skills directory comment (line 17)**

Edit `docs/architecture.md`. Find:
```
├── skills/                         ← Skills (universal, $TOOL_DIR agnostic)
```

Replace with:
```
├── skills/                         ← Skills
```

- [ ] **Step 4: Add ADR 0007 to the ADR tree (line 47)**

Edit `docs/architecture.md`. Find:
```
│   │   ├── 0004-skill-creator-methodology.md
│   │   └── 0005-tool-agnostic-agents-md.md  ← Tool-agnostic architecture decision
```

Replace with:
```
│   │   ├── 0004-skill-creator-methodology.md
│   │   ├── 0005-tool-agnostic-agents-md.md  ← Superseded by 0007
│   │   └── 0007-claude-code-only.md         ← Current architecture decision
```

- [ ] **Step 5: Update the templates comment (line 54)**

Edit `docs/architecture.md`. Find:
```
│       └── generic/                ← Language-agnostic generic templates (includes AGENTS.md.template)
```

Replace with:
```
│       └── generic/                ← Language-agnostic generic templates
```

- [ ] **Step 6: Update the Skill responsibilities table (line 70)**

Edit `docs/architecture.md`. Find:
```
| **harness:init** | Setting up Harness for a new project from scratch | Tech stack info, project description | AGENTS.md + Hooks + docs/ + $TOOL_DIR/settings.json |
```

Replace with:
```
| **harness:init** | Setting up Harness for a new project from scratch | Tech stack info, project description | CLAUDE.md + Hooks + docs/ + .claude/settings.json |
```

- [ ] **Step 7: Verify architecture.md is clean**

Run:
```bash
grep -n "AGENTS\.md\|\$TOOL_DIR\|Tool-agnostic" docs/architecture.md
```

Expected: zero output.

### 4b. `README.md` (English, 9 occurrences)

Each occurrence below is a single substitution. Use the exact `Edit` `old_string` → `new_string` shown.

- [ ] **Step 8: Compat table row 1 (line 55)** — Edit `README.md`. Find:
```
| `AGENTS.md` | Universal memory layer (<=60 lines), the single source of truth |
| `CLAUDE.md` | 2-line entry point for Claude Code, points to AGENTS.md |
```
Replace with:
```
| `CLAUDE.md` | Project memory layer (<=60 lines), the single source of truth |
```

- [ ] **Step 9: harness:init row (line 81)** — Find:
```
| **harness:init** | New project / "set up my Harness" | Generates complete 6-layer Harness structure (AGENTS.md + Hooks + templates) |
```
Replace with:
```
| **harness:init** | New project / "set up my Harness" | Generates complete 6-layer Harness structure (CLAUDE.md + Hooks + templates) |
```

- [ ] **Step 10: harness:evolve trigger (line 83)** — Find:
```
| **harness:evolve** | "AGENTS.md is too long" / after new model release | Memory file trimming + Hook adaptation + garbage collection |
```
Replace with:
```
| **harness:evolve** | "CLAUDE.md is too long" / after new model release | Memory file trimming + Hook adaptation + garbage collection |
```

- [ ] **Step 11: /harness:trim description (line 105)** — Find:
```
| `/harness:trim` | Trim AGENTS.md to <=60 lines | After new model release |
```
Replace with:
```
| `/harness:trim` | Trim CLAUDE.md to <=60 lines | After new model release |
```

- [ ] **Step 12: Templates blurb (line 129)** — Find:
```
- **Generic** -- Language-agnostic Harness skeleton (includes AGENTS.md template)
```
Replace with:
```
- **Generic** -- Language-agnostic Harness skeleton
```

- [ ] **Step 13: Compatibility matrix row (line 139)** — Find:
```
| AGENTS.md universal memory | Yes | Yes |
```
Replace with: (delete this row entirely — it's a compat-matrix row that no longer makes sense after dropping multi-tool support). Use a context-aware replacement: open the file, identify the surrounding compat table, and remove just this one row, keeping the rest of the table intact. If the table becomes meaningless (only this row was about multi-tool), remove the whole table — flag for human review.

- [ ] **Step 14: Single-source-of-truth bullet (line 164)** — Find:
```
- `AGENTS.md` <=60 lines, the single source of truth
```
Replace with:
```
- `CLAUDE.md` <=60 lines, the single source of truth
```

- [ ] **Step 15: Directory tree (line 197)** — Find:
```
├── AGENTS.md                             <- Universal memory file (single source of truth, <=60 lines)
```
Replace with:
```
├── CLAUDE.md                             <- Project memory file (single source of truth, <=60 lines)
```

- [ ] **Step 16: Templates description (line 239)** — Find:
```
│   └── templates/                        Five language stack templates (incl. AGENTS.md.template)
```
Replace with:
```
│   └── templates/                        Five language stack templates
```

### 4c. `README.zh-CN.md` (Chinese mirror)

Apply the same substitutions to the Chinese README. The lines are at the same numbers (55, 56, 81, 83, 105, 129, 139, 150, 197 from the spec grep).

- [ ] **Step 17: Apply Chinese-side substitutions (8 edits)**

Use `Edit` for each:

| Line | Find | Replace with |
|------|------|--------------|
| 55-56 | `\| ``AGENTS.md`` \| 通用记忆层（≤60 行），唯一真相来源 \|\n\| ``CLAUDE.md`` \| Claude Code 用户的 2 行入口，指向 AGENTS.md \|` | `\| ``CLAUDE.md`` \| 项目记忆层（≤60 行），唯一真相来源 \|` |
| 81 | `生成完整六层 Harness 结构（AGENTS.md + Hooks + 模板）` | `生成完整六层 Harness 结构（CLAUDE.md + Hooks + 模板）` |
| 83 | `「AGENTS.md 太长了」/ 新模型发布后` | `「CLAUDE.md 太长了」/ 新模型发布后` |
| 105 | `精简 AGENTS.md 至 60 行以内` | `精简 CLAUDE.md 至 60 行以内` |
| 129 | `语言无关的 Harness 骨架（含 AGENTS.md 模板）` | `语言无关的 Harness 骨架` |
| 139 | `\| AGENTS.md 通用记忆 \| ✅ \| ✅ \|` | (delete the row — same caveat as Step 13: if the row's parent table loses all meaning, flag for human review) |
| 150 | `- ``AGENTS.md`` ≤ 60 行，是唯一真相来源` | `- ``CLAUDE.md`` ≤ 60 行，是唯一真相来源` |
| 197 (if present) | `├── AGENTS.md` line in tree (mirror of English) | replace with `├── CLAUDE.md` mirror |

After all edits, the file should mirror the English README in structure.

- [ ] **Step 18: Verify both READMEs and architecture.md are clean**

Run:
```bash
grep -n "AGENTS\.md\|\$TOOL_DIR\|Tool-agnostic" README.md README.zh-CN.md docs/architecture.md
```

Expected: zero output.

- [ ] **Step 19: Commit Task 4**

```bash
git add docs/architecture.md README.md README.zh-CN.md
git commit -m "$(cat <<'EOF'
docs: update architecture + README for Claude-Code-only positioning

Drops AGENTS.md references and the tool-agnostic framing from
top-level docs. Updates the directory diagrams, the compat tables,
and the Skill responsibility tables to match the new architecture.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Clean training and reference materials

**Files:**
- Modify: `references/harness-evaluation-handbook.md` (currently **untracked** — verify with pre-flight Step 1; skip if user reserved it)
- Modify: `training/instructor-notes.md`
- Modify: `training/demo-script.md`
- Modify: `docs/training-plan-90min.md` (currently **untracked** — same caveat)

### 5a. `references/harness-evaluation-handbook.md`

- [ ] **Step 1: Remove the "跨工具兼容" eval block (lines 829-832)**

Edit `references/harness-evaluation-handbook.md`. Find:
```
# 跨工具兼容（满分 10）
has_agents_md = EXISTS(AGENTS.md) ? 5 : 0
no_hardcoded_paths = COUNT(skills/**/*.md GREP "\.claude/" or "\.codebuddy/") == 0 ? 5 : 0
score_vendor_neutral = has_agents_md + no_hardcoded_paths

```

Replace with: (delete the entire block including the trailing blank line — empty string)

Use Edit with the exact 5-line `old_string` above and an empty `new_string`.

After this edit, the scoring total in the handbook drops by 10. **Search for any "总分" / "total score" line that refers to this category and either subtract 10 or strike-through with a note.** Read 50 lines around line 829 to locate any total-score summary that needs updating.

### 5b. `training/instructor-notes.md`

- [ ] **Step 2: Update line 62**

Edit `training/instructor-notes.md`. Find:
```
> 第二个：用过 Claude Code、Cursor、CodeBuddy 这类——能在你 IDE 里直接写代码的——agentic 编程工具的，请举手。
```

Replace with:
```
> 第二个：用过 Claude Code、Cursor 这类——能在你 IDE 里直接写代码的——agentic 编程工具的，请举手。
```

### 5c. `training/demo-script.md`

- [ ] **Step 3: Update intro at line 66**

Edit `training/demo-script.md`. Find:
```
1. 打开 Claude Code（或 CodeBuddy / Cursor 等任意 agentic 工具）
```

Replace with:
```
1. 打开 Claude Code
```

- [ ] **Step 4: Remove the CodeBuddy FAQ row at line 421**

Edit `training/demo-script.md`. Read 5 lines around line 421 to see the table context. Find:
```
| "我们公司用通义灵码/CodeBuddy 不是 Claude，能用吗？" | AGENTS.md 是跨工具中性约定。Hook 在不同工具有不同 API 但概念相同。 |
```

Replace with: (delete the entire row — empty string for that line; preserve the surrounding table structure)

### 5d. `docs/training-plan-90min.md`

- [ ] **Step 5: Update line 65**

Edit `docs/training-plan-90min.md`. Find:
```
   - "用过 Claude Code、Cursor、CodeBuddy 这类 agentic 编程工具的，请举手"
```

Replace with:
```
   - "用过 Claude Code、Cursor 这类 agentic 编程工具的，请举手"
```

- [ ] **Step 6: Update line 499**

Edit `docs/training-plan-90min.md`. Find:
```
T=0:30  打开 Claude Code（或 CodeBuddy）
```

Replace with:
```
T=0:30  打开 Claude Code
```

### 5e. Verify and commit Task 5

- [ ] **Step 7: Verify**

Run:
```bash
grep -rln -i "codebuddy" --exclude-dir=.git --exclude=CHANGELOG.md --exclude="0005-*" .
```

Expected: zero output (CHANGELOG.md and the soon-to-be-superseded ADR 0005 are the only allowed remaining mentions).

- [ ] **Step 8: Commit**

```bash
git add references/harness-evaluation-handbook.md training/instructor-notes.md training/demo-script.md docs/training-plan-90min.md
git commit -m "$(cat <<'EOF'
docs(training): remove CodeBuddy mentions from training + handbook

Drops the "跨工具兼容" eval category from the harness evaluation
handbook and removes CodeBuddy from the agentic-tool examples in
the 90-min training and demo script.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

(If any of these files were untracked at pre-flight, only `git add` the ones the user authorized.)

---

## Task 6: ADR evolution — supersede 0005, add 0007, update index

**Files:**
- Modify: `docs/decisions/0005-tool-agnostic-agents-md.md` (add Superseded banner)
- Create: `docs/decisions/0007-claude-code-only.md`
- Modify: `docs/decisions/README.md`

- [ ] **Step 1: Add Superseded banner to ADR 0005**

Edit `docs/decisions/0005-tool-agnostic-agents-md.md`. Find:
```markdown
# ADR 0005：工具无关架构 — AGENTS.md 作为通用记忆文件
```

Replace with:
```markdown
> **⚠️ SUPERSEDED by [ADR 0007](0007-claude-code-only.md) — 2026-05-23**
> CodeBuddy 已于 v1.10.1 移除支持，本 ADR 论证的"工具无关架构"不再适用。
> 文件保留作为历史决策记录。

# ADR 0005：工具无关架构 — AGENTS.md 作为通用记忆文件
```

The rest of the file body remains unchanged per spec §3 row 18.

- [ ] **Step 2: Create ADR 0007**

Create new file `docs/decisions/0007-claude-code-only.md` with this exact content:

```markdown
# ADR 0007：Claude Code Only — 移除工具无关兼容层

- **状态**：Accepted（Supersedes [ADR 0005](0005-tool-agnostic-agents-md.md)）
- **日期**：2026-05-23
- **决策者**：huangbaixun

## 背景

[ADR 0005](0005-tool-agnostic-agents-md.md)（2026-04-08）在 Tencent CodeBuddy 是相关迁移目标时，选择了工具无关架构：以 `AGENTS.md` 作为跨工具通用记忆文件，`CLAUDE.md` 和 `CODEBUDDY.md` 退化为 2 行 wrapper，模板和 Skill 使用 `$TOOL_DIR` / `$TOOL_NAME` 间接层避免硬编码路径。

v1.10.1 release 已删除 `.codebuddy-plugin/` 目录与脚本侧的 CodeBuddy 支持。此时间接层失去对应收益，徒增三类成本：

1. **认知负担**：用户需理解 AGENTS.md / CLAUDE.md 双文件结构的同步关系
2. **维护成本**：Skill 内容编写需绕过路径硬编码，导致表达迂回
3. **文档复杂度**：README、架构图、培训材料都需要解释"为什么有两个记忆文件"

## 决策

`CLAUDE.md` 重新成为唯一 canonical memory file。删除 `AGENTS.md`、`CODEBUDDY.md`、`docs/templates/generic/AGENTS.md.template`、`$TOOL_DIR` / `$TOOL_NAME` 间接层。Plugin 定位明确为 **Claude Code marketplace 专用 plugin**。

## 后果

### 收益
- 用户认知负担降低：一个文件、一种路径
- Skill / Hook / 模板与 Claude Code 现实 1:1 对应，无抽象绕道
- 文档收敛，README 更易理解

### 已知成本
- 放弃 `AGENTS.md` 这个新兴行业标准（OpenAI Codex / Cursor / Aider 都读它）—— 未来若重新支持非 Claude 工具需新 ADR
- 已迁移到 `AGENTS.md` 的用户项目需自行回迁（plugin 不强制覆盖既有文件）

## 迁移

- 既有用户项目的 `AGENTS.md` 不被 plugin 触碰
- 新 `harness:init` 只生成 `CLAUDE.md`
- v1.11.0 CHANGELOG 标注 Breaking Change

## 相关

- Supersedes：[ADR 0005](0005-tool-agnostic-agents-md.md)
- 触发：v1.10.1 release（CodeBuddy 移除）
- 实现 spec：[2026-05-23-remove-codebuddy-design.md](../superpowers/specs/2026-05-23-remove-codebuddy-design.md)
```

- [ ] **Step 3: Update `docs/decisions/README.md` index**

Edit `docs/decisions/README.md`. Find:
```
| 0005 | 工具无关架构 — AGENTS.md 作为通用记忆文件 | 已接受 | 2026-04-08 |
```

Replace with:
```
| 0005 | 工具无关架构 — AGENTS.md 作为通用记忆文件 | Superseded by 0007 | 2026-04-08 |
| 0006 | Harness 评估系统 | 已接受 | 2026-05 |
| 0007 | Claude Code Only — 移除工具无关兼容层 | 已接受 | 2026-05-23 |
```

Note: ADR 0006 (`docs/decisions/0006-harness-evaluation-system.md`) is **currently untracked** in the working tree but already exists as a file. Include it in the index if the user confirms (pre-flight Step 1 should have flagged it). If user defers ADR 0006, only add the 0007 row.

- [ ] **Step 4: Verify ADR work**

Run:
```bash
test -f docs/decisions/0007-claude-code-only.md && echo "0007 created ✓"
head -3 docs/decisions/0005-tool-agnostic-agents-md.md
grep -n "0007\|Superseded" docs/decisions/README.md
```

Expected:
- `0007 created ✓`
- First line of 0005 starts with `> **⚠️ SUPERSEDED by`
- README.md grep shows both the 0005 "Superseded" cell and the 0007 row

- [ ] **Step 5: Commit**

```bash
git add docs/decisions/0005-tool-agnostic-agents-md.md docs/decisions/0007-claude-code-only.md docs/decisions/README.md
git commit -m "$(cat <<'EOF'
docs(decisions): supersede ADR 0005, add ADR 0007 Claude-Code-only

ADR 0005 retains its body but gains a Superseded banner. ADR 0007
documents the architectural reversion driven by the v1.10.1 CodeBuddy
removal: collapses AGENTS.md + double-wrapper + \$TOOL_DIR back to a
single canonical CLAUDE.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Release wiring — CHANGELOG v1.11.0 + plugin.json version

**Files:**
- Modify: `CHANGELOG.md` (prepend new section, do **not** touch historical entries)
- Modify: `.claude-plugin/plugin.json` (version bump)

- [ ] **Step 1: Prepend the v1.11.0 section to CHANGELOG**

Edit `CHANGELOG.md`. Read the first 20 lines to find the existing top header (likely `# Changelog` or similar) and the first entry (`## [1.10.1]` or `## [Unreleased]`).

Find the first existing version section, e.g.:
```markdown
## [1.10.1] — ...
```

Insert ABOVE it (do not replace):

```markdown
## [1.11.0] — 2026-05-23
**Breaking: Claude Code only — multi-tool compatibility layer removed**

- **Removed AGENTS.md as the canonical memory file**: `CLAUDE.md` once again
  becomes the single source of truth. The `AGENTS.md` + `CLAUDE.md` wrapper
  + `CODEBUDDY.md` wrapper pattern (introduced in v1.8.0) is removed.
- **Removed `$TOOL_DIR` / `$TOOL_NAME` indirection** from `init.sh.template`
  and `AGENTS.md.template` (template itself deleted). Templates now hardcode
  `.claude` / "Claude Code".
- **Documentation, training materials, and references** updated to reflect
  Claude-Code-only positioning.
- **ADR 0005 superseded** by new ADR 0007 ("Claude Code only").

Migration: existing user projects with their own `AGENTS.md` are not touched
by this plugin. New projects generated via `harness:init` will only produce
`CLAUDE.md`.

```

Use `Edit` with `old_string` = the existing first version section header line and `new_string` = the new v1.11.0 block followed by that same header line.

- [ ] **Step 2: Verify historical CHANGELOG entries are preserved**

Run:
```bash
grep -n "^## \[" CHANGELOG.md | head -10
grep -c "1.10.1\|1.8.0" CHANGELOG.md
```

Expected:
- Top entry is `## [1.11.0]`, followed by previous versions in descending order
- Both `1.10.1` and `1.8.0` strings still appear in the file (their historical entries are intact)

- [ ] **Step 3: Bump `.claude-plugin/plugin.json` version**

Edit `.claude-plugin/plugin.json`. Find:
```
  "version": "1.10.1",
```

Replace with:
```
  "version": "1.11.0",
```

- [ ] **Step 4: Verify JSON validity and version**

Run:
```bash
python3 -m json.tool .claude-plugin/plugin.json | head -5
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo "marketplace.json: valid ✓"
```

Expected:
- plugin.json parses; `"version": "1.11.0"` visible in output
- `marketplace.json: valid ✓`

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md .claude-plugin/plugin.json
git commit -m "$(cat <<'EOF'
release: v1.11.0 — Claude Code only, AGENTS.md removed

Marketplace plugin version bump and CHANGELOG entry documenting
the breaking removal of the multi-tool compatibility layer.
Historical v1.8.0 / v1.10.1 entries preserved.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Final verification — gates 1–4 + mandatory manual `harness:init` check

**Files:** none modified in this task (verification only).

### Gate 1 — Content residue (grep automation)

- [ ] **Step 1: Verify codebuddy mentions are confined**

Run:
```bash
grep -rli "codebuddy" --exclude-dir=.git .
```

Expected: only `./CHANGELOG.md` and `./docs/decisions/0005-tool-agnostic-agents-md.md` appear. Any other file is a fail — go back and edit.

- [ ] **Step 2: Verify AGENTS.md mentions are confined**

Run:
```bash
grep -rln "AGENTS\.md" --exclude-dir=.git .
```

Expected: only `./CHANGELOG.md`, `./docs/decisions/0005-tool-agnostic-agents-md.md`, `./docs/decisions/0007-claude-code-only.md`, and `./docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` and `./docs/superpowers/plans/2026-05-23-remove-codebuddy.md` (this plan itself). Any other file → fail.

- [ ] **Step 3: Verify $TOOL_DIR / $TOOL_NAME are gone from templates and skills**

Run:
```bash
grep -rn '\$TOOL_DIR\|\$TOOL_NAME' docs/templates/ skills/ commands/
```

Expected: zero output. (Note: `scripts/post-observe.sh` and `pre-protect-env.sh` use `TOOL_NAME` as a local var holding the Claude hook payload's `tool_name` field — unrelated to this cleanup, do **not** touch.)

- [ ] **Step 4: Verify CODEBUDDY remnants**

Run:
```bash
grep -rl "CODEBUDDY" --exclude-dir=.git .
```

Expected: only CHANGELOG.md and `docs/decisions/0005-*.md`.

### Gate 2 — Structure & rendering

- [ ] **Step 5: Verify line counts and absence**

Run:
```bash
wc -l CLAUDE.md docs/templates/generic/CLAUDE.md.template
python3 -m json.tool .claude-plugin/plugin.json | grep version
find docs/templates -name "AGENTS.md.template"
test ! -f AGENTS.md && test ! -f CODEBUDDY.md && echo "legacy files: absent ✓"
```

Expected:
- Both `wc -l` values ≤ 60
- JSON parse shows `"version": "1.11.0"`
- `find` returns nothing
- `legacy files: absent ✓`

### Gate 3 — Functional (manual `harness:init` is **MANDATORY**)

- [ ] **Step 6: Skip `bash scripts/self-test.sh`**

That script does not exist in this repo. Pre-flight Step 2 confirmed this. Document in PR description as a known gap (`score_selftest = 0` per the eval handbook).

- [ ] **Step 7: Render and run `init.sh.template`**

Run:
```bash
mkdir -p /tmp/harness-render-check
sed 's/{{PROJECT_NAME}}/test/g' docs/templates/generic/init.sh.template > /tmp/harness-render-check/init.sh
bash /tmp/harness-render-check/init.sh 2>&1 | tee /tmp/harness-render-check/output.txt
grep -c "CLAUDE.md" /tmp/harness-render-check/output.txt
grep -c "AGENTS.md\|TOOL_DIR\|TOOL_NAME" /tmp/harness-render-check/output.txt
```

Expected:
- Output ends with `Harness 就绪，可以开始会话 ✓`
- First grep returns ≥ 1 (the "Agent 记忆：CLAUDE.md" line)
- Second grep returns 0
- Cleanup: `rm -rf /tmp/harness-render-check`

- [ ] **Step 8: Manual `harness:init` dry run (MANDATORY)**

In a fresh scratch directory:

```bash
mkdir -p /tmp/harness-init-check && cd /tmp/harness-init-check
git init
# Trigger harness:init Skill in Claude Code with: "set up Harness for this project, generic / no tech stack details"
# Step through the prompts choosing minimal options
```

After the Skill completes, verify in `/tmp/harness-init-check/`:

```bash
test -f CLAUDE.md && echo "CLAUDE.md generated ✓" || echo "MISSING ✗"
test ! -f AGENTS.md && echo "AGENTS.md absent ✓" || echo "LEAKED ✗"
test ! -f CODEBUDDY.md && echo "CODEBUDDY.md absent ✓" || echo "LEAKED ✗"
grep -c "TOOL_DIR\|TOOL_NAME" init.sh 2>/dev/null || echo "0 (no init.sh or no leakage)"
```

Expected: all three `✓` messages, and grep returns `0`.

This gate is the spec's mandatory acceptance — if any check fails, return to the corresponding task and fix before declaring done. Cleanup: `rm -rf /tmp/harness-init-check`.

### Gate 4 — Link integrity

- [ ] **Step 9: Verify AGENTS.md links are dead-or-archival only**

Run:
```bash
grep -rE "\]\([^)]*AGENTS\.md\)" --exclude-dir=.git .
```

Expected: matches only in CHANGELOG.md, ADR 0005, ADR 0007 (as "Supersedes" reference), or in this plan/spec file. Any other match → fail.

- [ ] **Step 10: Verify ADR cross-links**

Run:
```bash
grep -rE "docs/decisions/0005" --exclude-dir=.git . | grep -v "^docs/decisions/0005"
grep -rE "docs/decisions/0007" --exclude-dir=.git . | grep -v "^docs/decisions/0007"
```

Expected:
- 0005 references: only in `docs/decisions/0007-claude-code-only.md` and `docs/decisions/README.md`
- 0007 references: in `CLAUDE.md`, `CHANGELOG.md`, `docs/decisions/README.md`, `docs/decisions/0005-*.md` (the banner), `docs/architecture.md`

### Definition of Done

- [ ] **Step 11: Final DoD checklist**

Verify against spec §6:

```bash
git diff --stat $(git log --reverse --format=%H | sed -n '1p')~..HEAD -- . | tail -5
git log --oneline | head -10
```

Expected:
- `git diff --stat` total: ~22 files (±2 tolerance per spec)
- `git log` shows 7 task-commits + 1 spec commit (`c381582`) at the top of history

Manual checks (read with eyes, no command):
- [ ] CHANGELOG historical entries (v1.8.0, v1.10.1) still appear in file
- [ ] commit messages follow the format `refactor: ...` / `docs(...): ...` / `release: v1.11.0 ...` (the `feat!` prefix from the spec is replaced by clearer per-task verbs — the **release** commit is the BREAKING-marker commit)
- [ ] Gate 3 Step 8 (`harness:init` dry run) was actually executed

- [ ] **Step 12: Final commit (only if any tweaks were made during gates)**

If any of the gates surfaced an issue that required a fix, commit those fixes as:

```bash
git add <fixed-files>
git commit -m "$(cat <<'EOF'
fix: address gate-verification findings in v1.11.0 cleanup

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Otherwise skip this step — Task 7 was the last functional commit.

---

## Out of scope (do not do as part of this plan)

- AGENTS.md industry-standard support (would be a separate ADR + feature)
- User-project migration scripts (plugin doesn't touch user files)
- Renaming Skills or restructuring templates beyond what's listed
- Creating `scripts/self-test.sh` (the eval handbook flags it as missing; that's a separate piece of work)
- Fixing the README compat-matrix tables if removing the AGENTS.md row leaves them looking awkward (flag for human review, don't restructure unilaterally)

---

## Plan Self-Review

**1. Spec coverage:** All 22 file changes in spec §3 are covered:
- §3 rows 1-3 (deletions) → Task 1 Step 2
- Row 4 (new CLAUDE.md) → Task 1 Step 1
- Rows 5-6 (templates) → Task 2
- Rows 7-10 (skills) → Task 3
- Rows 11-13 (architecture + READMEs) → Task 4
- Rows 14-17 (training/handbook) → Task 5
- Rows 18-20 (ADR work) → Task 6
- Rows 21-22 (release wiring) → Task 7
- Spec §5 gates 1-4 → Task 8

**2. Placeholder scan:** No `TBD` / `TODO` / "implement later". Every step shows the exact `old_string` and `new_string` or a complete code/markdown block to write.

**3. Type / name consistency:** `.claude/`, `CLAUDE.md`, `1.11.0`, `2026-05-23` used consistently across all tasks. `feat!` commit-message prefix from spec §6 was intentionally replaced with per-task verbs (`refactor:` / `docs(...):` / `release:`) — the `release:` commit is the natural BREAKING-marker commit, matching the repo's existing style (`release: v1.10.1 — marketplace prep, ...`).

**4. Gaps discovered during planning:**
- `scripts/self-test.sh` referenced by spec gate 3 does not exist → adjusted Task 8 Step 6 to explicitly skip and document, instead of failing
- `references/harness-evaluation-handbook.md` and `docs/training-plan-90min.md` are currently untracked → pre-flight Step 1 surfaces this for user authorization before edit
- Removing the AGENTS.md row from README compat tables may leave a single-row "table" → Steps 13 & 17 flag this for human review rather than restructuring unilaterally
- The handbook's "跨工具兼容（满分 10）" block is 4 lines, not just line 831 → Task 5 Step 1 specifies the full block

These gaps are now explicit in the plan; no spec amendment needed (the spec is a snapshot of intent — these are implementation-time discoveries).
