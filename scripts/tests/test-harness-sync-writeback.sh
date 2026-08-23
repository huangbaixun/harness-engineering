#!/bin/bash
# F005 补充 — 创建后必须把 Issue 编号回写 features.json。
# 回归防线：github_issue 是持久锚点；缺了它，影子（gitignore、可丢弃）
# 一旦丢失就会重复创建 Issue，推翻 spec 的「无状态对账」性质。
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"; : > "$GH_LOG"
export GH_BODY_LOG="$TMP/gh.body"; : > "$GH_BODY_LOG"
fail(){ echo "FAIL: $1"; exit 1; }

cat > "$TMP/features.json" <<'JSON'
{"schema_version":"2.1","github":{"enabled":true,"repo":"o/r","label_prefix":"harness"},
 "features":[{"id":"F001","name":"a","status":"building","priority":1,"description":"d",
   "acceptance_criteria":["c"],"out_of_scope":[],"spec":"","dependencies":[],"github_issue":null}]}
JSON
echo '[]' > "$TMP/issues.json"; echo '[]' > "$TMP/labels.json"
export GH_ISSUES_JSON="$TMP/issues.json" GH_LABELS_JSON="$TMP/labels.json"

( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true

NUM=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['features'][0].get('github_issue'))" "$TMP/features.json")
[ "$NUM" = "999" ] || fail "创建后未回写 github_issue（实际 ${NUM}，桩返回的编号是 999）"

# 影子丢失后不得重复创建 —— 这才是回写的意义
rm -rf "$TMP/.harness"
cat > "$TMP/issues.json" <<'JSON'
[{"number":999,"title":"a","body":"x","labels":[],"assignees":[],"milestone":null,"state":"OPEN"}]
JSON
: > "$GH_LOG"
( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true
grep -q "issue create" "$GH_LOG" && fail "影子丢失后重复创建了 Issue（无状态对账性质被破坏）"
echo PASS
