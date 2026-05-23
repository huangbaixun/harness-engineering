# CLAUDE.md — Mini 留言板（with harness）

> 这个文件是 AI 工作时的"项目宪法"。改动前必读。

## 项目定位

Mini 留言板演示项目。核心功能：列出 / 新建 / 删除留言。所有数据在内存中，**不持久化**。

## 测试

```bash
npm test          # 跑全部测试，必须全绿才能合入
```

测试文件：`tests/board.test.js`。共 3 个用例：列出、新建、删除。

## 架构约定

- **存储层**：进程内存（`server.js` 顶部的 `messages` 数组）。**禁止**改成 localStorage / Redis / 数据库——这是 demo 项目，存储已是范围外。
- **样式约定**：颜色和字号通过 `public/style.css` 顶部的 `:root` CSS 变量管理。**禁止**在组件里直接写 hex 颜色值。
- **API 契约**：
  - `GET /api/messages` 返回 `[{id, text, author, createdAt}]`
  - `POST /api/messages` 接 `{text, author}`
  - `DELETE /api/messages/:id`
  - 不要随意修改字段名或返回结构。

## 禁止规则（rigid）

- ❌ 不引入新的 npm 依赖（项目仅依赖 express）
- ❌ 不修改存储层（保持内存数组）
- ❌ 不改 `:root` CSS 变量名
- ❌ 不在功能 PR 中夹带"顺手重构"
- ❌ 任何新功能必须先有失败测试再写实现（TDD）

## 工作流（rigid）

新需求落地必须走：

1. `/harness:plan` — 先澄清，产出 features.json（含 acceptance_criteria 和 out_of_scope）
2. `/harness:tdd` — Red → Green → Refactor，每步 commit
3. `/harness:audit` — 完工前自检
4. 提交 PR，附 design doc 链接

## 决策记录

架构决策放 `docs/decisions/`。已有 ADR：

- ADR-0001：选择内存存储而非数据库（演示项目，故意不持久化）
