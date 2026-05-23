# harness-delta: dispatching-parallel-agents

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json grounding
Every parallel agent dispatched must have its scope mapped to a `features.json` entry (or explicitly marked as `bug:` per `systematic-debugging` convention). Orphan parallel work — work that doesn't trace to a feature — is **blocked**.

Before dispatching, the controller must:
1. Read `features.json` to identify in-progress (`building`) features
2. Confirm each parallel task maps to one of those features OR is a documented sub-task that descends from one
3. Reject "let's also do X while we're here" suggestions unless X is added to features.json first

### Architecture layer dependency respect
Parallel work must respect the project's dependency direction: `references → templates → skills → commands` (per CLAUDE.md). Agents working on a lower layer (e.g., `commands/`) cannot proceed in parallel with agents working on a layer they depend on (e.g., `skills/`) if those upstream changes haven't been committed yet. This is enforced by the controller via task sequencing — parallel batches must not span layer dependencies in conflicting directions.

### ADR
None directly. If parallel work surfaces an architectural disagreement between agents, escalate to brainstorming + ADR rather than committing inconsistent code.

## Soft hints
- Group parallel tasks by feature, not by file or layer.
- Aim for ~3-4 agents per batch; larger batches lose review efficiency.

## Stop Hook contract
None directly. The controller is responsible for enforcement.

## Verification (covered by evals)
- with-skill: every dispatched agent's task description references a features.json `id`
- baseline: agents may be dispatched with orphan scope
