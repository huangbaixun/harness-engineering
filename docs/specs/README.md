# docs/specs/

This directory holds design specs produced by `harness:brainstorming`.

## Convention
- Filename: `YYYY-MM-DD-<topic>-design.md`
- Front-matter (required):

```yaml
---
date: YYYY-MM-DD
topic: <slug>
type: feature | adr-proposal | exploration
status: proposed | building | done
features: [<features.json-id>, ...]   # required when type=feature
adr: [<NNNN>, ...]                    # required when type=adr-proposal
superseded_by: <path>                 # optional
---
```

## Spec ↔ features.json linkage
- `type: feature` requires one or more entries in `features.json`, each with a `spec:` pointer back to this file (back-reference).
- `type: adr-proposal` requires one or more ADR files under `docs/decisions/`.
- `type: exploration` may dangle as historical record.

## Migration note
Earlier specs under `docs/superpowers/specs/` (pre-v2.0.0 default location) are migrated here in Phase 3 of the superpowers integration project. New specs always land in `docs/specs/`.
