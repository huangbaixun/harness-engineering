# Upstream provenance: finishing-a-development-branch

- **Source:** superpowers v6.3.0
- **Commit SHA:** b36e0829c6d0140e93cfef2ca599b1b07d4a7797
- **Forked at:** 2026-05-23 (initial vendor at v5.1.0, SHA f2cbfbefebbfef77321e4c9abc9e949826bea9d7)
- **Last synced:** 2026-08-22 (v5.1.0 → v6.3.0)

## Local divergences (intentional)
- `name:` frontmatter is `harness:finishing-a-development-branch` (was `finishing-a-development-branch`) — required to namespace into the harness plugin.
- A single pointer line inserted between the frontmatter and the body, pointing readers to `harness-delta.md`.
- One blank line on each side of the pointer blockquote for readability.

Everything else in `SKILL.md` is byte-for-byte upstream. Companion files are byte-for-byte upstream with no edits at all.

## Vendored companion files (upstream, unmodified)
- (none — this skill is a single `SKILL.md` upstream)

## Upstream changes we deliberately did NOT adopt
- (none) — note that the v5.1.0 vendor carried a locally-extended `description:` ("...- guides completion of development work by presenting structured options for merge, PR, or cleanup"). That edit was outside the two allowed by ADR-0009 and undocumented; this sync reverts it to the upstream description.
