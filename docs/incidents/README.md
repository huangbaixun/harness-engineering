# docs/incidents/

This directory holds debug notes produced by `harness:systematic-debugging`.

## Convention
- Filename: `YYYY-MM-DD-<slug>.md`
- Each incident note should record:
  - Symptom observed
  - Reproduction steps
  - Root cause (or hypothesis if unresolved)
  - Fix applied (or escalation path if still open)
  - Whether the incident invalidated any ADR assumption — if so, link the affected ADR and update its **Consequences** section

## Cross-skill triggers
- Production incidents may invoke `harness:canary` rollback procedures.
- Incidents tied to a `features.json` entry should set that entry's status or link back via `related_files`.
