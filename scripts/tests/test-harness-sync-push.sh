#!/bin/bash
# F005 Task 2 — push：幂等、区块外保全、label 命名空间、超限报数
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"; : > "$GH_LOG"
export GH_BODY_LOG="$TMP/gh.body"; : > "$GH_BODY_LOG"

HUMAN_AFTER=$'\n\nPM 评审：注意并发\n末行'
python3 - "$TMP" "$ROOT" <<'PY'
import json, os, sys, importlib.util
tmp, root = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("hs", os.path.join(root,"scripts/harness_sync.py"))
hs = importlib.util.module_from_spec(spec); spec.loader.exec_module(hs)
feat = {"id":"F001","name":"alpha","status":"building","priority":1,
        "description":"d","acceptance_criteria":["c1"],"out_of_scope":[],
        "spec":"","dependencies":[],"github_issue":42}
data = {"schema_version":"2.1","github":{"enabled":True,"repo":"o/r","label_prefix":"harness"},
        "features":[feat]}
json.dump(data, open(os.path.join(tmp,"features.json"),"w"), ensure_ascii=False, indent=2)
# 已存在的 Issue：托管区块内容已与当前 feature 一致 -> 第二次 push 不应 PATCH
body = "PM 背景\n\n" + hs.render_block(feat) + "\n\nPM 评审：注意并发\n末行"
issues = [{"number":42,"body":body,"labels":[{"name":"P1"},{"name":"state/accepted"},{"name":"harness/building"}],
           "assignees":[],"milestone":None,"state":"OPEN","title":"alpha"}]
json.dump(issues, open(os.path.join(tmp,"issues.json"),"w"), ensure_ascii=False)
PY
export GH_ISSUES_JSON="$TMP/issues.json"

fail(){ echo "FAIL: $1"; echo "--- gh 调用 ---"; cat "$GH_LOG"; exit 1; }

# 幂等：内容一致时不得产生 issue edit（验收 3）
( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true
grep -q "issue edit" "$GH_LOG" && fail "内容一致却仍 PATCH（幂等失败，验收 3）"

# 改动 feature -> 应产生恰好一次 edit，且区块外内容字节不变（验收 4）
python3 - "$TMP" <<'PY'
import json
p=f"{__import__('sys').argv[1]}/features.json"
d=json.load(open(p)); d["features"][0]["acceptance_criteria"]=["c1","c2-new"]
json.dump(d, open(p,"w"), ensure_ascii=False, indent=2)
PY
: > "$GH_LOG"
( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || true
[ "$(grep -c 'issue edit' "$GH_LOG")" = "1" ] || fail "变更后应恰好一次 edit，实际 $(grep -c 'issue edit' "$GH_LOG")"
grep -q "PM 背景" "$GH_BODY_LOG" || fail "区块外内容（前）未随 body 一起提交（验收 4）"
grep -q "末行" "$GH_BODY_LOG" || fail "区块外内容（后）丢失（验收 4）"

# label 命名空间：只允许 add harness/ 前缀（验收 6）
if grep -oE '\-\-add-label [^ ]+' "$GH_LOG" | grep -vq 'harness/'; then
  fail "add 了非 harness/ 前缀的 label（验收 6）"
fi
grep -oE '\-\-remove-label [^ ]+' "$GH_LOG" | grep -v 'harness/' && fail "移除了非 harness/ label（验收 6）"

# 超限报数：limit=0 时须明确报出剩余条数，不静默截断（验收 7）
# 前置：上一步 push 已更新影子，须再次弄脏 feature 才有 dirty 集
python3 - "$TMP" <<'PY2'
import json, sys
p=f"{sys.argv[1]}/features.json"
d=json.load(open(p)); d["features"][0]["acceptance_criteria"]=["c1","c2-new","c3-again"]
json.dump(d, open(p,"w"), ensure_ascii=False, indent=2)
PY2
: > "$GH_LOG"
OUT=$( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" push --limit 0 2>&1 ) || true
echo "${OUT}" | grep -qE "未检查|remaining" || fail "超限未报出剩余条数（验收 7）：${OUT}"
echo "${OUT}" | grep -qE "实际写入" || fail "超限消息未报实际写入数（谎报风险）：${OUT}"
grep -q "issue edit" "$GH_LOG" && fail "limit=0 却仍推送"

echo PASS
