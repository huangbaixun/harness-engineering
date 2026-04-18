# harness:router — Harness Engineering Meta Skill

> This Skill is loaded at the start of every session to ensure Harness Engineering capabilities are properly activated.
> Inspired by the `using-superpowers` forced-trigger pattern from obra/superpowers.

## Core Rule: Mandatory Skill Invocation

**Whenever any of the following situations arise, you have no discretion — you must immediately invoke the corresponding Skill:**

| Situation | Must Invoke | Trigger Examples |
|-----------|-------------|------------------|
| New project / setting up AI engineering environment / project just started | **harness:init** | "Help me initialize this project", "How do I start a new project", "Setup Claude Code", "I need a CLAUDE.md" |
| Agent repeatedly makes the same type of mistake / poor AI collaboration efficiency / want to understand project health | **harness:audit** | "Why does Claude always...", "How's the code quality", "Check my Harness", "Help me diagnose" |
| Model upgrade / streamline CLAUDE.md / Harness optimization / garbage collection | **harness:evolve** | "CLAUDE.md is too long", "Do a GC pass", "New version is out, what needs updating", "Optimize the Harness" |
| **Implementing a new feature / fixing a bug / refactoring** (estimated >30 min or involves 3+ files) | **harness:plan** | "Help me implement this feature", "Let's do the next feature", "There's an issue here that needs fixing" |
| **Any implementation work** (including the execution phase after harness:plan) | **tdd** | Automatically activated before writing any code to ensure the RED->GREEN->REFACTOR cycle |
| **About to declare a task complete** / before updating claude-progress.json | **harness:verify** | "Done", "Finished writing it", "Ready to merge", about to mark a feature as done |

**The 1% Rule**: If there is even a 1% chance that a Skill applies to the current task, you must invoke it. Do not wait until you are certain.

## How to Invoke Skills

Use the platform's Skill tool invocation, rather than manually reading SKILL.md files:

```
# Correct approach (Cowork / Claude Code)
Skill tool: "harness:init"
Skill tool: "harness:audit"
Skill tool: "harness:evolve"
```

## Decision Flow

Before responding to any user request, complete the following checks:

```
Step 1: Is the user initializing / setting up a new project?
  -> Yes -> Invoke harness:init

Step 2: Is the user describing Agent failures, code issues, or engineering quality problems?
  -> Yes -> Invoke harness:audit

Step 3: Is the user optimizing / streamlining / upgrading an existing Harness?
  -> Yes -> Invoke harness:evolve

Step 4: Does the user want to implement a feature / fix a bug / refactor, estimated >30 min or involving 3+ files?
  -> Yes -> First invoke harness:plan (planning gate), then begin coding after the plan is confirmed

Step 5: Currently writing any implementation code?
  -> Yes -> Activate the tdd workflow (RED->GREEN->REFACTOR), no skipping steps allowed

Step 6: About to declare "done" or update claude-progress.json?
  -> Yes -> First invoke verification; only declare done after all checks pass

Step 7: None of the above -> Respond normally, but if any of the above situations arise during the process, immediately invoke the corresponding Skill
```

## Why This Rule Matters

Passive trigger-word matching ("initialize", "harness:init") misses a large number of real scenarios:
- User says "Help me set up Claude's config" -> Should trigger harness:init, but contains no matching keywords
- User says "Claude always writes code I don't want" -> Should trigger harness:audit, but the word "audit" never appears

Mandatory intent recognition provides over 10x better coverage than word matching.
