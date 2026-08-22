# ADR-0009: harness-delta sidecar 4-file convention for vendored skills

## Status
Accepted — 2026-05-23

## Context
ADR-0008 commits to vendoring 13 superpowers skills with local rules layered on top (integration with `features.json`, ADRs, docs). The structural question is *where* those local rules live without polluting upstream content.

Three patterns were considered during brainstorming (recorded in `docs/specs/2026-05-23-superpowers-integration-design.md` §2):

1. **Inline delta** in `SKILL.md` (the pattern used by the previous v1.x forks)
2. **Sidecar delta file** alongside an unmodified upstream `SKILL.md`
3. **Wrapper skill** that calls the upstream skill and adds checks

## Decision
Each vendored skill directory contains exactly four files:

```
skills/<name>/
├── SKILL.md           # superpowers v5.1.0 content verbatim, only frontmatter `name` changed + one pointer line inserted
├── harness-delta.md   # harness-specific integrations (features.json / ADR / docs / Stop Hook contract)
├── UPSTREAM.md        # provenance: source commit SHA, last-sync date, intentional divergences
└── evals/
    └── evals.json     # per ADR-0004; tests that harness-delta behavior takes effect
```

`using-harness` is **exempt** (harness-original skill, no upstream); it has 2 files: `SKILL.md` + `evals/evals.json`.

## Allowed edits to vendored `SKILL.md`
Only two:
1. `name:` frontmatter field becomes `harness:<upstream-name>`
2. One pointer line inserted after the frontmatter:
   > **harness local rules:** Always read [harness-delta.md](./harness-delta.md) before invoking this skill. It defines mandatory integrations with features.json, ADR, and docs.

All other content is byte-for-byte upstream.

## Considered alternatives
- **Inline delta** — rejected: makes upstream sync diff noisy and error-prone
- **Wrapper skill** — rejected: duplicates 99% of content; two "session-start" meta skills conflict

## Consequences
**Positive:**
- Upstream diffs stay clean — sync workflow (Section 11 of integration spec) becomes mechanical
- Local rules are independently editable and lint-able
- Provenance per skill is explicit (UPSTREAM.md)

**Negative:**
- Agents must load two files per skill invocation
- Discipline required: SKILL.md body must never be edited outside the two allowed changes

**Amendment — 2026-08-22 (superpowers v6.3.0 sync):**
The "exactly four files" wording was written when every vendored skill happened to be a single upstream `SKILL.md`. It never
was: upstream ships companion files next to several skills (`brainstorming/visual-companion.md`, `requesting-code-review/code-reviewer.md`,
`systematic-debugging/root-cause-tracing.md`, `subagent-driven-development/*-prompt.md` and `scripts/`, …), and the initial
v5.1.0 vendor silently dropped them — leaving live links in our `SKILL.md` bodies pointing at files that did not exist.

The convention is therefore **four harness files plus whatever companion files upstream ships for that skill**:

```
skills/<name>/
├── SKILL.md            # upstream verbatim, only the 2 allowed edits
├── <companions>        # upstream verbatim, ZERO edits (md, scripts, examples — whatever upstream ships)
├── harness-delta.md    # harness-only
├── UPSTREAM.md         # harness-only; lists the vendored companion files
└── evals/evals.json    # harness-only
```

Companion files get **no** allowed edits at all — not even the `name:` rewrite, since they carry no frontmatter. `UPSTREAM.md`
lists them so a sync can tell "upstream deleted this" from "we forgot to copy it".

Two consequences follow. First, the ≤500-line SKILL.md cap in CLAUDE.md now reads as harness-original-only; upstream's
`writing-skills` (681 lines) and `subagent-driven-development` (570) exceed it, and trimming them would break the verbatim
guarantee. Second, `using-superpowers` stays un-vendored (harness ships `using-harness`), so the handful of
`../using-superpowers/references/*` links in upstream bodies are inert here — recorded per-skill under "deliberately did NOT
adopt" rather than patched, since those files document Codex/Gemini runtimes and ADR-0007 scopes this plugin to Claude Code.

**Load-bearing note (added per ADR-0010):**
`using-harness` is no longer ornamental — its SKILL.md body is read by the SessionStart hook on every conversation start and injected as session context. Renaming the file or changing its path requires a coordinated update to `scripts/session-start` in the same commit, and the body must stay tight (the cost is paid every session).

## Implementation
Phase 1 of `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` applies this convention to the 4 renamed forks. Phase 2 (separate plan) applies it to the 10 new vendored skills.

## Related
- ADR-0004 (skill-creator methodology)
- ADR-0008 (vendor superpowers v5.1.0)
- ADR-0010 (meta-skill SessionStart injection — makes `using-harness` load-bearing)
