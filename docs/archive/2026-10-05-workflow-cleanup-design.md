---
date: 2026-10-05
topic: workflow-cleanup
type: feature
status: done
features: [F008]
adr: [0014]
archived_at: 2026-10-05T12:49:57.087887+00:00
completed_by: codex
feature_id: F008
---

# User-approved Harness workflow cleanup

Scope/order accepted by user: P0 defaults and real checks, P1 execution/context and
progress consistency, P2 evidence-based skills/evaluation and portable packaging.
Interfaces: shared runtime verify/context, Codex compatibility entry, Claude native
stdin adapter, neutral state checkpoint, initializer --tool codex|claude.

Defaults: no progress commits, empty formatter or telemetry; empty checks do not
pass. Existing settings/permission policies are untouched by adoption. Native hook
trust stays with the host. Narrow direct-path protection does not secure shell.

Preserve upstream bytes/provenance, compatibility manifests, opt-in Issue sync,
existing custom checks and project instructions. No AIDC edits, deployment or
credentials. See ADR 0014 and the implementation plan for decisions/verification.
