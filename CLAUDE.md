# Harness Engineering Plugin — CLAUDE.md

## 项目概述
Harness Engineering 能力建设 plugin：为新项目初始化和存量项目优化提供标准化 AI Agent Harness 工程体系。

## 技术栈
- Shell 脚本（Hook 模板和自动化脚本）
- Markdown + JSON（Skills、Commands、配置模板）
- Python 3.10+（辅助脚本：健康度评分、架构扫描）
- 多语言模板：TypeScript、Python、Go、通用

## 关键命令
- 验证 Skill 结构：`find .claude/skills -name "SKILL.md" | head -20`
- 检查 JSON 合法性：`python3 -m json.tool docs/templates/*/features.json`
- 运行自测：`bash scripts/self-test.sh`

## 架构约定
- 依赖方向：references → templates → skills → commands（禁止逆向）
- 所有 Skill 的 SKILL.md 必须包含 YAML frontmatter（name, description）
- 所有 Hook 脚本必须遵循「成功静默、失败可见」原则
- 模板文件中的占位符统一用 `{{PLACEHOLDER}}` 格式

## Skill 开发强制流程
任何 Skill 的新增或修改必须经过 skill-creator 工作流，不允许跳过：
1. 起草 SKILL.md → 2. 在对应 `evals/evals.json` 写测试用例 → 3. 运行 eval（with-skill vs baseline）→ 4. 生成 eval-viewer 供人审阅 → 5. 根据反馈迭代
- eval 文件位置：`skills/<name>/evals/evals.json`，格式兼容 skill-creator
- 禁止在未经 eval 验证的情况下直接修改 SKILL.md 并提交
- 详见：docs/decisions/0004-skill-creator-methodology.md

## 禁止规则
- 永远不要在模板中硬编码具体项目名或团队信息
- 永远不要生成超过 60 行的 CLAUDE.md 模板
- 永远不要让 Hook 模板在成功时输出日志
- 永远不要在单个 Skill 文件中超过 500 行

## 更多上下文
- 架构图：docs/architecture.md
- 设计决策：docs/decisions/
- 模板目录：docs/templates/
- 方法论完整手册：references/HarnessEngineering.md（本地文件，不纳入版本控制，需自行放置）
- 概念速查：references/harness-engineering-handbook.md
