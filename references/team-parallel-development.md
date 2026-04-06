# 多人全栈团队并行开发指南

> 综合 Anthropic Agent Teams 官方文档、OpenAI Codex 团队实践、C 编译器并行 Agent 压测案例，
> 聚焦：**如何通过 features.json 设计和工具选择，实现多人全栈团队的效率最大化。**
>
> 更新：2026-04-06

---

## 核心洞见：并行的前提是"独立性"

从三个规模迥异的真实案例里，有一个反复出现的教训：

> **并行化失败的原因几乎从不是 Agent 能力不足，而是任务切割方式导致了隐性依赖。**

**C 编译器项目（16 Agent 并行压测）**：最初让所有 Agent 同时攻 Linux 内核时彻底失败——每个 Agent 遇到同样的 Bug，然后互相覆盖对方的修复。解决方案是让每个 Agent 负责不同的文件集，并引入基于文件锁的任务认领机制。

**OpenAI Codex 团队（3 人 → 7 人）**：早期进展慢，不是模型不行，是"环境规格不足（underspecified）"。团队扩大到 7 人后吞吐量持续提升——说明 Harness 的质量放大了人效，而不是人数本身。

**结论**：并行开发的投入应该优先用于"切割任务的方式"，而不是"增加人手"。

---

## 一、features.json 的并行支持升级

当前基础骨架适合单人流程，支持多人并行需要增加几个关键字段：

### 完整 Schema

```json
{
  "project": "用户协作平台",
  "updated": "2026-04-06",
  "coordination": {
    "max_parallel": 5,
    "worktree_mode": true,
    "claim_strategy": "git-commit-race"
  },
  "features": [
    {
      "id": "F-001",
      "title": "用户认证模块",
      "status": "in_progress",
      "priority": "high",
      "layer": "backend",
      "owner": "simon",
      "worktree": "feature-auth",
      "files_owned": [
        "src/auth/",
        "src/middleware/auth.ts",
        "tests/auth/"
      ],
      "depends_on": [],
      "blocks": ["F-003", "F-005"],
      "description": "JWT 认证 + session 管理。API key 在 .env JWT_SECRET。失败时返回 401，不抛异常。token 有效期 7 天，refresh token 30 天。",
      "acceptance": [
        "登录接口返回 access_token + refresh_token",
        "过期 token 返回 401 而非 500",
        "所有测试通过：pnpm test src/auth"
      ]
    },
    {
      "id": "F-002",
      "title": "用户管理 UI",
      "status": "planned",
      "priority": "medium",
      "layer": "frontend",
      "owner": "unassigned",
      "worktree": null,
      "files_owned": [
        "src/pages/users/",
        "src/components/UserCard.tsx",
        "src/components/UserTable.tsx"
      ],
      "depends_on": ["F-004"],
      "blocks": [],
      "description": "用户列表、搜索、分页。使用已有的 DataTable 组件（src/components/DataTable.tsx）。API 接口见 docs/api/users.md。",
      "acceptance": [
        "列表支持按 email/name 搜索",
        "分页每页 20 条",
        "E2E 测试通过：pnpm test:e2e users"
      ]
    },
    {
      "id": "F-003",
      "title": "基于角色的权限控制",
      "status": "planned",
      "priority": "high",
      "layer": "backend",
      "owner": "unassigned",
      "worktree": null,
      "files_owned": [
        "src/permissions/",
        "src/middleware/rbac.ts"
      ],
      "depends_on": ["F-001"],
      "blocks": ["F-002"],
      "description": "角色：admin / member / viewer。权限矩阵见 docs/design/rbac.md。",
      "acceptance": [
        "viewer 无法访问写接口",
        "权限检查失败返回 403"
      ]
    }
  ]
}
```

### 新增字段说明

| 字段 | 作用 | 并行重要性 |
|------|------|-----------|
| `owner` | 任务归属，防止两人同时认领 | ⭐⭐⭐ 最关键 |
| `files_owned` | 文件所有权边界 | ⭐⭐⭐ 避免合并冲突的根本手段 |
| `worktree` | 对应的 git worktree 名称 | ⭐⭐ 支持 worktree 隔离模式 |
| `depends_on` / `blocks` | 显式依赖图 | ⭐⭐⭐ 让可并行的任务一眼可见 |
| `layer` | frontend / backend / infra | ⭐ 按层分工时的过滤依据 |
| `acceptance` | 验收标准 | ⭐⭐ 减少 Agent 需要询问人类的次数 |
| `coordination.max_parallel` | 同时进行的最大任务数 | ⭐ 成本控制 |

---

## 二、任务认领机制：防止重复领取

### 方案 A：Git Commit Race（推荐，无需额外工具）

利用 Git 的同步机制天然防止两人同时认领：

```bash
# 认领任务的标准流程
git pull origin main                      # 先拉最新，确保 owner 字段是最新状态
# 检查 F-002 的 owner 是否仍为 unassigned
# 如果是，编辑 features.json 把 owner 改为自己的名字
git add docs/features.json
git commit -m "claim(F-002): alice 认领用户管理 UI"
git push origin main                      # 立即推送，先到先得
# 如果 push 被拒（别人抢先），则 pull 后重新检查
```

这个模式的关键是：**认领动作本身就是一次 git commit + push**，先推的人赢，后推的人会看到 pull 后 owner 已被占用。

### 方案 B：Agent Teams 共享任务列表（自动协调）

Claude Code v2.1.32+ 的 Agent Teams 功能内置了 task list + file locking：

```text
# 启动多 Agent 团队，让 Agent 自动认领和协调
Create an agent team to implement these 5 features.
Each teammate claims tasks from features.json and works independently.
No two teammates should touch the same files_owned list.
```

任务状态自动维护：`pending → in_progress → done`，完成时自动解锁依赖任务。

### 方案 C：文件锁（适合 CI/CD 自动化场景）

参照 C 编译器项目的做法：

```bash
# 认领 F-002
touch .claude/locks/F-002.lock
git add .claude/locks/F-002.lock
git commit -m "lock: claim F-002"
git push origin main

# 完成后解锁
git rm .claude/locks/F-002.lock
git commit -m "unlock: F-002 done"
git push origin main
```

---

## 三、三种分工模型

### 模型 A：按层切割（Layer Ownership）

每人在一个 Sprint 内专注一层，并行度最高：

```
Simon  → backend features（F-001, F-003, F-007）
Alice  → frontend features（F-002, F-006, F-008）
Bob    → infra/devops（F-004, F-009）
```

**优点**：文件几乎不重叠，合并冲突最少，Agent 可以真正并行运行。

**适用场景**：有明确前后端分离架构的项目，Sprint 内特性较多时。

**注意**：全栈工程师"只碰后端"的心理阻力在 Agent 驱动开发时会显著降低——因为个人工作重心是 review 和方向决策，而不是亲自写代码。

### 模型 B：按特性切割（Feature Ownership）

每人完整负责一个端到端特性（从 API 到 UI），用 `files_owned` 严格隔离文件边界：

```
Simon → F-001 认证（src/auth/ + src/pages/login/）
Alice → F-002 用户管理（src/pages/users/ + src/api/users/）
Bob   → F-004 基础设施（infra/ + CI 配置）
```

**优点**：每人保持全栈感，feature 完整性好。

**适用场景**：特性之间共享代码较少，团队成员喜欢独立负责完整功能时。

**注意**：如果两个特性都需要改 `BaseController` 或 `api/types.ts` 等共享文件，需要提前协商或串行化这部分工作。

### 模型 C：Planner-Coder-Reviewer 三角色（质量优先）

Anthropic 最新博客推荐的模式，专门解决"AI 自己审查自己的输出"问题：

```
规划者（Planner）  → 维护 features.json，拆解需求，做架构决策
执行者（Coder）    → 启动 Agent 实现代码，最大化 Agent 并行度
评估者（Reviewer） → 独立审查 Agent 输出，不让创建者自评
```

在 3 人全栈团队里，三个角色可以每个 Sprint 轮换，避免固化。

**优点**：质量门禁最高，适合有明确 PR review 要求的团队。

**适用场景**：对代码质量要求高，或正在建立质量文化的早期阶段。

---

## 四、Git Worktree 隔离：多人并行的基础设施

Git Worktree 是多人并行开发的技术基础，它让多个 Agent 会话同时运行而不互相干扰：

```bash
# 每人（或每个特性）一个独立的 worktree
claude --worktree feature-auth       # Simon 的工作空间
claude --worktree feature-users      # Alice 的工作空间
claude --worktree infra-setup        # Bob 的工作空间
```

Worktree 创建在 `.claude/worktrees/<name>/`，每个都有自己的分支，但共享同一个 `.git` 历史和远端连接。

**关键配置**：

```bash
# 在 .gitignore 里忽略 worktree 目录
echo ".claude/worktrees/" >> .gitignore

# 在 .worktreeinclude 里声明需要复制的本地配置
cat > .worktreeinclude << EOF
.env
.env.local
config/local.json
EOF
```

**Worktree 与 features.json 的联动**：features.json 中的 `worktree` 字段记录对应的 worktree 名称，Agent 启动时读取这个字段，自动进入正确的 worktree。

---

## 五、减少人与 Agent 依赖的设计原则

> Agent 等待人类输入 = 效率归零。目标是让 Agent 在人类离开时也能持续推进。

### 原则 1：在 features.json 的 description 里预答 Agent 的问题

提前回答 Agent 在实现过程中最可能问的问题：

```json
{
  "id": "F-006",
  "title": "邮件通知",
  "description": "用 SendGrid 发送注册确认邮件。API key 在 .env SENDGRID_KEY。模板在 src/templates/email/welcome.html。失败时重试 3 次（指数退避），超时后写入 dead_letter_queue 表，不抛异常到调用方。测试时用 mailtrap：.env.test 里有配置。"
}
```

description 写得越具体（使用哪个库、配置在哪、失败时怎么处理），Agent 需要打断你询问的次数就越少。

### 原则 2：acceptance 字段是可执行的验收条件

```json
"acceptance": [
  "pnpm test src/email -- --coverage（覆盖率 > 80%）",
  "发送失败时 dead_letter_queue 表有记录",
  "不影响注册接口的响应时间（< 200ms）"
]
```

acceptance 写成可验证的条件，Agent 完成后可以自我验证，不需要人工逐一检查。

### 原则 3：depends_on 让 Agent 自己判断是否可以开始

在 CLAUDE.md 中写入这条规则后，Agent 每次启动都会自动检查依赖：

```markdown
## features.json 协作规则
- 开始任何任务前，确认 depends_on 中所有 feature 的 status 为 done
- 确认自己要修改的文件不在其他 in_progress 任务的 files_owned 列表中
- 任务完成后，将 blocks 中的任务 status 从 planned 改为 ready（唯一允许 Agent 写 features.json 的场景）
```

### 原则 4：Notification Hook 让人在等待时不需要盯屏幕

```json
// ~/.claude/settings.json
{
  "hooks": {
    "Notification": [{
      "matcher": "idle_prompt",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Agent 完成，等待下一步\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

---

## 六、两种协调模式对比

### 模式 A：Agent Teams（自动协调，适合单人监督多 Agent）

```text
一个会话作为 Team Lead，自动分发任务，Agent 之间可以直接通信：

Lead → 维护 task list，分配工作
Teammate 1 → 认领 F-001，完成后通知 Lead
Teammate 2 → 认领 F-002，同时进行
Teammate 3 → 等待 F-001 完成后认领 F-003
```

**Token 成本**：每个 teammate 是独立的上下文窗口，成本线性叠加。3-5 个 teammate 是最佳实践。

**适用**：单人工程师监督多 Agent 并行；任务之间需要 Agent 互相讨论时（比如架构决策、竞争假设调试）。

### 模式 B：Git Worktrees 手动并行（人工协调，适合多工程师团队）

```text
每个工程师在自己的 worktree 里运行独立的 Claude Code 会话：

Simon:  claude --worktree feature-auth    （处理 F-001）
Alice:  claude --worktree feature-users   （处理 F-002）
Bob:    claude --worktree infra-setup     （处理 F-004）
```

**Token 成本**：每人独立，互不影响，成本可控。

**适用**：多工程师团队；任务之间独立性高；需要人工 review 和方向控制时。

### 对比总结

| 维度 | Agent Teams | Git Worktrees 手动 |
|------|------------|-------------------|
| 协调方式 | Agent 自动协调 | 工程师人工协调 |
| Token 成本 | 较高（多上下文） | 低（各自独立） |
| Agent 间通信 | 支持（mailbox） | 不支持 |
| 控制粒度 | 较低 | 高 |
| 适合任务 | 需要讨论/辩论的复杂任务 | 边界清晰的独立任务 |
| 现阶段成熟度 | Experimental | Stable |

---

## 七、真实效率数据参考

| 团队 | 规模 | 配置 | 吞吐量 |
|------|------|------|--------|
| OpenAI Codex 团队 | 3 人 | 不限 Agent 数 | 3.5 PR/工程师/天 |
| OpenAI Codex 团队（扩张） | 7 人 | Harness 更完善 | 吞吐量持续提升 |
| Stripe Minions | 企业规模 | 400+ MCP 工具 | 1000+ PR/周 |
| Boris Cherny（个人，CC 创作者） | 1 人 | 10-15 并行 worktree | 未公开具体数字 |
| C 编译器压测 | 1 人监督 16 Agent | Docker 隔离 + 文件锁 | 2000 次会话，10 万行 |
| 社区报告（Worktree 模式） | 小团队 | 3-5 并行 worktree | 约 18% 吞吐提升 |

**实践上限**：Boris Cherny 推荐 **3-5 个并行 worktree**，这是人类注意力可以合理覆盖的上限；超过后，上下文切换的认知成本开始抵消并行收益。

---

## 八、一个具体的 Sprint 工作流

以 3 人全栈团队、一周 Sprint 为例：

### Sprint 开始（周一上午，30 分钟）

```bash
# 1. 团队同步，更新 features.json
#    - 确认各 feature 的 depends_on 关系
#    - 每人认领 1-2 个 feature（git commit race）
#    - 检查 files_owned 无重叠

# 2. 每人创建自己的 worktree
claude --worktree feature-auth    # Simon
claude --worktree feature-users   # Alice
claude --worktree infra-k8s       # Bob

# 3. 在自己的 worktree 里启动 Agent
# 让 Agent 读取 features.json 和 architecture.md，建立上下文
```

### Sprint 中（周一-周四，异步进行）

```bash
# 每人在自己的 worktree 里让 Agent 持续推进
# 依赖就绪时（F-001 done → F-003 变为 ready），Slack 通知相关人

# 每天 15 分钟 standup：
# - 昨天 Agent 完成了什么
# - 今天 Agent 计划做什么
# - 有无 blocker（通常是跨文件依赖冲突）
```

### Sprint Review（周五下午，1 小时）

```bash
# 1. 各 worktree 的 PR merge 到 main
git worktree list        # 确认所有 worktree 状态
# 逐一 review PR，Agent 生成的代码需要人工确认关键路径

# 2. Harness 改进（10 分钟）
# 回顾本周 Agent 失败案例 → 每个失败对应一条 features.json 或 CLAUDE.md 改进

# 3. 更新 features.json
# 把 done 的 feature 标记为 done，准备下周 Sprint
```

---

## 九、反模式与常见陷阱

| 反模式 | 现象 | 正确做法 |
|--------|------|---------|
| 隐式文件依赖 | 两人的 files_owned 有重叠，产生合并冲突 | 任务切割时先检查 files_owned，共享文件串行化 |
| description 过于模糊 | Agent 反复打断人类询问细节 | description 预答 Agent 最可能问的 3 个问题 |
| depends_on 未声明 | Agent 在依赖未就绪时开始实现，后来发现接口变了 | 用 depends_on/blocks 显式声明所有依赖 |
| 无限增加 teammate 数量 | Token 成本暴涨，协调开销超过并行收益 | 3-5 人/Agent 是上限，优先提高任务独立性 |
| 忽略 acceptance 字段 | Agent 完成后无法自我验证，需要人工逐一检查 | acceptance 写成可执行的命令（pnpm test） |
| 同一文件两人同时修改 | 合并地狱 | files_owned 是硬约束，不是建议 |

---

## 十、与 harness-init 的集成

如果在项目初始化时启用多人协作模式，`harness-init` 应该在 Phase 5 生成支持并行的 features.json，并在 CLAUDE.md 中写入以下规则：

```markdown
## 多人并行协作规则
- 开始任务前：depends_on 中所有 feature 必须为 done
- 开始任务前：确认 files_owned 不与其他 in_progress 任务重叠
- 认领任务：修改 owner 字段 → git commit → git push（先到先得）
- 完成任务：将 blocks 中的任务 status 改为 ready（Agent 写 features.json 的唯一允许场景）
- 文件冲突：立即停止，在 claude-progress.json notes 里记录，由人类决策
```

---

## 参考来源

| 来源 | 内容 |
|------|------|
| [Claude Code Agent Teams 官方文档](https://code.claude.com/docs/en/agent-teams) | Agent Teams 架构、task list、mailbox 机制 |
| [Claude Code Git Worktrees 官方文档](https://code.claude.com/docs/en/common-workflows) | Worktree 并行模式、.worktreeinclude、--worktree 标志 |
| [Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | 16 Agent 并行压测，文件锁、任务认领机制 |
| [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) | 3人→7人扩展，知识库架构，层级依赖强制执行 |
| HarnessEngineering.md 第三章、第五章 | OpenAI Codex 量化成果，团队实践落地路径 |
