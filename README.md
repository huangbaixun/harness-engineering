# Harness Engineering Plugin

[![Version](https://img.shields.io/badge/version-v1.5.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A51.0.0-orange)](https://docs.claude.com)

**把工程师的核心工作从「编写代码」转变为「设计让 AI 智能体可靠工作的环境」。**

Harness Engineering Plugin 将这套方法论落地为可直接使用的 Skills、Commands 和 Agents——安装即用，无需额外配置。

---

## 快速上手

**第一步：安装**

```bash
claude plugins add harness-engineering
```

或在 Cowork 中点击「安装 Plugin」。

**第二步：初始化新项目**

在 Claude Code 或 Cowork 中说：

> 「帮我初始化这个项目的 Harness」

`harness-init` Skill 将自动生成完整的六层 Harness 结构，包括 `CLAUDE.md`、Hooks、`docs/` 目录和语言栈最佳实践配置。

**第三步：持续受益**

Hooks 自动运行类型检查、格式化和进度保存。Commands 支持随时触发审计、PR 审查和代码熵增检测。

---

## 核心 Skills

安装后，以下 Skill 根据你的意图自动触发，无需记忆命令名：

| Skill | 触发场景 | 做什么 |
|-------|---------|--------|
| **harness-init** | 新项目 / 「帮我搭建 Harness」 | 生成完整六层 Harness 结构 |
| **harness-audit** | 「Agent 老是犯同样的错」/ 存量项目审计 | 七维度健康评分 + 优先级修复方案 |
| **harness-evolve** | 「CLAUDE.md 太长了」/ 新模型发布后 | CLAUDE.md 瘦身 + Hooks 适配 + 垃圾回收 |
| **using-harness** | 所有场景（1% 规则，每次加载） | 意图识别，确保上述三个 Skill 被正确触发 |

---

## Slash Commands

| Command | 功能 | 推荐频率 |
|---------|------|---------|
| `/harness-init` | 初始化 Harness | 项目启动 |
| `/harness-audit` | Harness 健康度审计 | 按需 |
| `/review-pr` | PR 全面审查（质量 + 安全 + 架构） | 每次 PR |
| `/context-dump` | 保存会话进度到 claude-progress.json | 上下文 50% 时 |
| `/doc-sync` | 文档与代码一致性检查 | 每日 |
| `/arch-scan` | 架构健康度扫描 | 每周 |
| `/trim-claudemd` | 精简 CLAUDE.md 至 60 行以内 | 新模型发布后 |
| `/entropy-scan` | 死代码 + 重复实现 + 过度耦合检测 | 每月 |

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

`harness-init` 支持五种技术栈，初始化时自动选择匹配的模板：

- **TypeScript / Node.js** — strict mode, pnpm, Jest/Vitest, Biome/ESLint
- **Python** — type hints, poetry/uv, pytest, mypy/ruff
- **Go** — go modules, golangci-lint, testing
- **Java** — JUnit 5 + Mockito + AssertJ, Maven/Gradle, Checkstyle + SpotBugs
- **通用** — 语言无关的 Harness 骨架

---

## 本地验证安装

```bash
# 解压 .skill 包到测试目录
unzip harness-engineering.skill -d /tmp/harness-test

# 加载插件
claude --plugin-dir /tmp/harness-test
```

---

## 项目设计原则

本 plugin 完全自举（dogfooding）——用 Harness Engineering 规范开发 Harness Engineering Plugin 本身：

- `CLAUDE.md` ≤ 60 行
- `docs/architecture.md` 包含明确的依赖规则
- `docs/decisions/` 有完整 ADR 记录每个关键决策
- Hook 脚本遵循「成功静默、失败可见」原则

---

## 参与贡献

欢迎提交新 Skill、语言模板或改进 Hook 脚本。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

<details>
<summary>完整文件清单</summary>

```
harness-engineering-plugin/
├── .claude-plugin/
│   └── plugin.json                   ← 官方规范 manifest
├── skills/
│   ├── using-harness/SKILL.md        元 Skill（强制触发，1% 规则）
│   ├── harness-init/SKILL.md         新项目初始化（六阶段）
│   ├── harness-audit/SKILL.md        存量审计（七维度）
│   └── harness-evolve/SKILL.md       持续演进（垃圾回收+瘦身）
├── commands/
│   ├── harness-init.md
│   ├── harness-audit.md
│   ├── review-pr.md
│   ├── context-dump.md
│   ├── doc-sync.md
│   ├── arch-scan.md
│   ├── trim-claudemd.md
│   └── entropy-scan.md
├── agents/
│   ├── security-reviewer.md          Opus
│   ├── explore-agent.md              Haiku
│   ├── code-review-agent.md          Sonnet
│   └── coding-agent.md               Sonnet
├── hooks/
│   └── hooks.json                    ← JSON Hook 注册
├── scripts/
│   ├── stop-typecheck.sh
│   ├── pre-protect-env.sh
│   ├── post-format.sh
│   ├── stop-commit-progress.sh
│   └── post-observe.sh
├── docs/
│   ├── architecture.md
│   ├── decisions/                    ADR 记录
│   └── templates/                    五种语言栈模板
├── references/
│   ├── harness-engineering-handbook.md
│   ├── hook-patterns.md
│   └── anti-patterns.md
├── evals/
│   └── evals.json                    9 个 eval 用例（3 功能 + 6 压力）
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── CLAUDE.md                         自举：≤60 行项目记忆
```

</details>
