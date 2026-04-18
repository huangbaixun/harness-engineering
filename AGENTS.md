# Harness Engineering Plugin — AGENTS.md

> Universal agent memory file. Supports Claude Code (reads CLAUDE.md)
> and all AI coding tools compatible with AGENTS.md. Content is identical across tools.

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
- Run self-tests: `bash scripts/self-test.sh`

## Architecture Conventions
- Dependency direction: references → templates → skills → commands (reverse is prohibited)
- Every Skill's SKILL.md must include YAML frontmatter (name, description)
- All Hook scripts must follow the "silent on success, visible on failure" principle
- Placeholders in template files must use the `{{PLACEHOLDER}}` format
- Skills/Commands must not hardcode `.claude/` paths; use `$TOOL_DIR` instead

## Mandatory Skill Development Workflow
Any new or modified Skill must go through the skill-creator workflow — no exceptions:
1. Draft SKILL.md → 2. Write test cases in the corresponding `evals/evals.json` → 3. Run eval (with-skill vs baseline) → 4. Generate eval-viewer for human review → 5. Iterate based on feedback
- Eval file location: `skills/<name>/evals/evals.json`, format compatible with skill-creator
- Directly modifying and committing SKILL.md without eval validation is prohibited
- See: docs/decisions/0004-skill-creator-methodology.md

## Prohibited Practices
- Never hardcode specific project names or team information in templates
- Never generate an AGENTS.md template exceeding 60 lines
- Never let Hook templates produce output on success
- Never exceed 500 lines in a single Skill file
- Never hardcode `.claude/` paths in Skill content

## Further Context
- Architecture diagram: docs/architecture.md
- Design decisions: docs/decisions/
- Template directory: docs/templates/
- Methodology reference manual: references/HarnessEngineering.md (primary source)
- Concept quick reference: references/harness-engineering-handbook.md
- Multi-tool compatibility decision: docs/decisions/0005-tool-agnostic-agents-md.md
