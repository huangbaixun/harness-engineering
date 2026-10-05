# harness-delta: requesting-code-review

## Upstream
superpowers v6.4.2 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Pre-review checklist gate
Before requesting review, this skill must verify ALL of the following:
1. **All rigid constraints satisfied**: every `acceptance_criterion` in `features.json` for the in-progress feature is demonstrably met (test passing, behavior observable).
2. **No out_of_scope drift**: no commit in this branch touches an item listed in `features.json` `out_of_scope` for the feature.
3. **Architecture layer dependencies clean**: no reverse-direction dependency (e.g., `skills/` importing from `commands/`).

If any check fails, this skill refuses to dispatch the review request until the gap is closed (or the user explicitly updates features.json to revise constraints).

### PR description template
The PR description template (Markdown body) must include a `feature:` field at the top:

```markdown
## feature
F002 (superpowers-vendor-skills)

## summary
<2-3 bullets>

## test plan
<verification steps>
```

The `feature:` value is the `id` from `features.json`. If multiple features are touched, list all.

### ADR
None directly. If the PR is born out of an ADR decision, the description should reference the ADR number under a `## related` section.

## Soft hints
- Squash commits before requesting review only if the project history prefers squash; this repo's recent history is non-squash (see git log).
- For long-lived branches, run `git rebase main` first to keep the diff focused.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: review request blocked when any rigid constraint is unsatisfied
- with-skill: PR body includes feature: <id> line
- baseline: review may be requested with unsatisfied constraints or missing feature reference

## Codex and GPT-6 workflow adapter

Read `references/platforms/codex.md` from the runtime root when running on Codex; map tools to the actual host and preserve native permissions. Long-running workflow policy is in `references/gpt6-workflows.md`, loaded only when relevant. The user's existing approval and scope remain authoritative; do not repeat approval gates already satisfied. Native execution records a checkpoint, runs all approved tasks, and gets one final independent review. Planning records interfaces and checkable decisions rather than implementing the product during planning. Do not change models or global configuration implicitly.
