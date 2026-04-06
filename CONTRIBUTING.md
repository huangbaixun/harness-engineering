# Contributing to Harness Engineering Plugin

感谢你对本项目的兴趣！本文档说明如何参与贡献。

## 贡献类型

本项目接受三类贡献，每类有不同的门槛和流程：

### 1. 新增或改进 Skill

Skills 是最欢迎的贡献形式。**所有 Skill 的新增和修改必须经过 skill-creator 工作流**——这是 Anthropic 官方元技能，提供起草 → 测试 → 评估 → 迭代的结构化流程，确保每个 Skill 有客观的质量基线。

**标准流程（skill-creator 工作流）：**

**Step 1 — 起草 SKILL.md**

在 `skills/your-skill-name/SKILL.md` 中写 Skill 草稿，包含 YAML frontmatter：

```markdown
---
name: your-skill-name
description: >
  触发条件描述。当用户提到...时激活。
  即使用户只是提到...，也应使用此 Skill。
---
```

**Step 2 — 写 eval 测试用例**

在 `skills/your-skill-name/evals/evals.json` 中写测试，格式兼容 skill-creator：

```json
{
  "skill_name": "your-skill-name",
  "evals": [
    {
      "id": 1,
      "eval_name": "basic-functional",
      "type": "functional",
      "prompt": "触发这个 Skill 的典型用户输入",
      "expected_output": "Agent 应该执行的操作描述",
      "files": [],
      "assertions": [
        { "name": "检查点描述", "check": "客观可验证的判断标准" }
      ]
    },
    {
      "id": 2,
      "eval_name": "constraint-pressure",
      "type": "pressure",
      "rule_under_test": "Skill 中的某条关键约束",
      "prompt": "用户施压让 Agent 跳过约束的表达",
      "expected_output": "Agent 应坚守约束的行为描述",
      "files": [],
      "assertions": [
        { "name": "约束被坚守", "check": "输出中不包含妥协表述" }
      ]
    }
  ]
}
```

**Step 3 — 运行 skill-creator eval**

使用 skill-creator 启动 eval 运行器，同时跑 with-skill 和 baseline（无 Skill）两组，生成对比结果：

```
在 Claude Code 中触发 skill-creator，告知：
「请对 skills/your-skill-name 运行 eval，
  eval 文件在 skills/your-skill-name/evals/evals.json」
```

skill-creator 会自动生成 eval-viewer HTML，供你审阅 with-skill vs baseline 的输出差异和 assertion 通过率。

**Step 4 — 根据结果迭代**

在 eval-viewer 中留下反馈，skill-creator 据此修改 SKILL.md，进入下一轮迭代，直到所有 functional eval 通过、pressure eval 约束不被破坏。

**Step 5 — 描述优化（可选但推荐）**

使用 skill-creator 的描述优化功能（`run_loop.py`）对 description 字段做触发准确率优化。

**Skill 目录结构：**

```
skills/
└── your-skill-name/
    ├── SKILL.md                    # 必须
    └── evals/
        └── evals.json              # 必须，skill-creator 兼容格式
```

**PR 要求**：附上 skill-creator 生成的 benchmark 截图或 `benchmark.json` 摘要，说明 with-skill vs baseline 的 assertion 通过率对比。

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
