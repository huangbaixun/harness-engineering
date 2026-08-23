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

# features.json 位置解析：schema 2.0 起本文件在仓库根目录；
# docs/ 是 v1 的旧位置，保留以兼容尚未迁移的用户项目。
resolve_features_file() {
  if   [ -f "features.json" ];      then echo "features.json"
  elif [ -f "docs/features.json" ]; then echo "docs/features.json"
  else echo ""
  fi
}
FEATURES_FILE="$(resolve_features_file)"

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

# ── GitHub/GHE 拉取（F005，opt-in）─────────────────────────────────────────
# 未配置 github.enabled 时 harness_sync.py 立即返回，零网络、零开销。
# 硬超时保证：网络再慢也不拖住会话启动；超时即用本地数据继续。
SYNC_SCRIPT="$PLUGIN_ROOT/scripts/harness_sync.py"
if [ -f "$SYNC_SCRIPT" ] && command -v python3 >/dev/null 2>&1; then
  if command -v timeout >/dev/null 2>&1; then
    timeout 5 python3 "$SYNC_SCRIPT" pull --timeout 5 2>&1 >/dev/null | head -1 >&2
  else
    python3 "$SYNC_SCRIPT" pull --timeout 5 2>&1 >/dev/null | head -1 >&2
  fi
fi

# ── 渲染启动摘要 ──────────────────────────────────────────────────────────────
# progress 与 features 是两个独立文件，任一存在即渲染；各子块独立判定。
if [ -f "$PROGRESS_FILE" ] || [ -n "$FEATURES_FILE" ]; then
  IN_PROGRESS=""
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
  fi

  # ── features.json 摘要 ──────────────────────────────────────────────────────
  FEATURES_SUMMARY=""
  if [ -f "$FEATURES_FILE" ]; then
    FEATURES_SUMMARY=$(python3 -c "
import json
try:
    d = json.load(open('$FEATURES_FILE'))
    # schema 2.0 枚举为 proposed/building/done；括号内为 v1 旧值，仅为兼容未迁移项目
    V2_BUILDING = ('building', 'in_progress')
    V2_PROPOSED = ('proposed', 'pending', 'ready', 'planned')
    V2_DONE     = ('done', 'completed')
    feats = d.get('features', [])
    ip      = [f for f in feats if f.get('status') in V2_BUILDING]
    pending = [f for f in feats if f.get('status') in V2_PROPOSED]
    done    = [f for f in feats if f.get('status') in V2_DONE]
    if ip:
        print(f'  🔧 building：{ip[0][\"id\"]} {ip[0].get(\"name\",\"\")}')
    if pending:
        nxt = pending[0]
        print(f'  📌 下一个：{nxt[\"id\"]} {nxt.get(\"name\",\"\")} (priority={nxt.get(\"priority\",\"?\")})')
    print(f'  📊 特性统计：{len(done)} done / {len(ip)} building / {len(pending)} proposed')
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
  # 编号动态生成：缺失的文件不占号，避免出现 ① ③ ④ 这种看起来像 bug 的断号
  _n=0
  _step() { _n=$((_n+1)); echo "  ${_n}. $1"; }
  _step "pwd 确认工作目录"
  [ -f "$PROGRESS_FILE" ] && _step "读取 $PROGRESS_FILE 了解当前进度"
  [ -n "$FEATURES_FILE" ] && _step "读取 $FEATURES_FILE 了解需求和验收标准"
  _step "运行项目测试命令确认基线（记录失败数量）"
  _step "确认 building 特性，继续或标记 done 后再取下一个"
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
