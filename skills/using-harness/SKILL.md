---
name: harness:using-harness
description: >
  Mandatory routing/meta skill for the harness-engineering plugin. Loads at every session start
  and enforces the "1% rule" — if there's even a 1% chance a harness skill applies, invoke it.
  Routes between 19 skills (13 vendored from superpowers v5.1.0 + 6 harness-original).
---

# harness:using-harness — Harness Engineering Meta Skill

> This skill is loaded at the start of every session to ensure harness-engineering capabilities
> are properly activated. Inspired by the `using-superpowers` forced-trigger pattern from
> `obra/superpowers`, but with the harness skill catalog and mandatory invocation table.

## Core Rule: Mandatory Skill Invocation

If there is even a 1% chance one of the skills below applies, **you must invoke it** — you have no discretion.

## Skill catalog

### Vendored from superpowers v5.1.0 (13)
| Trigger | Skill |
|---|---|
| Planning a multi-step task before touching code | `harness:writing-plans` |
| Implementing a feature or fixing a bug | `harness:test-driven-development` |
| About to claim work is complete | `harness:verification-before-completion` |
| Any creative/design task (new feature, modify behavior) | `harness:brainstorming` |
| Executing a written plan task-by-task | `harness:executing-plans` |
| Executing a plan via fresh subagent per task | `harness:subagent-driven-development` |
| 2+ independent parallel tasks | `harness:dispatching-parallel-agents` |
| Need an isolated workspace | `harness:using-git-worktrees` |
| Any bug, test failure, or unexpected behavior | `harness:systematic-debugging` |
| Receiving code review feedback | `harness:receiving-code-review` |
| Asking for code review | `harness:requesting-code-review` |
| Implementation complete; integrating the work | `harness:finishing-a-development-branch` |
| Creating or editing a skill | `harness:writing-skills` |

### Harness-original (6)
| Trigger | Skill |
|---|---|
| (this skill itself) | `harness:using-harness` |
| Task completion / archiving | `harness:archive` |
| Health check on existing project Harness setup | `harness:audit` |
| Pre-production deploy planning | `harness:canary` |
| Garbage collection / drift cleanup | `harness:evolve` |
| New project initialization | `harness:init` |

## Hard rules
- Invoke the relevant skill **before** any response or action (including clarifying questions).
- Never rationalize skipping a skill ("this is simple", "I remember this", "the skill is overkill").
- When the user explicitly types `/<skill>`, invoke it immediately.

## Cross-skill handoffs
- `harness:brainstorming` → must hand off to `harness:writing-plans` (terminal state for brainstorming).
- `harness:writing-plans` → hands off to `harness:executing-plans` or `harness:subagent-driven-development`.
- `harness:verification-before-completion` → triggers `harness:finishing-a-development-branch` → which must call `harness:archive`.
