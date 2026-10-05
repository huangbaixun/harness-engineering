---
name: harness:init
description: Initialize or adopt Harness Engineering for an explicitly requested Claude Code or Codex project, preserving existing instructions, configuration and permissions.
---

# Offline project adoption

Identify the actual host and choose one delivery: project-local resources or an
already installed plugin. Inspect existing instructions and configuration first.
Do not silently replace them, infer unknown test commands, install global settings
or enable external effects. Existing approved adoption is sufficient authorization
for the matching managed block; do not ask again merely because rules are long.

From the framework/runtime root preview the real initializer:

```sh
python3 scripts/harness_init.py --tool <codex|claude> --project <project> --delivery <project|plugin> --dry-run
```

Use --adopt-existing when appending/updating the managed instruction block was
requested. Inspect the plan and conflicts, then apply without --dry-run within the
approved scope. Conflicts outside the managed block fail before writes; preserve
existing settings, permission policies and custom verification commands. Do not
replace a project with generic scaffolding or trim rules to a fixed line quota.

Project delivery installs runtime and skills under `.agents/harness` / `.agents/skills`
for Codex, or `.claude/harness` / `.claude/skills` for Claude Code. Skill sibling layout,
helper executability, licenses and provenance must survive. Plugin delivery copies
no duplicate skill/runtime tree; resolve tools from the installed plugin root.

Both hosts use `.harness/config.json`, root features.json (proposed/building/done)
and a configured neutral checkpoint (default docs/harness-progress.json). Legacy
progress is read-only fallback. The initializer leaves verification_commands empty,
auto-commit and Issue sync disabled, and does not activate hooks or expand permissions.
Unknown checks are **unconfigured**, never verified. Configure only actual project
commands as argv arrays; execute and inspect them before claiming success.

Explicit verification: `python3 scripts/harness_runtime.py verify --project <project>`.
Explicit checkpoint: `python3 scripts/harness_state.py checkpoint --project <project>
--task <task> --next-action <next step>`. Resolve script paths from the selected runtime.
The compatibility codex_hook.py verify entrypoint uses the same verifier.

Optional native hooks require host trust and deliberate configuration; preserve
existing settings. Default plugin lifecycle uses bounded context and real configured
checks, not auto-commit, empty formatting or telemetry. A Stop hook does not intercept
git commit or certify completion. Direct-file protection supplements native permissions
and does not parse shell commands. Observe is opt-in event metadata, not cost measurement.

For Codex load references/platforms/codex.md only for relevant platform details.
Report files actually changed, checks actually run, conflicts and unverified host
loading. No credentials or network are required for initialization/local checks.
