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

## Implementation
Phase 1 of `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` applies this convention to the 4 renamed forks. Phase 2 (separate plan) applies it to the 10 new vendored skills.

## Related
- ADR-0004 (skill-creator methodology)
- ADR-0008 (vendor superpowers v5.1.0)
