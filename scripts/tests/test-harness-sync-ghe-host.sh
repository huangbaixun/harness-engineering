#!/bin/bash
# GHE 主机路由回归。
#
# gh 的 `--hostname` 只有 auth 系子命令认，issue/label 一律不认，靠 GH_HOST
# 环境变量路由。此前 gh() 给每个子命令都追加 --hostname，导致所有 GHE 项目的
# list/create/edit 无一例外失败；而 `unknown flag` 被兜底归入 offline，
# 对外只显示「网络不可达，下次自动重试」—— 永远不重试成功，也看不出真实原因。
# github.com 命中白名单不加 flag，所以这个 bug 在 github.com 上永不暴露。
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT="$(pwd)"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export HARNESS_GH_BIN="$ROOT/scripts/tests/stubs/gh-stub"
export GH_LOG="$TMP/gh.log"; export GH_ENV_LOG="$TMP/gh.env"
fail(){ echo "FAIL: $1"; exit 1; }

# ── 1. 单元：命令行不带 --hostname，主机改由 GH_HOST 传递 ──
python3 - "$ROOT" <<'PY' || fail "gh() 主机路由断言未通过（见上方 AssertionError）"
import importlib.util, sys

spec = importlib.util.spec_from_file_location("hs", sys.argv[1] + "/scripts/harness_sync.py")
hs = importlib.util.module_from_spec(spec); spec.loader.exec_module(hs)

seen = {}
class _P: returncode, stdout, stderr = 0, "{}", ""
def fake_run(cmd, **kw):
    seen["cmd"], seen["env"] = cmd, kw.get("env"); return _P()
hs.subprocess.run = fake_run

hs.gh(["issue", "list", "--repo", "o/r"], {"host": "example.ghe.com"})
assert "--hostname" not in seen["cmd"], f"issue 子命令仍带 --hostname: {seen['cmd']}"
assert seen["env"] is not None, "GHE 主机未注入环境"
assert seen["env"]["GH_HOST"] == "example.ghe.com", f"GH_HOST 错误: {seen['env'].get('GH_HOST')}"
assert "PATH" in seen["env"], "env 未继承 os.environ，会丢掉 PATH/凭据缓存路径"

hs.gh(["issue", "list"], {"host": "github.com"})
assert "--hostname" not in seen["cmd"], "github.com 不应带 --hostname"
assert seen["env"] is None, "github.com 不应覆写环境"

hs.gh(["issue", "list"], {})
assert seen["env"] is None, "未配 host 时不应覆写环境"

# 用法错误必须与「可自愈的网络问题」分开，否则误导用户干等重试
assert hs._classify("unknown flag: --hostname") == "usage", "unknown flag 应归为 usage"
assert hs._classify("unknown command \"foo\" for \"gh\"") == "usage", "unknown command 应归为 usage"
assert hs._classify("error connecting to host") == "offline", "真实网络错误分类被改坏"
print("  单元：--hostname 已移除，GH_HOST 已注入，usage 已独立分类")
PY

# ── 2. 端到端：GHE 配置下 push 必须真的推成功（桩会像真 gh 一样拒绝 --hostname）──
d="$TMP/ghe"; mkdir -p "$d"
cat > "$d/features.json" <<'JSON'
{"schema_version":"2.1","github":{"enabled":true,"repo":"o/r","host":"example.ghe.com",
 "label_prefix":"harness"},
 "features":[{"id":"F001","name":"a","status":"building","priority":1,"description":"新内容",
 "acceptance_criteria":["c"],"out_of_scope":[],"spec":"","dependencies":[],"github_issue":42}]}
JSON
cat > "$d/issues.json" <<'JSON'
[{"number":42,"title":"a","body":"旧内容","labels":[],"assignees":[],"milestone":null,"state":"OPEN"}]
JSON
: > "$GH_LOG"; : > "$GH_ENV_LOG"
err=$( cd "$d" && GH_ISSUES_JSON="$d/issues.json" \
       python3 "$ROOT/scripts/harness_sync.py" push 2>&1 >/dev/null ) || fail "GHE push 非零退出"
[ -z "$err" ] || fail "GHE push 应静默成功，实际输出：$err"
grep -q "issue edit" "$GH_LOG" || fail "GHE 配置下未发生 issue edit（同步实际未成功）"
grep -q "example.ghe.com" "$GH_ENV_LOG" || fail "gh 子进程未收到 GH_HOST=example.ghe.com"
echo "  端到端：GHE push 成功，GH_HOST 抵达 gh 子进程"

# ── 3. 用法错误不得伪装成网络问题 ──
# 必须用全新目录：步骤 2 已写下影子副本，同目录再推是幂等空操作，根本不会调 gh
u="$TMP/usage"; mkdir -p "$u"; cp "$d/features.json" "$d/issues.json" "$u/"
: > "$GH_LOG"
err=$( cd "$u" && GH_MODE=usage GH_ISSUES_JSON="$u/issues.json" \
       python3 "$ROOT/scripts/harness_sync.py" push 2>&1 >/dev/null ) || fail "usage 模式非零退出"
echo "$err" | grep -q "网络不可达" && fail "用法错误被谎报成网络问题：$err"
echo "$err" | grep -q "bug" || fail "用法错误未提示上报 bug：$err"
echo "  分类：unknown flag → 「参数有误，请报 bug」，不再谎报网络"

# ── 4. 未识别的错误同样不得冒充「网络不可达」（兜底不说「等等就好」）──
w="$TMP/weird"; mkdir -p "$w"; cp "$d/features.json" "$d/issues.json" "$w/"
err=$( cd "$w" && GH_MODE=weird GH_ISSUES_JSON="$w/issues.json" \
       python3 "$ROOT/scripts/harness_sync.py" push 2>&1 >/dev/null ) || fail "weird 模式非零退出"
echo "$err" | grep -q "网络不可达" && fail "未识别的错误被谎报成网络问题：$err"
echo "$err" | grep -q "something nobody classified" || fail "兜底未带出 gh 原文：$err"
echo "  兜底：未识别错误照实说，并带出 gh 原文"
echo PASS
