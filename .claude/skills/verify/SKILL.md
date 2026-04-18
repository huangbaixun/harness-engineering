# harness:verify — Pre-Completion Verification

> **upstream**: obra/superpowers `verification-before-completion` @ [917e5f5](https://github.com/obra/superpowers/tree/917e5f5/skills/verification-before-completion)
> **harness-delta**: Renamed to verification (shorter trigger), added Architecture layer checks (layer dependency violation detection), auto-updates claude-progress.json + features.json status after verification

> Adapted from the obra/superpowers Verification Before Completion skill.
> Core principle: Agents will confidently claim "it's done," but claiming completion ≠ actually complete.
> This Skill adds semantic-layer verification on top of Stop Hooks.

## Mandatory Trigger: Before Any "Done" Claim

Before uttering any of the following, you must pass this verification checklist:
- "Done" / "completed" / "finished"
- "Implemented" / "written"
- "You can test it now" / "ready to merge"
- About to update `claude-progress.json` to mark a feature as completed

## Verification Checklist (Execute in Order)

### Layer 1: Functional Verification
- [ ] Run the full test suite — **zero failures** (no "this failure doesn't matter")
- [ ] Check each `acceptance_criteria` entry in `features.json` for this feature and confirm every one is met
- [ ] Items listed in `out_of_scope` have **not** been implemented (over-implementation is also a problem)

### Layer 2: Quality Verification
- [ ] Lint / type checks pass (`{{LINT_COMMAND}}`)
- [ ] No new TODO / FIXME / HACK comments (or they are documented as known debt)
- [ ] New code has corresponding tests (coverage is no lower than the existing baseline)
- [ ] Public APIs / functions have doc comments

### Layer 3: Architecture Verification
- [ ] No violations of dependency rules in `docs/architecture.md`
- [ ] No cross-layer direct calls (e.g., UI calling Repo directly)
- [ ] No hardcoded secrets / configuration values

### Layer 4: Integration Verification
- [ ] Build succeeds (`{{BUILD_COMMAND}}`)
- [ ] If e2e tests exist, all e2e tests pass
- [ ] If API endpoints are affected, API documentation has been updated accordingly

## On Verification Failure

If any item fails → **do not claim completion; continue fixing**.

No rationalizing with "commit first, fix later" or "this minor issue doesn't affect functionality."

## After Verification Passes

```
1. Update docs/claude-progress.json:
   - Move from in_progress to completed_features
   - Record completion time and number of tests passed

2. Update docs/features.json:
   - Set the feature's status to "completed"

3. If completed_features exceeds 10 entries:
   - Trigger the archival mechanism (see AGENTS.md archival rules)
```

## Relationship with Stop Hooks

```
Stop Hook (stop-typecheck.sh): Hard interception — blocks tool calls if tests/type checks fail
harness:verify Skill (this document): Soft discipline — semantic-level definition of "truly complete"

They are complementary:
  Stop Hook prevents "completion with errors"
  harness:verify Skill prevents "completion with missed acceptance criteria"
```
