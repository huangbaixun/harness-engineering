# Changelog

## v1.10.1 (2026-04-18)

**Marketplace preparation + CodeBuddy removal**

- **Removed CodeBuddy support**: `.codebuddy-plugin/` directory removed, `CODEBUDDY.md` marked deprecated, all CodeBuddy references cleaned from Skills, Commands, Agents, templates, and docs. Plugin now targets Claude Code exclusively.
- **English-first documentation**: README.md, CONTRIBUTING.md, CHANGELOG.md, all 8 SKILL.md files, 9 Command files, 4 Agent files, architecture.md, and marketplace-submission.md translated to English. Chinese README preserved as `README.zh-CN.md`.
- **Plugin metadata in English**: plugin.json description, userConfig fields, and keywords; marketplace.json description and version bump.
- **New: harness:archive Skill** (P0-1): 4-step workflow — archive completed specs to `docs/archive/` (preserving git history via `git mv`), check doc-code consistency, run architecture health scan, generate structured archive report.
- **Enhanced: harness:plan** (P0-2): now enforces `<action>/<verify>/<done>` triple structure for every task. Reads `rigid` vs `flexible` constraints from `features.json` — rigid items must map to tasks, flexible items are advisory. 100% rigid constraint coverage check before execution.
- **Enhanced: session-start.sh** (P0-3): added features.json summary output (in-progress feature, next feature, stats) and 5-step ceremony chain checklist for Agent.
- **Expanded safety hooks**: `pre-protect-env` upgraded with comprehensive secret detection patterns (SSH keys, service accounts, .netrc, AWS credentials), dangerous command blocking (force-push, hard-reset, chmod 777, curl-pipe-to-shell), and inline secret detection.
- **Marketplace submitted**: v1.10.1 submitted to Anthropic Plugin Directory for review (Claude Code + Claude Cowork).

## v1.10.0 (2026-04-12)

**Unified `harness:` namespace**

- **Simplified plugin name**: `harness-engineering` → `harness`, so users see `harness:init` instead of `harness-engineering:harness-init`
- **Skills renamed**: harness-init → init, harness-audit → audit, harness-evolve → evolve, using-harness → router, writing-plans → plan, verification → verify (tdd unchanged)
- **Commands renamed**: standardized to `verb-noun` format: arch-scan → scan-arch, entropy-scan → scan-entropy, assign-features → assign, context-dump → dump, doc-sync → sync-docs, trim-claudemd → trim
- **Full reference update**: all SKILL.md cross-references, eval JSON, architecture.md, marketplace docs, README, CONTRIBUTING, and 36+ other files updated in sync
- **Breaking**: old slash commands (`/harness-init`, etc.) no longer work; use the new names (`/harness:init`, etc.)

## v1.9.3 (2026-04-12)

**Cross-platform hooks + upstream version tracking**

- **Cross-platform polyglot hook wrappers** (inspired by obra/superpowers `polyglot-hooks`):
  - Added `.cmd` polyglot entry for each hook script (valid as both CMD and bash); auto-detected by Windows Git Bash
  - `hooks.json` registration entries changed from `.sh` to `.cmd`
  - Kept `.sh` files for backward compatibility; added extensionless bash logic files (`.cmd` delegates to them)
  - On Windows, silently succeeds (exit 0) when bash is not found, avoiding workflow blocking
- **Upstream version tracking**: three workflow Skills (writing-plans / tdd / verification) now include `upstream` + `harness-delta` metadata in their headers, pinned to obra/superpowers @ `917e5f5`, documenting each Skill's delta from upstream
- Updated README: scripts directory description, cross-platform compatibility table

## v1.9.2 (2026-04-11)

**Superpowers workflow integration**

- Added `skills/writing-plans/`: pre-implementation planning Skill, triggered for tasks >30 min or touching 3+ files; outputs tasks.md with a human confirmation gate
- Added `skills/tdd/`: TDD workflow Skill (RED → GREEN → REFACTOR), bound to the 1% rule — automatically triggered on any code writing
- Added `skills/verification/`: pre-completion verification Skill with four-layer checks (Functional / Quality / Architecture / Integration)
- Added `scripts/session-start.sh`: SessionStart hook that reads `claude-progress.json` on session open, displaying in-progress tasks, to-do count, and blockers; triggers an archive reminder when completed items >= 10
- Updated `hooks/hooks.json`: registered `SessionStart` event
- Updated `skills/using-harness/SKILL.md`: added Steps 4-6 documenting trigger conditions for writing-plans / tdd / verification
- Updated `skills/harness-init/SKILL.md`: init artifact table and file structure diagram now include the three new Skills and session-start.sh
- Updated `docs/templates/generic/CLAUDE.md.template`: added "Workflow Skill auto-trigger" section
- Updated `references/HarnessEngineering.md`: added Section L (Superpowers Integration) with comparison table, integration points, full execution chain diagram, 14-Skill mapping; reference table now includes three new obra/superpowers entries

## v1.9.1 (2026-04-10)

**harness-init Phase 5: archive mechanism + features.json tiering strategy**

- Changed `features.json` positioning: from "optional for long-cycle projects" to "optional for solo / required for multi-person or multi-Agent"; init now auto-decides whether to generate it based on team size
- Added a two-file responsibility comparison table (who writes / what it records / token growth trend / multi-Agent conflict risk)
- Added extension field documentation for multi-person/multi-Agent scenarios (`owner`, `depends_on`, `files_owned`, `worktree`, `acceptance`)
- **Added archive mechanism**: triggers archiving when `completed_features` exceeds 10 entries, preventing token bloat (~8000 tokens after 6 months); init now also generates `docs/archive/` directory skeleton and archive strategy README
- Three archive rules written into AGENTS.md (archive threshold / done-entry compression strategy / Agent read-scope restriction)
- Added `docs/templates/generic/archive-readme.md.template`

## v1.9.0 (2026-04-10)

**Claude Marketplace support (Plan B)**

- **marketplace.json**: added `.claude-plugin/marketplace.json` for community marketplace subscription distribution. Users can subscribe with auto-updates via:
  ```
  /plugin marketplace add https://raw.githubusercontent.com/huangbaixun/harness-engineering/main/.claude-plugin/marketplace.json
  ```
- **plugin.json improvements**: added `homepage` and `repository` fields (required for official marketplace submission); added `userConfig` (`team_name`, `default_tech_stack`) — Claude Code prompts the user to fill these on enable, no manual configuration needed
- **${CLAUDE_PLUGIN_ROOT} path fix**: all internal path references in `harness-init` (template directory, init.sh.template) now use `${CLAUDE_PLUGIN_ROOT}` prefix, ensuring correct path resolution in marketplace cache mode
- **Init artifact table fix**: `.claude/hooks/` paths changed to `$TOOL_DIR/hooks/`, consistent with the tool-agnostic architecture
- **Keyword expansion**: `plugin.json` keywords now include `codebuddy`, `team`, `sprint` for better marketplace discoverability

## v1.8.0 (2026-04-08)

**Tool-agnostic architecture — full CodeBuddy compatibility**

- **AGENTS.md as cross-tool universal memory file** (ADR 0005):
  - Added `AGENTS.md`: unified memory file serving as the single source of truth for all project rules, readable by both Claude Code and CodeBuddy
  - `CLAUDE.md` reduced to a 2-line wrapper that directs Claude Code users to `AGENTS.md`
  - Added `CODEBUDDY.md`: 2-line wrapper that directs CodeBuddy users to `AGENTS.md`
- **Removed hardcoded tool paths**:
  - Added `.codebuddy-plugin/plugin.json`: CodeBuddy plugin manifest (v1.8.0)
  - `harness-init` Phase 2 six-layer table now uses `$TOOL_DIR` variable instead of hardcoded `.claude/`
  - `harness-init` Phase 3 file structure diagram updated to show dual-tool compatible layout with `AGENTS.md` hierarchy
  - `harness-audit` SKILL.md tool detection logic and memory file diagnostics adapted for multi-tool support (merged before v1.8.0)
- **Template updates**:
  - Added `docs/templates/generic/AGENTS.md.template`: includes `$TOOL_DIR` no-hardcode convention
  - `docs/templates/generic/init.sh.template` added 10-line tool detection block that auto-detects CodeBuddy / Claude Code and exports `$TOOL_DIR` and `$TOOL_NAME`
- **ADR 0005**: documents the tool-agnostic architecture decision, with three-option comparison and Agent constraint rules
- **docs/architecture.md** updated: reflects dual-tool compatible structure, directory diagram includes `.codebuddy-plugin/`, `CODEBUDDY.md`, `AGENTS.md`, and `references/team-parallel-development.md`

## v1.7.0 (2026-04-06)

**Multi-person collaboration + features.json lifecycle improvements**

- Added `/assign-features` command: sprint feature assignment planner inspired by superpowers `writing-plans`, five-phase workflow —
  - Phase 1: analyze features.json dependency graph, compute `startable` (all dependencies done?) and `criticality` (transitive closure block count)
  - Phase 2: auto-read CLAUDE.md `## Team Members` section; prompt and write back if missing
  - Phase 3: four-rule assignment algorithm (file conflict detection / load cap protection / critical path priority / layer affinity)
  - Phase 4: generate `sprint-kickoff.sh` with per-person sections containing git claim + worktree + Agent launch commands
  - Phase 5: append assignment records to `claude-progress.json` `sprint_history` for traceability
- Added `commands/evals/evals.json`: 4 command test cases (standard 3-person sprint, file conflict detection, dependency-unlock scheduling, overload protection)
- Added `references/team-parallel-development.md`: parallel development guide for multi-person full-stack teams, synthesizing Anthropic Agent Teams official docs, OpenAI Codex team practices, and a 16-Agent parallel stress test case study on a C compiler; covers features.json parallel field upgrades, Git Worktree isolation configuration, three division-of-labor models, and design principles for reducing human-Agent dependencies
- `harness-init` Phase 5 added features.json usage rules: "Agent read-only principle" and "cancel-don't-delete principle" (status=cancelled + cancelled_reason, never delete entries)

## v1.6.0 (2026-04-06)

**Methodology deepening + Skill TDD improvements**

- Added `references/HarnessEngineering.md`: comprehensive methodology handbook distilled from Anthropic, OpenAI, InfoQ, and Hacker News best practices, serving as the primary source for plugin design
- `harness-init` added **Phase 0 existing-project detection**: scans for existing CLAUDE.md before init, branching into new project / existing project / corrupted file paths; existing-project mode offers three options (incremental supplement / optimize and consolidate / full rebuild) with mandatory `.bak` backup before execution
- `harness-init` added **init artifact manifest**: lists all output files at the top of the Skill so users know what will be generated before triggering
- Added `docs/templates/generic/init.sh.template`: session startup script template that runs before each new Claude Code session, displaying progress/feature list/architecture doc entry points (inspired by walkinglabs/learn-harness-engineering harness-creator pattern)
- **Evals restructured**: split from a single file into per-skill directories, converted to skill-creator compatible format (with `assertions[]` array for objective grading by a grader subagent)
  - `skills/harness-init/evals/evals.json` (3 evals, including new existing-project detection case)
  - `skills/harness-audit/evals/evals.json` (1 eval)
  - `skills/harness-evolve/evals/evals.json` (1 eval)
  - `skills/using-harness/evals/evals.json` (2 evals)
  - `evals/agents/coding-agent.json` (3 evals)
  - `evals/evals.json` converted to an index file
- `README.md` added "Methodology Reference" section with artifact preview table after the quick-start second step
- `CLAUDE.md` added methodology handbook reference link

## v1.5.1 (2026-04-05)

- Fixed: release.yml version validation and tag matching (initial release correction)

## v1.5.0 (2026-04-05)

**Open-source preparation**

- Added `LICENSE` (MIT)
- Added `CONTRIBUTING.md`: Skill TDD contribution workflow, language template contribution guidelines, hook script conventions, PR format
- Rewrote `README.md`: targeted at first-time users, 3-step quick start, badges, collapsible file inventory
- Added `.github/workflows/release.yml`: auto-packages `.skill` and creates GitHub Release on semver tag, with manifest version validation
- Added `.github/workflows/validate.yml`: auto-validates plugin structure, manifest, hooks.json, and eval format on PR
- Added `.github/ISSUE_TEMPLATE/`: bug_report and feature_request templates
- Added `.github/PULL_REQUEST_TEMPLATE.md`: includes Skill TDD checklist

## v1.4.1 (2026-04-05)

- **Fixed**: removed path declaration fields from `plugin.json`, resolving "`agents: Invalid input`" loading error
- Relies on Claude Code auto-discovery of default directories; only metadata fields retained

## v1.4.0 (2026-04-05)

- **Changed**: restructured to comply with official Claude Code plugin spec
  - Manifest moved to `.claude-plugin/plugin.json`
  - `commands/`, `agents/`, `skills/` moved to plugin root
  - Hooks converted to `hooks/hooks.json` JSON registration format
  - Hook scripts migrated to `scripts/`, using `${CLAUDE_PLUGIN_ROOT}` path variable
  - `author` field changed to object format

## v1.3.0 (2026-04-05)

- Added `using-harness` meta-Skill (forced intent-recognition trigger, based on obra/superpowers 1% rule)
- Evals expanded to 9 test cases with 6 new stress tests
- `coding-agent` now embeds a two-stage mandatory review (Spec Compliance → Code Quality)

## v1.2.0 (2026-04-05)

- Added `coding-agent` (Sonnet model, long-cycle multi-session coding, per handbook Section F.4)
- Added Java language stack template (JUnit 5 + Mockito + Checkstyle + SpotBugs)
- Language templates expanded to five

## v1.1.0 (2026-04-05)

- Added `explore-agent` (Haiku model, context-efficient exploration subagent)
- Added `code-review-agent` (Sonnet model, code quality inferential sensor)
- Added `/entropy-scan` command (fourth-category garbage collection: code entropy detection)
- Added `plugin.json` version manifest

## v1.0.0 (2026-04-04)

- Initial release: three core Skills + seven Commands + five Hooks + multi-language templates + `security-reviewer`
