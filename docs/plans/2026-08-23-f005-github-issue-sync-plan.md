# F005 features.json ↔ GitHub/GHE Issue 双向同步 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use harness:subagent-driven-development (recommended) or harness:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 features.json 与 GitHub/GHE Issue 双向联动，且不破坏「闸门链离线可跑」。

**Architecture:** 同步逻辑集中在一个可测的 Python 脚本 `scripts/harness_sync.py`（子命令 pull / push / status），bash hook 只作薄包装。字段级单写所有权（ADR-0011）使对账成为无状态纯函数。网络仅发生在 SessionStart（拉）与 Stop（推）两点，编辑热路径零网络。

**Tech Stack:** Python 3.10+（同步核心）、Bash（hook 三元组）、`gh` CLI（认证与 API，不自管凭据）

**Spec:** `docs/specs/2026-08-22-features-github-sync-design.md`

## Global Constraints

CLAUDE.md 项目级约束，每个任务隐含包含：

- 依赖方向 `references → templates → skills → commands`，反向禁止
- 每个 SKILL.md 必须含 YAML frontmatter（`name`、`description`）
- Hook 脚本必须"成功完全静默，失败才输出"
- 模板占位符必须用 `{{PLACEHOLDER}}` 格式
- harness-original SKILL.md 不超过 500 行
- SKILL.md 新增或修改必须走 skill-creator eval 流程（ADR-0004）
- hook 脚本按三元组交付：`<name>` + `<name>.sh`（同内容）+ `<name>.cmd`（polyglot）
- 改 `scripts/session-start` 路径或文件名须同 commit 协调 `skills/using-harness/SKILL.md`（ADR-0009）

**本特性专属硬约束（来自 spec 与 ADR-0011/0012）：**

- features.json 规范位置为仓库根目录，`docs/` 为永久回退（ADR-0012）
- 字段单写：harness 写 name/description/acceptance_criteria/out_of_scope/spec/dependencies/status；
  GitHub 写 priority/delivery_state/assignee/milestone；technical_notes/related_files 不同步
- **未配置 `github.enabled` 时零网络调用**
- **PATCH 前必须 GET 比对托管区块**，内容相同则不写（每次 PATCH 都会通知所有 watcher）
- **只创建/修改带 `harness/` 前缀的 label**，其余一律只读
- Stop hook 任何失败均 `exit 0`，失败时输出**恰好一行**警告
- 绝不自管凭据，全部走 `gh auth`

**测试注入点：** 所有 `gh` 调用经由 `$HARNESS_GH_BIN`（默认 `gh`），使测试可注入桩程序，
全部测试离线可跑。

---

### Task 1: 同步核心库 —— 配置解析与托管区块渲染

**Files:**
- Create: `scripts/harness_sync.py`
- Test: `scripts/tests/test-harness-sync-core.sh`

**Interfaces:**
- Consumes: 无
- Produces:
  - `resolve_features_path() -> str | None` —— 根目录优先，docs/ 回退，都无则 None
  - `load_config(features: dict) -> dict | None` —— 返回 github 块；`enabled` 非 True 时返回 None
  - `render_block(feature: dict) -> str` —— 生成 `<!-- harness:begin ... -->…<!-- harness:end -->`
  - `split_body(body: str) -> tuple[str, str | None, str]` —— (before, block, after)；无标记时 block 为 None
  - `replace_block(body: str, new_block: str) -> str` —— 无标记时追加到末尾

- [ ] **Step 1: 写失败测试**

覆盖四点：未配置时 `load_config` 返回 None；`render_block` 含验收清单与 out_of_scope 围栏；
`split_body` 能正确切分且**区块外内容逐字节保留**；无标记时 `replace_block` 追加而非重复。

- [ ] **Step 2: 跑测试确认失败**（脚本尚不存在）

- [ ] **Step 3: 实现上述五个函数**

- [ ] **Step 4: 跑测试确认通过**

---

### Task 2: push —— 差异集、幂等比对、label 命名空间

**Files:**
- Modify: `scripts/harness_sync.py`
- Test: `scripts/tests/test-harness-sync-push.sh`（含 `gh` 桩）

**Interfaces:**
- Consumes: Task 1 的 `render_block` / `replace_block` / `load_config`
- Produces:
  - `cmd_push(dry_run: bool, limit: int) -> int` —— 返回退出码；dry-run 时只报告不写
  - 影子副本 `.harness/last-synced.json`：仅用于算差异集，丢失则退化为全量对账

- [ ] **Step 1: 写失败测试**

断言：连续两次 push 第二次零 PATCH（验收 3）；区块外内容字节不变（验收 4）；
只 add 带 `harness/` 前缀的 label，`P0/P1/P2` 与 `state/*` 只读（验收 6）；
超限时报出剩余条数（验收 7）。

- [ ] **Step 2-4: 红 → 绿**

---

### Task 3: pull —— GitHub 域字段回流与 harness/track 入站

**Files:**
- Modify: `scripts/harness_sync.py`
- Test: `scripts/tests/test-harness-sync-pull.sh`

**Interfaces:**
- Consumes: Task 1 的 `load_config` / `resolve_features_path`
- Produces: `cmd_pull(timeout: int) -> int`

- [ ] **Step 1: 写失败测试**

断言：priority/delivery_state/assignee/milestone 回流；harness 域字段**不被 pull 覆盖**；
不带 `harness/track` 的 Issue 不入库（验收 5）；schema 2.0 文件无新字段仍正常（验收 9）。

- [ ] **Step 2-4: 红 → 绿**

---

### Task 4: 失败模式与并发锁

**Files:**
- Modify: `scripts/harness_sync.py`
- Test: `scripts/tests/test-harness-sync-failures.sh`

**Interfaces:**
- Consumes: Task 2/3
- Produces: `acquire_lock() -> bool`（mkdir 原子锁，拿不到即返回 False，绝不等待）

- [ ] **Step 1: 写失败测试**

九个失败模式各一条：离线、401、403 限流、404 Issue 被删、托管区块被删、
features.json 语法错、锁被占、未配置、gh 不存在。断言均为「不抛栈、不阻断、恰好一行警告」。

- [ ] **Step 2-4: 红 → 绿**

---

### Task 5: hook 接线与命令

**Files:**
- Create: `scripts/stop-sync-issues` + `.sh` + `.cmd`
- Modify: `scripts/session-start`（+ `.sh`）、`hooks/hooks.json`
- Create: `commands/sync-issues.md`
- Test: `scripts/tests/test-sync-hooks.sh`

**Interfaces:**
- Consumes: Task 1-4 的 `harness_sync.py`
- Produces: Stop hook 契约（任何失败 exit 0）；`/harness:sync-issues` 命令面

- [ ] **Step 1: 写失败测试**

断言：未配置时 hook 零 `gh` 调用（验收 1）；Stop hook 在 push 失败时仍 `exit 0`
且 stderr 恰好一行（验收 8）；SessionStart 超时不阻断。

- [ ] **Step 2-4: 红 → 绿**

---

### Task 6: schema 2.1、模板与 assign.md 归属来源

**Files:**
- Modify: `features.json`、`docs/templates/generic/features.json.template`
- Modify: `commands/assign.md`、`commands/evals/evals.json`
- Modify: `.gitignore`
- Modify: `docs/architecture.md`、`CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1-5
- Produces: schema 2.1 契约（新增字段全部可选）

- [ ] **Step 1**: features.json 顶层加 `github` 块（`enabled: false`），per-feature 加
  `github_issue` / `delivery_state` / `assignee` / `milestone`，`schema_version` → `2.1`
- [ ] **Step 2**: 模板同步，`enabled: false`
- [ ] **Step 3**: assign.md 归属来源改为 `assignee`，移除 owner 的 TODO(F005) 注释（验收 10）
- [ ] **Step 4**: `.gitignore` 加 `.harness/`
- [ ] **Step 5**: architecture.md 与 CHANGELOG 同步

---

## 验收标准覆盖检查（100% rigid coverage gate）

| F005 acceptance_criterion | 覆盖任务 |
|---|---|
| 1. 未配置时零网络调用 | Task 1（load_config）+ Task 5（hook 层断言） |
| 2. 断网时闸门链完整可用 | Task 4（失败模式）+ Task 5（exit 0 契约） |
| 3. 连续两次 Stop 不产生第二次 PATCH | Task 2 |
| 4. 托管区块外内容字节不变 | Task 1（split/replace）+ Task 2 |
| 5. 不带 harness/track 的 Issue 不入库 | Task 3 |
| 6. 不带 harness/ 前缀的 label 不被改动 | Task 2 |
| 7. 超限时报出剩余条数 | Task 2 |
| 8. Stop hook 任何失败 exit 0 且恰好一行警告 | Task 4 + Task 5 |
| 9. schema 2.1 字段全部可选，2.0 文件仍可用 | Task 3 + Task 6 |
| 10. assign.md 以 assignee 为归属来源 | Task 6 |

无孤儿验收标准。

## 完成后

调用 `harness:verification-before-completion` → `harness:finishing-a-development-branch`
→ `harness:archive`，F005 转 `done`。届时共用 spec 的两个特性均已完成，
可连同 F004 的归档一并处理。
