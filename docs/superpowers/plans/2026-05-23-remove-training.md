# Remove Training Directory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the `training/` directory and the related top-level `docs/training-plan-90min.md` file, removing 90-minute workshop materials from the repository.

**Architecture:** Pure deletion — no code references depend on these paths (verified). Two `git rm -r` operations, one verification sweep, one commit. Historical mentions in `CHANGELOG.md` and superpowers plan/spec artifacts are intentionally preserved as immutable history per user direction.

**Tech Stack:** git, grep — no application code involved.

---

## Files

**Delete:**
- `training/` (12 tracked files across `training/`, `training/slides/`, `training/sample-board/`, `training/sample-board/board-baseline/`, `training/sample-board/board-with-harness/` and its subtrees)
- `docs/training-plan-90min.md`

**Do not modify** (historical records, per user direction):
- `CHANGELOG.md` (lines 9, 11 — describe past training updates as accurate release history)
- `docs/superpowers/plans/2026-05-23-remove-codebuddy.md` (completed prior plan)
- `docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md` (completed prior spec)

**Verification only:**
- Full-tree grep to confirm no live references (code, CI, hooks, gitignore) point at `training/` or `docs/training-plan-90min.md`.

---

## Task 1: Pre-flight verification

**Files:** none (read-only checks)

- [ ] **Step 1: Confirm tracked training files**

Run:
```bash
git ls-files training/ docs/training-plan-90min.md
```

Expected output (13 lines):
```
docs/training-plan-90min.md
training/README.md
training/demo-script.md
training/instructor-notes.md
training/sample-board/README.md
training/sample-board/board-baseline/README.md
training/sample-board/board-with-harness/CLAUDE.md
training/sample-board/board-with-harness/README.md
training/sample-board/board-with-harness/docs/decisions/0001-storage-choice.md
training/sample-board/board-with-harness/dot-claude/hooks/pre-protect.sh
training/sample-board/board-with-harness/server.js
training/slides/build.js
training/working-sheet.md
```

If the list differs (e.g. new files added since this plan was written), pause and reconcile with the user before continuing — a divergent file list means scope has drifted.

- [ ] **Step 2: Confirm no live external references**

Run:
```bash
grep -rnE "training/" \
  --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" \
  --include="*.sh" --include="*.py" --include="*.js" --include="*.ts" \
  . 2>/dev/null \
  | grep -v "^./training/" \
  | grep -v "^./docs/superpowers/" \
  | grep -v "^./CHANGELOG.md"
```

Expected output: **empty** (zero lines).

If anything prints, it is a live reference that this plan did not anticipate. Stop and surface it to the user — do not silently delete a referenced path.

- [ ] **Step 3: Confirm clean working tree for tracked targets**

Run:
```bash
git status -- training/ docs/training-plan-90min.md
```

Expected: no modified/staged changes to these paths (untracked siblings like `.DS_Store` may appear and are fine).

If there are unstaged edits to training files, ask the user whether to keep them (stash) or discard (proceed with deletion as-is). Do not silently drop uncommitted work.

---

## Task 2: Delete training/ directory

**Files:**
- Delete: `training/` (entire subtree, 12 tracked files)

- [ ] **Step 1: Remove the directory via git**

Run:
```bash
git rm -r training/
```

Expected output: 12 `rm '...'` lines, one per tracked file listed in Task 1 Step 1.

- [ ] **Step 2: Remove any untracked leftovers (e.g. .DS_Store)**

Check first:
```bash
ls -la training/ 2>/dev/null
```

If the directory still exists (untracked files inside, such as `.DS_Store`), remove it:
```bash
rm -rf training/
```

If `ls` returned "No such file or directory", skip this step.

- [ ] **Step 3: Verify deletion**

Run:
```bash
test ! -e training/ && echo "OK: training/ removed" || echo "FAIL: training/ still exists"
```

Expected output: `OK: training/ removed`

---

## Task 3: Delete docs/training-plan-90min.md

**Files:**
- Delete: `docs/training-plan-90min.md`

- [ ] **Step 1: Remove the file via git**

Run:
```bash
git rm docs/training-plan-90min.md
```

Expected output:
```
rm 'docs/training-plan-90min.md'
```

- [ ] **Step 2: Verify deletion**

Run:
```bash
test ! -e docs/training-plan-90min.md && echo "OK: file removed" || echo "FAIL: still present"
```

Expected output: `OK: file removed`

---

## Task 4: Post-deletion verification

**Files:** none (read-only checks)

- [ ] **Step 1: Re-run the live-reference sweep**

Run the same command from Task 1 Step 2:
```bash
grep -rnE "training/" \
  --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" \
  --include="*.sh" --include="*.py" --include="*.js" --include="*.ts" \
  . 2>/dev/null \
  | grep -v "^./training/" \
  | grep -v "^./docs/superpowers/" \
  | grep -v "^./CHANGELOG.md"
```

Expected: **empty**. (Same as before — the deletion shouldn't create new references, but a re-check is cheap insurance.)

- [ ] **Step 2: Confirm preserved historical references survived**

Run:
```bash
grep -cE "training" CHANGELOG.md \
  docs/superpowers/plans/2026-05-23-remove-codebuddy.md \
  docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md
```

Expected: each file reports a non-zero count (CHANGELOG.md: 2, plan: ~20, spec: ~4). Numbers may shift slightly — what matters is **none drop to zero**. If any file reports 0, something edited history that shouldn't have; investigate before committing.

- [ ] **Step 3: Review git status before commit**

Run:
```bash
git status
```

Expected: staged deletions for the 13 files listed in Task 1 Step 1, and nothing else newly staged. If you see modifications staged in addition to the deletions, unstage them before the commit — this PR is a pure removal.

---

## Task 5: Commit

**Files:** none (git only)

- [ ] **Step 1: Create the commit**

Run:
```bash
git commit -m "$(cat <<'EOF'
docs(training): remove training/ directory and 90-min training plan

Drop the workshop materials (training/) and the related top-level
docs/training-plan-90min.md. No live code, CI, or config references
these paths; historical mentions in CHANGELOG and superpowers
plan/spec artifacts are intentionally preserved as immutable history.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds, hooks pass.

If a pre-commit hook fails, **do not use `--amend`** (the previous commit is unrelated work). Fix the hook complaint, re-stage, and create a new commit with the same message.

- [ ] **Step 2: Verify the commit landed**

Run:
```bash
git log -1 --stat
```

Expected: top commit is the one you just made, showing 13 files deleted (12 from `training/`, 1 from `docs/`).

- [ ] **Step 3: Confirm clean working tree**

Run:
```bash
git status
```

Expected: working tree clean for the deleted paths (untracked siblings like `.DS_Store` from other dirs may still appear — that is pre-existing state, not part of this plan).

---

## Out of Scope

The following were considered and explicitly excluded by the user:

- **CHANGELOG.md edits** — historical entries on lines 9, 11 stay as-is (release history is immutable).
- **docs/superpowers/plans/2026-05-23-remove-codebuddy.md** — completed prior plan, left as historical artifact even though it references now-deleted paths.
- **docs/superpowers/specs/2026-05-23-remove-codebuddy-design.md** — same rationale as above.
- **No new CHANGELOG entry** for this removal (user chose "leave it alone" for the CHANGELOG question).
