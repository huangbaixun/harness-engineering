# Mini 留言板 — Baseline 分支

> 培训演示中"裸 Claude Code，无 harness"路径用的项目。

## 运行

```bash
npm install
npm start          # http://localhost:3000
npm test           # 跑 3 个原测试
```

## 演示中扮演的角色

这是 baseline 路径——讲师当场让 AI 加"点赞功能"，故意不提任何 harness 约束，演示 AI 会：

1. 不澄清需求就动手
2. 顺手把内存存储改成 localStorage（范围外）
3. 不写新测试
4. 顺手改坏既有的"删除留言"测试

最终产出 5 文件改动 + 1 个回归 bug + 0 测试 + 0 决策记录。

## 重要

不要在这个分支加任何 CLAUDE.md / .claude/ / hooks。harness 配置只放 `board-with-harness/`。
