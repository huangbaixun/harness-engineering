# harness-delta: subagent-driven-development

## Upstream
superpowers v6.3.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json grounding for subagent scope
Each subagent dispatched must have its task scope traceable to a `features.json` entry. The controller (the agent invoking this skill) must verify before dispatching:
- The task is part of an in-progress (`building`) feature's plan, OR
- The task is documented under a `bug:` prefix (per `systematic-debugging` convention)

No orphan subagent work. If a task can't be tied to a feature, pause and ask the user whether to add it to features.json or scope it out.

### `.claude/agents/` project-specific definitions
This plugin uses `.claude/agents/` for project-specific subagent definitions (e.g., `code-review-agent`, `Explore`, etc.). When dispatching, prefer project-specific agents over the default `general-purpose` agent when their description matches the task. This is read by the controller, not enforced by this skill.

### ADR
None directly.

### Plan must carry a `Spec:` pointer (new in v6.3.0)
v6.3.0 has SDD read the spec at setup and resolve plan conflicts against it instead of guessing. That requires the plan to name its spec. `harness:writing-plans` emits the upstream `Spec:` field; before dispatching, confirm the plan has one and that it points at a real file under `docs/specs/`. A plan with no `Spec:` pointer is **blocked** — send it back to writing-plans rather than dispatching against a guess.

### Circuit-breaker rulings are recorded, not silent (new in v6.3.0)
v6.3.0 lets the controller rule on non-catastrophic plan conflicts and keep going instead of stalling. In this repo a recorded ruling that changes scope must still reach `features.json`: if a ruling adds, drops, or redefines work relative to the feature's `acceptance_criteria`, update the entry (or push back to brainstorming) before the Finish report — a ruling is not a licence to drift from the spec.

## Soft hints
- Use the model parameter to right-size cost (Haiku for mechanical tasks, Sonnet for judgment, Opus for design). v6.3.0 requires the model be specified explicitly on every dispatch.
- Review is now **one task review per task** covering spec compliance and code quality together, plus a broad whole-branch review at the end. (Through v5.1.0 these were two sequential per-task reviews; the old ordering rule no longer applies.)
- Implementers and reviewers must not spawn their own subagents — the upstream prompt templates carry that contract. Do not edit it out.
- The `scripts/` helpers (`sdd-workspace`, `task-brief`, `review-package`) and the three prompt templates are vendored as of this sync; prefer them over hand-rolled dispatch text.

## Stop Hook contract
None directly; per-task review checkpoints handle quality enforcement.

## Verification (covered by evals)
- with-skill: every subagent dispatch references a features.json id
- with-skill: project-specific agents from .claude/agents/ are considered when matching
- baseline: subagents may be dispatched with orphan scope
