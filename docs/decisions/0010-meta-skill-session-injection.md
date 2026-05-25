# ADR-0010: Meta-skill enforcement via SessionStart injection

## Status
Accepted — 2026-05-25

## Context
ADR-0008 vendored superpowers v5.1.0. ADR-0009 carved out `using-harness` as a harness-original meta-skill mirroring superpowers' `using-superpowers` pattern (the "1% rule" forced-trigger protocol).

Analyzing the upstream mechanism more carefully reveals that the soul of the design is **not** the meta-skill file itself, but the *injection path*:

1. Claude Code's SessionStart hook output is delivered to the model as session-prefix context on every startup / clear / compact.
2. `obra/superpowers` uses this channel to inject the full body of `using-superpowers` (wrapped in `<EXTREMELY_IMPORTANT>` sentinels).
3. The result: the model sees the meta-protocol *before generating its first token of any response*, including before clarifying questions.

In this repo today:
- `skills/using-harness/SKILL.md` exists (ADR-0009).
- `scripts/session-start.sh` runs on SessionStart and outputs progress/features summaries.
- **But the hook never injects `using-harness` content.** The enforcement loop is broken: the catalog and "1% rule" sit in a file the model has no reason to load at turn start.

Without injection, `using-harness` is a passive document equivalent in strength to CLAUDE.md — it works only when the model elects to read it, which is exactly the failure mode the meta-skill is supposed to prevent.

## Decision
Extend `scripts/session-start.sh` to inject the body of `skills/using-harness/SKILL.md` into SessionStart output, before the progress/features summary.

**Injection format:**
- Wrap in `<EXTREMELY_IMPORTANT>...</EXTREMELY_IMPORTANT>` sentinels (mirrors upstream — load-bearing for instruction priority).
- Emit the SKILL.md body verbatim from the file (no inline duplication in the hook script).
- Order: meta-skill block first, then existing "Harness SessionStart — 仪式性启动链" output.

**Source-of-truth rule:**
- `skills/using-harness/SKILL.md` remains the single source. The hook reads from the file at runtime.
- If the file path moves, `sync-superpowers.sh` and any vendoring tools must be updated atomically.

## Considered alternatives
- **Rely on CLAUDE.md to carry the meta-protocol** — rejected: CLAUDE.md is passive (loaded into context but not flagged as priority instruction), and the model has no forcing function to consult the skill catalog before answering.
- **Embed meta-skill content directly in `plugin.json` description / system prompt** — rejected: Claude Code plugin manifest does not expose a per-session prefix; description is static metadata, not injected context.
- **Per-skill activation triggers only** (no meta layer) — rejected: defeats the purpose. Without a meta-skill announcing "check the catalog first," each individual skill's trigger description must compete for the model's attention, and there is no enforcement of the "1% rule."
- **Inline the meta-skill body inside `session-start.sh`** — rejected: duplicates the SKILL.md content, breaks ADR-0009's single-source convention, and creates a divergence risk between what the hook injects and what `/harness:using-harness` reads.

## Consequences
**Positive:**
- Enforcement strength matches `obra/superpowers` — the protocol is unavoidable, not opt-in.
- `using-harness` becomes load-bearing rather than ornamental, justifying its place in ADR-0009's harness-original carve-out.
- Keeps SKILL.md as the single source of truth; the hook is a thin reader.

**Negative:**
- Every session pays the token cost of injecting the meta-skill body (~60 lines today). Mitigation: keep `using-harness` SKILL.md tight; do not let it grow into a documentation dumping ground.
- Couples `scripts/session-start.sh` to the path `skills/using-harness/SKILL.md`. Any rename requires updating the hook in the same commit. Codify this in `references/hook-patterns.md`.
- Increases user-visible startup noise unless we use stderr or the `additional context` channel correctly. Test on real Claude Code sessions before merging.

## Implementation
1. Modify `scripts/session-start.sh` — prepend a block that reads `${CLAUDE_PLUGIN_ROOT:-.}/skills/using-harness/SKILL.md`, strips YAML frontmatter, wraps in `<EXTREMELY_IMPORTANT>` sentinels, and echoes before the existing progress summary.
2. Add a Windows equivalent in `scripts/session-start.cmd`.
3. Add an eval in `skills/using-harness/evals/evals.json` asserting that after SessionStart, the model treats the "1% rule" as active (test prompt: an action that should trigger a skill check; assert the skill is invoked, not bypassed).
4. Update `references/hook-patterns.md` with a new row documenting the injection pattern and the rename-coupling caveat.
5. Note in ADR-0009's "Consequences" that `using-harness` is now load-bearing (cross-link this ADR).

## Related
- ADR-0008 (vendor superpowers v5.1.0)
- ADR-0009 (harness-delta sidecar — defines `using-harness` as harness-original)
- `references/hook-patterns.md` (SessionStart hook conventions)
- Upstream pattern: `obra/superpowers` `using-superpowers` SessionStart injection
