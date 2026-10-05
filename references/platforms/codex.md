# Codex platform adapter

## Scope

Supports project-scoped skills and a separate Codex plugin entrypoint. Choose one delivery; installing skills does not register hooks. Project resources use `.agents/harness` as runtime root; plugin resources use the installed plugin root. Read local project instructions first.

## Tools and workflow

Read skill files from disk when there is no Skill tool. Use actual available shell, patch, clarification and agent tools; never fabricate calls to Claude's Skill/AskUserQuestion/Task tools. User scope and host instruction hierarchy remain authoritative. Use a fresh reviewer when available and required by the selected execution workflow; otherwise disclose self-review.

Resolve harness-original skill names through the discovered catalog. Vendored upstream cross-links such as `superpowers:writing-plans` refer to the corresponding local `harness:writing-plans` implementation and its sidecar. With project delivery, resolve `skills/<name>` at `.agents/skills/<name>`; references/scripts/templates are under `.agents/harness`.

## Lifecycle

Codex reads AGENTS.md and `.agents/skills`; portable root plugin.json declares skills and extensions.com.openai.hooks pointing to hooks/codex.json. This inline object replaces the entire compatibility overlay, so its explicit hook override must remain. Do not load Claude hooks/hooks.json in Codex: it includes opt-in Issue operations and a different path guard. No sync or auto-commit occurs in the Codex adapter. Claude also uses shared bounded context and real verification; its old auto-commit default is retired.

Use `python3 .agents/harness/scripts/codex_hook.py verify --project .` in project mode, or the same script under plugin root in plugin mode. A verification command is an argv array, not shell text. Empty configuration is not successful verification. Legacy progress is read-only fallback.

Native hooks must be reviewed/trusted through `/hooks`; never bypass trust. Project mode does not modify `.codex/config.toml` or global config automatically. Unregistered PreTool protection is not a security barrier: native permissions remain the enforcement boundary.

## Version and evidence

Initial compatibility target: Codex CLI 0.158.0. CLI parsing/loading and representative workflow results are recorded separately in the platform smoke report. Codex App and Work Cloud are not assumed equivalent to CLI. Cloud orchestration may not support local shell hooks. Unknown tools and absent lifecycle capabilities require explicit disclosure and manual verification.

Sources (checked 2026-10-05):
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/hooks
- https://developers.openai.com/plugins/build/plugins

For long-running workflow decisions, read `references/gpt6-workflows.md` from the runtime root. Store checkpoints with `scripts/harness_state.py`; old progress files remain untouched.

Codex plugin discovery automatically adds the plugin namespace: this source uses `harness:<name>`, so the local plugin loader reports `harness:harness:<name>`. Resolve actual discovered names rather than assuming project and plugin names are identical; project discovery remains `harness:<name>`. This preserves the shared source and ADR-0009 namespace constraint.
