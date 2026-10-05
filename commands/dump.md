---
description: Save a minimal neutral checkpoint for continuing approved work across sessions
---

Use `scripts/harness_state.py checkpoint --project <project> --task <current task>
--next-action <next step>` from the runtime root. Add --steering and --blocker when
relevant. Preserve extension fields and legacy progress; never write the legacy file.
Use the configured neutral path (default docs/harness-progress.json). Record durable
architectural decisions in an ADR. Saving state does not require ending the session,
committing, synchronizing Issues or marking a feature done.
