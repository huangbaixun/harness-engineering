# harness-delta: subagent-driven-development

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

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

## Soft hints
- Use the model parameter to right-size cost (Haiku for mechanical tasks, Sonnet for judgment, Opus for design).
- Spec compliance review must happen before code quality review — order matters per the upstream skill.

## Stop Hook contract
None directly; per-task review checkpoints handle quality enforcement.

## Verification (covered by evals)
- with-skill: every subagent dispatch references a features.json id
- with-skill: project-specific agents from .claude/agents/ are considered when matching
- baseline: subagents may be dispatched with orphan scope
