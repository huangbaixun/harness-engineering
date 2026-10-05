# harness-delta: test-driven-development

## Upstream
superpowers v6.4.2 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Locate the current in-progress feature (status=`building`) in `features.json`. Use its `acceptance_criteria` array as the **test input source**:
- Each criterion should map to at least one test case.
- Test names should reference the criterion (e.g., `test_pagination_at_50_per_page` for criterion "paginate API at 50 per page").

### features.json writes
None. This skill does not modify features.json.

### ADR
None directly.

### Task-relevant routing
Use test-first work for applicable behavior changes in the selected workflow. Mentioning code alone does not authorize implementation or force this skill for read-only analysis.

## Soft hints
- Prefer integration tests over unit tests when integration coverage is unclear; ADR-0004's "integration-first" stance applies.

## Stop Hook contract
A configured Stop verifier supplies feedback at session stopping only. It does not intercept commits or enforce test-first work. Explicit inspected test results remain required.

## Verification (covered by evals)
- with-skill: when features.json has a `building` feature, the first test written cites the specific `acceptance_criterion` by content.
- baseline: without the skill, tests may be written but won't trace to the criteria.

## Codex and GPT-6 workflow adapter

Read `references/platforms/codex.md` from the runtime root when running on Codex; map tools to the actual host and preserve native permissions. Long-running workflow policy is in `references/gpt6-workflows.md`, loaded only when relevant. The user's existing approval and scope remain authoritative; do not repeat approval gates already satisfied. Native execution records a checkpoint, runs all approved tasks, and gets one final independent review. Planning records interfaces and checkable decisions rather than implementing the product during planning. Do not change models or global configuration implicitly.
