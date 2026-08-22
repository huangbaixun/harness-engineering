# Upstream provenance: writing-skills

- **Source:** superpowers v6.3.0
- **Commit SHA:** b36e0829c6d0140e93cfef2ca599b1b07d4a7797
- **Forked at:** 2026-05-23 (initial vendor at v5.1.0, SHA f2cbfbefebbfef77321e4c9abc9e949826bea9d7)
- **Last synced:** 2026-08-22 (v5.1.0 → v6.3.0)

## Local divergences (intentional)
- `name:` frontmatter is `harness:writing-skills` (was `writing-skills`) — required to namespace into the harness plugin.
- A single pointer line inserted between the frontmatter and the body, pointing readers to `harness-delta.md`.
- One blank line on each side of the pointer blockquote for readability.

Everything else in `SKILL.md` is byte-for-byte upstream. Companion files are byte-for-byte upstream with no edits at all.

## Vendored companion files (upstream, unmodified)
- `anthropic-best-practices.md`
- `examples/CLAUDE_MD_TESTING.md`
- `graphviz-conventions.dot`
- `persuasion-principles.md`
- `render-graphs.js`
- `testing-skills-with-subagents.md`

## Upstream changes we deliberately did NOT adopt
- `../using-superpowers/references/codex-tools.md` and `../using-superpowers/references/gemini-tools.md` — linked from the SKILL.md body but NOT vendored. Those files document skill paths for Codex / Gemini CLI runtimes; ADR-0007 scopes this plugin to Claude Code, and the same sentence already states the Claude Code path (`~/.claude/skills/`) inline, so nothing our audience needs is lost. The two links are inert by design.
