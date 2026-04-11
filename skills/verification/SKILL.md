# verification — 完成前验证

> 整合自 obra/superpowers Verification Before Completion skill。
> 核心理念：Agent 会自信地声称"完成了"，但声明完成≠真的完成。
> 本 Skill 在 Stop Hook 之上增加语义层验证。

## 强制触发：任何"完成"声明前

在说出以下任何词汇前，必须先通过本验证清单：
- "已完成" / "done" / "finished"
- "实现了" / "写好了"
- "你可以测试了" / "可以合并了"
- 准备更新 `claude-progress.json` 将特性标为 completed

## 验证清单（按顺序执行）

### 层次一：功能验证
- [ ] 运行全套测试，**零失败**（不允许"这个失败无关紧要"）
- [ ] 对照 `features.json` 中该特性的每条 `acceptance_criteria`，逐条确认满足
- [ ] `out_of_scope` 中列出的内容**没有被实现**（过度实现也是问题）

### 层次二：质量验证
- [ ] Lint / 类型检查通过（`{{LINT_COMMAND}}`）
- [ ] 没有新增的 TODO / FIXME / HACK 注释（或已记录为 known debt）
- [ ] 新增代码有对应测试（覆盖率不低于现有基线）
- [ ] 公共 API / 函数有文档注释

### 层次三：架构验证
- [ ] 没有违反 `docs/architecture.md` 中的依赖规则
- [ ] 没有跨层直接调用（如 UI 直接调 Repo）
- [ ] 没有硬编码的 secret / 配置值

### 层次四：集成验证
- [ ] 构建成功（`{{BUILD_COMMAND}}`）
- [ ] 如有 e2e 测试，e2e 全部通过
- [ ] 如影响 API 接口，接口文档已同步更新

## 验证失败时

任何一项未通过 → **不声明完成，继续修复**。

不允许"先提交，问题后续修"或"这个小问题不影响功能"的合理化。

## 验证通过后

```
1. 更新 docs/claude-progress.json：
   - 将 in_progress 移入 completed_features
   - 记录完成时间和测试通过数

2. 更新 docs/features.json：
   - 将该特性 status 改为 "completed"

3. 如 completed_features 超过 10 条：
   - 触发归档机制（见 AGENTS.md 归档规则）
```

## 与 Stop Hook 的关系

```
Stop Hook（stop-typecheck.sh）：硬拦截 —— 测试/类型检查不通过则阻止工具调用
verification Skill（本文档）：软规范 —— 语义层面的"真正完成"定义

两者互补：
  Stop Hook 防止"带错误的完成"
  verification Skill 防止"遗漏验收标准的完成"
```
