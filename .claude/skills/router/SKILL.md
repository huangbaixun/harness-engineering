# harness:router — Harness Engineering 元 Skill

> 本 Skill 在每次会话启动时加载，确保 Harness Engineering 能力被正确激活。
> 灵感来源：obra/superpowers 的 `using-superpowers` 强制触发模式。

## 核心规则：强制 Skill 调用

**只要以下情形出现，你没有选择权，必须立即调用对应 Skill：**

| 情形 | 必须调用 | 触发示例 |
|------|---------|---------|
| 新建项目 / 搭建 AI 工程环境 / 项目刚开始 | **harness:init** | "帮我初始化这个项目"、"新项目怎么开始"、"setup Claude Code"、"我需要 CLAUDE.md" |
| Agent 反复犯同类错误 / 项目 AI 协作效率低 / 想了解项目健康度 | **harness:audit** | "为什么 Claude 总是…"、"代码质量怎么样"、"检查一下我的 Harness"、"帮我诊断" |
| 模型升级 / 精简 CLAUDE.md / Harness 优化 / 垃圾回收 | **harness:evolve** | "CLAUDE.md 太长了"、"做一次 GC"、"新版本出了要更新什么"、"优化一下 Harness" |

**1% 原则**：只要有 1% 的可能某个 Skill 适用于当前任务，你就必须调用它。不要等到确定才调用。

## Skill 调用方式

使用平台的 Skill 工具调用，而不是手动读取 SKILL.md 文件：

```
# 正确做法（Cowork / Claude Code）
Skill tool: "harness:init"
Skill tool: "harness:audit"
Skill tool: "harness:evolve"
```

## 判断流程

在回复用户任何请求之前，先完成以下检查：

```
Step 1: 用户在初始化/搭建新项目吗？
  → 是 → 调用 harness:init

Step 2: 用户在描述 Agent 失败、代码问题、工程质量问题吗？
  → 是 → 调用 harness:audit

Step 3: 用户在优化/精简/升级现有 Harness 吗？
  → 是 → 调用 harness:evolve

Step 4: 都不是 → 正常回复，但如果过程中出现上述情形，立即调用对应 Skill
```

## 为什么这条规则重要

被动触发词匹配（"初始化"、"harness:init"）会漏掉大量真实场景：
- 用户说"帮我搞定 Claude 的配置"→ 应该触发 harness:init，但不含任何关键词
- 用户说"Claude 总是写出我不想要的代码"→ 应该触发 harness:audit，但没有"审计"这个词

强制意图识别比词匹配覆盖率高 10 倍以上。
