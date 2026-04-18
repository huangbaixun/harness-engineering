---
name: harness:evolve
description: >
  Continuous iteration and evolution of the Harness framework. Activate when the user mentions
  "trim Harness", "remove unnecessary rules", "update Harness after new model release",
  "Harness maintenance", "garbage collection", "code entropy", "documentation drift",
  "architecture drift", "CLAUDE.md is too long", "harness evolve", "slim down Harness",
  "optimize token usage", or "clean up outdated rules".
  Also use this Skill when the user has updated the Claude model version, the project has gone
  through a long iteration cycle, or the Harness feels bloated and no longer efficient —
  use it to streamline and evolve the Harness framework.
---

# Harness Continuous Evolution Skill

> This Skill guides the continuous streamlining and evolution of the Harness framework.
> Core principle: **Streamline the Harness as models improve — when a new model inherently handles a class of failures, proactively remove the corresponding scaffolding.** The Harness is not append-only; it must be continuously adjusted to match model capabilities and project changes.

## Three Dimensions of Evolution

### Dimension 1: Garbage Collection — Fighting Codebase Entropy

Codebase-level entropy manifests in three forms:

**Documentation Drift**: Code changes but documentation does not update. Rules in CLAUDE.md are no longer necessary but still consume tokens.

**Architecture Drift**: Early architecture rules are quietly violated by new code over time. "Only one place violates the rule" gradually becomes "every place violates the rule."

**Code Entropy**: Dead code, duplicate implementations, excessive coupling, naming convention divergence.

#### Four Types of Garbage Collection

**Type 1: Documentation Sync (recommended daily)**

Scan the directory structure in docs/architecture.md and compare it against the actual src/ directory to find inconsistencies. Check whether each rule in CLAUDE.md still applies in the codebase. Check whether ADR statuses match actual technology choices.

For each detected drift, generate a specific fix recommendation.

**Type 2: Architecture Constraint Scan (recommended weekly)**

Run dependency analysis tools to check for violations:
- Dependency direction violations
- Oversized modules (> 300 lines)
- New files missing tests
- Circular dependencies

**Type 3: CLAUDE.md Slimming (after each new model release)**

Evaluate each rule in CLAUDE.md one by one:

1. Does Claude still follow this rule naturally without it being stated?
   -> If yes, delete the rule (reduce token cost)

2. Is this rule already covered by a Hook or Linter?
   -> If a Computational Sensor covers it, the text version is just redundant

3. Does this rule correspond to a failure mode that actually exists?
   -> Check Agent failure records from the past 4 weeks; if it was never triggered, consider deleting it

Goal: Keep CLAUDE.md under 60 lines.

**Type 4: Code Entropy Detection (recommended monthly)**

- Dead code detection
- Duplicate code detection
- Excessive coupling detection (which modules are referenced by more than 3 other modules)
- Test quality assessment (are tests verifying implementation details instead of behavior)

### Dimension 2: Harness Streamlining — Adjusting to Model Capabilities

After each model update, reassess whether each Harness component is still necessary.

#### Evaluation Process

```
Step 1: Confirm the new model version
Step 2: Test with a standard task (at least 5 features)
Step 3: Observe whether the following behaviors occur
  [ ] Context anxiety (wrapping up too early)
  [ ] Architecture violations (ignoring dependency rules)
  [ ] Over-implementation (exceeding out_of_scope)
  [ ] Format inconsistencies
Step 4: Adjust based on results
  Problem occurs -> Keep/strengthen the corresponding Harness component
  No problem -> Delete the corresponding Harness component (reduce complexity)
```

#### Streamlining Decision Matrix

| Harness Component | Model Handles It Natively | Action |
|-------------------|--------------------------|--------|
| Context reset scripts | No anxiety behavior | Delete; switch to auto-compaction |
| Formatting Hook | Output is always well-formatted | Keep; formatting is a deterministic operation |
| Type-checking Hook | — | Always keep; does not depend on model capability |
| CLAUDE.md prohibition rules | Agent no longer makes this mistake | Consider deleting, but conservatively comment out first |
| Security review Sub-agent | — | Always keep; security cannot be compromised |

**Principle**: Computational Sensors (type checking, Linters) are always kept, regardless of how strong the model is. Inferential-layer constraints can be streamlined as the model improves.

### Dimension 3: Capability Upgrade — From Reactive to Proactive

The maturity evolution path for the Harness:

```
Stage 1: Humans build the Harness; the Agent works within it
         (Current state for most teams)

Stage 2: The Agent discovers Harness issues and logs them in progress.json
         Humans review the logs and update the Harness
         (Recommended current target)

Stage 3: The Agent discovers issues and directly opens a PR to improve the Harness
         Humans approve and merge the PR
         (OpenAI "garbage collection Agent" pattern)

Stage 4: The Harness auto-optimizes itself (Meta-Harness, experimental stage)
```

#### Upgrading to Stage 2

Add the following to the coding Agent's prompt:
```
When you encounter any of the following, log it in the notes field of claude-progress.json:
- A rule is unclear and causes you to hesitate
- You need a tool or permission that is not available
- Documentation is inconsistent with the code
- You feel a Harness rule is unnecessary
```

Humans review the notes once a week; valuable feedback is converted into Harness improvements.

#### Upgrading to Stage 3

Create a `/harness-improve` Command:
```markdown
1. Read recent notes from claude-progress.json
2. Filter for Harness-related feedback
3. For each piece of feedback, evaluate:
   - Is this a systemic issue (occurred multiple times)?
   - What is the complexity and risk of the fix?
4. Generate specific PRs for low-risk improvements
5. For high-risk improvements, only log recommendations and wait for human decision
```

## Core Loop of Continuous Improvement

```
Agent fails
    |
    v
Identify the missing capability
    |
    v
Engineer a fix (update docs / add Linter / build tooling)
    |
    v
That failure never happens again
```

This loop is the essence of Harness Engineering.

## Measuring Effectiveness: The Right Metrics

```
WRONG metric: "Fixed 20 bugs for the Agent this week"
RIGHT metric: "Added 3 architecture Linter rules this week; this class of bugs will never recur"

WRONG metric: "Reviewed all of the Agent's PRs"
RIGHT metric: "Set up an automated security review Hook; PR quality issues are caught automatically"

WRONG metric: "Wrote a detailed CLAUDE.md so the Agent won't make mistakes"
RIGHT metric: "Used Hooks + settings.json to make those mistakes physically impossible"
```

When humans are dissatisfied with Agent output, the correct response is not to fix the output directly, but to improve the Harness that produced it.
