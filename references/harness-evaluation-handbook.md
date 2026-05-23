# Harness 组件评价手册（HEval Handbook v1.0）

> 本手册定义 Harness Engineering 项目用于评价 AI Agent harness 组件能力的方法论、维度、任务集和聚合公式。
>
> **核心定位**：HEval 不是给 LLM 打分，而是给"包裹 LLM 的工程脚手架"打分——评测对象是 OpenSpec、Superpowers、gstack、GSD、harness-engineering 这一类 harness 框架本身的工程能力。
>
> **决策来源**：[ADR-0006 Harness 组件评价体系](../docs/decisions/0006-harness-evaluation-system.md)
>
> **历史上下文**：本手册取代 [four-frameworks-comparison.md](./four-frameworks-comparison.md) 作为权威评价方法。星矩阵保留为历史档案。

---

## 目录

1. [评价目标与范围](#1-评价目标与范围)
2. [评价对象的定义](#2-评价对象的定义)
3. [四层评价方法概览](#3-四层评价方法概览)
4. [L1 静态分析（Static）](#4-l1-静态分析static)
5. [L2 结构化评分（Rubric）](#5-l2-结构化评分rubric)
6. [L3 标准任务集（Benchmark）](#6-l3-标准任务集benchmark)
7. [L4 用户反馈与 dogfooding（Feedback）](#7-l4-用户反馈与-dogfoodingfeedback)
8. [聚合公式与等级](#8-聚合公式与等级)
9. [`harness:evaluate` 自动化评测架构](#9-harnessevaluate-自动化评测架构)
10. [报告 schema 与示例](#10-报告-schema-与示例)
11. [评价者中立性与抗偏见](#11-评价者中立性与抗偏见)
12. [验证案例：5 款现有 harness 的样例评分](#12-验证案例5-款现有-harness-的样例评分)
13. [与 four-frameworks-comparison.md 的兼容性](#13-与-four-frameworks-comparisonmd-的兼容性)
14. [附录 A：Rubric 锚点完整定义](#附录-arubric-锚点完整定义)
15. [附录 B：Benchmark 任务规格](#附录-bbenchmark-任务规格)
16. [附录 C：Static 指标完整公式](#附录-cstatic-指标完整公式)

---

## 1. 评价目标与范围

### 1.1 评价目标

HEval 解决三个具体问题：

1. **选型决策**：团队/个人选 harness 时，希望看到一个跨厂商可比的总分 + 维度分布，而不是各家自卖自夸的 README。
2. **演进监控**：harness 自身从 v0.5 → v0.6 时，需要量化"这次升级到底动了哪个能力"——不能只靠 changelog 的形容词。
3. **借鉴决策**：harness-engineering 决定从 OpenSpec / GSD / gstack / Superpowers 借鉴哪些能力时，用维度分布定位差距而不是凭直觉。

### 1.2 范围

**HEval 评价**：

- harness 框架（一个 git 仓库 + 一份明确的方法论）
- 单一版本（git tag 或 commit SHA 锚定）
- 默认配置（厂商 README 推荐的安装/启用方式）

**HEval 不评价**：

- 单个 prompt 的质量（属于 prompt engineering 范畴）
- 单个 LLM 模型的能力（SWE-bench / HumanEval / METR 已有覆盖）
- 任意 AI 编程工具（Cursor / Cline / Aider / Copilot 等 IDE/agent 不在范围内——它们是 harness 的宿主，不是 harness 本身）
- IDE 插件、第三方 MCP server、个人 dotfiles

### 1.3 与 harness:audit 的关系

| 工具 | 评价对象 | 用途 |
|------|---------|------|
| `harness:audit` | 一个**用户项目**的 harness 设置（你的项目里的 CLAUDE.md / Hooks / Skills 健康度） | 优化自己的项目 |
| **HEval** / `harness:evaluate` | 一个 **harness 框架本身**（OpenSpec / Superpowers 这种产品） | 选型与对比 |

二者维度有部分重叠（都涉及 6 层结构、Hook 强制、文档完备度），但视角不同：audit 看"这个项目用 harness 用得怎么样"，HEval 看"这个 harness 提供了什么能力"。

---

## 2. 评价对象的定义

### 2.1 什么算一个 Harness 组件

满足以下所有条件的 git 仓库可作为 HEval 评价对象：

- **可发现**：有公开 README，说明用途与安装方式。
- **可安装**：能通过 git clone / npm install / `claude plugin install` 等明确方式部署到一个新项目。
- **包含工程能力**：至少提供以下任一：skill / command / hook / agent / MCP / 系统提示词模板 / 工作流脚本。仅有 README 但没有可执行/可加载工件的不算。
- **有方法论主张**：README 或文档中能提炼出至少 1 条明确的 SDLC 哲学（"强制 TDD"、"spec 即活文档"、"fresh context per wave"、"角色拟人化"等）。

### 2.2 版本绑定

每次评测必须绑定到具体版本：

```
<harness-name>@<version-locator>

例：
  superpowers@v0.5.2
  openspec@2026-04-15  (commit short SHA)
  harness-engineering@v1.10.0
```

报告 metadata 中必须记录：

- `version_locator`：tag 或 SHA
- `evaluated_at`：评测日期
- `benchmark_version`：使用的 Benchmark 任务集版本
- `evaluator_runtime`：评测时的 Claude 模型版本（如 `claude-sonnet-4-6`）

### 2.3 评测时间窗

L4 用户反馈采用 **过去 90 天滚动窗口** 的数据。L1/L2/L3 是版本快照，与时间无关。

---

## 3. 四层评价方法概览

```
                          HES 总分（0-100，S/A/B/C/D 等级）
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │           │               │               │
      15%         30%             40%             15%
        │           │               │               │
       L1          L2              L3              L4
     Static     Rubric         Benchmark        Feedback
   静态分析    结构化评分      标准任务集        用户反馈
   (脚本)     (评审+LLM)       (运行时)         (数据采集)
        │           │               │               │
        ▼           ▼               ▼               ▼
   仓库结构      7 维度          6 任务          GitHub +
   元指标       0-5 锚点        SDLC 跑分       dogfooding
```

**为什么是这四层**：

- **L1 Static**：抗作弊 anchor。只看可机械计算的事实（skill 数量、hook 类型、ADR 个数），任何评分员都能复现，但无法反映质量。
- **L2 Rubric**：连接主观与客观。给 7 个互斥维度配明文锚点，让"我觉得这个 harness 严格"变成"它在『强制性与门禁』维度得了 4 分，因为有 Stop Hook 但没 PreToolUse 拦截 force-push"。
- **L3 Benchmark**：行为 ground truth。让 harness 真的跑 SDLC 任务，看能不能在长周期、并行、回归、归档场景下保持质量。这一层权重最大。
- **L4 Feedback**：用真实信号校准。star 数量、issue 解决率、第三方使用案例稀释设计期纸面优势。

四层互相校验：如果 L2 给了高分但 L3 跑分失败，说明 Rubric 锚点没对齐实际能力，触发 handbook 修订。

---

## 4. L1 静态分析（Static）

### 4.1 设计原则

**L1 只衡量"事实"，不衡量"质量"**。任何需要语义判断的指标都不放在 L1。L1 的总分是 **0-100，权重 15%**。

### 4.2 指标矩阵

| 指标 | 测量方式 | 满分条件 | 权重 |
|------|---------|---------|------|
| Skill 原子化度 | `skills/` 目录下 SKILL.md 数量 ÷ 平均行数 | ≥10 个 skill 且平均 < 200 行 | 15 |
| Frontmatter 完整率 | 含完整 `name + description + 触发短语` 的 SKILL.md / 总数 | 100% | 10 |
| Hook 类型覆盖 | settings.json 中触发的 hook 事件类型数（PreToolUse / PostToolUse / Stop / SessionStart / UserPromptSubmit） | ≥4 类 | 15 |
| Hook 静默成功 | 测试 hook 在成功路径无输出 | 100% silent on success | 5 |
| ADR 数量与时间分布 | `docs/decisions/` 数量 + 最近 6 个月有更新 | ≥5 篇且 6 个月内有更新 | 10 |
| 文档密度 | docs/ + references/ 总字数 ÷ 代码行数 | ≥0.5 字/行（手册型） | 10 |
| Self-test 脚本 | 是否存在 self-test.sh 或等价 CI | 存在且运行通过 | 10 |
| Marketplace 可发现性 | 是否在 Anthropic / 第三方 marketplace 可装 | 已上架 | 5 |
| 依赖卫生 | 第三方依赖数量 + license 合规扫描 | ≤5 个非 dev 依赖且 license 兼容 | 5 |
| 元测试覆盖率 | harness 自身的 skill / hook 的测试 | ≥1 类 skill 有测试 | 5 |

总分 90 分，按比例标准化到 0-100。详细计算公式见附录 C。

### 4.3 实现方式

由 `harness:evaluate` 内嵌的静态扫描器 (`tools/static-scanner.py` 设计中) 自动产出。无需 LLM 介入。

---

## 5. L2 结构化评分（Rubric）

### 5.1 7 个维度

| 维度 | 关键词 | 一句话定义 |
|------|-------|-----------|
| D1 方法论完整度 | SDLC 阶段覆盖 | 从 clarify / design / plan / code / verify / ship / monitor，覆盖几个阶段 |
| D2 能力分层结构 | 六层模型 | Memory / Rules / Skills / Agents / Hooks / Tools 中提供了哪几层 |
| D3 强制性与门禁 | rigid / Hook | rigid 约束清晰度、Hook 强制能力、绕过门禁的难度 |
| D4 可追溯性与归档 | 活规格 / ADR | 决策、proposal、变更是否被持久化到可检索归档 |
| D5 上下文管理与抗腐蚀 | fresh context / parallel | context rot、并行 subagent、长周期项目支持 |
| D6 可观测性与反馈闭环 | canary / postmortem | 发布后监测、失败回流改进、dogfooding 证据 |
| D7 生态与文档 | marketplace / 文档 | marketplace 可发现性、社区生态、文档完备度、扩展机制 |

#### 5.1.1 维度归属歧义消解（重要）

某些能力会同时触及多个维度。为避免重复计分或漂移，使用以下**单一归属规则**——每个能力只能在它最契合的维度上加分，其他维度只作为佐证（不重复打分）：

| 能力 | 默认归属 | 判断依据 |
|------|---------|---------|
| TDD（红绿重构） | **D1** 方法论 | 只要 SDLC 中有 verify 阶段就算覆盖；D3 仅在 TDD 被 Hook 强制时才加分 |
| TDD Hook 强制 | **D3** 强制性 | 与上一行区分：D1 看"流程是否覆盖"、D3 看"流程是否可绕过" |
| 并行 subagent | **D5** 上下文管理 | 并行的核心价值是 context rot 抵御，不计 D2 |
| Agents 层（角色 subagent） | **D2** 能力分层 | 当 subagent 用于角色拟人化（CEO/QA/Eng）而非 context 隔离时算 D2 |
| 真浏览器 E2E | **D6** 可观测性 | 测试覆盖归 D1（方法论 verify 阶段），但端到端运行时反馈归 D6 |
| MCP 工具集成 | **D2** 能力分层 | Tools 层；不计 D7（D7 看的是 harness 自身能否被多 IDE/工具承载，与 MCP 无关） |
| Spec 归档 vs ADR 归档 | **D4** | 都归 D4；D1 方法论只看"是否产出 spec"，不看是否归档 |

**通用判别原则**：一个能力**存在** → D2；**被强制** → D3；**被持久化检索** → D4；**用于 context 复位** → D5；**用于运行时反馈** → D6；**支持 marketplace/文档生态** → D7；上述都不沾、只是 SDLC 阶段覆盖 → D1。

### 5.2 评分锚点（0/2/4/5）

每个维度在 0、2、4、5 四个锚点上有明文定义；1 与 3 是介于相邻锚点之间的判断。**完整锚点矩阵见附录 A**。

举例（D3 强制性与门禁）：

- **0 分**：完全靠提示词约束，没有任何机械强制；TDD/破坏性命令拦截全靠模型自觉。
- **2 分**：有部分 PreToolUse 或 Stop Hook，但覆盖单一场景（仅保护 .env 等）。
- **4 分**：rigid/flexible 在 frontmatter 显式标注；Hook 覆盖 ≥3 个事件；提供 force-push / DROP TABLE / rm -rf 三类破坏性命令拦截。
- **5 分**：有"门禁可观测性"——绕过门禁会被记录到 audit log；rigid skill 自带元测试验证强制路径；Hook 失败时给出可执行的修复建议。

### 5.3 评分流程

```
                  Rubric 评分流程

     输入：harness@version 仓库
              │
              ▼
   ┌─────────────────────┐
   │ Step 1: 准备证据包  │  扫描仓库提取每个维度的"证据"
   └─────────────────────┘  (相关文件路径、关键代码片段、文档摘录)
              │
              ▼
   ┌─────────────────────┐
   │ Step 2: LLM 评分员  │  用 Sonnet/Opus 按锚点打分
   └─────────────────────┘  输出 7 个维度分 + 每分的引用证据
              │
              ▼
   ┌─────────────────────┐
   │ Step 3: 外部评审人   │  人类（非该 harness 作者）复核
   └─────────────────────┘  对分歧 ≥1 分的维度做仲裁
              │
              ▼
   ┌─────────────────────┐
   │ Step 4: 锁定快照     │  scores.json + evidence/*.md
   └─────────────────────┘  写入 eval-reports/
```

**强制约束**：

- Step 2 的 LLM 模型必须在 metadata 中注明（不同模型分会漂移，跨版本对比时同模型才可比）。
- Step 3 的人类评审人**不能是该 harness 的作者或核心维护者**。
- 当 LLM 评分与人类评分相差 ≥2 分时，必须在 evidence/dispute.md 中记录分歧理由。

---

## 6. L3 标准任务集（Benchmark）

### 6.1 设计原则

Benchmark 不是测 LLM 解题能力（SWE-bench 已经做了），而是测**这套 harness 是否提升了同一 LLM 在多阶段 SDLC 中的稳定性**。

每个任务在两种配置下各跑一次：

- **Baseline**：裸 Claude Code，无 harness。
- **Treatment**：装上待评 harness。

最终关心的是 **Δ = Treatment − Baseline**，即 harness 带来的增量价值。

### 6.2 6 个标准任务

| 编号 | 任务名 | 难度 | 关键能力测试 | 时长上限 |
|------|--------|-----|--------------|----------|
| T1 | 微改 bug fix | ⭐ | 能否守住 scope，不过度实现 | 10 min |
| T2 | 单 feature CRUD | ⭐⭐ | clarify → plan → TDD → verify 完整链路 | 30 min |
| T3 | 单文件重构 | ⭐⭐ | 重构边界、回归保护、git history 整洁 | 30 min |
| T4 | 跨服务集成 | ⭐⭐⭐ | 设计 ADR、依赖管理、契约测试 | 60 min |
| T5 | 5-feature mini SaaS | ⭐⭐⭐⭐ | 长周期抗 context rot、并行 subagent、归档 | 120 min |
| T6 | Prod incident triage + postmortem | ⭐⭐⭐⭐ | incident workflow、回滚、blameless 总结 | 60 min |

> **v1.1 路线图（已识别但本期不收）**：以下三个任务是当前任务集的明确缺口，将在 benchmark v2 引入：
>
> - **T7 安全审查任务** —— 给定 PR 含 SQL 注入 / 凭据明文 / 越权读取，测 harness 能否给出准确审查结论；当前 D3 强制性的运行时验证主要靠 T2/T3 顺带，覆盖弱。
> - **T8 性能回归任务** —— 给定 baseline 性能数据，引入慢查询，测 harness 是否触发 benchmark / canary；当前 D6 可观测性仅靠 T6 single shot 测量。
> - **T9 文档优先任务** —— 仅产出 ADR 与 design doc 的纯文档任务，测 D4 归档能力；当前 D4 评分主要靠 T2/T4 的副产物，没有独立 ground truth。

每个任务的完整规格（task.md / setup.sh / verify.sh / oracle.json / fixtures/）见附录 B 与 `eval/benchmarks/v1/T*/` 目录（设计中）。

### 6.3 每个任务的指标

| 指标 | 含义 | 取值 |
|------|------|------|
| `pass` | 验证脚本是否全部通过 | 0/1 |
| `hands_off` | 完成过程中是否需要人工干预 | 0/1（1=完全自动） |
| `tokens_total` | 总 token 消耗 | int |
| `wall_clock_sec` | 任务总耗时 | int |
| `regression_count` | 引入了多少新失败的测试 | int（越低越好） |
| `artifacts_produced` | 是否产出 spec / ADR / postmortem | 0/1（仅相关任务记） |
| `scope_drift` | 实际改动文件数 / 任务声明文件数 | float（接近 1 最好） |

### 6.4 单任务得分公式

```
task_score = pass × (
    50                                          # 通过率基础分
  + 20 × hands_off                              # 自动化加分
  + 10 × clamp(1 - regression_count / 3, 0, 1)  # 回归惩罚
  + 10 × artifacts_produced                     # 文档加分
  + 10 × clamp(2 - scope_drift, 0, 1)           # scope 守纪
)
# token 与 wall_clock 不进单任务分；进效率分（独立报告，不计入 HES）
```

未通过的任务直接 0 分。6 个任务总分相加 → 标准化到 0-100。

### 6.5 抗作弊设计

- 任务集放在私有仓库，仅在评测时下发到沙箱（避免 harness 厂商把 fixture 答案预置到 skill 里）。
- 每个任务有 ≥3 个变体（同语义、不同变量名/结构），评测时随机选一个，结果用变体平均。
- Benchmark 任务集本身有版本号；当任务集 v1 → v2 时，所有历史评分会重新跑一遍以保持可比性，或显式标注"基于 benchmark v1，不与 v2 评分直接比较"。

---

## 7. L4 用户反馈与 dogfooding（Feedback）

### 7.1 数据源

| 数据源 | 测量项 | 权重 |
|--------|-------|------|
| GitHub | star / fork / watcher、月增长率 | 25 |
| GitHub | open issue 数 + 平均关闭时长 + bug:feature 比 | 20 |
| GitHub | 贡献者数 + 90 天活跃 PR 数 | 15 |
| 第三方提及 | 独立 blog / 视频 / 公开实践分享数 | 15 |
| Marketplace | Anthropic 或第三方 marketplace 评分（如有） | 10 |
| Dogfooding | 用此 harness 完成过 ≥3 个真实项目的明确证据 | 15 |

### 7.2 计算细节

- star / 月增长率使用对数标准化，避免大型项目通吃：`log10(stars + 1) / log10(10000) × 100`，封顶 100。
- 「issue 平均关闭时长」分四档：< 7d / 7-30d / 30-90d / >90d 对应 100/75/50/25 分。
- 「90 天活跃 PR 数」用 z-score 跨当前评测集所有 harness 标准化（这是相对指标）。

### 7.3 冷启动豁免

新发布 < 90 天的 harness：

- L4 的 6 个数据源中，「GitHub 三项」与「marketplace 评分」可置 N/A。
- L4 总权重从 15% 暂降为 0%，分数补回到 L3（权重升至 55%）。
- 评测报告必须显式标注 `feedback_status: cold_start`。

### 7.4 抗刷分设计

- star/fork 历史数据要看曲线，不看绝对值——用 GitHub Archive 拉 90 天日增数据，识别明显的"批量 star"事件并排除。
- 第三方提及必须有 URL 与作者识别，自家博客、自家员工博客、付费推广不计入。
- Dogfooding 证据必须是 **公开可验证** 的项目（开源仓库或带证明的私有截图）。

---

## 8. 聚合公式与等级

### 8.1 公式

```
HES = L1_score × 0.15
    + L2_score × 0.30
    + L3_score × 0.40
    + L4_score × 0.15

其中每层 score 已标准化到 0-100。
```

冷启动 harness（< 90 天发布、L4 数据稀疏）：

```
HES_cold = L1 × 0.20   # +5%
         + L2 × 0.40   # +10%
         + L3 × 0.40   # 不变
         + L4 × 0.00   # 标记为 cold_start
```

**为何不把 L4 全部并入 L3**：冷启动 harness 的 benchmark 跑分本身波动最大（任务集与 harness 设计预期不一定对齐），把 15% 全压到 L3 会让 grade 由单点决定。改为分散到 L1（事实指标稳定）+ L2（评审有人类校准），让冷启动评分的稳定性接近成熟 harness。

### 8.2 等级映射

| 等级 | HES 区间 | 含义 |
|------|---------|------|
| **S** | 90-100 | 全维度领先；可作为团队默认推荐 |
| **A** | 80-89 | 强；具体维度可能有空缺，需补 |
| **B** | 70-79 | 主流可用；与 baseline 相比有显著提升 |
| **C** | 60-69 | 概念可用，但工程化不成熟；适合早期采用者 |
| **D** | < 60 | 不建议生产使用，或仅适合特定场景（如纯 demo） |

### 8.3 维度雷达图

报告中除了 HES 总分，必须出**维度雷达图**展示 L2 的 7 个维度分布——总分相同的两款 harness 可能在维度分布上完全不同（例如同 80 分，一款均衡，一款 D3/D4 满分但 D7 缺位），雷达图让选型决策能落在维度上。

---

## 9. `harness:evaluate` 自动化评测架构

### 9.1 设计概览（不在本期实现，仅定型）

```
┌─────────────────────────────────────────────────────────────────┐
│                     harness:evaluate                              │
│                                                                  │
│  Input:  --target <git-url>@<ref>  --benchmark <version>          │
│  Output: eval-reports/<harness>@<version>/{report.md,scores.json} │
│                                                                  │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐         │
│   │ 1. Static    │   │ 2. Rubric    │   │ 3. Benchmark │         │
│   │    Scanner   │   │    Evaluator │   │    Runner    │         │
│   │  (no LLM)    │   │  (LLM agent) │   │  (sandbox)   │         │
│   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘         │
│          │                  │                  │                  │
│          └──────────────────┼──────────────────┘                  │
│                             │                                     │
│                ┌────────────▼────────────┐                        │
│                │  4. Feedback Collector  │                        │
│                │  (GitHub API / manual)  │                        │
│                └────────────┬────────────┘                        │
│                             │                                     │
│                ┌────────────▼────────────┐                        │
│                │  5. Aggregator          │                        │
│                │  (formula → HES)        │                        │
│                └────────────┬────────────┘                        │
│                             │                                     │
│                ┌────────────▼────────────┐                        │
│                │  6. Report Generator    │                        │
│                │  (md + json + radar)    │                        │
│                └─────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 各模块职责

#### Module 1: Static Scanner（无 LLM）

- 输入：harness 仓库本地 clone。
- 处理：扫 SKILL.md / settings.json / hooks/ / docs/decisions/，统计附录 C 定义的全部指标。
- 输出：`l1.json`，结构化指标 + 计算后的 0-100 分。
- 实现：纯 Python/shell 脚本，无 LLM，结果完全可复现。

#### Module 2: Rubric Evaluator（LLM 驱动）

- 输入：harness 仓库 + handbook 中的 7 维度锚点。
- 处理：分两阶段：
  - Stage A — 证据收集：对每个维度，从仓库提取 ≤5 个证据片段（文件路径 + 引用代码/文档）。
  - Stage B — 锚点匹配：用 Sonnet/Opus 比对证据与锚点定义，给出 0-5 分及理由。
- 输出：`l2.json` + `l2-evidence/<dim>.md`。
- 关键约束：必须有外部人类评审人在分歧 ≥2 分时介入仲裁，仲裁结果覆盖 LLM 输出。

#### Module 3: Benchmark Runner（沙箱）

- 输入：harness 仓库 + Benchmark 任务集 v1。
- 处理：每个任务在干净的 docker 沙箱中跑 baseline 和 treatment 各一次（变体随机），记录全部指标。
- 输出：`l3.json` + `l3-traces/<task>/{baseline,treatment}/{transcript.md, diff.patch}`。
- 关键约束：
  - 沙箱有 token 预算上限，超额视为任务失败。
  - 沙箱网络出站只允许 allowlist（git / npm / pip / Anthropic API），防止任务作弊上网搜答案。
  - 每次跑分有完整 transcript，方便事后审计。

#### Module 4: Feedback Collector

- 输入：harness 仓库 URL + 90 天时间窗。
- 处理：调 GitHub GraphQL API 拉数据；对第三方提及 / dogfooding 走半自动流程（搜索 + 人工审核）。
- 输出：`l4.json`。
- 关键约束：必须区分"原始数据"与"计算分数"——l4.json 同时保留两者，方便复审。

#### Module 5: Aggregator

- 输入：l1 / l2 / l3 / l4 的 score。
- 处理：套公式 → HES + 等级。
- 输出：`scores.json`。

#### Module 6: Report Generator

- 输入：所有上游 json + evidence。
- 处理：渲染 markdown 报告 + 雷达图（svg/png）+ 等级徽章。
- 输出：`report.md`。

### 9.3 与现有 harness-engineering 的集成点

- 新增 skill：`skills/evaluate/SKILL.md`（用 ADR-0001 的 skill-based 架构）。
- 新增 command：`commands/evaluate.md` → `/harness:evaluate`。
- Benchmark 任务集独立目录：`eval/benchmarks/v1/`。
- 评测报告归档：`eval/reports/<harness>@<version>/`，遵循 ADR（待建）的归档规范，git mv 保留历史。
- 在现有 `harness:audit` 中加交叉引用：用户问"我该选什么 harness"时，audit 引导到 evaluate 报告。

### 9.4 代价估算（参考）

- 单次评测：
  - L2 约 200K tokens（7 维度 × 证据收集 + 评分）。
  - L3 约 6 任务 × baseline+treatment × **3 变体**（§6.5 抗作弊要求） × 50K tokens ≈ **1.8M tokens**。
  - 合计单次评测 ≈ 2M tokens 量级。
- 计算时长：L1/L4 < 5 min；L2 ≈ 30 min；L3 ≈ 12-18 小时（含沙箱启动 + 变体并行）。
- 推荐评测频率：**harness 每发布 minor 版本时一次 + 季度统一评测一次**。
- 节流策略：变体抽样可降至 1（牺牲抗作弊度），把单次评测压到 600K tokens / 4-6 小时；重要发版用全量，常规体检用抽样。

---

## 10. 报告 schema 与示例

### 10.1 scores.json schema

```json
{
  "harness": "superpowers",
  "version_locator": "v0.5.2",
  "evaluated_at": "2026-05-03T08:00:00Z",
  "benchmark_version": "v1",
  "evaluator_runtime": {
    "L2_rubric_model": "claude-sonnet-4-6",
    "L3_benchmark_model": "claude-sonnet-4-6",
    "note": "示例占位，正式评测应填实际模型字符串"
  },
  "feedback_status": "active",

  "L1_static": {
    "score": 82,
    "metrics": {
      "skill_atomicity": 14,
      "frontmatter_complete_pct": 100,
      "hook_event_types": 4,
      "...": "..."
    }
  },

  "L2_rubric": {
    "score": 76,
    "dimensions": {
      "D1_methodology": 5,
      "D2_layering": 3,
      "D3_enforcement": 5,
      "D4_traceability": 2,
      "D5_context_hygiene": 4,
      "D6_observability": 3,
      "D7_ecosystem": 5
    },
    "human_reviewer": "external-reviewer-a",
    "llm_human_disputes": 0
  },

  "L3_benchmark": {
    "score": 66,
    "tasks": {
      "T1_bugfix":      {"pass": 1, "hands_off": 1, "regression_count": 0, "scope_drift": 1.0, "artifacts_produced": 0, "score": 90},
      "T2_crud":        {"pass": 1, "hands_off": 1, "regression_count": 0, "scope_drift": 1.2, "artifacts_produced": 0, "score": 88},
      "T3_refactor":    {"pass": 1, "hands_off": 1, "regression_count": 0, "scope_drift": 1.0, "artifacts_produced": 0, "score": 90},
      "T4_integration": {"pass": 1, "hands_off": 0, "regression_count": 0, "scope_drift": 2.5, "artifacts_produced": 0, "score": 60},
      "T5_5feature":    {"pass": 1, "hands_off": 0, "regression_count": 0, "scope_drift": 2.5, "artifacts_produced": 1, "score": 70},
      "T6_incident":    {"pass": 0, "score": 0}
    },
    "_note": "L3.score = mean(task_scores) = (90+88+90+60+70+0)/6 = 66.3"
  },

  "L4_feedback": {
    "score": 88,
    "github": {"stars": 4200, "forks": 310, "issue_close_p50_days": 12},
    "third_party_mentions": 18,
    "dogfooding_evidence": ["url1", "url2", "url3"]
  },

  "HES": 74.7,
  "grade": "B",
  "radar_chart": "report-assets/radar.svg"
}
```

### 10.2 report.md 结构

```markdown
# HEval Report — superpowers@v0.5.2

**Total HES**: 74.7  **Grade**: B
**Evaluated**: 2026-05-03 (benchmark v1, claude-sonnet-4-6)

## 一句话总结
方法论最纯，门禁最严；归档与 incident 工作流待补。

## 维度雷达
[radar.svg]

## 各层得分
- L1 Static     82
- L2 Rubric     76
- L3 Benchmark  66
- L4 Feedback   88

公式回算：0.15×82 + 0.30×76 + 0.40×66 + 0.15×88 = 12.3 + 22.8 + 26.4 + 13.2 = 74.7

## 关键发现
1. T6 Prod incident 任务失败：缺 incident workflow skill。
2. D4 Traceability 仅 2 分：无 spec 归档机制。
3. D7 Ecosystem 满分：已上 Anthropic marketplace + 完备文档。

## 建议借鉴方
- 想要 D3 强制性满分能力 → 借鉴 superpowers 的 rigid/flexible frontmatter。
- 不要把 T6 的失败当作硬伤——可以与 gstack 的 /careful 系列结合补齐。

## 完整证据
- [L2 维度证据](./l2-evidence/)
- [L3 任务 transcript](./l3-traces/)
```

---

## 11. 评价者中立性与抗偏见

HEval 直接落到 Harness Engineering 第 2 原则上：**永远不要让创建者独立评审自己的产出**。

### 11.1 评价 harness-engineering 自身的特殊规则

- L2 Rubric 至少需要 2 个外部评审人（非 harness-engineering 维护者），分歧 ≥1 分时讨论后取均值，不取最高方。
- L3 Benchmark 由其他 harness 厂商也跑一遍同任务集形成对比 baseline，避免我们的任务集隐性偏向自己。
- 报告必须公开发布到仓库，包含完整 evidence/ 与 traces/，允许任何人复跑反驳。

### 11.2 跨 harness 评价时的中立化

- L2 LLM 评分员对所有 harness 用同一个 prompt 模板，仅替换"待评 harness"参数。
- L3 sandbox 配置完全一致（同 LLM、同 token 预算、同网络 allowlist、同变体 seed）。
- L4 数据采集同时对所有 harness 拉同一时间窗。

### 11.3 公开异议机制

任何 harness 厂商对自己的 HEval 评分不服，可走"举证 → 重评"流程：

1. 提交 issue 指出具体维度的证据缺失或锚点误判。
2. handbook 维护者 24 h 内回复是否需要重评。
3. 如重评，原报告标记 superseded，新报告 metadata 中 reference 旧报告。

---

## 12. 验证案例：5 款现有 harness 的样例评分

> 本节是 dry-run，目的是验证 7 个维度有区分度（不会让 5 款 harness 全部得 4 分）。
> 数据来源：本仓库 `references/four-frameworks-comparison.md` + 各 harness 公开仓库阅读。
> **正式评分必须走 §3-§9 完整流程**；本节仅作设计验证，不构成权威排名。

| 维度 | OpenSpec | Superpowers | gstack | GSD | harness-engineering |
|------|----------|-------------|--------|-----|--------------------|
| D1 方法论完整度 | 3 | 5 | 3 | 4 | 4 |
| D2 能力分层结构 | 2 | 4 | 4 | 3 | 4 |
| D3 强制性与门禁 | 1 | 5 | 4 | 3 | 4 |
| D4 可追溯性与归档 | 5 | 1 | 1 | 4 | 3 |
| D5 上下文管理与抗腐蚀 | 3 | 3 | 2 | 5 | 4 |
| D6 可观测性与反馈闭环 | 2 | 3 | 5 | 3 | 3 |
| D7 生态与文档 | 3 | 5 | 3 | 2 | 4 |
| **L2 总分（标准化到 100）** | **54** | **74** | **63** | **69** | **74** |

观察：

- **OpenSpec** 在 D4 满分（活规格归档是它的杀手锏）但 D3 仅 1 分（没有任何强制 hook），分布极度偏科——这正是 four-frameworks-comparison.md 中"OpenSpec 需要配合其他框架才完整"判断的量化证据。
- **Superpowers** 在 D1/D3/D7 三项满分，但 D4 仅 1 分——和原星矩阵中"没有活规格归档"的弱点完全吻合。
- **gstack** 在 D6 满分（独占真浏览器 QA + canary + benchmark），但 D4 1 分——典型的"产品化强、方法论弱"特征。
- **GSD** 在 D5 满分（fresh context 是它的核心主张），D2 仅 3 分（角色/agent 层薄弱）。
- **harness-engineering** 与 Superpowers 同为 74 分，分布不同——后者在方法论纯度（D1/D3/D7）上更尖锐，前者在分层结构（D2）+ context 管理（D5）+ 归档（D4）上更均衡。harness-engineering 设计上没有任何一项是杀手锏，需要靠 P1/P2 借鉴 OpenSpec 的 D4 和 gstack 的 D6 补齐。
- **D2 评分中立性自查**：harness-engineering 在 D2 给 4 分（不给 5），因为虽然六层模型完整，但层间依赖规则的自动化校验（D2 满分必要条件之一）目前依赖人工 review，不是机械检查。这处自我克制是 §11.1 中立性规则的具体应用。

**区分度结论**：在 7 维度 × 5 harness = 35 个评分中，1-5 分均有出现，无单一维度被全部打满或打低，区分度合格。设计 OK。

---

## 13. 与 four-frameworks-comparison.md 的兼容性

### 13.1 维度映射

| four-frameworks 旧维度 | HEval 新维度 |
|----------------------|---------------|
| 规格归档 | D4 可追溯性与归档 |
| 长周期抗 context rot | D5 上下文管理与抗腐蚀 |
| TDD 严格度 | D3 强制性与门禁（部分） + D1 方法论（部分） |
| 并行执行 | D5 上下文管理（合并） |
| 产品/scope 挑战 | D1 方法论完整度（覆盖到 clarify 阶段） |
| 真浏览器 E2E | D6 可观测性（合并） |
| 破坏性动作防护 | D3 强制性与门禁（合并） |
| 生产发布与监测 | D6 可观测性（合并） |
| 方法论纯度 | D1 方法论完整度 |

旧的 9 维度部分重叠（如"TDD 严格度"和"方法论纯度"互相影响），HEval 合并到 7 个互斥维度。

### 13.2 旧文档的去留

- `four-frameworks-comparison.md` **保留**作为 historical context，但顶部需加 deprecation note 指向本 handbook 与 HEval 报告。
- 任何引用对外推荐 harness 选型的场合，必须用 HEval 报告，不再用旧星矩阵。
- 旧文档第三节"本项目可借鉴建议"的 P0/P1/P2 路线图保留，但首批 HEval 报告产出后需要重排（用维度差距而不是凭直觉排）。

---

## 附录 A：Rubric 锚点完整定义

> 每个维度给出 0 / 2 / 4 / 5 四档明文定义。1、3 档由评分员判断（介于相邻锚点之间）。

### D1 方法论完整度

- **0**：无明确方法论主张，仅是工具集合。
- **2**：覆盖 SDLC 中 2-3 个阶段（如仅 plan + code），其他阶段无显式工件。
- **4**：覆盖 5+ 阶段（clarify / design / plan / code / verify），每阶段有可识别的入口（skill / command / 文档 section）。
- **5**：覆盖完整 SDLC（含 ship / monitor），且阶段间有显式契约（一阶段输出 = 下一阶段输入），方法论在 README 中以哲学陈述明文表达。

### D2 能力分层结构

> **重要中立性说明**：六层模型本身是 harness-engineering 项目的概念；为避免 D2 锚点直接奖励"采用 harness-engineering 的语言"，本维度的判断标准是"承载的能力**类型**数量"而非具体层名。任何 harness 用自己的语言表达同等能力（例如 superpowers 的 skill + agent + hook 分类）都计入相应层。

- **0**：仅有 1 类能力（如只有 prompt 模板）。
- **2**：覆盖 2-3 类能力。
- **4**：覆盖 4-5 类能力 **或** 覆盖 6 类但层间依赖规则不显式。
- **5**：覆盖完整 6 类能力（静态记忆 / 确定性规则 / 按需技能 / 隔离智能体 / 强制钩子 / 工具扩展），**且**有显式的层间依赖规则（哪层禁止依赖哪层），**且**这条规则被自动化校验（不是空文档）。

### D3 强制性与门禁

- **0**：完全靠提示词约束，无机械强制。
- **2**：有部分 PreToolUse 或 Stop Hook，覆盖单一场景（如仅保护 .env）。
- **4**：rigid/flexible 在 frontmatter 显式标注；Hook 覆盖 ≥3 个事件类型；提供至少 2 类破坏性命令拦截（force-push / DROP TABLE / rm -rf 等）。
- **5**：有"门禁可观测性"——绕过门禁可被记录到 audit log；rigid skill 有元测试验证强制路径；Hook 失败时给出可执行的修复建议。

### D4 可追溯性与归档

- **0**：无任何 spec / 决策 / 进度的持久化机制。
- **2**：有 ADR 或 progress 文件，但归档机制缺失（旧记录直接被覆盖）。
- **4**：有 spec 与 ADR 的归档机制（如 changes/ → archive/），归档保留 git history。
- **5**：归档机制完整且可被自动化检索；提供 query / dump 的 skill；归档 schema 明文定义；进度文件机器可读 + 人类可读双格式。

### D5 上下文管理与抗腐蚀

- **0**：无任何 context 管理策略；context 自然膨胀直至崩溃。
- **2**：有 trim / clear 类操作但全靠人工调用；无并行 subagent。
- **4**：有显式的"fresh context per phase"机制；提供并行 subagent skill；session 间能恢复进度。
- **5**：context 健康度被持续监测（token 用量基线对比）；并行/串行依赖图自动推断；context rot 检测能触发自动重置。

### D6 可观测性与反馈闭环

- **0**：发布后即结束，无任何后续监测；失败不回流改进。
- **2**：有失败记录到 ADR / postmortem 的习惯，但全靠人工。
- **4**：有 canary / benchmark / E2E 任一项的自动化监测；postmortem 流程显式。
- **5**：覆盖 canary + benchmark + E2E 三类自动化反馈；失败到 harness 改进的回流路径在文档中显式描述并 dogfooded（有真实案例）。

### D7 生态与文档

- **0**：仅在单一工具上工作，路径硬编码，无文档。
- **2**：单工具但文档完备；或多工具但路径仍硬编码。
- **4**：上架 ≥1 marketplace；文档分层（README / handbook / ADR）；架构图 + ADR 体系完整。
- **5**：跨 ≥3 工具兼容；marketplace 有 ≥3 自然增长 install；社区贡献者 ≥10；提供"扩展自身"的 skill（writing-skills 或等价物）。

---

## 附录 B：Benchmark 任务规格

> 每个任务的 task.md / setup.sh / verify.sh / oracle.json 在 `eval/benchmarks/v1/T*/` 目录下完整化。本附录给出每个任务的设计意图与验证要点。

### T1 — 微改 bug fix

**Setup**：给定一个 50 行的小服务，单元测试中有 1 个失败（off-by-one）。
**任务**：让 harness 修复，并且**不能**改任何与 bug 无关的代码。
**Verify**：
- 失败测试转绿。
- `git diff` 影响行数 ≤ 5 行且仅在原失败函数。
- 不引入新文件。

**测什么**：scope 守纪 + 最小改动。多数 harness 应该在这里满分；不及格说明它有过度实现倾向。

### T2 — 单 feature CRUD

**Setup**：一个 todo app 的骨架（已有用户表），任务是加"按 tag 过滤"功能。
**Verify**：
- 新接口符合 oracle.json 中的 OpenAPI 契约。
- 有对应的单元 + 集成测试。
- 出现 spec / plan 之类的文档工件（D4 加分）。

**测什么**：完整 SDLC 链路 + 是否产出归档工件。

### T3 — 单文件重构

**Setup**：一个 600 行的单文件服务，需要拆成 ≥3 个模块。
**Verify**：
- 所有原有测试仍通过（regression_count = 0）。
- git history 中重构与功能改动是分开的 commit。
- 模块边界与拆分理由有 ADR 或 design doc 记录。

**测什么**：重构纪律（不夹带功能）+ 决策记录。

### T4 — 跨服务集成

**Setup**：两个独立服务 A、B，要求通过 message queue 集成；客户端先调 A，A 异步通知 B。
**Verify**：
- 集成测试覆盖 happy path + 1 个失败重试场景。
- 有 ADR 记录"为什么用 MQ 而不是 sync HTTP"。
- 契约测试（A 发什么、B 接什么）单独存在。

**测什么**：跨边界设计 + ADR 流程。

### T5 — 5-feature mini SaaS（长周期）

**Setup**：从空白起，按一个 5-feature spec 列表完整开发：用户注册、登录、发帖、点赞、通知。
**Verify**：
- 5 个 feature 全部通过端到端测试。
- 任务过程中没有出现因 context 满而漏掉某个 feature。
- 有进度持久化文件能让任务被中断后从中点继续。
- 并行不阻塞依赖（点赞依赖发帖，但发帖与登录可并行）。

**测什么**：长周期 context 抗腐蚀、并行 subagent、归档机制——这一项最区分 harness 的工程深度。

### T6 — Prod incident triage + postmortem

**Setup**：给定一个已经"上线"的服务（脚本模拟），oracle 注入一条 prod incident（数据库连接池耗尽导致 5xx 飙升）。
**Verify**：
- 完成 triage：识别根因、定位代码位置。
- 完成 fix：连接池配置或代码层面的修复。
- 完成 postmortem：blameless 文档 + action items + harness 改进项。

**测什么**：incident workflow 是否覆盖、是否能闭环到 harness 改进。

---

## 附录 C：Static 指标完整公式

```
# Skill 原子化度（满分 15）
skill_count = COUNT(skills/**/SKILL.md)
avg_skill_lines = AVG(LINES(skills/**/SKILL.md))
score_atomicity = clamp(
  (skill_count / 10) * 0.5 + (1 - clamp(avg_skill_lines / 200, 0, 1)) * 0.5,
  0, 1
) * 15

# Frontmatter 完整率（满分 10）
fm_complete = COUNT(skills 中含 name+description+触发短语) / skill_count
score_frontmatter = fm_complete * 10

# Hook 事件类型覆盖（满分 15）
hook_event_types = UNIQUE(settings.json 中 hooks.* 的 event 字段)
score_hook_coverage = clamp(LEN(hook_event_types) / 4, 0, 1) * 15

# Hook 静默成功（满分 5）
score_hook_silent = (在 dry-run 中所有 hook 成功路径无 stdout) ? 5 : 0

# ADR 数量与新鲜度（满分 10）
adr_count = COUNT(docs/decisions/0*.md)
recent_adr = COUNT(docs/decisions/*.md WHERE mtime > now - 180d)
score_adr = clamp(adr_count / 5, 0, 1) * 5 + clamp(recent_adr, 0, 1) * 5

# 文档密度（满分 10）
doc_words = WORDCOUNT(docs/**, references/**)
code_lines = LINES(skills/**, hooks/**, scripts/**)
score_doc_density = clamp((doc_words / max(code_lines, 1)) / 0.5, 0, 1) * 10

# Self-test（满分 10）
score_selftest = (EXISTS(self-test.sh) AND PASSES) ? 10 : 0

# Marketplace 可发现性（满分 5）
score_marketplace = (在 ≥1 marketplace 上架) ? 5 : 0

# 依赖卫生（满分 5）
non_dev_deps = COUNT(package.json/dependencies + 等价)
licenses_ok = ALL(deps WHERE license IN allowlist)
score_deps = (non_dev_deps <= 5 AND licenses_ok) ? 5 : 0

# 元测试（满分 5）
score_meta_tests = (≥1 类 skill 有 tests) ? 5 : 0

# L1 总分（0-100）
L1_score = SUM(全部 score_*)
```

---

## 变更日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-03 | v1.0 | 初版发布；7 维度 + 6 任务 + 4 层评价框架定型 |

> 维度锚点、任务集、聚合权重的任何修改必须在此处留 changelog，并同步更新 ADR-0006 的"下次 review 触发条件"。
