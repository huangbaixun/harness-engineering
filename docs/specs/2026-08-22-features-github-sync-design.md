---
date: 2026-08-22
topic: features-github-sync
type: feature
status: proposed
features: [F004, F005]
adr: [0011]
---

# features.json ↔ GitHub/GHE Issue 双向同步

## 1. 问题

`features.json` 是 harness 的需求契约 —— 28 个文件读写它，`proposed → building → done`
生命周期被 brainstorming / writing-plans / executing-plans / verification-before-completion /
finishing-a-development-branch / archive 整条闸门链依赖。

但它是一份**只有 Agent 和写代码的人能看见的文件**。团队的产品侧决策（优先级、指派、是否发布）
发生在 GitHub / GHE 的 Issue 上，两边各自演进，谁也不知道对方改了什么。

目标：让 features.json 与 GitHub/GHE 的 Issue 双向联动，且不破坏「闸门链离线可跑」这一性质。

## 2. 核心设计性质：冲突面 = 空集

所有字段划分为三类，**每个字段恰好一个写方**：

| features.json 字段 | 写方 | Issue 上的表示 |
|---|---|---|
| `name` | harness | title |
| `description` | harness | body 托管区块内正文段 |
| `acceptance_criteria` | harness | body 托管区块内 `- [ ]` 任务列表 |
| `out_of_scope` | harness | body 托管区块内围栏区块 |
| `spec` | harness | body 托管区块内链接 |
| `dependencies` | harness | body 托管区块内 `Blocked by #N` |
| `status` | harness | label `harness/<status>` |
| `priority` | **GitHub** | label `P0` / `P1` / `P2`（harness **只读**） |
| `delivery_state` | **GitHub**（新增） | label `state/*` 或 Issue 开关态（harness **只读**） |
| `assignee` | **GitHub**（新增） | Issue assignee |
| `milestone` | **GitHub**（新增） | Issue milestone |
| `technical_notes` | harness | **不同步** |
| `related_files` | harness | **不同步** |

三个推论，整个方案都建立在它们之上：

**推论 1 —— 对账是无状态的纯函数。** 既然每个字段恰好一个写方，reconcile 就是
「harness 域无条件推、GitHub 域无条件拉」，不需要时间戳、content hash 或三方合并。

**推论 2 —— 影子副本只是性能优化。** `.harness/last-synced.json` 用于算出脏 feature 集合，
避免全量扫描。它丢失、损坏或首次运行时，退化成全量对账，**结果完全一致**。

**推论 3 —— 不需要冲突合并 UI。** 没有需要人裁决的场景。若将来发现需要，说明字段所有权划错了，
正确的修法是回去改划分，而不是加一层合并界面。

### 2.1 status 与 delivery_state 是正交的两个维度

`status` 是工程实例状态（harness 单写）：`proposed → building → done`。
`delivery_state` 是产品决策（GitHub 单写）：`triage / accepted / shipped / wontfix`。

`status=done` + `delivery_state=wontfix` 是合法且有意义的组合 —— 做完了但决定不发。
用单一 status 字段无法表达这个状态，这正是拆分的理由。

### 2.2 新增字段

per-feature 新增 `github_issue`（Issue 编号，`null` 表示尚未同步）作为唯一的配对锚点，
以及 GitHub 单写的 `delivery_state` / `assignee` / `milestone`。
顶层新增 `github` 配置块（见 §4）。**全部可选**，schema 2.0 文件不加字段照常工作。

注意 `github_issue`（per-feature 指针）与顶层 `github`（远端配置）是两个不同的东西，
命名相近但层级不同。

### 2.3 托管区块

Issue body 只有标记之间的内容由 harness 管理，每次推送**只替换区块内容**：

```markdown
<!-- harness:begin  自动生成，勿手改；要改请编辑 features.json -->
（description / 验收清单 / out_of_scope / spec 链接 / 依赖）
<!-- harness:end -->

↓ 这条线以下随便写，harness 永不触碰
```

区块外的人类讨论、评审意见完全安全。这是不选「整体覆写 body」的原因。

## 3. 同步机制

### 3.1 两个 hook 触点

| Hook | 动作 | 网络开销 |
|---|---|---|
| SessionStart | 拉 GitHub 域字段合入 features.json | 1 次 list |
| Stop | mtime 比对 → 差异集 → 推托管区块 + 回写 issue 编号 | 1 次 list + K 次 PATCH（K 见 §3.3） |

**编辑热路径上没有网络。** 不使用 PostToolUse —— marker 提供不了 mtime 给不了的信息，
而热路径上已挂着 `post-format`（`Write|Edit`）和 `post-observe`（全量）两个 hook。

SessionStart 的护栏三条：硬超时（默认 5s，超时即用本地数据继续）、失败绝不阻断会话、
未配置远端时整段跳过（零开销）。

### 3.2 推送幂等（关键）

PATCH 之前先 GET 当前 body，**只有托管区块内容真的不同才写**。

理由：每次 PATCH 都会通知 Issue 的所有 watcher。一个会话推 5 次 = 5 封邮件轰炸 PM，
这足以让团队直接把这套东西关掉。幂等不是优化，是可用性前提。

### 3.3 批量化与真实网络开销

两侧的 list 都取全量后在本地配对，**不按 feature 逐条请求**：

- SessionStart：`gh issue list --label <prefix> --json number,labels,assignees,milestone,state`
- Stop：同一个 list 但**额外取 `body`**，使 §3.2 的幂等比对在本地完成，
  不需要为每个 feature 各发一次 GET

单次会话的网络开销因此是 **2 次 list + K 次 PATCH**，其中 K 是托管区块内容
**真的变了**的 feature 数 —— 稳态下 K 通常为 0，一次 brainstorming 产出新 feature 时为 1。
K 与 feature 总数无关，这是幂等比对在本地完成带来的性质。

### 3.4 入站路径

GitHub 上带 `harness/track` 标签、但没有对应 feature 的 Issue，被拉进 features.json 成为
`status: proposed` 的 stub（有 name/description，`acceptance_criteria` 为空），
再由 brainstorming 补齐结构后推回。

这让 PM 在 GHE 上提的需求能真正流进 harness 闸门链，而不只是单向汇报。
**不带该标签的 Issue 一律不碰** —— 团队日常 bug 单不会被卷进来。

### 3.5 删除的不对称处理

- Issue 被关闭 → 那是 GitHub 域的 `delivery_state`，拉下来即可，**不删 feature**
- feature 在本地被删 → **不自动关 Issue**，只告警

理由：关 Issue 对外可见且会通知他人，属于不可轻易撤销的外部动作，
不该由一次本地编辑静默触发。

### 3.6 首次接入

**绝不按 title 模糊配对已有 Issue** —— 配错就是把 harness 的验收标准覆盖到别人的单子上。
首次只处理 `github_issue: null` 的新建；已存在的 Issue 走一次交互式 `--adopt` 逐条确认。

## 4. 配置与分发

**opt-in 是硬要求。** 这是分发给用户项目的插件，hook 会在每个装了它的仓库里跑。
未配置远端时必须整段跳过、零网络、零开销 —— 否则就是在别人的仓库里偷偷发网络请求。

配置随仓库走，放 features.json 顶层：

```json
{
  "schema_version": "2.1",
  "github": {
    "enabled": true,
    "host": "catl.ghe.com",
    "repo": "org/repo",
    "label_prefix": "harness",
    "track_label": "harness/track"
  }
}
```

放这里而不是 `.harness/config.json` 或插件 `userConfig`：同步配置是**项目事实**，
应团队共享、随 clone 走、进 code review。而 `plugin.json` 的 `userConfig`
（team_name、default_tech_stack）是跨项目的个人偏好，语义不同。

`host` / `repo` 可省略，缺省从 `git remote get-url origin` 推断。

**认证完全复用 `gh auth`，绝不自己管凭据。** 仓库、配置、环境变量里都不出现 token。
GHE 侧靠 `gh auth login --hostname <host>`。这同时是安全边界：插件不接触任何密钥。

**label 命名空间隔离。** label 分两类，边界是硬的：

- **harness 可写**：仅 `harness/` 前缀（`harness/building`、`harness/track`）。
  只有这一类会被创建、增删。
- **harness 只读**：其余全部，包括 `P0/P1/P2` 和 `state/*`。它们是 GitHub 域字段的
  读取源，harness **绝不创建、修改或删除**它们 —— 即使发现 `P1` 不存在也不代建。

这条保证团队既有的 label 体系不会被这套东西动到一根汗毛。

**手动命令与 hook 互补**，不互相取代。`/harness:sync-issues` 承担三件 hook 干不了的事：
`--dry-run` 排查漂移、`--adopt` 首次接入配对、失败后手动重试。

**分发**：`features.json.template` 带 `github` 块但 `enabled: false`；`harness:init` 询问是否启用。

**一个 features.json 只绑一个远端。** 多远端会让「谁是 GitHub 域字段的权威」
重新变成冲突问题，而那正是第 2 节结构性消掉的东西。

## 5. 失败模式

**同步失败永不阻断任何 harness 闸门。** features.json 本地始终完整可用，
brainstorming → plan → TDD → verify → finishing 整条链离线可跑。同步是旁路，不是关键路径。

| 失败 | 处理 |
|---|---|
| 离线 / 网络超时 | 一行警告，`exit 0`，**影子不更新** → 下次会话自然重试 |
| 认证失效（401） | 与离线区别对待 —— 重试不自愈。给可操作提示：`gh auth login --hostname <host>` |
| 限流（403） | 单会话推送数设上限，超出则**明确报出剩余条数**，绝不静默截断 |
| Issue 被删（404） | 不当作「没同步过」去重建 —— 会丢评论和历史。告警并要求人工决定 |
| 托管区块被删 | 不盲目追加（会重复）。找不到标记就在 body 末尾重建一个，并提示一次 |
| 有人在区块内手改 | 会被覆盖 —— 设计意图，但区块头注释必须写明，让人**改之前**看到 |
| features.json 语法错误 | 静默跳过同步。报 JSON 错误不是同步的职责，hook 绝不因此崩 |
| 两个会话同时 Stop | `.harness/` 下原子锁（mkdir）。**拿不到锁就跳过**，绝不等待 |
| 首次接入大批量 | 走 `--adopt` 交互确认，不走 hook 自动路径 |

限流一条按 `writing-skills` 的「No silent caps」规则设计：一旦限制了覆盖范围就必须说出来，
静默截断会被读成「全都同步好了」，而实际没有。

Stop hook 一律 `exit 0` —— Claude Code 里 Stop hook 非零退出会阻断会话结束，
同步失败绝不该让人卡在会话里。按 CLAUDE.md「失败可见」原则，失败时输出**一行**警告；
这不违反「成功静默」，因为失败频率是每会话一次，不是每次编辑一次。

## 6. 前置阻塞项：features.json schema 漂移（F004）

本方案的一端是 GitHub，另一端是「谁在读写 features.json」。如果读端本来就读不到，
同步做得再对也是空转。当前有三处 v1→v2 迁移残留：

| 位置 | 症状 |
|---|---|
| `scripts/session-start`（**load-bearing hook**） | 读 `docs/features.json`（本仓库在根目录）；用 v1 枚举 `pending`/`ready`/`in_progress` |
| `skills/archive/SKILL.md` | 读 `docs/features.json`；用 `status: "completed"` |
| `commands/assign.md` | 读 `docs/features.json`；用 `planned`/`ready`/`in_progress` + `depends_on`/`blocks`/`owner` 等 v1 字段 |

schema 2.0 的枚举是 `proposed / building / done`。`session-start` 的特性摘要段**实际上从未生效过**。

F004 先修这三处，F005 再做同步。拆开的理由：它们是既有 bug，有独立价值，
应该有独立的 eval 和独立的回滚边界。

## 7. Out of scope

- Projects v2（看板 / 迭代 / 自定义字段）—— 需 `project` scope 重新授权，且 GHES 版本支持未验证
- Issue 评论的双向同步 / 读取
- PR ↔ feature 关联（`commands/review-pr.md` 是另一条线）
- 自动关闭或删除 Issue
- 多远端同时同步
- 任何形式的凭据管理
- 冲突合并 UI（按第 2 节推论 3，不存在需要它的场景）

## 8. 可验证性（eval 断言来源）

- 未配置远端时**零网络调用**
- 断网时闸门链完整可用，无任何闸门被阻断
- 连续两次 Stop 不产生第二次 PATCH（幂等）
- 托管区块外的人类内容**字节不变**
- 不带 `harness/track` 的 Issue 不被拉入 features.json
- 不带 `harness/` 前缀的 label 不被修改或删除
- 超出单会话推送上限时，剩余条数被明确报出（无静默截断）

## 9. 相关

- ADR-0011（features.json 字段所有权与 schema 2.1）—— 本 spec 的架构决策部分
- ADR-0003（dogfooding）—— 本仓库自己先吃狗粮
- ADR-0009（vendored skill 结构）—— hook 脚本三元组约定
- F004（schema 漂移对齐，前置）、F005（本特性）
