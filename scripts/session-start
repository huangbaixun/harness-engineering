#!/bin/bash
# scripts/session-start.sh
# SessionStart Hook — 跨会话记忆恢复
#
# 整合自 obra/superpowers session-start 模式 + Harness Engineering 结构化交接机制
# 触发时机：每次会话启动（startup / clear / compact）
# 输出层次：
#   ① 元技能注入（ADR-0010，无条件发出）— 强制 "1% rule" 协议
#   ② 进度/特性摘要（仅当 docs/claude-progress.json 存在时）
#   ③ 归档提示（仅当 completed_features ≥ 10 时）
# 原则：用户可见错误保持静默；session-context 注入是预期输出,不是 noise

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

PROGRESS_FILE="docs/claude-progress.json"
FEATURES_FILE="docs/features.json"

# ── 元技能注入 (ADR-0010) ────────────────────────────────────────────────────
# 在 SessionStart 时把 using-harness 正文注入到 session 上下文,强制建立
# "先查技能再行动" 的元协议。来源单一: skills/using-harness/SKILL.md (ADR-0009)
META_SKILL="$PLUGIN_ROOT/skills/using-harness/SKILL.md"
if [ -f "$META_SKILL" ]; then
  echo "<EXTREMELY_IMPORTANT>"
  awk 'BEGIN{n=0} /^---$/{n++; next} n>=2{print}' "$META_SKILL"
  echo "</EXTREMELY_IMPORTANT>"
  echo ""
fi

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

  # ── features.json 摘要 ──────────────────────────────────────────────────────
  FEATURES_SUMMARY=""
  if [ -f "$FEATURES_FILE" ]; then
    FEATURES_SUMMARY=$(python3 -c "
import json
try:
    d = json.load(open('$FEATURES_FILE'))
    feats = d.get('features', [])
    pending = [f for f in feats if f.get('status') in ('pending', 'ready')]
    ip = [f for f in feats if f.get('status') == 'in_progress']
    done = [f for f in feats if f.get('status') in ('completed', 'done')]
    if ip:
        print(f'  🔧 进行中特性：{ip[0][\"id\"]} {ip[0].get(\"name\",\"\")}')
    if pending:
        nxt = pending[0]
        print(f'  📌 下一个特性：{nxt[\"id\"]} {nxt.get(\"name\",\"\")} (priority={nxt.get(\"priority\",\"?\")})')
    print(f'  📊 特性统计：{len(done)} done / {len(ip)} in_progress / {len(pending)} pending')
except:
    pass
" 2>/dev/null)
  fi

  echo "═══════════════════════════════════════"
  echo "  Harness SessionStart — 仪式性启动链"
  echo "═══════════════════════════════════════"
  if [ -n "$IN_PROGRESS" ]; then
    echo "$IN_PROGRESS"
  fi
  if [ -n "$FEATURES_SUMMARY" ]; then
    echo "$FEATURES_SUMMARY"
  fi
  echo ""
  echo "  启动检查清单（按顺序执行，不要跳过）："
  echo "  ① pwd 确认工作目录"
  echo "  ② 读取 $PROGRESS_FILE 了解当前进度"
  echo "  ③ 读取 $FEATURES_FILE 了解需求和验收标准"
  echo "  ④ 运行项目测试命令确认基线（记录失败数量）"
  echo "  ⑤ 确认 in_progress 特性，继续或标记完成后再取下一个"
  echo "═══════════════════════════════════════"
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
