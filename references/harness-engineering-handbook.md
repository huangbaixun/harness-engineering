# Harness Engineering 速查手册

> 本文件是 Harness Engineering 核心概念的浓缩参考，供 Skills 和 Commands 按需加载。
> 完整手册见：`references/HarnessEngineering.md`（本地文件，不纳入版本控制）

## 核心定义

Harness Engineering 是将工程师的核心工作从「编写代码」转变为「设计让 AI 智能体可靠工作的环境」。

模型是骏马——强大但不自知方向；Harness 是缰绳、鞍具和衔铁——引导力量朝正确方向。

## 三个演进阶段

| 阶段 | 时间 | 核心关注点 |
|------|------|-----------|
| Prompt Engineering | 2022–2024 | 优化单次推理的指令质量 |
| Context Engineering | 2025 | 确保模型在推理时获得正确的上下文 |
| **Harness Engineering** | **2026–** | **在系统层面架构约束、反馈循环和验证机制** |

## 四大组成要素

| 要素 | 内容 |
|------|------|
| 上下文工程 | 持续充实的知识库（CLAUDE.md、设计文档、架构图） |
| 架构约束 | 通过 Linter 和结构化测试机械性强制执行 |
| 验证与反馈 | CI 管道、测试；每次失败都触发 Harness 改进 |
| 垃圾回收 | 周期性运行清理，检测文档陈旧、架构漂移、代码熵增 |

## 六层模型

| 层级 | 组件 | 核心职责 |
|------|------|---------|
| ① 记忆层 | CLAUDE.md | 静态知识：架构约定、禁止规则、测试命令 |
| ② 规则层 | settings.json | 确定性行为：权限、模型、输出配置 |
| ③ 技能层 | skills/ + commands/ | 按需知识和手动触发工作流 |
| ④ 智能体层 | agents/ | 上下文隔离的专用 Subagent |
| ⑤ 钩子层 | Hooks | 确定性强制：不依赖模型判断 |
| ⑥ 工具层 | MCP Servers | 能力扩展：外部服务接入 |

**单层失效陷阱**：三者协同才能真正有效——CLAUDE.md 规则单独使用会被偶尔忽略；Hooks 单独使用无法处理判断性任务；settings.json 单独使用缺乏上下文。

## 核心原则

1. **上下文重置优于无限压缩**：定期清空并结构化交接比累积更有效
2. **永远不要让创建者独立评审自己的产出**：分离生成与评估角色
3. **随模型进化精简 Harness**：新模型解决了某类失败时，主动删除脚手架
4. **约束赋能，而非限制**：架构约束越严格，Agent 产出越可靠
5. **上下文是稀缺资源**：批判性审视每个加入上下文窗口的内容
6. **权限强制与模型推理分离**：CLAUDE.md 解释原因，Hook 强制执行

## 核心循环

```
Agent 失败 → 识别缺失的能力 → 工程化修复（更新文档/添加Linter/构建工具）→ 该失败永不再发生
```

## 「在环路上」的角色定位

```
在环路外（Vibe Coding）  → 人给需求，Agent 自由发挥 → 可能可用，但不可控
在环路中（微管理）       → 审查每行代码 → 质量有保证，但人是瓶颈
在环路上（Harness Engineering）→ 设计约束、维护 Harness → 质量有保证，速度快
```

正确做法：对 Agent 产出不满意时，改进产生这个产物的 Harness，而不是直接修改产物。

## 前馈与反馈体系

| 控制方向 | 类型 | 典型实现 |
|---------|------|---------|
| 前馈（Guides） | Computational | CLAUDE.md 架构约定、依赖规则 |
| 前馈（Guides） | Inferential | Skills 领域知识注入 |
| 反馈（Sensors） | Computational | Stop Hook 类型检查、CI 结构测试 |
| 反馈（Sensors） | Inferential | 安全审查 Sub-agent |

原则：先用 Computational 覆盖 80% 常见问题，再用 Inferential 处理语义层面的剩余 20%。

## 反模式速查

| 反模式 | 修复 |
|--------|------|
| CLAUDE.md 超过 100 行 | 精简至 <60 行，移入 docs/ |
| 滥用 MCP（20+ Server） | 按需接入，不用时禁用 |
| 测试成功时输出 4000 行日志 | 成功静默，失败才输出 |
| 所有约定放 CLAUDE.md | 必须执行 = Hook，应该遵守 = CLAUDE.md |
| 单会话处理 10+ 功能 | 每功能一个会话 + /context-dump |
| 依赖 Compaction 保持记忆 | 用 claude-progress.json 结构化交接 |

## 三层防护

```
Layer 1: settings.json     → 控制 Agent 可以调用哪些工具（系统级）
Layer 2: PreToolUse Hook   → 在允许的工具范围内检查参数（拦截层）
Layer 3: CLAUDE.md         → 解释约束原因，帮助 Agent 主动避免（理解层）
```

## MCP 使用决策框架

```
判断 1：模型有没有内置知识？
  git/npm/docker/gh CLI... → 直接用 CLI（模型已训练过）
  你公司的内部 API        → 需要 MCP 或自定义 CLI 封装

判断 2：工具有多少个操作？
  只用 3 个操作 → 写 CLI 封装 + CLAUDE.md 说明（约 100 Token）
  用 20+ 操作  → 使用 MCP Server（约 3000-9000 Token）

判断 3：CLI 输出是否高效？
  简洁结构化 → 用 CLI
  冗长噪声多 → 用 MCP（可控制返回格式）
```

## Harness 成熟度路径

```
阶段 1：人建 Harness，Agent 在 Harness 内工作（大多数团队当前状态）
阶段 2：Agent 发现问题，记录在 progress.json，人定期审查转化为改进（推荐目标）
阶段 3：Agent 发现问题后直接提 PR，人审批后合并（OpenAI 垃圾回收 Agent 模式）
阶段 4：Harness 自动优化自身（Meta-Harness，实验阶段）
```

## 衡量成效的正确指标

```
❌ 错误：「本周帮 Agent 修复了 20 个 Bug」
✅ 正确：「本周新增了 3 条架构 Linter 规则，这类 Bug 不会再出现」

❌ 错误：「写了详细的 CLAUDE.md 让 Agent 不犯错」
✅ 正确：「通过 Hook + settings.json 让物理上无法犯那些错」
```
