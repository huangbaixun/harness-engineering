# harness-delta: systematic-debugging

## Upstream
superpowers v6.3.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Bug scope tracking
Every bug investigation must be either:
- **Tied to a feature**: reference the `features.json` `id` of the affected feature in the debug note's metadata.
- **Standalone bug**: use the `bug:` prefix convention in the incident filename: `docs/incidents/YYYY-MM-DD-bug-<slug>.md`

This ensures bugs don't become orphan work that bypasses feature accountability.

### docs/incidents/ output
Debug notes must be written to `docs/incidents/YYYY-MM-DD-<slug>.md` per the convention established in Plan A. Each note should record (per `docs/incidents/README.md`):
- Symptom observed
- Reproduction steps
- Root cause (or hypothesis if unresolved)
- Fix applied (or escalation path if open)
- ADR invalidation check

### ADR invalidation check
If debugging reveals that a bug exists because an ADR's stated assumption is wrong (e.g., "we assumed X always holds" → bug shows X can fail), this skill MUST:
1. Identify the affected ADR by number
2. Open the ADR file and append to its `## Consequences` section: a dated bullet noting the invalidated assumption + how the bug manifested
3. Reference the ADR number in the incident note

Silent workarounds (fixing the bug without updating the ADR) are **prohibited** — they leave architectural debt.

### Production incident → harness:canary
For production incidents (not test/dev), surface `harness:canary` for rollback planning. Do not auto-invoke.

## Soft hints
- Reproduce before diagnosing — assume the bug is real until proven otherwise.
- Bisect aggressively for regressions.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: every debug session produces a docs/incidents/ note tied to a feature or with bug: prefix
- with-skill: ADR-invalidating bugs result in ADR Consequences update
- baseline: bugs may be fixed silently without ADR or features.json tracking
