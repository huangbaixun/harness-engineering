---
description: 对当前项目的 Harness 体系进行健康度审计，生成评分报告和优化建议
---

执行 Harness 健康度审计：

1. 扫描当前项目的六层 Harness 状态（记忆层、规则层、技能层、智能体层、钩子层、工具层）
2. 按七维度评分：Bootstrap / Task Entry / Validation / Lint Gates / Repo Map / Structured Docs / Decision Records
3. 诊断常见失败模式（CLAUDE.md 膨胀、Hook 覆盖不足、上下文污染、架构漂移、文档陈旧）
4. 生成结构化优化方案（按优先级：立即行动 / 本月完成 / 持续改进）
5. 如果用户同意，直接执行优化操作并提交 PR
