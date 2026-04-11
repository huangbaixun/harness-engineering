# tdd — 测试驱动开发工作流

> 整合自 obra/superpowers TDD skill，适配 Harness Engineering 六层模型。
> 在 Harness 环境中，Stop Hook 提供硬拦截，本 Skill 提供流程规范。

## 核心循环：RED → GREEN → REFACTOR

任何功能实现必须严格遵循三阶段循环，**不允许跳步**：

```
RED（写失败测试）
  → 先写能描述期望行为的测试
  → 运行测试，确认它失败（红色）
  → 失败原因必须是"功能未实现"，而非"测试本身写错了"

GREEN（最小实现）
  → 写最少的代码让测试通过
  → 不允许过度设计，只让当前测试通过
  → 运行全套测试，确认全部绿色

REFACTOR（重构）
  → 在测试保护下清理代码
  → 消除重复、提升可读性
  → 重构后再次运行测试确认仍然全绿
```

## 触发条件（1% 原则）

只要有 1% 可能，必须在开始实现前激活本工作流：

| 情形 | 示例 |
|------|------|
| 实现新功能 | "帮我写一个 X 功能" |
| 修复 Bug | "这里有个问题，帮我修" |
| 重构代码 | "这段代码需要优化" |
| 实现 features.json 中的条目 | coding-agent 取下一个特性时 |

## 与 Harness 其他层的协作

```
features.json（需求锚点）
    ↓  取出 acceptance_criteria
writing-plans Skill（任务拆解）
    ↓  拆解为 2-5 分钟任务
tdd Skill（本工作流）
    ↓  RED → GREEN → REFACTOR
Stop Hook（stop-typecheck.sh）
    ↓  测试全通过才允许完成
verification Skill（最终确认）
    ↓  对照 acceptance_criteria 验收
claude-progress.json（状态更新）
```

## 每个测试应满足

- **一个测试只测一件事** — 失败时原因明确
- **测试名描述行为** — `test_user_cannot_login_with_wrong_password`，不是 `test_login`
- **AAA 结构** — Arrange（准备）→ Act（执行）→ Assert（断言）
- **测试独立** — 不依赖其他测试的执行顺序或状态

## 常见错误和纠正

| 错误模式 | 正确做法 |
|----------|---------|
| 先写实现再补测试 | 必须先写测试，看到红色才开始实现 |
| 一次写多个测试 | 一次只写一个测试，通过后再写下一个 |
| REFACTOR 阶段不运行测试 | 每次重构后必须重新运行全套测试 |
| 测试通过就跳过 REFACTOR | REFACTOR 是必要步骤，不是可选项 |
| 为了让测试通过而修改测试 | 测试是规格，修改测试意味着改变需求 |
