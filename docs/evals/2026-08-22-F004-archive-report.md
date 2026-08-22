# 归档报告 — F004（2026-08-22）

由 `harness:archive` 在 `verification-before-completion → finishing-a-development-branch → archive`
链条终点生成。

## 已归档

- `docs/plans/2026-08-22-features-json-schema-drift-plan.md` → `docs/archive/`
  （`git mv`，git 识别为 rename，`log --follow` 可追溯；已前置 `archived_at` / `feature_id` 元数据）

## 刻意未归档

- `docs/specs/2026-08-22-features-github-sync-design.md` —— **F004 与 F005 共用**。
  F005 仍是 `proposed`，归档会切断它的 spec 回指。archive skill 的 Step 1 按特性逐个
  搬运设计文档，未处理「一份 spec 服务多个特性」的情形，此处按引用面判断保留。
- F001–F003 的 spec 与三份 phase 计划 —— 既有归档积压，不属 F004 范围。
  它们被 `docs/decisions/0008`、`0009` 与 `scripts/sync-superpowers.sh` 引用，
  归档需同步修链，应作为独立任务。

## 文档漂移（已修）

`docs/architecture.md` 的 docs 树有四处失准：
- 列出了**不存在**的 `docs/design/`（幻影目录）
- 遗漏了实际存在的 `docs/archive/`、`docs/evals/`、`docs/superpowers/`
- ADR 清单停在 0009，而实际已有 0010 / 0011 / 0012

均已同步。复核：docs 子目录声明与实际完全一致，幻影目录零残留。

## 架构健康快检

| 项 | 结果 |
|---|---|
| CLAUDE.md 行数 | 44 / 60 |
| harness-original SKILL.md > 500 行 | 无 |
| vendored SKILL.md 仍为 ADR-0009 允许的 2 处编辑 | 13 / 13 |
| ADR 索引与实际文件 | 一致 |
| features.json 的 spec 指针 | 全部有效 |
| 架构层依赖方向（新增反向依赖） | 无 |

## 部署面判定

本次改动未触及 `.github/workflows/`、Dockerfile、IaC、k8s 或环境变量，
**不触发 `harness:canary`**。

## 过程偏差（如实记录）

1. **F004 的状态生命周期被压缩**。约定是 `proposed → building → done`，但执行期间
   我从未把它置为 `building`，收尾时直接 `proposed → done`。这是流程执行的疏失，
   不是 schema 问题；下次执行应在开工时先转 `building`。

2. **`claude-progress.json` 未同步**。`finishing-a-development-branch` 的 harness-delta
   要求把结果镜像到 `claude-progress.json`，但本仓库从来没有这个文件。凭空创建它
   会启动一个此前刻意没有的新惯例（且 `stop-commit-progress` hook 会开始自动提交它），
   属于独立决策，故未执行，在此记录而非静默跳过。
