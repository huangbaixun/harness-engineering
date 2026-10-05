# ADR 0013：共享 Harness 核心与 Claude / Codex 平台适配

- 状态：Proposed
- 日期：2026-10-05
- Supersedes：ADR-0007 的 Claude Code only 限制（执行验收后生效）

## 背景

用户要求使用自研 harness 开发 AIDC，而当前运行工具为 Codex。现有框架以 CLAUDE.md、Claude hook 协议和 .claude 路径绑定平台。仅改名不能保证技能发现、验证或保护行为成立。

## 决定

共享 features.json、skills、ADR、验证和归档资源，平台入口负责技能加载、初始化和事件协议。Claude 入口保留；Codex 独立注册hooks，默认不启用自动提交和Issue同步。新增项目支持 AGENTS.md 及项目级 .agents/skills，不覆盖既有规则。不将提示性规则称为确定性安全拦截。

技能上游保持 ADR-0009 来源约束；平台差异通过 sidecar/reference 表达。Codex hooks 遵守原生信任流程，未验证能力明确降级至显式检查。

## 代价与验证

双端适配增加测试矩阵，换取统一工程流程。按 docs/plans/2026-10-05-codex-adaptation-plan.md 完成离线初始化、真实发现、协议及回归测试；未验证的CLI/App能力不宣称支持。现有用户行为保持兼容，启用新适配按显式入口选择。
