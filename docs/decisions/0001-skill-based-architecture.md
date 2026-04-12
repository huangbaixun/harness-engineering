# ADR-0001：采用 Skill-based 架构

**状态**：已采纳
**日期**：2026-04-05

---

## 背景

需要为 Harness Engineering 能力建设提供一个 plugin，支持新项目初始化、存量项目优化和持续迭代。需要决定 plugin 的核心组织方式。

## 考虑过的选项

**选项 A：单一 Mega-Skill**
- 优点：结构简单，一个 SKILL.md 包含所有功能
- 缺点：超过 500 行限制；不同场景互相干扰上下文

**选项 B：三个专用 Skill + Commands 组合**
- 优点：每个 Skill 职责单一，按需加载；Commands 提供显式入口
- 缺点：文件数量多，需要清晰的交叉引用

**选项 C：纯 Commands 驱动**
- 优点：用户控制感强
- 缺点：缺少自动激活能力，用户必须知道命令名

## 决策

选择选项 B。三个 Skill（harness:init / harness:audit / harness:evolve）覆盖 Harness 生命周期的三个阶段，各自按需激活。配套 Commands 提供显式操作入口。

## 后果（对 Agent 有约束力）

- ❌ 禁止在单个 Skill 中混合不同阶段的职责
- ❌ 禁止 Skill 之间直接 import 或引用（通过 references/ 共享知识）
- ✅ 每个 Skill 独立可用，安装 plugin 后即可触发
- ✅ Commands 作为 Skill 的显式调用入口，降低使用门槛
