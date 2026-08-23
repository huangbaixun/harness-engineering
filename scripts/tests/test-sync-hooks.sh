#!/bin/bash
# F005 Task 5 — hook 契约：未配置零网络、失败仍 exit 0 且恰好一行、SessionStart 不阻断
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"
fail(){ echo "FAIL: $1"; exit 1; }

# A. 未配置：Stop hook 零 gh 调用、零输出、exit 0（验收 1）
D="$TMP/noconf"; mkdir -p "$D"
echo '{"schema_version":"2.0","features":[]}' > "$D/features.json"
: > "$GH_LOG"
OUT=$(CLAUDE_PROJECT_DIR="$D" CLAUDE_PLUGIN_ROOT="$ROOT" bash scripts/stop-sync-issues 2>&1) || fail "未配置时 Stop hook 非零退出"
[ -s "$GH_LOG" ] && fail "未配置却调用 gh（验收 1）"
[ -z "$OUT" ] || fail "未配置却有输出（成功须静默）：$OUT"
echo "  A 未配置 → exit 0, 零 gh, 静默"

# B. 配置了但离线：仍 exit 0，stderr 恰好一行（验收 8）
D="$TMP/offline"; mkdir -p "$D"
cat > "$D/features.json" <<'JSON'
{"schema_version":"2.1","github":{"enabled":true,"repo":"o/r","label_prefix":"harness"},
 "features":[{"id":"F001","name":"a","status":"building","priority":1,"description":"d",
 "acceptance_criteria":["c"],"out_of_scope":[],"spec":"","dependencies":[],"github_issue":42}]}
JSON
echo '[{"number":42,"title":"a","body":"x","labels":[],"assignees":[],"milestone":null,"state":"OPEN"}]' > "$D/issues.json"
RC=0
ERR=$(CLAUDE_PROJECT_DIR="$D" CLAUDE_PLUGIN_ROOT="$ROOT" GH_MODE=offline GH_ISSUES_JSON="$D/issues.json" \
      bash scripts/stop-sync-issues 2>&1 >/dev/null) || RC=$?
[ "$RC" = "0" ] || fail "离线时 Stop hook 退出码 $RC（须为 0，验收 8）"
N=$(echo "$ERR" | grep -c . || true)
[ "$N" -le 1 ] || fail "离线时输出 $N 行（须恰好 ≤1，验收 8）：$ERR"
echo "  B 离线 → exit 0, ${N} 行"

# C. SessionStart 未配置时不因同步而变慢/报错，且摘要仍正常
D="$TMP/ss"; mkdir -p "$D"
echo '{"schema_version":"2.0","features":[{"id":"F001","name":"alpha","status":"building","priority":1}]}' > "$D/features.json"
: > "$GH_LOG"
OUT=$(CLAUDE_PROJECT_DIR="$D" CLAUDE_PLUGIN_ROOT="$ROOT" bash scripts/session-start 2>/dev/null) || fail "session-start 非零退出"
echo "$OUT" | grep -q "F001" || fail "session-start 摘要回归失败"
[ -s "$GH_LOG" ] && fail "未配置却在 SessionStart 调用 gh（验收 1）"
echo "  C SessionStart → 摘要正常, 零 gh"

# D. hooks.json 已注册 Stop hook 且 JSON 合法
python3 -c "
import json,sys
d=json.load(open('$ROOT/hooks/hooks.json'))
cmds=[h['command'] for g in d['hooks'].get('Stop',[]) for h in g['hooks']]
sys.exit(0 if any('stop-sync-issues' in c for c in cmds) else 1)" || fail "hooks.json 未注册 stop-sync-issues"
echo "  D hooks.json → 已注册"

# E. 三元组齐备且 bare 与 .sh 逐字节一致
for f in scripts/stop-sync-issues scripts/stop-sync-issues.sh scripts/stop-sync-issues.cmd; do
  [ -f "$ROOT/$f" ] || fail "缺少 $f"
done
cmp -s "$ROOT/scripts/stop-sync-issues" "$ROOT/scripts/stop-sync-issues.sh" || fail "bare 与 .sh 不一致"
echo "  E 三元组 → 齐备且一致"
echo PASS
