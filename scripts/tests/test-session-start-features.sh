#!/bin/bash
# F004 Task 1 — session-start 必须读根目录 features.json 并使用 schema 2.0 状态枚举
set -euo pipefail
cd "$(dirname "$0")/../.."

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cat > "$TMP/features.json" <<'JSON'
{"schema_version":"2.0","features":[
 {"id":"F001","name":"alpha","status":"building","priority":1},
 {"id":"F002","name":"beta","status":"proposed","priority":2},
 {"id":"F003","name":"gamma","status":"done","priority":3}]}
JSON
mkdir -p "$TMP/docs"
echo '{"in_progress":"x","completed_features":[]}' > "$TMP/docs/claude-progress.json"

OUT=$(CLAUDE_PROJECT_DIR="$TMP" CLAUDE_PLUGIN_ROOT="$(pwd)" bash scripts/session-start 2>/dev/null)

fail() { echo "FAIL: $1"; echo "--- 实际输出 ---"; echo "$OUT"; exit 1; }
echo "$OUT" | grep -q "F001" || fail "building 特性 F001 未出现在摘要中"
echo "$OUT" | grep -q "F002" || fail "proposed 特性 F002 未出现在摘要中"
printf '%s' "$OUT" | python3 -c 'import json,sys; c=json.load(sys.stdin)["hookSpecificOutput"]["additionalContext"]; s=json.loads(c.split("<harness-state>")[1].split("</harness-state>")[0]); assert s["done_count"]==1' || fail "done 计数错误"
echo "$OUT" | grep -q "EXTREMELY_IMPORTANT" && fail "不应无条件注入元技能"
echo PASS

# ── 回归：features.json 存在但 claude-progress.json 不存在时，摘要仍须渲染 ──
# （修复前整段被 PROGRESS_FILE 卡死，本仓库自身就是这个场景）
TMP2=$(mktemp -d); trap 'rm -rf "$TMP" "$TMP2"' EXIT
cp "$TMP/features.json" "$TMP2/features.json"
OUT2=$(CLAUDE_PROJECT_DIR="$TMP2" CLAUDE_PLUGIN_ROOT="$(pwd)" bash scripts/session-start 2>/dev/null)
fail2() { echo "FAIL(no-progress): $1"; echo "$OUT2"; exit 1; }
echo "$OUT2" | grep -q "F001" || fail2 "无 progress 文件时特性摘要未渲染"
echo "$OUT2" | grep -q "了解当前进度" && fail2 "无 progress 文件却仍提示去读它"
echo "$OUT2" | grep -q "hookSpecificOutput" || fail2 "缺少合法启动协议输出"
echo PASS-no-progress
