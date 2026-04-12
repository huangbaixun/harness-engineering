---
description: 为当前项目初始化完整的 AI Agent Harness 工程体系
---

执行 Harness 初始化流程：

1. 检测当前项目技术栈（扫描 package.json / requirements.txt / go.mod / Cargo.toml 等）
2. 询问用户确认技术栈信息和项目类型
3. 使用 harness:init Skill 的流程，按六层模型生成完整 Harness 结构：
   - CLAUDE.md（≤ 60 行）
   - .claude/settings.json（Hook 注册 + 权限配置）
   - .claude/hooks/（Stop + PreToolUse + PostToolUse）
   - docs/architecture.md（100-150 行架构图）
   - docs/decisions/README.md（ADR 索引）
   - docs/claude-progress.json（进度追踪骨架）
4. 验证生成的文件完整性
5. 输出初始化摘要和「第 1-2 周观察事项」建议
