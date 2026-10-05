---
name: harness:audit
description: Diagnose an existing Harness setup using observed agent failures, executable checks and platform configuration; produce prioritized repairs with evidence.
---

# Audit an existing Harness

Inspect the actual host configuration, project instructions, relevant skills and
scripts, test/CI entrypoints, runtime state and observed failures. Read only the
artifacts needed to establish a finding. Existing inventory is discovery data,
not a health score: a hook that exits zero without running checks is not validation.

Report each finding with evidence (file or observed run), behavior affected,
severity, repair and verification method. Use **pass / fail / unknown** for each
claim. Unknown includes checks not run, unavailable host token/cost measurements,
and untested hook lifecycle. Do not invent measurements or equate file presence,
more hooks, more commands or automatic formatting with better outcomes.

Prioritize reproduced side effects, broken checks and lost task state before
optional tuning. Pre-commit, CI, explicit checks and host hooks are valid control
points; their value depends on what they enforce. Verify configured argv commands
actually execute and failures propagate. Empty configurations never pass. Respect
native hook trust and permissions. A direct-path guard cannot secure arbitrary shell
commands; explain its actual coverage instead of promising a complete boundary.

Review instructions for stale/conflicting policy, unconditional startup work,
forced early termination, duplicate reviews and implicit external mutations.
Instruction length and module size are clues, not universal 60/300-line or 20k-token
limits. Keep project invariants and permission rules; move conditional details to
references only when useful. Native compaction should preserve checkpoints and
continue approved work.

Keep requirements in root features.json. New state writes use the configured
neutral progress file through scripts/harness_state.py; legacy progress is read-only.
For platform-specific diagnosis read references/platforms/codex.md or the host's
actual documentation. For evaluation design see references/harness-evaluation-handbook.md.

A requested audit produces findings. Implement repairs when already authorized;
otherwise present a concrete plan. Preserve existing instructions/configuration,
never infer permission for commits, Issue writes, pushes, deploys or account changes.
After repairs run relevant checks and inspect results; distinguish local adapter
coverage from real trusted-host loading.
