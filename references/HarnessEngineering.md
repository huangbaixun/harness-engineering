# Harness Engineering：AI 驱动工程团队完整实践手册

> 综合 Anthropic · InfoQ · Hacker News · X.com 实践精华 + Claude 工具针对性指导
>
> 2026 年 3 月

---

本手册分两部分：**第一部分**系统整理 Anthropic 工程博客、InfoQ、Hacker News 及 X.com 的 Harness Engineering 核心实践；**第二部分**以 Claude Code CLI 和 Claude Agent SDK 为具体载体，提供可直接使用的配置模板、Hook 脚本和多 Agent 编排模式。

---

# 第一部分：核心概念与多来源实践综合

---

## 一、什么是 Harness Engineering

> *Harness Engineering 是 2026 年软件工程领域最重要的新兴范式转变——将工程师的核心工作从「编写代码」转变为「设计让 AI 智能体可靠工作的环境」。*

「Harness」（驾驭架）源自马具比喻：模型是骏马，强大但不自知方向；Harness 是缰绳、鞍具和衔铁——引导力量朝正确方向。

> **📖 Mitchell Hashimoto（Terraform/HashiCorp 创始人）定义**
>
> 「每当发现智能体犯了一个错误，就花时间设计一个解决方案，确保这个错误永远不再发生。」

### 三个演进阶段

| 阶段 | 时间 | 核心关注点 |
|------|------|-----------|
| Prompt Engineering | 2022–2024 | 优化单次推理的指令质量 |
| Context Engineering | 2025 | 确保模型在推理时获得正确的上下文 |
| **Harness Engineering** | **2026–** | **在系统层面架构约束、反馈循环和验证机制** |

> **🧠 Hacker News 核心洞见**
>
> 「更准确的理解：AI = LLM + Harness 构成的控制论系统。当 Harness 改进所带来的效益与模型本身改进相当时，二者必须被同等重视。」*(logicprog, HN)*

### 1.1 Harness 的四大组成要素

| 要素 | 内容 | 核心来源 |
|------|------|---------|
| **上下文工程** | 持续充实的知识库（AGENTS.md、设计文档、架构图）及动态可观察性数据接入 | OpenAI / Anthropic |
| **架构约束** | 通过 Linter 和结构化测试机械性强制执行依赖层级、模块边界、数据结构规范 | OpenAI Codex 团队 |
| **验证与反馈** | CI 管道、单元测试、集成测试；每次失败都触发 Harness 改进而非手动修复 | Mitchell Hashimoto |
| **垃圾回收** | 周期性运行清理智能体，检测文档陈旧、架构漂移、代码熵增，自动提交修复 PR | OpenAI / Martin Fowler |

---

## 二、Anthropic 实践：长周期任务驾驭架设计

> 📌 来源：Anthropic Engineering Blog — *"Effective harnesses for long-running agents"*（2025.11）& *"Harness design for long-running application development"*（2026）

### 2.1 核心挑战：记忆断层

每次新会话开始时，Agent 对之前发生的事情没有任何记忆。典型失败模式有两种：

1. **贪婪执行模式**：Agent 试图一次性完成整个任务，导致上下文溢出，下一会话面对半完成且无文档的代码
2. **过早收工模式**：后期会话看到「已有进展」便宣告完成，留下未实现的功能

### 2.2 双智能体解决方案

> **🏗️ 初始化智能体（Initializer Agent）**
>
> 仅首次运行，建立 Git 仓库结构、创建 JSON 格式特性清单、生成进度跟踪文件，为后续会话奠定稳固基础。

> **⚙️ 编码智能体（Coding Agent）**
>
> 每次会话仪式性启动：确认位置 → 读进度文档 → 检视特性清单 → 跑现有测试 → 才开始实现。每次完成一个特性后留下干净代码状态供下一会话接手。

### 2.3 结构化交接物

- **JSON 格式特性清单**：比 Markdown 更受 Agent 尊重，不会被轻易误改
- **Git 历史**：可被后续会话读取以了解已完成的工作
- **进度文件**：明确记录「已完成 / 进行中 / 待处理」状态

### 2.4 GAN 启发的三智能体架构（进阶）

| 角色 | 职责 | 关键约束 |
|------|------|---------|
| **规划智能体（Planner）** | 将高层 Brief 转化为产品规格，保持高层次 | 避免引入实现错误级联 |
| **生成智能体（Generator）** | 按冲刺分批实现功能，每批可验证 | 单点突破，降低上下文污染 |
| **评估智能体（Evaluator）** | 用 Playwright 对运行中应用交互测试，四维度打分 | 分离创建者与评审者角色 |

> **💰 实证数据**
>
> - 无评估架构：20 分钟，$9——产出不可用功能
> - 完整三智能体 Harness：6 小时，$200——交付功能完善、UX 显著更好的应用
>
> 评估智能体捕获了路由顺序错误、缺失实体连线、工具实现不当等生成智能体「自信发布」的问题。

### 2.5 关键原则

- **上下文重置优于无限压缩**：对于上下文焦虑型模型，定期清空并结构化交接比一直累积更有效
- **永远不要让创建者独立评审自己的产出**：模型无法可靠地自我评估，分离生成与评估角色是可靠性的基础
- **随模型进化精简 Harness**：当新模型自身解决了某类失败，主动删除相应脚手架

---

## 三、OpenAI 实践：百万行代码零人工编写

> 📌 来源：OpenAI Engineering Blog *"Harness engineering: leveraging Codex in an agent-first world"* (2026.02) · InfoQ 报道

OpenAI Codex 团队用五个月，三名工程师引导 Codex 智能体生成超过 100 万行代码的生产级产品，零人工手写代码。

### 3.1 核心工程洞见

「早期进展慢，不是 Codex 能力不足，而是**环境规格不足（underspecified）**。失败时，解决方案几乎从不是「更努力尝试」，而是问：缺少了什么能力，如何让它对智能体既可解读（legible）又可强制执行（enforceable）？」

### 3.2 知识库架构：地图而非百科全书

❌ **反模式** — 一个「巨型 AGENTS.md」：
- 上下文占用大，重要约束被淹没
- 智能体局部模式匹配而非全局导航
- 即刻陈旧，无法被机械验证

✅ **正确模式** — AGENTS.md 约 100 行作为「目录」，指向 `docs/` 目录下结构化知识库：
- `docs/architecture.md` — 架构图（领域地图）
- `docs/design/` — 设计规格（执行计划）
- `docs/quality.md` — 质量评分文档（各域现状）
- `docs/decisions/` — 决策记录（ADR）

所有文档交叉链接，由 Linter 和 CI 强制校验一致性。

### 3.3 强制执行的架构层级

依赖关系单向流动，通过自定义 Linter 和结构化测试机械执行：

```
Types  →  Config  →  Repo  →  Service  →  Runtime  →  UI
```

每层只能从左侧层引入依赖——由结构测试强制，不是建议。

| 层 | 职责 | 可依赖 | 典型内容 |
|----|------|--------|---------|
| **Types** | 全局共享的数据结构、接口、枚举、常量 | 无 | `User`, `OrderStatus`, `MAX_RETRY` |
| **Config** | 读取环境变量、解析配置，统一对外暴露 | Types | `dbConfig`, `appConfig` |
| **Repo** | 数据库/缓存/外部存储的唯一读写出入口 | Types, Config | `findUserById()`, `saveOrder()` |
| **Service** | 业务逻辑、校验、事务编排 | Types, Config, Repo | `promoteToAdmin()`, `placeOrder()` |
| **Runtime** | 将 Service 暴露给外部：HTTP 路由、队列消费者、定时任务 | 以上所有 | `handleRequest()`, `consumeEvent()` |
| **UI** | 前端组件与页面，只通过 API 与后端通信 | Types + Runtime API | React 组件、页面路由 |

**对 Agent 的意义**：层级约束让 Agent 无法在 UI 里直接写 SQL、无法在 Service 里散落 `process.env`，结构测试在 CI 中自动拦截跨层错误引用，违规即 Build 失败。

### 3.4 量化成果

| 指标 | 数值 | 背景 |
|------|------|------|
| 代码产出 | 超过 100 万行，1500+ 个 PR | 5 个月 |
| 人均 PR/天 | 3.5 个 PR / 工程师 / 天 | 初始 3 人团队 |
| 速度变化 | 随团队扩大到 7 人，吞吐量持续提升 | 更好 Harness 放大了人效 |
| 相对时效 | 约为手写代码时间的 1/10 | OpenAI 估算 |

---

## 四、社区智慧：Hacker News 与 X.com 实践洞察

> 📌 来源：HN — *"Improving 15 LLMs at Coding in One Afternoon. Only the Harness Changed"* / *"Effective harnesses for long-running agents"*

### 4.1 Hacker News 核心讨论

> **🎯「模型是护城河，Harness 是桥梁」**
>
> 「『酷炫演示』和『可靠工具』之间的差距，不是模型魔法，而是在工具边界上认真、枯燥的经验性工程。」*(chrisweekly, HN)*

> **💸「Token 是资源，像 CPU/RAM 一样管理」**
>
> 「用 Claude Code `/cost` 命令看到会话的美元成本，这是衡量 CLAUDE.md 和各类 Harness 组件的好基准。」*(chasd00, HN)*

> **⚠️「MCP 过度使用是陷阱」**
>
> 「MCP 被过度用于一切场景——用百亿参数模型去决定如何调用，通常完全没必要。MCP 是让一切看起来都像钉子的锤子。」*(robbomacrae, HN)*

### 4.2 Mitchell Hashimoto 六阶段 AI 采用路径

> 📌 来源：mitchellh.com *"My AI Adoption Journey"* · X.com @mitchellh

| 阶段 | 内容 | 关键洞见 |
|------|------|---------|
| 阶段 1 | 从 Chat 界面切换到 Agent（工具调用循环体） | Chat 界面不适合编码任务 |
| 阶段 2 | 探索 Agent 擅长与不擅长的边界 | 了解边界比盲目使用更有价值 |
| 阶段 3 | 效率接近手工——不更快但不更慢 | 强迫自己完成相同任务两次以校准 |
| 阶段 4 | 块式时间法：下班前 30 分钟启动 Agent 异步工作 | 深研、并行探索、Issue 分类最有价值 |
| **阶段 5 ★** | **构建 Harness：每次 Agent 犯错，工程化防止再犯** | **这是核心阶段，效益复利增长** |
| 阶段 6 | 持续运行 Agent——若无 Agent 在跑，问「有何任务适合」 | Agent 背景运行占工作日 10–20% |

### 4.3 Stripe「Minions」企业规模实践

- 每周产出超过 **1000 个合并 Pull Request**
- 开发者在 Slack 发布任务，Agent 写代码、通过 CI、开 PR——全程无交互
- Agent 在隔离的「devbox」中运行，接入超过 **400 个内部工具**的 MCP 服务器
- **关键洞见**：给 Agent 与人类工程师相同的工具和上下文，而不是事后补丁式集成

---

## 五、团队实践指导：逐步落地路径

### 5.1 立刻可做（Day 1）

1. **创建 AGENTS.md（或 CLAUDE.md）** — 技术栈、测试命令、禁止规则、编码约定，严格控制在 60 行以内
2. **审查 Pre-commit Hooks** — 确保 Linter、格式化器、类型检查在本地运行——为 Agent 提供即时反馈
3. **建立「失败即改进」反射** — Agent 犯错时，第一反应是「如何让它永不再犯？」然后更新配置或添加工具

### 5.2 本周完成（Week 1）

1. **建立 `docs/` 知识库结构** — 创建架构图、领域地图、ADR；将 AGENTS.md 精简为指向这些文档的目录
2. **引入初始化+编码双 Agent 模式** — 初始化 Agent 建立 JSON 特性清单和进度文件；编码 Agent 每次启动先读取状态
3. **测量基线** — 记录每次会话的 Token 成本，建立对比基准

### 5.3 本月建立（Month 1）

1. **机械化架构约束** — 用自定义 Linter 或结构测试强制执行依赖层级，CI 自动失败
2. **分离生成与评估角色** — 引入独立的评估 Agent，永远不让创建者独立评审自己的输出
3. **建立「垃圾回收」机制** — 定期运行清理 Agent，扫描陈旧文档、架构漂移，自动提 PR 修复
4. **构建 Skills 库** — 将高频任务封装为独立指令文件，按需加载

> **🔁 核心循环**
>
> Agent 失败 → 识别缺失的能力 → 工程化修复（更新文档 / 添加 Linter / 构建工具）→ 该失败**永不再发生**。
>
> 这个循环是 Harness Engineering 的本质。

### 5.4 持续演进原则

- **随模型迭代精简 Harness**：新模型发布后主动删除已不必要的脚手架
- **约束赋能，而非限制**：架构约束越严格，Agent 产出越可靠——反直觉但实证支持
- **上下文是稀缺资源**：批判性审视每个加入上下文窗口的内容
- **保持人类在决策节点**：不可逆操作、安全变更，Harness 应自动引入人工审批

---

## 六、团队 Harness 健康度检查清单

### 6.1 Agent 可解读性评分（OpenAI Scorecard）

| 评估维度 | 检查问题 | 操作建议 |
|---------|---------|---------|
| Bootstrap Self-Sufficiency | Agent 能否无人工干预完成首次配置自测？ | 检查 init 脚本是否自动化 |
| Task Entrypoints | 入口任务是否清晰可发现？ | 检查 CLAUDE.md 中任务导航 |
| Validation Harness | CI / 测试能否自动验证 Agent 输出？ | 检查 CI 覆盖率与速度 |
| Lint + Format Gates | 格式检查是否在 pre-commit 自动运行？ | 检查是否有本地 Hook |
| Agent Repo Map | 仓库是否有清晰的领域架构图？ | 检查 docs/architecture.md |
| Structured Docs | 设计文档是否有结构、版本、交叉链接？ | 检查 docs/ 目录完整性 |
| Decision Records | 架构决策是否有 ADR 记录并维护？ | 检查 adr/ 或 docs/decisions/ |

### 6.2 每周 Harness 维护仪式

1. **失败分析（10 分钟）** — 回顾本周 Agent 失败案例，每个失败转化为一条 Harness 改进
2. **文档新鲜度检查（5 分钟）** — 确认 CLAUDE.md 和 docs/ 中没有陈旧规则或已失效链接
3. **成本基线对比（5 分钟）** — 对比本周 vs 上周 Token 使用趋势，识别异常增长
4. **Harness 精简（按需）** — 随模型更新，评估并删除不再必要的脚手架组件

---

# 第二部分：Claude 工具针对性实践指导

> *以 Claude Code CLI · Claude Agent SDK 为例的工程实战手册*

---

## A. Claude Code 驾驭架六层模型

> *Claude Code 的 Harness 不是单一配置文件，而是六个相互协作的层。理解各层职责是避免「配置越多越混乱」的关键。*

| 层级 | 组件 / 位置 | 核心职责 |
|------|-----------|---------|
| ① 记忆层 | `CLAUDE.md`（项目根 / 子目录 / `~/.claude/CLAUDE.md`） | 静态知识：架构约定、禁止规则、测试命令——Agent 始终可见 |
| ② 规则层 | `.claude/settings.json`（权限、模型、输出风格） | 确定性行为：settings.json 控制的行为不会被 Agent 遗忘或忽略 |
| ③ 技能层 | `.claude/skills/` + `.claude/commands/` | 按需知识：Skills 自动激活，Slash Commands 手动触发 |
| ④ 智能体层 | `.claude/agents/`（专用 Subagent 定义） | 上下文隔离：将重读文件 / 大输出任务委托出去，主线程保持干净 |
| ⑤ 钩子层 | Hooks（PreToolUse / PostToolUse / Stop 等） | 确定性强制：不依赖模型判断，机械性保障 |
| ⑥ 工具层 | MCP Servers（外部服务接入） | 能力扩展：数据库、GitHub、Slack、Playwright 等，按需接入 |

> **⚠️ 单层失效陷阱**
>
> CLAUDE.md 规则单独使用会被偶尔忽略；Hooks 单独使用无法处理判断性任务；Settings.json 单独使用缺乏上下文。**三者协同才能真正有效。**

---

## B. CLAUDE.md 工程化设计

> *ETH Zurich 研究：AI 自动生成的 CLAUDE.md 导致性能下降并多消耗 20% Token；人工编写且精简的文件才真正有效。*

### B.1 层级覆盖机制

```
~/.claude/CLAUDE.md             ← 个人全局规则（所有项目适用）
project-root/CLAUDE.md          ← 项目级规则（团队共享，纳入 Git）
project-root/backend/CLAUDE.md  ← 子目录规则（追加，非覆盖）
project-root/frontend/CLAUDE.md
```

### B.2 精简模板（≤60 行原则）

```markdown
# Project: [名称] — CLAUDE.md

## 技术栈
- TypeScript strict mode, Node.js 22, React 18, PostgreSQL via Prisma
- 包管理器：pnpm（禁止使用 npm / yarn）

## 关键命令
- 测试：`pnpm test`  |  监听：`pnpm test:watch`
- 构建：`pnpm build`  |  类型检查：`pnpm typecheck`
- 数据库迁移：`pnpm db:migrate`

## 架构约定
- 依赖方向：types → config → repo → service → api → ui（禁止逆向）
- 所有公共 API 必须有 JSDoc 注释
- 新代码必须有对应测试（覆盖率 >80%）

## 禁止规则
- 永远不要删除数据库迁移文件
- 永远不要在代码中硬编码 secret / API key
- 提交前必须通过 typecheck（见 Stop Hook）

## 更多上下文
- 架构图：docs/architecture.md
- 设计决策：docs/decisions/
- 长任务进度：docs/claude-progress.json
```

✅ **好的规则示例**：「永远不要删除迁移文件」——具体、可验证、对应过去真实的 Agent 失败

❌ **坏的规则示例**：「写高质量代码」——模糊、无法验证、消耗 Token 却不产生约束力

### B.3 三种机制分工

| 机制 | 适用场景 |
|------|---------|
| `CLAUDE.md`（静态） | 团队共享约定；纳入 Git；用 `/init` 生成初稿后人工精简 |
| Auto Memory（动态） | Claude 自动保存会话学习（构建命令、调试洞见）；跨会话持久；用 `/memory` 管理 |
| `settings.json`（确定性） | 凡是「必须发生、不依赖 Claude 判断」的行为（如 `attribution.commit`）放此处 |

### B.4 docs/architecture.md 详解

> *这是 CLAUDE.md 里 `- 架构图：docs/architecture.md` 这行链接指向的文件。它的核心目标只有一个：让 Agent 在新会话开始时，能快速建立对整个系统的空间感知——知道代码在哪里、模块怎么分、去哪里找什么。*

#### 典型内容结构

**1. 系统全局地图**

用最简洁的语言说清楚「这是个什么系统、有哪几块」：

```markdown
## 系统概览

这是一个 SaaS 协作平台，用户可以创建项目、邀请成员、管理任务。
主要由三个子系统构成：

- **API 服务**：处理所有客户端请求（REST + WebSocket）
- **Worker 服务**：处理异步任务（邮件、通知、数据导出）
- **Admin 服务**：内部管理后台，仅内网可访问
```

**2. 目录结构说明**

告诉 Agent「每个目录放什么」，比 README 更精准：

```markdown
## 目录结构

src/
├── types/        # 共享类型定义、接口、枚举（无任何业务逻辑）
├── config/       # 配置读取，统一从这里获取环境变量
├── repo/         # 数据库访问层，只做 CRUD，不含业务判断
├── service/      # 业务逻辑层，所有核心计算在这里
├── runtime/      # 应用入口、路由注册、中间件
└── ui/           # 前端组件

tests/
├── unit/         # 单元测试，不启动数据库
├── integration/  # 集成测试，使用测试数据库
└── architecture/ # 架构约束测试（依赖方向检查）← 见下文

docs/
├── architecture.md        ← 本文件
├── decisions/             # 架构决策记录（ADR）
├── design/                # 各功能模块的设计文档
└── claude-progress.json   # Agent 长任务进度追踪
```

**3. 层级依赖规则（最重要）**

把架构约束写清楚，让 Agent 知道边界在哪里。这是 CLAUDE.md 里「架构约定」一行的展开版：

```markdown
## 依赖方向规则

允许的依赖方向（只能向右引用：Agent有时候喜欢走捷径）：

  types → config → repo → service → runtime → ui

禁止规则：
- repo 层不能 import service 层（数据层不能有业务逻辑）
- types 层不能 import 任何其他层（纯粹的类型定义）
- ui 组件不能直接 import repo 层（必须经过 service）

跨切面关注点（auth、日志、feature flag）统一通过
Providers 接口注入，不能在各层之间直接传递。

这些规则由 tests/architecture/ 中的结构化测试自动验证。
违反规则时 CI 自动失败，错误信息包含具体修复方式。
```

**4. 关键模块说明**

对复杂模块做一句话解释，让 Agent 知道去哪找：

```markdown
## 关键模块

| 模块 | 路径 | 职责 |
|------|------|------|
| 认证 | src/service/auth/ | JWT 签发、刷新、撤销 |
| 权限 | src/service/permission/ | RBAC 规则，所有权限判断入口 |
| 通知 | src/service/notification/ | 邮件、站内信、Webhook 的统一发送 |
| 任务队列 | src/service/queue/ | 异步任务的入队和调度 |
| 文件存储 | src/repo/storage/ | S3 上传/下载的封装 |
```

**5. 外部依赖说明**

```markdown
## 外部依赖

| 服务 | 用途 | 接入位置 |
|------|------|---------|
| PostgreSQL | 主数据库 | src/repo/db/ |
| Redis | 会话缓存、队列 | src/repo/cache/ |
| S3 | 文件存储 | src/repo/storage/ |
| SendGrid | 邮件发送 | src/service/notification/ |
| Stripe | 支付处理 | src/service/billing/ |
```

**6. 指向更深层文档的链接**

```markdown
## 延伸阅读

- 认证系统详细设计 → docs/design/auth.md
- 支付流程时序图   → docs/design/billing-flow.md
- 数据库 Schema    → docs/design/schema.md
- 重要架构决策     → docs/decisions/
```

#### 写法原则

architecture.md 和 CLAUDE.md 有几条相同的反直觉要求：

| 原则 | 错误做法 | 正确做法 |
|------|---------|---------|
| **写给 Agent 看，不是写给人看** | 「这个大家都知道」 | 凡是影响 Agent 决策的信息都写明 |
| **精确优于详尽** | 「代码要写得优雅」 | 「所有 public 函数必须有 JSDoc，否则 lint 失败」 |
| **可验证优于可读** | 软性建议 | 写清楚「哪里会自动检查、违反了会怎样」 |
| **保持短小、用链接分层** | 所有内容塞进一个文件 | 本文件控制在 100–150 行，复杂子系统各自有 design 文档 |

> 这就是 OpenAI 强调的「地图而非百科全书」的具体落地——architecture.md 是索引，不是全书。

### B.5 docs/decisions/ 详解（ADR 架构决策记录）

> *architecture.md 里「重要架构决策 → docs/decisions/」这行链接指向的目录。它解决一个核心问题：Agent 没有历史记忆，每次会话从零开始。没有 ADR，它可能「好心」地把代码改成它认为更好的方式，结果破坏了当初的设计意图。*

#### 为什么 Agent 特别需要它

没有 ADR 时，代码里会存在大量「不明原因的约束」：

```
// 为什么这里不直接用 Redis，要绕一层 cache/？
// 为什么会话不用 JWT，要存数据库？
// 为什么这个接口要走消息队列而不是同步调用？
```

人类工程师可以去问同事，Agent 没有这个选项。它只能猜——而猜错的代价是破坏当初刻意为之的设计。

ADR 把这些「为什么」固化在仓库里，Agent 读到之后知道：**这是一个刻意的决定，不要改它。**

#### 单个 ADR 文件模板

文件名带编号和标题，如 `0012-use-redis-for-session.md`：

```markdown
# ADR-0012：使用 Redis 存储用户会话

**状态**：已采纳
**日期**：2025-11-03
**决策者**：@zhang-wei, @li-fang

---

## 背景

用户会话数据目前存在 PostgreSQL 里。随着 DAU 增长到 50 万，
每次请求都查一次数据库导致 P99 延迟超过 800ms，不可接受。

## 考虑过的选项

**选项 A：PostgreSQL + 连接池优化**
- 优点：不引入新组件，运维简单
- 缺点：会话读写是热点，连接池治标不治本

**选项 B：Redis**
- 优点：内存读写，延迟 <1ms；TTL 天然支持会话过期
- 缺点：需要配置持久化，多一个维护组件

**选项 C：JWT 无状态方案**
- 优点：彻底不需要存储
- 缺点：无法主动撤销 Token，安全团队明确反对

## 决策

选择选项 B（Redis）。会话数据是「读多写少、有过期时间」
的典型场景。安全团队要求保留主动撤销能力，排除了 JWT。

## 后果（对 Agent 有约束力）

- ❌ 禁止在 service 层直接 import Redis 客户端
  → 必须通过 src/repo/cache/ 的封装
- ❌ 禁止存储超过 10KB 的对象到 Redis
  → 大对象存 S3，Redis 只存引用 ID
- ✅ 会话 TTL 统一在 SessionRepo 里管理，不要分散硬编码
- 下次 review：DAU 超过 200 万时重新评估是否需要 Redis Cluster
```

**「后果」部分是 Agent 最需要读到的**——它把决策转化为可执行的约束，告诉 Agent「不要碰这里、必须走那里」。

#### 目录整体组织

```
docs/decisions/
├── README.md              ← 决策索引，列出所有 ADR 的一行摘要
├── 0001-monorepo.md
├── 0002-typescript.md
├── 0003-postgresql.md
├── 0012-redis-session.md
└── 0015-deprecate-rest.md ← 已废弃的决策同样保留
```

`README.md` 是 Agent 的入口，先读索引，再按需深入：

```markdown
# 架构决策索引

| 编号 | 标题 | 状态 | 日期 |
|------|------|------|------|
| 0001 | 采用 Monorepo 结构 | 已采纳 | 2024-03 |
| 0002 | TypeScript strict 模式 | 已采纳 | 2024-03 |
| 0012 | Redis 存储用户会话 | 已采纳 | 2025-11 |
| 0015 | 部分接口迁移 GraphQL | **已废弃** | 2025-08 |
```

**「已废弃」的决策同样重要**——让 Agent 知道「这条路走过、放弃了、原因在这里」，避免它重蹈覆辙。

#### 写作要点

| 要点 | 说明 |
|------|------|
| **背景要写触发条件** | 不是「我们想用 Redis」，而是「P99 延迟超过 800ms，不可接受」——Agent 需要知道约束的紧迫程度 |
| **必须列被否决的选项** | Agent 可能独立想到这些选项，看到它们被否决及原因，才不会再提 |
| **后果写禁止规则** | 用「❌ 禁止 X，必须走 Y」格式，比散文描述对 Agent 更有约束力 |
| **状态字段必须维护** | 决策被推翻时，把状态改为「已废弃」并说明原因，不要删文件 |
| **长度控制在一屏** | ADR 不是设计文档，核心内容 50–80 行足够，细节链接到 design/ |

#### 与其他文档的分工

```
CLAUDE.md          → 「禁止 service 层直接用 Redis」（规则本身）
architecture.md    → 「Redis 接入位置：src/repo/cache/」（位置信息）
docs/decisions/    → 「为什么这样设计、当时排除了什么、未来何时重新评估」（决策上下文）
docs/design/       → Redis 封装层的具体实现细节
```

四个文件各司其职，Agent 根据任务类型决定读哪里——实现新功能读 CLAUDE.md 和 architecture.md，遇到不理解的约束读 decisions/，需要了解实现细节读 design/。

---

## C. Hooks 系统：确定性质量门禁

> *Hooks 是 Claude Code Harness 的「确定性强制层」——无论 Agent 如何判断，Hooks 都会执行。是实现「让错误永不再发生」原则最有力的工具。*

**判断标准**：「这个行为必须始终发生，不论 Claude 的判断如何？」→ 如果是，用 Hook；否则用 CLAUDE.md。

### C.1 Hook 事件类型

| Hook 事件 | 触发时机 | 典型用途 |
|----------|---------|---------|
| `PreToolUse` | 工具调用前，可拦截或修改参数 | 阻止危险命令；限制文件访问范围 |
| `PostToolUse` | 工具完成后立即触发 | 自动格式化；测量 Token 消耗 |
| `Stop` | 主 Agent 完成响应后 | TypeScript 类型检查；测试覆盖率报告 |
| `UserPromptSubmit` | 用户提交 Prompt 前 | 注入额外上下文；防注入检测 |
| `TaskCompleted` | 任务标记为完成时（2026 新增） | 触发 CI；更新进度文件 |

### C.2 实战 Hook 示例

#### Stop Hook — TypeScript 类型检查强制门禁

```bash
#!/bin/bash
# .claude/hooks/stop-typecheck.sh
cd "$CLAUDE_PROJECT_DIR"

# 并行运行格式化和类型检查（加速反馈循环）
biome check --write . > /dev/null 2>&1 || biome check --write . > /dev/null 2>&1

TYPECHECK=$(pnpm typecheck 2>&1)
if [ $? -ne 0 ]; then
  echo "类型检查失败，请修复以下错误：" >&2
  echo "$TYPECHECK" >&2
  exit 2   # exit 2 = 将错误反馈给 Claude，Claude 将继续工作
fi
exit 0    # 成功时静默退出，不污染上下文
```

#### PreToolUse Hook — 阻止危险文件操作

```bash
#!/bin/bash
# .claude/hooks/pre-protect-env.sh
TOOL_INPUT=$(cat)
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.tool_input.path // empty')

if [[ "$FILE_PATH" == *".env"* ]] || [[ "$FILE_PATH" == *"secret"* ]]; then
  echo "拒绝：禁止访问敏感文件 $FILE_PATH" >&2
  exit 2
fi
exit 0
```

#### PostToolUse Hook — 自动格式化（成功静默，失败可见）

```bash
#!/bin/bash
# .claude/hooks/post-format.sh
# 关键原则：成功完全静默，只有失败才产生输出
# 4000 行通过日志会使 Agent 失去任务焦点（HumanLayer 实践教训）
cd "$CLAUDE_PROJECT_DIR"
FORMAT_OUTPUT=$(pnpm lint:fix 2>&1)
if [ $? -ne 0 ]; then
  echo "格式化失败：" >&2
  echo "$FORMAT_OUTPUT" >&2
fi
# 成功 = 完全静默
```

### C.3 Hooks 配置示例（settings.json）

```json
// .claude/settings.json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{ "type": "command", "command": ".claude/hooks/stop-typecheck.sh" }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": ".claude/hooks/pre-protect-env.sh" }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": ".claude/hooks/post-format.sh" }]
    }]
  }
}
```

---

## D. Subagents 与上下文隔离策略

> *Subagent 的核心价值不是并行，而是隔离——将产生大量输出的任务委托出去，主线程只接收摘要。*

### D.1 两种编排模式

| 模式 | 适用场景与权衡 |
|------|-------------|
| **Master-Clone 架构（推荐）** | 主 Agent 上下文包含全量 CLAUDE.md；用内置 `Task(...)` 克隆自身处理子任务；Agent 自主决定何时委托，动态灵活；可跨域整体推理 |
| **Lead-Specialist 架构（谨慎）** | 在 `.claude/agents/` 预定义专用 Subagent；刚性高，需手动触发；适合需要权限隔离的安全敏感任务 |

> **💡 Master-Clone 的核心优势**
>
> 主 Agent 可以整体推理变更（「修改这个 API 端点，对所有下游消费者的影响是什么？」），而 Lead-Specialist 模式中 Specialist 只能看到自己的上下文，无法跨域推理。

### D.2 安全审查 Subagent 定义模板

```yaml
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: >
  专业安全代码审查。在以下情况自动调用：提交前审查、
  新增认证/授权逻辑、外部 API 集成、用户输入处理。
tools: Read, Grep, Glob, Bash
model: opus
---
你是一名高级安全工程师，专注于：
- 注入漏洞（SQL、XSS、命令注入）
- 认证和授权缺陷
- 代码中的 secret 或凭据

不要修改代码——只提供带文件名和行号的审查报告。
```

### D.3 Explore Subagent — 上下文高效探索

```bash
# 在 Prompt 中显式使用 Explore
"用 subagent 调研我们的认证系统如何处理 token 刷新，
 以及是否有可复用的 OAuth 工具函数。"

# 效果：Claude 用 Haiku 模型扫描文件（低成本），
# 只向主线程返回摘要，主线程 Token 不受影响
```

---

## E. 上下文管理：最关键的工程决策

> *上下文是 Claude Code 最稀缺的资源。上下文污染（context pollution）是长任务失败的首要原因。*

### E.1 上下文健康度指标

| 指标 | 目标值与操作建议 |
|------|--------------|
| 基线成本（新会话） | `< 20k Token`（约占 200k 窗口的 10%）；用 `/context` 检查 |
| CLAUDE.md 大小 | `< 2000 Token`；超出则分拆到 `docs/` 子目录 |
| MCP 工具总 Token | `< 20k Token`；过多工具导致选择噪声，按需接入 |
| 手动 `/compact` 时机 | 到达 50% 用量时手动压缩，避免等到 Agent 自动触发 |
| 上下文清除频率 | 每 60k Token 或切换新任务时使用 `/clear` |
| 测试通过输出 | 成功时**完全静默**，只显示失败——通过日志污染上下文 |

### E.2 模型选择策略（成本 × 能力）

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| Plan Mode / 架构设计 | **Opus** | 复杂推理，值得更高成本；计划错误最昂贵 |
| 日常编码实现 | **Sonnet** | 速度与质量最佳平衡；90% 任务的最优选择 |
| 文件探索 / Explore Agent | **Haiku** | 大量文件读取，成本敏感；摘要质量足够 |
| 并行任务（Git Worktrees） | **Sonnet × N** | 多实例并行，单个成本控制优先 |
| 深度 Debug / 复杂重构 | **Opus（deep mode）** | 30+ 分钟任务，高质量优先于速度 |

### E.3 Git Worktrees 并行开发

```bash
# Claude Code 自动管理 Worktree 生命周期
claude --worktree feature-auth
claude --worktree feature-payment
claude --worktree refactor-db

# 每个 Worktree：独立分支 + 独立文件系统状态 + 独立 Claude 会话

# 手动方式
git worktree add ../myapp-auth -b feature/auth
cd ../myapp-auth && claude "实现 JWT 认证系统"
```

> **📌 并行上限建议**：本地同时运行 2–3 个为宜；更多实例可考虑云端开发环境（每个 Agent 独立容器）。

---

## F. Claude Agent SDK：长周期任务实现

> *对于需要数小时乃至数天的任务（或多人任务），需要用 Claude Agent SDK 构建专用 Harness，实现跨上下文窗口的持久工程。*

### F.1 SDK Harness 文件结构

```
project-root/
├── docs/
│   ├── claude-progress.json     ← 进度追踪（JSON 格式，而非 Markdown）
│   ├── features.json            ← 特性清单（结构化，Agent 不易误改）
│   ├── architecture.md
│   └── decisions/              ← ADR 记录
├── .claude/
│   ├── agents/                 ← Subagent 定义
│   ├── skills/                 ← Skills 目录
│   ├── commands/               ← 自定义 Slash Commands
│   ├── hooks/                  ← Hook 脚本
│   └── settings.json
├── CLAUDE.md                   ← 精简目录（< 60 行）
└── AGENTS.md                   ← 团队级 Agent 约定（可选）
```

### F.2 进度文件设计与维护（claude-progress.json）

使用 JSON 而非 Markdown：Agent 对结构化数据的尊重程度显著高于纯文本，不会无意覆盖或误删记录。

**维护原则：由 Agent 写，人只监督。** 人类工程师只在两种情况下直接编辑：需求变化导致任务列表变化、Agent 写错了需要纠正。

#### 完整结构示例

```json
{
  "project": "用户协作平台",
  "created_at": "2026-03-30T08:00:00Z",
  "last_updated": "2026-03-30T11:30:00Z",
  "current_phase": "implementation",

  "completed_features": [
    {
      "id": "F001",
      "name": "用户注册登录",
      "status": "done",
      "commit": "a3f8c2d",
      "completed_at": "2026-03-30T11:30:00Z",
      "test_coverage": "87%",
      "notes": "密码重置功能推迟到 F006，当前实现不包含"
    }
  ],

  "in_progress": {
    "id": "F002",
    "name": "JWT 认证刷新",
    "started_at": "2026-03-30T11:30:00Z",
    "current_step": "已完成 token 签发，刷新逻辑还未开始",
    "files_touched": [
      "src/service/auth/jwt.service.ts",
      "src/repo/token.repo.ts"
    ],
    "blockers": []
  },

  "pending_features": [
    {"id": "F003", "name": "OAuth 第三方登录", "priority": 3},
    {"id": "F004", "name": "权限管理 RBAC", "priority": 4},
    {"id": "F005", "name": "审计日志", "priority": 5}
  ],

  "session_startup_checklist": [
    "运行 pwd 确认工作目录",
    "读取本文件了解当前状态",
    "读取 docs/features.json 了解完整需求和验收标准",
    "运行 pnpm test 确认基线，记录失败数量",
    "确认 in_progress 特性，继续或标记完成后再取下一个"
  ],

  "notes": [
    {
      "type": "scope_concern",
      "feature_id": "F003",
      "message": "OAuth 实现发现同邮箱账户自动合并涉及数据一致性风险，建议人工确认验收标准",
      "raised_at": "2026-03-30T14:00:00Z",
      "resolved": false
    }
  ]
}
```

#### 文件生命周期

```
初始化 Agent（首次运行）
  → 创建文件骨架，写入所有 pending_features
  → 建立 session_startup_checklist

编码 Agent（每次会话结束前）
  → 把完成的特性从 in_progress 移到 completed_features
  → 把下一个特性从 pending_features 移到 in_progress
  → 更新 current_step 和 files_touched
  → 记录 blockers 或 notes
  → 更新 last_updated 时间戳

/harness:dump 命令（人手动触发）
  → Agent 把当前会话关键决策追加写入 notes
```

#### 遇到 blocker 时的记录方式

Agent 卡住时不应猜测继续，而是记录 blocker 停下来，等人介入：

```json
"in_progress": {
  "id": "F003",
  "blockers": [
    {
      "id": "B001",
      "description": "Google OAuth 回调 URL 需在 Google Console 配置，当前无权限",
      "blocked_at": "2026-03-30T14:20:00Z",
      "needs_human": true,
      "workaround": "可先用 mock OAuth 实现主流程，等配置后接真实接口"
    }
  ]
}
```

人看到 `needs_human: true` 后介入处理，下次会话 Agent 继续。

#### 防止 Agent 乱改的三个设计

```
1. completed_features 只追加，不删不改
   → 在启动 Prompt 里明确写：completed_features 是只追加
     的历史记录，任何情况下不得删除或修改已有条目

2. 用 id 而不是名称做引用
   → 避免「用户注册登陆」vs「用户注册登录」的拼写歧义

3. Stop Hook 自动 commit 进度文件
   → 每次会话有完整 git 历史，任何错误都可回滚
```

```bash
# .claude/hooks/stop-commit-progress.sh
cd "$CLAUDE_PROJECT_DIR"
if git diff --quiet docs/claude-progress.json; then
  exit 0  # 没有变化，跳过
fi
git add docs/claude-progress.json
git commit -m "chore: update agent progress [skip ci]"
```

---

### F.3 需求文件设计与维护（features.json）

`features.json` 是「产品需求书」，记录要做什么。与 `claude-progress.json` 分开存放的原因：**需求相对稳定，进度频繁变化。分开存放，Agent 更新进度时不会误改需求。**

#### 完整结构示例

```json
{
  "version": "1.0",
  "product": "用户协作平台",
  "last_updated": "2026-03-30T08:00:00Z",
  "updated_by": "zhang-wei",

  "features": [
    {
      "id": "F001",
      "name": "用户注册登录",
      "priority": 1,
      "status": "done",

      "description": "支持邮箱注册、登录、密码重置。不包含第三方登录（见 F003）。",

      "acceptance_criteria": [
        "用邮箱+密码注册成功，重复邮箱返回 409",
        "登录成功返回 access_token 和 refresh_token",
        "密码错误返回 401，不透露是邮箱不存在还是密码错误",
        "连续失败 5 次返回 429 并锁定账户 15 分钟"
      ],

      "out_of_scope": [
        "手机号注册（产品决策排除，见 ADR-0018）",
        "记住我功能（F008 处理）"
      ],

      "dependencies": [],

      "technical_notes": "密码用 bcrypt，cost factor 12。token 存 Redis，见 ADR-0012。",

      "related_files": [
        "src/service/auth/",
        "src/repo/user.repo.ts",
        "tests/integration/auth.test.ts"
      ]
    },

    {
      "id": "F003",
      "name": "OAuth 第三方登录",
      "priority": 3,
      "status": "in_progress",

      "description": "支持 Google 和 GitHub OAuth 2.0，已有账户自动关联。",

      "acceptance_criteria": [
        "点击「Google 登录」跳转授权页，授权后创建或关联账户",
        "同邮箱的本地账户和 OAuth 账户自动合并",
        "OAuth 账户受同样的账户锁定规则约束"
      ],

      "out_of_scope": [
        "微信、微博等国内平台（国际化阶段再做）"
      ],

      "dependencies": ["F001", "F002"],

      "blockers": [
        "Google OAuth 回调 URL 需在 Google Console 配置——等运维处理（预计 2026-04-01）"
      ]
    },

    {
      "id": "F006",
      "name": "文件版本历史",
      "priority": 6,
      "status": "cancelled",
      "cancelled_reason": "MVP 阶段砍掉，见产品决策 2026-04-01。勿删此条目，防止 Agent 误以为是遗漏。"
    }
  ],

  "constraints": {
    "implementation_order": "严格按 priority 顺序，有 dependency 的特性必须等依赖完成",
    "code_state_rule": "每个特性完成后代码必须可合并（测试全通过、无 TODO、有基本注释）",
    "scope_rule": "out_of_scope 的内容不实现，即使很简单。需求变更必须先更新本文件"
  }
}
```

#### 维护责任划分

| 操作 | 由谁做 | 说明 |
|------|--------|------|
| **初始创建** | 初始化 Agent | 人给高层描述，Agent 分解为结构化条目，人审阅修正 |
| **日常变更** | 人直接编辑 | 新增、修改、取消特性 |
| **取消特性** | 人编辑，改状态为 `cancelled` | 不要删除——防止 Agent 误以为是遗漏去补做 |
| **标记完成** | **不由人做** | 由编码 Agent 在 progress.json 里更新，features.json 的 status 由初始化 Agent 或人统一同步 |
| **发现问题** | Agent 记录在 claude_progress.json 的 notes 里 | Agent 不直接改 features.json，等人决策 |

#### 三个最关键的字段

**`acceptance_criteria`（验收标准）**

这是 Agent 判断「特性做完了没有」的唯一依据。写得越具体，Agent 越不容易提前收工：

```json
// ❌ 坏的写法——Agent 不知道怎么验证
"acceptance_criteria": ["实现用户登录"]

// ✅ 好的写法——Agent 可以逐条核对
"acceptance_criteria": [
  "登录成功返回 200 和包含 userId、role、expiresAt 的 token",
  "密码错误返回 401",
  "连续失败 5 次返回 429 并锁定 15 分钟"
]
```

**`out_of_scope`（不做什么）**

防止 Agent 过度实现——它有时会「顺手」把相关功能一起做了，超出预期范围影响后续特性：

```json
"out_of_scope": [
  "手机号注册（产品决策排除，见 ADR-0018）",
  "记住我功能（F008 处理）"
]
```

**`dependencies`（依赖关系）**

防止 Agent 跳序实现，在依赖特性还未建好时就开始做上层逻辑：

```json
"dependencies": ["F001", "F002"]
// Agent 读到这里，确认 F001 和 F002 是 done 状态才开始
```

#### 四个文件的完整分工

```
features.json        → 做什么、验收标准、边界（需求，人维护，Agent 只读）
claude-progress.json → 做到哪了、当前状态（进度，Agent 维护，人监督）
architecture.md      → 怎么做、模块在哪里（技术约定，人维护，Agent 只读）
docs/decisions/      → 为什么这样做（决策记录，人维护，Agent 只读）
```

---

### F.4 编码 Agent 启动 Prompt 模板

```
你是一名编码 Agent，负责为 [项目名] 实现功能。

启动检查清单（按顺序执行，不要跳过）：
1. 运行 `pwd` 确认当前工作目录
2. 读取 docs/claude-progress.json 了解当前进度
3. 读取 docs/features.json 了解完整特性列表和验收标准
4. 运行 `pnpm test` 确认测试基线（记录失败数量）
5. 确认 in_progress 特性，继续或标记完成后再取下一个

工作原则：
- 每次只实现一个特性，完成后更新 claude-progress.json
- 每个特性完成后代码必须处于「干净状态」
  （可合入 main，测试全通过，有必要的注释）
- 以 features.json 中的 acceptance_criteria 逐条验证，
  全部满足才能标记为 done
- 绝对不要实现 out_of_scope 里的内容，即使看起来很简单
- 绝对不要删除或修改已完成特性的测试
- 如遇到 blocker，在 in_progress.blockers 中记录，
  needs_human: true，不要猜测继续
- 发现 features.json 需要修改，在 claude-progress.json 的 notes
  里记录，不要直接改 features.json
- 完成所有特性后，在进度文件中标记 current_phase: done
```

---

### F.5 四个文件与需求规格说明书的关系

> *需求规格说明书是给人读的，这四个文件是把需求规格说明书「翻译」成 Agent 可执行的形式。*

#### 传统需求规格说明书对 Agent 的三个致命问题

一份典型需求规格说明书里的功能描述是这样的：

```
3.2 用户认证模块

系统应支持用户通过邮箱和密码进行注册和登录操作。
注册时系统应对输入数据进行验证，确保邮箱格式正确、
密码符合安全要求。登录成功后系统应生成会话凭证...
```

这种格式对 Agent 有三个致命问题：

- **无法判断「完成了没有」**：「确保邮箱格式正确」不是可核对的验收标准
- **不知道边界在哪里**：哪些是这次做的、哪些是以后的，需要读大量上下文才能判断
- **无法追踪状态**：文档本身不记录进度，Agent 每次都要重新理解全局

#### 四个文件是需求规格说明书的结构化拆解

```
需求规格说明书
（人写的、自然语言、静态）
         │
         ├── 功能需求部分 ──────→ features.json
         │   （要做什么）           结构化、可追踪、带验收标准
         │
         ├── 架构设计部分 ──────→ architecture.md
         │   （怎么组织代码）        目录结构、层级规则、模块地图
         │
         ├── 技术决策部分 ──────→ docs/decisions/
         │   （为什么这样选型）       ADR，保留被否决选项和原因
         │
         └── （无对应部分）  ──→ claude-progress.json
             需求规格说明书         执行时产生，记录进度和状态
             不记录执行进度
```

#### 逐一对应关系

**features.json ← 功能需求**

需求规格说明书的散文描述，经过结构化处理变成可执行的验收标准：

```
需求规格说明书：
「系统应支持用户通过邮箱和密码进行注册，
  注册时应验证邮箱格式，密码长度不少于 8 位...」

↓ 翻译为

features.json：
{
  "acceptance_criteria": [
    "重复邮箱返回 409",
    "密码少于 8 位返回 400",
    "注册成功返回 201 和 userId"
  ],
  "out_of_scope": ["手机号注册", "第三方注册"]
}
```

关键转变：**散文变列表**（可逐条核对）、**隐含边界变显式 out_of_scope**（Agent 不会越界实现）。

**architecture.md ← 系统架构设计**

需求规格说明书的架构描述通常只有概念，architecture.md 把它变成机械约束：

```
需求规格说明书：
「系统采用分层架构，前后端分离...」

↓ 翻译为

architecture.md：
依赖规则：types → config → repo → service → ui
违反规则时 CI 自动失败（见 tests/architecture/）
```

关键转变：**概念描述变可验证约束**。「分层架构」是一个词，依赖规则是会触发 CI 失败的硬约束。

**docs/decisions/ ← 技术选型说明**

需求规格说明书里的技术选型只写结论，ADR 保留了决策过程和被否决的选项：

```
需求规格说明书：
「会话管理采用 Redis 存储...」

↓ 翻译为

ADR-0012：
被否决的选项：JWT（安全团队反对，无法主动撤销）
后果：禁止 service 层直接引用 Redis，必须走 repo/cache/ 封装
```

关键转变：**只有结论变有上下文的决策过程**。Agent 知道「为什么不用 JWT」，就不会在实现时「优化」成 JWT 方案。

**claude-progress.json ← 需求规格说明书没有对应物**

这是最大的区别。需求规格说明书是静态文档，不记录执行状态。传统项目用 Jira、Linear 记录进度，Agent 工程把它内化进仓库本身：

```
需求规格说明书：（无此部分）

↓ 执行时由 Agent 产生

claude-progress.json：
{
  "in_progress": {"current_step": "已完成 token 签发，刷新逻辑未开始"},
  "blockers": [{"needs_human": true, "description": "需要配置 OAuth 回调 URL"}]
}
```

#### 项目启动工作流

从需求规格说明书到四个文件的转化，建议用以下工作流：

```
Step 1  人写需求规格说明书（或产品文档）
           ↓
Step 2  初始化 Agent 读需求规格说明书
        → 生成 features.json 初稿（功能拆解、验收标准）
        → 生成 architecture.md 初稿（目录结构建议）
           ↓
Step 3  人审阅并修正两个文件
        → 补充 out_of_scope（Agent 最容易越界的地方）
        → 补充技术约束和禁止规则
        → 为关键选型决策创建 ADR
           ↓
Step 4  编码 Agent 开始工作
        → 只读上述文件，不读原始需求规格说明书
        → 维护 claude-progress.json
```

> 需求规格说明书对 Agent 来说太「人性化」了——信息密度低、边界模糊、无法机械验证。四个文件是它的机器可读版本，这个翻译过程本身就是 Harness Engineering 的重要一环。

---

## G. Slash Commands 与 Skills：团队工作流标准化

> *Slash Commands 和 Skills 是将「好实践」固化为「自动行为」的工具——前者由人触发，后者由 Agent 自动激活。*

### G.1 设计决策：命令 vs 技能 vs Subagent

| 机制 | 激活方式 & 最佳适用场景 | 示例 |
|------|---------------------|------|
| **Slash Command** | 手动触发 `/command`；适合有明确起点的工作流 | `/harness:review-pr`, `/deploy-staging` |
| **Skill** | Claude 自动激活（description 匹配任务）；适合「进行式」知识注入 | commit-message skill, api-endpoint skill |
| **Subagent** | 显式或自动委托；适合需要上下文隔离的深度任务 | security-review, performance-benchmark |
| **CLAUDE.md 规则** | 始终存在；适合所有任务都需要的约定 | TypeScript strict, 禁止 secret 硬编码 |
| **Hook** | 事件驱动，必须执行；适合不可协商的质量门禁 | Stop hook 类型检查, PreToolUse 权限控制 |

### G.2 团队 Slash Commands 模板

#### `/harness:review-pr` — PR 代码审查

```markdown
# .claude/commands/harness:review-pr.md
---
description: 对当前分支的 PR 进行全面代码审查
---

用 subagent 执行以下步骤后汇总：
1. 运行 `git diff main...HEAD` 获取所有变更
2. 检查代码质量（TypeScript 错误、未使用变量、逻辑漏洞）
3. 检查安全问题（注入、认证缺陷、secret 暴露）
4. 验证测试覆盖率（新代码必须有对应测试）
5. 检查 API 文档更新（所有公共 API 必须有 JSDoc）

输出格式：
- 必须修复（阻塞合并）
- 建议改进（可选）
- 值得肯定的地方
```

#### `/harness:dump` — 长任务上下文保存

```markdown
# .claude/commands/dump.md
---
description: 保存当前会话的关键决策和进度到文档
---

将以下信息写入 docs/claude-progress.json：
1. 本次会话完成的特性（更新 completed_features）
2. 当前进行中的工作（更新 in_progress）
3. 遇到的重要决策和理由（追加到 docs/decisions/ 目录）
4. 下一个 Agent 需要知道的关键上下文

同时更新 last_updated 时间戳。
完成后输出摘要：「已保存 X 个完成特性，当前进度：[特性名]」
```

### G.3 Skills 目录结构示例

```
.claude/skills/
├── api-endpoint/
│   ├── SKILL.md         ← 「创建 API 端点时自动激活」
│   └── template.ts      ← 端点模板文件
├── db-migration/
│   ├── SKILL.md         ← 「创建数据库迁移时自动激活」
│   └── migration-guide.md
├── commit-message/
│   └── SKILL.md         ← 「生成提交信息时自动激活」
└── test-pattern/
    ├── SKILL.md         ← 「编写测试时自动激活」
    └── examples/
```

```markdown
# .claude/skills/api-endpoint/SKILL.md
---
name: api-endpoint
description: >
  创建 REST API 端点时使用。包含 Zod 验证、OpenAPI 文档、
  错误处理、测试的完整模式。
  当用户提到「新建路由」「添加接口」「API endpoint」时激活。
---

## API 端点创建规范
1. 在 packages/api/src/routes/ 目录创建
2. 使用 Zod 进行请求/响应验证
3. 所有端点需要 OpenAPI 文档注释
4. 创建对应的 .test.ts 文件
5. 在 routes/index.ts 中注册路由
```

---

## H. 常见反模式与修复指南

| 反模式 | 症状与原因 | 修复方案 |
|--------|---------|---------|
| **过度膨胀的 CLAUDE.md** | 规则超过 100 行；Claude 开始忽略其中部分规则 | 删减至 <60 行；Claude 已正确执行的规则直接删除；复杂规则移入 Hook |
| **滥用 MCP** | 接入 20+ MCP Server；Agent 经常选错工具 | 每个工具接入前问「这个任务没它能完成吗？」；按需接入，不用时禁用 |
| **全量测试输出** | 测试成功时输出 4000 行日志；Agent 开始讨论测试文件 | Hook 中成功完全静默；只有失败才输出；加入 `head -50` 截断超长错误 |
| **过度定制 Subagent** | 为每类任务定义 Specialist；Agent 无法整体推理跨域变更 | 改用 Master-Clone 架构；主 Agent 用 `Task(...)` 克隆自身 |
| **「巨型」单会话** | 一个会话处理 10+ 功能；上下文超 100k 后输出质量下滑 | 每个功能一个会话；用 `/harness:dump` 保存进度 |
| **依赖 Compaction 保持记忆** | 跨窗口时 Agent 开始猜测「上次做了什么」 | 改用结构化进度文件；Agent 启动时主动读取 |
| **所有约定放 CLAUDE.md** | 「必须」的行为放 CLAUDE.md，被偶尔忽略 | 「必须执行」= Hook；「应该遵守」= CLAUDE.md；「确定配置」= settings.json |

---

## I. 团队快速启动：30 分钟 Harness 建立

### 步骤 1：10 分钟建立 CLAUDE.md

1. 运行 `/init` 让 Claude 生成初稿（作为基线，不要直接使用）
2. 人工精简：删除 Claude 已自然遵守的规则；保留技术栈、测试命令、架构约定、禁止规则
3. 控制 `< 60 行`：超出部分移入 `docs/architecture.md`，CLAUDE.md 中用链接指向
4. 提交到 Git：CLAUDE.md 是团队共享资产，纳入版本管理

### 步骤 2：10 分钟配置核心 Hooks

1. **Stop Hook** — TypeScript 类型检查 + Linter；失败时 `exit 2` 强制 Claude 继续修复
2. **PostToolUse Hook** — 文件编辑后自动格式化；成功完全静默
3. **PreToolUse Hook（可选）** — 阻止读写 `.env` 和密钥文件
4. 配置 `settings.json`：注册三个 Hook；运行 `/hooks` 确认激活状态

### 步骤 3：10 分钟建立工作流命令

1. 创建 `/harness:review-pr`：PR 提交前的统一审查入口
2. 创建 `/harness:dump`：长任务中保存进度到 `claude-progress.json`
3. 创建 `docs/` 目录：建立 `architecture.md` 和 `decisions/` 目录

> **🔁 持续改进节奏**
>
> 每周五 10 分钟：回顾本周 Agent 失败案例 → 每个失败对应一条 Harness 改进（更新 CLAUDE.md / 添加 Hook / 建立 Skill）→ 这个复利循环是 Harness Engineering 的本质。

---

## J. 最新进展补充：能力建设背景与原理（2026.04）

> *本节综合 Anthropic 最新工程博客（2026.03.24）、Claude Code 源码分析（2026.03.31）及社区实践，对第二部分各章节的关键原理做背景补充，直接服务于团队 Harness 工程能力建设工作。*

---

### J.1 上下文焦虑（Context Anxiety）：为什么压缩不够

#### 现象描述

上下文焦虑是一个此前未记录的失败模式：模型在接近它认为的上下文限制时，会开始过早收尾工作。 具体表现是 Agent 在任务未完成时突然声称「已完成」，或者跳过剩余步骤直接提交。

#### 根本原因

Agent 在训练时学到了一个隐性行为：当上下文窗口接近满时，要「整理并收尾」。这是合理的单次对话行为，但在长任务场景里会变成一个破坏性的反模式。

```
上下文窗口使用率
0%                    50%                   100%
|------正常工作--------|---开始焦虑---|---强制收尾---|
```

#### 压缩（Compaction）为什么不够

压缩是把较早的对话历史「摘要化」，让同一个 Agent 继续工作：

```
[完整历史] → 压缩 → [摘要 + 近期历史]
                         ↑
                    同一个 Agent 继续
                    但它「知道」自己已工作很久
                    焦虑状态持续存在
```

**上下文重置**是完全清空，用结构化交接物启动一个新 Agent：

```
[完整历史] → 保存进度到 claude-progress.json
                         ↓
                    新 Agent 从零开始
                    读取进度文件重建状态
                    没有「已工作很久」的感知
```

#### 与模型版本的关系

Sonnet 4.5 的上下文焦虑足够强烈，仅靠压缩不足以保证长任务性能，上下文重置成为必要。Opus 4.5 基本上自行消除了这种行为，可以完全去掉上下文重置，改用自动压缩处理上下文增长。

**能力建设行动**：每次新模型发布，用一个标准长任务（至少 5 个特性）测试是否出现过早收工行为。根据结果决定是否保留重置机制——模型改善时主动精简 Harness，模型退化时补回重置脚手架。

```
模型测试结论 → Harness 配置决策

出现上下文焦虑  → 保留上下文重置 + claude-progress.json 交接
没有上下文焦虑  → 改用自动压缩，删除重置脚本（减少复杂度）
```

---

### J.2 Prompt Caching：Harness 的成本基础设施

#### 什么是 Prompt Caching

Anthropic API 会缓存 Prompt 的前缀部分。如果两次请求的 Prompt 开头内容完全相同（字节级别），第二次就不需要重新处理这部分，成本和延迟显著降低（输入 Token 成本降至约 10%）。

```
Request 1:  [系统提示 2000 Token] + [任务描述] + [工具调用历史]
Request 2:  [系统提示 2000 Token] + [新任务描述] + [新工具调用历史]
                ↑
          这 2000 Token 命中缓存，不重新计费
```

#### Claude Code 如何设计缓存感知的系统提示

Claude Code 使用模块化系统提示，带有缓存感知的边界。系统提示由多个片段组成：基础行为指令、工具特定指导、项目上下文（来自 CLAUDE.md 文件）和会话特定状态。

**设计原则：稳定内容前置，变化内容后置**

```
系统提示结构（按稳定性降序排列）：

[Block 1：基础行为指令]  ← 最稳定，几乎不变，最长缓存
你是一个 TypeScript 编码专家...
永远不要删除测试...
禁止硬编码 secret...

[Block 2：项目级 CLAUDE.md]  ← 较稳定，项目启动后基本固定
## 技术栈
TypeScript strict mode...
## 架构约定
依赖方向：types → repo → service...

[Block 3：会话上下文]  ← 每次任务可能变化，缓存概率低
当前任务：实现 OAuth 登录...
相关文件：src/service/auth/...

[Block 4：动态状态]  ← 每轮都变，不缓存
当前 Token 用量：45,230...
最新工具调用结果：...
```

#### 并行 Agent 的缓存优化

所有 Fork 子 Agent 对每个 `tool_result` 块使用字节完全相同的占位符文本，只有最终指令文本不同。这是刻意的缓存优化——字节相同的占位符确保最大缓存命中率，显著降低并行操作的延迟和成本。

**能力建设行动**：在 Claude Agent SDK 构建的多 Agent 系统中，为并行 Sub-agent 设计共享的 Prompt 前缀模板，可变部分放在最后。监控 Prompt Cache 命中率（通过 API 返回的 usage 字段），命中率低于 60% 时检查 Prompt 结构设计。

---

### J.3 Hook 系统完整架构：26 个事件与 4 种处理器

#### 为什么有 26 个 Hook 事件

Hook 事件覆盖 Agent 生命周期的完整流程：SessionStart → UserPromptSubmit → PreToolUse → PostToolUse → SubagentStart → SubagentStop → Stop → SessionEnd，以及 FileChanged、WorktreeCreate/Remove、PreCompact/PostCompact 等状态变化事件，共 26 种。

理解 Hook 事件的最佳方式是把 Agent 工作过程看成一个状态机：

```
会话开始 (SessionStart)
    ↓
用户提交 Prompt (UserPromptSubmit)  ← 可在此注入上下文或检测注入攻击
    ↓
Agent 决定调用工具
    ↓
工具调用前 (PreToolUse)  ← 可在此拦截危险操作
    ↓
工具执行
    ↓
工具调用后 (PostToolUse / PostToolUseFailure)  ← 可在此格式化、验证
    ↓
文件发生变化 (FileChanged)  ← 可触发增量测试
    ↓
Agent 完成本轮响应 (Stop)  ← 可在此做质量检查
    ↓
会话结束 (SessionEnd)  ← 可在此保存进度、发送通知
```

#### 4 种处理器类型的选择原则

**Command（Shell 脚本）** — 最常用，适合确定性操作：

```bash
# 适合：格式化、类型检查、权限验证
# 特点：执行快、结果确定、易调试
exit 0   # 成功，继续
exit 2   # 失败，错误信息反馈给 Agent，Agent 继续修复
exit 其他 # 失败，不反馈给 Agent（非阻塞）
```

**Prompt（LLM 评估）** — 适合需要判断的场景：

```json
// 适合：评估输出质量、检测微妙的违规
// 特点：可以理解语义，但成本高、速度慢
{
  "type": "prompt",
  "prompt": "检查上述代码是否包含任何业务逻辑在 repo 层中，如有返回 VIOLATION，否则返回 OK"
}
```

**Agent（派生子 Agent）** — 适合复杂验证任务：

```json
// 适合：多步骤验证、需要读取多个文件的检查
// 特点：有完整工具访问，可以自主探索，结果可信
{
  "type": "agent",
  "prompt": "审查刚才修改的认证相关文件，检查是否有 JWT 验证缺失或权限绕过风险",
  "model": "haiku"
}
```

**HTTP（外部服务）** — 适合与企业系统集成：

```json
// 适合：触发 CI、通知 Slack、更新 Jira
{
  "type": "http",
  "url": "https://your-ci/trigger",
  "headers": {"Authorization": "Bearer ${CI_TOKEN}"}
}
```

**选择决策树**：

```
这个验证需要「理解语义」吗？
  → 是：用 Prompt 或 Agent 类型
  → 否：用 Command 类型（更快更便宜）

需要读取多个文件或执行多步骤吗？
  → 是：用 Agent 类型
  → 否：用 Prompt 类型

需要触发外部系统（CI、通知）吗？
  → 是：用 HTTP 类型
```

#### 能力建设行动：按失败类型选择 Hook

| 团队常见失败 | 对应 Hook | 处理器类型 | 优先级 |
|-------------|---------|----------|--------|
| 类型错误被提交 | Stop | Command（pnpm typecheck） | ⭐⭐⭐ 立即 |
| 修改了 .env 文件 | PreToolUse | Command（文件路径检查） | ⭐⭐⭐ 立即 |
| 代码格式不统一 | PostToolUse | Command（pnpm lint:fix） | ⭐⭐⭐ 立即 |
| 架构违规未被发现 | PostToolUse | Agent（架构约束检查） | ⭐⭐ 本周 |
| Agent 过早收工 | Stop | Command（检查 progress.json 完整性） | ⭐⭐ 本周 |
| Sub-agent 未记录进度 | SubagentStop | HTTP（触发进度同步） | ⭐ 本月 |
| 会话结束未 commit 进度 | SessionEnd | Command（git commit progress） | ⭐ 本月 |

---

### J.4 权限强制与模型推理必须分离

#### 为什么这是架构原则而不只是实践建议

权限强制与模型推理应该是不同的层。模型决定尝试什么，系统决定允许什么。大量 Agent Harness 把二者混在一起——这是一个设计错误。

混在一起时会发生什么：

```
❌ 混合设计的失败链条：

CLAUDE.md 规则：「不要修改生产数据库」
    ↓
Agent 理解这条规则
    ↓
Agent 在某个推理链路中「认为」这个操作是必要的
    ↓
Agent 执行了修改（它「理解」但「误判」了必要性）
    ↓
生产数据被修改
```

```
✅ 分离设计的防护链条：

CLAUDE.md 规则：「不要修改生产数据库」（解释原因，帮助 Agent 理解）
    +
settings.json：禁止 bash 工具执行包含「production」DB 连接串的命令
    +
PreToolUse Hook：检测 DB 连接串，发现生产环境字符串立即拦截
    ↓
即使 Agent 推理出「需要修改」，系统层面也会阻止
```

**核心原则**：

- **CLAUDE.md** = 解释「为什么不能做」，帮助 Agent 理解意图，引导正确行为
- **settings.json + Hooks** = 强制「无论如何都不能做」，不依赖 Agent 的理解和判断

两者都要，各司其职。只有 CLAUDE.md 是软约束，只有 Hook 是硬约束但缺少上下文解释，两者结合才是完整防护。

#### 三层防护的具体落地

```
Layer 1：settings.json（最高优先级，系统级强制）
  allowedTools: ["Read", "Edit", "Bash"]
  # 精确控制 Agent 可以调用哪些工具

Layer 2：PreToolUse Hook（工具调用前拦截）
  # 在允许的工具范围内，进一步检查参数
  # 例如：Bash 工具允许，但包含 rm -rf 的命令不允许

Layer 3：CLAUDE.md 规则（Agent 理解层）
  # 解释约束的原因，帮助 Agent 主动避免
  # 例如：「永远不要删除迁移文件，因为这会破坏生产数据库结构」

三层的关系：
  Layer 1 拒绝工具本身
  Layer 2 拒绝具体的危险参数
  Layer 3 帮助 Agent 理解为什么，减少它尝试绕过的动机
```

---

### J.5 MCP 使用的成本原理与决策逻辑

#### MCP 工具为什么消耗上下文

每个 MCP Server 连接时，它的所有工具定义都会被注入到系统提示里：

```
GitHub MCP Server 连接后，系统提示里增加了：
- github.get_issue: 获取 Issue 详情，参数：issue_number...
- github.create_issue: 创建 Issue，参数：title, body, labels...
- github.list_pull_requests: 列出 PR，参数：state, head...
... (可能 30-50 个工具定义)

每个工具定义约 100-300 Token
30 个工具 = 额外 3,000-9,000 Token 系统提示
这些 Token 在每次请求时都要发送和处理
```

Anthropic 已经发布了实验性 MCP 工具搜索支持，当用户连接了太多 MCP 工具时，可以渐进式地向 Claude 暴露工具。如果 MCP Server 重复了训练数据中已有良好表示的 CLI 工具功能，让 Agent 直接使用 CLI 效果更好——模型已经训练过这些工具，还可以与 grep、jq 等工具组合使用实现更高上下文效率。

#### 决策框架：什么时候用 MCP，什么时候用 CLI

**原则**：模型的「先天知识」是最便宜的 Token。

```
判断 1：模型有没有内置知识？
  git, npm, docker, gh CLI, psql... → 模型训练时大量见过
  你公司的内部 API              → 模型从未见过

判断 2：工具有多少个操作？
  你只用 3 个 GitHub 操作       → 写 3 行 CLI 用法到 CLAUDE.md
  你用 GitHub 的 20+ 个操作     → 用 MCP Server

判断 3：CLI 交互是否足够高效？
  CLI 输出简洁、结构化           → 用 CLI
  CLI 输出太冗长（大量噪声）      → 用 MCP（可以控制返回格式）
```

#### 自定义轻量 CLI 的模式

对于只使用少数操作的工具，写一个极简 CLI 封装往往比 MCP 更高效：

```bash
#!/bin/bash
# linear-cli: 只封装团队实际用到的 5 个 Linear 操作
case "$1" in
  get)    curl -s "https://api.linear.app/issues/$2" | jq '{id,title,status}' ;;
  list)   curl -s "https://api.linear.app/issues?assignee=me" | jq '[.[] | {id,title}]' ;;
  done)   curl -X PATCH "https://api.linear.app/issues/$2" -d '{"stateId":"done-id"}' ;;
  *)      echo "用法: linear get|list|done [issue-id]" ;;
esac
```

```markdown
# CLAUDE.md 里的 6 行说明（替代整个 Linear MCP Server）
## Linear
使用 linear CLI 操作 Linear：
- 获取 Issue：`linear get ENG-123`
- 列出我的 Issue：`linear list`
- 标记完成：`linear done ENG-123`
```

**对比**：
- Linear MCP Server：注入 ~50 个工具定义，约 5,000 Token
- 自定义 CLI + CLAUDE.md 说明：约 100 Token

---

### J.6 Skills + MCP + Sub-agent 协作的设计模式

#### 三者的本质区别

```
Skills      → 改变 Agent 知道什么（领域知识注入）
MCP         → 改变 Agent 能做什么（工具能力扩展）
Sub-agent   → 改变 Agent 怎么组织工作（上下文隔离）
```

#### 为什么需要三者协作

单独使用任何一个都有局限：

- **只有 Skills**：Agent 知道规范，但没有工具执行；主线程被探索过程污染
- **只有 MCP**：Agent 有工具，但不知道这个项目的约定是什么
- **只有 Sub-agent**：隔离了上下文，但 Sub-agent 也需要知识和工具

三者协作的完整示例——「实现并审查一个新 API 端点」：

```
1. 主 Agent 收到任务：「新增用户导出接口」

2. api-endpoint Skill 自动激活（description 匹配）
   → 注入：Zod 验证规范、OpenAPI 文档要求、测试模板
   → Agent 现在知道「怎么做」

3. 主 Agent 实现接口，调用 GitHub MCP 工具创建 PR

4. 主 Agent 委托 security-reviewer Sub-agent：
   → Sub-agent 在独立上下文里读取所有相关文件
   → Sub-agent 只返回：「发现 SQL 注入风险：第 47 行未参数化查询」
   → 主线程只增加这一行输出，不携带 Sub-agent 读取的所有文件内容

5. 主 Agent 根据报告修复，再次提交

整个流程：
  主线程上下文增加 ≈ 任务描述 + Skill 规范 + 审查报告 ≈ 2,000 Token
  Sub-agent 消耗 ≈ 读取 10 个文件 + 分析 ≈ 8,000 Token（隔离释放）
  净节省：6,000 Token 不留在主线程
```

#### 团队标准化工作流的设计模式

基于三者协作，为常见开发场景建立标准工作流：

```
场景：「实现新功能」的标准工作流

.claude/skills/feature-impl/SKILL.md
  → 注入：功能实现规范、测试要求、文档标准

.claude/commands/implement.md（/implement 命令）
  → 步骤 1: 读取 features.json 找到当前特性和验收标准
  → 步骤 2: 用 Explore Sub-agent 调研相关代码（保持主线程干净）
  → 步骤 3: 实现代码
  → 步骤 4: 委托 security-reviewer Sub-agent 做安全检查
  → 步骤 5: 通过 GitHub MCP 提 PR
  → 步骤 6: 更新 claude-progress.json

每次调用 /implement，走完整个流程，不需要重复 Prompt
```

---

### J.7 「在环路上」：Harness 能力建设的角色定位

#### 三种人类与 Agent 的关系模式

「在环路外」（Outside the loop）：人类只管理「为什么循环」（我们想要什么），把「如何循环」（怎么构建）完全交给 Agent——即「Vibe Coding」。「在环路中」（In the loop）：人类深入参与最底层的编码循环，手动审查每行 AI 生成的代码——人成为瓶颈。

「在环路上」（On the loop）：人类设计和改进控制 Agent 工作的 Harness，而不是亲自执行每一步——这是正确的角色定位。

```
在环路外（Vibe Coding）
  人：「帮我做一个用户管理系统」
  Agent：自由发挥
  结果：可能可用，但不可控、不可维护

在环路中（微管理）
  人：审查每行代码、每个决定
  Agent：等待人的确认
  结果：质量有保证，但人是瓶颈，速度慢

在环路上（Harness Engineering）
  人：设计约束、维护 Harness、处理异常
  Agent：在约束内自主工作
  结果：质量有保证，速度快，人专注于判断
```

#### Harness 能力建设工作的正确定位

「在环路上」和「在环路中」的区别在于：对 Agent 产出不满意时，「在环路中」的做法是直接修改产物；「在环路上」的做法是改进产生这个产物的 Harness，让它下次自动产出正确结果。

这意味着 Harness 能力建设工作的核心指标不是「修复了多少 Agent 的错误」，而是「**永久消除了多少类错误**」：

```
衡量 Harness 能力建设成效的指标：

❌ 错误指标：「本周帮 Agent 修复了 20 个 Bug」
✅ 正确指标：「本周新增了 3 条架构 Linter 规则，这类 Bug 不会再出现」

❌ 错误指标：「回顾了 Agent 的所有 PR」
✅ 正确指标：「建立了自动安全审查 Hook，PR 质量问题自动被拦截」

❌ 错误指标：「写了详细的 CLAUDE.md 让 Agent 不犯错」  
✅ 正确指标：「通过 Hook + settings.json 让物理上无法犯那些错」
```

#### 「飞轮效应」：让 Agent 改进 Harness

下一个层次是人类指导 Agent 来管理和改进 Harness，而不是手动去做。当 Harness 足够成熟时，你可以让 Agent 自动扫描代码库寻找违规，更新质量评分，开 PR 修复架构漂移——这正是 OpenAI 的「垃圾回收 Agent」所做的。

Harness 成熟度的演进路径：

```
阶段 1：人建 Harness，Agent 在 Harness 内工作
         （当前大多数团队）

阶段 2：Agent 发现 Harness 的问题，在 progress.json 里记录
         人看到记录后更新 Harness
         （本手册推荐的当前目标）

阶段 3：Agent 发现问题后，直接提 PR 改进 Harness
         人审批 PR 后自动合并
         （OpenAI「垃圾回收 Agent」模式）

阶段 4：Harness 自动优化自身（Meta-Harness，实验阶段）
```

对于正在建设 Harness 工程能力的团队，**阶段 2 是当前合理目标**：建立机制让 Agent 记录它遇到的 Harness 缺陷，人定期审查并转化为 Harness 改进。这比让 Agent 直接修改 Harness 更安全，也比完全手动更高效。

---

### J.8 前 30 天实施路线图（修订版）

> *基于旧金山工程领袖田野调查（2026.04）的修正：不要在第一天就标准化。先观察，再约束。*

#### 第 1-2 周：观察与记录

第一步不是在第一天制定标准。先用两周时间在真实工作上运行 Agent，记录每一次回滚、返工和拒绝。然后围绕你实际观察到的失败模式构建约束，而不是假设的失败模式。

```
第 1 周行动：
□ 选一个中等复杂度的真实任务运行 Agent
□ 用简单的 CLAUDE.md（< 30 行，只写技术栈和测试命令）
□ 记录每次需要人工干预的情况：为什么干预？Agent 哪里错了？
□ 记录每次回滚：改了什么？为什么要撤销？

第 2 周行动：
□ 对记录的失败按「频率 × 严重程度」排序
□ 识别前 3 个最高优先级失败模式
□ 只为这 3 个失败模式构建对应的 Harness 约束
```

#### 第 3-4 周：精准构建

```
针对观察到的失败模式，按类型构建约束：

「Agent 每次都忘记写测试」
  → Stop Hook：运行测试，覆盖率低于 80% 时反馈给 Agent
  → CLAUDE.md 规则：说明为什么测试是必须的

「Agent 经常引入架构违规」  
  → 建立 tests/architecture/ 目录，写结构化测试
  → CI 配置：PR 时自动运行架构测试

「Agent 在 repo 层引入了业务逻辑」
  → 自定义 Linter 脚本：检查 repo 层的 import 范围
  → 在错误信息里写清楚修复方式
```

#### 第 5-8 周：迭代与精简

```
每周复盘：
□ 上周的 Harness 约束有没有触发？触发了几次？
□ 有没有误报（拦截了正确行为）？
□ 有没有漏报（没有拦截应该拦截的行为）？

根据复盘调整：
- 触发 0 次 = 这条规则可能多余，或 Agent 已经学会遵守
- 高频误报 = 规则太严或写法有问题，需要细化
- 有漏报 = 规则需要加强，或补充新的检查维度
```

---

## K. 验证与反馈、垃圾回收：深度实践指南

> *本节是对手册第一部分「1.1 Harness 四大要素」中「验证与反馈」和「垃圾回收」的系统性展开，综合 Birgitta Böckeler（Thoughtworks，2026.04.02）、Datadog、OpenTelemetry 及业界实践，提供可直接落地的操作模式。*

---

### K.1 验证体系的基础框架：前馈（Guides）与反馈（Sensors）

#### 核心概念

为了驾驭编码 Agent，我们既要预期不想要的输出并尝试预防，也要设置传感器以允许 Agent 自我纠正：**Guides（前馈控制）**——预期 Agent 的行为并在它行动之前进行引导；**Sensors（反馈控制）**——在 Agent 行动之后进行观察并帮助它自我纠正，当传感器产生针对 LLM 消费优化的信号时尤其强大。

单独使用任何一种都是残缺的：

```
只有 Guides（前馈）：
  Agent 编码了规则，但从来不知道规则是否生效
  → 规则积累，质量停滞，不知道哪些约束真正有效

只有 Sensors（反馈）：
  Agent 知道自己做错了，但不知道怎么做对
  → Agent 反复犯同样的错误，在修复循环里空转

Guides + Sensors（前馈 + 反馈）：
  Agent 在行动前被引导，行动后被验证
  → 错误被预防，遗漏被捕获，整个系统持续改善
```

#### 两类执行模式

Guides 和 Sensors 有两种执行类型：**Computational（计算式）**——确定性且快速，由 CPU 运行，包括测试、Linter、类型检查、结构分析，在毫秒到秒级运行，结果可靠；**Inferential（推理式）**——语义分析、AI 代码审查、「LLM 作为评判者」，通常由 GPU 或 NPU 运行，速度较慢、成本较高，结果具有更多不确定性。

| 维度 | Computational | Inferential |
|------|--------------|------------|
| **速度** | 毫秒—秒级 | 秒—分钟级 |
| **成本** | 低（CPU） | 高（GPU/API） |
| **确定性** | 完全确定 | 概率性 |
| **适合检查** | 格式、类型、依赖、边界 | 语义、设计质量、安全意图 |
| **触发频率** | 每次变更 | 关键检查点 |

**实践原则**：先用 Computational 方案覆盖 80% 的常见问题，再用 Inferential 方案处理需要理解语义的剩余 20%。不要用昂贵的 LLM 判断来替代能用脚本解决的问题。

#### Guides 与 Sensors 的对应关系表

Guides 和 Sensors 的示例对应：编码规范 → 前馈，推理式（AGENTS.md、Skills）；结构测试 → 反馈，计算式（运行 ArchUnit 测试检查模块边界违规的 pre-commit Hook）。

| 控制对象 | 方向 | 类型 | 具体实现 |
|---------|------|------|---------|
| 架构依赖规则 | 前馈 | Computational Guide | CLAUDE.md 架构约定 |
| 架构依赖验证 | 反馈 | Computational Sensor | 结构测试 + Stop Hook |
| 编码规范 | 前馈 | Inferential Guide | AGENTS.md、Skills |
| 代码质量审查 | 反馈 | Inferential Sensor | /code-review Skill 或审查 Sub-agent |
| API 使用方式 | 前馈 | Computational Guide | MCP 工具定义、CLI 说明 |
| 类型错误 | 反馈 | Computational Sensor | Stop Hook（pnpm typecheck） |
| 安全漏洞 | 反馈 | Inferential Sensor | 安全审查 Sub-agent（Opus 模型） |

---

### K.2 质量左移：把验证分布在整个变更生命周期

#### 核心原则

持续集成的团队一直面临挑战：如何根据成本、速度和关键性，在开发时间线上分布测试、检查和人工审查。当你追求持续交付时，理想情况下每个提交状态都应是可部署的。应尽可能把检查放在生产路径的左边，因为越早发现问题，修复成本越低。

```
变更生命周期中的质量检查分布：

[本地开发阶段]（最左，最便宜）
  Computational Guides：LSP 实时提示、架构规则 CLAUDE.md
  Computational Sensors：Linter、快速单元测试（< 30 秒）
  → 在 Agent 提交前就给出反馈

[提交/PR 阶段]（中等成本）
  Computational Sensors：完整测试套件、类型检查、架构测试
  Inferential Sensors：基础代码审查 Agent（Haiku/Sonnet 模型）
  → 在代码进入共享分支前拦截

[集成/CI 阶段]（较高成本，但自动）
  重复上述所有检查 + 集成测试
  Inferential Sensors：更全面的代码审查（考虑更大范围上下文）
  → 最终质量门禁

[部署/生产阶段]（观察而非阻止）
  可观测性：遥测、追踪、指标
  影子部署验证：新旧实现的行为对比
  → 发现测试覆盖不到的边缘情况
```

#### 对应到 Claude Code 的具体工具

```
[本地开发阶段]
  → CLAUDE.md（Guides）
  → PostToolUse Hook：每次文件编辑后运行 Linter（静默成功）

[提交阶段]
  → Stop Hook：TypeScript 类型检查 + 测试（失败时反馈给 Agent）
  → PreToolUse Hook：拦截危险操作

[PR 阶段]
  → /harness:review-pr Slash Command（触发审查 Sub-agent）
  → GitHub Actions：结构化测试、覆盖率检查

[部署阶段]
  → 遥测接入（OpenTelemetry Traces）
  → 影子部署钩子（PostToolUse → 触发 HTTP Hook 通知 CI）
```

---

### K.3 验证的三个层次：可维护性、架构适应性、行为

Harness 的调节类别分为三组：**可维护性 Harness**——确保代码长期可维护（命名规范、文件大小限制、注释覆盖率）；**架构适应性 Harness**——确保代码符合架构约束（依赖方向、模块边界）；**行为 Harness**——确保代码行为正确（测试、端到端验证）。

```
Layer 1：可维护性验证
  目标：AI 生成的代码能被未来的 Agent 和人类读懂和修改
  工具：命名约定检查、文件长度限制、JSDoc 覆盖率
  实现：Computational Sensors（自定义 Linter）

  示例规则：
  - 函数超过 50 行 → Linter 警告并建议拆分
  - 公共函数缺少 JSDoc → Stop Hook 反馈
  - 魔法数字超过 3 个 → 提示提取为命名常量

Layer 2：架构适应性验证
  目标：AI 生成的代码符合系统架构约束
  工具：结构测试、依赖分析（dep-cruiser）、模块边界检查
  实现：Computational Sensors（tests/architecture/）

  示例规则：
  - repo 层 import service 层 → CI 失败，附修复说明
  - 循环依赖 → 立即拦截
  - 新增对外部服务的直接调用（绕过封装层）→ 警告

Layer 3：行为验证
  目标：AI 生成的代码按照预期工作
  工具：单元测试、集成测试、E2E 测试（Playwright）、合约测试
  实现：Computational + Inferential Sensors

  示例规则：
  - 新代码没有对应测试 → Stop Hook 要求补充
  - 测试覆盖率低于 80% → CI 失败
  - 关键路径缺少 E2E 覆盖 → 评估 Sub-agent 检查
```

---

### K.4 可观测性：让 Agent 能「看见」自己的行为

#### 为什么 Agent 需要可观测性

AI Agent 的遥测是指在运行时从 Agent 工作流中收集追踪、指标和日志。这一点很重要，因为 Agent 的决策发生在模型内部，而不是在源代码中。没有遥测，你就无法调试、测试或验证生产中的 Agent 行为。

没有可观测性，这个循环就没有闭合。我们仍然处于早期阶段，但方向感觉是对的：人类定义工作和结果，Harness 决定如何实现它们。

传统可观测性问题：「服务器是否正常？」
AI Agent 可观测性问题：「Agent 是否推理正确？」

#### OpenTelemetry：业界标准骨干

到 2026 年初，超过 70% 的企业 AI Agent 部署使用 OpenTelemetry 作为遥测骨干。CrewAI、Pydantic AI 等框架都以 OpenTelemetry 格式发送数据。它不再是可选的——它是基线。

OpenTelemetry 对 LLM Agent 定义了标准语义约定，统一捕获：

```python
# 一个完整的 Agent Span 包含：
span = {
    "name": "claude.agent.turn",
    "attributes": {
        # LLM 调用信息
        "gen_ai.system": "anthropic",
        "gen_ai.model": "claude-sonnet-4-6",
        "gen_ai.usage.input_tokens": 4523,
        "gen_ai.usage.output_tokens": 876,
        "gen_ai.usage.cache_read_tokens": 3100,  # 缓存命中
        
        # Agent 行为信息
        "agent.tool_calls": ["Read", "Edit", "Bash"],
        "agent.task_id": "F003",
        "agent.session_id": "2026-03-30-001",
        "agent.retry_count": 0,
        
        # 成本信息
        "gen_ai.cost.total_usd": 0.0312,
        "gen_ai.cost.cache_savings_usd": 0.0089,
    }
}
```

#### 四层遥测数据

```
Tier 1：Traces（追踪）
  每个 Agent 动作的完整调用链
  工具调用序列、推理步骤、重试记录
  → 用于：调试失败、理解 Agent 决策过程

Tier 2：Metrics（指标）
  Token 用量、成本、延迟、缓存命中率
  工具调用成功率、任务完成率
  → 用于：性能监控、成本控制、质量趋势

Tier 3：Logs（日志）
  结构化事件流（JSON 格式）
  Agent 启动/停止、特性完成、Blocker 记录
  → 用于：审计、长任务进度追踪

Tier 4：Trajectories（轨迹）
  Agent 在特定任务上的完整行为路径
  包括所有中间状态和决策点
  → 用于：评估 Agent 质量、发现系统性失败模式
```

#### 在 Claude Code / Agent SDK 中接入遥测

**方式 1：PostToolUse Hook 收集每次工具调用数据**

```bash
#!/bin/bash
# .claude/hooks/post-observe.sh
# 每次工具调用后记录遥测

TOOL_NAME=$(echo "$CLAUDE_TOOL_NAME" 2>/dev/null || echo "unknown")
SESSION_ID=$(echo "$CLAUDE_SESSION_ID" 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# 追加到结构化日志文件
cat >> /tmp/agent-telemetry.jsonl << EOF
{"timestamp":"$TIMESTAMP","session":"$SESSION_ID","tool":"$TOOL_NAME","status":"$1"}
EOF

# 可选：发送到 OpenTelemetry Collector
# curl -s -X POST http://localhost:4318/v1/traces \
#   -H "Content-Type: application/json" \
#   -d "{\"tool\":\"$TOOL_NAME\",\"session\":\"$SESSION_ID\"}" > /dev/null
```

**方式 2：Claude Agent SDK 中集成 OpenTelemetry**

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from anthropic import Anthropic

# 初始化追踪
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("agent-harness")

def run_agent_with_telemetry(task: str, feature_id: str):
    with tracer.start_as_current_span("agent.task") as span:
        span.set_attribute("agent.feature_id", feature_id)
        span.set_attribute("agent.task", task[:200])
        
        client = Anthropic()
        
        # 记录每次 API 调用的 Token 用量
        response = client.messages.create(...)
        
        span.set_attribute("gen_ai.usage.input_tokens", 
                          response.usage.input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens",
                          response.usage.output_tokens)
        span.set_attribute("gen_ai.cost.total_usd",
                          calculate_cost(response.usage))
        
        return response
```

**方式 3：Stop Hook 输出每日摘要**

```bash
#!/bin/bash
# .claude/hooks/stop-telemetry-summary.sh
# 会话结束时生成可读摘要

SESSION_LOG="/tmp/agent-telemetry.jsonl"
if [ ! -f "$SESSION_LOG" ]; then exit 0; fi

# 统计本次会话数据
TOOL_COUNT=$(wc -l < "$SESSION_LOG")
UNIQUE_TOOLS=$(jq -r '.tool' "$SESSION_LOG" | sort -u | tr '\n' ', ')

echo "本次会话摘要：" >&2
echo "  工具调用次数：$TOOL_COUNT" >&2
echo "  使用工具：$UNIQUE_TOOLS" >&2

# 清理日志，准备下次会话
> "$SESSION_LOG"
```

#### 可观测性驱动的闭环

开发周期变成了一个闭合循环：Agent 为代码添加监控，运行变更，收集遥测，查询追踪，运行评估，如果需要则迭代，并提交带有证据的变更。没有遥测，Agent 就是在盲目操作。

```
Agent 实现代码
    ↓
Stop Hook 运行测试，收集追踪
    ↓
Agent 读取追踪数据查询失败原因
    ↓
Agent 修复并重新运行
    ↓
测试通过，追踪数据正常
    ↓
Agent 提交 PR，附带遥测证据
（「此 PR 通过 47 个测试，P99 延迟 <200ms，Token 成本 $0.031」）
```

---

### K.5 部署验证：影子部署在 Agent 场景中的应用

#### 为什么部署验证特别重要

Agent 生成的代码通过了所有测试，但在生产环境中与真实用户的行为交互时，可能会暴露测试覆盖不到的边缘情况。影子部署是在零用户影响下验证新实现的最可靠方式。

Datadog 的方式是以 Harness 优先的工程：与其逐行阅读 Agent 生成的代码，不如投资于能在几秒内高置信度告知代码是否正确的自动化检查。Agent 生成代码，Harness 验证它，生产遥测确认它，如果出了问题，反馈更新 Harness，Agent 再次尝试。

#### Claude Agent SDK 场景下的影子部署实现

**Step 1：在 Agent 实现新版本时同时部署影子实例**

```python
# 在 features.json 中为需要影子验证的特性添加标记
{
  "id": "F003",
  "name": "OAuth 第三方登录",
  "shadow_validation": {
    "enabled": true,
    "traffic_percentage": 100,  # 复制 100% 流量到影子
    "compare_fields": ["user_id", "session_token", "redirect_url"],
    "ignore_fields": ["timestamp", "request_id"],  # 忽略不稳定字段
    "alert_on_diff_rate": 0.01  # 差异率超过 1% 时告警
  }
}
```

**Step 2：通过 Stop Hook 触发影子部署验证**

```bash
#!/bin/bash
# .claude/hooks/stop-shadow-validate.sh
# 特性完成后触发影子部署验证

FEATURE_ID=$(cat docs/claude-progress.json | jq -r '.in_progress.id // empty')
if [ -z "$FEATURE_ID" ]; then exit 0; fi

# 检查该特性是否需要影子验证
SHADOW_ENABLED=$(cat docs/features.json | \
  jq --arg id "$FEATURE_ID" \
  '.features[] | select(.id == $id) | .shadow_validation.enabled // false')

if [ "$SHADOW_ENABLED" = "true" ]; then
  echo "触发影子部署验证：$FEATURE_ID" >&2
  
  # 通过 HTTP Hook 触发 CI 系统启动影子部署
  curl -s -X POST "$CI_SHADOW_DEPLOY_URL" \
    -H "Authorization: Bearer $CI_TOKEN" \
    -d "{\"feature_id\": \"$FEATURE_ID\", \"branch\": \"$(git branch --show-current)\"}" \
    > /dev/null
    
  echo "影子部署已触发，结果将通过 Slack 通知" >&2
fi
```

**Step 3：影子比对结果反馈给 Agent**

```python
# 影子比对服务：发现差异后写入 blockers
def shadow_validation_callback(feature_id: str, diff_results: dict):
    if diff_results["diff_rate"] > 0.01:
        # 将差异写入进度文件的 blockers
        progress = load_progress()
        progress["in_progress"]["blockers"].append({
            "id": f"B-SHADOW-{feature_id}",
            "description": f"影子部署发现行为差异：{diff_results['summary']}",
            "needs_human": False,  # Agent 可以自行修复
            "shadow_diff": diff_results["sample_diffs"][:3]  # 提供示例
        })
        save_progress(progress)
        
        # 下次 Agent 会话启动时会读到这个 blocker，自动修复
```

#### 三种部署验证策略

| 策略 | 适用场景 | 成本 | 实现方式 |
|------|---------|------|---------|
| **影子部署** | 核心业务逻辑重写 | 中 | 流量复制，对比输出，用户无感知 |
| **金丝雀发布** | 性能优化、UI 改动 | 低 | 5% 用户先用新版本，监控异常 |
| **沙箱测试** | 有副作用的操作（支付、邮件） | 低 | 隔离环境完整运行，验证后删除 |

**对 Agent 生成代码的关键原则**：

```
涉及数据写入的特性   → 必须经过沙箱测试再影子验证
涉及算法/逻辑重写   → 影子部署对比新旧行为
涉及纯 UI/文案改动  → 金丝雀 + 用户行为指标监控
涉及性能优化        → 影子部署测量延迟变化
```

---

### K.6 垃圾回收：对抗代码库熵增的系统性机制

#### 熵增的本质

内部称之为「上下文熵」——AI Agent 在长会话中随复杂度增长变得混乱或产生幻觉的倾向。Harness 对此有多层回退机制。

代码库层面的熵增更隐蔽，以三种形式出现：

```
类型 1：文档漂移
  代码改了，文档没更新
  CLAUDE.md 里的规则已经不再必要，却还在消耗 Token
  architecture.md 里的模块结构已经过时

类型 2：架构漂移
  早期的架构规则随时间被新代码悄悄违反
  「只有一个地方违反」逐渐变成「每个地方都违反」
  没有持续检测，违规堆积成技术债

类型 3：代码熵（Code Entropy）
  死代码、重复实现、过度耦合
  命名约定开始分叉
  测试开始针对实现细节而非行为
```

#### OpenAI 的演化：从周五大扫除到持续小批次

OpenAI 最初每周五花 20% 时间清理「AI 产生的杂乱代码」——不可持续。他们的解决方案是把清理工作编码进仓库，建立一个持续运行的清理流程：后台 Codex 任务扫描偏差，更新质量分级，开具有针对性的重构 PR，大多数这些 PR 在一分钟内被审阅并自动合并。技术债被视为高息贷款，每天小额偿还而不是让其积累。

**关键转变**：从「事后集中清理」到「持续自动维护」。

#### 四类垃圾回收 Agent

**类型 1：文档同步 Agent（每日运行）**

```markdown
# .claude/commands/sync-docs.md
---
description: 检查文档和代码的一致性，发现漂移时提 PR 修复
---
用 subagent 执行以下检查：

1. 扫描 docs/architecture.md 中的目录结构描述
   与 src/ 实际目录对比，找出不一致之处

2. 检查 CLAUDE.md 中的每条规则
   在代码库中验证是否仍然适用
   - 规则对应的错误模式是否还存在？
   - 规则是否已被其他机制（Hook/Linter）覆盖而变得多余？

3. 检查 docs/decisions/ 中状态为「已采纳」的 ADR
   验证对应的技术选型是否仍然在使用

对每个发现的漂移，生成具体的修复建议，汇总后提交 PR。
PR 标题格式：「docs: 同步文档与代码实际状态 [自动]」
```

**类型 2：架构约束扫描 Agent（每周运行）**

```bash
#!/bin/bash
# scripts/harness:scan-arch.sh
# 扫描所有架构违规，生成质量报告

echo "=== 架构健康度扫描 ===" 

# 检查依赖方向违规
echo "## 依赖方向违规"
npx dep-cruiser src --config .deprc.json \
  --output-type markdown 2>&1 | head -50

# 检查过大的模块
echo "## 过大文件（> 300 行）"
find src -name "*.ts" -not -path "*/node_modules/*" | \
  xargs wc -l | sort -rn | head -20

# 检查缺少测试的新文件
echo "## 缺少对应测试的文件"
for f in $(git log --since="7 days ago" --name-only --format="" | grep "^src/" | sort -u); do
  test_file="${f/src\//tests\/}"
  test_file="${test_file%.ts}.test.ts"
  if [ ! -f "$test_file" ]; then
    echo "  缺少测试：$f"
  fi
done
```

```markdown
# .claude/commands/scan-arch.md
---
description: 运行架构健康度扫描并处理发现的问题
---
1. 运行 `bash scripts/harness:scan-arch.sh` 获取架构健康报告
2. 对每个发现的问题评估严重程度：
   - 依赖方向违规：立即修复，提 PR
   - 过大文件：评估是否需要拆分，在 notes 里记录建议
   - 缺少测试：补充基本测试，提 PR
3. 更新 docs/quality.md 中的质量评分
```

**类型 3：CLAUDE.md 瘦身 Agent（每次新模型发布后）**

```markdown
# .claude/commands/trim.md
---
description: 评估 CLAUDE.md 中哪些规则已经不再必要
---
对 CLAUDE.md 中的每条规则逐一评估：

问题 1：Claude 是否在没有这条规则时仍然自然遵守？
  → 用 Claude 本身来检验：给出没有这条规则的 Prompt，
    看 Claude 是否自动做出正确行为
    
问题 2：这条规则是否已被 Hook 或 Linter 覆盖？
  → 如果同样的约束已有 Computational Sensor，
    CLAUDE.md 中的文字版本只是冗余 Token

问题 3：这条规则是否对应一个真实存在的失败模式？
  → 检查最近 4 周的 Agent 失败记录，
    这条规则是否被触发过？

对可以删除的规则生成 PR，注明删除原因。
目标：CLAUDE.md 保持在 60 行以内。
```

**类型 4：代码熵检测 Agent（每月运行）**

```markdown
# .claude/commands/scan-entropy.md
---
description: 检测代码库熵增，发现需要重构的区域
---
用 subagent 执行以下检测：

1. 死代码检测
   运行 `npx ts-prune` 找出从未被调用的导出
   
2. 重复代码检测  
   运行 `npx jscpd src --threshold 10` 找出重复代码块
   
3. 过度耦合检测
   分析 src/service/ 中哪些服务被超过 3 个其他服务引用
   
4. 测试质量评估
   找出只测试实现细节（不测行为）的测试文件
   标志：大量 spy/mock 但没有用户场景验证

汇总生成「代码健康度报告」，存入 docs/quality.md，
并为最严重的 3 个问题各自创建 GitHub Issue。
```

#### 垃圾回收的调度配置

```yaml
# .github/workflows/harness-maintenance.yml
name: Harness 自动维护

on:
  schedule:
    - cron: '0 2 * * *'    # 每天凌晨 2 点：文档同步
    - cron: '0 3 * * 1'    # 每周一：架构扫描
    - cron: '0 4 1 * *'    # 每月 1 日：代码熵检测
  workflow_dispatch:         # 支持手动触发

jobs:
  doc-sync:
    if: github.event.schedule == '0 2 * * *' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 运行文档同步 Agent
        run: claude --headless "/harness:sync-docs"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

### K.7 上下文熵管理：Claude Code 的三层记忆架构

#### 上下文熵（Context Entropy）

最重要的竞争收获在于 Anthropic 如何解决「上下文熵」——AI Agent 随着长会话的复杂度增长变得混乱或产生幻觉的倾向。泄露的源码揭示了一个复杂的三层记忆架构，从传统的「存储一切」检索方式转变而来。

#### 三层记忆架构

架构核心是 MEMORY.md，一个轻量级的指针索引（每行约 150 个字符），始终加载到上下文中。这个索引不存储数据，它存储位置。实际项目知识分布在「主题文件」中按需获取，而原始对话记录从不完整读回上下文，只是对特定标识符进行「grep」。「严格写入纪律」——Agent 只在成功写入文件后才更新其索引——防止模型用失败尝试污染上下文。

```
Layer 1：MEMORY.md（永久在上下文中，极小）
  每行约 150 字符，只存位置指针
  例如：
  「认证逻辑 → src/service/auth/，见 auth-decisions.md」
  「数据库模式 → docs/design/schema.md，最后更新 2026-03-15」
  不存实际内容，只存「去哪里找」

Layer 2：主题文件（按需加载到上下文）
  auth-decisions.md：认证相关的设计决策
  api-patterns.md：API 设计模式
  testing-patterns.md：测试规范
  按需加载，使用完后从上下文移除

Layer 3：历史对话（永不完整读回）
  存在 ~/.claude/projects/ 中
  只通过 grep 查找特定信息
  例如：grep "OAuth 错误处理" 历史会话
  不是把整个历史加载回来
```

#### 对团队 Harness 设计的启发

这个架构有三个值得借鉴的设计原则：

**原则 1：索引而非内容**

不要把所有信息塞进 CLAUDE.md，而是在 CLAUDE.md 里放「在哪里找」的指针，实际内容放在分散的专题文件里。

```markdown
# CLAUDE.md（保持 < 60 行）

## 关键文档索引
- 认证设计 → docs/design/auth.md
- 数据库模式 → docs/design/schema.md  
- API 规范 → docs/design/api-conventions.md
- 架构决策 → docs/decisions/README.md
- 当前进度 → docs/claude-progress.json
```

**原则 2：按需加载知识**

使用 Skills 实现知识的按需注入：只有当任务匹配时，才把相关的详细知识加载进上下文。这就是 Claude Code 的 Skills 系统的设计哲学。

**原则 3：严格写入纪律**

Agent 更新 MEMORY.md 或 claude-progress.json 时，必须在文件成功写入后才更新索引。通过 PostToolUse Hook 验证文件写入成功：

```bash
#!/bin/bash
# .claude/hooks/post-verify-write.sh
# 文件写入后验证成功，防止索引与实际内容不一致

TOOL=$(echo "$CLAUDE_TOOL_NAME" 2>/dev/null || echo "")
FILE=$(echo "$CLAUDE_TOOL_INPUT" 2>/dev/null | jq -r '.path // empty')

if [ "$TOOL" = "Write" ] && [ -n "$FILE" ]; then
  if [ ! -f "$FILE" ]; then
    echo "错误：文件写入声明成功但文件不存在：$FILE" >&2
    exit 2  # 反馈给 Agent，要求重新写入
  fi
fi
exit 0
```

---

### K.8 实践路线图：从零到完整验证体系

以下是根据手册 J.8 「前 30 天路线图」的配套验证能力建设顺序：

**第 1-2 周：建立基础 Sensors（Computational）**

```
优先级 1：Stop Hook（类型检查 + Linter）
  → 这是最高 ROI 的单个投入
  → 覆盖：代码格式、类型错误、基本规范

优先级 2：PreToolUse Hook（权限控制）
  → 防止访问敏感文件
  → 防止危险命令执行

优先级 3：基础遥测日志
  → 每次会话的工具调用记录
  → Token 成本追踪（用于建立基线）
```

**第 3-4 周：建立架构验证（Architecture Fitness）**

```
优先级 4：架构结构测试（tests/architecture/）
  → 依赖方向检查
  → CI 自动运行

优先级 5：自定义 Linter 规则
  → 针对第 1-2 周观察到的最常见违规
  → 错误信息附带修复说明

优先级 6：/harness:review-pr Slash Command
  → 基于 Sub-agent 的代码审查（Inferential Sensor）
  → PR 提交前统一审查入口
```

**第 5-8 周：建立垃圾回收与持续观测**

```
优先级 7：文档同步 Agent（定时任务）
  → 每天自动检查文档漂移

优先级 8：OpenTelemetry 接入
  → 标准化遥测数据格式
  → 接入可视化平台（Langfuse/Braintrust 等）

优先级 9：影子部署验证流程
  → 从最高风险的特性开始
  → 逐步扩展到所有核心业务逻辑
```

**第 9-12 周：闭环与自动改进**

```
优先级 10：CLAUDE.md 定期瘦身机制
  → 每次新模型发布后评估

优先级 11：代码熵月度扫描
  → 自动生成质量报告

优先级 12：遥测驱动的 Harness 改进
  → 分析追踪数据，识别系统性失败模式
  → 把发现的模式转化为新的 Sensors
```



## L. Superpowers 整合：工作流纪律层

> 📌 来源：[obra/superpowers](https://github.com/obra/superpowers)（Jesse Vincent，MIT）
> Superpowers 是与 Harness Engineering 互补的开源工作流框架，专注于在单次任务执行中强制施加开发纪律（TDD、设计前规划、完成前验证）。

---

### L.1 两者的本质差异

| 维度 | Superpowers | Harness Engineering |
|------|------------|---------------------|
| 核心问题 | Agent 急于动手、跳过设计和测试 | Agent 在复杂环境中偏离、跨会话失忆 |
| 时间视野 | 单次任务执行（小时级） | 多会话长期项目（周/月级） |
| 强制机制 | "1% 规则"：每次响应前必须检查 Skill | 六层协同：Hook 硬拦截 + JSON 状态接力 |
| 跨会话记忆 | 无（依赖当前会话上下文） | `claude-progress.json` + `features.json` |
| 开发规范 | 强制 TDD（RED→GREEN→REFACTOR） | 通过 Hook 执行项目自定义规则 |

一句话：**Superpowers 管「怎么做一件事」，Harness Engineering 管「在什么环境里做事」。**

---

### L.2 整合后的三条连接线

**① Superpowers 工作流 → Harness Skills 层**

将 Superpowers 核心技能适配到 Harness 六层模型的 Skills 层：

| Skill | 触发条件 | 与 Harness 的连接 |
|-------|---------|-----------------|
| **harness:plan** | 实现前（>30 分钟 / 3+ 文件） | 规划结果写入 `claude-progress.json.in_progress` |
| **tdd** | 任何代码编写阶段 | 与 Stop Hook（stop-typecheck.sh）形成软硬双层约束 |
| **harness:verify** | 声明完成前 | 语义层补充 Stop Hook 的机械层，对照 `features.json.acceptance_criteria` |

**② Superpowers 规划流 → 喂入 features.json**

Superpowers 的 Brainstorm → Plan 流程天然充当功能进入 `features.json` 的门控节点，与 OpenSpec 共同构成三层规划链：

```
Superpowers: Brainstorm + harness:plan Skill
        ↓ 人工 Review（对齐意图）
OpenSpec:    proposal.md → tasks.md（可选）
        ↓ 批准后
Harness:     features.json（需求锚点）→ claude-progress.json（执行状态）
```

**③ Harness 跨会话记忆 → 填补 Superpowers 空白**

Superpowers 没有跨会话状态管理。SessionStart Hook 在会话开启时自动读取进度，让 Superpowers 工作流的执行能从上次中断点恢复：

```bash
# scripts/session-start.sh（SessionStart Hook）
# 读取 claude-progress.json → 显示进行中任务
# 读取 features.json       → 重建需求上下文
# 触发归档提示             → completed_features ≥ 10 时
```

---

### L.3 完整执行链路（整合后）

```
SessionStart Hook
  → 恢复 claude-progress.json 中的 in_progress 状态
  → 重建 features.json 需求上下文

harness:plan Skill（整合自 Superpowers）
  → 澄清 features.json 中当前特性的 acceptance_criteria
  → 拆解为 2-5 分钟可验证任务块
  → 等待人工确认后开始执行

tdd Skill（整合自 Superpowers）
  → RED：先写失败测试，确认红色
  → GREEN：最小实现让测试通过
  → REFACTOR：在测试保护下清理

Stop Hook（stop-typecheck.sh）
  → 硬拦截：类型检查 + 测试不通过则阻止完成

harness:verify Skill（整合自 Superpowers）
  → 对照 acceptance_criteria 逐条验收
  → 四层检查：功能 / 质量 / 架构 / 集成

claude-progress.json 更新
  → in_progress → completed_features
  → features.json status → "completed"
```

---

### L.4 Superpowers 的 14 个 Skill 与 Harness 的对应

| Superpowers Skill | 在 Harness 中的位置 | 优先级 |
|---|---|---|
| Using Superpowers（元 Skill） | → `harness:router` 触发规则 Steps 4-6 | 已整合 |
| Writing Plans | → `skills/plan/` | 已整合 |
| Test-Driven Development | → `skills/tdd/` | 已整合 |
| Verification Before Completion | → `skills/verify/` | 已整合 |
| Systematic Debugging | → `skills/` 可按需添加 | 推荐 |
| Dispatching Parallel Agents | → `agents/` 层已有类似模式 | 参考 |
| Using Git Worktrees | → 可作为 features.json 多人协作扩展 | 参考 |
| Finishing a Development Branch | → `/harness:review-pr` Command 已覆盖部分 | 参考 |

---

| 资源 | 内容 |
|------|------|
| [Anthropic 官方博客](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | *"Effective harnesses for long-running agents"*（2025.11） |
| [Anthropic 官方博客](https://www.anthropic.com/engineering/harness-design-long-running-apps) | *"Harness design for long-running application development"*（2026.03.24）★ |
| [OpenAI Engineering](https://openai.com/index/harness-engineering/) | *"Harness engineering: leveraging Codex in an agent-first world"*（2026.02） |
| [InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/) | *"OpenAI Introduces Harness Engineering"*（2026.02） |
| [Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) | Harness Engineering 分析（2026.02，2026.04 更新）★ |
| [Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) | *"Humans and Agents in Software Engineering Loops"*（2026.03.04）★ |
| [Mitchell Hashimoto](https://mitchellh.com/writing/my-ai-adoption-journey) | *"My AI Adoption Journey"*（2026.02） |
| [Claude Code 官方最佳实践](https://code.claude.com/docs/en/best-practices) | 官方权威指导 |
| [Claude Code 官方 Sub-agents 文档](https://code.claude.com/docs/en/sub-agents) | Sub-agent 完整使用文档（含 26 个 Hook 事件）★ |
| [HumanLayer：MCP vs CLI 实践](https://www.humanlayer.dev/blog/skill-issue-harness-engineering) | MCP 工具选型与 Hook 真实脚本案例★ |
| [Claude Code 源码架构分析](https://wavespeed.ai/blog/posts/claude-code-agent-harness-architecture/) | 基于 2026.03.31 源码泄露的架构解析★ |
| [社区最佳实践](https://rosmur.github.io/claudecode-best-practices/) | 6 个月社区经验汇总 |
| [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) | Skills/Hooks/Commands 精选资源库 |
| [Claude Code Deep Dive](https://tw93.fun/en/2026-03-12/claude.html) | 六层架构深度分析 |
| [SF 工程领袖田野调查](https://www.infosectoday.io/everything-i-learned-about-harness-engineering-and-ai-factories-in-san-francisco-april-2026/) | 2026.04 旧金山一线实践报告★ |
| [obra/superpowers](https://github.com/obra/superpowers) | Superpowers：14 个可组合工作流 Skill，TDD + 规划 + 验证（Jesse Vincent，MIT）★★ |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | Spec-Driven Development（SDD）框架，规格作为资产，YC W26★★ |
| [Martin Fowler：SDD 三类工具分析](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) | Kiro、spec-kit、Tessl 横向对比（2026.04）★★ |

> ★ 标注为 2026 年 3-4 月新增资源，对应 J 节内容
> ★★ 标注为 2026 年 4 月新增资源，对应 L 节 Superpowers 整合内容
