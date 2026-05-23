# Spec: 移除 CodeBuddy 残留 — Claude Code Only

- **Date**: 2026-05-23
- **Status**: Approved — ready for implementation
- **Target version**: v1.11.0
- **Scope**: 单 PR / 单 commit，22 文件改动
- **Brainstormed via**: `superpowers:brainstorming`
- **Next step**: `writing-plans` skill

---

## 1. 目标

让仓库对外只呈现一个故事："Harness Engineering 是 Claude Code 专用 marketplace plugin"。

v1.10.1 已删除 `.codebuddy-plugin/` 目录与脚本侧的 CodeBuddy 支持，但 8 个领域仍残留兼容层（AGENTS.md 双文件结构、`$TOOL_DIR`/`$TOOL_NAME` 间接层、ADR 0005、培训材料、handbook、README）。本 spec 完成最后一次清理。

## 2. 决策

### 2.1 已锁定的设计选择

| 决策点 | 选择 | 理由 |
|---|---|---|
| AGENTS.md 去留 | **删除**，回退到 CLAUDE.md-only | 用户明确要求"只支持 Claude Code"；保留 AGENTS.md 会让设计意图与代码现实脱节 |
| 历史/培训材料 | **完全清理** + ADR 0005 标 Superseded | 对外只暴露当前事实；CHANGELOG / ADR 0005 留痕作为决策演化记录 |
| 打包方式 | **单 PR 方案 A** | 主题一致，atomic 优于多 PR 引入中间不一致期 |
| 版本号 | v1.11.0（minor bump，含 Breaking 标识） | v1.10.1 已是事实上的 breaking；这次是结构层收尾 |

### 2.2 明确不动的范围

- `CHANGELOG.md` 的历史条目（v1.8.0 / v1.10.1 段）原样保留
- `scripts/post-observe.sh` / `scripts/pre-protect-env.sh` 里的 `TOOL_NAME` 变量（这是 Claude hook payload 字段，非 AI 工具命名，与 CodeBuddy 无关）
- 既有用户项目里的 `AGENTS.md` / `.claude/` 运行时产物（plugin 不强制覆盖）
- per-language 模板（`docs/templates/{typescript,python,go,java}/CLAUDE.md.template`）已干净，不动
- `agents/` / `commands/` / `hooks/` / `.github/` 已干净，不动
- ADR 0005 正文不修改（只在头部追加 Superseded 横幅）

## 3. 完整文件改动清单（22 处）

| # | 操作 | 路径 | 说明 |
|---|---|---|---|
| 1 | 🗑️ 删 | `AGENTS.md` | 内容并入 CLAUDE.md |
| 2 | 🗑️ 删 | `CODEBUDDY.md` | DEPRECATED stub |
| 3 | 🗑️ 删 | `docs/templates/generic/AGENTS.md.template` | — |
| 4 | ✏️ 重写 | `CLAUDE.md` (root) | 从 2 行 wrapper → 正本（≤60 行） |
| 5 | ✏️ 改 | `docs/templates/generic/CLAUDE.md.template` | 见 §4.5（明确：迁哪条、丢哪条） |
| 6 | ✏️ 改 | `docs/templates/generic/init.sh.template` | 删 `TOOL_DIR`/`TOOL_NAME` 导出；文案改为 CLAUDE.md |
| 7 | ✏️ 大改 | `skills/init/SKILL.md` | 8 处 AGENTS.md 引用 + MEMORY_FILE 检测逻辑 + "<=60 行原则"全部改为 CLAUDE.md |
| 8 | ✏️ 改 | `skills/archive/SKILL.md` | line 47 |
| 9 | ✏️ 改 | `skills/verify/SKILL.md` | line 58 |
| 10 | ✏️ 改 | `skills/audit/SKILL.md` | line 5, 28-29, 66, 75 — 删 MEMORY_FILE 检测 |
| 11 | ✏️ 改 | `docs/architecture.md` | 删除 "Tool-agnostic design" 段；目录树去 AGENTS.md |
| 12 | ✏️ 改 | `README.md` | 9 处 AGENTS.md → CLAUDE.md；删兼容性表中的 AGENTS.md 行 |
| 13 | ✏️ 改 | `README.zh-CN.md` | 同 12 中文版 |
| 14 | ✏️ 改 | `references/harness-evaluation-handbook.md` | line 831：eval 规则去掉 `.codebuddy/` |
| 15 | ✏️ 改 | `training/instructor-notes.md` | line 62 |
| 16 | ✏️ 改 | `training/demo-script.md` | line 66；line 421 整条 FAQ 删除 |
| 17 | ✏️ 改 | `docs/training-plan-90min.md` | line 65, 499 |
| 18 | ✏️ 改 | `docs/decisions/0005-tool-agnostic-agents-md.md` | 头部加 Superseded by 0007 横幅，正文不动 |
| 19 | 🆕 新建 | `docs/decisions/0007-claude-code-only.md` | 见 §4.2 |
| 20 | ✏️ 改 | `docs/decisions/README.md` | 索引：0005 标 superseded、追加 0007 |
| 21 | ✏️ 改 | `CHANGELOG.md` | 顶部新增 v1.11.0 段；历史条目**原样保留** |
| 22 | ✏️ 改 | `.claude-plugin/plugin.json` | version → "1.11.0" |

## 4. 内容设计

### 4.1 新 `CLAUDE.md`（root）

基于现有 `AGENTS.md`，应用以下 diff：

```diff
- # Harness Engineering Plugin — AGENTS.md
+ # Harness Engineering Plugin — CLAUDE.md

- > Universal agent memory file. Supports Claude Code (reads CLAUDE.md)
- > and all AI coding tools compatible with AGENTS.md. Content is identical across tools.

  ## Project Overview / Tech Stack / Key Commands ... （保留）

  ## Architecture Conventions
  - Dependency direction: references → templates → skills → commands
  - Every Skill's SKILL.md must include YAML frontmatter
  - All Hook scripts must follow "silent on success, visible on failure"
  - Placeholders in template files must use the {{PLACEHOLDER}} format
- - Skills/Commands must not hardcode `.claude/` paths; use `$TOOL_DIR` instead

  ## Prohibited Practices
  - Never hardcode specific project names or team information in templates
- - Never generate an AGENTS.md template exceeding 60 lines
+ - Never generate a CLAUDE.md template exceeding 60 lines
  - Never let Hook templates produce output on success
  - Never exceed 500 lines in a single Skill file
- - Never hardcode `.claude/` paths in Skill content

  ## Further Context
  ...
- - Multi-tool compatibility decision: docs/decisions/0005-tool-agnostic-agents-md.md
+ - Architecture decision (Claude Code only): docs/decisions/0007-claude-code-only.md
```

预期结果：约 35 行，仍在项目 ≤60 行硬约束内。

### 4.2 ADR 0007 — Claude Code Only

| 字段 | 内容 |
|---|---|
| Status | Accepted（Supersedes 0005） |
| Date | 2026-05-23 |
| Context | ADR 0005 (2026-04-08) 在 CodeBuddy 是相关目标时选择了 tool-agnostic（AGENTS.md + 双 wrapper + `$TOOL_DIR` 间接层）。v1.10.1 移除 CodeBuddy 支持后，该间接层失去对应收益，徒增认知成本。 |
| Decision | CLAUDE.md 重新成为唯一 canonical memory file。删除 AGENTS.md / CODEBUDDY.md / `$TOOL_DIR` 间接层。Plugin 定位明确为 Claude Code marketplace 专用。 |
| Consequences ✅ | (a) 用户认知负担降低：一个文件、一种路径<br>(b) Skill / Hook / 模板与 Claude Code 现实 1:1 对应<br>(c) 文档收敛，README 更易懂 |
| Consequences ⚠️ | (a) 放弃 AGENTS.md 这个新兴行业标准（OpenAI Codex / Cursor / Aider 都读它）—— 未来若重新支持非 Claude 工具需新 ADR<br>(b) 已迁移到 AGENTS.md 的用户项目需自行回迁（plugin 不强制覆盖既有文件） |
| Migration | (a) 既有用户项目的 `AGENTS.md` 不动<br>(b) 新 `harness:init` 只生成 `CLAUDE.md`<br>(c) v1.11.0 CHANGELOG 标注 Breaking Change |
| Links | Supersedes [ADR 0005](0005-tool-agnostic-agents-md.md)；相关：v1.10.1 release notes |

### 4.3 ADR 0005 Superseded 横幅（追加到文件顶部）

```markdown
> **⚠️ SUPERSEDED by [ADR 0007](0007-claude-code-only.md) — 2026-05-23**
> CodeBuddy 已于 v1.10.1 移除支持，本 ADR 论证的"工具无关架构"不再适用。
> 文件保留作为历史决策记录。
```

### 4.5 `docs/templates/generic/CLAUDE.md.template` 修改

`AGENTS.md.template` 即将删除，比对它与现有 `CLAUDE.md.template`：

**迁移到 CLAUDE.md.template 的内容**（仅 1 条，AGENTS.md.template 独有且与工具无关）：

```markdown
- 永远不要直接写入 `docs/features.json`（Agent 只读，变更记录至 claude-progress.json）
```
→ 追加到 `CLAUDE.md.template` 现有 "禁止规则" 段末尾。

**丢弃不迁移的内容**（AGENTS.md.template 独有但本次决策淘汰）：

```markdown
- Hook 脚本和 Skills 内容不得硬编码工具路径，统一使用 `$TOOL_DIR`
```
→ 直接丢弃（`$TOOL_DIR` 间接层本次移除）。

**`CLAUDE.md.template` 其余内容不动**（工作流 Skill 触发段等已经是 CLAUDE.md 专属）。

### 4.6 CHANGELOG v1.11.0 段（顶部追加，历史条目保留）

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

## 5. 验证计划（4 道闸门）

任何一道不过，回到对应文件再改，不向前推进。

### 闸门 1 — 内容残留检查（grep 自动化）

| 命令 | 期望 |
|---|---|
| `grep -rli "codebuddy" --exclude-dir=.git .` | 只在 `CHANGELOG.md` 和 `docs/decisions/0005-*.md` 出现 |
| `grep -rln "AGENTS\.md" --exclude-dir=.git .` | 只在 `CHANGELOG.md` / `docs/decisions/0005-*.md` / `docs/decisions/0007-*.md` 出现 |
| `grep -rn "\$TOOL_DIR\|\$TOOL_NAME" docs/templates/ skills/ commands/` | **零结果** |
| `grep -rl "CODEBUDDY" --exclude-dir=.git .` | 只在 CHANGELOG / ADR 0005 历史段 |

### 闸门 2 — 结构与渲染检查

| 命令 | 期望 |
|---|---|
| `wc -l CLAUDE.md` | ≤ 60 |
| `wc -l docs/templates/generic/CLAUDE.md.template` | ≤ 60 |
| `python3 -m json.tool .claude-plugin/plugin.json` | parse 成功，`"version": "1.11.0"` |
| `python3 -m json.tool .claude-plugin/marketplace.json` | parse 成功 |
| `find docs/templates -name "AGENTS.md.template"` | 零结果 |
| `test ! -f AGENTS.md && test ! -f CODEBUDDY.md` | exit 0 |

### 闸门 3 — 功能检查（强制）

| 命令 | 期望 |
|---|---|
| `bash scripts/self-test.sh` | 全部通过（如 self-test 含 AGENTS.md 断言需一并更新） |
| **手动执行** `harness:init` skill on a scratch dir | 生成目录里只有 `CLAUDE.md`；生成的 `init.sh` 不含 `TOOL_DIR=` 行 |
| 渲染 `docs/templates/generic/init.sh.template` 后 bash 执行 | 输出含 "📖 Agent 记忆：CLAUDE.md"，无 AGENTS.md 字样 |

> **闸门 3 第二条为强制验收**——必须真实执行一次 `harness:init`，否则不允许声明完成。

### 闸门 4 — 链接完整性

| 命令 | 期望 |
|---|---|
| `grep -rE "\]\([^)]*AGENTS\.md\)" --exclude-dir=.git .` | 仅在 ADR 0005 / ADR 0007 / CHANGELOG 出现 |
| `grep -rE "docs/decisions/0005" --exclude-dir=.git .` | 仅在 ADR 0007（Supersedes）/ ADR README 索引出现 |
| `grep -rE "docs/decisions/0007" --exclude-dir=.git .` | 至少在 ADR README / CLAUDE.md "Further Context" / CHANGELOG 出现 |

## 6. Definition of Done

- [ ] 闸门 1–4 全部通过
- [ ] `git diff --stat` 显示约 22 个文件改动（±2 容差，self-test.sh 可能需要更新）
- [ ] commit message：`feat!(v1.11.0): drop AGENTS.md + CodeBuddy compatibility — Claude Code only`（`!` 标 BREAKING）
- [ ] **手动核对** CHANGELOG 历史条目（v1.8.0、v1.10.1）未被误删
- [ ] **手动执行** `harness:init` on scratch dir 通过

## 7. 不在范围内（明确推迟）

- AGENTS.md 行业标准的未来支持：若日后要重新接入非 Claude 工具，新开 ADR 处理，本次不预留兼容层
- 既有用户项目的迁移工具/脚本：plugin 不负责回迁用户文件
- Skill 命名 / 模板结构的进一步重构：与本次主题无关，禁止顺手做

---

## Self-Review（spec 写完后自查）

- [x] **Placeholder scan**: 全文无 TBD / TODO / 未填段落
- [x] **Internal consistency**: §3 文件清单 22 项与 §5 闸门、§6 DoD 一致；§4.1 diff 与 §4.2 ADR consequences 描述无矛盾
- [x] **Scope check**: 单一主题（移除 CodeBuddy 残留），适合单一 implementation plan，无需 decomposition
- [x] **Ambiguity check**: "完全清理" 在 §2.2 显式列出不动项；"22 文件 ±2 容差" 给出可量化判据；闸门 3 "强制" 明确加粗；§3 row 5 通过 §4.5 明确迁移/丢弃规则
