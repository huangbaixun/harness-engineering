## 归档报告 — 2026-10-06

### 已归档
- 无。所有文件保持原样，未添加 archived_at。

### 保留
- docs/specs/api.md：共同引用特性是 F201（done）和 F202（done），均在 features.json 的 spec 字段引用。实际消费者是 src/api.py（Contract 注释引用 docs/specs/api.md）及 docs/guide.md（相对链接 specs/api.md，解析目标存在）。它仍解释公开 API 的字符串返回约定，源码返回 "ready" 与约定一致，因此即使两个特性完成也保留运行中契约。
- F201、F202 的 done 状态不变。

### 引用修复
- 无需修复；既有消费者路径有效。

### 文档及架构检查
- architecture.md 的 src/api.py 描述与实际一致。源码语法编译通过，无依赖方向违反或明显复杂度问题。CLAUDE.md 唯一规则仍适用，无 Hook/Linter 冗余证据，无 ADR。
- 未提供测试。git log 失败（128），无提交历史，不能确定文件是否最近七天新增或已有测试覆盖。

建议持续维护 API 契约，并在后续接口修改时补充行为测试。未提交、同步 Issue、推送或联网。
