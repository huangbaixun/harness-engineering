---
description: Sprint feature 分配规划。分析 docs/features.json 的依赖图和团队负载，输出最优 owner 分配方案 + 可直接执行的 sprint-kickoff.sh 脚本。
---

# /harness:assign — Sprint Feature 分配规划器

> 目标：让每位团队成员在 Sprint 开始时，5 分钟内拿到一份"我应该做什么、怎么开始"的可执行脚本，而不是一张需要二次解读的分配表。

## Phase 1：读取并分析 features.json

```bash
cat docs/features.json
```

从 JSON 中提取：

- **待分配池**：`status` 为 `planned` 或 `ready` 的 feature
- **进行中**：`status` 为 `in_progress` 的 feature（含 owner）
- **依赖图**：构建 `depends_on` → `blocks` 的有向图

然后计算每个待分配 feature 的两个关键属性：

**可立即开始？**（`startable`）
```
startable = depends_on 为空，
         OR depends_on 中所有 feature 的 status == "done"
```

**关键路径权重**（`criticality`）
```
criticality = 直接 blocks 数 + 递归 blocks 数（传递闭包）
```

输出状态快照，格式如下：

```
🟢 可立即开始（N 个）
  F-001 认证模块         [criticality=3, layer=backend]
  F-004 基础设施         [criticality=2, layer=infra  ]

🟡 等待解锁（N 个）
  F-003 权限控制         [等待: F-001]
  F-005 用户设置         [等待: F-001, F-002]

🔄 进行中（N 个）
  F-002 用户管理 UI      [owner: alice, layer=frontend]

📊 关键路径：F-001 → F-003 → F-006（共 3 跳，影响 4 个下游）
```

---

## Phase 2：获取团队快照

**优先读取 CLAUDE.md 中的 `## 团队成员` 章节**（若已声明）。格式示例：

```markdown
## 团队成员
- simon: backend, 当前负载 1
- alice: fullstack, 当前负载 1
- bob: infra, 当前负载 0
```

若 CLAUDE.md 中没有此章节，询问用户：

> 请告诉我团队成员信息（每人一行，格式：姓名 / layer偏好 / 当前 in_progress 数量）
> 例如：simon / backend / 1

收集后，将成员信息更新到 CLAUDE.md 的 `## 团队成员` 章节（若不存在则新增，且不计入 60 行限制外，放在文件末尾）。

---

## Phase 3：生成分配方案

按以下四条规则依次约束，输出每个待分配 feature 的推荐 owner：

### 规则 1（硬约束）：files_owned 不重叠
两个同时 `in_progress` 的 feature，其 `files_owned` 列表不得有公共路径前缀。
违反此规则的分配直接拒绝，标记为 `⚠️ 文件冲突`，提示人类决策。

### 规则 2（硬约束）：每人最多 2 个 in_progress
超过后标记为 `⚠️ 负载过高`，放入下一批次。

### 规则 3（软优先级）：关键路径优先
`criticality` 高的 feature 优先分配，确保不阻塞下游。

### 规则 4（软优先级）：layer 亲和性
将 feature 分配给 `layer` 匹配的成员，减少认知切换成本。
同一 Sprint 内，优先让同一人负责同一 layer 的多个 feature。

输出分配方案表：

```
┌────────┬─────────────────────┬────────┬──────────────┬───────────────────────────────┐
│ Owner  │ Feature             │ layer  │ criticality  │ 分配理由                       │
├────────┼─────────────────────┼────────┼──────────────┼───────────────────────────────┤
│ simon  │ F-001 认证模块       │backend │ ★★★（3）      │ 关键路径首位，layer 匹配       │
│ alice  │ F-002 用户管理 UI    │frontend│ ★★（2）       │ 已在进行中，保持连续性         │
│ bob    │ F-004 基础设施       │infra   │ ★★（2）       │ layer 匹配，负载最低           │
│ simon  │ F-007 API 文档       │backend │ ★（1）        │ 与 F-001 共享 src/api/，合并   │
├────────┼─────────────────────┼────────┼──────────────┼───────────────────────────────┤
│ 下批次 │ F-003 权限控制       │backend │ ★★★（待解锁）  │ 等待 F-001 完成后分配         │
│ ⚠️ 冲突 │ F-008 搜索功能       │        │              │ files_owned 与 F-002 重叠     │
└────────┴─────────────────────┴────────┴──────────────┴───────────────────────────────┘
```

对于 `⚠️ 冲突` 的 feature，明确说明重叠的文件路径，等待用户决策后再分配。

---

## Phase 4：生成 sprint-kickoff.sh

为本次 Sprint 生成一个可执行脚本，每位成员的操作独立成 section，可直接发给对方执行：

```bash
#!/usr/bin/env bash
# Sprint Kickoff Script — 生成于 {DATE}
# 用法：bash sprint-kickoff.sh [成员名]
# 若不带参数，显示所有成员的操作

MEMBER=${1:-"all"}

# =====================
# === simon 的任务 ===
# =====================
if [ "$MEMBER" = "simon" ] || [ "$MEMBER" = "all" ]; then
  echo "=== simon: 认领 F-001 + F-007 ==="
  git pull origin main

  # 认领 F-001
  python3 -c "
import json, sys
with open('docs/features.json') as f: data = json.load(f)
for feat in data['features']:
    if feat['id'] == 'F-001':
        feat['owner'] = 'simon'
        feat['status'] = 'in_progress'
with open('docs/features.json', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print('F-001 已认领')
"
  # 认领 F-007
  python3 -c "
import json
with open('docs/features.json') as f: data = json.load(f)
for feat in data['features']:
    if feat['id'] == 'F-007':
        feat['owner'] = 'simon'
        feat['status'] = 'in_progress'
with open('docs/features.json', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print('F-007 已认领')
"
  git add docs/features.json
  git commit -m "claim(F-001, F-007): simon 认领"
  git push origin main

  # 启动 worktree（若项目使用 worktree 模式）
  claude --worktree feature-auth -p "
    读取 docs/features.json 中 id=F-001 的任务。
    files_owned 是你的文件边界，不修改边界外的文件。
    description 说明了实现要求，acceptance 是验收标准。
    完成后运行 acceptance 中的所有测试命令，全部通过后提 PR。
  " &
fi

# =====================
# === alice 的任务 ===
# =====================
if [ "$MEMBER" = "alice" ] || [ "$MEMBER" = "all" ]; then
  echo "=== alice: 继续 F-002 ==="
  # alice 已有 F-002，无需认领，直接启动
  git pull origin main
  claude --worktree feature-users -p "
    读取 docs/features.json 中 id=F-002 的任务。
    继续上次的工作，参考 docs/claude-progress.json 了解已有进度。
  " &
fi

# =====================
# === bob 的任务 ===
# =====================
if [ "$MEMBER" = "bob" ] || [ "$MEMBER" = "all" ]; then
  echo "=== bob: 认领 F-004 ==="
  git pull origin main
  python3 -c "
import json
with open('docs/features.json') as f: data = json.load(f)
for feat in data['features']:
    if feat['id'] == 'F-004':
        feat['owner'] = 'bob'
        feat['status'] = 'in_progress'
with open('docs/features.json', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print('F-004 已认领')
"
  git add docs/features.json
  git commit -m "claim(F-004): bob 认领"
  git push origin main
  claude --worktree feature-infra -p "
    读取 docs/features.json 中 id=F-004 的任务。
    files_owned 是你的文件边界。acceptance 是验收标准。
  " &
fi

echo "✅ Sprint 已启动。各成员的 Agent 在后台运行。"
echo "📌 当任何任务完成后，运行 /harness:dump 保存进度。"
```

将此脚本保存到项目根目录：`sprint-kickoff.sh`，并 `chmod +x sprint-kickoff.sh`。

---

## Phase 5：记录 Sprint 分配到 claude-progress.json

将本次分配追加到 `docs/claude-progress.json` 的 `sprint_history` 数组：

```json
{
  "sprint_history": [
    {
      "date": "{DATE}",
      "assignments": [
        { "owner": "simon", "features": ["F-001", "F-007"], "reason": "关键路径 + layer 匹配" },
        { "owner": "alice", "features": ["F-002"],           "reason": "继续已有任务" },
        { "owner": "bob",   "features": ["F-004"],           "reason": "layer 匹配，负载最低" }
      ],
      "deferred": ["F-003（等待 F-001）"],
      "conflicts": ["F-008（files_owned 冲突，待人工决策）"]
    }
  ]
}
```

---

## 输出摘要

最后以一段简洁的文字说明：

```
✅ 本次 Sprint 分配完成

分配了 3 人 × 4 个 feature：
  simon → F-001（关键路径）+ F-007
  alice → F-002（继续进行中）
  bob   → F-004

等待下批次：F-003（依赖 F-001 完成后解锁）
需要人工决策：F-008（files_owned 与 F-002 冲突）

已生成：sprint-kickoff.sh（可直接运行或分发给团队成员）
已记录：docs/claude-progress.json sprint_history
```

---

## 反模式提醒

| 反模式 | 原因 | 正确做法 |
|--------|------|---------|
| 凭感觉分配，不看 criticality | 阻塞了关键路径，下游积压 | 始终优先分配 criticality 最高的 |
| 一人同时认领 3+ 个 feature | 认知负载过高，每个都推进缓慢 | 每人最多 2 个 in_progress |
| 忽略 files_owned 重叠 | 合并冲突，互相覆盖工作 | 冲突的 feature 必须串行或重新切割 |
| 不记录分配历史 | 无法复盘，下次 Sprint 没有参考 | 每次都追加到 sprint_history |
