---
name: harness:archive
description: >
  Completion archiving and documentation sync at the end of a unit of work. Activate when the user
  mentions "archive", "task is done", "feature complete", "wrap up", "end of sprint", "sprint cleanup",
  "sync the docs", "docs are out of date", "documentation drift", "clean up finished specs",
  "harness archive", or invokes /harness:archive.
  Also use this Skill without being asked whenever harness:verification-before-completion has just
  passed, whenever a feature's status is about to move to done, after a major refactor lands, or when
  the session reports a growing pile of completed features — those are the moments handoff artifacts
  and documentation silently fall out of sync with the code.
---

# harness:archive — Completion Archiving and Documentation Sync

> **Source**: OpenSpec `/opsx:archive` + Handbook S K.6 "Documentation Sync Agent" + Handbook S 2.3 "Structured Handoff Artifacts"
> **Integration**: Merges the core checks from commands/sync-docs.md and commands/scan-arch.md into a single Skill,
> triggered automatically upon task completion to ensure handoff artifacts are complete and documentation is consistent with code.

## When to Use

| Trigger Condition | Example |
|---------|------|
| Feature marked as completed | After harness:verification-before-completion passes |
| Manual invocation via `/harness:archive` | End-of-sprint cleanup |
| completed_features >= 10 | session-start prompts archiving |
| Major refactor completed | Sync documentation after architecture changes |

## Archiving Workflow

### Step 1: Archive Completed Specs

Check `features.json` (repo root; fall back to `docs/features.json` for legacy projects) for features with `status: "done"`:

```
For each completed feature:
  1. If a corresponding design document exists (docs/specs/F-xxx.md or docs/plans/F-xxx.md)
     -> git mv to docs/archive/ (preserve git history)
  2. Prepend completion metadata at the top of the archived file:
     ---
     archived_at: {{TIMESTAMP}}
     completed_by: {{SESSION_ID}}
     feature_id: F-xxx
     ---
  3. Update features.json: add the archived_at field
```

**Directory convention**: The archive directory is always `docs/archive/`. Create it if it does not exist. Use `git mv` instead of copy+delete to ensure `git log --follow` can trace the full history.

### Step 2: Documentation Consistency Check

Run the following comparisons (source: commands/sync-docs.md):

1. **Directory structure comparison**
   - Read the directory structure described in `docs/architecture.md`
   - Compare against the actual `src/` directory
   - List directories that are new but undocumented, and directories that are deleted but still referenced

2. **CLAUDE.md rule validity**
   - Check each rule in CLAUDE.md one by one
   - Flag redundant rules already covered by Hooks or Linters
   - Flag obsolete rules whose corresponding error patterns no longer exist

3. **ADR status sync**
   - Check ADRs in `docs/decisions/` with status "Adopted"
   - Verify that the corresponding technology choices are still in use

### Step 3: Architecture Health Quick Check (source: commands/scan-arch.md)

Lightweight architecture scan (use `/harness:audit` for the full version):

- [ ] Dependency direction violations (per architecture.md)
- [ ] Source files exceeding 300 lines
- [ ] Files added in the last 7 days that have no tests

### Step 4: Generate Archiving Report

Output format:

```markdown
## Archiving Report — {{DATE}}

### Archived
- F-001: User Login -> docs/archive/F-001-user-login.md

### Documentation Drift
- [Critical] docs/architecture.md missing description for src/services/notification/
- [Suggestion] CLAUDE.md line 12 rule is already covered by pre-protect-env Hook

### Architecture Quick Check
- [Warning] src/utils/helpers.ts exceeds 300 lines (currently 342 lines)

### Suggested Actions
1. Update architecture.md to add the notification module description
2. Remove the redundant rule on line 12 of CLAUDE.md
```

## Relationship with Other Components

```
harness:verification-before-completion (verification passed)
    |
    v
harness:archive (this Skill — archiving + documentation sync)
    |
    v
Stop Hook (commit progress)

Trigger chain: verify confirms completion -> archive organizes handoff artifacts -> stop saves state
```

## Division of Responsibility with harness:evolve

```
harness:archive: Triggered on each task completion, focused on "archiving + documentation sync"
harness:evolve:  Triggered on demand (model update / end of sprint), focused on "streamlining and evolving the Harness itself"

Documentation drift found by archive -> if it involves Harness components themselves -> hand off to evolve
```
