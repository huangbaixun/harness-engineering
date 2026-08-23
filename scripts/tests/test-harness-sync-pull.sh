#!/bin/bash
# F005 Task 3 — pull：GitHub 域回流、harness 域不被覆盖、track 入站、schema 2.0 兼容
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"; : > "$GH_LOG"
fail(){ echo "FAIL: $1"; exit 1; }

cat > "$TMP/features.json" <<'JSON'
{"schema_version":"2.1",
 "github":{"enabled":true,"repo":"o/r","label_prefix":"harness","track_label":"harness/track"},
 "features":[{"id":"F001","name":"alpha","status":"building","priority":1,
   "description":"harness 写的描述","acceptance_criteria":["c1"],"out_of_scope":[],
   "spec":"","dependencies":[],"github_issue":42}]}
JSON
cat > "$TMP/issues.json" <<'JSON'
[{"number":42,"title":"人在 GitHub 上改过的标题","body":"x",
  "labels":[{"name":"P0"},{"name":"state/shipped"},{"name":"harness/building"}],
  "assignees":[{"login":"alice"}],"milestone":{"title":"Sprint 12"},"state":"CLOSED"},
 {"number":77,"title":"PM 提的新需求","body":"来自 GHE 的需求描述",
  "labels":[{"name":"harness/track"}],"assignees":[],"milestone":null,"state":"OPEN"},
 {"number":88,"title":"日常 bug 单","body":"不该被卷进来",
  "labels":[{"name":"bug"}],"assignees":[],"milestone":null,"state":"OPEN"}]
JSON
export GH_ISSUES_JSON="$TMP/issues.json"

( cd "$TMP" && python3 "$ROOT/scripts/harness_sync.py" pull >/dev/null 2>&1 ) || fail "pull 非零退出"

python3 - "$TMP" <<'PY'
import json, sys
d=json.load(open(f"{sys.argv[1]}/features.json"))
f={x["id"]:x for x in d["features"]}
def ck(n,c):
    if not c: print(f"FAIL: {n}"); sys.exit(1)
a=f["F001"]
# GitHub 域回流
ck("priority 回流",        a.get("priority")==0)
ck("assignee 回流",        a.get("assignee")=="alice")
ck("milestone 回流",       a.get("milestone")=="Sprint 12")
ck("delivery_state 回流",  a.get("delivery_state")=="shipped")
# harness 域不被 pull 覆盖（单写所有权）
ck("name 未被覆盖",        a.get("name")=="alpha")
ck("description 未被覆盖", a.get("description")=="harness 写的描述")
ck("status 未被覆盖",      a.get("status")=="building")
# harness/track 入站为 proposed stub；非 track 的 Issue 不入库（验收 5）
tracked=[x for x in d["features"] if x.get("github_issue")==77]
ck("track Issue 已入站",   len(tracked)==1)
ck("入站为 proposed",      tracked[0]["status"]=="proposed")
ck("入站 acceptance 为空", tracked[0]["acceptance_criteria"]==[])
ck("非 track 不入库",      not any(x.get("github_issue")==88 for x in d["features"]))
print("pull-ok")
PY

# schema 2.0 文件（无新字段、无 github 块）必须仍可正常工作且零网络（验收 9、1）
TMP2=$(mktemp -d)
cat > "$TMP2/features.json" <<'JSON'
{"schema_version":"2.0","features":[{"id":"F001","name":"a","status":"done","priority":1,
 "description":"","acceptance_criteria":[],"out_of_scope":[],"spec":"","dependencies":[],
 "technical_notes":"","related_files":[]}]}
JSON
: > "$GH_LOG"
( cd "$TMP2" && python3 "$ROOT/scripts/harness_sync.py" pull >/dev/null 2>&1 ) || fail "2.0 文件 pull 非零退出"
( cd "$TMP2" && python3 "$ROOT/scripts/harness_sync.py" push >/dev/null 2>&1 ) || fail "2.0 文件 push 非零退出"
[ -s "$GH_LOG" ] && fail "未配置却发生了 gh 调用（验收 1）"
diff <(python3 -c "import json;print(json.dumps(json.load(open('$TMP2/features.json')),sort_keys=True))") \
     <(echo '{"features": [{"acceptance_criteria": [], "dependencies": [], "description": "", "id": "F001", "name": "a", "out_of_scope": [], "priority": 1, "related_files": [], "spec": "", "status": "done", "technical_notes": ""}], "schema_version": "2.0"}') \
  >/dev/null || fail "2.0 文件被同步逻辑改动了（验收 9）"
rm -rf "$TMP2"
echo PASS
