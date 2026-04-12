---
name: harness:audit
description: >
  存量项目 Harness 健康度检查与优化。当用户提到「检查 Harness」「优化 CLAUDE.md」
  「优化 AGENTS.md」「优化 CODEBUDDY.md」「Agent 老是犯错」「Harness 健康度」
  「审计 Harness」「评估 AI 编码环境」「harness audit」「检查 Agent 配置」
  「为什么 Agent 不听话」「改善 Agent 效果」「现有项目加 Harness」「存量优化」时激活。
  当用户抱怨 Agent 行为不符合预期、反复犯同样的错误、或项目已有一段时间但
  缺乏系统化的 Harness 体系时，也应使用此 Skill 来诊断和改进。
---

# Harness 健康度审计 Skill

> 本 Skill 对存量项目的 Harness 体系进行系统性诊断，识别薄弱环节并提供具体优化建议。
> 核心理念：**围绕你实际观察到的失败模式构建约束，而不是假设的失败模式。**

## 审计流程

### Step 1：扫描现有 Harness 状态

用 Explore subagent 或直接扫描以下文件和目录：

```bash
# 工具检测：自动识别 Claude Code / CodeBuddy / 其他工具
TOOL_DIR=$([ -d ".codebuddy" ] && echo ".codebuddy" || echo ".claude")
MEMORY_FILE=$([ -f "AGENTS.md" ] && echo "AGENTS.md" \
           || ([ -f "CODEBUDDY.md" ] && echo "CODEBUDDY.md") \
           || echo "CLAUDE.md")
echo "检测到工具配置目录：$TOOL_DIR，记忆文件：$MEMORY_FILE"

# 检查六层 Harness 的每一层
echo "=== 1. 记忆层 ===" && cat "$MEMORY_FILE" 2>/dev/null | wc -l
echo "=== 2. 规则层 ===" && cat "$TOOL_DIR/settings.json" 2>/dev/null
echo "=== 3. 技能层 ===" && ls "$TOOL_DIR/skills/" "$TOOL_DIR/commands/" 2>/dev/null
echo "=== 4. 智能体层 ===" && ls "$TOOL_DIR/agents/" 2>/dev/null
echo "=== 5. 钩子层 ===" && grep -r "hooks" "$TOOL_DIR/settings.json" 2>/dev/null
echo "=== 6. 工具层 ===" && grep -r "mcpServers" "$TOOL_DIR/settings.json" 2>/dev/null
echo "=== 文档体系 ===" && ls docs/ 2>/dev/null
echo "=== ADR ===" && ls docs/decisions/ 2>/dev/null
```

### Step 2：七维度健康度评分

基于 OpenAI Scorecard 框架，逐一评估并打分（0-3 分）：

| 维度 | 评估问题 | 0 分 | 1 分 | 2 分 | 3 分 |
|------|---------|------|------|------|------|
| **Bootstrap** | Agent 能否无人工干预完成首次配置自测？ | 无自动化 | 有部分脚本 | 可自测但需手动步骤 | 完全自动化 |
| **Task Entry** | 入口任务是否清晰可发现？ | 无导航 | CLAUDE.md 有列表 | 有 Commands | 有 Skills + Commands |
| **Validation** | CI/测试能否自动验证 Agent 输出？ | 无测试 | 手动测试 | CI 有测试 | CI + Hooks 自动验证 |
| **Lint Gates** | 格式检查是否在 pre-commit 自动运行？ | 无检查 | 有但手动 | pre-commit | PostToolUse Hook |
| **Repo Map** | 仓库是否有清晰的领域架构图？ | 无文档 | README | architecture.md | 含依赖规则的 arch.md |
| **Structured Docs** | 设计文档是否结构化、有链接？ | 无 docs/ | 有但散乱 | 有结构 | 结构化 + 交叉链接 |
| **Decision Records** | 架构决策是否有 ADR 记录并维护？ | 无 ADR | 有但过时 | 有且更新 | 有且含废弃记录 |

**总分解读**：
- 0-7 分：🔴 基础缺失，建议用 harness:init 从零建立
- 8-14 分：🟡 有基础但薄弱，重点补强最低分维度
- 15-21 分：🟢 良好，进入精细化优化阶段

### Step 3：识别失败模式

检查以下常见失败模式并生成诊断报告：

**A. 记忆文件（AGENTS.md / CLAUDE.md / CODEBUDDY.md）问题诊断**

```
检查项：
□ 行数是否超过 60 行？→ 需要精简
□ 是否包含 Agent 已自然遵守的规则？→ 删除冗余规则
□ 是否有模糊不可验证的规则（如「写好代码」）？→ 改为具体可验证
□ 是否有应该用 Hook 强制但却放在记忆文件的规则？→ 迁移到 Hook
□ 是否有过时的规则？→ 删除或标记
□ 多文件是否内容一致？（AGENTS.md / CLAUDE.md / CODEBUDDY.md 应同步）
```

**B. Hook 覆盖度诊断**

```
检查项：
□ 是否有 Stop Hook 做质量门禁？→ 最高优先级
□ 是否有 PreToolUse Hook 保护敏感文件？→ 安全必需
□ 是否有 PostToolUse Hook 做自动格式化？→ 一致性保障
□ Hook 成功时是否静默？→ 输出会污染上下文
□ Hook 失败时退出码是否正确（exit 2）？→ 影响反馈链路
```

**C. 上下文健康度诊断**

```
检查项：
□ 基线成本（新会话）是否 < 20k Token？
□ CLAUDE.md 大小是否 < 2000 Token？
□ MCP 工具总 Token 是否 < 20k？
□ 是否有过多 MCP Server 连接？→ 按需接入
□ 测试输出是否在成功时静默？
```

**D. 架构约束诊断**

```
检查项：
□ 是否有明确的依赖方向规则？
□ 依赖规则是否有自动验证（Linter / 结构测试）？
□ 是否有 architecture.md 记录模块边界？
□ 架构违规是否在 CI 中被拦截？
```

**E. 文档体系诊断**

```
检查项：
□ architecture.md 是否存在且与代码一致？→ 检查目录结构
□ ADR 索引是否完整？→ 检查 decisions/README.md
□ 是否有「已废弃」状态的 ADR？→ 这很重要
□ 进度追踪是否使用 JSON 格式？
```

### Step 4：生成优化方案

按「频率 × 严重程度」排序问题，输出结构化优化方案：

```markdown
## Harness 健康度报告

### 当前评分：XX / 21

### 🔴 立即行动（本周）
1. [问题描述] → [具体修复步骤]
2. ...

### 🟡 本月完成
1. [问题描述] → [具体修复步骤]
2. ...

### 🟢 持续改进
1. [问题描述] → [具体修复步骤]
2. ...
```

### Step 5：执行优化

如果用户同意，直接执行优化操作：

1. **精简 CLAUDE.md**：删除冗余规则，保留核心约束
2. **补充 Hooks**：根据诊断结果生成缺失的 Hook 脚本
3. **建立文档体系**：创建 architecture.md、ADR 目录
4. **配置 settings.json**：注册 Hook、设置权限
5. **提交优化 PR**：每个修复单独 commit，便于回滚

### Step 6：建立持续改进机制

为项目设置「每周 Harness 维护仪式」：

1. **失败分析（10 分钟）** — 回顾本周 Agent 失败案例，每个失败转化为一条 Harness 改进
2. **文档新鲜度检查（5 分钟）** — 确认 CLAUDE.md 和 docs/ 中没有陈旧规则
3. **成本基线对比（5 分钟）** — 对比本周 vs 上周 Token 使用趋势
4. **Harness 精简（按需）** — 随模型更新，评估并删除不再必要的脚手架

建议设置 `/harness:sync-docs` 和 `/harness:scan-arch` 定时任务自动化这些检查。

## 验证体系框架

审计时特别关注「前馈 + 反馈」两类控制是否完备：

**Guides（前馈控制）**：在 Agent 行动之前进行引导
- CLAUDE.md 架构约定 → Computational Guide
- Skills 领域知识注入 → Inferential Guide

**Sensors（反馈控制）**：在 Agent 行动之后验证
- Stop Hook 类型检查 → Computational Sensor
- 安全审查 Sub-agent → Inferential Sensor

原则：先用 Computational 方案覆盖 80% 常见问题，再用 Inferential 处理需要理解语义的剩余 20%。
