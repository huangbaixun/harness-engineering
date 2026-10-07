已通过 git mv 将 F301 执行计划移至 docs/archive/f301.md。保留 owner: release-team，加入 archived_at、completed_by 和 feature_id，更新 features.json 的计划路径与 archived_at，并修复 docs/history.md 的入链。计划中的 ../architecture.md 在归档后仍正确指向 docs/architecture.md。

没有发现文档结构漂移；src/ 和 ADR 不存在，相关架构检查不适用。git diff --check 通过。仓库没有提交历史；已使用 git mv 保持可追溯的移动操作，未创建提交、同步 Issue 或推送。
