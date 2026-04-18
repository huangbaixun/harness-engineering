---
description: Sprint feature assignment planner. Analyze the dependency graph and team workload from docs/features.json, output the optimal owner assignment plan + a ready-to-run sprint-kickoff.sh script.
---

# /harness:assign — Sprint Feature Assignment Planner

> Goal: Give every team member a ready-to-execute script within 5 minutes of Sprint start — "what I should do and how to begin" — instead of an assignment table that requires further interpretation.

## Phase 1: Read and Analyze features.json

```bash
cat docs/features.json
```

Extract from the JSON:

- **Unassigned pool**: features with `status` of `planned` or `ready`
- **In progress**: features with `status` of `in_progress` (including owner)
- **Dependency graph**: build a directed graph from `depends_on` to `blocks`

Then compute two key properties for each unassigned feature:

**Can start immediately?** (`startable`)
```
startable = depends_on is empty,
         OR all features in depends_on have status == "done"
```

**Critical path weight** (`criticality`)
```
criticality = direct blocks count + recursive blocks count (transitive closure)
```

Output a status snapshot in the following format:

```
🟢 Ready to start (N items)
  F-001 Auth module          [criticality=3, layer=backend]
  F-004 Infrastructure       [criticality=2, layer=infra  ]

🟡 Waiting to unblock (N items)
  F-003 Access control       [waiting: F-001]
  F-005 User settings        [waiting: F-001, F-002]

🔄 In progress (N items)
  F-002 User management UI   [owner: alice, layer=frontend]

📊 Critical path: F-001 → F-003 → F-006 (3 hops, affects 4 downstream)
```

---

## Phase 2: Get Team Snapshot

**First read the `## Team Members` section in CLAUDE.md** (if declared). Example format:

```markdown
## Team Members
- simon: backend, current load 1
- alice: fullstack, current load 1
- bob: infra, current load 0
```

If CLAUDE.md does not have this section, ask the user:

> Please provide team member information (one per line, format: name / layer preference / current in_progress count)
> Example: simon / backend / 1

After collecting, update the member information into the `## Team Members` section of CLAUDE.md (create if it doesn't exist, placed at the end of the file, not counted toward the 60-line limit).

---

## Phase 3: Generate Assignment Plan

Apply the following four rules in order to output a recommended owner for each unassigned feature:

### Rule 1 (Hard constraint): No files_owned overlap
Two features that are simultaneously `in_progress` must not have any common path prefix in their `files_owned` lists.
Assignments violating this rule are rejected outright, marked as `⚠️ File conflict`, prompting human decision.

### Rule 2 (Hard constraint): Max 2 in_progress per person
Exceeding this marks the feature as `⚠️ Overloaded`, deferred to the next batch.

### Rule 3 (Soft priority): Critical path first
Features with higher `criticality` are assigned first to avoid blocking downstream work.

### Rule 4 (Soft priority): Layer affinity
Assign features to members whose `layer` matches, reducing cognitive switching cost.
Within the same Sprint, prefer assigning multiple features of the same layer to the same person.

Output the assignment plan table:

```
┌────────┬─────────────────────┬────────┬──────────────┬───────────────────────────────┐
│ Owner  │ Feature             │ layer  │ criticality  │ Assignment reason              │
├────────┼─────────────────────┼────────┼──────────────┼───────────────────────────────┤
│ simon  │ F-001 Auth module   │backend │ ★★★ (3)      │ Top of critical path, layer match │
│ alice  │ F-002 User mgmt UI  │frontend│ ★★ (2)       │ Already in progress, maintain continuity │
│ bob    │ F-004 Infrastructure│infra   │ ★★ (2)       │ Layer match, lowest load       │
│ simon  │ F-007 API docs      │backend │ ★ (1)        │ Shares src/api/ with F-001, bundled │
├────────┼─────────────────────┼────────┼──────────────┼───────────────────────────────┤
│ Next   │ F-003 Access control│backend │ ★★★ (pending)│ Assign after F-001 completes   │
│ ⚠️ Conflict │ F-008 Search   │        │              │ files_owned overlaps with F-002│
└────────┴─────────────────────┴────────┴──────────────┴───────────────────────────────┘
```

For features marked `⚠️ Conflict`, clearly state the overlapping file paths and wait for user decision before assigning.

---

## Phase 4: Generate sprint-kickoff.sh

Generate an executable script for this Sprint, with each member's operations in an independent section that can be sent directly to them to run:

```bash
#!/usr/bin/env bash
# Sprint Kickoff Script — Generated on {DATE}
# Usage: bash sprint-kickoff.sh [member_name]
# If no argument is given, show all members' operations

MEMBER=${1:-"all"}

# =====================
# === simon's tasks ===
# =====================
if [ "$MEMBER" = "simon" ] || [ "$MEMBER" = "all" ]; then
  echo "=== simon: Claiming F-001 + F-007 ==="
  git pull origin main

  # Claim F-001
  python3 -c "
import json, sys
with open('docs/features.json') as f: data = json.load(f)
for feat in data['features']:
    if feat['id'] == 'F-001':
        feat['owner'] = 'simon'
        feat['status'] = 'in_progress'
with open('docs/features.json', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print('F-001 claimed')
"
  # Claim F-007
  python3 -c "
import json
with open('docs/features.json') as f: data = json.load(f)
for feat in data['features']:
    if feat['id'] == 'F-007':
        feat['owner'] = 'simon'
        feat['status'] = 'in_progress'
with open('docs/features.json', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print('F-007 claimed')
"
  git add docs/features.json
  git commit -m "claim(F-001, F-007): simon claimed"
  git push origin main

  # Start worktree (if project uses worktree mode)
  claude --worktree feature-auth -p "
    Read the task with id=F-001 from docs/features.json.
    files_owned defines your file boundary — do not modify files outside it.
    description explains the implementation requirements, acceptance lists the acceptance criteria.
    After completion, run all test commands in acceptance. Submit a PR once all pass.
  " &
fi

# =====================
# === alice's tasks ===
# =====================
if [ "$MEMBER" = "alice" ] || [ "$MEMBER" = "all" ]; then
  echo "=== alice: Continuing F-002 ==="
  # alice already has F-002, no need to claim — start directly
  git pull origin main
  claude --worktree feature-users -p "
    Read the task with id=F-002 from docs/features.json.
    Continue from where you left off. Refer to docs/claude-progress.json for existing progress.
  " &
fi

# =====================
# === bob's tasks ===
# =====================
if [ "$MEMBER" = "bob" ] || [ "$MEMBER" = "all" ]; then
  echo "=== bob: Claiming F-004 ==="
  git pull origin main
  python3 -c "
import json
with open('docs/features.json') as f: data = json.load(f)
for feat in data['features']:
    if feat['id'] == 'F-004':
        feat['owner'] = 'bob'
        feat['status'] = 'in_progress'
with open('docs/features.json', 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)
print('F-004 claimed')
"
  git add docs/features.json
  git commit -m "claim(F-004): bob claimed"
  git push origin main
  claude --worktree feature-infra -p "
    Read the task with id=F-004 from docs/features.json.
    files_owned defines your file boundary. acceptance lists the acceptance criteria.
  " &
fi

echo "✅ Sprint launched. Each member's Agent is running in the background."
echo "📌 When any task completes, run /harness:dump to save progress."
```

Save this script to the project root: `sprint-kickoff.sh`, and run `chmod +x sprint-kickoff.sh`.

---

## Phase 5: Record Sprint Assignment in claude-progress.json

Append this assignment to the `sprint_history` array in `docs/claude-progress.json`:

```json
{
  "sprint_history": [
    {
      "date": "{DATE}",
      "assignments": [
        { "owner": "simon", "features": ["F-001", "F-007"], "reason": "Critical path + layer match" },
        { "owner": "alice", "features": ["F-002"],           "reason": "Continue existing task" },
        { "owner": "bob",   "features": ["F-004"],           "reason": "Layer match, lowest load" }
      ],
      "deferred": ["F-003 (waiting on F-001)"],
      "conflicts": ["F-008 (files_owned conflict, pending human decision)"]
    }
  ]
}
```

---

## Output Summary

End with a concise summary:

```
✅ Sprint assignment complete

Assigned 3 people x 4 features:
  simon → F-001 (critical path) + F-007
  alice → F-002 (continuing in progress)
  bob   → F-004

Waiting for next batch: F-003 (unblocked after F-001 completes)
Needs human decision: F-008 (files_owned conflicts with F-002)

Generated: sprint-kickoff.sh (ready to run or distribute to team members)
Recorded: docs/claude-progress.json sprint_history
```

---

## Anti-pattern Reminders

| Anti-pattern | Reason | Correct approach |
|--------|------|---------|
| Assigning by gut feel without checking criticality | Blocks the critical path, causes downstream backlog | Always assign highest criticality first |
| One person claiming 3+ features at once | Cognitive overload, slow progress on each | Max 2 in_progress per person |
| Ignoring files_owned overlap | Merge conflicts, overwriting each other's work | Conflicting features must be serialized or re-scoped |
| Not recording assignment history | Cannot retrospect, no reference for next Sprint | Always append to sprint_history |
