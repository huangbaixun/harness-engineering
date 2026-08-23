#!/bin/bash
# F005 补充 — label 自举：缺失的 harness/ 前缀 label 必须被创建；非 harness/ 一律不碰
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"; : > "$GH_LOG"
fail(){ echo "FAIL: $1"; echo "--- gh 调用 ---"; cat "$GH_LOG"; exit 1; }

cat > "$TMP/features.json" <<'JSON'
{"schema_version":"2.1","github":{"enabled":true,"repo":"o/r","label_prefix":"harness"},
 "features":[{"id":"F001","name":"a","status":"building","priority":1,"description":"d",
   "acceptance_criteria":["c"],"out_of_scope":[],"spec":"","dependencies":[],"github_issue":null},
  {"id":"F002","name":"b","status":"done","priority":1,"description":"d",
   "acceptance_criteria":["c"],"out_of_scope":[],"spec":"","dependencies":[],"github_issue":null}]}
JSON
echo '[]' > "$TMP/issues.json"
# 仓库现有 label 里没有任何 harness/ 前缀
cat > "$TMP/labels.json" <<'JSON'
[{"name":"bug"},{"name":"enhancement"},{"name":"wontfix"}]
JSON
export GH_ISSUES_JSON="$TMP/issues.json" GH_LABELS_JSON="$TMP/labels.json"

( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true

grep -q "label create harness/building" "$GH_LOG" || fail "缺失的 harness/building 未被创建"
grep -q "label create harness/done"     "$GH_LOG" || fail "缺失的 harness/done 未被创建"
# 绝不创建/修改非 harness/ 前缀（验收 6）
if grep -oE 'label create [^ ]+' "$GH_LOG" | grep -vq 'harness/'; then
  fail "创建了非 harness/ 前缀的 label（验收 6）"
fi
grep -qE 'label (delete|edit) ' "$GH_LOG" && fail "对既有 label 做了删除/修改"
# 已存在的 harness/ label 不重复创建
: > "$GH_LOG"
cat > "$TMP/labels.json" <<'JSON'
[{"name":"bug"},{"name":"harness/building"},{"name":"harness/done"}]
JSON
rm -rf "$TMP/.harness"
( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true
grep -q "label create" "$GH_LOG" && fail "已存在的 label 被重复创建"
echo PASS
