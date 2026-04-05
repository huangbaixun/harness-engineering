# Harness Engineering Plugin — 架构图

## 系统概览

这是一个 Claude Code / Cowork plugin，为工程团队提供标准化的 AI Agent Harness 工程能力建设。
主要由三个核心 Skill 和一组配套 Commands、Hooks、References 构成。

## 目录结构

```
harness-engineering-plugin/
├── CLAUDE.md                       ← 项目级规则（< 60 行，自举示范）
├── .claude/
│   ├── skills/
│   │   ├── harness-init/           ← 新项目 Harness 初始化
│   │   │   ├── SKILL.md
│   │   │   └── scripts/            ← 初始化生成脚本
│   │   ├── harness-audit/          ← 存量项目健康度检查与优化
│   │   │   ├── SKILL.md
│   │   │   └── scripts/            ← 扫描和评分脚本
│   │   └── harness-evolve/         ← 持续迭代优化
│   │       ├── SKILL.md
│   │       └── scripts/            ← 垃圾回收和精简脚本
│   ├── commands/                   ← Slash Commands
│   │   ├── harness-init.md         ← /harness-init
│   │   ├── harness-audit.md        ← /harness-audit
│   │   ├── review-pr.md            ← /review-pr
│   │   ├── context-dump.md         ← /context-dump
│   │   ├── doc-sync.md             ← /doc-sync
│   │   ├── arch-scan.md            ← /arch-scan
│   │   └── trim-claudemd.md        ← /trim-claudemd
│   ├── hooks/                      ← Hook 模板脚本
│   │   ├── stop-typecheck.sh
│   │   ├── pre-protect-env.sh
│   │   ├── post-format.sh
│   │   ├── stop-commit-progress.sh
│   │   └── post-observe.sh
│   └── agents/                     ← Subagent 定义
│       └── security-reviewer.md
├── docs/
│   ├── architecture.md             ← 本文件
│   ├── decisions/                  ← ADR 架构决策记录
│   │   ├── README.md
│   │   ├── 0001-skill-based-architecture.md
│   │   ├── 0002-multi-language-templates.md
│   │   └── 0003-dogfooding-harness.md
│   ├── design/
│   │   └── skill-interaction-flow.md
│   └── templates/                  ← 多语言项目模板
│       ├── typescript/
│       ├── python/
│       ├── go/
│       └── generic/                ← 语言无关的通用模板
├── references/                     ← 参考文档（按需加载）
│   ├── harness-engineering-handbook.md
│   ├── hook-patterns.md
│   └── anti-patterns.md
└── scripts/                        ← 辅助脚本
    ├── self-test.sh
    ├── health-score.py
    └── generate-harness.sh
```

## 三个核心 Skill 的职责分工

| Skill | 触发场景 | 输入 | 输出 |
|-------|---------|------|------|
| **harness-init** | 新项目从零建立 Harness | 技术栈信息、项目描述 | CLAUDE.md + Hooks + docs/ + settings.json |
| **harness-audit** | 存量项目评估和优化 | 现有代码库 | 健康度报告 + 优化建议 + 修复 PR |
| **harness-evolve** | 持续迭代改进 | 失败记录、模型更新 | Harness 精简/增强建议 + 自动维护 |

## 层级依赖规则

允许的依赖方向（只能向右引用）：

```
references → templates → skills → commands
```

禁止规则：
- commands 不能直接引用 references（必须通过 skills 中转）
- templates 不能引用 skills（模板是被 skills 消费的静态资源）
- hooks 是独立的确定性脚本，不依赖 skills 或 commands
