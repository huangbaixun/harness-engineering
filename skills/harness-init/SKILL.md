---
name: harness-init
description: >
  新项目 AI Agent Harness 工程初始化。当用户提到「新项目」「项目初始化」「搭建 Harness」
  「创建 CLAUDE.md」「设置 Agent 环境」「init harness」「从零开始」「初始化 AI 编码环境」
  「建立 Agent 约束」「设置 Claude Code 项目」时激活。
  即使用户只是提到要「开始一个新项目」或「配置 AI 开发环境」，也应使用此 Skill，
  因为任何新项目都应该从建立 Harness 开始。
---

# Harness 初始化 Skill

> 本 Skill 指导你为一个新项目建立完整的 AI Agent Harness 工程体系。
> 核心理念：**先观察再约束**——不要在第一天就写满所有规则，而是建立最小可用的 Harness，让团队在实际使用中发现需要补充什么。

## 初始化产物

运行此 Skill 后，项目根目录将生成以下文件：

| 文件 | 作用 | 是否必须 |
|------|------|---------|
| `CLAUDE.md` | Agent 记忆层，≤60 行，架构约定 + 禁止规则 + 测试命令 | ✅ 必须 |
| `.claude/settings.json` | 权限控制 + Hook 注册 | ✅ 必须 |
| `.claude/hooks/stop-typecheck.sh` | Stop Hook：类型检查门禁 | ✅ 必须 |
| `.claude/hooks/pre-protect-env.sh` | PreToolUse：防止 .env 被覆盖 | ✅ 必须 |
| `.claude/hooks/post-format.sh` | PostToolUse：自动格式化 | ✅ 必须 |
| `init.sh` | 会话启动脚本，每次新会话前运行以恢复上下文 | ✅ 必须 |
| `docs/architecture.md` | 架构图，Agent 的空间感知文档，100-150 行 | ✅ 必须 |
| `docs/decisions/README.md` | ADR 索引 | ✅ 必须 |
| `docs/features.json` | 特性清单（结构化需求，Agent 只读） | 🔵 长周期任务时 |
| `docs/claude-progress.json` | 进度追踪骨架（Agent 可写） | 🔵 长周期任务时 |

> **用户期望**：完成初始化后运行 `bash init.sh`，看到当前项目状态摘要，即表示 Harness 基座就绪。

## 初始化流程

### Phase 0：检测已有 Harness（新增）

**在询问任何问题之前**，先扫描项目根目录的现有状态：

```bash
# 检查关键文件是否已存在
ls CLAUDE.md .claude/settings.json .claude/hooks/ init.sh 2>/dev/null
wc -l CLAUDE.md 2>/dev/null
```

根据检测结果，进入以下三条路径之一：

| 场景 | 判断标准 | 处理方式 |
|------|---------|---------|
| **全新项目** | CLAUDE.md 不存在 | 正常走 Phase 1-6，从零生成 |
| **存量项目（有 CLAUDE.md）** | CLAUDE.md 存在，内容有意义 | 进入「存量模式」（见下方） |
| **损坏 / 空文件** | CLAUDE.md 存在但为空或 <5 行 | 提示用户，按全新项目处理 |

#### 存量模式：CLAUDE.md 已存在时的处理流程

1. **读取并评估现有 CLAUDE.md**
   - 行数是否 ≤60？超出多少？
   - 是否有 YAML frontmatter 或结构化章节？
   - 是否包含具体可验证的规则（测试命令、禁止项）？
   - 是否存在模糊无效规则（「写好代码」「保持整洁」）？

2. **告知用户评估结果，明确询问意图**：
   > 「检测到项目已有 CLAUDE.md（当前 X 行）。我可以：
   > A) **增量补充**——保留现有内容，补全缺失的结构（Hooks、docs/ 等）
   > B) **优化整合**——精简现有规则至 ≤60 行，同时补全结构
   > C) **完整重建**——备份现有文件为 CLAUDE.md.bak，重新生成
   > 你倾向于哪种方式？」

3. **执行前强制备份**：
   ```bash
   cp CLAUDE.md CLAUDE.md.bak
   echo "已备份至 CLAUDE.md.bak"
   ```

4. **按选择执行**：
   - **增量补充**：仅在现有文件末尾追加缺失章节，不修改已有内容
   - **优化整合**：调用 `harness-evolve` 的 CLAUDE.md 精简逻辑，再补全结构
   - **完整重建**：用模板重新生成，将原有有价值的规则（测试命令等）迁移进新文件

> 同理检查 `.claude/settings.json`、`init.sh`、`docs/architecture.md` 是否已存在，
> 已存在的文件不覆盖，只在用户明确确认后才替换。

---

### Phase 1：信息收集

在开始生成任何文件之前，先确认以下信息（如果用户没有提供，主动询问）：

1. **技术栈**：主要编程语言、框架、包管理器
2. **项目类型**：Web 应用 / API 服务 / CLI 工具 / 库 / Monorepo
3. **测试框架**：Jest / Vitest / pytest / go test / 其他
4. **CI/CD**：GitHub Actions / GitLab CI / 其他
5. **团队规模**：单人 / 小团队（2-5）/ 中型（5-15）/ 大型（15+）

### Phase 2：生成六层 Harness 结构

Claude Code 的 Harness 不是单一配置文件，而是六个相互协作的层。理解各层职责是避免「配置越多越混乱」的关键。

| 层级 | 组件 | 核心职责 |
|------|------|---------|
| ① 记忆层 | `CLAUDE.md` | 静态知识：架构约定、禁止规则、测试命令 |
| ② 规则层 | `.claude/settings.json` | 确定性行为：权限、模型、输出配置 |
| ③ 技能层 | `.claude/skills/` + `.claude/commands/` | 按需知识和手动触发的工作流 |
| ④ 智能体层 | `.claude/agents/` | 上下文隔离的专用 Subagent |
| ⑤ 钩子层 | Hooks（settings.json 中配置） | 确定性强制：不依赖模型判断 |
| ⑥ 工具层 | MCP Servers | 能力扩展：外部服务接入 |

**三者协同原则**：CLAUDE.md 规则单独使用会被偶尔忽略；Hooks 单独使用无法处理判断性任务；settings.json 单独使用缺乏上下文。三者协同才能真正有效。

### Phase 3：按技术栈生成文件

读取对应的模板目录生成文件。模板位置：

- TypeScript 项目 → 读取 `docs/templates/typescript/`
- Python 项目 → 读取 `docs/templates/python/`
- Go 项目 → 读取 `docs/templates/go/`
- 其他 → 读取 `docs/templates/generic/`

#### 必须生成的文件清单

```
项目根/
├── CLAUDE.md                     ← ≤ 60 行，精简目录
├── init.sh                       ← 会话启动脚本（每次新会话前运行）
├── .claude/
│   ├── settings.json             ← 权限 + Hook 注册
│   └── hooks/                    ← Hook 脚本
│       ├── stop-typecheck.sh     ← Stop Hook（语言适配）
│       ├── pre-protect-env.sh    ← PreToolUse：保护敏感文件
│       └── post-format.sh        ← PostToolUse：自动格式化
├── docs/
│   ├── architecture.md           ← 架构图（100-150 行）
│   ├── decisions/
│   │   └── README.md             ← ADR 索引
│   └── claude-progress.json      ← Agent 进度追踪（空骨架）
```

`init.sh` 模板见：`docs/templates/generic/init.sh.template`

#### CLAUDE.md 编写原则

CLAUDE.md 是 Agent 的「世界观」——它定义了 Agent 对项目的基本认知。

**好的规则**：具体、可验证、对应过去真实的 Agent 失败
- 「永远不要删除迁移文件」
- 「所有公共 API 必须有 JSDoc 注释」
- 「测试命令：`pnpm test`」

**坏的规则**：模糊、无法验证、消耗 Token 却不产生约束力
- 「写高质量代码」
- 「保持代码整洁」

**≤ 60 行原则**：ETH Zurich 研究表明，AI 自动生成的过长 CLAUDE.md 导致性能下降并多消耗 20% Token。人工编写且精简的文件才真正有效。超出部分移入 `docs/` 子目录，CLAUDE.md 中用链接指向。

#### architecture.md 编写原则

核心目标只有一个：让 Agent 在新会话开始时，快速建立对整个系统的空间感知。

必须包含：
1. **系统全局地图**：一句话说清「这是什么系统、有哪几块」
2. **目录结构说明**：每个目录放什么，比 README 更精准
3. **层级依赖规则**：最重要，写清楚边界和自动验证机制
4. **关键模块说明**：复杂模块一句话解释
5. **外部依赖说明**：服务、用途、接入位置
6. **延伸阅读链接**：指向更深层文档

控制在 100-150 行，是「地图而非百科全书」。

#### Hook 脚本原则

**判断标准**：「这个行为必须始终发生，不论 Claude 的判断如何？」→ 如果是，用 Hook。

**成功静默，失败可见**：4000 行通过日志会使 Agent 失去任务焦点。

**退出码约定**：
- `exit 0` — 成功，继续
- `exit 2` — 失败，错误信息反馈给 Agent，Agent 继续修复
- `exit 其他` — 失败，不反馈给 Agent（非阻塞）

### Phase 4：建立初始 ADR

为项目已做出的关键技术决策各创建一个 ADR。每个 ADR 必须包含：
- 背景（写触发条件，不是结论）
- 考虑过的选项（包括被否决的，防止 Agent 重蹈覆辙）
- 决策及理由
- 后果（用「❌ 禁止 X，必须走 Y」格式，对 Agent 最有约束力）

### Phase 5：初始化进度追踪

如果项目需要长周期 Agent 任务（多个特性的实现），生成：

- `docs/features.json` — 需求清单（结构化，Agent 只读）
- `docs/claude-progress.json` — 进度追踪（Agent 可写）

使用 JSON 而非 Markdown：Agent 对结构化数据的尊重程度显著高于纯文本。

### Phase 6：验证与交付

完成初始化后，运行验证检查：

1. CLAUDE.md 行数 ≤ 60
2. 所有 Hook 脚本有执行权限（`chmod +x`）
3. settings.json 中 Hook 注册正确
4. architecture.md 包含依赖规则
5. docs/decisions/README.md 索引完整

输出初始化摘要，包括：
- 生成的文件清单
- 建议的「第 1-2 周观察事项」（先用两周时间在真实工作上运行 Agent，记录失败模式）
- 后续迭代建议（指向 harness-audit 和 harness-evolve）

## 权限强制与模型推理分离

初始化时特别注意这个架构原则：

- **CLAUDE.md** = 解释「为什么不能做」，帮助 Agent 理解意图
- **settings.json + Hooks** = 强制「无论如何都不能做」，不依赖 Agent 的理解

两者都要，各司其职。只有 CLAUDE.md 是软约束，只有 Hook 是硬约束但缺少上下文解释，两者结合才是完整防护。

## 反模式提醒

生成时注意避免以下反模式：

| 反模式 | 正确做法 |
|--------|---------|
| 过度膨胀的 CLAUDE.md（>100 行） | 删减至 <60 行，复杂规则移入 Hook |
| 所有约定都放 CLAUDE.md | 「必须执行」= Hook；「应该遵守」= CLAUDE.md |
| 不写被否决的选项 | ADR 必须列被否决的选项，防止 Agent 重提 |
| Hook 成功时输出日志 | 成功完全静默，只有失败才产生输出 |
