# Mini 留言板 — With Harness 分支

> 培训演示中"装上 harness-engineering"路径用的项目。业务代码与 `board-baseline/` 完全相同，唯一区别是有 CLAUDE.md / .claude/ / docs/decisions/ 配置。

## 运行

```bash
bash setup.sh                  # 把 dot-claude/ 重命名为 .claude/ + 加 hook 执行权限 + npm install
npm start                      # http://localhost:3000
npm test                       # 跑 3 个原测试
```

> Cowork 沙箱里 `.claude/` 是受保护目录无法直接写，所以仓库里以 `dot-claude/` 形态分发；`setup.sh` 第一次跑会自动 rename。

## 文件总览

```
board-with-harness/
├── server.js / public/* / tests/*    ← 业务代码（同 baseline）
├── CLAUDE.md                         ← 项目宪法，60 行
├── dot-claude/  →  .claude/          ← setup.sh 后变成
│   ├── settings.json                 ← Hook 注册
│   └── hooks/
│       ├── pre-protect.sh            ← 拦截改存储/全局样式/加依赖
│       └── stop-test.sh              ← 强制 npm test 全绿
├── docs/decisions/
│   └── 0001-storage-choice.md        ← ADR：为什么用内存
└── .harness/changes/                 ← 演示中 features.json 的归档目标目录
```

## 演示中扮演的角色

让 AI 加"点赞功能"，但通过 `/harness:plan` 触发流程：

1. AI **主动澄清**——问去重维度、金色色值、是否切存储
2. AI **产出 features.json**——锁定 acceptance_criteria 和 out_of_scope
3. AI 走 **TDD**——红测试 → 绿实现 → refactor
4. 中途 **PreToolUse Hook 拦截**一次（AI 试图加 localStorage 时被挡）
5. **Stop Hook 强制**测试全绿才能"结束"
6. 产出 PR 含 design doc + ADR + 干净 commit history

## 重要

`.claude/skills/` 和 `.claude/commands/` 在真实场景下应该软链或安装 harness-engineering plugin。演示中讲师可以用 `/harness:plan` 命令名口头引导，AI 行为依赖 CLAUDE.md + Hooks 即可大致还原 treatment 体验。

完整 plugin 安装方式参见 harness-engineering 项目根 README。
