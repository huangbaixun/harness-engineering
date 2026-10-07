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
| Handoff history becomes hard to navigate | Review archive candidates on demand |
| Major refactor completed | Sync documentation after architecture changes |

## Archiving Workflow

### Step 1: Classify and Archive Completed Artifacts

Read root `features.json` (fall back to `docs/features.json` for legacy projects).
Use the selected completed feature's `spec`, plan links and related files to find
candidates; do not infer filenames from its ID or archive unrelated historical work.
Process each candidate once, even when several features share it.

Before moving a candidate, inspect all feature references and repository inbound
references, including relative Markdown links, source comments, scripts and user
documentation. Search its path and filename (for example with `rg`), resolve links
relative to their referring files, and distinguish actual consumers from historical
mentions. Record referring paths and the reason for each keep/move decision.

- **Shared spec:** retain it while any referring feature is not `done`. Completion
  of one feature does not complete a shared design.
- **Living spec:** even when all referring features are `done`, retain a spec still
  used as a contract or explanation by released code, scripts or user documentation.
  Repairable bookkeeping links alone do not make a document a living contract.
- **Execution plan:** archive after its work is verified complete and it is no longer
  needed by active work. Historical links may be updated; a finished plan does not
  become living documentation merely because it has inbound links.
- **Unknown:** if completion or reference use cannot be established, retain the
  candidate and report the missing evidence rather than claiming it is safe to move.

For eligible artifacts, first list the inbound links that need repair and check
that `docs/archive/<filename>` does not already contain a different file. If it
conflicts, retain the source and report the conflict; do not overwrite the target.
Use `git mv` to preserve traceable history, update affected feature paths and other
repairable links, then verify the new targets and check for stale active references.
Keep unrelated fields and documents unchanged. No commit, Issue sync, push or deploy
is implied by archiving.

Prepend archive metadata to moved files, preserving any existing frontmatter:
`archived_at`, `completed_by` (only when known), and `feature_id` or `feature_ids`
for shared artifacts. Set the selected feature's `archived_at` only after its
eligible artifacts and reference repairs are complete. If all candidates stay in
place, report that outcome without inventing an archive timestamp. Retaining a
living/shared spec does not revoke the feature's verified `done` status.

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
- [ ] Modules violating justified project-specific limits or exhibiting measured complexity
- [ ] Files added in the last 7 days that have no tests

### Step 4: Generate Archiving Report

Output format:

```markdown
## Archiving Report — {{DATE}}

### Archived
- F-001: User Login -> docs/archive/F-001-user-login.md

### Retained / Unknown
- docs/specs/shared-design.md: retained; F-002 is still building

### Reference Repairs
- features.json: spec path updated after move
- docs/guide.md: relative link repaired and target checked
- List unresolved links or archive conflicts; do not report them as verified

### Documentation Drift
- [Critical] docs/architecture.md missing description for src/services/notification/
- [Suggestion] CLAUDE.md line 12 rule is already covered by pre-protect-env Hook

### Architecture Quick Check
- [Warning] src/utils/helpers.ts combines unrelated responsibilities; split if observed complexity warrants it

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
Explicit neutral checkpoint (no auto-commit)

Trigger chain: verify provides evidence -> authorized archive organizes handoff -> scripts/harness_state.py saves a neutral checkpoint. Hooks do not commit progress.
```

## Division of Responsibility with harness:evolve

```
harness:archive: Triggered on each task completion, focused on "archiving + documentation sync"
harness:evolve:  Triggered on demand (model update / end of sprint), focused on "streamlining and evolving the Harness itself"

Documentation drift found by archive -> if it involves Harness components themselves -> hand off to evolve
```
