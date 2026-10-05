# harness-delta: using-git-worktrees

## Upstream
superpowers v6.4.2 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Branch naming convention — features.json id
Worktree branches must be named `feature/<features.json-id>` where `<id>` is the lowercase id from `features.json` (e.g., `feature/f002` for working on F002). This makes the worktree's purpose immediately obvious from `git branch` output and from the worktree directory name.

If working on a non-feature task (bug, refactor, etc.), use prefixes:
- `bug/<slug>` for bug fixes
- `chore/<slug>` for chores

### Cross-skill: merge → harness:archive
On worktree merge completion (Option 1 of `finishing-a-development-branch`), this skill (and finishing-a-development-branch jointly) must trigger `harness:archive`. The chain is:

```
using-git-worktrees (merge) → finishing-a-development-branch → harness:archive
```

### ADR
None directly.

## Soft hints
- The harness platform tool `EnterWorktree` is preferred over `git worktree add` per the upstream Step 1a guidance.
- ExitWorktree(action=keep) before merging to main; cleanup the worktree directory after merge succeeds.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: created worktree branch names follow `feature/<id>` / `bug/<slug>` / `chore/<slug>` convention
- with-skill: merge → archive chain is triggered
- baseline: worktree branch names may be arbitrary

## Codex and GPT-6 workflow adapter

Read `references/platforms/codex.md` from the runtime root when running on Codex; map tools to the actual host and preserve native permissions. Long-running workflow policy is in `references/gpt6-workflows.md`, loaded only when relevant. The user's existing approval and scope remain authoritative; do not repeat approval gates already satisfied. Native execution records a checkpoint, runs all approved tasks, and gets one final independent review. Planning records interfaces and checkable decisions rather than implementing the product during planning. Do not change models or global configuration implicitly.
