# ADR 0007：Claude Code Only — 移除工具无关兼容层

- **状态**：Accepted（Supersedes [ADR 0005](0005-tool-agnostic-agents-md.md)）
- **日期**：2026-05-23
- **决策者**：huangbaixun

## 背景

[ADR 0005](0005-tool-agnostic-agents-md.md)（2026-04-08）在 Tencent CodeBuddy 是相关迁移目标时，选择了工具无关架构：以 `AGENTS.md` 作为跨工具通用记忆文件，`CLAUDE.md` 和 `CODEBUDDY.md` 退化为 2 行 wrapper，模板和 Skill 使用 `$TOOL_DIR` / `$TOOL_NAME` 间接层避免硬编码路径。

v1.10.1 release 已删除 `.codebuddy-plugin/` 目录与脚本侧的 CodeBuddy 支持。此时间接层失去对应收益，徒增三类成本：

1. **认知负担**：用户需理解 AGENTS.md / CLAUDE.md 双文件结构的同步关系
2. **维护成本**：Skill 内容编写需绕过路径硬编码，导致表达迂回
3. **文档复杂度**：README、架构图、培训材料都需要解释"为什么有两个记忆文件"

## 决策

`CLAUDE.md` 重新成为唯一 canonical memory file。删除 `AGENTS.md`、`CODEBUDDY.md`、`docs/templates/generic/AGENTS.md.template`、`$TOOL_DIR` / `$TOOL_NAME` 间接层。Plugin 定位明确为 **Claude Code marketplace 专用 plugin**。

## 后果

### 收益
- 用户认知负担降低：一个文件、一种路径
- Skill / Hook / 模板与 Claude Code 现实 1:1 对应，无抽象绕道
- 文档收敛，README 更易理解

### 已知成本
- 放弃 `AGENTS.md` 这个新兴行业标准（OpenAI Codex / Cursor / Aider 都读它）—— 未来若重新支持非 Claude 工具需新 ADR
- 已迁移到 `AGENTS.md` 的用户项目需自行回迁（plugin 不强制覆盖既有文件）

## 迁移

- 既有用户项目的 `AGENTS.md` 不被 plugin 触碰
- 新 `harness:init` 只生成 `CLAUDE.md`
- v1.11.0 CHANGELOG 标注 Breaking Change

## 相关

- Supersedes：[ADR 0005](0005-tool-agnostic-agents-md.md)
- 触发：v1.10.1 release（CodeBuddy 移除）
- 实现 spec：[2026-05-23-remove-codebuddy-design.md](../superpowers/specs/2026-05-23-remove-codebuddy-design.md)
