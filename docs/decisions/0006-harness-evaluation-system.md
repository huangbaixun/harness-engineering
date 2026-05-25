# ADR-0006：Harness 组件评价体系（HEval）

- **状态**：已采纳（设计阶段，未实现）
- **日期**：2026-05-03
- **作者**：Harness Engineering
- **关联文档**：[references/harness-evaluation-handbook.md](../../references/harness-evaluation-handbook.md)、[references/four-frameworks-comparison.md](../../references/four-frameworks-comparison.md)

---

## 背景

`references/four-frameworks-comparison.md` 用 9 个维度的星级矩阵手工对比了 OpenSpec、GSD、gstack、Superpowers 四款 Claude Code harness 框架，并据此为 harness-engineering 制定了 P0/P1/P2 借鉴路线图。这套星矩阵在选型阶段够用，但作为长期使用的评价体系存在三个问题：

1. **维度定义不正交**——「方法论纯度」与「TDD 严格度」等维度互相重叠；星级评分的锚点（什么算 ★★★★ vs ★★★★★）没有明文定义，复评时分数会漂移。
2. **缺少行为证据**——所有评分基于阅读源码和文档的主观判断，没有"让这套 harness 跑一个真实任务"的运行时验证。当 harness 升级一个版本，无法判断分数是否真的变了。
3. **没有反馈闭环**——分数定下来后，社区使用、GitHub 数据、内部 dogfooding 的真实信号没有回流到评价里，评分迅速变成静态历史档案。

随着 harness-engineering 自身演进、Anthropic marketplace 上 harness 数量增长、企业内部需要选型 harness 标准化方案，需要一套**正交、可重复、可自动化、可演进**的评价体系。

---

## 考虑过的选项

### 方案 A：仅升级现有星矩阵（轻量）

继续维护 `four-frameworks-comparison.md`，把 9 维度补全锚点定义、明确每颗星对应的客观标准，复评时按锚点打分。

- 优点：改动最小，零工具链依赖，维护成本低。
- 缺点：依然全靠人工判读；新出的 harness 没人评就缺位；版本升级触发复评的成本不低；没有运行时验证手段。

### 方案 B：四层评价体系 + 自动化评测 harness（当前选择）

设计 L1 静态分析 + L2 结构化评分 + L3 标准任务集 + L4 用户反馈 共四层评价，加权聚合到统一分数（HES，Harness Evaluation Score，0-100 分 + S/A/B/C/D 等级）。再设计 `harness:evaluate` 自动化评测 harness 的架构（本次仅出设计，不实现）。

- 优点：行为证据 + 主观判断 + 元数据 + 社区反馈四路交叉，单点偏差被稀释；维度正交且锚点明文；与 harness-engineering 现有的六层模型、四要素、Computational/Inferential 反馈分离原则一致；自动化 harness 让分数随 harness 版本演进自动更新。
- 缺点：设计期工作量大；Benchmark 任务集需要持续维护；L3 跑分需要沙箱环境与 token 预算；L4 数据采集涉及 GitHub API、可能的隐私边界。

### 方案 C：直接复用 SWE-bench / METR / Princeton-NLP 学术 benchmark

把现成 LLM coding benchmark 套用到 harness 评测——给同一个 LLM 配不同 harness，比较 SWE-bench 通过率。

- 优点：任务集已经存在，结果有学术可比性。
- 缺点：SWE-bench 主要测「LLM 解决 bug 的能力」，不测 harness 提供的工程能力（spec 归档、parallel、context hygiene、canary 等等）；且这类 benchmark 任务粒度太单一，测不出多阶段 SDLC 的差异。harness 的核心价值在 SWE-bench 里被遮蔽。

---

## 决策

采用**方案 B — 四层评价体系 HEval**，详细方法论与维度定义见 `references/harness-evaluation-handbook.md`。

四层结构与权重：

| 层 | 名称 | 评价方式 | 权重 | 谁来打 |
|----|------|---------|------|--------|
| L1 | 静态分析（Static） | 自动扫描 harness 仓库结构 | 15% | 脚本 |
| L2 | 结构化评分（Rubric） | 7 维度 × 0-5 锚点 | 30% | 评审人 + LLM 交叉 |
| L3 | 标准任务集（Benchmark） | 6 个标准 SDLC 任务跑分 | 40% | 自动化 runner |
| L4 | 用户反馈（Feedback） | GitHub 数据 + dogfooding | 15% | 数据采集 |

L3 权重最大，因为运行时行为是 ground truth；L1/L4 各 15% 防止单点失真；L2 是连接主观判断与客观数据的中间层。

L2 的 7 个评价维度（每维度 0-5 分）：方法论完整度、能力分层结构、强制性与门禁、可追溯性与归档、上下文管理与抗腐蚀、可观测性与反馈闭环、生态与可移植性。每个维度在 handbook 里有 0/2/4/5 四个明文锚点。

`harness:evaluate` 自动化评测 harness 设计（不在本 ADR 实现范围）：六模块流水线 — 静态扫描器 → Rubric LLM 评分员 → Benchmark Runner → Feedback Collector → 聚合器 → 报告生成器。每次评测产出 `eval-reports/<harness-name>@<version>/{report.md, scores.json}`，作为该版本的可追溯快照。

---

## 后果（对 Agent / 维护者有约束力）

### ✅ 必须遵守

- 评价某款 harness 时，必须**绑定具体版本号**（git tag 或 commit SHA），评分快照永久保留；不允许"对最新版本"这种漂移说法。
- 同一款 harness 的 L2 Rubric 评分**不能由该 harness 的作者独立完成**——遵循 Harness Engineering 第 2 原则"永远不要让创建者独立评审自己的产出"。至少需要 1 个 LLM 评分员 + 1 个外部评审人。
- 新增评价维度需要走 ADR 流程；现有 7 维度的锚点定义改动也需要在 handbook 里留 changelog，避免静默调权。
- L3 Benchmark 任务集存放在 `eval/benchmarks/` 目录，每个任务有完整的 `task.md / setup.sh / verify.sh / oracle.json`。任务集本身有版本号，跨版本评分仅在同一 benchmark 版本内可比。

### ❌ 禁止

- ❌ 禁止用单一指标（如"GitHub stars"）对 harness 排名——HES 必须是四层加权结果。
- ❌ 禁止在 L1 静态分析维度纳入"代码风格/命名美感"等主观项；L1 只放可机械计算的指标。
- ❌ 禁止把 four-frameworks-comparison.md 的星矩阵当作权威——保留为 historical context，对外引用必须用 HEval 报告。

### ⚠️ 已知局限

- 设计阶段未实现自动化 runner，首批评分仍需人工执行 Benchmark；具体实现的 ADR 后续单独立项。
- L4 用户反馈对刚发布、社区数据稀疏的 harness 有偏；handbook §7.3 定义的「冷启动豁免」适用于发布 < 90 天的 harness，权重重新分配到 L1+5% 与 L2+10%（不全部并入 L3，避免 benchmark 噪声主导冷启动评分）。
- Benchmark 任务集本身是评价工具，自身演进会影响历史可比性——通过任务集版本号 + 锚定 baseline harness 缓解，无法根除。
- 当前 benchmark v1 缺少安全审查 / 性能回归 / 文档优先三类任务（handbook §6.2 列出，将在 v2 引入）；在此之前 D3/D6/D4 部分能力主要靠 L2 评审，运行时验证不充分。

### 下次 review 触发条件

- 任何 harness 厂商对自己的 HEval 评分提出系统性异议时
- Benchmark 任务集主版本变更时（v1 → v2）
- harness-engineering 自身发布 minor 版本（验证我们没在偏向自己的设计上打高分）

---

## 参考

- Harness Engineering 第 2 原则：永远不要让创建者独立评审自己的产出
- Harness Engineering 六层模型 / 四要素 / 反馈循环（references/harness-engineering-handbook.md）
- four-frameworks-comparison.md 的初版星矩阵（已被 HEval 取代，保留作历史档案）
- ADR-0001 Skill-based 架构（HEval 自动化 runner 后续将作为新 skill 落地）
- ADR-0003 Dogfooding 原则（HEval L4 设计直接受其约束）
