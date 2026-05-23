# harness-delta: finishing-a-development-branch

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json writes — status transition to `done`
This skill OWNS the final transition of feature status to `done`. After this skill completes (Option 1 merge or Option 2 PR-merged), the corresponding feature in `features.json` must be updated from `building` → `done`. Identify the feature by:
- The feature whose `spec:` field matches the spec the work implements, OR
- The feature explicitly referenced in the branch name (per `using-git-worktrees` convention `feature/<features.json-id>`)

### claude-progress.json sync
After status transition, mirror the outcome to `claude-progress.json` (existing convention so subsequent sessions see the state).

### Mandatory `harness:archive` call
Before reporting completion, this skill MUST invoke `harness:archive` to:
- Verify documentation is in sync with code
- Run architecture health scan (per spec §5 Phase 4)
- Generate structured archive report

This is non-negotiable per the integration spec §7 row 13.

### Conditional `harness:canary` prompt
If the merged work touches deployment surfaces (CI/CD configs, infrastructure-as-code, dockerfiles, k8s manifests, env vars in production), prompt the user about whether `harness:canary` pre-deployment planning should be invoked. Do not auto-invoke — surface the recommendation.

### ADR
None directly. If a deferred ADR was promised during planning and hasn't been written by completion time, this skill should surface that gap before allowing transition to `done`.

## Soft hints
- Squash-merge vs ff-only vs no-ff is a judgment call — match what existing project history does.
- For Plan A's milestone, `--no-ff` made the merge commit visible; that pattern may repeat for major plans.

## Stop Hook contract
None directly; this is itself a terminal-state skill.

## Verification (covered by evals)
- with-skill: completing a feature triggers features.json status update + harness:archive invocation
- with-skill: deploy-touching change triggers harness:canary prompt
- baseline: feature may be merged with stale features.json or skipped archive
