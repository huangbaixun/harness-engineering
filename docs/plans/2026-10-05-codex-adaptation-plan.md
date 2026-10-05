# Harness Engineering Codex Adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking. 推荐 Native：任务共享平台接口，由当前会话连续实现，最后独立审查。

**Goal:** 保留 Claude Code 支持，使自研 harness 在 Codex 中具备可靠的技能发现、初始化、会话恢复与验证，并在验收后接入 AIDC。

**Architecture:** 共享 skills/、features.json、ADR 和通用检查；平台适配层负责发现、初始化与 hook 协议。Claude 入口保留；Codex 入口显式指定独立 hook 文件，防止默认发现 Claude 的自动提交和 Issue 同步。上游技能正文仅应用 ADR-0009 允许的两处编辑。

**Tech Stack:** Python 3.10+ 标准库、Bash、Markdown/JSON、Codex CLI 0.158.0（当前核对版本）。本地测试不新增外部依赖、凭证或账号权限。

**Spec:** docs/specs/2026-10-05-codex-adaptation-design.md

## Global Constraints

- 原始本地基线6b5bec2；已核对远端main基线2b6bc0261901ed6ab5fc23ddf051e968d530843a。开始执行时重新核对，不自动接受未审阅的新提交。
- 不批量改写vendored SKILL.md；依ADR-0009通过sidecar和平台参考文件承载本地差异。
- 初始化必须可预览、幂等，已有AGENTS.md/CLAUDE.md/配置保留；冲突返回明确诊断。
- 新增项目默认离线：不自动提交、推送、创建/更新Issue、部署或写入用户全局配置。
- 启用hooks遵守原生信任审核，能力缺失时提供显式验证命令，不绕过权限。
- references → templates → skills → commands；新脚本不依赖命令文档。
- CLAUDE.md模板≤60行；模板占位符为{{PLACEHOLDER}}；操作型hooks成功时静默。SessionStart上下文是协议输出，需在能力矩阵标注此例外。
- 修改技能遵循CLAUDE.md的skill-creator with-skill/baseline评估要求；不将JSON结构检查替代行为评估。
- F006（共享/活文档归档）独立保留proposed，不纳入此次Codex适配；其历史归档积压亦不处理。
- AIDC保留原AGENTS.md、四栋/16 POD/1536计算柜、作用域隔离、道路消防、来源和规划声明；dist/是手写源代码。
- 本计划仅完成harness适配与AIDC接入，不包含多厂商GPU功能实现；之后恢复此前产品目标。

## Review Focus

1. 路径含空格和单引号：参数作为数组/Path传递，禁止将路径拼入python -c字符串（Task 2/3）。
2. 二次初始化或原项目已有规则：内容不丢失，无部分写入；冲突诊断可定位（Task 2）。
3. 畸形hook输入或未知工具：不误称已保护；阻断诊断明确，不记录原始敏感输入（Task 3）。
4. 无网络/未启用同步：启动和验证均不调用gh/git push，不依赖真实账号（Task 2/3/5）。
5. 项目技能与插件同时安装：选择单一路径，避免同名重复；能力与信任状态如实呈现（Task 2/5）。

---

### Task 1: 固定基线、平台ADR和可执行回归入口

**Files:** 新增scripts/validate.py、scripts/tests/test-validation.py、AGENTS.md、docs/decisions/0013-claude-codex-adapters.md；修改.github/workflows/validate.yml、docs/decisions/README.md、docs/architecture.md、features.json。

**Interfaces:** `python3 scripts/validate.py --structure-only`检查必需文件、JSON、技能结构和shell语法；不运行hooks、不调用网络。`python3 scripts/validate.py`再以子进程运行每个scripts/tests/test-*.sh及test-*.py；任何失败返回非零。

- [ ] **1. 固定开发分支。** 原仓库已有本次spec/plan未跟踪文件，先将这两份文档精确保存至临时备份；执行`git fetch origin main`核对SHA与设计一致，以`git switch -c codex/harness-adaptation 2b6bc0261901ed6ab5fc23ddf051e968d530843a`建分支，恢复两份文档。Git若因未跟踪文件冲突拒绝，停止覆盖，使用`git worktree add -b codex/harness-adaptation <隔离目录> <SHA>`。不reset、不改写main。
- [ ] **2. 写失败测试。** `scripts/tests/test-validation.py`用标准库unittest与临时fixture，至少包括：

```python
def test_missing_required_skill_is_reported(self):
    # fixture包含最小有效manifest、hooks和必需文档，但缺少using-harness。
    result = subprocess.run([sys.executable, str(VALIDATOR), '--structure-only',
                             '--root', str(self.fixture)], capture_output=True, text=True)
    self.assertNotEqual(result.returncode, 0)
    self.assertIn('skills/using-harness/SKILL.md', result.stderr)
    self.assertNotIn('skills/router/SKILL.md', result.stderr)
```

运行`python3 scripts/tests/test-validation.py`，记录因为验证入口缺失的失败；增加有效fixture成功、无效JSON失败、无网络子进程的测试。
- [ ] **3. 实现验证入口。** 用argparse解析`--root`、`--structure-only`；必需技能为using-harness/init/audit/evolve。json.load检查manifest和eval；subprocess.run(['bash','-n',path])检查shell；按路径排序运行测试，排除验证测试自身的递归调用。累计失败并返回1，成功返回0。CI调用该入口，删除router检查；不新增发布job。
- [ ] **4. ADR与跟踪。** 新ADR supersede ADR-0007的Claude-only限制；共享资源由平台入口读取，明确Codex不复用Claude默认hooks。AGENTS.md复述真实工程约束，CLAUDE.md保留。features.json追加F007，验收标准逐项复制spec的1–7，status保持proposed，执行开始后按生命周期转building；保留所有原字段和F006。不执行Issue同步。
- [ ] **5. 验证并提交。** `python3 scripts/validate.py`应结构检查成功且9个原shell测试通过；`git diff --check`。提交本任务文件及设计/计划，消息`feat(harness): establish dual-platform validation baseline`。

### Task 2: 幂等Codex项目初始化和独立插件入口

**Files:** 新增scripts/harness_init.py、scripts/tests/test-codex-init.py、docs/templates/codex/AGENTS.md.template、docs/templates/codex/harness.json.template、.codex-plugin/plugin.json、references/platforms/codex.md。

**Interfaces:** `python3 scripts/harness_init.py --tool codex --project PATH --dry-run`输出JSON清单但不写入；移除`--dry-run`执行。`--delivery project|plugin`默认project。已存在目标内容不一致退出2且全部目标不写；相同内容视为no-op。不支持的平台参数由argparse拒绝。

- [ ] **1. 写失败测试并运行。** 使用subprocess数组，临时目录包含空格和单引号。覆盖：

```python
def test_dry_run_does_not_create_files(self):
    result = self.init('--dry-run')
    self.assertEqual(result.returncode, 0)
    self.assertFalse((self.project / 'AGENTS.md').exists())

def test_existing_rules_are_never_overwritten(self):
    rules = self.project / 'AGENTS.md'
    rules.write_text('既有项目规则\n')
    result = self.init()
    self.assertEqual(result.returncode, 2)
    self.assertEqual(rules.read_text(), '既有项目规则\n')
    self.assertFalse((self.project / '.harness/config.json').exists())
```

再覆盖重复运行文件hash不变、project/plugin交付只启用一套技能、计划中的全部写入在冲突前先校验。运行`python3 scripts/tests/test-codex-init.py`记录RED。
- [ ] **2. 实现初始化。** `build_plan(project: Path, delivery: str) -> list[tuple[Path, bytes]]`渲染模板并返回写入清单；`apply_plan(plan, dry_run: bool) -> int`先校验所有冲突，再写入。路径相对project，不使用shell插值，不读用户全局配置。project交付复制skills及其完整资源到.agents/skills/harness-*，引用采用项目内相对路径；plugin交付不复制项目技能，只输出本地插件加载指南。
- [ ] **3. 定义配置。** `.harness/config.json`包含`schema_version:1`、`tool:codex`、`delivery`、`progress_file:docs/harness-progress.json`、`auto_commit:false`、`github_sync:false`、`verification_commands:[]`。初始化features.json使用已有generic模板，github默认关闭；绝不复制本框架仓库的github.repo配置。
- [ ] **4. 独立manifest。** 根据官方文档和本机CLI解析核对`.codex-plugin/plugin.json`，技能目录显式指向`./skills/`、hooks显式指向`./hooks/codex.json`；不得让Codex默认加载`hooks/hooks.json`。先创建空codex hooks配置，Task 3接线。平台参考文件列出CLI/App/未信任hooks三种模式。
- [ ] **5. 验证并提交。** `python3 scripts/tests/test-codex-init.py`、`python3 scripts/validate.py`、`git diff --check`；提交`feat(codex): add idempotent project and plugin entrypoints`。

### Task 3: Codex会话上下文与显式验证hooks

**Files:** 新增scripts/codex_hook.py、scripts/tests/test-codex-hooks.py、hooks/codex.json；必要时抽取scripts/harness_context.py。不改Claude的脚本三元组和事件注册。

**Interfaces:** `python3 scripts/codex_hook.py session-start|pre-tool|verify`。stdin为Codex事件JSON；项目根从事件cwd解析，插件根从脚本位置/PLUGIN_ROOT解析。SessionStart只向stdout输出官方协议JSON；操作成功静默。`verify --project PATH`也可人工运行，返回项目验证命令的真实状态。

- [ ] **1. 固定协议。** 阅读当前官方hooks说明并对照本机`codex --help`和本地插件解析能力，在references/platforms/codex.md记录实际支持事件、工具字段、输出结构和CLI版本。输入fixture仅含人工合成数据，绝不记录真实会话/凭证。
- [ ] **2. 写RED测试。** 覆盖根目录features优先、legacy进度回退、无进度文件、非法JSON、非对象JSON、未知工具、验证失败。

```python
def test_session_does_not_run_sync(self):
    result = self.event('session-start', {'cwd': str(self.project)})
    self.assertEqual(result.returncode, 0)
    payload = json.loads(result.stdout)
    self.assertEqual(payload['hookSpecificOutput']['hookEventName'], 'SessionStart')
    self.assertIn('F007', payload['hookSpecificOutput']['additionalContext'])
    self.assertFalse(self.gh_call_log.exists())

def test_verify_returns_failed_command_status(self):
    self.config['verification_commands'] = [[sys.executable, '-c', 'raise SystemExit(3)']]
    self.save_config()
    result = self.verify()
    self.assertNotEqual(result.returncode, 0)
```

输入/输出字段须先由第1步文档核对；若本机不支持对应事件，测试不伪造可用性，保持人工入口并报告差异。运行`python3 scripts/tests/test-codex-hooks.py`记录RED。
- [ ] **3. 实现上下文。** `render_context(project: Path) -> str`读根features（docs/features为legacy回退），优先harness-progress，缺失时读claude-progress。不自动迁移、不覆盖旧进度。读取失败给明确短诊断，不回显原始JSON。仅提示规划/归档，不改变feature状态。
- [ ] **4. 实现验证。** `run_verification(project: Path, commands: list[list[str]]) -> int`只接受非空字符串数组，subprocess.run(cmd,cwd=project)，不shell=True。空列表返回明确“未配置”错误，不宣称通过。Stop按官方协议反馈失败；无无限自动重试。
- [ ] **5. 接线与保护边界。** Codex只注册已核对的session/验证hooks。PreTool输入中的exec_command/apply_patch分别识别命令及补丁路径；无法可靠解析时不给“已保护”结论，不绕过原生审批。若实现PreTool阻断则测试`.env`修改、目录穿越及多文件补丁；若当前接口无法可靠拦截，保持未注册并在矩阵写明，仅提供原生权限加显式验证。两种情况都不复用Claude Bash|Edit|Write matcher冒充兼容。
- [ ] **6. 验证并提交。** `python3 scripts/tests/test-codex-hooks.py`、`python3 scripts/validate.py`、`git diff --check`；提交`feat(codex): adapt session and verification lifecycle`。

### Task 4: Superpowers差异协调和技能行为评估

**Files:** 修改scripts/sync-superpowers.sh及skills/*/harness-delta.md、UPSTREAM.md、必要的harness-original SKILL.md与evals；新增scripts/tests/test-superpowers-sync.py、docs/evals/2026-10-05-codex-adaptation-report.md。vendored正文和companions仅按上游来源同步。

**Interfaces:** sync-superpowers.sh保持只读；`CACHE_BASE`显式覆盖优先；否则识别Claude/Codex两个缓存，按数值版本排序，报告选中的版本和路径。输出包含正文、新增/缺失/改变的companion差异；没有缓存非零退出并说明。

- [ ] **1. 写RED测试。** 在临时fixture构造6.3.0、6.4.1、6.10.0目录，确保选择6.10.0，显式CACHE_BASE优先，目录带空格可用，运行前后文件hash相同。

```python
def test_sync_never_modifies_vendor_files(self):
    before = self.hash_tree(self.vendor)
    result = self.run_sync()
    self.assertEqual(result.returncode, 0)
    self.assertEqual(before, self.hash_tree(self.vendor))
    self.assertIn('6.10.0', result.stdout)
```

运行`python3 scripts/tests/test-superpowers-sync.py`记录RED。
- [ ] **2. 改进同步发现。** 用Python标准库数值tuple排序替代依赖平台的sort -V，目录遍历用Path；保留比较行为及两处编辑豁免，不忽略正文中的其他差异。取最新稳定候选时核对release/tag和SHA，不用浮动HEAD当固定来源。
- [ ] **3. 逐技能协调。** 对13个vendored技能列出差异、影响和“更新/保留”决定。接受版本必须取得完整同SHA正文及companions，应用`name: harness:<name>`和sidecar pointer，更新UPSTREAM.md；若未取得可靠来源或eval失败，保留6.3.0并给明确理由。不得把“已看到6.4.2标签”写成“已升级6.4.2”。
- [ ] **4. 平台规则与skill-creator。** 先读取适用skill-creator；为init/using-harness和修改过的sidecar/eval准备真实场景：已有AGENTS规则、Codex不支持的工具、断网验证、两个入口重复、用户明确执行范围。按相同prompt运行with-skill和baseline，保留实际结果、评分与供人工审阅的viewer；评估报告不可捏造独立运行。引入中性进度时仅兼容说明，不顺便实现F006归档改造。
- [ ] **5. 验证并提交。** `python3 scripts/tests/test-superpowers-sync.py`、`python3 scripts/validate.py`、结构/正文来源检查；评估结果注明人工审阅状态。提交`feat(harness): reconcile platform skills and upstream provenance`。

### Task 5: 双端冒烟、独立审查与AIDC接入

**Files:** 更新README.md、README.zh-CN.md、docs/architecture.md、CHANGELOG.md、features.json；新增docs/evals/2026-10-05-platform-smoke.md。AIDC仅增加项目内技能和.harness/config.json及必要的规则补充。

**Interfaces:** 外部接入复用Task 2 `--dry-run`，已有AGENTS.md冲突不得覆盖，采用显式受管理追加段并审查diff；GitHub同步与自动提交关闭。AIDC验证命令精确为`[["npm","run","check"],["npm","test"]]`。

- [ ] **1. 写验收测试。** 临时项目初始化后检查配置及skills资源可发现，禁用网络的gh/git stub若调用即失败；已有规则hash保持。测试项目同时发现插件和项目入口时给出重复提示，安装文档明确择一。

```python
def test_default_workflow_has_no_external_side_effects(self):
    result = self.run_session_with_forbidden_network_stubs()
    self.assertEqual(result.returncode, 0)
    self.assertFalse(self.side_effect_log.exists())
    self.assertEqual(self.rules_before, self.read_existing_rules())
```

运行所归属的init/hooks测试并记录新用例RED，按行为补齐实现。
- [ ] **2. 真实CLI冒烟。** 使用隔离项目和用户当前已授权登录，核对Codex加载结果，运行代表性规划/TDD/验证/归档场景；不得新增API key、绕过hook信任或修改全局配置。Claude可用时运行同等场景；不可用则报告仅完成结构回归，不能宣称双端端到端通过。App若未实际加载，仅记录未验证。
- [ ] **3. 独立审查。** 按已选执行技能请求fresh-context审查，覆盖真实规则保留、未知工具降级、网络副作用、重复发现、命令失败传播和vendor来源。重要问题用RED→GREEN修复，全套回归再次运行；无推送/合并。
- [ ] **4. 接入AIDC。** 先预览；既有AGENTS规则完整保留，项目级技能择一注册。接入无源码变更时仍执行`npm run check`和`npm test`；`npm run dev`浏览器验证园区→POD→R096→设备→返回、POD状态隔离及移动端入口，记录范围。没有真实GPU画面证据时如实标注未验证，不以静态测试替代。
- [ ] **5. 完成证据。** `python3 scripts/validate.py`、`git diff --check`及AIDC两条命令输出归档。F007仅在spec验收满足后转done；未通过的能力明确保留building。文档给出安装、卸载、legacy回退和信任审核方式。提交`docs(harness): record Codex compatibility and project adoption`，交付diff及验证结果。原仓库与AIDC分别报告；不自动合并main、推送或发布。

## 验收覆盖自查

| Spec验收 | 任务 | 证据 |
|---|---|---|
| 1 双端ADR/矩阵/manifest | 1、2、5 | ADR、结构测试、真实加载记录 |
| 2 技能与核心工作流 | 2、4、5 | 发现测试、行为评估、CLI冒烟 |
| 3 失败和异常输入 | 2、3 | conflict、路径、非法JSON、验证失败测试 |
| 4 离线与权限边界 | 2、3、5 | forbidden-stub日志、规则hash及信任记录 |
| 5 CI和原9测试 | 1、5 | validate.py完整输出 |
| 6 skill-creator评估 | 4 | baseline/with-skill实际记录与viewer |
| 7 隔离冒烟再AIDC | 5 | 双仓库验证及浏览器记录 |

## 执行交接

设计已获用户确认。计划尚待审阅；推荐Native连续执行并在末尾独立审查，因为初始化、hook和manifest紧密共享接口。用户选择Subagent-driven时切换对应执行技能；未选方法前不开始产品实现。
