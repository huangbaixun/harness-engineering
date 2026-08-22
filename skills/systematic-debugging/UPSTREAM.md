# Upstream provenance: systematic-debugging

- **Source:** superpowers v6.3.0
- **Commit SHA:** b36e0829c6d0140e93cfef2ca599b1b07d4a7797
- **Forked at:** 2026-05-23 (initial vendor at v5.1.0, SHA f2cbfbefebbfef77321e4c9abc9e949826bea9d7)
- **Last synced:** 2026-08-22 (v5.1.0 → v6.3.0)

## Local divergences (intentional)
- `name:` frontmatter is `harness:systematic-debugging` (was `systematic-debugging`) — required to namespace into the harness plugin.
- A single pointer line inserted between the frontmatter and the body, pointing readers to `harness-delta.md`.
- One blank line on each side of the pointer blockquote for readability.

Everything else in `SKILL.md` is byte-for-byte upstream. Companion files are byte-for-byte upstream with no edits at all.

## Vendored companion files (upstream, unmodified)
- `CREATION-LOG.md`
- `condition-based-waiting-example.ts`
- `condition-based-waiting.md`
- `defense-in-depth.md`
- `find-polluter.sh`
- `root-cause-tracing.md`
- `test-academic.md`
- `test-pressure-1.md`
- `test-pressure-2.md`
- `test-pressure-3.md`

## Upstream changes we deliberately did NOT adopt
- (none — this sync took v6.3.0 in full)
