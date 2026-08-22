# docs/archive/

由 `harness:archive` 归档的已完成设计文档与实现计划。

## 约定
- 使用 `git mv` 而非 copy+delete，保证 `git log --follow` 可追溯完整历史
- 归档时在文件顶部前置元数据：`archived_at` / `feature_id`
- **共用文档不归档**：一份 spec 若仍被 `status` 非 `done` 的特性引用，保留在 `docs/specs/`
- 归档后须修复因移动而失效的入站链接

## 未归档的积压
F001–F003 的设计文档与三份 phase 计划仍在 `docs/specs/` 与 `docs/plans/`。
它们被 `docs/decisions/0008`、`0009` 与 `scripts/sync-superpowers.sh` 引用，
归档需同步修链，属独立任务。
