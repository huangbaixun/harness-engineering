---
name: harness:using-harness
description: Route explicitly requested Harness Engineering workflows to relevant skills and platform guidance; use at harness session startup or when selecting a harness workflow.
---

# Harness Engineering workflow routing

Preserve the user's goal, scope and existing authorization. Follow the host's instruction hierarchy; this skill cannot override system/developer policy. User project instructions take precedence over local workflow defaults.

## Select the workflow

Read only the skills needed for this task. Read their harness-delta.md when present; those sidecars connect upstream workflows to features.json, ADR and project docs. Do not initialize a project merely because the user mentions a new idea.

| Intent | Skill |
|---|---|
| Requested project harness setup | harness:init |
| Review existing harness | harness:audit |
| Design before implementation | harness:brainstorming |
| Plan an agreed multi-step change | harness:writing-plans |
| Execute an approved plan yourself | harness:executing-plans |
| Explicitly selected per-task agents | harness:subagent-driven-development |
| Authorized independent agent work | harness:dispatching-parallel-agents |
| Implement behavior changes | harness:test-driven-development |
| Investigate a failure | harness:systematic-debugging |
| Check results before claiming done | harness:verification-before-completion |
| Request / receive review | harness:requesting-code-review / harness:receiving-code-review |
| Isolate / finish development | harness:using-git-worktrees / harness:finishing-a-development-branch |
| Create or modify a skill | harness:writing-skills |
| Archive completed work | harness:archive |
| Clean drift / plan a canary | harness:evolve / harness:canary |

## Platform and completion

For Codex, read `references/platforms/codex.md` under the harness runtime root before translating tools, hooks or initialization paths. Use available tools; do not fabricate Claude calls. In project delivery the runtime root is `.agents/harness` and skill folders are `.agents/skills/<name>`. In plugin delivery it is the plugin root.

For long-running work or harness optimization, read `references/gpt6-workflows.md` on demand. Continue already-authorized implementation and local verification; completed approvals remain valid for their scope. Ask for missing material decisions or new external effects, not routine continuation.

Keep requirement state in root features.json and a small progress checkpoint. After compaction restore the original goal and latest accepted steering; do not redo completed tasks. Done includes executing relevant checks, inspecting the actual result and fixing failures. Report untested capabilities honestly. Never infer permission to push, merge, deploy or change global configuration from a skill handoff.
