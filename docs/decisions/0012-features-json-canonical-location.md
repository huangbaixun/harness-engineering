# ADR-0012: features.json 的规范位置为仓库根目录

## Status
Accepted — 2026-08-22

## Context

执行 F004（schema 漂移对齐）时，全仓库 grep 门禁暴露出一个比计划预设更严重的事实：
本插件内部并存着**两套 features.json 约定**，且分别被不同的代码路径依赖。

| | 位置 | 状态枚举 |
|---|---|---|
| 本仓库（ADR-0003 dogfooding） | 根目录 `features.json` | `proposed / building / done` |
| `init.sh.template` 分发给用户项目 | `docs/features.json` | `pending` / `in_progress` / `done` |

F004 原本被描述为「三处 v1→v2 迁移残留」（`scripts/session-start`、
`skills/archive/SKILL.md`、`commands/assign.md`）。实际上那三处只是症状，
根因是从未有人裁定过哪个位置是规范 —— 另有约 10 个文件跟随模板那一套，
包括 `agents/coding-agent.md`、`commands/evals/evals.json`、三份 template、
`references/HarnessEngineering.md`、`skills/canary/SKILL.md`、`skills/init/SKILL.md`。

这直接阻塞 ADR-0011 与 F005：同步方案的一端是 GitHub，另一端是「谁在读写
features.json」。读端指向两个不同的文件时，同步的语义没有定义。

## Decision

**仓库根目录 `features.json` 是规范位置。**

`docs/features.json` 作为**永久回退**保留，用于兼容按旧模板初始化的用户项目。
所有读端按固定顺序解析：根目录优先，`docs/` 其次，都不存在则视为该项目未启用
features.json。

理由：`features.json` 是**项目级契约**而非文档 —— 它声明验收标准与范围边界，
是 Agent 闸门链的判定依据。与 `package.json` / `Cargo.toml` / `go.mod` 同级放在
根目录，语义一致且易被发现。放进 `docs/` 会暗示它是可选的说明材料。

ADR-0011 的 schema 2.1 设计也已假定根目录，本决策使该假定成立而非事后追认。

## Consequences

**正面：**
- 读端有唯一规范答案，新增读端不必各自发明查找顺序
- 已按旧模板初始化的用户项目**零破坏** —— 回退路径永久保留
- 解除 ADR-0011 / F005 的阻塞

**负面：**
- 每个读端都要实现两级回退，这是永久成本，不是过渡期成本
- 「零命中」类的 grep 门禁**不再是有效验收手段** —— 回退路径必须保留，
  `docs/features.json` 会长期合法存在于代码中。F004 的两条相关验收标准据此改写。
- 模板与用户项目之间出现版本差：新项目建在根目录，旧项目留在 `docs/`，
  同一份文档要同时描述两者

**未决：** 是否为已有用户项目提供一键迁移（把 `docs/features.json` 移到根目录并
更新引用）。本 ADR 不承诺迁移工具 —— 回退路径已使迁移非必需，迁移仅为整洁性。
若将来提供，应作为 `harness:evolve` 的一个动作而非独立命令。

## Considered alternatives

1. **`docs/features.json` 为规范，本仓库迁回 docs/** —— 否决：改动面确实最小，
   但与 ADR-0011 已成文的根目录假定冲突；且契约文件放 `docs/` 语义别扭。
2. **双路径永久并存、不裁定规范** —— 否决：这正是当前混乱的成因。
   新人不知道该建哪个，每个新读端都要重新发明查找顺序。
3. **只改本仓库的三处，不动模板** —— 否决：那会让插件的 dogfooding 实践
   与它分发给用户的模板长期背离，违反 ADR-0003 的意图。

## Related

- ADR-0003（dogfooding —— 本仓库与模板背离即违反其意图）
- ADR-0011（features.json 字段所有权与 schema 2.1 —— 假定根目录，被本决策坐实）
- F004（schema 漂移对齐 —— 本 ADR 由其执行过程浮现）
- F005（GitHub 同步 —— 被本决策解除阻塞）
