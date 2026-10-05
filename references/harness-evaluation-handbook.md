# Harness evaluation: observed outcomes

Use this reference when comparing or auditing Harness behavior. Inventory discovers
entrypoints; it does not establish health. HEval v1 remains a historical design in
[the archive](../docs/archive/2026-10-05-heval-v1-historical.md), not an implemented
harness:evaluate command. ADR 0014 supersedes its policy scores.

For each capability record the version/configuration, task, expected behavior,
observed result, artifacts and **pass / fail / unknown**. Unknown is mandatory when
no execution or measurement exists. Separate structural validation, adapter fixture
execution, trusted native host loading and product acceptance.

Compare no-skill control, prior-skill behavior and updated-skill behavior using the
same realistic scenarios and concrete assertions. Keep actual outputs and failures.
Disclose sample size and selection; a few samples do not prove general reliability.
Use a reviewable viewer/artifact. Do not grade only phrasing, headings or file presence.

Useful outcomes: scope-correct task completion, failures detected and propagated,
state restored, intervention count, measured latency and native host token/cost.
Do not estimate absent host costs as zero. Hook or instruction counts, universal
line/token quotas and automated-review claims are not substitutes for outcomes.

Include failures: empty/no-op checks, malformed events, staged user work, existing
settings, path spaces/symlinks, opt-in isolation, compaction and duplicate pipelines.
For runtime changes run offline regressions; for skill changes follow ADR 0004.
Retain permissions, licenses and provenance. No live Issue writes or deployment
are needed for local evaluations.
