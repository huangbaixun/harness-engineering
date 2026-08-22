# ADR-0011: features.json 字段所有权与 schema 2.1

## Status
Proposed — 2026-08-22

## Context

`features.json` 是 harness 的需求契约，28 个文件读写它，`proposed → building → done`
生命周期被整条闸门链依赖。它同时也是一份**只有 Agent 和写代码的人能看见的文件**——
团队的产品侧决策（优先级、指派、是否发布）发生在 GitHub / GHE 的 Issue 上。

要让两者联动，必须先回答一个问题：同一个概念在两处都能被修改时，谁说了算。

传统答案是时间戳仲裁或三方合并。两者在这里都不成立：
`last_updated` 是**文件级**粒度，任何字段变动都会刷新它，根本无法为字段级冲突仲裁；
而三方合并需要一个共同祖先，意味着要持久化同步状态，一旦状态丢失就无法判断。

## Decision

**不做冲突消解，做冲突消除。** 把 features.json 的每个字段指派给恰好一个写方：

- **harness 单写**：`name`、`description`、`acceptance_criteria`、`out_of_scope`、
  `spec`、`dependencies`、`status`
- **GitHub 单写**：`priority`、`delivery_state`、`assignee`、`milestone`
- **不同步**：`technical_notes`、`related_files`

划分原则：**rigid 约束归 harness，产品决策归 GitHub。**
`acceptance_criteria` 和 `out_of_scope` 是 Agent 闸门判定的依据，必须本地权威且离线可读；
`priority`、指派、是否发布是人的决策，GitHub 才是团队实际做这些决策的地方。

### status 拆分为两个正交维度

原 `status` 同时承载了工程进度和产品决策两种语义，是唯一真正的双写点。拆开：

- `status`（harness 单写）：`proposed / building / done` —— 工程实例状态
- `delivery_state`（GitHub 单写，新增）：`triage / accepted / shipped / wontfix` —— 产品决策

`status=done` + `delivery_state=wontfix` 是合法且有意义的组合（做完了但决定不发），
单一 status 字段无法表达。

### schema 2.0 → 2.1

新增 `github_issue`、`delivery_state`、`assignee`、`milestone` 四个 per-feature 字段，
以及顶层 `github` 配置块。**全部可选** —— 2.0 文件不加字段照常工作，只是不参与同步，
用户项目无需强制迁移。

## Consequences

**正面：**

- **对账退化为无状态纯函数**：harness 域无条件推、GitHub 域无条件拉。
  不需要时间戳、content hash 或共同祖先。
- **同步状态可随意丢弃**：影子副本 `.harness/last-synced.json` 纯属性能优化，
  丢失即退化成全量对账，结果一致。这消除了整类「状态损坏」故障。
- **不需要冲突合并 UI**：不存在需要人裁决的场景。
- **闸门链保持离线可跑**：rigid 约束全在本地权威字段里。

**负面：**

- `priority` 归 GitHub 意味着**离线时无法调整优先级**，且 `commands/assign.md`
  的排序依据从本地数字变成 PM 在 GitHub 上排的序。
- 人要理解两个状态维度而不是一个，认知成本上升。
- 字段划分是**契约**：以后新增字段必须先定所有权。划分错了的代价是重新出现冲突面，
  且届时正确的修法是回来改划分，而不是加合并逻辑 —— 这个约束需要长期守住。

**触发的既有 bug：** 落地过程中发现三处 v1→v2 schema 迁移残留
（`scripts/session-start`、`skills/archive/SKILL.md`、`commands/assign.md`
均在读 `docs/features.json` 并使用 v1 状态枚举）。其中 `session-start` 是
SessionStart hook，其特性摘要段实际上从未生效过。这些作为 F004 前置修复。

## Considered alternatives

1. **时间戳仲裁（后写者胜）** —— 否决：`last_updated` 是文件级粒度，
   任不起字段级仲裁；且静默丢失变更。
2. **features.json 单向推送到 GitHub** —— 否决：PM 在 GitHub 上改优先级、
   指派、关闭 Issue 全部不生效，人类协作者的操作会被下次推送覆盖。
3. **GitHub 为唯一真相，features.json 降为生成物** —— 否决：
   `acceptance_criteria` / `out_of_scope` 这些 rigid 约束会寄生在 Issue body 里，
   使整条闸门链依赖网络可用性。
4. **只存 issue URL 指针，不同步内容** —— 否决：两边内容各自漂移，
   谁也不为一致性负责，等于没有联动。

## Related

- `docs/specs/2026-08-22-features-github-sync-design.md`（本决策的完整设计）
- ADR-0003（dogfooding）
- ADR-0009（vendored skill 结构 / hook 脚本三元组约定）
- F004（schema 漂移对齐）、F005（双向同步实现）
