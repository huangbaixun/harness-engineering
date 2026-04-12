# Changelog

## v1.10.0 (2026-04-12)

**统一 `harness:` 命名空间**

- **Plugin name 简化**：`harness-engineering` → `harness`，用户看到 `harness:init` 而非 `harness-engineering:harness-init`
- **Skills 重命名**：harness-init → init, harness-audit → audit, harness-evolve → evolve, using-harness → router, writing-plans → plan, verification → verify（tdd 保持不变）
- **Commands 重命名**：统一 `动词-名词` 格式：arch-scan → scan-arch, entropy-scan → scan-entropy, assign-features → assign, context-dump → dump, doc-sync → sync-docs, trim-claudemd → trim
- **全量引用更新**：所有 SKILL.md 交叉引用、eval JSON、architecture.md、marketplace 文档、README、CONTRIBUTING 等 36+ 文件同步更新
- **向后兼容说明**：旧版 slash commands（`/harness-init` 等）已不再生效，需改用 `/harness:init` 等新名称

## v1.9.3 (2026-04-12)

**跨平台 Hook + 上游版本追踪**

- **跨平台 Polyglot Hook 包装器**（借鉴 obra/superpowers `polyglot-hooks` 方案）：
  - 每个 hook 脚本新增 `.cmd` polyglot 入口（CMD + bash 双有效），Windows Git Bash 环境自动识别
  - `hooks.json` 注册入口从 `.sh` 改为 `.cmd`
  - 保留 `.sh` 文件向后兼容，新增无后缀 bash 逻辑文件（`.cmd` 委托给它）
  - Windows 下找不到 bash 时静默成功（exit 0），不阻塞工作流
- **上游版本追踪**：三个工作流 Skill（writing-plans / tdd / verification）头部新增 `upstream` + `harness-delta` 元信息，锁定上游 obra/superpowers @ `917e5f5`，明确每个 Skill 相对上游的差异点
- 更新 README：scripts 目录说明、跨平台兼容性表格

## v1.9.2 (2026-04-11)

**Superpowers 工作流整合**

- 新增 `skills/writing-plans/`：实现前规划 Skill，>30 分钟或涉及 3+ 文件时触发，输出 tasks.md，含人工确认门禁
- 新增 `skills/tdd/`：TDD 工作流 Skill（RED→GREEN→REFACTOR），与 1% 规则绑定，任何代码编写自动触发
- 新增 `skills/verification/`：完成前验证 Skill，四层检查（Functional / Quality / Architecture / Integration）
- 新增 `scripts/session-start.sh`：SessionStart Hook，会话开启时自动读取 `claude-progress.json`，展示 in_progress 任务、待办数、阻塞项；已完成 ≥10 条时触发归档提醒
- 更新 `hooks/hooks.json`：新增 `SessionStart` 事件注册
- 更新 `skills/using-harness/SKILL.md`：新增 Steps 4-6，写明 writing-plans / tdd / verification 触发条件
- 更新 `skills/harness-init/SKILL.md`：初始化产物表和文件结构图新增三个 Skill 和 session-start.sh
- 更新 `docs/templates/generic/CLAUDE.md.template`：新增「工作流 Skill 自动触发」说明段
- 更新 `references/HarnessEngineering.md`：新增 Section L（Superpowers 整合），含对比表、集成点、执行链全图、14 Skills 映射；参考表新增 obra/superpowers 等三条 ★★ 条目

## v1.9.1 (2026-04-10)

**harness-init Phase 5 完善：归档机制 + features.json 分层策略**

- `features.json` 定位调整：从「长周期可选」改为「单人可选 / 多人或多 Agent 必须」，初始化时按团队规模自动判断是否生成
- 新增两文件职责对比表（谁写 / 记什么 / token 增长趋势 / 多 Agent 冲突风险）
- 多人/多 Agent 场景补充扩展字段说明（`owner`、`depends_on`、`files_owned`、`worktree`、`acceptance`）
- **新增归档机制**：`completed_features` 超 10 条触发归档，防止 6 个月后 token 膨胀至 ~8000；初始化时同时生成 `docs/archive/` 目录骨架和归档策略 README
- 三条归档规则写入 AGENTS.md（归档阈值 / done 条目压缩策略 / Agent 读取范围限制）
- 新增 `docs/templates/generic/archive-readme.md.template`

## v1.9.0 (2026-04-10)

**Claude Marketplace 支持（方案 B）**

- **marketplace.json**：新增 `.claude-plugin/marketplace.json`，支持社区 marketplace 订阅分发。用户可通过以下命令一键订阅并获得自动更新：
  ```
  /plugin marketplace add https://raw.githubusercontent.com/huangbaixun/harness-engineering/main/.claude-plugin/marketplace.json
  ```
- **plugin.json 完善**：补充 `homepage`、`repository` 字段（官方 marketplace 提交必需）；新增 `userConfig`（`team_name`、`default_tech_stack`），启用时由 Claude Code 提示用户填写，无需手动配置
- **${CLAUDE_PLUGIN_ROOT} 路径修复**：`harness-init` 中所有 plugin 内部路径引用（模板目录、init.sh.template）统一改用 `${CLAUDE_PLUGIN_ROOT}` 前缀，确保 marketplace 缓存模式下路径正确解析
- **初始化产物表修复**：`.claude/hooks/` 路径统一改为 `$TOOL_DIR/hooks/`，与工具无关架构保持一致
- **关键词扩充**：`plugin.json` keywords 新增 `codebuddy`、`team`、`sprint`，提升 marketplace 搜索可发现性

## v1.8.0 (2026-04-08)

**工具无关架构 — 全面兼容 CodeBuddy**

- **AGENTS.md 作为跨工具通用记忆文件**（ADR 0005）：
  - 新增 `AGENTS.md`：统一记忆文件，所有项目规则的唯一真相来源，Claude Code 和 CodeBuddy 均可读取
  - `CLAUDE.md` 缩减为 2 行 wrapper，引导 Claude Code 用户至 `AGENTS.md`
  - 新增 `CODEBUDDY.md`：2 行 wrapper，引导 CodeBuddy 用户至 `AGENTS.md`
- **工具路径去硬编码**：
  - 新增 `.codebuddy-plugin/plugin.json`：CodeBuddy plugin 清单（v1.8.0）
  - `harness-init` Phase 2 六层表格改用 `$TOOL_DIR` 变量，不再硬编码 `.claude/`
  - `harness-init` Phase 3 文件结构图更新，展示双工具兼容布局及 `AGENTS.md` 层级
  - `harness-audit` SKILL.md 工具检测逻辑和记忆文件诊断已适配多工具（v1.8.0 前已合并）
- **模板更新**：
  - 新增 `docs/templates/generic/AGENTS.md.template`：包含 `$TOOL_DIR` 无硬编码约定
  - `docs/templates/generic/init.sh.template` 新增 10 行工具检测块，自动检测 CodeBuddy / Claude Code 并导出 `$TOOL_DIR` 和 `$TOOL_NAME`
- **ADR 0005**：记录工具无关架构决策，含三种方案对比和 Agent 约束规则
- **docs/architecture.md** 更新：反映双工具兼容结构，目录图含 `.codebuddy-plugin/`、`CODEBUDDY.md`、`AGENTS.md` 及 `references/team-parallel-development.md`

## v1.7.0 (2026-04-06)

**多人协作 + features.json 生命周期完善**

- 新增 `/assign-features` 命令：Sprint feature 分配规划器，参照 superpowers `writing-plans` 风格，五阶段工作流——
  - Phase 1：分析 features.json 依赖图，计算 `startable`（依赖是否全 done）与 `criticality`（传递闭包 blocks 数）
  - Phase 2：自动读取 CLAUDE.md `## 团队成员` 章节，缺失时询问并写回
  - Phase 3：四规则分配算法（文件冲突检测 / 负载上限保护 / 关键路径优先 / layer 亲和性）
  - Phase 4：生成 `sprint-kickoff.sh`，每人独立 section，含 git 认领 + worktree + Agent 启动全套命令
  - Phase 5：分配记录追加到 `claude-progress.json` `sprint_history`，可追溯
- 新增 `commands/evals/evals.json`：4 个命令测试用例（标准3人Sprint、文件冲突检测、依赖解锁调度、负载过高防护）
- 新增 `references/team-parallel-development.md`：多人全栈团队并行开发指南，综合 Anthropic Agent Teams 官方文档、OpenAI Codex 团队实践、C 编译器16-Agent 并行压测案例，涵盖 features.json 并行字段升级、Git Worktree 隔离配置、三种分工模型、减少人与 Agent 依赖的设计原则
- `harness-init` Phase 5 补充 features.json 使用规则：明确「Agent 只读原则」和「取消不删原则」（status=cancelled + cancelled_reason，永不删除条目）

## v1.6.0 (2026-04-06)

**方法论深化 + Skill TDD 完善**

- 新增 `references/HarnessEngineering.md`：综合 Anthropic · OpenAI · InfoQ · Hacker News 实践精华的完整方法论手册，作为 plugin 设计的一手来源
- `harness-init` 新增 **Phase 0 存量检测**：初始化前先扫描 CLAUDE.md 是否已存在，区分全新项目 / 存量项目 / 损坏文件三条路径；存量模式提供「增量补充 / 优化整合 / 完整重建」三种处理方式，执行前强制备份为 `.bak`
- `harness-init` 新增**初始化产物宣言**：Skill 开头即列出所有产物文件，用户在触发前就知道会生成什么
- 新增 `docs/templates/generic/init.sh.template`：会话启动脚本模板，每次新 Claude Code 会话前运行，输出进度/特性清单/架构文档入口（借鉴 walkinglabs/learn-harness-engineering harness-creator 模式）
- **Evals 重组**：从单文件拆分为 per-skill 目录，转为 skill-creator 兼容格式（含 `assertions[]` 数组，可被 grader subagent 客观评分）
  - `skills/harness-init/evals/evals.json`（3 evals，含新增存量检测用例）
  - `skills/harness-audit/evals/evals.json`（1 eval）
  - `skills/harness-evolve/evals/evals.json`（1 eval）
  - `skills/using-harness/evals/evals.json`（2 evals）
  - `evals/agents/coding-agent.json`（3 evals）
  - `evals/evals.json` 改为索引文件
- `README.md` 新增「方法论参考」区块，快速上手第二步后加产物预览表格
- `CLAUDE.md` 新增方法论手册引用链接

## v1.5.1 (2026-04-05)

- 修复：release.yml 版本校验与 tag 匹配（初始发布修正）

## v1.5.0 (2026-04-05)

**开源化调整**

- 新增 `LICENSE`（MIT）
- 新增 `CONTRIBUTING.md`：Skill TDD 贡献流程、语言模板贡献规范、Hook 脚本约定、PR 格式
- 重写 `README.md`：面向首次使用者，3 步快速上手、badge、文件清单折叠
- 新增 `.github/workflows/release.yml`：打 semver tag 时自动打包 `.skill` 并创建 GitHub Release，含 manifest 版本校验
- 新增 `.github/workflows/validate.yml`：PR 时自动校验 plugin 结构、manifest、hooks.json、eval 格式
- 新增 `.github/ISSUE_TEMPLATE/`：bug_report、feature_request 模板
- 新增 `.github/PULL_REQUEST_TEMPLATE.md`：含 Skill TDD 检查清单

## v1.4.1 (2026-04-05)

- **修复**：移除 `plugin.json` 中的路径声明字段，解决「`agents: Invalid input`」加载错误
- 依赖 Claude Code 自动发现默认目录，只保留 metadata 字段

## v1.4.0 (2026-04-05)

- **结构修复**：符合 Claude Code 官方 plugin 规范
  - manifest 移至 `.claude-plugin/plugin.json`
  - `commands/`, `agents/`, `skills/` 移到插件根目录
  - hooks 改为 `hooks/hooks.json` JSON 注册格式
  - hook 脚本迁移至 `scripts/`，使用 `${CLAUDE_PLUGIN_ROOT}` 路径变量
  - `author` 字段改为 object 格式

## v1.3.0 (2026-04-05)

- 新增 `using-harness` 元 Skill（强制意图识别触发，参考 obra/superpowers 1% 规则）
- evals 扩充至 9 个用例，新增 6 个压力测试
- `coding-agent` 内嵌两阶段强制 Review（Spec Compliance → Code Quality）

## v1.2.0 (2026-04-05)

- 新增 `coding-agent`（Sonnet 模型，长周期多会话编码，手册 F.4 节）
- 新增 Java 语言栈模板（JUnit 5 + Mockito + Checkstyle + SpotBugs）
- 语言模板扩展至五种

## v1.1.0 (2026-04-05)

- 新增 `explore-agent`（Haiku 模型，上下文高效探索 Subagent）
- 新增 `code-review-agent`（Sonnet 模型，代码质量 Inferential Sensor）
- 新增 `/entropy-scan` 命令（第四类垃圾回收：代码熵增检测）
- 新增 `plugin.json` 版本清单

## v1.0.0 (2026-04-04)

- 初始发布：三大 Skills + 七个 Commands + 五个 Hooks + 多语言模板 + `security-reviewer`
