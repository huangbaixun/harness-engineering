# ADR 0005：工具无关架构 — AGENTS.md 作为通用记忆文件

- **状态**：已接受
- **日期**：2026-04-08
- **作者**：Harness Engineering

---

## 背景

Harness Engineering plugin 最初专为 Claude Code 设计，记忆文件为 `CLAUDE.md`，配置目录固定为 `.claude/`。随着腾讯 CodeBuddy 等兼容工具的兴起，用户需要在多种 AI 编程工具之间切换或并用，但原有设计导致 Skills 内容与工具强耦合，移植成本高。

参考 `learn-harness-engineering` 项目的供应商无关合约设计，识别到以下核心问题：

1. `CLAUDE.md` 文件名与 Claude Code 品牌强绑定，CodeBuddy 等工具不会优先读取
2. `.claude/` 路径在 Skills/Commands 内容中被大量硬编码，每次适配新工具需要大规模替换
3. 没有统一的「跨工具真相来源」，双工具用户需要维护两份内容相同的记忆文件

---

## 考虑过的选项

### 方案 A：每种工具维护独立 plugin 分支
- 优点：各工具深度定制，体验最优
- 缺点：维护成本翻倍，规则易分叉，用户使用两种工具时需切换不同 plugin

### 方案 B：共享记忆文件 + 工具特定配置目录（当前选择）
- 优点：单一真相来源（`AGENTS.md`），运行时动态检测工具类型，Skills 内容零修改即可跨工具复用
- 缺点：需要 init.sh 的工具检测逻辑，部分工具可能不读取 `AGENTS.md`（但实测 Claude Code、CodeBuddy 均已支持）

### 方案 C：强制要求用户手动配置工具路径
- 优点：无自动检测复杂度
- 缺点：用户体验差，违背「开箱即用」原则

---

## 决策

采用**方案 B — 工具无关架构**，以 `AGENTS.md` 作为跨工具通用记忆文件。

具体落地：

| 文件 | 角色 | 说明 |
|------|------|------|
| `AGENTS.md` | 唯一真相来源 | 所有项目规则、禁止项、测试命令放这里 |
| `CLAUDE.md` | 2 行 wrapper | 将 Claude Code 用户引导至 `AGENTS.md` |
| `CODEBUDDY.md` | 2 行 wrapper | 将 CodeBuddy 用户引导至 `AGENTS.md` |
| `init.sh` | 工具检测入口 | 检测 `.claude/` vs `.codebuddy/`，导出 `$TOOL_DIR` |
| Skills/Commands | 使用 `$TOOL_DIR` | 不再硬编码 `.claude/` 或 `.codebuddy/` |

---

## 后果

### ✅ 正向影响
- 用户只需维护一份 `AGENTS.md`，工具切换零成本
- Skill 内容通过 `$TOOL_DIR` 变量跨工具复用，无需 fork
- `.codebuddy-plugin/plugin.json` 使 CodeBuddy 用户可直接安装同一个 plugin

### ❌ 约束（Agent 必须遵守）
- 永远不要在 Skill/Command 内容中硬编码 `.claude/` 或 `.codebuddy/` 路径，必须使用 `$TOOL_DIR`
- 生成初始化文件时，工具路径判断必须通过 `init.sh` 的检测逻辑，不得假设固定路径
- `CLAUDE.md` 和 `CODEBUDDY.md` 保持 2 行 wrapper 格式，不得直接写入规则（规则统一放 `AGENTS.md`）

### ⚠️ 已知局限
- `$TOOL_DIR` 变量在 Claude Code 会话中由 init.sh 导出，但 Agent 在生成 Hook 脚本时需确保脚本自身也包含工具检测逻辑（不依赖外部环境变量）

---

## 参考
- [learn-harness-engineering: vendor-agnostic contracts](https://github.com/walkinglabs/learn-harness-engineering)
- [CodeBuddy 兼容性分析](../references/team-parallel-development.md)
- ADR 0001：Skill-based Architecture
