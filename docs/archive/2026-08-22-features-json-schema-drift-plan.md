---
archived_at: 2026-08-22T13:56:49Z
feature_id: F004
archived_by: harness:archive
note: 本计划的 spec (docs/specs/2026-08-22-features-github-sync-design.md) 未随之归档 —— F005 仍在使用
---

# F004 features.json Schema 漂移对齐 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use harness:subagent-driven-development (recommended) or harness:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修掉三处 v1→v2 features.json schema 迁移残留，让读端真正读得到 features.json。

**Architecture:** 三处独立的读端各自修正路径与状态枚举，互不依赖，可并行。每处配 eval 覆盖。`session-start` 是 load-bearing hook（ADR-0010），改动最重，单列一个任务且需与 `using-harness` 协调。

**Tech Stack:** Bash + Python 3.10（hook 脚本）、Markdown（SKILL.md / command）、skill-creator evals.json

**Spec:** `docs/specs/2026-08-22-features-github-sync-design.md`（§6 前置阻塞项）

## Global Constraints

以下为 CLAUDE.md 的项目级约束，每个任务的要求都隐含包含本节：

- 依赖方向 `references → templates → skills → commands`，反向禁止
- 每个 SKILL.md 必须含 YAML frontmatter（`name`、`description`）
- Hook 脚本必须"成功完全静默，失败才输出"
- 模板占位符必须用 `{{PLACEHOLDER}}` 格式
- harness-original SKILL.md 不超过 500 行
- 任何 SKILL.md 新增或修改必须走 skill-creator eval 流程（ADR-0004），无例外
- hook 脚本按三元组交付：`<name>` + `<name>.sh`（同内容）+ `<name>.cmd`（polyglot 包装器）
- `scripts/session-start` 路径或文件名变更必须在同一 commit 内协调更新 `skills/using-harness/SKILL.md`（ADR-0009 load-bearing note）

**schema 2.0 事实（三处修正的共同目标）：**
- 文件位置：仓库根目录 `features.json`（**不是** `docs/features.json`）
- 状态枚举：`proposed / building / done`（**不是** `pending`/`ready`/`in_progress`/`completed`/`planned`）
- 依赖字段：`dependencies`（**不是** `depends_on`/`blocks`）
- v2.0 中**不存在** `owner`、`layer` 字段

---

### Task 1: session-start hook 的 features.json 读取修正

**Files:**
- Modify: `scripts/session-start`（`FEATURES_FILE` 定义 + 特性摘要 Python 块）
- Modify: `scripts/session-start.sh`（必须与 bare 文件逐字节相同）
- Test: `scripts/tests/test-session-start-features.sh`（新建）

**Interfaces:**
- Consumes: 无（本任务是三者中最独立的一个）
- Produces: `resolve_features_file()` —— 一个 bash 函数，返回 features.json 的实际路径，
  查找顺序 `features.json` → `docs/features.json`（向后兼容用户项目），都不存在则返回空串。
  Task 2、Task 3 不复用它（它们是 Markdown 指令而非可执行代码），但三者的查找顺序必须口径一致。

- [ ] **Step 1: 写失败测试**

```bash
#!/bin/bash
# scripts/tests/test-session-start-features.sh
set -euo pipefail
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cat > "$TMP/features.json" <<'EOF'
{"schema_version":"2.0","features":[
 {"id":"F001","name":"alpha","status":"building","priority":1},
 {"id":"F002","name":"beta","status":"proposed","priority":2},
 {"id":"F003","name":"gamma","status":"done","priority":3}]}
EOF
mkdir -p "$TMP/docs"
echo '{"in_progress":"x","completed_features":[]}' > "$TMP/docs/claude-progress.json"

OUT=$(CLAUDE_PROJECT_DIR="$TMP" CLAUDE_PLUGIN_ROOT="$(pwd)" bash scripts/session-start)

echo "$OUT" | grep -q "F001" || { echo "FAIL: building 特性 F001 未出现在摘要中"; exit 1; }
echo "$OUT" | grep -q "F002" || { echo "FAIL: proposed 特性 F002 未出现在摘要中"; exit 1; }
echo "$OUT" | grep -qE "1 done|done.*1"  || { echo "FAIL: done 计数错误"; exit 1; }
echo PASS
```

- [ ] **Step 2: 跑测试确认失败**

Run: `bash scripts/tests/test-session-start-features.sh`
Expected: `FAIL: building 特性 F001 未出现在摘要中` —— 因为当前代码读 `docs/features.json` 且匹配 v1 枚举

- [ ] **Step 3: 加入路径解析函数**

在 `scripts/session-start` 的 `cd` 之后、`PROGRESS_FILE` 定义之前插入：

```bash
resolve_features_file() {
  if   [ -f "features.json" ];      then echo "features.json"
  elif [ -f "docs/features.json" ]; then echo "docs/features.json"
  else echo ""
  fi
}
FEATURES_FILE="$(resolve_features_file)"
```

并删除原有的 `FEATURES_FILE="docs/features.json"` 一行。

- [ ] **Step 4: 修正状态枚举**

把特性摘要 Python 块中的三行筛选改为 schema 2.0 枚举，并同时容忍 v1 值（用户项目可能尚未迁移）：

```python
V2_BUILDING = ('building', 'in_progress')
V2_PROPOSED = ('proposed', 'pending', 'ready', 'planned')
V2_DONE     = ('done', 'completed')
feats = d.get('features', [])
ip      = [f for f in feats if f.get('status') in V2_BUILDING]
pending = [f for f in feats if f.get('status') in V2_PROPOSED]
done    = [f for f in feats if f.get('status') in V2_DONE]
```

摘要输出行改用 `building / proposed / done` 措辞，不再输出 `in_progress` / `pending` 字样。

- [ ] **Step 5: 跑测试确认通过**

Run: `bash scripts/tests/test-session-start-features.sh`
Expected: `PASS`

- [ ] **Step 6: 同步 .sh 副本并验证逐字节一致**

Run: `cp scripts/session-start scripts/session-start.sh && cmp scripts/session-start scripts/session-start.sh && echo IDENTICAL`
Expected: `IDENTICAL`

- [ ] **Step 7: 在本仓库真实验证摘要确实产生输出**

Run: `CLAUDE_PROJECT_DIR="$(pwd)" CLAUDE_PLUGIN_ROOT="$(pwd)" bash scripts/session-start | grep -A3 "特性统计"`
Expected: 出现 F004 或 F005（当前 `proposed`）与 `3 done` 计数 —— 这是"从未生效过的摘要段现在生效了"的直接证据

- [ ] **Step 8: 提交**

Run: `git add scripts/session-start scripts/session-start.sh scripts/tests/test-session-start-features.sh && git commit -m "fix(hook): session-start 读根目录 features.json 并使用 schema 2.0 枚举"`

---

### Task 2: archive skill 的 features.json 引用修正

**Files:**
- Modify: `skills/archive/SKILL.md`
- Modify: `skills/archive/evals/evals.json`

**Interfaces:**
- Consumes: Task 1 确立的路径查找顺序（`features.json` 优先，`docs/features.json` 兼容）—— 口径必须一致
- Produces: 无下游消费者

- [ ] **Step 1: 先写 eval（ADR-0004 要求 eval 先行）**

在 `skills/archive/evals/evals.json` 的 `evals` 数组追加：

```json
{
  "id": 4,
  "eval_name": "reads-root-features-json-with-v2-status",
  "type": "behavior",
  "rule_under_test": "archive 必须读根目录 features.json 并使用 schema 2.0 的 done 枚举，不得引用 docs/features.json 或 completed",
  "prompt": "归档一下已完成的特性。",
  "expected_output": "读取根目录 features.json，按 status=done 筛选已完成特性执行归档。不出现 docs/features.json 路径，不使用 completed 作为状态值。",
  "files": ["features.json"],
  "assertions": [
    {"name": "读根目录", "check": "输出或工具调用中读取的是 features.json，不是 docs/features.json。"},
    {"name": "用 done 枚举", "check": "筛选条件使用 status == done，不使用 completed。"},
    {"name": "archived_at 写回", "check": "归档后向 features.json 对应条目写入 archived_at 字段。"}
  ]
}
```

- [ ] **Step 2: 跑 baseline 确认当前失败**

Run: 用 harness:writing-skills 的 eval 流程跑 `skills/archive/evals/evals.json` 的 id=4，仅 baseline 臂
Expected: 断言"读根目录"失败 —— 当前 SKILL.md 明写 `docs/features.json`

- [ ] **Step 3: 修正 SKILL.md**

`skills/archive/SKILL.md` 中：
- `Check \`docs/features.json\` for features with \`status: "completed"\`` → `Check \`features.json\` (repo root; fall back to \`docs/features.json\` for legacy projects) for features with \`status: "done"\``
- 归档流程伪代码中的 `docs/features.json` → `features.json`
- `Update docs/features.json: add the archived_at field` → `Update features.json: add the archived_at field`

**不得**修改 SKILL.md 的其他内容 —— 本任务只做 schema 对齐。

- [ ] **Step 4: 跑 with-skill 臂确认通过**

Expected: 三条断言全通过

- [ ] **Step 5: 提交**

Run: `git add skills/archive/ && git commit -m "fix(skills): archive 对齐 features.json v2.0 schema"`

---

### Task 3: assign command 的 features.json 引用修正

**Files:**
- Modify: `commands/assign.md`
- Test: `commands/evals/`（若目录已有 assign 的 eval 则追加，否则新建 `commands/evals/assign.json`）

**Interfaces:**
- Consumes: Task 1 确立的路径查找顺序
- Produces: 无

**范围边界（重要）：** 本任务**只**修路径与状态枚举、并把 `depends_on`/`blocks` 归一到 `dependencies`。
`owner` 字段的归属来源改造**不在本任务内** —— 它已显式移交 F005（`assignee` 由 F005 引入）。
本任务遇到 `owner` 时保留原样并加一行 TODO 注释指向 F005。

- [ ] **Step 1: 写 eval**

新建或追加，断言：读根目录 `features.json`；`startable` 判定使用 `dependencies` 而非 `depends_on`；
未分配池的筛选使用 `proposed` 而非 `planned`/`ready`；进行中使用 `building` 而非 `in_progress`。

- [ ] **Step 2: 跑 baseline 确认失败**

Expected: 全部断言失败 —— 当前 command 通篇 v1 schema

- [ ] **Step 3: 修正 commands/assign.md**

- frontmatter `description` 中 `docs/features.json` → `features.json`
- `cat docs/features.json` → `cat features.json`
- 未分配池：`status` 为 `planned` 或 `ready` → `status` 为 `proposed`
- 进行中：`status == "in_progress"` → `status == "building"`
- 依赖图：`从 depends_on 到 blocks 构建有向图` → `从 dependencies 构建有向图；blocks 为其反向边，本地推导`
- `startable` 公式中 `depends_on` → `dependencies`
- `criticality` 定义改为基于反向边推导，不再假设存在 `blocks` 字段
- 在 `owner` 首次出现处加注释：`<!-- TODO(F005): owner 在 schema 2.0 中不存在；归属来源将改为 GitHub 单写的 assignee -->`

- [ ] **Step 4: 跑 with-skill 臂确认通过**

- [ ] **Step 5: 全仓库 grep 门禁**

```bash
git grep -n "docs/features\.json" -- ':!CHANGELOG.md' ':!docs/plans/' ':!docs/specs/' | grep -v "legacy" && echo "FAIL: 仍有 docs/features.json 引用" || echo "PASS"
git grep -nE "'(pending|ready|planned|in_progress|completed)'" -- skills/ commands/ scripts/ | grep -v "V2_\|legacy\|兼容" && echo "FAIL: 仍有裸 v1 枚举" || echo "PASS"
```
Expected: 两条均 `PASS`

- [ ] **Step 6: 提交**

Run: `git add commands/assign.md commands/evals/ && git commit -m "fix(commands): assign 对齐 features.json v2.0 schema"`

---

## 验收标准覆盖检查（100% rigid coverage gate）

| F004 acceptance_criterion | 覆盖任务 |
|---|---|
| session-start 读根目录 + v2 枚举 + 摘要实际产生输出 | Task 1（Step 3/4/7） |
| archive 不再引用 docs/features.json 与 completed | Task 2（Step 3） |
| assign.md 不再引用 docs/features.json、v1 枚举、v1 字段 | Task 3（Step 3） |
| 全局 grep `docs/features.json` 零命中 | Task 3（Step 5） |
| 全局 grep v1 状态枚举零命中 | Task 3（Step 5） |
| 三处各有 eval 且 SKILL.md 变更走 ADR-0004 | Task 1（Step 1）/ Task 2（Step 1-4）/ Task 3（Step 1-4） |

无孤儿验收标准。

## 完成后

三个任务全绿后调用 `harness:finishing-a-development-branch`，并把 F004 状态由
`proposed` 迁移到 `done`。F005 的实现计划在 F004 落地**之后**再写 —— 因为 F005 的
拉取逻辑要挂进 Task 1 重构后的 `session-start`，现在写会planning against 一个即将改变的文件。
