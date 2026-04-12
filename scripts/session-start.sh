#!/bin/bash
# scripts/session-start.sh
# SessionStart Hook — 跨会话记忆恢复
#
# 整合自 obra/superpowers session-start 模式 + Harness Engineering 结构化交接机制
# 触发时机：每次会话启动（startup / clear / compact）
# 原则：成功完全静默；只有在关键状态文件缺失时才输出提示（不是错误）

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

PROGRESS_FILE="docs/claude-progress.json"
FEATURES_FILE="docs/features.json"

# ── 检查进度文件 ──────────────────────────────────────────────────────────────
if [ -f "$PROGRESS_FILE" ]; then
  # 读取关键状态字段并输出给 Agent（作为 session context）
  IN_PROGRESS=$(python3 -c "
import json, sys
try:
    d = json.load(open('$PROGRESS_FILE'))
    ip = d.get('in_progress')
    if ip:
        print(f\"⚡ 进行中：{ip}\")
    phase = d.get('current_phase', '')
    if phase:
        print(f\"📍 当前阶段：{phase}\")
    pending = d.get('pending_features', [])
    if pending:
        print(f\"📋 待处理特性：{len(pending)} 个\")
    completed = d.get('completed_features', [])
    if completed:
        print(f\"✅ 已完成：{len(completed)} 个特性\")
    blockers = [n.get('content','') for n in d.get('notes',[]) if 'blocker' in n.get('content','').lower()]
    if blockers:
        print(f\"⚠️  Blocker：{blockers[0]}\")
except Exception as e:
    pass
" 2>/dev/null)

  if [ -n "$IN_PROGRESS" ]; then
    echo "═══════════════════════════════════════"
    echo "  Harness SessionStart — 进度恢复"
    echo "═══════════════════════════════════════"
    echo "$IN_PROGRESS"
    echo ""
    echo "  → 读取 $PROGRESS_FILE 获取完整状态"
    echo "  → 读取 $FEATURES_FILE 获取需求和验收标准"
    echo "═══════════════════════════════════════"
  fi
fi

# ── 检查是否需要归档 ──────────────────────────────────────────────────────────
if [ -f "$PROGRESS_FILE" ]; then
  COMPLETED_COUNT=$(python3 -c "
import json
try:
    d = json.load(open('$PROGRESS_FILE'))
    print(len(d.get('completed_features', [])))
except:
    print(0)
" 2>/dev/null)

  if [ "${COMPLETED_COUNT:-0}" -ge 10 ]; then
    echo "📦 提示：completed_features 已有 ${COMPLETED_COUNT} 条，建议运行 /harness:evolve 归档历史记录以控制 token 消耗。"
  fi
fi

exit 0
