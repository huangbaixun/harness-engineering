# Harness Engineering contributor guide

- Read CLAUDE.md for repository conventions and docs/decisions/ for rationale.
- Shared resources: skills/, features.json, ADRs. Platform adapters must preserve Claude behavior.
- Python 3.10+ standard library and Bash; local checks must not need credentials or network.
- Run `python3 scripts/validate.py`; it validates structure and all offline regression files.
- Dependency direction: references → templates → skills → commands. Hooks are standalone deterministic scripts.
- Never overwrite existing project instructions or install global configuration implicitly.
- New/modified skills require skill-creator baseline/with-skill evaluation per ADR-0004.
- Vendored SKILL.md allows only namespace and sidecar pointer edits; companions retain upstream bytes and provenance.
- Operational hooks are silent on success; SessionStart context is intentional protocol output.
- Project initialization defaults to no auto-commit, Issue sync, push or deploy. Do not run this repository's opt-in Issue hooks as a development check.
- Keep framework adaptation and consuming-product changes separately reviewable.
