# Changelog

## v2.2.1 (2026-08-23)

**修复：GHE 主机路由 —— 所有非 github.com 项目的同步 100% 失败且被谎报为网络问题**

由 aiops（catl.ghe.com）接入时实测暴露。

- **根因**：`gh()` 给**每个** gh 子命令都追加 `--hostname`，但该 flag 只有 `gh auth`
  系子命令认。`gh issue` / `gh label` 一律报 `unknown flag: --hostname` 并退出 1，
  于是 `list_issues` / `list_labels` / `ensure_labels` / `issue create` / `issue edit`
  无一例外失败。改为在继承 `os.environ` 的基础上叠加 `GH_HOST`（继承是必需的：
  覆盖式 env 会让子进程丢掉 PATH 与凭据缓存路径）。
- **为什么藏了一整个版本**：`host` 命中 `github.com` 白名单时走的是不加 flag 的分支，
  **在 github.com 上做多少次真实试跑都覆盖不到 GHE 分支**。v2.2.0 的「真实试跑」正是
  只跑了 github.com。
- **比失败本身更糟的是分类**：`unknown flag` 落入 `_classify` 兜底，被显示成
  「网络不可达，同步已跳过；下次会话自动重试」。那句话在语义上是安抚 —— 它让人停止排查。
  用户开了 `github.enabled` 后只会看到一行假的网络提示，永远不成功，也永远看不出真实原因。

**连带收紧的两处（同一因，不只治标）：**

- `_classify` 新增 `usage` 类（`unknown flag` / `unknown command` / `unknown shorthand`）
  → 「gh 调用参数有误，重试不会自愈，请提交 bug」。
- **兜底不再冒充网络问题**。未识别的 stderr 改为照实说分不出类，并原样带出 gh 原文。
  否则任何不可自愈的故障都会被包装成可自愈的样子而永久静默 —— 这个 bug 一半的寿命来自这里。

**测试（约束下沉到桩，而非写进 checklist）：** `stubs/gh-stub` 现在像真 gh 一样，
对非 auth 子命令的 `--hostname` 直接报 `unknown flag` 并退出 1 —— 任何离线测试踩到
这条路径都立刻红，不依赖谁记得去跑 GHE 真实试跑（CI 里也跑不了，GHE 不可达）。
新增 `scripts/tests/test-harness-sync-ghe-host.sh`（单元断言命令行无 `--hostname`、
`GH_HOST` 正确、env 继承 PATH；GHE 端到端 push 成功；usage 与兜底均不谎报网络），
`test-harness-sync-failures.sh` 失败矩阵加 `usage` 一行。测试套 8 → 9，全绿；
反验证：补丁回退后新测试立刻转红。

**无 schema / 契约变更**，features.json 与 Issue 格式不受影响。

## v2.2.0 (2026-08-23)

**features.json ↔ GitHub/GHE Issue 双向同步（F005）+ schema 漂移对齐（F004）**

设计见 `docs/specs/2026-08-22-features-github-sync-design.md`，架构决策见
ADR-0011（字段所有权 / schema 2.1）与 ADR-0012（features.json 规范位置）。

**核心性质：冲突面 = 空集。** 每个字段恰好一个写方 —— rigid 约束
（acceptance_criteria / out_of_scope / status）归 harness，产品决策
（priority / assignee / milestone / delivery_state）归 GitHub。由此对账退化为
无状态纯函数，不需要时间戳、content hash 或三方合并，也不需要冲突合并 UI。

- **`status` 拆为两个正交维度**：`status`（harness 单写，工程进度）与
  `delivery_state`（GitHub 单写，产品决策）。`status=done` + `delivery_state=wontfix`
  （做完了但决定不发）在单字段下无法表达。
- **两个 hook 触点**：SessionStart 拉（硬超时 5s）、Stop 推。编辑热路径零网络，
  闸门链断网完整可跑。
- **推送幂等**：PATCH 前先比对托管区块，内容一致则不写。每次 PATCH 都会通知所有
  watcher，一个会话推 5 次就是 5 封邮件轰炸 PM —— 幂等不是优化而是可用性前提。
- **托管区块**：Issue body 仅 `harness:begin/end` 之间由 harness 管理，
  区块外的人类讨论逐字节保全。
- **入站路径**：带 `harness/track` 的 Issue 收为 `proposed` stub，由 brainstorming
  补齐结构 —— PM 在 GHE 提的需求能真正流进闸门链。不带该标签的日常 bug 单不被卷入。
- **label 命名空间隔离**：只增删 `harness/` 前缀；`P0/P1/P2` 与 `state/*` 只读。
- **opt-in**：未配置 `github.enabled` 时零网络、零开销。模板默认 `enabled: false`。
- **凭据零接触**：全部走 `gh auth`，仓库、配置、环境变量中不出现 token。

**新增：** `scripts/harness_sync.py`（pull/push/status）、Stop hook 三元组
`stop-sync-issues`、`/harness:sync-issues` 命令、`scripts/tests/` 五套离线测试
（gh 经 `$HARNESS_GH_BIN` 注入桩）。

**F004 —— schema 漂移对齐（前置）：** 原以为是三处 v1→v2 残留，实为两套约定并存
且从未裁定规范；实际影响 13 个文件。ADR-0012 裁定根目录为规范、`docs/` 为永久回退。
其中 `scripts/session-start` 的特性摘要段此前**从未生效过**（路径错、枚举错，
且整段被 `claude-progress.json` 是否存在卡死），`skills/init/SKILL.md` 展示给用户的
样板是完整 v1 schema —— 每个新项目都会照它建错。

**兼容性：** schema 2.1 新增字段全部可选，2.0 文件不加字段照常工作且不被同步逻辑
改动。Python 兼容下调至 3.7+（macOS 系统自带 3.9，插件不能要求用户升级解释器）。

Migration：无。未配置 `github` 块的项目行为完全不变。

## v2.1.0 (2026-08-22)

**Upstream sync: superpowers v5.1.0 → v6.3.0**

All 13 vendored skills re-taken verbatim from `obra/superpowers` v6.3.0 (SHA `b36e082`). Each `SKILL.md` now differs from upstream by exactly the 2 edits ADR-0009 allows; `scripts/sync-superpowers.sh` reports `diff-lines=2` across the board.

Notable upstream behavior changes now in effect:
- **`brainstorming` classifies requests as spike / bounded / architectural.** Ceremony scales to the task — only the architectural path writes a spec file. The approval gate before implementation fires on all three paths and never scales down.
- **`subagent-driven-development` reworked** (281 → 570 lines): one task review per task covering spec compliance *and* code quality (replacing the two sequential per-task reviews), a whole-branch review at the end, plans carrying a `Spec:` pointer, batched dispatch for small same-shape tasks, recorded circuit-breaker rulings instead of stalling on plan conflicts, and a no-nested-subagents contract for implementers and reviewers.
- **`writing-skills`: "Claude Search Optimization (CSO)" is now "Skill Discovery Optimization (SDO)"**, plus new "Match the Form to the Failure" and wording micro-test sections.
- **`writing-plans`** gains `Spec:`, `Global Constraints`, per-task `Interfaces` blocks, and a Task Right-Sizing section.
- **`using-git-worktrees`** drops the legacy `~/.config/superpowers/worktrees/` path and renumbers its steps.
- **`finishing-a-development-branch`** no longer reaches for `git worktree remove --force` when a tree holds uncommitted work — it stops and names the files.

**Companion files now vendored (ADR-0009 amended).** The v5.1.0 vendor silently dropped the files upstream ships next to its skills, leaving live links in our `SKILL.md` bodies pointing at nothing. 26 companion files are now carried byte-for-byte: `brainstorming/{visual-companion.md, spec-document-reviewer-prompt.md, scripts/}`, `requesting-code-review/code-reviewer.md`, `systematic-debugging/{root-cause-tracing.md, defense-in-depth.md, condition-based-waiting.md, …}`, `subagent-driven-development/{implementer-prompt.md, task-reviewer-prompt.md, re-review-prompt.md, scripts/}`, `test-driven-development/writing-good-tests.md`, `writing-plans/plan-document-reviewer-prompt.md`, `writing-skills/{testing-skills-with-subagents.md, persuasion-principles.md, anthropic-best-practices.md, graphviz-conventions.dot, render-graphs.js, examples/}`. Companions take **zero** edits and are inventoried in each `UPSTREAM.md`.

**Other changes:**
- `harness-delta.md` updated for the skills whose upstream semantics moved: `brainstorming` (path-to-gate mapping table), `subagent-driven-development` (`Spec:` pointer gate, circuit-breaker rulings must reach features.json, corrected review-order hint), `writing-plans` (`Spec:` field + Global Constraints carry CLAUDE.md project rules), `writing-skills` (SDO rename, line-cap scoping, micro-tests sit inside ADR-0004 step 3, not instead of it).
- `finishing-a-development-branch`'s `description:` reverted to upstream — the v5.1.0 vendor had extended it, which was outside the 2 allowed edits and undocumented.
- **CLAUDE.md**: the ≤500-line SKILL.md cap now reads as harness-original-only. Upstream's `writing-skills` (681 lines) and `subagent-driven-development` (570) exceed it by upstream's choice, and trimming them would break the verbatim guarantee.
- **`scripts/sync-superpowers.sh`** now also checks companion files, reporting three states: changed upstream, missing locally, orphaned here after upstream deleted it.
- **Evals refreshed** for the three skills whose harness-delta semantics moved: `brainstorming` (3 → 5; bounded path writes no spec, out_of_scope/layer-reversal upgrades the path), `writing-skills` (3 → 5; companion vendoring, line-cap pressure test, SDO terminology), `subagent-driven-development` (2 → 5; missing `Spec:` pointer blocks, scope-changing rulings reconcile to features.json, no nested subagents).
- **ADR-0009 amended** (2026-08-22) — "exactly four files" becomes "four harness files plus upstream companions".

Not adopted: `using-superpowers` stays un-vendored (harness ships `using-harness`), so the `../using-superpowers/references/*` links in upstream bodies are inert here. Those files document Codex / Gemini CLI runtimes and ADR-0007 scopes this plugin to Claude Code; recorded per-skill under "deliberately did NOT adopt" rather than patched.

Migration: none. No skill names, command names, or file paths changed.

## v2.0.0 (2026-05-23)

**Breaking: superpowers v5.1.0 vendor integration**

- **All 19 skills now under the `harness:` namespace.** End state: 13 vendored from `obra/superpowers` v5.1.0 (each with a `harness-delta.md` + `UPSTREAM.md` + `evals/evals.json` sidecar per ADR-0009) + 6 harness-original.
- **4 forks renamed back to upstream names** (replaces v1.10.0's short-name renames):
  - `harness:plan` → `harness:writing-plans`
  - `harness:tdd` → `harness:test-driven-development`
  - `harness:verify` → `harness:verification-before-completion`
  - `harness:router` → `harness:using-harness` (kept as harness-original; absorbs the upstream `using-superpowers` role)
- **10 new vendored skills:** `brainstorming`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `using-git-worktrees`, `writing-skills`. Each ships with a harness-delta integrating features.json / ADR / docs per spec §7.
- **features.json schema migrated to v2.0** — status enum is now `proposed → building → done` (was `pending` / `in_progress` / `completed`); new optional `spec:` field for back-references to design specs in `docs/specs/`. Top-level `schema_version: "2.0"` declared.
- **New ADRs:**
  - ADR-0008 — "Vendor superpowers v5.1.0" — supersedes the implicit fork strategy embedded in v1.9.x–v1.11.x.
  - ADR-0009 — "harness-delta sidecar 4-file convention" — defines the per-skill anatomy.
- **New directories:**
  - `docs/specs/` — design specs (output of `harness:brainstorming`). Replaces the pre-v2.0.0 default `docs/superpowers/specs/`; existing artifact migrated.
  - `docs/incidents/` — debug notes (output of `harness:systematic-debugging`).
- **Root `features.json` introduced** — this plugin now dogfoods its own conventions per ADR-0003.
- **`scripts/sync-superpowers.sh` added** — read-only upstream reconciliation helper; emits per-skill diff summary against the currently installed superpowers cache. See ADR-0008 §"Implementation".
- **`commands/review-pr.md` rewritten** as a thin wrapper over `harness:requesting-code-review` + `harness:receiving-code-review`. Other commands retained.
- **CLAUDE.md** gains 2 prohibited-practice rules enforcing the vendor discipline (file still ≤ 60 lines).

Migration: Old slash command names (`/harness:plan`, `/harness:tdd`, `/harness:verify`, `/harness:router`) no longer resolve. Use the full upstream names listed above. Existing user projects with their own features.json files using the old status enum will be flagged by `harness:audit` as a hint (back-compatible — new schema fields are optional; old status values still parse but should be migrated).

## v1.11.0 (2026-05-23)

**Breaking: Claude Code only — multi-tool compatibility layer removed**

- **Removed AGENTS.md as the canonical memory file**: `CLAUDE.md` once again becomes the single source of truth. The `AGENTS.md` + `CLAUDE.md` wrapper + `CODEBUDDY.md` wrapper pattern (introduced in v1.8.0) is removed.
- **Removed `$TOOL_DIR` / `$TOOL_NAME` indirection** from `init.sh.template` and `AGENTS.md.template` (template itself deleted). Templates now hardcode `.claude` / "Claude Code".
- **Documentation, training materials, and references** updated to reflect Claude-Code-only positioning: README × 2, CONTRIBUTING, architecture, marketplace submission, harness evaluation handbook (D7 dimension re-framed from "vendor-neutral / 跨工具" to "marketplace / 文档", total score 100→90), HarnessEngineering methodology doc, and the 90-minute training materials.
- **ADR 0005 superseded** by new ADR 0007 ("Claude Code Only"). ADR 0006 (Harness 评价体系) catalogued in the index.
- **Workshop sample** `training/sample-board/board-with-harness/AGENTS.md` renamed to `CLAUDE.md`; all training narrative re-pitched around CLAUDE.md instead of AGENTS.md as a cross-tool standard.

Migration: existing user projects with their own `AGENTS.md` are not touched by this plugin. New projects generated via `harness:init` will only produce `CLAUDE.md`.

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
