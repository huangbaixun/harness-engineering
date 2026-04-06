# ADR 0004: 采用 skill-creator 作为 Skill 开发的唯一方法论

**状态**：已采纳
**日期**：2026-04-06
**决策者**：Harness Engineering 团队

---

## 背景

Skill 是本 plugin 最核心的交付物，但 Skill 质量难以客观衡量：一个 Skill 是否真的让 Agent 更好地完成任务？关键约束在用户施压时是否被坚守？仅靠人眼审阅 SKILL.md 无法回答这些问题。

早期版本（v1.0–v1.2）采用「手写 Skill → 人工判断效果」的方式，存在以下问题：

1. **没有基线对比**：不知道 with-skill 比 without-skill 好多少
2. **Eval 格式不统一**：`evals/evals.json` 是主观文字描述，不可程序化评分
3. **迭代缺乏闭环**：Skill 修改后无法快速验证是否变好

---

## 考虑过的选项

**A) 维持现有手工 TDD**：继续用主观 `expected_behavior` 文字描述，由人工判断通过与否。

**B) 自研 eval 框架**：自己写 eval runner、grader、benchmark 工具。

**C) 采用 skill-creator**：使用 Anthropic 官方元技能，提供完整的 起草→测试→评估→迭代 工作流，含 eval runner、assertion grader、benchmark viewer、描述优化器。

---

## 决策

**采用 C：skill-creator 作为所有 Skill 开发的强制工作流。**

选择原因：
- skill-creator 是 Anthropic 官方元技能，与 Claude Code 深度集成，维护成本由 Anthropic 承担
- 提供 with-skill vs baseline 的客观对比，每个 assertion 有明确通过/失败判断
- eval-viewer 让人工审阅从「读文字」变成「看实际输出对比」
- 描述优化器（`run_loop.py`）可以客观测量 Skill 触发准确率，解决 `using-harness` 的 1% 规则效果问题
- 与现有 `evals/evals.json` 格式高度兼容，只需补充 `assertions[]` 字段

---

## 后果

**对 Agent 的约束（不可绕过）**：
- ❌ 禁止在未经 skill-creator eval 的情况下修改 SKILL.md 并提交
- ❌ 禁止以「这个改动很小」「只是文字调整」为由跳过 eval 流程
- ✅ 每个 Skill 目录必须包含 `evals/evals.json`（skill-creator 格式）
- ✅ PR 必须附上 benchmark 结果（with-skill vs baseline assertion 通过率）

**对贡献者的要求**：
- Skill 贡献流程已更新至 CONTRIBUTING.md，skill-creator 工作流是门槛，不是建议
- 描述优化步骤可选，但强烈推荐用于新 Skill 首次发布前

**已完成的迁移工作**：
- v1.6.0 已将所有 evals 按 skill-creator 格式重组到各 Skill 目录
- 每个 eval 补充了 `assertions[]` 数组，可被 grader subagent 客观评分

---

## 参考

- [Anthropic skill-creator SKILL.md](.claude/skills/skill-creator/SKILL.md)
- [各 Skill eval 文件](../../skills/)
- [ADR 0001: Skill-based Architecture](0001-skill-based-architecture.md)
