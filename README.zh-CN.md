# Harness Engineering Plugin

[![Version](https://img.shields.io/badge/version-v1.10.1-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A51.0.0-orange)](https://docs.claude.com)

**把工程师的核心工作从「编写代码」转变为「设计让 AI 智能体可靠工作的环境」。**

Harness Engineering Plugin 将这套方法论落地为可直接使用的 Skills、Commands 和 Agents——安装即用，无需额外配置。

---

## 快速上手

**第一步：安装**

**方式 A — Marketplace 订阅（推荐，自动更新）**

在 Claude Code 对话中运行：

```
/plugin marketplace add https://raw.githubusercontent.com/huangbaixun/harness-engineering/main/.claude-plugin/marketplace.json
```

订阅后从列表中选择安装，新版本发布时 Claude Code 自动提示更新。

**方式 B — 从 GitHub 克隆本地加载**

```bash
git clone https://github.com/huangbaixun/harness-engineering.git
claude --plugin-dir ./harness-engineering
```

适合想先本地验证再决定是否长期使用的场景。

**方式 C — 官方 Marketplace（即将上线）**

```bash
# 待 Anthropic 审核通过后可用
claude plugins add harness-engineering
```

或在 Cowork 中搜索「Harness Engineering」点击安装。

**第二步：初始化新项目**

在 Claude Code 中说：

> 「帮我初始化这个项目的 Harness」

初始化完成后，你的项目会获得：

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | 通用记忆层（≤60 行），唯一真相来源 |
| `CLAUDE.md` | Claude Code 用户的 2 行入口，指向 AGENTS.md |
| `init.sh` | 会话启动脚本，每次新会话前运行 |
| `.claude/settings.json` | 权限控制 + Hook 注册（含 SessionStart） |
| `.claude/hooks/session-start.sh` | SessionStart Hook：会话开启时恢复进度上下文 |
| `.claude/hooks/` | 类型检查、.env 保护、自动格式化 |
| `.claude/skills/plan/` | 实现前规划 Skill（>30 分钟或 3+ 文件时触发） |
| `.claude/skills/tdd/` | TDD Skill（RED→GREEN→REFACTOR 强制循环） |
| `.claude/skills/verify/` | 完成前验证 Skill（声明 done 前四层检查） |
| `docs/architecture.md` | 架构图，Agent 的空间感知文档 |
| `docs/claude-progress.json` | 跨会话进度追踪 |

验证就绪：`bash init.sh`，看到「Harness 就绪 ✓」即可开始使用。

**第三步：持续受益**

SessionStart Hook 每次会话开启自动恢复进度上下文。harness:plan / harness:tdd / harness:verify 三个工作流 Skill 在实现阶段自动介入，确保规划→实现→验证完整闭环。Commands 支持随时触发审计、PR 审查和代码熵增检测。

---

## 核心 Skills

安装后，以下 Skill 根据你的意图自动触发，无需记忆命令名。所有 Skill 统一使用 `harness:` 命名空间：

| Skill | 触发场景 | 做什么 |
|-------|---------|--------|
| **harness:init** | 新项目 / 「帮我搭建 Harness」 | 生成完整六层 Harness 结构（AGENTS.md + Hooks + 模板） |
| **harness:audit** | 「Agent 老是犯同样的错」/ 存量项目审计 | 七维度健康评分 + 优先级修复方案 |
| **harness:evolve** | 「AGENTS.md 太长了」/ 新模型发布后 | 记忆文件瘦身 + Hooks 适配 + 垃圾回收 |
| **harness:router** | 所有场景（1% 规则，每次加载） | 意图识别，确保上述 Skill 被正确触发 |
| **harness:plan** | 实现新功能 / 修 Bug（>30 分钟或涉及 3+ 文件） | 拆解为可验证任务块，`<action>/<verify>/<done>` 三段式结构 |
| **harness:archive** | 特性完成后归档 | Spec 归档至 `docs/archive/`、文档一致性检查、架构快检 |
| **harness:tdd** | 任何代码编写（与 1% 规则绑定） | 强制 RED→GREEN→REFACTOR 循环，先写测试再写实现 |
| **harness:verify** | 准备声明任务完成前 | 四层检查（Functional / Quality / Architecture / Integration） |

---

## Slash Commands

| Command | 功能 | 推荐频率 |
|---------|------|---------|
| `/harness:init` | 初始化 Harness | 项目启动 |
| `/harness:audit` | Harness 健康度审计 | 按需 |
| `/harness:assign` | Sprint feature 分配规划，自动算依赖 + 生成认领脚本 | Sprint 开始时 |
| `/harness:review-pr` | PR 全面审查（质量 + 安全 + 架构） | 每次 PR |
| `/harness:dump` | 保存会话进度到 claude-progress.json | 上下文 50% 时 |
| `/harness:sync-docs` | 文档与代码一致性检查 | 每日 |
| `/harness:scan-arch` | 架构健康度扫描 | 每周 |
| `/harness:trim` | 精简 AGENTS.md 至 60 行以内 | 新模型发布后 |
| `/harness:scan-entropy` | 死代码 + 重复实现 + 过度耦合检测 | 每月 |

---

## Agents

| Agent | 模型 | 用途 |
|-------|------|------|
| **security-reviewer** | Opus | 注入漏洞、认证缺陷、secret 泄露 |
| **code-review-agent** | Sonnet | 架构合规、可维护性、技术债 |
| **coding-agent** | Sonnet | 长周期多会话编码，跨会话进度交接 |
| **explore-agent** | Haiku | 代码库探索，保持主线程上下文干净 |

---

## 语言模板

`harness:init` 支持五种技术栈，初始化时自动选择匹配的模板：

- **TypeScript / Node.js** — strict mode, pnpm, Jest/Vitest, Biome/ESLint
- **Python** — type hints, poetry/uv, pytest, mypy/ruff
- **Go** — go modules, golangci-lint, testing
- **Java** — JUnit 5 + Mockito + AssertJ, Maven/Gradle, Checkstyle + SpotBugs
- **通用** — 语言无关的 Harness 骨架（含 AGENTS.md 模板）

---

## 平台兼容性

本 plugin 从 v1.9.3 起支持 Windows 跨平台 Hook：

| 特性 | Claude Code | Windows |
|------|-------------|---------|
| AGENTS.md 通用记忆 | ✅ | ✅ |
| init.sh 自动检测 | ✅ | ✅（Git Bash） |
| Skills / Commands | ✅ | ✅ |
| Hooks（Polyglot 包装器） | ✅ | ✅（Git Bash / MSYS2） |

---

## 项目设计原则

本 plugin 完全自举（dogfooding）——用 Harness Engineering 规范开发 Harness Engineering Plugin 本身：

- `AGENTS.md` ≤ 60 行，是唯一真相来源
- `docs/architecture.md` 包含明确的依赖规则
- `docs/decisions/` 有完整 ADR 记录每个关键决策
- Hook 脚本遵循「成功静默、失败可见」原则
- Skills 使用 `.claude/` 路径

---

## 方法论参考

本 plugin 基于 [Harness Engineering 完整实践手册](references/HarnessEngineering.md) 构建——综合 Anthropic、OpenAI、InfoQ、Hacker News 的一手实践，涵盖长周期任务驾驭架设计、多 Agent 架构、垃圾回收体系等核心模式。

v1.9.2 整合了 [obra/superpowers](https://github.com/obra/superpowers) 的工作流设计思路：writing-plans（实现前规划门禁）、tdd（RED→GREEN→REFACTOR 强制循环）、verification（四层完成检查）三个 Skill 直接来源于该项目的核心实践。

多人协作设计参考 [团队并行开发指南](references/team-parallel-development.md)，含 features.json 并行字段设计、Git Worktree 隔离和 Sprint 分配算法。

---

## 参与贡献

欢迎提交新 Skill、语言模板或改进 Hook 脚本。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

[English documentation](README.md)
