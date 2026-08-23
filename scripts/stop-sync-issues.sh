#!/bin/bash
# Stop Hook — features.json → GitHub/GHE Issue 推送（F005）
#
# 契约（spec §5）：
#   - 任何失败均 exit 0。Stop hook 非零退出会阻断会话结束，
#     同步失败绝不该让人卡在会话里。
#   - 成功完全静默；失败输出恰好一行（每会话一次，不是每次编辑一次）。
#   - 未配置 github.enabled 时整段跳过，零网络、零开销。
#   - 拿不到并发锁即跳过，绝不等待。

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}" 2>/dev/null || exit 0

SYNC="$PLUGIN_ROOT/scripts/harness_sync.py"
[ -f "$SYNC" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

python3 "$SYNC" push --require-lock 2>&1 >/dev/null | head -1 >&2

exit 0
