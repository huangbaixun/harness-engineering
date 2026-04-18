---
description: Initialize the full AI Agent Harness engineering system for the current project
---

Execute the Harness initialization workflow:

1. Detect the current project's tech stack (scan package.json / requirements.txt / go.mod / Cargo.toml, etc.)
2. Ask the user to confirm the tech stack information and project type
3. Follow the harness:init Skill workflow to generate the complete Harness structure based on the six-layer model:
   - CLAUDE.md (60 lines max)
   - .claude/settings.json (Hook registration + permission configuration)
   - .claude/hooks/ (Stop + PreToolUse + PostToolUse)
   - docs/architecture.md (100-150 line architecture diagram)
   - docs/decisions/README.md (ADR index)
   - docs/claude-progress.json (progress tracking skeleton)
4. Verify the completeness of all generated files
5. Output an initialization summary and "Week 1-2 observation items" recommendations
