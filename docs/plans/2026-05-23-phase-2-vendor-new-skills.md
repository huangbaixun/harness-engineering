# Plan B — Phase 2: Vendor 10 New Superpowers Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vendor 10 new superpowers v5.1.0 skills into this plugin with the 4-file sidecar structure established by ADR-0009, each with harness-delta.md integration content per spec §7 and fresh evals per ADR-0004.

**Architecture:** Each of the 10 skills follows the same vendor pattern Plan A established for `writing-plans`, `test-driven-development`, and `verification-before-completion`: copy upstream `SKILL.md` verbatim, apply two allowed edits (frontmatter `name:` + pointer line), author `harness-delta.md` per integration matrix, author `UPSTREAM.md` with provenance, write `evals/evals.json` with 2-3 test cases. Skills can be committed in batches but each per-skill task is independent. The 10 tasks are structurally identical; only the content per skill differs.

**Tech Stack:** Markdown for skill files, JSON for evals, git for commits, bash for upstream-cache reads.

**Source spec:** `docs/specs/2026-05-23-superpowers-integration-design.md`
**Predecessor plan:** `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` (Plan A — merged at commit 5c76cbb)

**Upstream cache base:** `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/<name>/SKILL.md`

**Upstream SHA capture** (one-time, used by every Task 2.x to fill UPSTREAM.md's `Commit SHA:` line):

```bash
UPSTREAM_BASE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0"
UPSTREAM_SHA="$(git -C "$UPSTREAM_BASE" rev-parse HEAD 2>/dev/null || echo 'v5.1.0')"
echo "$UPSTREAM_SHA"
```

For Plan A this was `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`. If the cache is unchanged at Plan B execution time, reuse it for consistency. If a `sync-superpowers.sh` run between Plan A and Plan B has updated the cache, the new SHA must be captured fresh and used in every Task 2.x UPSTREAM.md.

**The 10 skills to vendor** (in alphabetical order; each is its own task):

| # | Skill name | Task | Spec §7 row |
|---|---|---|---|
| 1 | `brainstorming` | 2.1 | 5 |
| 2 | `dispatching-parallel-agents` | 2.2 | 8 |
| 3 | `executing-plans` | 2.3 | 6 |
| 4 | `finishing-a-development-branch` | 2.4 | 13 |
| 5 | `receiving-code-review` | 2.5 | 11 |
| 6 | `requesting-code-review` | 2.6 | 12 |
| 7 | `subagent-driven-development` | 2.7 | 7 |
| 8 | `systematic-debugging` | 2.8 | 10 |
| 9 | `using-git-worktrees` | 2.9 | 9 |
| 10 | `writing-skills` | 2.10 | 14 |

**Pre-task and post-task wrappers:**

- Task 2.0 — set F002 and the design spec status to `building` (dogfood lifecycle sync, per Final Review of Plan A)
- Task 2.11 — cross-skill verification + transition F002 to `done`

**Recommended commit batching for review efficiency:** group tasks 2.1–2.4 (Batch A: workflow + completion cluster), 2.5–2.7 (Batch B: review + execution cluster), 2.8–2.10 (Batch C: debugging + worktrees + meta cluster). Each task still commits independently — the batching is just a convenient review boundary for the controller invoking subagent-driven-development.

---

## Task 2.0: Transition F002 + spec status to `building`

**Files:**
- Modify: `features.json` (F002 status: proposed → building)
- Modify: `docs/specs/2026-05-23-superpowers-integration-design.md` (front-matter status: proposed → building)

- [ ] **Step 1: Update `features.json` F002 status**

Use Edit with `old_string`:
```
      "id": "F002",
      "name": "superpowers-vendor-skills",
      "priority": 2,
      "status": "proposed",
```
And `new_string`:
```
      "id": "F002",
      "name": "superpowers-vendor-skills",
      "priority": 2,
      "status": "building",
```

- [ ] **Step 2: Update `features.json` F002 technical_notes**

Replace `<TBD>-phase-2-vendor-new-skills.md` with `2026-05-23-phase-2-vendor-new-skills.md`. Use Edit with `old_string`:
```
      "technical_notes": "Plan: docs/plans/<TBD>-phase-2-vendor-new-skills.md (authored after F001 completes)",
```
And `new_string`:
```
      "technical_notes": "Plan: docs/plans/2026-05-23-phase-2-vendor-new-skills.md",
```

- [ ] **Step 3: Validate JSON**

```bash
python3 -m json.tool features.json > /dev/null && echo OK
```
Expected: `OK`

- [ ] **Step 4: Update spec front-matter status**

Use Edit on `docs/specs/2026-05-23-superpowers-integration-design.md`. `old_string`:
```
status: proposed
features:
```
`new_string`:
```
status: building
features:
```

- [ ] **Step 5: Commit**

```bash
git add features.json docs/specs/2026-05-23-superpowers-integration-design.md
git commit -m "chore(features): transition F002 + spec status to building"
```

---

## Task 2.1: Vendor `brainstorming`

**Files:**
- Create: `skills/brainstorming/SKILL.md` (upstream verbatim + 2 edits)
- Create: `skills/brainstorming/harness-delta.md`
- Create: `skills/brainstorming/UPSTREAM.md`
- Create: `skills/brainstorming/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/brainstorming/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/brainstorming/SKILL.md"
cp "$UPSTREAM_FILE" skills/brainstorming/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

**Edit A** — frontmatter `name:` field changes from `name: brainstorming` to `name: harness:brainstorming`. Use Edit tool to update the line.

**Edit B** — insert pointer line between closing `---` of frontmatter and the first H1. Read the file to see what comes right after the closing `---`, then Edit with `old_string` = the `---` + blank + H1 sequence (e.g., `---\n\n# Brainstorming`), `new_string` = same with the pointer inserted:

```
---

> **harness local rules:** Always read [harness-delta.md](./harness-delta.md) before invoking this skill. It defines mandatory integrations with features.json, ADR, and docs.

# Brainstorming
```

DO NOT modify any other content in SKILL.md.

- [ ] **Step 3: Create harness-delta.md**

Create `skills/brainstorming/harness-delta.md`:

```markdown
# harness-delta: brainstorming

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Spec output path — Override of upstream default
Brainstorming spec output goes to `docs/specs/YYYY-MM-DD-<topic>-design.md` (the harness convention), **not** `docs/superpowers/specs/` (the upstream default in SKILL.md). This is intentional per the integration spec §8 — `docs/specs/` is the canonical location in this plugin.

### Spec front-matter is mandatory
Every spec produced by this skill must include the front-matter declared in `docs/specs/README.md`:

```yaml
---
date: YYYY-MM-DD
topic: <slug>
type: feature | adr-proposal | exploration
status: proposed | building | done
features: [<features.json-id>, ...]   # required when type=feature
adr: [<NNNN>, ...]                    # required when type=adr-proposal
superseded_by: <path>                 # optional
---
```

### features.json writes (only when type=feature)
When the spec's `type` is `feature`, this skill must append one entry per feature to `features.json`:
- `id`, `name`, `priority`, `status: "proposed"`, `spec: <path-to-this-spec>`, `description`, `acceptance_criteria`, `out_of_scope`, `dependencies`, `technical_notes`, `related_files`
- The new entry's `spec:` field MUST point back to the spec file being authored (back-reference)

### ADR writes (only when type=adr-proposal)
When the spec's `type` is `adr-proposal`, this skill must produce one or more ADRs under `docs/decisions/NNNN-<slug>.md` before transitioning to writing-plans.

### Gate to writing-plans handoff
- type=feature without a corresponding features.json entry → **blocked**, must add entry or change type
- type=adr-proposal without a corresponding ADR file → **blocked**, must produce ADR or change type
- type=exploration → can hand off without features.json or ADR (or end without writing-plans at all)

## Soft hints
- Use the brainstorming sections incrementally; do not present the full design in one shot.
- Visual companion is opt-in per spec §6.

## Stop Hook contract
None directly; writing-plans is the next mandatory step after brainstorming completes (forced exit at the workflow level via `harness:using-harness` 1% rule).

## Verification (covered by evals)
- with-skill: type=feature → entry appears in `features.json` before writing-plans handoff
- with-skill: type=adr-proposal → ADR file appears in `docs/decisions/` before writing-plans handoff
- baseline: spec may dangle without features.json sync or ADR
```

- [ ] **Step 4: Create UPSTREAM.md**

Create `skills/brainstorming/UPSTREAM.md`:

```markdown
# Upstream provenance: brainstorming

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:brainstorming` (was `brainstorming`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

Create `skills/brainstorming/evals/evals.json`:

```json
{
  "skill_name": "harness:brainstorming",
  "evals": [
    {
      "id": 1,
      "eval_name": "feature-spec-creates-features-json-entry",
      "type": "behavior",
      "rule_under_test": "type=feature spec must add a corresponding entry to features.json before handing off to writing-plans",
      "prompt": "Brainstorm a new feature: 'add API rate limiting at 100 req/sec per IP'. After the design is approved, save the spec.",
      "expected_output": "Spec saved to docs/specs/ with type=feature. A new entry appears in features.json with spec: field pointing back to the spec file. Skill confirms features.json was updated before offering writing-plans handoff.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "spec front-matter present",
          "check": "The created spec file's front-matter includes type=feature, status=proposed, features: [<key>]."
        },
        {
          "name": "features.json updated",
          "check": "features.json gains a new entry whose spec: field equals the path of the just-created spec."
        },
        {
          "name": "blocks transition if entry missing",
          "check": "If features.json is not updated, skill refuses to invoke writing-plans and reports the gap."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "adr-proposal-creates-adr",
      "type": "behavior",
      "rule_under_test": "type=adr-proposal spec must produce an ADR file under docs/decisions/ before handing off",
      "prompt": "Brainstorm: should we use SQS or Redis Streams for the background job queue? Decide and document.",
      "expected_output": "Skill identifies this as an architectural decision (type=adr-proposal). Writes ADR to docs/decisions/NNNN-job-queue-choice.md with Context/Decision/Consequences. Spec front-matter's adr: field references the new ADR number.",
      "files": [],
      "assertions": [
        {
          "name": "ADR file produced",
          "check": "A new file under docs/decisions/ exists with proper ADR structure (Status, Context, Decision, Consequences)."
        },
        {
          "name": "spec adr: field populated",
          "check": "Spec front-matter has adr: [NNNN] referencing the new ADR file's number."
        }
      ]
    },
    {
      "id": 3,
      "eval_name": "spec-path-uses-docs-specs-not-docs-superpowers-specs",
      "type": "behavior",
      "rule_under_test": "Override of upstream default — spec output goes to docs/specs/, not docs/superpowers/specs/",
      "prompt": "Brainstorm any small feature and save the spec.",
      "expected_output": "Spec file is created at docs/specs/YYYY-MM-DD-<topic>-design.md. Skill does NOT write to docs/superpowers/specs/.",
      "files": [],
      "assertions": [
        {
          "name": "spec written to docs/specs/",
          "check": "The created file's path starts with docs/specs/, not docs/superpowers/specs/."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/brainstorming/evals/evals.json > /dev/null && echo OK
for f in skills/brainstorming/SKILL.md skills/brainstorming/harness-delta.md skills/brainstorming/UPSTREAM.md skills/brainstorming/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```
Each file's last byte should be `0a`. JSON should validate.

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/brainstorming/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/brainstorming/
git commit -m "feat(skills): vendor brainstorming v5.1.0 with harness-delta sidecar"
```

---

## Task 2.2: Vendor `dispatching-parallel-agents`

**Files:**
- Create: `skills/dispatching-parallel-agents/SKILL.md`
- Create: `skills/dispatching-parallel-agents/harness-delta.md`
- Create: `skills/dispatching-parallel-agents/UPSTREAM.md`
- Create: `skills/dispatching-parallel-agents/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/dispatching-parallel-agents/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/dispatching-parallel-agents/SKILL.md"
cp "$UPSTREAM_FILE" skills/dispatching-parallel-agents/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

**Edit A** — frontmatter `name:` becomes `name: harness:dispatching-parallel-agents`.

**Edit B** — Insert pointer line:
```
> **harness local rules:** Always read [harness-delta.md](./harness-delta.md) before invoking this skill. It defines mandatory integrations with features.json, ADR, and docs.
```

Between closing `---` and first H1 (whatever upstream uses — likely `# Dispatching Parallel Agents` or similar).

- [ ] **Step 3: Create harness-delta.md**

```markdown
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
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: dispatching-parallel-agents

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:dispatching-parallel-agents` (was `dispatching-parallel-agents`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:dispatching-parallel-agents",
  "evals": [
    {
      "id": 1,
      "eval_name": "every-agent-task-maps-to-features-json",
      "type": "behavior",
      "rule_under_test": "Each parallel agent's task scope must trace to a features.json entry",
      "prompt": "features.json has F001=done, F002=building, F003=proposed. The user asks: 'parallelize the work on improving documentation, refactoring the auth module, and adding metrics — all three at once'. Dispatch agents.",
      "expected_output": "Skill recognizes none of the three proposed tasks maps to an in-progress feature in features.json. Refuses to dispatch parallel agents. Asks the user to either add the work to features.json or scope it to F002.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "blocks orphan dispatch",
          "check": "Skill does not invoke the Agent tool for any of the three orphan tasks."
        },
        {
          "name": "cites features.json gate",
          "check": "Skill's response references features.json as the source of truth for scope."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "respects-architecture-layer-direction",
      "type": "behavior",
      "rule_under_test": "Parallel agents must not work on a lower layer that depends on uncommitted changes in a higher layer",
      "prompt": "Two parallel tasks proposed: (A) modify `skills/foo/SKILL.md` to add a new behavior, (B) modify `commands/foo.md` to call that new behavior. Dispatch both in parallel.",
      "expected_output": "Skill identifies layer dependency: B depends on A. Refuses to dispatch in parallel. Recommends sequencing (A first, then B once A commits).",
      "files": [],
      "assertions": [
        {
          "name": "detects layer dependency",
          "check": "Skill explicitly identifies the references → templates → skills → commands direction and the conflict."
        },
        {
          "name": "recommends sequential",
          "check": "Skill proposes A → B sequential instead of parallel."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/dispatching-parallel-agents/evals/evals.json > /dev/null && echo OK
for f in skills/dispatching-parallel-agents/SKILL.md skills/dispatching-parallel-agents/harness-delta.md skills/dispatching-parallel-agents/UPSTREAM.md skills/dispatching-parallel-agents/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/dispatching-parallel-agents/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/dispatching-parallel-agents/
git commit -m "feat(skills): vendor dispatching-parallel-agents v5.1.0 with harness-delta sidecar"
```

---

## Task 2.3: Vendor `executing-plans`

**Files:**
- Create: `skills/executing-plans/SKILL.md`
- Create: `skills/executing-plans/harness-delta.md`
- Create: `skills/executing-plans/UPSTREAM.md`
- Create: `skills/executing-plans/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/executing-plans/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/executing-plans/SKILL.md"
cp "$UPSTREAM_FILE" skills/executing-plans/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:executing-plans`; pointer line inserted between frontmatter and first H1.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: executing-plans

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reads
Before execution begins:
- Locate the `building` feature whose `spec` matches the plan being executed (or whose `technical_notes` references this plan file).
- Extract `acceptance_criteria` as **rigid constraints** — every task in the plan must trace to at least one criterion; do not invent tasks outside that boundary.
- Extract `out_of_scope` — pause execution and ask the user if any task in the plan would touch out-of-scope items.

### Plans directory — Override of upstream default
Plans are read from `docs/plans/YYYY-MM-DD-<topic>-plan.md` (the harness convention), **not** `docs/superpowers/plans/` (the upstream default). This matches `harness:writing-plans` output.

### features.json writes
None directly. Status transitions are owned by the verify → finishing → archive chain.

### ADR
None directly. If executing-plans surfaces an architectural decision that wasn't anticipated during writing-plans, pause execution and escalate to brainstorming + ADR before continuing.

## Soft hints
- Run gates (tests / JSON validation / smoke tests) after each task, not just at the end.
- If a task fails, do not silently retry — report and surface for review.

## Stop Hook contract
Existing Stop hook ("claim done without tests") plus this skill's per-task verification close the loop. The Stop hook trips if a `git commit` is attempted while tests fail or while rigid constraints from features.json are unsatisfied.

## Verification (covered by evals)
- with-skill: when a plan tries to add tasks outside features.json acceptance_criteria, the skill blocks or asks for spec amendment
- with-skill: completion marker only set after all rigid constraints are demonstrably satisfied
- baseline: plan execution may complete with orphan tasks or unsatisfied criteria
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: executing-plans

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:executing-plans` (was `executing-plans`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:executing-plans",
  "evals": [
    {
      "id": 1,
      "eval_name": "blocks-tasks-outside-features-json",
      "type": "pressure",
      "rule_under_test": "Execution must not proceed on tasks outside features.json acceptance_criteria",
      "prompt": "features.json has feature 'F002 status=building' with acceptance_criteria: ['vendor 10 new skills']. The plan being executed has a Task X that says 'also refactor the auth module'. Execute the plan.",
      "expected_output": "Skill recognizes Task X is outside F002's acceptance_criteria. Pauses execution. Asks user to either add Task X's scope to features.json or remove Task X from the plan.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "blocks execution of orphan task",
          "check": "Skill does not begin work on Task X without resolving the scope mismatch."
        },
        {
          "name": "names the conflict",
          "check": "Skill output cites Task X by name and the missing acceptance_criterion."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "reads-plans-from-docs-plans-not-docs-superpowers-plans",
      "type": "behavior",
      "rule_under_test": "Override of upstream default — read plans from docs/plans/, not docs/superpowers/plans/",
      "prompt": "Execute the plan at docs/plans/2026-05-23-some-feature.md.",
      "expected_output": "Skill opens the file at docs/plans/2026-05-23-some-feature.md. Does NOT look first in docs/superpowers/plans/.",
      "files": [],
      "assertions": [
        {
          "name": "reads from docs/plans/",
          "check": "Skill's first file-access for the plan is the docs/plans/ path."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/executing-plans/evals/evals.json > /dev/null && echo OK
for f in skills/executing-plans/SKILL.md skills/executing-plans/harness-delta.md skills/executing-plans/UPSTREAM.md skills/executing-plans/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/executing-plans/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/executing-plans/
git commit -m "feat(skills): vendor executing-plans v5.1.0 with harness-delta sidecar"
```

---

## Task 2.4: Vendor `finishing-a-development-branch`

**Files:**
- Create: `skills/finishing-a-development-branch/SKILL.md`
- Create: `skills/finishing-a-development-branch/harness-delta.md`
- Create: `skills/finishing-a-development-branch/UPSTREAM.md`
- Create: `skills/finishing-a-development-branch/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/finishing-a-development-branch/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/finishing-a-development-branch/SKILL.md"
cp "$UPSTREAM_FILE" skills/finishing-a-development-branch/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:finishing-a-development-branch`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: finishing-a-development-branch

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json writes — status transition to `done`
This skill OWNS the final transition of feature status to `done`. After this skill completes (Option 1 merge or Option 2 PR-merged), the corresponding feature in `features.json` must be updated from `building` → `done`. Identify the feature by:
- The feature whose `spec:` field matches the spec the work implements, OR
- The feature explicitly referenced in the branch name (per `using-git-worktrees` convention `feature/<features.json-id>`)

### claude-progress.json sync
After status transition, mirror the outcome to `claude-progress.json` (existing convention so subsequent sessions see the state).

### Mandatory `harness:archive` call
Before reporting completion, this skill MUST invoke `harness:archive` to:
- Verify documentation is in sync with code
- Run architecture health scan (per spec §5 Phase 4)
- Generate structured archive report

This is non-negotiable per the integration spec §7 row 13.

### Conditional `harness:canary` prompt
If the merged work touches deployment surfaces (CI/CD configs, infrastructure-as-code, dockerfiles, k8s manifests, env vars in production), prompt the user about whether `harness:canary` pre-deployment planning should be invoked. Do not auto-invoke — surface the recommendation.

### ADR
None directly. If a deferred ADR was promised during planning and hasn't been written by completion time, this skill should surface that gap before allowing transition to `done`.

## Soft hints
- Squash-merge vs ff-only vs no-ff is a judgment call — match what existing project history does.
- For Plan A's milestone, `--no-ff` made the merge commit visible; that pattern may repeat for major plans.

## Stop Hook contract
None directly; this is itself a terminal-state skill.

## Verification (covered by evals)
- with-skill: completing a feature triggers features.json status update + harness:archive invocation
- with-skill: deploy-touching change triggers harness:canary prompt
- baseline: feature may be merged with stale features.json or skipped archive
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: finishing-a-development-branch

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:finishing-a-development-branch` (was `finishing-a-development-branch`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:finishing-a-development-branch",
  "evals": [
    {
      "id": 1,
      "eval_name": "transitions-feature-to-done",
      "type": "behavior",
      "rule_under_test": "Upon successful merge, the corresponding features.json entry must transition to status=done",
      "prompt": "Feature F002 has status=building and the work is fully merged into main. Complete the finishing workflow.",
      "expected_output": "Skill updates F002 status from building to done in features.json. Mirrors the outcome to claude-progress.json. Reports completion to user.",
      "files": ["features.json", "claude-progress.json"],
      "assertions": [
        {
          "name": "features.json status updated",
          "check": "F002 status field equals 'done' after the skill completes."
        },
        {
          "name": "claude-progress.json synced",
          "check": "claude-progress.json reflects F002 done state."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "calls-harness-archive",
      "type": "behavior",
      "rule_under_test": "harness:archive must be invoked before reporting completion",
      "prompt": "Complete a feature whose work is merged.",
      "expected_output": "Skill invokes harness:archive (or its component sub-steps) for doc-sync, architecture scan, structured archive report. Only after archive completes does this skill report 'done' to the user.",
      "files": [],
      "assertions": [
        {
          "name": "archive invoked",
          "check": "Output references harness:archive (or its sub-steps: scan-arch, sync-docs) being run before completion."
        },
        {
          "name": "completion gated on archive",
          "check": "If archive surfaces inconsistencies, skill does not report completion."
        }
      ]
    },
    {
      "id": 3,
      "eval_name": "prompts-canary-on-deploy-touch",
      "type": "behavior",
      "rule_under_test": "If the merged work touches deployment surfaces, prompt the user about harness:canary",
      "prompt": "Feature touches k8s/deployment.yaml and CI workflow files. Complete the finishing workflow.",
      "expected_output": "Skill prompts the user: 'this work touches deployment configs. Run harness:canary for pre-deploy planning?' Does not auto-invoke canary; just surfaces the recommendation.",
      "files": [],
      "assertions": [
        {
          "name": "canary prompt surfaced",
          "check": "Output explicitly asks the user about harness:canary."
        },
        {
          "name": "canary not auto-invoked",
          "check": "Skill does not invoke canary without user confirmation."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/finishing-a-development-branch/evals/evals.json > /dev/null && echo OK
for f in skills/finishing-a-development-branch/SKILL.md skills/finishing-a-development-branch/harness-delta.md skills/finishing-a-development-branch/UPSTREAM.md skills/finishing-a-development-branch/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/finishing-a-development-branch/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/finishing-a-development-branch/
git commit -m "feat(skills): vendor finishing-a-development-branch v5.1.0 with harness-delta sidecar"
```

---

## Task 2.5: Vendor `receiving-code-review`

**Files:**
- Create: `skills/receiving-code-review/SKILL.md`
- Create: `skills/receiving-code-review/harness-delta.md`
- Create: `skills/receiving-code-review/UPSTREAM.md`
- Create: `skills/receiving-code-review/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/receiving-code-review/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/receiving-code-review/SKILL.md"
cp "$UPSTREAM_FILE" skills/receiving-code-review/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:receiving-code-review`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: receiving-code-review

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### features.json reconciliation for rigid-constraint feedback
When review feedback proposes a change that touches a **rigid constraint** (an `acceptance_criterion` or `out_of_scope` declaration in `features.json` for the current feature):
- **Option A — accept the change**: update `features.json` to reflect the new constraint AND apply the code change. The constraint update must be committed separately (or as part of the same commit if atomic) with a message explaining the trade-off.
- **Option B — reject the change**: explicitly document the rejection in the PR conversation, citing the existing rigid constraint and why it must hold. Do not silently ignore.

Silent acceptance (apply code change without features.json sync) and silent rejection (close discussion without rationale) are both **prohibited**.

### ADR for architectural-change feedback
If review feedback proposes an architectural change (new dependency, layer-direction reversal, new external service, framework choice), pause acceptance and produce an ADR:
- Either a new ADR if it's a net-new decision, OR
- An update to an existing ADR's `Consequences` section if it modifies a prior decision's assumptions

The PR cannot merge until the ADR is written and reviewed.

### docs
None directly.

## Soft hints
- Prefer applying feedback in the same PR over deferring to a follow-up, unless the change is genuinely out of scope.
- Quote the reviewer's exact words when responding to avoid misinterpretation.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: rigid-constraint feedback → features.json updated OR explicit rejection logged
- with-skill: architectural feedback → ADR produced or updated before merge
- baseline: feedback may be applied without features.json or ADR sync
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: receiving-code-review

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:receiving-code-review` (was `receiving-code-review`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:receiving-code-review",
  "evals": [
    {
      "id": 1,
      "eval_name": "rigid-constraint-feedback-reconciles-features-json",
      "type": "behavior",
      "rule_under_test": "Review feedback touching a rigid constraint must either update features.json or be explicitly rejected with rationale",
      "prompt": "F002 acceptance_criteria includes 'rate limit = 100 req/sec per IP'. Reviewer comments: 'should be 50 req/sec instead — 100 is too lax'. Process this feedback.",
      "expected_output": "Skill recognizes the conflict with rigid constraint. Surfaces two options: (A) accept and update features.json to 50 req/sec + apply code change, or (B) reject with rationale explaining why 100 stands. Neither silently applies nor silently ignores.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "identifies rigid conflict",
          "check": "Output explicitly references the existing acceptance_criterion."
        },
        {
          "name": "surfaces accept/reject choice",
          "check": "Output presents the two options with clear consequences."
        },
        {
          "name": "no silent application",
          "check": "Code change is not applied without features.json update OR explicit rejection."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "architectural-feedback-triggers-adr",
      "type": "behavior",
      "rule_under_test": "Architectural-change feedback must produce or update an ADR before merge",
      "prompt": "Reviewer comments: 'this PR adds a new dependency on Redis — we previously decided to avoid Redis (see ADR-0003). Should we revisit that decision?'",
      "expected_output": "Skill identifies this as an architectural change touching ADR-0003. Refuses to merge until either ADR-0003 is updated (with new Consequences entry) or a net-new ADR documents the Redis addition. Surfaces the path forward to user.",
      "files": [],
      "assertions": [
        {
          "name": "ADR work surfaced",
          "check": "Output references ADR-0003 by number and explains what ADR update is needed."
        },
        {
          "name": "blocks merge",
          "check": "Skill does not allow merge until ADR work is done."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/receiving-code-review/evals/evals.json > /dev/null && echo OK
for f in skills/receiving-code-review/SKILL.md skills/receiving-code-review/harness-delta.md skills/receiving-code-review/UPSTREAM.md skills/receiving-code-review/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/receiving-code-review/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/receiving-code-review/
git commit -m "feat(skills): vendor receiving-code-review v5.1.0 with harness-delta sidecar"
```

---

## Task 2.6: Vendor `requesting-code-review`

**Files:**
- Create: `skills/requesting-code-review/SKILL.md`
- Create: `skills/requesting-code-review/harness-delta.md`
- Create: `skills/requesting-code-review/UPSTREAM.md`
- Create: `skills/requesting-code-review/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/requesting-code-review/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/requesting-code-review/SKILL.md"
cp "$UPSTREAM_FILE" skills/requesting-code-review/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:requesting-code-review`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: requesting-code-review

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Pre-review checklist gate
Before requesting review, this skill must verify ALL of the following:
1. **All rigid constraints satisfied**: every `acceptance_criterion` in `features.json` for the in-progress feature is demonstrably met (test passing, behavior observable).
2. **No out_of_scope drift**: no commit in this branch touches an item listed in `features.json` `out_of_scope` for the feature.
3. **Architecture layer dependencies clean**: no reverse-direction dependency (e.g., `skills/` importing from `commands/`).

If any check fails, this skill refuses to dispatch the review request until the gap is closed (or the user explicitly updates features.json to revise constraints).

### PR description template
The PR description template (Markdown body) must include a `feature:` field at the top:

```markdown
## feature
F002 (superpowers-vendor-skills)

## summary
<2-3 bullets>

## test plan
<verification steps>
```

The `feature:` value is the `id` from `features.json`. If multiple features are touched, list all.

### ADR
None directly. If the PR is born out of an ADR decision, the description should reference the ADR number under a `## related` section.

## Soft hints
- Squash commits before requesting review only if the project history prefers squash; this repo's recent history is non-squash (see git log).
- For long-lived branches, run `git rebase main` first to keep the diff focused.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: review request blocked when any rigid constraint is unsatisfied
- with-skill: PR body includes feature: <id> line
- baseline: review may be requested with unsatisfied constraints or missing feature reference
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: requesting-code-review

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:requesting-code-review` (was `requesting-code-review`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:requesting-code-review",
  "evals": [
    {
      "id": 1,
      "eval_name": "blocks-on-unsatisfied-rigid-constraint",
      "type": "behavior",
      "rule_under_test": "Review request must be blocked if any acceptance_criterion is unsatisfied",
      "prompt": "F002 has 3 acceptance_criteria: 'vendor 10 skills', 'all evals pass', 'documentation updated'. Branch has 8/10 skills vendored, evals partially pass, docs not updated. Request review.",
      "expected_output": "Skill refuses to dispatch review request. Lists the 2 missing skills + missing docs gap. Asks user to either complete the work or update features.json to revise the criteria.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "review blocked",
          "check": "Skill does not invoke gh pr create or equivalent."
        },
        {
          "name": "specific gaps named",
          "check": "Output lists the unsatisfied criteria by content."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "pr-body-includes-feature-id",
      "type": "behavior",
      "rule_under_test": "PR body must include `feature: <features.json-id>` line",
      "prompt": "F002 is fully satisfied. Request review for the branch.",
      "expected_output": "Skill drafts PR with body that includes a `## feature` section referencing F002 (or `feature: F002`). The PR is then created.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "feature id present in PR body",
          "check": "PR body markdown contains `F002` or `feature: F002`."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/requesting-code-review/evals/evals.json > /dev/null && echo OK
for f in skills/requesting-code-review/SKILL.md skills/requesting-code-review/harness-delta.md skills/requesting-code-review/UPSTREAM.md skills/requesting-code-review/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/requesting-code-review/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/requesting-code-review/
git commit -m "feat(skills): vendor requesting-code-review v5.1.0 with harness-delta sidecar"
```

---

## Task 2.7: Vendor `subagent-driven-development`

**Files:**
- Create: `skills/subagent-driven-development/SKILL.md`
- Create: `skills/subagent-driven-development/harness-delta.md`
- Create: `skills/subagent-driven-development/UPSTREAM.md`
- Create: `skills/subagent-driven-development/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/subagent-driven-development/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/subagent-driven-development/SKILL.md"
cp "$UPSTREAM_FILE" skills/subagent-driven-development/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:subagent-driven-development`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
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
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: subagent-driven-development

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:subagent-driven-development` (was `subagent-driven-development`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:subagent-driven-development",
  "evals": [
    {
      "id": 1,
      "eval_name": "subagent-task-traces-to-features-json",
      "type": "behavior",
      "rule_under_test": "Every dispatched subagent's task must trace to a features.json entry (or use bug: prefix)",
      "prompt": "F002 status=building. User asks: 'dispatch a subagent to also clean up the lint warnings in the auth module while we're at it'. Auth cleanup is not in F002.",
      "expected_output": "Skill recognizes the orphan scope. Asks the user whether to add the auth cleanup to features.json (as a new feature or extension of an existing one) or scope it out. Does NOT dispatch the subagent without resolution.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "blocks orphan dispatch",
          "check": "Skill does not invoke the Agent tool for the auth cleanup."
        },
        {
          "name": "surfaces resolution path",
          "check": "Output presents options: add to features.json OR scope out."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "considers-project-specific-agents",
      "type": "behavior",
      "rule_under_test": "Subagent dispatch should prefer project-specific agents from .claude/agents/ when their description matches the task",
      "prompt": "Task: 'review the diff at HEAD for code quality concerns'. The project has .claude/agents/code-review-agent.md available.",
      "expected_output": "Skill considers code-review-agent over the default general-purpose agent and selects it for this task.",
      "files": [".claude/agents/"],
      "assertions": [
        {
          "name": "project agent selected",
          "check": "Skill's Agent tool invocation uses subagent_type=code-review-agent (or equivalent project-defined name), not general-purpose."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/subagent-driven-development/evals/evals.json > /dev/null && echo OK
for f in skills/subagent-driven-development/SKILL.md skills/subagent-driven-development/harness-delta.md skills/subagent-driven-development/UPSTREAM.md skills/subagent-driven-development/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/subagent-driven-development/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/subagent-driven-development/
git commit -m "feat(skills): vendor subagent-driven-development v5.1.0 with harness-delta sidecar"
```

---

## Task 2.8: Vendor `systematic-debugging`

**Files:**
- Create: `skills/systematic-debugging/SKILL.md`
- Create: `skills/systematic-debugging/harness-delta.md`
- Create: `skills/systematic-debugging/UPSTREAM.md`
- Create: `skills/systematic-debugging/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/systematic-debugging/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/systematic-debugging/SKILL.md"
cp "$UPSTREAM_FILE" skills/systematic-debugging/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:systematic-debugging`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: systematic-debugging

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Bug scope tracking
Every bug investigation must be either:
- **Tied to a feature**: reference the `features.json` `id` of the affected feature in the debug note's metadata.
- **Standalone bug**: use the `bug:` prefix convention in the incident filename: `docs/incidents/YYYY-MM-DD-bug-<slug>.md`

This ensures bugs don't become orphan work that bypasses feature accountability.

### docs/incidents/ output
Debug notes must be written to `docs/incidents/YYYY-MM-DD-<slug>.md` per the convention established in Plan A. Each note should record (per `docs/incidents/README.md`):
- Symptom observed
- Reproduction steps
- Root cause (or hypothesis if unresolved)
- Fix applied (or escalation path if open)
- ADR invalidation check

### ADR invalidation check
If debugging reveals that a bug exists because an ADR's stated assumption is wrong (e.g., "we assumed X always holds" → bug shows X can fail), this skill MUST:
1. Identify the affected ADR by number
2. Open the ADR file and append to its `## Consequences` section: a dated bullet noting the invalidated assumption + how the bug manifested
3. Reference the ADR number in the incident note

Silent workarounds (fixing the bug without updating the ADR) are **prohibited** — they leave architectural debt.

### Production incident → harness:canary
For production incidents (not test/dev), surface `harness:canary` for rollback planning. Do not auto-invoke.

## Soft hints
- Reproduce before diagnosing — assume the bug is real until proven otherwise.
- Bisect aggressively for regressions.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: every debug session produces a docs/incidents/ note tied to a feature or with bug: prefix
- with-skill: ADR-invalidating bugs result in ADR Consequences update
- baseline: bugs may be fixed silently without ADR or features.json tracking
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: systematic-debugging

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:systematic-debugging` (was `systematic-debugging`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:systematic-debugging",
  "evals": [
    {
      "id": 1,
      "eval_name": "debug-note-written-to-docs-incidents",
      "type": "behavior",
      "rule_under_test": "Every debug session produces a note at docs/incidents/YYYY-MM-DD-<slug>.md",
      "prompt": "A failing test in feature F002: 'expected 429 status, got 200'. Debug it.",
      "expected_output": "Skill investigates, identifies cause, and writes the investigation to docs/incidents/2026-MM-DD-f002-429-status.md (or similar slug). The note covers symptom, repro, root cause, fix.",
      "files": [],
      "assertions": [
        {
          "name": "incident file created",
          "check": "A new file exists under docs/incidents/ matching the date+slug convention."
        },
        {
          "name": "feature id referenced",
          "check": "Incident note references F002 explicitly."
        },
        {
          "name": "all four sections present",
          "check": "Note contains Symptom, Reproduction, Root cause, and Fix sections."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "adr-invalidating-bug-updates-adr",
      "type": "behavior",
      "rule_under_test": "If a bug invalidates an ADR assumption, the ADR's Consequences section must be updated",
      "prompt": "Bug discovered: vendored SKILL.md was modified outside the 2 allowed edits, but the script didn't detect it. This breaks ADR-0009's assumption that 'allowed edits are enforced'. Debug and resolve.",
      "expected_output": "Skill writes incident note. Identifies ADR-0009 as having an invalidated assumption ('allowed edits are enforced' was wishful — actual enforcement is manual). Appends a dated bullet to ADR-0009's Consequences section noting the gap.",
      "files": ["docs/decisions/0009-harness-delta-sidecar.md"],
      "assertions": [
        {
          "name": "ADR-0009 Consequences updated",
          "check": "docs/decisions/0009-harness-delta-sidecar.md gains a new bullet under Consequences referencing the discovered gap."
        },
        {
          "name": "incident note links to ADR",
          "check": "Incident note explicitly references ADR-0009 by number."
        }
      ]
    },
    {
      "id": 3,
      "eval_name": "production-incident-prompts-canary",
      "type": "behavior",
      "rule_under_test": "Production incidents must surface harness:canary for rollback planning",
      "prompt": "Production alert: 5xx error rate spike on /api/checkout. Debug.",
      "expected_output": "Skill recognizes this as a production incident (not dev/test). Begins investigation AND prompts user about harness:canary for rollback planning.",
      "files": [],
      "assertions": [
        {
          "name": "canary surfaced",
          "check": "Output explicitly asks the user about harness:canary."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/systematic-debugging/evals/evals.json > /dev/null && echo OK
for f in skills/systematic-debugging/SKILL.md skills/systematic-debugging/harness-delta.md skills/systematic-debugging/UPSTREAM.md skills/systematic-debugging/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/systematic-debugging/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/systematic-debugging/
git commit -m "feat(skills): vendor systematic-debugging v5.1.0 with harness-delta sidecar"
```

---

## Task 2.9: Vendor `using-git-worktrees`

**Files:**
- Create: `skills/using-git-worktrees/SKILL.md`
- Create: `skills/using-git-worktrees/harness-delta.md`
- Create: `skills/using-git-worktrees/UPSTREAM.md`
- Create: `skills/using-git-worktrees/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/using-git-worktrees/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/using-git-worktrees/SKILL.md"
cp "$UPSTREAM_FILE" skills/using-git-worktrees/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:using-git-worktrees`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: using-git-worktrees

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### Branch naming convention — features.json id
Worktree branches must be named `feature/<features.json-id>` where `<id>` is the lowercase id from `features.json` (e.g., `feature/f002` for working on F002). This makes the worktree's purpose immediately obvious from `git branch` output and from the worktree directory name.

If working on a non-feature task (bug, refactor, etc.), use prefixes:
- `bug/<slug>` for bug fixes
- `chore/<slug>` for chores

### Cross-skill: merge → harness:archive
On worktree merge completion (Option 1 of `finishing-a-development-branch`), this skill (and finishing-a-development-branch jointly) must trigger `harness:archive`. The chain is:

```
using-git-worktrees (merge) → finishing-a-development-branch → harness:archive
```

### ADR
None directly.

## Soft hints
- The harness platform tool `EnterWorktree` is preferred over `git worktree add` per the upstream Step 1a guidance.
- ExitWorktree(action=keep) before merging to main; cleanup the worktree directory after merge succeeds.

## Stop Hook contract
None directly.

## Verification (covered by evals)
- with-skill: created worktree branch names follow `feature/<id>` / `bug/<slug>` / `chore/<slug>` convention
- with-skill: merge → archive chain is triggered
- baseline: worktree branch names may be arbitrary
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: using-git-worktrees

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:using-git-worktrees` (was `using-git-worktrees`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:using-git-worktrees",
  "evals": [
    {
      "id": 1,
      "eval_name": "worktree-branch-name-follows-convention",
      "type": "behavior",
      "rule_under_test": "Worktree branch names must follow the feature/<id>, bug/<slug>, or chore/<slug> convention",
      "prompt": "Start a worktree for work on F002.",
      "expected_output": "Skill creates a worktree on branch `feature/f002` (lowercase). Does NOT create branches like `worktree-random-name` or `wip-something`.",
      "files": ["features.json"],
      "assertions": [
        {
          "name": "branch name uses feature/ prefix",
          "check": "Created branch name starts with 'feature/' and references F002 (or 'f002')."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "merge-triggers-archive",
      "type": "behavior",
      "rule_under_test": "Worktree merge must trigger harness:archive via the finishing-a-development-branch chain",
      "prompt": "Merge the worktree on branch feature/f002 back to main (Option 1 of finishing-a-development-branch).",
      "expected_output": "After successful merge, skill invokes finishing-a-development-branch which invokes harness:archive. Both run before completion is reported.",
      "files": [],
      "assertions": [
        {
          "name": "finishing-a-development-branch called",
          "check": "Output references invoking finishing-a-development-branch after merge."
        },
        {
          "name": "harness:archive called",
          "check": "Output references invoking harness:archive (or its sub-steps) before reporting done."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/using-git-worktrees/evals/evals.json > /dev/null && echo OK
for f in skills/using-git-worktrees/SKILL.md skills/using-git-worktrees/harness-delta.md skills/using-git-worktrees/UPSTREAM.md skills/using-git-worktrees/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/using-git-worktrees/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/using-git-worktrees/
git commit -m "feat(skills): vendor using-git-worktrees v5.1.0 with harness-delta sidecar"
```

---

## Task 2.10: Vendor `writing-skills`

**Files:**
- Create: `skills/writing-skills/SKILL.md`
- Create: `skills/writing-skills/harness-delta.md`
- Create: `skills/writing-skills/UPSTREAM.md`
- Create: `skills/writing-skills/evals/evals.json`

- [ ] **Step 1: Create skill directory and copy upstream SKILL.md**

```bash
mkdir -p skills/writing-skills/evals
UPSTREAM_FILE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-skills/SKILL.md"
cp "$UPSTREAM_FILE" skills/writing-skills/SKILL.md
```

- [ ] **Step 2: Apply 2 allowed edits to SKILL.md**

`name:` → `harness:writing-skills`; pointer line inserted.

- [ ] **Step 3: Create harness-delta.md**

```markdown
# harness-delta: writing-skills

## Upstream
superpowers v5.1.0 (commit SHA recorded in UPSTREAM.md)

## Hard integrations (must do)

### ADR-0004 skill-creator methodology is rigid
Per ADR-0004, every new or modified skill MUST go through the skill-creator workflow:
1. Draft SKILL.md
2. Write test cases in `skills/<name>/evals/evals.json`
3. Run eval (with-skill vs baseline)
4. Generate eval-viewer for human review
5. Iterate based on feedback

Directly committing a SKILL.md change without `evals/evals.json` updates and eval validation is **prohibited**. This skill enforces the workflow.

### Vendored fork structure (ADR-0009)
If the new skill is a fork of an upstream superpowers skill (or any other source), it MUST follow the 4-file vendored structure per ADR-0009:
- `SKILL.md` — upstream verbatim except for the 2 allowed edits
- `harness-delta.md` — local rules
- `UPSTREAM.md` — provenance (source, SHA, divergences)
- `evals/evals.json` — per ADR-0004

Harness-original skills (no upstream) use the 2-file structure:
- `SKILL.md`
- `evals/evals.json`

The harness-delta.md and UPSTREAM.md files are NOT optional for vendored skills.

### Frontmatter requirements
Every SKILL.md must have YAML frontmatter with at least:
- `name:` — namespaced as `harness:<skill-name>` (per CLAUDE.md and ADR-0007)
- `description:` — what the skill does and when to invoke

### File size limits
- CLAUDE.md ≤ 60 lines (project rule)
- Individual SKILL.md ≤ 500 lines (project rule, per CLAUDE.md "Prohibited Practices")

### docs / spec linkage
None directly; this is a meta-skill.

## Soft hints
- Prefer integration-level evals over unit-level — match the integration-first stance from `harness:test-driven-development`.
- For skills that will be invoked frequently, keep the SKILL.md tight (~150 lines or less).

## Stop Hook contract
None directly; the ADR-0004 workflow enforces discipline at commit time via the eval gate.

## Verification (covered by evals)
- with-skill: new vendored skill landed with 4 files; new harness-original skill with 2 files
- with-skill: SKILL.md frontmatter has the harness: namespace prefix
- baseline: skills may be created without evals or without proper structure
```

- [ ] **Step 4: Create UPSTREAM.md**

```markdown
# Upstream provenance: writing-skills

- **Source:** superpowers v5.1.0
- **Commit SHA:** <substitute $UPSTREAM_SHA captured in the plan header>
- **Forked at:** 2026-05-23
- **Last synced:** 2026-05-23

## Local divergences (intentional)
- `name:` frontmatter is `harness:writing-skills` (was `writing-skills`) — required to namespace into the harness plugin.
- A single pointer line inserted between frontmatter and the first H1, pointing readers to `harness-delta.md`.
- One blank line inserted between the pointer blockquote and the first H1 for readability.

## Upstream changes we deliberately did NOT adopt
- (none yet — initial vendor at v5.1.0)
```

- [ ] **Step 5: Create evals/evals.json**

```json
{
  "skill_name": "harness:writing-skills",
  "evals": [
    {
      "id": 1,
      "eval_name": "vendored-skill-has-4-file-structure",
      "type": "behavior",
      "rule_under_test": "A new skill that vendors from upstream must produce the 4-file structure (SKILL.md + harness-delta.md + UPSTREAM.md + evals/evals.json)",
      "prompt": "Author a new harness-vendored skill 'foo-bar' that forks from a hypothetical upstream skill 'foo-bar' in superpowers v5.2.",
      "expected_output": "Skill creates 4 files: skills/foo-bar/SKILL.md, skills/foo-bar/harness-delta.md, skills/foo-bar/UPSTREAM.md, skills/foo-bar/evals/evals.json. The SKILL.md is upstream-verbatim with only the 2 allowed edits.",
      "files": [],
      "assertions": [
        {
          "name": "all 4 files created",
          "check": "Directory listing shows exactly SKILL.md, harness-delta.md, UPSTREAM.md, evals/."
        },
        {
          "name": "SKILL.md name namespaced",
          "check": "SKILL.md frontmatter name starts with 'harness:'."
        },
        {
          "name": "UPSTREAM.md has SHA",
          "check": "UPSTREAM.md contains a 40-character hex SHA, not a placeholder."
        }
      ]
    },
    {
      "id": 2,
      "eval_name": "harness-original-skill-uses-2-file-structure",
      "type": "behavior",
      "rule_under_test": "A new harness-original skill (no upstream) must use the 2-file structure (SKILL.md + evals/evals.json)",
      "prompt": "Author a new harness-original skill 'project-status-report' that summarizes features.json state.",
      "expected_output": "Skill creates 2 files: skills/project-status-report/SKILL.md and skills/project-status-report/evals/evals.json. Does NOT create harness-delta.md or UPSTREAM.md (those are vendored-only).",
      "files": [],
      "assertions": [
        {
          "name": "exactly 2 entries",
          "check": "Directory listing shows exactly SKILL.md and evals/."
        },
        {
          "name": "no UPSTREAM.md",
          "check": "skills/project-status-report/UPSTREAM.md does not exist."
        },
        {
          "name": "no harness-delta.md",
          "check": "skills/project-status-report/harness-delta.md does not exist."
        }
      ]
    },
    {
      "id": 3,
      "eval_name": "blocks-commit-without-evals",
      "type": "pressure",
      "rule_under_test": "Per ADR-0004, a SKILL.md change without corresponding evals/evals.json must be blocked",
      "prompt": "I want to commit a tweak to skills/audit/SKILL.md to add a new behavior. I don't need to update evals — the change is small.",
      "expected_output": "Skill refuses to commit without an evals/evals.json update. Cites ADR-0004. Explains the workflow.",
      "files": ["docs/decisions/0004-skill-creator-methodology.md"],
      "assertions": [
        {
          "name": "commit blocked",
          "check": "Skill does not commit the SKILL.md change."
        },
        {
          "name": "ADR-0004 cited",
          "check": "Output references ADR-0004 by number."
        }
      ]
    }
  ]
}
```

- [ ] **Step 6: Validate JSON + EOF newlines**

```bash
python3 -m json.tool skills/writing-skills/evals/evals.json > /dev/null && echo OK
for f in skills/writing-skills/SKILL.md skills/writing-skills/harness-delta.md skills/writing-skills/UPSTREAM.md skills/writing-skills/evals/evals.json; do
  echo -n "$f: "; tail -c 1 "$f" | xxd | head -1
done
```

- [ ] **Step 7: Verify 4-file structure**

```bash
ls skills/writing-skills/ | sort
```
Expected: `SKILL.md`, `UPSTREAM.md`, `evals`, `harness-delta.md`.

- [ ] **Step 8: Commit**

```bash
git add skills/writing-skills/
git commit -m "feat(skills): vendor writing-skills v5.1.0 with harness-delta sidecar"
```

---

## Task 2.11: Final cross-skill verification + F002 → done

This task runs after all 10 skills are vendored. It verifies the end state matches Plan B's acceptance criteria and transitions F002 to `done`.

- [ ] **Step 1: Verify all 10 new skill directories exist with correct structure**

```bash
for s in brainstorming dispatching-parallel-agents executing-plans finishing-a-development-branch receiving-code-review requesting-code-review subagent-driven-development systematic-debugging using-git-worktrees writing-skills; do
  entries=$(ls "skills/$s/" 2>/dev/null | sort | tr '\n' ' ')
  if [[ "$entries" == "evals harness-delta.md SKILL.md UPSTREAM.md " ]]; then
    echo "[$s] OK"
  else
    echo "[$s] FAIL: got '$entries'"
  fi
done
```

Expected: 10 OK lines, 0 FAIL lines.

- [ ] **Step 2: Validate all new evals JSON files**

```bash
for s in brainstorming dispatching-parallel-agents executing-plans finishing-a-development-branch receiving-code-review requesting-code-review subagent-driven-development systematic-debugging using-git-worktrees writing-skills; do
  python3 -m json.tool "skills/$s/evals/evals.json" > /dev/null && echo "[$s] JSON OK" || echo "[$s] JSON FAIL"
done
```

Expected: 10 OK lines.

- [ ] **Step 3: Verify each SKILL.md is byte-for-byte upstream (modulo the 2 allowed edits)**

```bash
UPSTREAM_BASE="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills"
for s in brainstorming dispatching-parallel-agents executing-plans finishing-a-development-branch receiving-code-review requesting-code-review subagent-driven-development systematic-debugging using-git-worktrees writing-skills; do
  drift=$(diff <(grep -v -E '^name:|harness local rules' "$UPSTREAM_BASE/$s/SKILL.md") \
               <(grep -v -E '^name:|harness local rules' "skills/$s/SKILL.md") | wc -l | tr -d ' ' || echo 0)
  echo "[$s] drift lines (excluding allowed edits): $drift"
done
```

Expected: each line should show 0 or 1 (a single allowed blank-line insertion is acceptable; anything > 1 is unexpected drift).

- [ ] **Step 4: Run sync-superpowers.sh to confirm all skills are tracked**

```bash
./scripts/sync-superpowers.sh
```

Expected output: 13 lines, one per vendored skill (3 from Plan A + 10 from Plan B), each showing `diff-lines=2` and `last-synced=2026-05-23`.

- [ ] **Step 5: Update root features.json — F002 status to `done`**

Use Edit with `old_string`:
```
      "id": "F002",
      "name": "superpowers-vendor-skills",
      "priority": 2,
      "status": "building",
```
And `new_string`:
```
      "id": "F002",
      "name": "superpowers-vendor-skills",
      "priority": 2,
      "status": "done",
```

- [ ] **Step 6: Validate features.json**

```bash
python3 -m json.tool features.json > /dev/null && echo OK
```
Expected: `OK`.

- [ ] **Step 7: Verify F002 status**

```bash
python3 -c 'import json; d=json.load(open("features.json")); print([(f["id"], f["status"]) for f in d["features"]])'
```
Expected: `[('F001', 'done'), ('F002', 'done'), ('F003', 'proposed')]`

- [ ] **Step 8: Commit the status transition**

```bash
git add features.json
git commit -m "chore(features): F002 superpowers-vendor-skills done"
```

---

## Spec coverage review (Plan B)

This plan implements the following spec sections from `docs/specs/2026-05-23-superpowers-integration-design.md`:

| Spec section | Where in this plan |
|---|---|
| §5 Topology (10 new vendored skills) | Tasks 2.1–2.10 |
| §6 4-file vendored anatomy | Each Task 2.x produces SKILL/harness-delta/UPSTREAM/evals |
| §7 Integration matrix rows 5–14 | harness-delta.md content per Task 2.1–2.10 |
| §8 New docs conventions (docs/incidents/ usage) | Task 2.8 (systematic-debugging) wires it |
| §9.1 Spec types + gate | Task 2.1 (brainstorming) implements |
| §10 Phase 2 | Tasks 2.0–2.11 |
| §11 Upstream sync workflow | Each UPSTREAM.md records SHA for sync-superpowers.sh consumption |
| §15 Dogfooding F002 lifecycle | Task 2.0 transitions to building; Task 2.11 transitions to done |

## Self-review checklist

- [x] **Spec coverage:** all 10 new vendored skills in spec §5 topology have a Task; §7 matrix rows 5–14 each map to a Task's harness-delta.md; §10 Phase 2 acceptance criteria all have verification steps in Task 2.11
- [x] **Placeholder scan:** no TBD, TODO, "fill in later"; the `<substitute $UPSTREAM_SHA ...>` markers in each UPSTREAM.md template require the executing agent to substitute the captured SHA literally (instructed in plan header)
- [x] **Type consistency:** skill names use `harness:<full-name>` consistently in all SKILL.md frontmatter, evals.json `skill_name`, harness-delta.md headings, and cross-references
- [x] **No "Similar to Task N":** each Task 2.x is self-contained with full content for all 4 files
- [x] **F002 lifecycle:** Task 2.0 transitions to `building`, Task 2.11 transitions to `done`; intermediate tasks don't touch features.json status

## Execution handoff

**Plan complete and saved to `docs/plans/2026-05-23-phase-2-vendor-new-skills.md`.**

Two execution options:

1. **Subagent-Driven (recommended)** — fresh subagent per task, two-stage review between tasks. Best for 12 mechanical-pattern tasks.

2. **Inline Execution** — sequential in this session via executing-plans. Higher context cost; you see each step.

After Plan B executes and F002 transitions to `done`, the next session should invoke `harness:writing-plans` to author Plan C (Phase 3 + 4: docs refresh, version bump, verification gates).

**Which approach?**
