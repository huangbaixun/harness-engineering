#!/bin/bash
# F005 Task 1 — 配置解析与托管区块渲染
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 - <<'PY'
import sys, json, importlib.util
spec = importlib.util.spec_from_file_location("hs", "scripts/harness_sync.py")
hs = importlib.util.module_from_spec(spec); spec.loader.exec_module(hs)

def check(name, cond):
    if not cond: print(f"FAIL: {name}"); sys.exit(1)

# 1. 未配置 / enabled=false / 无 github 块 -> None（验收 1 的地基）
check("no github block -> None", hs.load_config({"features": []}) is None)
check("enabled=false -> None", hs.load_config({"github": {"enabled": False}}) is None)
check("enabled=true -> dict", isinstance(hs.load_config({"github": {"enabled": True, "repo": "o/r"}}), dict))

# 2. render_block 必须含验收清单与 out_of_scope，且被标记包裹
feat = {"id":"F001","name":"alpha","description":"desc here",
        "acceptance_criteria":["c1","c2"],"out_of_scope":["not this"],
        "spec":"docs/specs/x.md","dependencies":["F000"]}
b = hs.render_block(feat)
check("block has begin marker", "<!-- harness:begin" in b)
check("block has end marker", "<!-- harness:end -->" in b)
check("block has task list", "- [ ] c1" in b and "- [ ] c2" in b)
check("block has out_of_scope", "not this" in b)
check("block has spec link", "docs/specs/x.md" in b)
check("block has dependency ref", "F000" in b)

# 3. split_body 必须逐字节保留区块外内容（验收 4 的地基）
human_before = "PM 写的背景\n\n"
human_after  = "\n\n评审意见：注意并发\n最后一行无换行"
body = human_before + b + human_after
before, block, after = hs.split_body(body)
check("split preserves before byte-exact", before == human_before)
check("split preserves after byte-exact",  after == human_after)
check("split returns the block", block is not None and "harness:begin" in block)

# 4. replace_block 替换而非追加；无标记时追加且只追加一次
feat2 = dict(feat); feat2["name"] = "alpha2"; feat2["acceptance_criteria"] = ["c3"]
nb = hs.render_block(feat2)
out = hs.replace_block(body, nb)
check("replace keeps human before", out.startswith(human_before))
check("replace keeps human after",  out.endswith(human_after))
check("replace swapped content", "- [ ] c3" in out and "- [ ] c1" not in out)
check("replace did not duplicate markers", out.count("harness:begin") == 1)

no_marker = "只有人写的正文"
out2 = hs.replace_block(no_marker, nb)
check("append when no marker", out2.startswith(no_marker) and "harness:begin" in out2)
check("append exactly once", out2.count("harness:begin") == 1)

# 5. round-trip 幂等：同一 feature 渲染两次结果相同（验收 3 的地基）
check("render deterministic", hs.render_block(feat) == hs.render_block(feat))
print("PASS")
PY
