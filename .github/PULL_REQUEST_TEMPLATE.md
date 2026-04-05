## 变更类型

<!-- 在对应项前打 x -->

- [ ] `feat(skill)` — 新增 Skill
- [ ] `feat(template)` — 新增语言模板
- [ ] `feat(agent)` — 新增或改进 Agent
- [ ] `fix(hook)` — 修复 Hook 脚本
- [ ] `fix(agent)` — 修复 Agent 行为
- [ ] `docs` — 文档改进
- [ ] `eval` — 新增或改进 eval 用例

## 变更内容

<!-- 做了什么，为什么 -->

## 触发条件（Skill 类 PR 必填）

<!-- 哪些用户输入会触发这个 Skill？列举 3 个例子，包括不含关键词的意图表达 -->

## Eval 验证

<!-- 对应的 eval 用例 ID，以及预期行为描述 -->

- Eval ID：
- 预期行为：

## 自测记录

<!-- 用 Claude Code 实际测试过的场景，截图或输出片段 -->

## Checklist

- [ ] SKILL.md / Agent 文件有明确的触发条件说明
- [ ] 新增了对应的 eval 用例（functional + 至少 1 个 pressure）
- [ ] Hook 脚本成功时静默，失败时输出错误信息
- [ ] 更新了 CHANGELOG.md
