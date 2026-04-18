# harness:plan — 实现前规划

> **upstream**: obra/superpowers `writing-plans` @ [917e5f5](https://github.com/obra/superpowers/tree/917e5f5/skills/writing-plans)
> **harness-delta**: 新增 features.json 读取（Step 1）、OpenSpec XML 三段式任务结构、rigid/flexible 约束分类、人工确认门禁与 Harness 的 Stop Hook 联动

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

从 `docs/features.json` 读取当前特性，**区分 rigid 与 flexible 约束**：

**rigid（硬约束，不可跳过、不可降级）：**
- `acceptance_criteria` — 验收标准，每条必须映射到至少一个任务的 `<verify>`
- `out_of_scope` — 明确不做什么，违反则视为过度实现
- `forbidden_patterns` — 禁止模式（如有），违反则阻止完成
- `dependencies` — 前置依赖，必须在开始前确认已满足

**flexible（软约束，Agent 可根据实际情况调整）：**
- `description` — 功能意图，作为参考而非逐字规范
- `technical_notes` — 技术建议，可选择替代方案
- `related_files` — 参考文件，实际实现可能涉及更多

如有歧义，在开始规划前向用户确认，**不要假设**。

### Step 2：拆解为三段式任务块

将工作拆解为每块 **2-5 分钟**的独立任务。每个任务必须使用 **`<action> → <verify> → <done>` 三段式结构**：

- `<action>` — 具体执行什么（创建文件、修改函数、添加配置...）
- `<verify>` — 如何验证执行正确（测试通过、文件存在、命令输出匹配...）
- `<done>` — 完成标志和状态更新（更新 progress、标记 rigid 条目已覆盖...）

每块还需标注约束类型：
- **[rigid]** — 覆盖 features.json 中的 rigid 约束，不可跳过
- **[flexible]** — Agent 自行拆解的实现细节，可合并或调整

**输出格式（三段式）：**

```markdown
## 实现计划：[特性名称]

### rigid 约束（来自 features.json）
- AC-1: JWT token 有效期 24h
- AC-2: 密码 bcrypt 加密
- OOS-1: 不实现 OAuth 第三方登录

### 任务列表

T01 [rigid:AC-2] 创建密码加密模块
  <action> 创建 src/auth/password.ts，实现 hashPassword / verifyPassword
  <verify> 运行 pnpm test src/auth/password.test.ts，全部通过
  <done>   AC-2 已覆盖，更新 claude-progress.json

T02 [rigid:AC-1] 实现 JWT 签发与验证
  <action> 创建 src/auth/jwt.ts，设置 expiresIn: '24h'
  <verify> 单元测试验证 token 过期时间为 24h
  <done>   AC-1 已覆盖

T03 [flexible] 集成到 UserService
  <action> 在 src/services/user.ts 中调用 password + jwt 模块
  <verify> 集成测试通过
  <done>   更新 progress

T04 [flexible] 更新 API 路由
  <action> 添加 POST /api/auth/login 路由
  <verify> e2e 测试通过
  <done>   特性完成，触发 harness:verify

### 不做的事（out_of_scope）
- OOS-1: 不实现 OAuth 第三方登录

### 风险点
- T02 依赖 JWT_SECRET 环境变量已配置
```

**覆盖检查**：所有 rigid 约束必须被至少一个 `[rigid:xxx]` 任务覆盖。如有未覆盖的 rigid 条目，规划不完整，需补充任务。

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
- [ ] 每个任务有完整的 `<action>` / `<verify>` / `<done>` 三段
- [ ] 所有 rigid 约束（acceptance_criteria + out_of_scope + forbidden_patterns）被至少一个任务覆盖
- [ ] 没有任何任务描述是"实现 X 功能"这种模糊表述
- [ ] out_of_scope 明确列出
- [ ] 依赖顺序清晰（有依赖的任务排在被依赖任务之后）
- [ ] 总任务数 ≤ 15（超过说明特性太大，应该拆分到 features.json）
- [ ] [rigid] 任务不可被标记为"跳过"或"延后"
