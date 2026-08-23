# 归档报告 — F005（2026-08-23）

## 已归档
- `docs/plans/2026-08-23-f005-github-issue-sync-plan.md` → `docs/archive/`（git mv，识别为 rename）

## 刻意未归档：共用 spec

`docs/specs/2026-08-22-features-github-sync-design.md` 保留在原处。

F004 收尾时不归档的理由是「F005 仍在使用」；本次两者都已 done，理由变了但结论不变：
该 spec 已成为**已发布代码的活文档** —— `scripts/harness_sync.py` 的文件头和
`commands/sync-issues.md` 都指向它，共 10 处入边。归档它等于把用户会读的文档
移进归档区并制造 10 处断链。

**plan 是执行产物，执行完即可归档；被已发布代码引用的 spec 是活文档，应保留。**
archive skill 的 Step 1 没有这个区分。

## 立项：F006

archive skill 的两个盲区在 F004 与 F005 收尾时各踩到一次，两次都靠人工判断绕开：
1. 共用 spec —— 按特性逐个搬运会切断尚未完成特性的回指
2. 活文档 vs 执行产物 —— 没有区分，会把用户在读的文档归档掉

已立为 F006（proposed），不静默修也不静默丢。

## 架构健康

| 项 | 结果 |
|---|---|
| CLAUDE.md 行数 | 44 / 60 |
| harness-original SKILL.md > 500 行 | 无 |
| vendored SKILL.md 仍为 2 处允许编辑 | 13 / 13 |
| 新增反向层依赖 | 无 |
| 测试 | 6 套全绿，完全离线可跑 |
| 部署面 | 未触及，不触发 canary |

## 遗留（未处理，有明确归属）
- F001–F003 的归档积压 —— 需同步修 `0008` / `0009` / `sync-superpowers.sh` 三处链接
- `references/team-parallel-development.md` 的 owner/files_owned/worktree 方法论 schema
- schema 缺 `cancelled` 状态 —— ADR-0011 提议以 `delivery_state: wontfix` 承载，现已随 F005 落地，
  但 `skills/init/SKILL.md` 中的说明尚未回填指向该字段
