# Harness Engineering — 90 分钟培训物料

> 部门级零基础培训的全套物料。多角色（后端 / 前端 / QA / PM）混合听众，仅看演示形态，单次时长 1.5 小时。
>
> **设计理念**：先把"为什么需要"讲透，让"价值差"在 demo 里被亲眼看到，让每个角色找到一个想用的入口。

---

## 一图看懂结构

```
training/
├── README.md                     ← 本文档（交付清单 + 使用说明）
├── instructor-notes.md           ← 讲师讲义（19 页逐页 talking points + Q&A 库）
├── demo-script.md                ← 现场演示走位（baseline 8 min + treatment 10 min + 对比 4 min）
├── working-sheet.md              ← 听众工作纸（A4 单页 + 4 角色提示卡）
├── slides/
│   ├── training-90min.pptx       ← 19 页 PPT（中文，深蓝/古铜/米色）
│   └── build.js                  ← pptxgenjs 重生成脚本（改完 build.js 直接 node 跑）
└── sample-board/
    ├── README.md
    ├── board-baseline/           ← 演示用 mini 留言板（无 harness）
    └── board-with-harness/       ← 同样代码 + CLAUDE.md + Hooks（有 harness）
```

配套上游设计文档：

- `../docs/training-plan-90min.md` — 90 分钟时间分配总方案 + 设计决策

---

## 使用顺序（讲师视角）

### 培训前 7 天

1. 读 `../docs/training-plan-90min.md`，了解整体设计。
2. 读 `instructor-notes.md`，按时间锚点 dry-run 一遍。
3. 读 `demo-script.md`，本地拉 sample-board 跑通两条路径：
   ```bash
   cd sample-board/board-baseline && npm install && npm test
   cd ../board-with-harness && bash setup.sh && npm test
   ```
4. 录 baseline + treatment 备份视频（避免现场翻车）。

### 培训前 24 小时

1. 全程 dry-run 一遍，掐时 90 ± 5 min。
2. 打印 `working-sheet.md` × 30 份（A4 单页，按角色对应面）。
3. 准备投屏（字号 ≥ 18pt）+ 网络 + 备份视频可 1 秒切。

### 培训现场

按 `instructor-notes.md` 的 19 页时间锚点走。任何意外切到备份视频。**永远保 demo**。

### 培训后 48 小时

1. 收离场问卷，整理成 next-session 主题候选。
2. 把 PPT + sample-board 仓库链接发参与者。
3. 30 天后用 `instructor-notes.md` 附录 D 的模板找 follow-up。

---

## 物料清单（M1-M7）

| # | 文件 | 作用 | 状态 |
|---|------|------|------|
| M1 | `../docs/training-plan-90min.md` | 总方案：时间分配 + 各环节设计 + 风险与备选 | ✅ |
| M2 | `slides/training-90min.pptx` | 19 页演示文稿 | ✅ |
| M3 | `instructor-notes.md` | 讲师讲义：逐页 talking points + 时间锚点 + Q&A 库 + 翻车应急话术 + 30 天 follow-up 模板 | ✅ |
| M4 | `demo-script.md` | Demo 详细走位 + 录屏指南 + 现场翻车兜底 + 对比表 | ✅ |
| M5 | `sample-board/` | 演示用 mini 留言板双分支项目 | ✅ |
| M6 | `working-sheet.md` | A4 工作纸 + 4 角色提示卡 | ✅ |
| M7 | 离场问卷 | 模板见 `instructor-notes.md` 附录 C；自行投放到腾讯问卷/金数据 | 📋 模板已给 |

---

## 19 页 PPT 一览

| 页 | 段落 | 主题 |
|----|------|------|
| P1 | — | 封面（深蓝） |
| P2 | §A | 三个调研举手 |
| P3 | §B | 三阶段演进时间轴 |
| P4 | §B | 骏马与缰绳隐喻 |
| P5 | §B | 一次 AI 失败的真实剖面 |
| P6 | §B | 工程师工作重心的转变 |
| P7 | §C | 后端痛点（蓝） |
| P8 | §C | 前端痛点（红） |
| P9 | §C | QA 痛点（绿） |
| P10 | §C | PM 痛点（紫） |
| P11 | §D | Demo 入场（深蓝节标题） |
| P12 | §D | Demo 对比表 9 行 3 列 |
| P13 | §E | 三大核心原则 |
| P14 | §E | 六层模型 |
| P15 | §E | 反馈循环 + 四种修复方式 |
| P16 | §F | 工作纸题目 |
| P17 | §G | 落地路径（个人 + 团队） |
| P18 | §G | Q&A（深蓝节标题） |
| P19 | §G | 致谢 + 下一步（深蓝） |

PPT 配色：深蓝 `#1E2A38`（主导）+ 古铜 `#C8A65A`（accent）+ 米色 `#F4EFE6`（内容底）。中文用 Microsoft YaHei，跨 Mac/Win 显示一致。

## 重新生成 PPT

如果你改了 `slides/build.js`：

```bash
cd training/slides
npm install pptxgenjs    # 第一次需要装
node build.js            # 输出 output.pptx
```

把 output.pptx 重命名为 training-90min.pptx 即可。

---

## 关键设计决策（写给后续维护者）

1. **Demo 占 28% 时长**——零基础最有效说服方式是亲眼看差异，所以演示是命脉，永远保 demo。
2. **零基础用纸笔动手**——听众不预装环境，§F 工作纸把"识别失败 → 工程化护栏"这一核心动作让每人当场做一遍。
3. **多角色 4 痛点对称**——P7-P10 用同一模板 + 不同 motif 色（蓝/红/绿/紫），保证每个角色都有被点名的瞬间。
4. **Sample 项目双分支同业务代码**——为了让听众相信"差异完全来自 harness 配置不是项目本身"，业务代码必须 1:1 一致。
5. **dot-claude/ 而非 .claude/**——某些沙箱保护 .claude/ 目录，setup.sh 解决发布与可用性。
6. **PPT 文字硬编码不用 emoji**——LibreOffice 转 PDF 时 ✓ ✗ 等符号会渲染成 □；中文文字方案最稳。

---

## 联系与反馈

讲师：simon (huangbaixun@gmail.com)

反馈渠道：参考 `instructor-notes.md` 附录 D 的 30 天 follow-up 模板。回收的反馈整理到 `references/training-feedback-2026.md`，下次培训前一周看一遍。
