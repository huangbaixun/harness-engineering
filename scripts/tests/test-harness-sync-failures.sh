#!/bin/bash
# F005 Task 4 — 九个失败模式：均不抛栈、不阻断、恰好一行警告
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"
export GH_BODY_LOG="$TMP/gh.body"
fail(){ echo "FAIL: $1"; exit 1; }

mk(){ cat > "$1/features.json" <<'JSON'
{"schema_version":"2.1","github":{"enabled":true,"repo":"o/r","label_prefix":"harness"},
 "features":[{"id":"F001","name":"a","status":"building","priority":1,"description":"d",
 "acceptance_criteria":["c"],"out_of_scope":[],"spec":"","dependencies":[],"github_issue":42}]}
JSON
cat > "$1/issues.json" <<'JSON'
[{"number":42,"title":"a","body":"旧内容","labels":[],"assignees":[],"milestone":null,"state":"OPEN"}]
JSON
}

run(){ # run <mode> <cmd...>  -> 打印 stderr，断言 exit 0
  local d="$TMP/$1"; mkdir -p "$d"; mk "$d"
  : > "$GH_LOG"
  local err; local rc=0
  err=$( cd "$d" && GH_MODE="$1" GH_ISSUES_JSON="$d/issues.json" \
         python3 "$ROOT/scripts/harness_sync.py" "${@:2}" 2>&1 >/dev/null ) || rc=$?
  [ "$rc" = "0" ] || fail "$1 模式退出码 ${rc}（应为 0，验收 2/8）"
  echo "$err" | grep -qi "traceback" && fail "$1 模式抛出 Python 栈"
  local n; n=$(echo "$err" | grep -c . || true)
  [ "$n" -le 1 ] || fail "$1 模式输出 $n 行（应恰好 ≤1 行，验收 8）：$err"
  echo "  $1 → rc=0, ${n} 行: $(echo "$err" | head -1 | cut -c1-70)"
}

echo "失败模式矩阵："
run offline   push
run auth      push
run ratelimit push
run notfound  push

# 5. features.json 语法错 -> 静默跳过，不报 JSON 错（非同步职责）
d="$TMP/badjson"; mkdir -p "$d"; echo '{ not json' > "$d/features.json"
err=$( cd "$d" && python3 "$ROOT/scripts/harness_sync.py" push 2>&1 >/dev/null ) || fail "坏 JSON 非零退出"
[ -z "$err" ] || fail "坏 JSON 不应输出：$err"
echo "  badjson → rc=0, 静默"

# 6. 未配置 -> 零网络、零输出
d="$TMP/noconf"; mkdir -p "$d"; echo '{"schema_version":"2.0","features":[]}' > "$d/features.json"
: > "$GH_LOG"
err=$( cd "$d" && python3 "$ROOT/scripts/harness_sync.py" push 2>&1 >/dev/null ) || fail "未配置非零退出"
[ -s "$GH_LOG" ] && fail "未配置却调用了 gh（验收 1）"
[ -z "$err" ] || fail "未配置不应输出"
echo "  noconfig → rc=0, 零 gh 调用, 静默"

# 7. gh 不存在
d="$TMP/nogh"; mkdir -p "$d"; mk "$d"
err=$( cd "$d" && HARNESS_GH_BIN="$TMP/definitely-missing" GH_ISSUES_JSON="$d/issues.json" \
       python3 "$ROOT/scripts/harness_sync.py" push 2>&1 >/dev/null ) || fail "缺 gh 非零退出"
echo "$err" | grep -q "gh" || fail "缺 gh 未给出提示：$err"
echo "  nogh → rc=0, 1 行: $(echo "$err" | head -1 | cut -c1-60)"

# 8. 并发锁：锁被占时立即跳过，绝不等待
d="$TMP/lock"; mkdir -p "$d"; mk "$d"; mkdir -p "$d/.harness/sync.lock"
: > "$GH_LOG"
START=$(python3 -c "import time;print(time.time())")
err=$( cd "$d" && GH_ISSUES_JSON="$d/issues.json" \
       python3 "$ROOT/scripts/harness_sync.py" push --require-lock 2>&1 >/dev/null ) || fail "锁占用非零退出"
ELAPSED=$(python3 -c "import time;print(time.time()-$START)")
python3 -c "import sys;sys.exit(0 if $ELAPSED < 1.0 else 1)" || fail "锁被占时等待了 ${ELAPSED}s（应立即返回）"
[ -s "$GH_LOG" ] && fail "锁被占却仍调用 gh"
echo "  locked → rc=0, 立即返回 (${ELAPSED}s), 零 gh 调用"

# 9. 托管区块被人删除 -> 重建且只重建一次，不重复追加
d="$TMP/noblock"; mkdir -p "$d"; mk "$d"
: > "$GH_LOG"; : > "$GH_BODY_LOG"
( cd "$d" && GH_ISSUES_JSON="$d/issues.json" python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true
[ "$(grep -c 'harness:begin' "$GH_BODY_LOG" 2>/dev/null || echo 0)" = "1" ] || fail "区块未恰好重建一次"
grep -q "旧内容" "$GH_BODY_LOG" || fail "重建区块时丢失了人写的原内容"
echo "  block-deleted → 重建且保留原内容"
echo PASS
