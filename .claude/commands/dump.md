---
description: 保存当前会话的关键决策和进度到文档，用于长任务的跨会话交接
---

将以下信息写入 docs/claude-progress.json：
1. 本次会话完成的特性（更新 completed_features）
2. 当前进行中的工作（更新 in_progress）
3. 遇到的重要决策和理由（追加到 docs/decisions/ 目录）
4. 下一个 Agent 需要知道的关键上下文
5. 如有 blocker，记录在 in_progress.blockers 中

同时更新 last_updated 时间戳。
完成后输出摘要：「已保存 X 个完成特性，当前进度：[特性名]」
