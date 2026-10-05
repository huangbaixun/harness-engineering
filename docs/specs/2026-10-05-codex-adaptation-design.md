---
date: 2026-10-05
topic: codex-adaptation
type: exploration
status: proposed
---

# Harness Engineering：Codex 适配与更新设计

## 目的与基线

先使自研 harness 可在 Codex 中可靠运行，再以它开发厂商中立的 AIDC 规划数字孪生。保留 Claude Code 支持、features.json 生命周期、ADR、测试先行、验证与归档。原始本地仓库基线为 6b5bec2；核对到的远端 main 为 2b6bc0261901ed6ab5fc23ddf051e968d530843a，相差21提交。工作区干净；当前远端 vendored Superpowers 为6.3.0，本机另有6.4.1，已确认远端存在6.4.2标签；不据此将任一版本宣称为最新稳定版。

## 现状证据

- ADR-0007限制Claude Code并删除AGENTS.md通用入口，新增Codex支持须新ADR supersede此限制。
- 初始化和进度恢复使用CLAUDE.md、.claude目录、docs/claude-progress.json。
- hooks/hooks.json含自动进度提交及Issue同步；目标AIDC项目不允许因初始化自动扩大权限或引入发布流程。
- validate.yml要求skills/router/SKILL.md，该路径不存在；架构文档亦引用不存在的self-test.sh、generate-harness.sh。
- 远端最新副本9个scripts/tests/test-*.sh均通过（stub测试），未验证完整CI、真实Issue同步或Codex运行。
- 本机Codex CLI 0.158.0；官方文档支持.agents/skills、插件及需要审核信任的hooks。CLI/App能力分别验证，不推断跨端一致。

## 方案比较与选择

1. 推荐：共享框架核心，薄Claude/Codex适配层。清晰标注各端能力，保持现有用户兼容。
2. 独立Codex分叉：起步简单但双份维护易漂移，放弃。
3. 直接替换成Superpowers：丢失自研生命周期和归档能力，不采用。

## 架构与行为

共享层包含features.json、规划/规格/ADR、验证、归档和通用脚本。工具适配层负责技能发现、会话上下文、hook输入输出协议、工具名映射和进度文件位置。不批量改写vendored SKILL.md；依ADR-0009通过sidecar和平台参考文件承载本地差异。

Codex先提供可验证的项目级入口AGENTS.md与.agents/skills及插件分发入口；采用当前官方支持的manifest格式，并以本机CLI解析行为确认兼容性。避免同一技能在项目和插件内重复注册。Claude原入口继续工作。

初始化必须可预览、幂等，已有AGENTS.md/CLAUDE.md/配置保留；冲突返回明确诊断。进度协议使用中性字段，读取旧claude-progress.json时提供兼容迁移，不静默删除旧文件。

Codex hooks按真实事件与工具输入结构适配。提示性工作流与确定性检查分开标明；不把AGENTS.md提示当作可执行拦截。启用hooks遵守原生信任审核，能力缺失时提供显式验证命令，不绕过权限。

新增项目默认离线：不自动提交、推送、创建/更新Issue、部署或写入用户全局配置。原Claude项目已启用的行为保留，以显式配置控制。AIDC项目接入仅增加必要的本地开发工作流，保留既有AGENTS.md及零依赖检查命令。

Superpowers更新先核对版本与SHA、逐技能及companion差异；记录UPSTREAM.md来源、维护harness-delta和对应eval。同步脚本识别Claude及Codex缓存，保持只读差异报告。未经评估不批量升级。

## 验收

1. 新ADR、能力矩阵、文档与manifest准确反映双端支持，不声称不支持的自动化。
2. Codex发现技能；代表性规划、TDD、验证及归档工作流运行；Claude结构和回归仍通过。
3. hook有效/畸形输入、路径含空格、未知工具、失败命令、重复初始化和非受信hook均有测试。
4. 未启用同步时零网络；已有项目配置不被覆盖；无隐式提交、发布或扩大权限。
5. CI结构检查修复并纳入9个已有测试脚本及新增适配测试。
6. 修改技能依CLAUDE.md执行skill-creator评估，包含with-skill/baseline证据与供人工审阅的结果；不可将JSON结构检查当作行为评估。
7. 在隔离样例项目完成Codex本地冒烟后，再接入AIDC；接入后执行npm run check、npm test，并在开发浏览器中验证交互。

## 顺序与边界

先更新到核对的远端基线并建立开发分支，再修复验证入口、实现平台适配、评估并协调上游技能差异、运行双端回归，最后接入AIDC。本设计不包含GPU设备功能开发；该开发在harness验收后恢复。框架改动在独立副本中开发，完成后供审阅；合并、推送及全局安装分别处理。

## 官方依据

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/hooks
- https://developers.openai.com/plugins/build/plugins

## 待审阅

此文件是拟议设计，尚未开始产品实现。设计审阅后生成逐任务实施计划并选择执行方式，遵循Superpowers设计/计划门槛。
