---
description: features.json ↔ GitHub/GHE Issue 手动对账。hook 负责日常无感同步，本命令负责 hook 干不了的三件事：dry-run 排查漂移、首次接入配对已有 Issue、失败后手动重试。
---

# /harness:sync-issues — features.json ↔ Issue 手动对账

> 日常同步由 hook 自动完成（SessionStart 拉、Stop 推），**无需手动运行**。
> 本命令用于非常规操作。设计依据：`docs/specs/2026-08-22-features-github-sync-design.md`

## 前置

`features.json` 顶层需有 `github` 块且 `enabled: true`：

```json
"github": {
  "enabled": true,
  "host": "catl.ghe.com",
  "repo": "org/repo",
  "label_prefix": "harness",
  "track_label": "harness/track"
}
```

`host` / `repo` 可省略，缺省从 `git remote get-url origin` 推断。
认证复用 `gh auth`，本插件不接触任何凭据；GHE 需先 `gh auth login --hostname <host>`；同步时主机经 `GH_HOST` 传给 gh。

## 用法

### 1. 排查漂移（只读，不写入）

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_sync.py" status
```

列出将要创建/更新的 Issue，不做任何写入。这是**动手前应该先跑的一步**。

### 2. 手动推送（hook 失败后重试）

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_sync.py" push
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_sync.py" push --limit 50   # 放宽单次上限
```

默认单次最多推 20 条；超出会**明确报出剩余条数**，再次运行即可继续。

### 3. 手动拉取

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harness_sync.py" pull
```

回流 GitHub 单写的 `priority` / `delivery_state` / `assignee` / `milestone`，
并把带 `harness/track` 标签的新 Issue 收为 `status: proposed` 的 stub。

## 首次接入既有仓库

**绝不按 title 模糊配对已有 Issue** —— 配错就是把 harness 的验收标准覆盖到别人的单子上。

1. 先跑 `status` 看清将要创建什么
2. 对**已存在**的 Issue，人工在对应 feature 上填 `"github_issue": <编号>`
3. 再跑 `push`；此时只有 `github_issue` 为 null 的才会新建

**首次 pull 会清空本地已填的 GitHub 单写字段。** 单写所有权是无条件的：
`assignee` / `milestone` / `delivery_state` 一律以 Issue 为准 —— Issue 上为空，
本地值就被**清空**。接入前若已在 features.json 里手填过这几项（例如从排期表抄来的
milestone 日期），它们既不会被推上去，也会在第一次 pull 时消失。

要保留，先在 Issue 上设好（`gh issue edit <n> --milestone ... --add-assignee ...`）
再 pull。或者接受它们本就属于 GitHub 域：若 features.json 里另有字段指向排期表，
被清掉的只是一份副本，事实源仍然唯一。

## 字段所有权（ADR-0011）

| harness 单写 | GitHub 单写 | 不同步 |
|---|---|---|
| name / description | priority | technical_notes |
| acceptance_criteria | delivery_state | related_files |
| out_of_scope / spec | assignee | |
| dependencies / status | milestone | |

改 GitHub 单写字段请去 Issue 上改，本地改动会被下次 pull 覆盖（含被覆盖为空）；
唯一例外是 `priority`：仅当 Issue 带 `P0`/`P1`/`P2` 标签时才回流，无标签则保留本地值；
改 harness 单写字段请改 features.json，Issue 上的托管区块会被下次 push 覆盖。

**托管区块外的内容永不被触碰** —— PM 评审、讨论记录写在 `<!-- harness:end -->` 之后即可。

## 故障

| 现象 | 处理 |
|---|---|
| `认证已失效` | `gh auth login --hostname <host>`（重试不会自愈） |
| `触发 API 限流` | 稍后重试；或用 `--limit` 分批 |
| `目标 Issue 不存在` | 人工确认：清空该 feature 的 `github_issue` 重建，或恢复 Issue |
| `网络不可达` | 无需处理，下次会话自动重试 |
| `gh 调用参数有误` | 插件 bug，重试不会自愈，请提交 issue 并附提示中的 gh 原文 |
| `同步失败，已跳过` | 未能归类的 gh 错误，同上，请附 gh 原文 |
| 同步似乎没发生 | 检查 `github.enabled` 是否为 `true`；未配置时全链路静默跳过 |
