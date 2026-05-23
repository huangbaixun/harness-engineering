# Demo 脚本 — Baseline vs Harness 对比演示

> 90 分钟培训中的 §D 环节（25 分钟）。
> 目标：让零基础听众**亲眼看到**同一个项目、同一个 AI、同一个任务，装与不装 harness 的差异。

---

## 目录

- [演示前置（培训前 3 天完成）](#演示前置)
- [演示走位 — Baseline 路径（8 分钟）](#演示走位--baseline-路径)
- [演示走位 — Treatment 路径（10 分钟）](#演示走位--treatment-路径)
- [对比讨论（4 分钟）](#对比讨论)
- [录屏指南（备份视频）](#录屏指南)
- [现场翻车兜底](#现场翻车兜底)
- [可视化对比表（必带上墙）](#可视化对比表)

---

## 演示前置

### 培训前 7 天

- [ ] 拉 sample-board 项目到讲师本机
- [ ] 跑通 `board-baseline/`：`cd board-baseline && npm install && npm test`，期望 3/3 通过
- [ ] 跑通 `board-with-harness/`：`cd board-with-harness && bash setup.sh && npm test`，期望 3/3 通过
- [ ] 录两段备份视频（详见[录屏指南](#录屏指南)）

### 培训前 24 小时

- [ ] dry-run 一遍完整 demo，掐时（baseline 8 min + treatment 10 min + 对比 4 min = 22 min，留 3 min buffer）
- [ ] 浏览器打两个标签页：`http://localhost:3000`（演示 baseline 改坏后看效果）
- [ ] 终端开两个窗口：tab1 跑 dev、tab2 跑 git diff / npm test
- [ ] 投屏字号 ≥ 18 pt（Mac iTerm: ⌘+ 直到 80 列窗口里字够大）
- [ ] 网络确认（Claude API 出网正常）

### 培训前 30 分钟

- [ ] 两个项目都 `git status` 确认 clean
- [ ] baseline 的 `tests/board.test.js` 提前看一眼（演示中要让听众看到"删除留言"测试）
- [ ] with-harness 的 CLAUDE.md 顶部 60 行准备好"快速过一下"
- [ ] 备份视频文件路径就绪，能 1 秒切

---

## 演示走位 — Baseline 路径

**时长**：8 分钟
**目标**：让听众看到 AI 在没有约束环境下的常见失败模式

### T=0:00 — 项目展示（0:30）

讲师动作：
1. 切到 `board-baseline/`
2. 终端跑 `npm test`，让听众看到 3 测试全绿
3. 浏览器打 `http://localhost:3000`，让听众看到留言板能用

讲师口播：
> "这是一个很简单的留言板。三个功能：列出、添加、删除。三个测试都过。
> 接下来我让 AI 加一个功能：每条留言可以点赞，重复点赞取消，点赞数超过 5 个用金色高亮。
> 我**不告诉它任何约束**——这是裸 AI，没有 harness。"

### T=0:30 — 任务下发（0:30）

讲师动作：
1. 打开 Claude Code
2. 输入：
   ```
   请在 board-baseline 项目中加一个点赞功能：每条留言可以点赞，
   重复点赞会取消。点赞数超过 5 的留言用金色高亮。
   ```

讲师口播：
> "看好——它不会问我任何问题，直接动手。"

### T=1:00 — AI 开始改（4:30）

讲师动作：
- 让 AI 自由发挥，**不要**打断
- 每改一个文件，讲师把鼠标移到 diff 上，让听众看清楚

预期 AI 行为（不需要 100% 复现，每出现一个就标红讲）：

| AI 动作 | 讲师对听众说的话 |
|--------|-----------------|
| 改 `index.html` 加按钮 | "OK，按钮加了。但'金色'是什么色值？它没问。" |
| 改 `app.js` 加点赞逻辑 | "重复点赞取消——但是同 IP？同 session？它假设了一个，没确认。" |
| **改 `server.js` 加 likes 路由** | "OK 这个合理。" |
| **顺手把 messages 数组改成 localStorage** ❌ | "等等——它把存储改了。我没让它改存储啊。" |
| 改 `style.css` 加 `.golden` class | "样式直接写 hex `#ffd700`，没用 CSS 变量。" |
| **没写新测试** ❌ | "新功能加完了，测试呢？没写。" |

如果 AI 没"自动"改坏存储，讲师可以接着提示："顺便能不能让数据刷新不丢？"——AI 大概率会切到 localStorage。

### T=5:30 — 跑测试看回归（1:30）

讲师动作：
1. 终端跑 `npm test`
2. **预期**：原本 3 个测试，至少 1 个挂（删除留言失败，因为 localStorage 不再用 `messages.splice`）

讲师口播：
> "看到没？它说'已实现'，但既有的删除测试坏了。
> 它不是恶意的——它每一步都'自以为合理'。但没人在它头上拦着。"

如果测试**没坏**（AI 这次比较保守），讲师 plan B：
- 直接展示 `git diff`，列出"改了 5 个文件，没新测试，存储被改"——也能体现失败模式

### T=7:00 — 回顾产出（1:00）

讲师动作：跑 `git diff --stat`

讲师口播（同时屏幕显示对比表草稿）：
> "我们这次拿到的是：
> - 改了 5 个文件
> - 1 个原测试坏了
> - 0 个新测试
> - 没有任何决策记录
>
> 如果你是 reviewer，这种 PR 你打算花多久？"

让听众回答（10 秒）。

### T=8:00 — 收尾过渡（0:00）

讲师口播：
> "下面同样的任务、同样的 AI，唯一区别是这个项目装了 harness。我们看差多少。"

切到 `board-with-harness/`。

---

## 演示走位 — Treatment 路径

**时长**：10 分钟
**目标**：让听众看到 harness 在每个关键点上把 AI 拉回正轨

### T=0:00 — 快速展示 harness 配置（2:00）

讲师动作：依次打开三个文件，每个 30 秒带过：

**1. CLAUDE.md**（30 秒）
- 让听众看顶部"项目定位 / 测试 / 架构约定"三段
- 重点圈红：rigid 禁止规则
  - 不引入新依赖
  - 不修改存储层
  - 不改 :root CSS 变量名
  - TDD：先红再绿

讲师口播：
> "这是项目宪法。AI 工作前会读这个。"

**2. dot-claude/settings.json**（30 秒）
- 展示两个 hook：`PreToolUse → pre-protect.sh`、`Stop → stop-test.sh`

讲师口播：
> "这是机械约束。AI 改 `package.json` 想加依赖？被这个 hook 拒。AI 想说'已实现'？这个 hook 强制跑测试。"

**3. dot-claude/hooks/pre-protect.sh**（1:00）
- 展示三个 grep 拦截规则
- 重点：`localStorage|sessionStorage|sqlite|redis|...` 这条

讲师口播：
> "看，这条 grep 就是上一个演示里 AI 改坏存储的免疫针——它再想顺手改，hook 直接 exit 2 拒绝。"

### T=2:00 — 任务下发（0:30）

讲师动作：在 Claude Code 输入：
```
/harness:plan
请加一个点赞功能：每条留言可以点赞，重复点赞会取消。
点赞数超过 5 的留言用金色高亮。
```

注意：
- 真实场景下 `/harness:plan` 是 plugin 提供的 slash command
- 演示中如果 plugin 未装，可改为：`阅读 CLAUDE.md 后用 plan-then-tdd 方式做这个需求`

### T=2:30 — Clarify 阶段（1:00）

预期 AI 行为：**主动问问题**，不立刻动手。常问的：

- "重复点赞按什么维度去重？同浏览器 session？同 cookie？同登录用户？"
- "金色高亮是只前端样式还是要存到数据 schema？"
- "CLAUDE.md 说不切存储——这是否意味着点赞数也只在内存？"

讲师扮演用户回答（速答）：
- 同 session 去重（用 sessionStorage 存"我已点赞过哪些 id"——不存进 server）
- 不进 schema，纯前端样式
- 是的，点赞数也在内存（重启清零，与现状一致）

讲师口播：
> "这就是 harness 让 AI 做的第一件事——澄清。
> 30 秒讨论，省了上一个演示里 5 分钟的返工。"

### T=3:30 — Plan 阶段（1:00）

预期 AI 行为：产出 `features.json`，写到 `.harness/changes/like-feature/proposal.md` 之类。

```json
{
  "name": "like-feature",
  "rigid": {
    "acceptance_criteria": [
      "每条留言展示当前点赞数",
      "点击点赞按钮 +1，再次点击 -1",
      "点赞数 > 5 的留言带金色高亮 class"
    ],
    "out_of_scope": [
      "不切换存储后端",
      "不重构既有 model",
      "不引入新依赖",
      "不修改 :root CSS 变量"
    ],
    "forbidden_patterns": ["localStorage", "Redis", "sqlite"]
  },
  "flexible": {
    "description": "前端展示点赞按钮 + 数字 + 条件高亮",
    "technical_notes": "session 去重用 sessionStorage 存已点赞 id 集合"
  }
}
```

讲师口播：
> "看到这个 `out_of_scope` 没？这就是 scope 锁。AI 后面再想'自由发挥'，自己写的边界自己撞。"

### T=4:30 — TDD 阶段（3:00）

预期 AI 行为：先写失败测试，再写最小实现。

#### Red（红，0:30）

```javascript
test('POST /api/messages/:id/like increments and toggles like count', async () => {
  // 这个测试现在会失败，因为路由不存在
  ...
});
```

讲师口播：
> "他先写测试。跑一下：失败。这是 TDD 的'红'阶段——必须看到红，才能开始绿。"

#### Green（绿，1:30）

AI 加最小实现：
- `server.js` 加 `POST /api/messages/:id/like` 路由（递增 / 递减）
- `app.js` 加点赞按钮 + sessionStorage 逻辑
- `style.css` 加 `.golden` class

**重点演示**：当 AI 试图改 `style.css` 的 `:root` 变量时，PreToolUse Hook 拦截。

```
PRE-PROTECT: 检测到 :root 变量改动 — 请确认这不是组件级样式调整。
```

AI 撤回 `:root` 改动，改成在 `.golden` 类下用现成变量 + 新增局部 hex（不改全局变量）。

讲师口播：
> "看到了！hook 拦截了一次。AI 自动调整了方式——这就是约束变能力。"

#### Refactor（5:30 - 6:30，1:00）

AI 整理代码，commit 信息分别是 `red:` / `green:` / `refactor:`。

跑 `npm test`：5 个测试（3 原 + 2 新）全绿。

### T=7:30 — Verify 阶段（1:30）

预期 AI 行为：
- 跑 `npm test`：全绿
- 检查 acceptance_criteria 是否每条都有对应测试覆盖
- Stop Hook 触发 → 也跑了一遍 → 通过 → 允许结束

如果 AI 试图绕过测试直接说"完成"，Stop Hook 会拒：
```
STOP-HOOK: npm test 失败 — 不能在测试不通过的状态下结束。
```

讲师口播：
> "看，AI 说'我做完了'前，hook 强制跑了一遍测试。绿了才放行。
> 这就是为什么 harness 里说：约束**赋能**——AI 不需要自己记得跑测试，环境替它跑。"

### T=9:00 — 看产出（1:00）

讲师动作：
1. `git log --oneline` —— 三个干净 commit：red / green / refactor
2. `ls .harness/changes/like-feature/` —— proposal.md / tasks.md 归档
3. `git diff --stat` —— 改了 2 个文件（server.js 和 app.js + style.css 的微改）
4. `npm test` —— 5/5 全绿

讲师口播：
> "对比上一个 baseline：5 文件 → 2 文件，1 测试坏 → 5 测试全绿，0 归档 → 完整 proposal。
> 你下次 review 这个 PR 大概几分钟？"

### T=10:00 — 切到对比讨论

---

## 对比讨论

**时长**：4 分钟

讲师把对比表打到屏幕（[见下](#可视化对比表)），让听众回答三个问题：

### Q1（1:30）— "Baseline 路径里，AI 哪一步开始走偏？"

期待答案：
- "一开始就没问，直接动手"
- "顺手改存储那一刻"
- "改了之后没自检"

讲师收口：**走偏不是某一步——是从'没有约束'那一刻起，每一步都可能走偏。**

### Q2（1:30）— "Treatment 路径里，最让你意外的是哪一点？"

期待答案：
- AI 主动问问题（很多人没见过 AI 倒提问）
- Hook 拦截那一下（机械约束力量感）
- 归档自动落盘（PM 角色会有触动）
- 测试先行（QA 角色会有触动）

讲师收口：**Harness 不是'更好的 prompt'，是把 prompt 之外的所有阶段都接管了。**

### Q3（1:00）— "如果让你接手这两份 PR review，时间差大概多少？"

期待答案：
- baseline："得来回扯几轮，至少 1 小时"
- treatment："5-10 分钟"

讲师收口：**Harness 不是给 AI 用的——是给整个团队用的。下游 reviewer / QA / PM 都受益。**

---

## 录屏指南

讲师培训前 3 天必须录两段备份视频，避免现场出意外。

### 录屏环境

- 屏幕分辨率 1920×1080（投屏标准）
- 终端字号 ≥ 16 pt
- iTerm / Terminal 单窗口宽 ≥ 100 列
- 浏览器打开 `http://localhost:3000`，缩放 125%
- 隐藏个人信息（关闭通知、清桌面）

### 录屏工具

- macOS：⌘+⇧+5 系统自带 / OBS Studio
- Windows：OBS / 雷电录屏
- 输出格式：mp4，1080p，比特率 5 Mbps 起

### 录屏 1：Baseline（目标 6 分钟）

按[Baseline 走位](#演示走位--baseline-路径)的 T=0:00 → T=8:00 完整录一遍。如果 AI 这次"很乖"没改坏存储：

- **重录一次**，提示 AI 时加一句"顺便能不能让刷新不丢"
- 或，**剪辑**：选最能体现失败模式的几次尝试拼接

### 录屏 2：Treatment（目标 8 分钟）

按[Treatment 走位](#演示走位--treatment-路径)录。重点确保：
- 镜头里能清楚看到 AI 主动问问题
- 镜头里能清楚看到 Hook 拦截 stderr 输出
- 镜头里能清楚看到最后 5 个测试全绿

如果某次 Hook 没触发，故意输入"用 localStorage 存数据"作为引导，让拦截可见。

### 备份视频命名

```
training/recordings/
├── baseline-vN-YYYYMMDD.mp4         (~70 MB)
└── treatment-vN-YYYYMMDD.mp4        (~90 MB)
```

每次小改 demo 流程都升 vN，防止用错版本。

---

## 现场翻车兜底

| 翻车场景 | 应对话术 + 动作 |
|---------|---------------|
| Claude API 抖动/超时 | "网络不稳，切到我准备的录屏。"立刻切到 baseline 视频。**不要现场调试网络。** |
| AI 这次没改坏（baseline 太"乖"） | "今天 AI 状态不错——但你看，它每天表现都不一样，这本身就是问题。我用上周的录屏给你看典型失败。" 切视频。 |
| Hook 没触发 | "Hook 这次没触发——可能 grep 没匹配到我刚才的输入。我换个明显的让你看到。" 现场输入"`messages` 改成 `localStorage.setItem`"，hook 应必触发。 |
| AI 输出超长，时间不够 | "我打断它一下——你已经看到关键失败了，重点是它根本没有约束去阻止。" 强制切到 git diff 看产出。 |
| 听众打断频繁 | "好问题，我把它记下来——为了不打乱节奏，我演完这段统一回答。" 把问题写到白板。 |
| 投屏字号小 | 立刻 ⌘+ 调大；同时口述屏幕内容确保后排听众听得到。 |
| 听众怀疑"是你预先调好的" | "代码和 prompt 都在仓库里——会后我把链接发群，你们可以自己跑。"（这就是 sample-board 仓库的价值。） |

---

## 可视化对比表

**这张表是 demo 的灵魂。必须在 §D 收尾时打到屏幕中央，成为听众离场时仍记得的那一帧。**

| 维度 | Baseline（无 harness） | Treatment（有 harness） | 差距 |
|------|---------------------|----------------------|------|
| 文件改动数 | 5 | 2 | -60% |
| 原测试通过 | 2/3 ❌ | 3/3 ✅ | 杜绝回归 |
| 新测试覆盖 | 0 | 2 | TDD 保证 |
| 范围越界 | 改了存储层 ❌ | 无 | scope 锁定 |
| 决策归档 | 无 | proposal.md + ADR ✅ | 三月后还能查 |
| Hook 拦截次数 | 0（没装） | 1（CSS 变量） | 机械防误伤 |
| commit 整洁度 | 1 个超长 commit | red / green / refactor 三个 | 易回滚 |
| 预估 review 时长 | ~60 min | ~10 min | -83% |
| 你信任这个 PR 吗 | 不太敢 | 敢 | — |

口播配套：
> "把这张表拍下来。下次你或你团队的同事抱怨'AI 写代码不靠谱'——你拿出这张表问他：你是装了 harness 还是没装？"

---

## 附：演示中可能被问的高频问题

| 问题 | 答案要点 |
|------|--------|
| "CLAUDE.md 这 60 行是你提前写的吧？" | 是。但写一份只要 30 分钟，模板可复用，不是 demo 专属。会后给链接。 |
| "Hook 用 bash 写不会被绕过吗？" | 在 Claude Code 中 Hook 是模型不可见的——它**接触不到**也无法绕过。 |
| "如果 hook 误拦了真的合理改动呢？" | 调整 hook 的 grep 规则即可。第一版总有误判，迭代过程的一部分。 |
| "学这套的时间成本？" | 第一份 CLAUDE.md 半小时。第一个 Hook 1-2 小时。完整 harness 1-2 周。 |
| "AI 越来越强，未来还需要 harness 吗？" | 部分会。harness 第三原则就是"随模型进化精简"。但失败模式会变，约束本身不会消失。 |
