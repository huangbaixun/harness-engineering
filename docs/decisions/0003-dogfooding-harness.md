# ADR-0003：项目自举（Dogfooding）

**状态**：已采纳
**日期**：2026-04-05

---

## 背景

本 plugin 本身是一个工程项目。需要决定是否用 Harness Engineering 规范来管理 plugin 自身的开发。

## 考虑过的选项

**选项 A：不做自举，简单结构**
- 优点：开发速度快
- 缺点：无法验证自身规范的可行性；对用户缺乏说服力

**选项 B：完全自举**
- 优点：验证规范可行性（eat your own dog food）；作为用户参考的活文档
- 缺点：初始设置成本略高

## 决策

选择选项 B。plugin 项目本身使用完整的 Harness 规范：CLAUDE.md、architecture.md、ADR、Hooks 体系。这既是对规范的实战验证，也是用户学习的最佳示例。

## 后果（对 Agent 有约束力）

- ❌ 禁止在 plugin 开发中违反自身规范（如 CLAUDE.md 超过 60 行）
- ✅ 每次新增功能或修改架构，必须同步更新 ADR
- ✅ plugin 的 CLAUDE.md 和 architecture.md 本身就是模板的活示例
