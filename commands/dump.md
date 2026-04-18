---
description: Save key decisions and progress from the current session to documentation, for cross-session handoff of long tasks
---

Write the following information to docs/claude-progress.json:
1. Features completed in this session (update completed_features)
2. Current work in progress (update in_progress)
3. Important decisions made and their rationale (append to docs/decisions/ directory)
4. Key context that the next Agent needs to know
5. If there are blockers, record them in in_progress.blockers

Also update the last_updated timestamp.
After completion, output a summary: "Saved X completed features, current progress: [feature name]"
