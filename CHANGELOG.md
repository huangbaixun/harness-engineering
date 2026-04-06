# Changelog

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
