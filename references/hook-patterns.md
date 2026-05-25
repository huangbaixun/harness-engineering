# Hook 设计模式参考

## Hook 事件类型

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| PreToolUse | 工具调用前，可拦截或修改参数 | 拦截危险命令、限制文件访问范围 |
| PostToolUse | 工具完成后立即触发 | 自动格式化、遥测记录 |
| Stop | 主 Agent 完成响应后 | 类型检查、测试覆盖率报告 |
| UserPromptSubmit | 用户提交 Prompt 前 | 注入额外上下文、防注入检测 |
| SessionStart | 会话开始时 | 环境检查、状态加载、问候消息、**元技能正文注入**（见下） |
| SessionEnd | 会话结束时 | 保存进度、发送通知、清理临时文件 |
| SubagentStop | Subagent 完成时 | 触发进度同步、记录子任务成本 |
| FileChanged | 文件变化时 | 触发增量测试 |

## 退出码约定

```
exit 0   → 成功，继续（完全静默）
exit 2   → 失败，错误信息反馈给 Agent，Agent 继续修复
exit 其他 → 失败，不反馈给 Agent（非阻塞，静默失败）
```

**关键原则**：成功永远静默。4000 行通过日志会使 Agent 失去任务焦点，开始讨论测试文件而非完成任务。

## 4 种处理器类型

| 类型 | 适合场景 | 特点 |
|------|---------|------|
| Command（Shell） | 确定性操作：格式化、类型检查、权限验证 | 执行快、结果确定、易调试、成本最低 |
| Prompt（LLM） | 语义判断：代码质量评估、微妙违规检测 | 理解语义，但成本高、速度慢 |
| Agent（派生子 Agent） | 复杂验证：多步骤、需读取多个文件 | 完整工具访问，可自主探索，结果可信 |
| HTTP（外部服务） | 系统集成：触发 CI、通知 Slack、更新 Jira | 与企业系统对接 |

**选择决策树**：
```
需要「理解语义」吗？
  → 是：用 Prompt 或 Agent 类型
  → 否：用 Command 类型（更快更便宜）

需要读取多个文件或执行多步骤吗？
  → 是：用 Agent 类型
  → 否：用 Prompt 类型

需要触发外部系统吗？
  → 是：用 HTTP 类型
```

## 按失败类型选择 Hook

| 团队常见失败 | 对应 Hook 事件 | 处理器类型 | 优先级 |
|-------------|-------------|----------|--------|
| 类型错误被提交 | Stop | Command（tsc / mypy / go vet） | ⭐⭐⭐ 立即 |
| 修改了 .env 文件 | PreToolUse | Command（文件路径检查） | ⭐⭐⭐ 立即 |
| 代码格式不统一 | PostToolUse | Command（lint:fix） | ⭐⭐⭐ 立即 |
| 架构违规未被发现 | PostToolUse | Agent（架构约束检查） | ⭐⭐ 本周 |
| Agent 过早收工 | Stop | Command（检查 progress.json） | ⭐⭐ 本周 |
| Sub-agent 未记录进度 | SubagentStop | HTTP（触发进度同步） | ⭐ 本月 |
| 会话结束未 commit 进度 | SessionEnd | Command（git commit progress） | ⭐ 本月 |

## settings.json 配置示例

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [
        { "type": "command", "command": ".claude/hooks/stop-typecheck.sh" }
      ]
    }],
    "PreToolUse": [{
      "matcher": "Bash|Edit|Write",
      "hooks": [
        { "type": "command", "command": ".claude/hooks/pre-protect-env.sh" }
      ]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [
        { "type": "command", "command": ".claude/hooks/post-format.sh" }
      ]
    }]
  }
}
```

## SessionStart 元技能注入模式（ADR-0010）

**问题**: 仅"在 skills/ 目录摆一个元技能 SKILL.md"无法让 LLM 真的在每次对话开始时遵循它——CLAUDE.md 是被动文档,模型是否读取、何时读取均不可控。

**机制**: Claude Code 把 SessionStart hook 的 stdout 作为 *additional session context* 注入到模型的首轮上下文中。利用这个通道,把元技能正文(策略/红旗信号/技能目录)在对话开始时无条件推送给模型,套上 `<EXTREMELY_IMPORTANT>` 哨兵强化优先级。

**最小实现**:
```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
META_SKILL="$PLUGIN_ROOT/skills/using-harness/SKILL.md"
if [ -f "$META_SKILL" ]; then
  echo "<EXTREMELY_IMPORTANT>"
  awk 'BEGIN{n=0} /^---$/{n++; next} n>=2{print}' "$META_SKILL"  # 剥离 YAML frontmatter
  echo "</EXTREMELY_IMPORTANT>"
fi
```

**关键约束**:
- **单一来源**: 注入内容必须从 SKILL.md 文件读取,**不可内嵌到 hook 脚本**,否则会与 `/harness:using-harness` 命令读到的版本漂移(ADR-0009)。
- **路径耦合**: hook 脚本硬编码 `skills/using-harness/SKILL.md` 路径。任何重命名/迁移必须在同一 commit 内同步更新 hook,且 `sync-superpowers.sh` 等工具不得移动该路径。
- **正文克制**: 注入每次都消耗 token。元技能 SKILL.md 必须保持精简(< 100 行,只放协议/目录),严禁堆积说明文档。
- **优先级声明**: 元技能内部必须显式声明 "用户显式指令 > 元技能 > 默认系统提示",否则会出现机械执行 1% rule、压过用户意图的反模式。

**何时不该用**:
- 普通业务项目无需自建元技能注入——这是给方法论框架/能力插件用的。
- 单技能场景:写一个具体技能比建一个元技能更划算。

## 最小可用 Hook 集（Day 1）

优先级最高的三个 Hook，ROI 最高：

1. **Stop Hook — 类型检查**：确保每次 Agent 完成时代码类型正确
2. **PostToolUse Hook — 自动格式化**：确保代码风格一致，成功完全静默
3. **PreToolUse Hook — 保护敏感文件**：防止访问 .env、secret 等文件

这三个 Hook 覆盖了 80% 的常见质量问题，是建立 Harness 最快的起点。
