# tdd — Test-Driven Development Workflow

> **upstream**: obra/superpowers `test-driven-development` @ [917e5f5](https://github.com/obra/superpowers/tree/917e5f5/skills/test-driven-development)
> **harness-delta**: Renamed to tdd (shorter trigger), bound to the harness:router 1% rule, integrates features.json acceptance_criteria as a test input source

> Adapted from the obra/superpowers TDD skill, tailored for the Harness Engineering six-layer model.
> In the Harness environment, Stop Hooks provide hard interception; this Skill provides workflow discipline.

## Core Loop: RED → GREEN → REFACTOR

All feature implementations must strictly follow the three-phase loop — **no skipping steps**:

```
RED (Write a Failing Test)
  → Write a test that describes the expected behavior first
  → Run the test and confirm it fails (red)
  → The failure reason must be "feature not implemented," not "the test itself is wrong"

GREEN (Minimal Implementation)
  → Write the minimum code to make the test pass
  → No over-engineering — only make the current test pass
  → Run the full test suite and confirm everything is green

REFACTOR (Refactor)
  → Clean up code under test protection
  → Eliminate duplication, improve readability
  → Run the tests again after refactoring to confirm everything is still green
```

## Trigger Conditions (1% Rule)

Whenever there is even a 1% chance it applies, activate this workflow before starting implementation:

| Scenario | Example |
|----------|---------|
| Implementing a new feature | "Help me build feature X" |
| Fixing a bug | "There's an issue here, help me fix it" |
| Refactoring code | "This code needs optimization" |
| Implementing a features.json entry | coding-agent picks up the next feature |

## Collaboration with Other Harness Layers

```
features.json (Requirements Anchor)
    ↓  Extract acceptance_criteria
harness:plan Skill (Task Breakdown)
    ↓  Break down into 2–5 minute tasks
tdd Skill (This Workflow)
    ↓  RED → GREEN → REFACTOR
Stop Hook (stop-typecheck.sh)
    ↓  All tests must pass before completion is allowed
harness:verify Skill (Final Verification)
    ↓  Validate against acceptance_criteria
claude-progress.json (Status Update)
```

## Each Test Should Satisfy

- **One test tests one thing** — failure reason is clear
- **Test names describe behavior** — `test_user_cannot_login_with_wrong_password`, not `test_login`
- **AAA structure** — Arrange → Act → Assert
- **Tests are independent** — no dependency on execution order or state of other tests

## Common Mistakes and Corrections

| Anti-Pattern | Correct Approach |
|--------------|-----------------|
| Write implementation first, then add tests | Write the test first; only start implementing after you see red |
| Write multiple tests at once | Write one test at a time; write the next only after the current one passes |
| Skip running tests during REFACTOR | Run the full test suite after every refactoring |
| Skip REFACTOR after tests pass | REFACTOR is a required step, not optional |
| Modify the test to make it pass | Tests are the spec; modifying a test means changing the requirements |
