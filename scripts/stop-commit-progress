#!/bin/bash
# Template: Stop Hook — 自动提交进度文件
# 每次会话有完整 git 历史，任何错误都可回滚

cd "$CLAUDE_PROJECT_DIR" || exit 0

# 检查进度文件是否有变化
if git diff --quiet docs/claude-progress.json 2>/dev/null; then
  exit 0  # 没有变化，跳过
fi

git add docs/claude-progress.json
git commit -m "chore: update agent progress [skip ci]" --no-verify 2>/dev/null

# 成功 = 静默
exit 0
