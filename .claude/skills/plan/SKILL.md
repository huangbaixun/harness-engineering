# harness:plan — Pre-Implementation Planning

> **upstream**: obra/superpowers `writing-plans` @ [917e5f5](https://github.com/obra/superpowers/tree/917e5f5/skills/writing-plans)
> **harness-delta**: Added features.json reading (Step 1), OpenSpec XML three-phase task structure, rigid/flexible constraint classification, human confirmation gate, and Stop Hook integration with Harness

> Adapted from the obra/superpowers Writing Plans skill for the Harness Engineering workflow.
> Core principle: Having the Agent align on design before coding is the highest-ROI checkpoint for reducing directional errors.

## When to Use

Under any of the following circumstances, execute this workflow **before writing any code**:

| Circumstance | Example |
|------|------|
| Implementing a new feature from features.json | coding-agent picks up the next feature |
| Non-trivial bug fix (affects more than 1 file) | Fix requires changes in multiple places |
| Refactoring (affects module boundaries or interfaces) | Adjusting layer relationships, splitting modules |
| Receiving a new requirement description | User describes a new feature |

Decision rule: **If the estimated implementation exceeds 30 minutes or involves more than 3 files, planning is mandatory.**

## Planning Workflow

### Step 1: Clarify Requirements (Brainstorm)

Read the current feature from `docs/features.json`, **distinguishing rigid from flexible constraints**:

**rigid (hard constraints, cannot be skipped or downgraded):**
- `acceptance_criteria` — Acceptance criteria; each must map to at least one task's `<verify>`
- `out_of_scope` — Explicitly what not to do; violations are treated as over-implementation
- `forbidden_patterns` — Forbidden patterns (if any); violations block completion
- `dependencies` — Prerequisites; must be confirmed satisfied before starting

**flexible (soft constraints, Agent may adjust based on actual conditions):**
- `description` — Feature intent, used as reference rather than a literal spec
- `technical_notes` — Technical suggestions; alternative approaches are acceptable
- `related_files` — Reference files; actual implementation may involve additional files

If there is any ambiguity, confirm with the user before starting to plan. **Do not assume.**

### Step 2: Break Down into Three-Phase Task Blocks

Break the work into independent tasks of **2-5 minutes** each. Each task must use the **`<action> -> <verify> -> <done>` three-phase structure**:

- `<action>` — What to execute specifically (create file, modify function, add configuration...)
- `<verify>` — How to verify correct execution (tests pass, file exists, command output matches...)
- `<done>` — Completion marker and status update (update progress, mark rigid item as covered...)

Each block must also be labeled with its constraint type:
- **[rigid]** — Covers a rigid constraint from features.json; cannot be skipped
- **[flexible]** — Implementation detail decomposed by the Agent; may be merged or adjusted

**Output format (three-phase):**

```markdown
## Implementation Plan: [Feature Name]

### Rigid Constraints (from features.json)
- AC-1: JWT token validity 24h
- AC-2: Password bcrypt encryption
- OOS-1: Do not implement OAuth third-party login

### Task List

T01 [rigid:AC-2] Create password encryption module
  <action> Create src/auth/password.ts, implement hashPassword / verifyPassword
  <verify> Run pnpm test src/auth/password.test.ts, all pass
  <done>   AC-2 covered, update claude-progress.json

T02 [rigid:AC-1] Implement JWT issuance and verification
  <action> Create src/auth/jwt.ts, set expiresIn: '24h'
  <verify> Unit test verifies token expiration is 24h
  <done>   AC-1 covered

T03 [flexible] Integrate into UserService
  <action> Call password + jwt modules in src/services/user.ts
  <verify> Integration tests pass
  <done>   Update progress

T04 [flexible] Update API routes
  <action> Add POST /api/auth/login route
  <verify> e2e tests pass
  <done>   Feature complete, trigger harness:verify

### Out of Scope
- OOS-1: Do not implement OAuth third-party login

### Risks
- T02 depends on JWT_SECRET environment variable being configured
```

**Coverage check**: All rigid constraints must be covered by at least one `[rigid:xxx]` task. If any rigid item is uncovered, the plan is incomplete and additional tasks must be added.

### Step 3: Human Confirmation Gate

**After outputting the plan, wait for user confirmation before starting execution.**

Do not automatically begin coding after planning. The plan is an alignment point, not an automatic trigger.

After user confirmation:
1. Write the task list to the `in_progress` field of `docs/claude-progress.json`
2. Execute in order, updating status after each task is completed
3. Run the corresponding verification after each task is completed

## Relationship with OpenSpec

If the project uses OpenSpec:
- `openspec/changes/proposal.md` corresponds to Step 1 of this Skill (clarify requirements)
- `openspec/changes/tasks.md` corresponds to Step 2 of this Skill (task breakdown)
- When they overlap, OpenSpec artifacts take precedence; this Skill provides Harness context sync

## Plan Quality Checklist

A good plan satisfies:
- [ ] Each task has a complete `<action>` / `<verify>` / `<done>` three-phase structure
- [ ] All rigid constraints (acceptance_criteria + out_of_scope + forbidden_patterns) are covered by at least one task
- [ ] No task description uses vague language like "implement X feature"
- [ ] out_of_scope is explicitly listed
- [ ] Dependency order is clear (dependent tasks come after the tasks they depend on)
- [ ] Total task count <= 15 (more than that means the feature is too large and should be split in features.json)
- [ ] [rigid] tasks cannot be marked as "skipped" or "deferred"
