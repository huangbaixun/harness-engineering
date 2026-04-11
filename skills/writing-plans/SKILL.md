# writing-plans — 实现前规划

> 整合自 obra/superpowers Writing Plans skill，适配 Harness Engineering 工作流。
> 核心理念：Agent 在编码前先对齐设计，是减少方向错误最高性价比的节点。

## 何时使用

在以下任何情形下，**在写任何代码前**先执行本工作流：

| 情形 | 示例 |
|------|------|
| 实现 features.json 中的新特性 | coding-agent 取下一个特性 |
| 非平凡 Bug 修复（影响超过 1 个文件） | 需要修改多处才能修复 |
| 重构（影响模块边界或接口） | 调整层级关系、拆分模块 |
| 接到新需求描述 | 用户描述了一个新功能 |

判断规则：**预估实现超过 30 分钟或涉及 3 个以上文件，必须先规划。**

## 规划流程

### Step 1：澄清需求（Brainstorm）

从 `docs/features.json` 读取当前特性的：
- `description` — 功能意图
- `acceptance_criteria` — 验收标准
- `out_of_scope` — 明确不做什么
- `dependencies` — 前置依赖

如有歧义，在开始规划前向用户确认，**不要假设**。

### Step 2：拆解为可验证任务块

将工作拆解为每块 **2-5 分钟**的独立任务，每块必须：
- 有明确的完成标志（"测试通过" / "文件存在" / "命令输出 X"）
- 可以独立验证（不依赖其他任务的中间状态）
- 足够小（如果某块超过 5 分钟，继续拆分）

**输出格式（tasks.md 或直接列出）：**

```markdown
## 实现计划：[特性名称]

### 任务列表
- [ ] T01：创建 UserRepository 接口（验证：文件存在，接口定义正确）
- [ ] T02：实现 PostgresUserRepository（验证：单元测试全通过）
- [ ] T03：集成到 UserService（验证：集成测试通过）
- [ ] T04：更新 API 路由（验证：e2e 测试通过）

### 不做的事
- 不实现缓存（out_of_scope）
- 不改动认证逻辑（超出本特性边界）

### 风险点
- T02 依赖数据库 schema 已迁移
```

### Step 3：人工确认门控

**输出计划后，等待用户确认再开始执行。**

不要在规划后自动开始编码。计划是对齐点，不是自动触发器。

用户确认后：
1. 将任务列表写入 `docs/claude-progress.json` 的 `in_progress` 字段
2. 按顺序执行，每完成一个任务更新状态
3. 每个任务完成后运行对应验证

## 与 OpenSpec 的关系

如果项目使用了 OpenSpec：
- `openspec/changes/proposal.md` 对应本 Skill 的 Step 1（澄清需求）
- `openspec/changes/tasks.md` 对应本 Skill 的 Step 2（任务拆解）
- 两者重叠时，以 OpenSpec 的产物为准，本 Skill 提供 Harness 上下文同步

## 计划质量检查

好的计划满足：
- [ ] 每个任务有可执行的验证步骤
- [ ] 没有任何任务描述是"实现 X 功能"这种模糊表述
- [ ] out_of_scope 明确列出
- [ ] 依赖顺序清晰（有依赖的任务排在被依赖任务之后）
- [ ] 总任务数 ≤ 15（超过说明特性太大，应该拆分到 features.json）
