# harness:archive — 完成归档与文档同步

> **来源**: OpenSpec `/opsx:archive` + 手册 §K.6「文档同步 Agent」+ 手册 §2.3「结构化交接物」
> **整合**: 将 commands/sync-docs.md + commands/scan-arch.md 的核心检查合并为一个 Skill，
> 在任务完成时自动触发，确保交接物完整、文档与代码一致。

## 何时使用

| 触发条件 | 示例 |
|---------|------|
| 特性标记为 completed | harness:verify 通过后 |
| 手动调用 `/harness:archive` | Sprint 结束整理 |
| completed_features >= 10 | session-start 提示归档 |
| 重大重构完成 | 架构变更后同步文档 |

## 归档流程

### Step 1：归档已完成的 Spec

检查 `docs/features.json` 中 `status: "completed"` 的特性：

```
对每个已完成特性：
  1. 如果存在对应的设计文档（docs/specs/F-xxx.md 或 docs/plans/F-xxx.md）
     → git mv 到 docs/archive/（保留 git 历史）
  2. 在归档文件顶部追加完成元数据：
     ---
     archived_at: {{TIMESTAMP}}
     completed_by: {{SESSION_ID}}
     feature_id: F-xxx
     ---
  3. 更新 docs/features.json：添加 archived_at 字段
```

**目录约定**：归档目录固定为 `docs/archive/`，如不存在则创建。使用 `git mv` 而非 copy+delete，确保 `git log --follow` 可追溯完整历史。

### Step 2：文档一致性检查

执行以下对比（来源：commands/sync-docs.md）：

1. **目录结构对比**
   - 读取 `docs/architecture.md` 中描述的目录结构
   - 与 `src/` 实际目录对比
   - 列出新增但未记录的目录、已删除但仍被引用的目录

2. **CLAUDE.md 规则有效性**
   - 逐条检查 CLAUDE.md / AGENTS.md 中的规则
   - 标记已被 Hook 或 Linter 覆盖的冗余规则
   - 标记对应错误模式已不存在的过时规则

3. **ADR 状态同步**
   - 检查 `docs/decisions/` 中状态为「已采纳」的 ADR
   - 验证对应技术选型是否仍在使用

### Step 3：架构健康快检（来源：commands/scan-arch.md）

轻量版架构扫描（完整版使用 `/harness:audit`）：

- [ ] 依赖方向违规（参照 architecture.md）
- [ ] 超过 300 行的源代码文件
- [ ] 最近 7 天新增但无测试的文件

### Step 4：生成归档报告

输出格式：

```markdown
## 归档报告 — {{DATE}}

### 已归档
- F-001: 用户登录 → docs/archive/F-001-user-login.md

### 文档漂移
- [严重] docs/architecture.md 缺少 src/services/notification/ 描述
- [建议] CLAUDE.md 第 12 行规则已被 pre-protect-env Hook 覆盖

### 架构快检
- [警告] src/utils/helpers.ts 超过 300 行（当前 342 行）

### 建议操作
1. 更新 architecture.md 补充 notification 模块描述
2. 删除 CLAUDE.md 第 12 行冗余规则
```

## 与其他组件的关系

```
harness:verify（验证通过）
    ↓
harness:archive（本 Skill — 归档 + 文档同步）
    ↓
Stop Hook（提交进度）

触发链：verify 确认完成 → archive 整理交接物 → stop 保存状态
```

## 与 harness:evolve 的分工

```
harness:archive：每次任务完成时触发，聚焦「归档 + 文档同步」
harness:evolve：  按需触发（模型更新/Sprint 结束），聚焦「Harness 自身的精简与演进」

archive 发现的文档漂移 → 如果涉及 Harness 组件本身 → 交给 evolve 处理
```
