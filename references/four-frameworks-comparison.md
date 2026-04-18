# 四大 Claude Code 框架对比与 harness-engineering 借鉴建议

## 一、单独画像

### OpenSpec（Fission-AI）—— 活规格引擎

核心主张："规格作为活文档，而不是一次性提示。"工作流 `/opsx:propose → /opsx:apply → /opsx:archive`，新建需求时自动产出 `openspec/changes/<feature>/` 目录下的 proposal.md（为什么）、specs/（要求与场景）、design.md（技术方案）、tasks.md（实现清单）。完工的改动 `archive` 到带时间戳的归档目录，规格留存作为未来参考。哲学是"fluid not rigid → iterative not waterfall"，任何 artifact 随时可改，无硬性阶段门禁。

优势：可追溯性最强；天然适合多人协作和跨 session 交接；归档机制避免 chat history 膨胀。
弱点：本身不管 TDD、不管并行、不管质量门禁；需要配合其他框架才完整；对小改动略重。

### GSD / Get Shit Done（glittercowboy / TACHES）—— 上下文抗腐蚀引擎

核心主张："解决 context rot。"把项目拆成 wave（波次），独立 plan 并行、依赖 plan 串行，每个 plan 在一个全新的 200K token context 的 subagent 里跑，提交后 context 丢弃。持久化 4 个核心文档 PROJECT.md / REQUIREMENTS.md / ROADMAP.md / STATE.md 加每阶段的 CONTEXT.md / PLAN.md / SUMMARY.md / VERIFICATION.md。6 步流程：new-project → discuss-phase → plan-phase → execute-phase → verify-work → ship。每个 plan 是 XML 结构，含 `<action>` `<verify>` `<done>` 三段。

优势：长周期项目质量最稳定（fresh context 不退化）；并行加速明显；内置 schema drift 检测、安全锚点、scope 收缩检测等质量门禁。
弱点：对小项目过度工程；文档量大；波次调度需要依赖图正确性。

### gstack（Garry Tan / YC）—— 角色拟人化团队

核心主张："让单个 AI 变成一支虚拟团队。"23-30 个斜杠命令按角色组织：CEO（/office-hours、/plan-ceo-review 做产品 scope 挑战）、Designer（/design-consultation、/design-shotgun 多方案、/design-html、/design-review）、Eng Manager（/plan-eng-review、/autoplan 一键全评审）、QA（/qa 真 Chromium 浏览器 + 原子 commit、/browse 让 agent 有"眼睛"）、Release Manager（/ship、/land-and-deploy、/canary 灰度监测、/benchmark 性能回归）、Safety（/careful、/freeze、/guard 三层破坏性动作拦截）、Utilities（/investigate、/learn、/retro、/codex 交叉模型 review）。

优势：真浏览器端到端验证在同类中独一份；角色视角多样，暴露盲区；safety wrappers 设计精巧；/canary + /benchmark 覆盖生产阶段。
弱点：不是 spec-driven，计划层弱；skill 间缺乏严格 pipeline；偏前端/产品型项目，后端基础设施项目收益低。

### Superpowers（obra / Jesse Vincent）—— 五段式 TDD 方法论

核心主张："强制 Claude 走五段路径 clarify → design → plan → code → verify，并以 TDD 为硬规则。"15 个 composable skill：brainstorming、writing-plans、dispatching-parallel-agents、using-git-worktrees、test-driven-development、systematic-debugging、executing-plans、subagent-driven-development、requesting-code-review、receiving-code-review、verification-before-completion、finishing-a-development-branch、writing-skills、using-superpowers。强调"即便 1% 相关也要调用 skill"；明确区分 rigid skill（TDD / debug，必须照做）和 flexible skill（模式，可酌情）。

优势：方法论最清晰、TDD 执行最严格；skill 原子化易复用；写 skill 的 skill 支持自我扩展；已进入 Anthropic 官方 marketplace。
弱点：没有活规格归档；并行是能力不是默认；缺少生产阶段（canary、benchmark）；不管产品级 scope 挑战。

## 二、四者能力矩阵

| 能力维度 | OpenSpec | GSD | gstack | Superpowers |
|---------|----------|-----|--------|-------------|
| 规格归档 | ★★★★★ | ★★★ | ★ | ★ |
| 长周期抗 context rot | ★★★ | ★★★★★ | ★★ | ★★★ |
| TDD 严格度 | ★ | ★★★ | ★★ | ★★★★★ |
| 并行执行 | ★ | ★★★★★ | ★★ | ★★★ |
| 产品/scope 挑战 | ★★ | ★★ | ★★★★★ | ★★ |
| 真浏览器 E2E | - | - | ★★★★★ | - |
| 破坏性动作防护 | - | ★ | ★★★★ | ★ |
| 生产发布与监测 | ★★ | ★★ | ★★★★★ | ★★★ |
| 方法论纯度 | ★★★★ | ★★★★ | ★★ | ★★★★★ |

## 三、本项目（harness-engineering v1.10.0）可借鉴建议

当前已经 fork 了 superpowers 并建立了 `harness:init / plan / tdd / verify / audit` 命名空间、features.json、三智能体 GAN 架构、PreToolUse/Stop Hook 体系。下面按借鉴来源 → 对接阶段 → 要解决的问题组织。

### 1. 借 OpenSpec 的"活规格归档" → 增强 `harness:plan` + 新增 `harness:archive`

在 `harness:plan` 生成 features.json 的同时，额外产出目录 `.harness/changes/<feature>/{proposal.md, design.md, tasks.md}`；完工后 `harness:archive` 把整个目录移入 `.harness/archive/YYYY-MM-DD-<feature>/`。解决：当前 features.json 完成后即终结，设计决策和"为什么这样做"散落在 git commit 里难以检索；归档机制给未来审计和人员交接提供单一事实源，对应 HarnessEngineering.md 中"防止文档陈旧和架构漂移"的垃圾回收原则。

### 2. 借 GSD 的"Wave 并行 + Fresh Context" → 增强 `harness:tdd`

把 features.json 里互相独立的 feature 分析依赖图，独立的 feature 分派到独立 subagent（每个 200K fresh context）并行跑 Red-Green-Refactor，依赖的串行。为每个 feature 落盘 `{N}-SUMMARY.md` + `{N}-VERIFICATION.md`。解决：长周期项目中主线程 context 膨胀导致后期质量退化——这是当前 three-engineers-5-months-1M-LOC 这类 OpenAI Codex 式规模最大的风险。Hashimoto 的"永不再犯"+ GSD 的"永不污染 context"是 Harness Engineering 的两条互补底线。

### 3. 借 GSD 的 XML 结构化 plan → 规范 features.json 单个 feature 的描述

每个 feature 在 features.json 里增加 `action / verify / done` 三段式声明（或链接到外部 plan.md）。解决：当前 features.json 是声明式的"做什么"，但"怎么验证完成"和"完成的证据"是隐式的，Evaluator agent 判断完成度时缺乏统一契约。

### 4. 借 gstack 的"安全 Hook 包装" → 增强 settings.json / PreToolUse Hook

吸收 `/careful`（破坏性命令前确认 rm -rf、DROP TABLE、force-push）、`/freeze`（调试期限制编辑到单一目录）、`/guard`（两者合并）作为三级 Hook 开关。解决：当前 PreToolUse 只阻止写 .env，对"agent 在 debug 过程中漫游到无关目录改坏东西"缺乏防护——这是 HN 讨论中 Harness Engineering 最常被提到的事故场景。

### 5. 借 gstack 的"真浏览器 QA" → 新增 `harness:e2e` 或作为 `harness:verify` 的子命令

对 Web 项目引入 Chromium 自动化（Playwright 或 CDP）作为四层完成度检查的第五层：Lint → 单测 → 集成测 → 评审 → 真浏览器。解决：Evaluator agent 目前在代码和测试层面判断完成度，但用户侧体验（首屏 LCP、交互报错、可访问性）看不见，相当于只验证了"代码对"但没验证"产品对"。

### 6. 借 gstack 的 `/canary` + `/benchmark` → 新增 `harness:canary`

发版后 N 分钟内监测 console 错误、性能回归、核心 Web Vitals，和 baseline 对比，超阈值触发 rollback 或 issue。解决：Harness Engineering 当前覆盖到 `harness:verify` 为止，发布后的"第一线证据"没闭环，等于反馈循环缺了最后一段。

### 7. 借 gstack 的 `/codex`（交叉模型评审） → 增强 `harness:audit`

在 Evaluator 智能体内嵌第二模型（Codex 或 Opus→Sonnet 交叉）作为独立评审眼，三模式：review gate / adversarial challenge / consultation。解决：单一模型家族容易产生同源盲区，符合 Anthropic"永远不要让创建者独立评审自己的产出"原则的更强版本。

### 8. 借 Superpowers 的"rigid vs flexible"标签 → 给 .harness/skills/*/SKILL.md 加 metadata

在每个 Skill 的 frontmatter 加 `execution: rigid | flexible` 字段，TDD 和 debug 标 rigid，架构建议类标 flexible。解决：当前所有 skill 在触发逻辑上地位平等，但 Claude Code 对"可协商"和"不可协商"规则缺少显式区分，导致 rigid 约束被当作 suggestion 忽略——这正是 TDD Guard 存在的原因。

### 9. 借 Superpowers 的 `dispatching-parallel-agents` skill → 独立抽离到 `.harness/skills/dispatch`

当前 features.json 的并行是隐式的，显式化成一个可复用 skill，让其他 harness:* 命令（比如 audit、archive）也能并行化。解决：并行能力目前和 tdd 流程耦合，迁移到其他阶段需要重新造轮子。

### 10. 借 GSD 的 STATE.md → 增强你现有的 claude-progress.json

STATE.md 以人类可读 markdown 记录当前进展、阻塞点、下一步决策，和机器可读的 claude-progress.json 互补。SessionStart Hook 同时恢复二者。解决：当前进度恢复只给 agent 用，人类看不懂；STATE.md 让早班同事或跨机器切换的作者能在 10 秒内 get back on track。

## 四、优先级推荐

按 ROI 排序，建议分三批落地：

**P0（立刻做，收益最高）**：借鉴 3（XML 三段式 feature）、8（rigid/flexible 标签）、10（STATE.md）——改动小，方法论收益大，和现有体系完全兼容。

**P1（下一个 minor 版本）**：借鉴 1（活规格归档 `harness:archive`）、4（safety Hook 三级开关）、6（`harness:canary` 发布监测）——补齐 "plan→verify" 之外的上下游缺口。

**P2（架构级迭代）**：借鉴 2（Wave 并行 fresh context）、5（真浏览器 E2E）、7（交叉模型 audit）——需要重构或引入新依赖，但能让项目从"个人最佳实践"升级到"团队级基础设施"。

## Sources

* Fission-AI/OpenSpec on GitHub
* Spec-Driven Development with OpenSpec and Claude Code
* gsd-build/get-shit-done on GitHub
* The Complete Beginner's Guide to GSD Framework
* GSD Framework on CC for Everyone
* garrytan/gstack on GitHub
* gstack skills documentation
* obra/superpowers on GitHub
* Superpowers, GSD, and gstack: What Each Claude Code Framework Actually Constrains
* Claude Code + OpenSpec + Superpowers: When to Use All Three
* A Claude Code Skills Stack: Combining Superpowers, gstack, and GSD
