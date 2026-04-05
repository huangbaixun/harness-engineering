# Contributing to Harness Engineering Plugin

感谢你对本项目的兴趣！本文档说明如何参与贡献。

## 贡献类型

本项目接受三类贡献，每类有不同的门槛和流程：

### 1. 新增或改进 Skill

Skills 是最欢迎的贡献形式——不需要理解整个插件架构，只需按照 Skill TDD 流程写好 `SKILL.md` 并通过 eval 验证。

**流程（Skill TDD）：**

**RED** — 先写 eval，定义 Skill 应该做什么和不应该做什么：

```jsonc
// evals/evals.json 中添加：
{
  "id": "your-skill-name-basic",
  "type": "functional",
  "skill": "your-skill-name",
  "prompt": "触发这个 Skill 的典型用户输入",
  "expected_behavior": "Agent 应该执行的操作",
  "failure_mode": "如果没有这个 Skill，Agent 会犯什么错误"
}
```

同时为每个关键约束各写一个压力 eval：

```jsonc
{
  "id": "your-skill-name-pressure-1",
  "type": "pressure",
  "skill": "your-skill-name",
  "rule_under_test": "你的 Skill 中的某条关键约束",
  "prompt": "用户施压让 Agent 跳过这条约束的表达",
  "expected_behavior": "Agent 应该坚守约束",
  "failure_mode": "Agent 如何会找到理由绕过约束",
  "pressure_level": "medium"
}
```

**GREEN** — 写 `skills/your-skill-name/SKILL.md`，让 Agent 通过上述 eval。

**REFACTOR** — 在 PR 描述中附上 eval 用例和预期输出，评审者会用 Agent 实际跑一遍。

**Skill 文件结构：**

```
skills/
└── your-skill-name/
    └── SKILL.md          # 必须，说明触发条件、步骤、约束
```

---

### 2. 新增语言模板

语言模板位于 `docs/templates/<language>/`，帮助工程师快速初始化某语言栈的 `CLAUDE.md`。

**文件结构：**

```
docs/templates/<language>/
├── CLAUDE.md.template    # 必须，包含该语言的测试框架、Lint 工具、架构约定
└── README.md             # 可选，说明模板适用场景和主要约定
```

**模板内容要求：**
- 指定测试框架和常用断言库（如 JUnit 5 + AssertJ）
- 指定 Lint / 格式化工具（如 Checkstyle + SpotBugs）
- 列出项目架构层次（如 entity → repository → service → controller）
- 列出语言特有的禁止项（如 raw types、silent catch Exception）

参考已有模板：`docs/templates/java/CLAUDE.md.template`

---

### 3. 改进 Hook 脚本

Hook 脚本位于 `scripts/`，对应 `hooks/hooks.json` 中注册的事件。

**约定：**
- 脚本成功时**静默**（无输出），只在失败时输出错误信息
- 使用 `${CLAUDE_PLUGIN_ROOT}` 引用插件内路径，不使用绝对路径
- 每个脚本做一件事，不做复合职责
- 改动已有脚本需在 PR 中说明为什么不创建新脚本

---

## PR 规范

**标题格式：** `type(scope): description`

- `feat(skill)`: 新增 Skill
- `feat(template)`: 新增语言模板
- `fix(hook)`: 修复 Hook 脚本
- `fix(agent)`: 修复 Agent 行为
- `docs`: 文档改进
- `eval`: 新增或改进 eval 用例

**PR 描述必须包含：**

```markdown
## 变更内容
<!-- 做了什么 -->

## 触发条件（仅 Skill 类 PR）
<!-- 哪些用户输入会触发这个 Skill -->

## Eval 验证
<!-- 附上你写的 eval 用例 ID 和预期行为描述 -->

## 自测记录
<!-- 你用 Claude Code 实际测试过的场景截图或输出片段 -->
```

---

## 本地验证

```bash
# 解压最新 .skill 包到测试目录
unzip harness-engineering.skill -d /tmp/harness-test

# 加载插件进行本地验证
claude --plugin-dir /tmp/harness-test
```

验证 plugin 加载成功：启动 Claude Code 后，在对话中输入「帮我初始化这个项目的 Harness」，应该自动触发 `harness-init` Skill。

---

## 行为准则

本项目遵循 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

核心原则：我们欢迎不同背景、经验水平的贡献者。如果你的 PR 被拒绝，maintainer 会解释原因并尽量给出改进建议。
