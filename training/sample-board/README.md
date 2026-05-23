# sample-board — 培训演示项目

> 一个 Mini 留言板，配两个分支（无 harness / 有 harness），用于 90 分钟培训的 §D 现场对比演示。
>
> 演示走位见 [`../demo-script.md`](../demo-script.md)。

## 目录结构

```
sample-board/
├── board-baseline/         ← 裸 Claude Code 演示（无 harness）
│   ├── package.json
│   ├── server.js           ← Express + 内存存储
│   ├── public/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── app.js
│   ├── tests/
│   │   └── board.test.js   ← 3 个原测试（列出/添加/删除）
│   └── README.md
│
└── board-with-harness/     ← 装上 harness 的同一项目
    ├── (同样的业务代码)
    ├── CLAUDE.md           ← 项目宪法 60 行
    ├── dot-claude/         ← setup.sh 后变成 .claude/
    │   ├── settings.json   ← Hook 注册
    │   └── hooks/
    │       ├── pre-protect.sh
    │       └── stop-test.sh
    ├── docs/decisions/
    │   └── 0001-storage-choice.md
    ├── .harness/changes/   ← 演示中 features.json 落盘目录
    ├── setup.sh            ← dot-claude → .claude + chmod + npm install
    └── README.md
```

## 快速开始

### Baseline 路径

```bash
cd board-baseline
npm install
npm test         # 期望 3/3 通过
npm start        # http://localhost:3000
```

演示中：让 AI 加点赞功能，**不要**给它任何约束。它大概率会顺手改坏存储 + 不写测试。

### Treatment 路径

```bash
cd board-with-harness
bash setup.sh    # rename dot-claude → .claude, chmod hooks, npm install
npm test         # 期望 3/3 通过
npm start        # http://localhost:3000
```

演示中：让 AI 加点赞功能，但通过 `/harness:plan` 触发流程。看 AI 主动澄清、Hook 拦截、TDD 执行、归档落盘。

## 为什么用内存存储

故意不持久化——见 [`board-with-harness/docs/decisions/0001-storage-choice.md`](./board-with-harness/docs/decisions/0001-storage-choice.md)。

## Cowork 沙箱注意

`.claude/` 在某些沙箱里是受保护目录无法写入。所以仓库里以 `dot-claude/` 形态分发，setup.sh 第一次跑会自动 rename 为 `.claude/`。

## 演示前清单

参见 [`../demo-script.md` § 演示前置](../demo-script.md#演示前置)。

## 为什么这两个分支的业务代码一模一样

这是 demo 的关键约束——必须让听众相信"差异完全来自 harness 配置，不是项目本身"。任何业务代码差异都会让对比说服力打折。
