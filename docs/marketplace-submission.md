# Anthropic Marketplace 提交材料

> 提交地址：https://claude.ai/settings/plugins/submit  
> 版本：v1.9.0  
> 准备日期：2026-04-10

---

## 1. 基本信息

| 字段 | 内容 |
|------|------|
| **Plugin Name** | harness-engineering |
| **Display Name** | Harness Engineering |
| **Version** | 1.9.0 |
| **Author / Organization** | Harness Engineering |
| **Repository URL** | https://github.com/huangbaixun/harness-engineering |
| **Homepage URL** | https://github.com/huangbaixun/harness-engineering |
| **License** | MIT |
| **Category** | Engineering / Developer Tools |

---

## 2. 一句话描述（Short Description，≤ 120 字符）

```
AI Agent 工程能力建设：初始化、审计、团队 Sprint 分配，支持 Claude Code 和 CodeBuddy，安装即用。
```

英文版：
```
AI Agent Harness Engineering: init, audit, team sprint allocation. Works with Claude Code & CodeBuddy.
```

---

## 3. 详细描述（Long Description，Markdown）

```markdown
## What is Harness Engineering?

Harness Engineering transforms how your team works with AI agents — shifting the focus from "writing code" to "designing environments where AI agents work reliably."

Instead of hoping Claude remembers your conventions, you encode them into a structured **6-layer Harness**: Memory (AGENTS.md), Rules (settings.json), Skills, Agents, Hooks, and MCP Tools.

## What This Plugin Does

Install once, and your projects get:

- **`harness-init`** — Bootstraps a complete AI agent harness for any new project in minutes. Generates AGENTS.md, init.sh, hooks (type-check, .env protection, auto-format), and architecture docs. Supports TypeScript, Python, Go, Java, and generic stacks.

- **`harness-audit`** — Scores your existing project's harness health across 7 dimensions. Pinpoints weak spots and generates a prioritized fix plan.

- **`harness-evolve`** — Runs periodic garbage collection on your harness: trims bloated AGENTS.md files, removes stale rules, adapts hooks to new model capabilities.

- **`/assign-features`** — Sprint planning for AI-assisted teams. Analyzes your `features.json` dependency graph, calculates critical path, and generates a `sprint-kickoff.sh` with per-member task assignments that minimize file conflicts and maximize parallel execution.

## Key Design Principles

- **Tool-agnostic**: Works with Claude Code (`.claude/`) and Tencent CodeBuddy (`.codebuddy/`) — `init.sh` auto-detects your tool at session start
- **AGENTS.md as single source of truth**: One universal memory file, two 2-line wrappers for each tool
- **≤ 60 lines rule**: Based on ETH Zurich research showing performance degrades with oversized memory files
- **Hooks over instructions**: Critical constraints enforced deterministically via hooks, not model judgment

## Quick Start

After installing, just say:

> "帮我初始化这个项目的 Harness" (Help me initialize this project's Harness)

The `harness-init` skill auto-triggers and walks you through setup.
```

---

## 4. 分类标签（Keywords / Tags）

```
harness, agent-engineering, devops, team, sprint, claude-code, codebuddy, hooks, memory, ai-engineering
```

---

## 5. 目标用户（Target Audience）

- 工程团队：希望在多个项目中标准化 AI Agent 工作流
- 全栈工程师：使用 Claude Code 或 CodeBuddy 进行日常编码
- 技术负责人：需要协调多人 AI 辅助开发的 Sprint 规划
- 平台工程师：为团队建立 AI 工程规范和约束体系

---

## 6. Skills 清单（供 Marketplace 展示）

| Skill / Command | 触发场景 | 核心功能 |
|----------------|---------|---------|
| `harness-init` | 新项目初始化 | 六层 Harness 结构生成 |
| `harness-audit` | 存量项目审计 | 七维度健康评分 + 修复方案 |
| `harness-evolve` | 持续优化 | AGENTS.md 瘦身 + Hooks 适配 |
| `using-harness` | 元 Skill（1% 规则） | 意图识别，自动路由到正确 Skill |
| `/assign-features` | Sprint 开始 | 依赖图分析 + 最优 owner 分配 |
| `/review-pr` | 每次 PR | 质量 + 安全 + 架构全面审查 |
| `/context-dump` | 上下文 50% 时 | 跨会话进度保存 |
| `/arch-scan` | 每周 | 架构健康扫描 |

---

## 7. 截图说明（Screenshot Descriptions）

建议准备以下截图：

1. **harness-init 运行效果**：展示初始化后生成的文件树（AGENTS.md、init.sh、hooks/）
2. **init.sh 输出**：展示 `bash init.sh` 后的 Harness 就绪检查输出（含工具检测、进度展示）
3. **harness-audit 健康报告**：展示七维度评分表和优先级修复方案
4. **/assign-features 分配结果**：展示 Sprint 分配表和生成的 sprint-kickoff.sh 片段
5. **AGENTS.md vs CLAUDE.md 对比**：展示工具无关架构的两个文件

---

## 8. 技术兼容性声明

| 环境 | 支持状态 |
|------|---------|
| Claude Code ≥ 1.0.0 | ✅ 完全支持 |
| CodeBuddy（腾讯） | ✅ 完全支持（v1.8.0+） |
| Cowork（Anthropic Desktop） | ✅ 支持（Skill 触发） |
| TypeScript / Node.js 项目 | ✅ 专用模板 |
| Python 项目 | ✅ 专用模板 |
| Go 项目 | ✅ 专用模板 |
| Java 项目 | ✅ 专用模板 |
| 其他语言 | ✅ 通用模板 |

---

## 9. 隐私与安全声明

- 本 plugin **不收集任何用户数据**，不发送任何网络请求
- `userConfig` 中的 `team_name` 和 `default_tech_stack` 仅本地使用，由 Claude Code 安全存储
- 所有 Hook 脚本均为本地 shell 脚本，源码公开可审查：[scripts/](../scripts/)
- 无第三方 MCP 依赖

---

## 10. 提交检查清单

提交前确认：

- [x] `plugin.json` 包含 `name`、`version`、`homepage`、`repository`、`license`
- [x] `skills/`、`commands/`、`agents/`、`hooks/` 均在 plugin 根目录
- [x] 所有 plugin 内部路径使用 `${CLAUDE_PLUGIN_ROOT}` 而非硬编码绝对路径
- [x] `SKILL.md` 包含有效的 YAML frontmatter（`name`、`description`）
- [x] Skills 在无 plugin 前缀时不与常见工具名冲突
- [x] LICENSE 文件存在（MIT）
- [x] README.md 包含快速上手说明
- [x] CHANGELOG.md 记录版本历史
- [x] 已在本地验证 plugin 加载成功（`bash init.sh` 输出正常）
