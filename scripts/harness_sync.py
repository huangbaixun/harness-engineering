#!/usr/bin/env python3
"""features.json ↔ GitHub/GHE Issue 双向同步。

设计依据：docs/specs/2026-08-22-features-github-sync-design.md
          ADR-0011（字段单写所有权）、ADR-0012（features.json 规范位置）

核心性质：每个字段恰好一个写方，因此对账是无状态纯函数 ——
harness 域无条件推、GitHub 域无条件拉，不需要时间戳或 content hash。
影子副本仅用于算差异集，丢失则退化为全量对账，结果一致。

所有 gh 调用经由 $HARNESS_GH_BIN（默认 gh），使测试可注入桩程序、离线可跑。
"""
# 兼容 Python 3.7+：macOS 系统自带 3.9，插件要分发给用户项目，
# 不能要求对方升级解释器。故用 __future__ 注解而非 3.10 的 X | Y 运行时语法。
from __future__ import annotations

import json
import os
import subprocess
import sys

BEGIN = "<!-- harness:begin  自动生成，勿手改；要改请编辑 features.json -->"
END = "<!-- harness:end -->"

# 字段所有权（ADR-0011）。改这里等于改契约，须同步更新 ADR。
HARNESS_OWNED = ("name", "description", "acceptance_criteria", "out_of_scope",
                 "spec", "dependencies", "status")
GITHUB_OWNED = ("priority", "delivery_state", "assignee", "milestone")
NOT_SYNCED = ("technical_notes", "related_files")


def gh_bin() -> str:
    return os.environ.get("HARNESS_GH_BIN", "gh")


def resolve_features_path(root: str = ".") -> str | None:
    """ADR-0012：根目录优先，docs/ 为兼容旧项目的永久回退。"""
    for rel in ("features.json", "docs/features.json"):
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            return p
    return None


def load_config(features: dict) -> dict | None:
    """返回 github 配置块；未配置或 enabled 非真时返回 None。

    返回 None 是「零网络调用」保证的唯一入口 —— 调用方见 None 即整段跳过。
    """
    if not isinstance(features, dict):
        return None
    cfg = features.get("github")
    if not isinstance(cfg, dict) or cfg.get("enabled") is not True:
        return None
    return cfg


def render_block(feature: dict) -> str:
    """渲染托管区块。必须是确定性的 —— 幂等比对依赖它。"""
    lines = [BEGIN, ""]
    desc = (feature.get("description") or "").strip()
    if desc:
        lines += [desc, ""]

    ac = feature.get("acceptance_criteria") or []
    if ac:
        lines.append("**验收标准**")
        lines += [f"- [ ] {c}" for c in ac]
        lines.append("")

    oos = feature.get("out_of_scope") or []
    if oos:
        lines.append("**不在范围内**")
        lines += [f"- {c}" for c in oos]
        lines.append("")

    spec = (feature.get("spec") or "").strip()
    if spec:
        lines += [f"**设计文档：** `{spec}`", ""]

    deps = feature.get("dependencies") or []
    if deps:
        lines += ["**依赖：** " + ", ".join(f"`{d}`" for d in deps), ""]

    lines.append(END)
    return "\n".join(lines)


def split_body(body: str) -> tuple[str, str | None, str]:
    """切分为 (before, block, after)。区块外内容必须逐字节保留。"""
    body = body or ""
    i = body.find(BEGIN)
    if i == -1:
        return body, None, ""
    j = body.find(END, i)
    if j == -1:
        return body, None, ""
    j += len(END)
    return body[:i], body[i:j], body[j:]


def replace_block(body: str, new_block: str) -> str:
    """替换托管区块；无标记时追加到末尾（只追加一次，绝不重复）。"""
    before, block, after = split_body(body)
    if block is None:
        sep = "" if not before or before.endswith("\n") else "\n\n"
        return before + sep + new_block
    return before + new_block + after


# ── 并发锁 ─────────────────────────────────────────────────────────────────

LOCK = os.path.join(".harness", "sync.lock")


def acquire_lock():
    """mkdir 原子锁。拿不到即返回 False —— 绝不等待。

    Stop hook 不该因为另一个会话在同步就把人卡住；跳过一次，下次会话自然补上。
    """
    try:
        os.makedirs(os.path.dirname(LOCK), exist_ok=True)
        os.mkdir(LOCK)
        return True
    except FileExistsError:
        return False
    except OSError:
        return False


def release_lock():
    try:
        os.rmdir(LOCK)
    except OSError:
        pass


# ── gh 调用 ────────────────────────────────────────────────────────────────

class GhError(Exception):
    """gh 调用失败。kind 用于区分处理方式：offline 可重试自愈，auth 不能。"""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind
        self.detail = detail


def _classify(stderr: str) -> str:
    s = (stderr or "").lower()
    if "401" in s or "bad credentials" in s or "authentication" in s:
        return "auth"
    if "403" in s or "rate limit" in s:
        return "ratelimit"
    if "404" in s or "not found" in s:
        return "notfound"
    if "connect" in s or "network" in s or "dial tcp" in s or "timeout" in s:
        return "offline"
    # 用法错误不可自愈，提示成「稍后重试」会让人一直不去查真实原因
    if "unknown flag" in s or "unknown command" in s or "unknown shorthand" in s:
        return "usage"
    return "unknown"


def gh(args, cfg, timeout=30, check=True):
    cmd = [gh_bin()] + list(args)
    host = (cfg or {}).get("host")
    env = None
    if host and host not in ("github.com",):
        # gh 的 --hostname 只有 auth 系子命令认；issue / label 一律靠 GH_HOST
        # 环境变量选主机。曾经写成 cmd += ["--hostname", host]，导致所有 GHE
        # 项目的每一次 gh 调用都以 "unknown flag" 失败，且被 _classify 误判为
        # 网络问题而静默重试 —— github.com 走白名单分支，永远暴露不出来。
        env = dict(os.environ, GH_HOST=host)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
    except FileNotFoundError:
        raise GhError("nogh", "gh CLI 未安装")
    except subprocess.TimeoutExpired:
        raise GhError("offline", f"gh 调用超时（{timeout}s）")
    if check and p.returncode != 0:
        raise GhError(_classify(p.stderr), (p.stderr or "").strip().splitlines()[0] if p.stderr else "gh 失败")
    return p.stdout


def repo_slug(cfg):
    if cfg.get("repo"):
        return cfg["repo"]
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return None
    if not url:
        return None
    url = url.removesuffix(".git") if hasattr(str, "removesuffix") else (
        url[:-4] if url.endswith(".git") else url)
    if url.startswith("git@"):
        url = url.split(":", 1)[-1]
    else:
        parts = url.split("/")
        if len(parts) >= 2:
            url = "/".join(parts[-2:])
    return url or None


# ── 状态与 label ───────────────────────────────────────────────────────────

def status_label(cfg, status):
    return f"{cfg.get('label_prefix', 'harness')}/{status}"


def harness_labels(cfg, names):
    """只返回带 harness/ 前缀的 label —— 其余一律只读（验收 6）。"""
    pre = cfg.get("label_prefix", "harness") + "/"
    return [n for n in names if n.startswith(pre)]


# ── 影子副本（纯性能优化，丢失则退化为全量对账）────────────────────────────

SHADOW = os.path.join(".harness", "last-synced.json")


def load_shadow():
    try:
        with open(SHADOW, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_shadow(mapping):
    os.makedirs(os.path.dirname(SHADOW), exist_ok=True)
    with open(SHADOW, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def harness_fingerprint(feature):
    """harness 域字段的指纹，用于算差异集。不承担正确性。"""
    return {k: feature.get(k) for k in HARNESS_OWNED}


# ── push ───────────────────────────────────────────────────────────────────

def list_issues(cfg, slug, with_body=False):
    fields = "number,labels,assignees,milestone,state,title"
    if with_body:
        fields += ",body"
    # 不用 `--label <prefix>` 过滤：gh 的 --label 是精确匹配，而真实 label 叫
    # harness/done、harness/track…，裸前缀 "harness" 这个 label 并不存在，
    # 用它过滤会永远返回空；多个 --label 又是 AND 语义，也不能枚举。
    #
    # 也不在这里按前缀本地筛：已经有 github_issue 指向的 Issue 必须始终可达，
    # 否则有人在 GitHub 上拿掉 harness/ label，该 feature 就静默停止同步了。
    # 前缀/track 筛选只用于**入站发现**（见 cmd_pull），不影响已建立的链接。
    out = gh(["issue", "list", "--repo", slug, "--state", "all",
              "--limit", "500", "--json", fields], cfg)
    try:
        issues = json.loads(out or "[]")
    except json.JSONDecodeError:
        return []
    return issues


def list_labels(cfg, slug):
    try:
        out = gh(["label", "list", "--repo", slug, "--limit", "200", "--json", "name"], cfg)
        return {l.get("name") for l in json.loads(out or "[]")}
    except (GhError, json.JSONDecodeError):
        return set()


def ensure_labels(cfg, slug, wanted):
    """创建缺失的 harness/ 前缀 label。

    只创建带前缀的；非前缀 label 一律不碰 —— 连「P1 不存在就代建」都不做，
    那是 GitHub 域，不归 harness 管（ADR-0011）。
    没有这一步，首次接入的仓库上 `gh issue create --label harness/xxx` 会直接失败。
    """
    pre = cfg.get("label_prefix", "harness") + "/"
    wanted = {w for w in wanted if w and w.startswith(pre)}
    if not wanted:
        return
    existing = list_labels(cfg, slug)
    for name in sorted(wanted - existing):
        try:
            gh(["label", "create", name, "--repo", slug,
                "--description", "managed by harness (F005)", "--color", "0E8A16"], cfg)
        except GhError:
            pass          # label 建不出来不该阻断同步；后续 issue 操作会自然报错


def cmd_push(dry_run=False, limit=20, root=".", require_lock=False):
    path = resolve_features_path(root)
    if not path:
        return 0
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # features.json 坏了不是同步的职责去报，静默跳过
        return 0
    holding = False
    if require_lock and not dry_run:
        if not acquire_lock():
            return 0                  # 另一个会话正在同步，跳过而非等待
        holding = True
    try:
        return _push_locked(data, path, dry_run, limit)
    finally:
        if holding:
            release_lock()


def _issue_number(create_output):
    """从 `gh issue create` 的输出 URL 末段解析 Issue 编号。"""
    for tok in reversed((create_output or "").strip().split()):
        tail = tok.rstrip("/").rsplit("/", 1)[-1]
        if tail.isdigit():
            return int(tail)
    return None


def _push_locked(data, path, dry_run, limit):
    features_dirty = [False]
    cfg = load_config(data)
    if cfg is None:
        return 0                      # 未配置 -> 零网络调用（验收 1）
    slug = repo_slug(cfg)
    if not slug:
        return 0

    shadow = load_shadow()
    feats = data.get("features", [])
    dirty = [f for f in feats
             if shadow.get(f.get("id")) != harness_fingerprint(f)]
    if not dirty:
        return 0

    issues = {i.get("number"): i for i in list_issues(cfg, slug, with_body=True)}
    if not dry_run:
        ensure_labels(cfg, slug,
                      {status_label(cfg, f.get("status", "")) for f in dirty})

    deferred = 0
    if limit is not None and len(dirty) > limit:
        deferred = len(dirty) - limit
        dirty = dirty[:limit]

    pushed = 0
    for feat in dirty:
        num = feat.get("github_issue")
        block = render_block(feat)
        if num and num in issues:
            cur = issues[num].get("body") or ""
            _, cur_block, _ = split_body(cur)
            if cur_block == block:
                # 内容一致 -> 不 PATCH。每次 PATCH 都会通知所有 watcher（验收 3）
                shadow[feat.get("id")] = harness_fingerprint(feat)
                continue
            new_body = replace_block(cur, block)
            if dry_run:
                print(f"[dry-run] 将更新 Issue #{num} ({feat.get('id')})")
            else:
                args = ["issue", "edit", str(num), "--repo", slug, "--body", new_body]
                st = status_label(cfg, feat.get("status", ""))
                if st and st not in [l.get("name") for l in issues[num].get("labels", [])]:
                    args += ["--add-label", st]
                    for old in harness_labels(cfg, [l.get("name") for l in issues[num].get("labels", [])]):
                        if old != st and old.rsplit("/", 1)[0] == cfg.get("label_prefix", "harness"):
                            args += ["--remove-label", old]
                gh(args, cfg)
            pushed += 1
        elif not num:
            if dry_run:
                print(f"[dry-run] 将创建 Issue（{feat.get('id')} {feat.get('name')}）")
            else:
                out = gh(["issue", "create", "--repo", slug, "--title", feat.get("name") or feat.get("id"),
                          "--body", block, "--label", status_label(cfg, feat.get("status", ""))], cfg)
                # 回写编号：github_issue 是持久锚点。缺了它，影子（可丢弃）一旦丢失
                # 就会重复创建 Issue —— 直接推翻「对账无状态」这条核心性质。
                new_num = _issue_number(out)
                if new_num is not None:
                    feat["github_issue"] = new_num
                    features_dirty[0] = True
            pushed += 1
        if not dry_run:
            shadow[feat.get("id")] = harness_fingerprint(feat)

    if deferred:
        # 绝不静默截断（验收 7）。报实际写入数而非候选数 —— 候选可能因内容一致
        # 而被跳过，说成「已推送」就是谎报。
        print(f"[harness-sync] 本次检查 {limit} 条（实际写入 {pushed} 条），"
              f"另有 {deferred} 条未检查；再次运行以继续。", file=sys.stderr)
    if not dry_run:
        save_shadow(shadow)
        if features_dirty[0]:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
    return 0


# ── pull ───────────────────────────────────────────────────────────────────

def _delivery_state(issue, cfg):
    """delivery_state 由 state/* label 决定；缺失时用 Issue 开关态兜底。"""
    for l in issue.get("labels") or []:
        n = l.get("name") or ""
        if n.startswith("state/"):
            return n.split("/", 1)[1]
    return "shipped" if (issue.get("state") or "").upper() == "CLOSED" else "triage"


def _priority(issue):
    for l in issue.get("labels") or []:
        n = (l.get("name") or "").strip()
        if len(n) == 2 and n[0] in "Pp" and n[1].isdigit():
            return int(n[1])
    return None


def cmd_pull(timeout=30, root="."):
    path = resolve_features_path(root)
    if not path:
        return 0
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return 0
    cfg = load_config(data)
    if cfg is None:
        return 0                      # 未配置 -> 零网络调用（验收 1）
    slug = repo_slug(cfg)
    if not slug:
        return 0

    issues = list_issues(cfg, slug)
    by_num = {i.get("number"): i for i in issues}
    feats = data.get("features", [])
    changed = False

    # 1) GitHub 域字段回流。harness 域一概不碰 —— 单写所有权（ADR-0011）
    for feat in feats:
        num = feat.get("github_issue")
        if not num or num not in by_num:
            continue
        iss = by_num[num]
        updates = {
            "delivery_state": _delivery_state(iss, cfg),
            "assignee": (iss.get("assignees") or [{}])[0].get("login") if iss.get("assignees") else None,
            "milestone": (iss.get("milestone") or {}).get("title") if iss.get("milestone") else None,
        }
        pr = _priority(iss)
        if pr is not None:
            updates["priority"] = pr
        for k, v in updates.items():
            if feat.get(k) != v:
                feat[k] = v
                changed = True

    # 2) 入站：带 track_label 且无对应 feature 的 Issue -> proposed stub（验收 5）
    track = cfg.get("track_label", f"{cfg.get('label_prefix', 'harness')}/track")
    known = {f.get("github_issue") for f in feats if f.get("github_issue")}
    existing_ids = {f.get("id") for f in feats}
    for iss in issues:
        num = iss.get("number")
        names = [l.get("name") for l in (iss.get("labels") or [])]
        if num in known or track not in names:
            continue                  # 不带 track 标签的 Issue 一律不碰
        n = 1
        while f"F{n:03d}" in existing_ids:
            n += 1
        new_id = f"F{n:03d}"
        existing_ids.add(new_id)
        feats.append({
            "id": new_id,
            "name": iss.get("title") or f"issue-{num}",
            "priority": _priority(iss) if _priority(iss) is not None else 3,
            "status": "proposed",
            "spec": "",
            "description": (iss.get("body") or "").strip(),
            "acceptance_criteria": [],   # 由 brainstorming 补齐结构
            "out_of_scope": [],
            "dependencies": [],
            "technical_notes": f"入站自 {slug}#{num}（{track}）；结构待 harness:brainstorming 补齐。",
            "related_files": [],
            "github_issue": num,
            "delivery_state": _delivery_state(iss, cfg),
            "assignee": (iss.get("assignees") or [{}])[0].get("login") if iss.get("assignees") else None,
            "milestone": (iss.get("milestone") or {}).get("title") if iss.get("milestone") else None,
        })
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0


# ── CLI ────────────────────────────────────────────────────────────────────

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 2
    cmd, rest = argv[0], argv[1:]

    def opt(name, default=None, cast=str):
        if name in rest:
            i = rest.index(name)
            if i + 1 < len(rest):
                return cast(rest[i + 1])
        return default

    try:
        if cmd == "pull":
            return cmd_pull(timeout=opt("--timeout", 30, int))
        if cmd == "push":
            return cmd_push(dry_run="--dry-run" in rest,
                            limit=opt("--limit", 20, int),
                            require_lock="--require-lock" in rest)
        if cmd == "status":
            return cmd_push(dry_run=True, limit=opt("--limit", 20, int))
        print(f"未知子命令：{cmd}", file=sys.stderr)
        return 2
    except GhError as e:
        # 失败恰好一行；离线可自愈、认证失效不能 —— 区别对待（spec §5）
        hint = {
            "auth": "认证已失效，运行 `gh auth login --hostname <host>` 后重试",
            "ratelimit": "触发 API 限流，稍后重试",
            "notfound": "目标 Issue 不存在，可能已被删除；请人工确认后清空 github_issue 或恢复 Issue",
            "nogh": "未找到 gh CLI，同步已跳过",
            "usage": "gh 调用参数有误，重试不会自愈，请提交 bug",
            "offline": "网络不可达，同步已跳过；下次会话自动重试",
            # 兜底不再冒充「网络不可达」：那句话在说「等等就好」，会让人不去查
            # 真实原因。分不出类就照实说分不出，并把 gh 原文带出来。
        }.get(e.kind, "同步失败，已跳过；若反复出现请附下方 gh 原文提交 bug")
        print(f"[harness-sync] {hint}（{e.detail}）", file=sys.stderr)
        return 0                      # 永不阻断（验收 2、8）


if __name__ == "__main__":
    sys.exit(main())
