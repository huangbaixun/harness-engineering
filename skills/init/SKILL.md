---
name: harness:init
description: >
  AI Agent Harness engineering initialization for new projects. Activate when users mention
  "new project", "project initialization", "set up Harness", "create CLAUDE.md",
  "set up Agent environment", "init harness", "start from scratch",
  "initialize AI coding environment", "establish Agent constraints", or
  "set up Claude Code project".
  Even if the user simply mentions wanting to "start a new project" or
  "configure an AI development environment", use this Skill,
  because every new project should begin by establishing a Harness.
---

# Harness Initialization Skill

> This Skill guides you in establishing a complete AI Agent Harness engineering system for a new project.
> Core philosophy: **Observe first, then constrain** — do not fill in every rule on day one. Instead, establish a minimal viable Harness and let the team discover what needs to be added through actual usage.

## Initialization Artifacts

After running this Skill, the following files will be generated in the project root:

| File | Purpose | Required |
|------|---------|----------|
| `CLAUDE.md` | Agent memory layer, <=60 lines, architecture conventions + prohibited rules + test commands + Skill trigger rules | Yes |
| `.claude/settings.json` | Permission control + Hook registration (including SessionStart) | Yes |
| `$TOOL_DIR/hooks/session-start.sh` | SessionStart: restore cross-session progress, archive prompts | Yes |
| `$TOOL_DIR/hooks/stop-typecheck.sh` | Stop Hook: type-checking gate | Yes |
| `$TOOL_DIR/hooks/pre-protect-env.sh` | PreToolUse: prevent .env from being overwritten | Yes |
| `$TOOL_DIR/hooks/post-format.sh` | PostToolUse: auto-format | Yes |
| `$TOOL_DIR/skills/plan/` | Pre-implementation planning Skill (integrated from Superpowers) | Yes |
| `$TOOL_DIR/skills/tdd/` | TDD workflow Skill (RED->GREEN->REFACTOR) | Yes |
| `$TOOL_DIR/skills/verify/` | Pre-completion verification Skill | Yes |
| `init.sh` | Session startup script, run before each new session to restore context | Yes |
| `docs/architecture.md` | Architecture diagram, Agent spatial awareness document, 100-150 lines | Yes |
| `docs/decisions/README.md` | ADR index | Yes |
| `docs/claude-progress.json` | Progress tracking (Agent-writable, requires archiving mechanism) | Yes |
| `docs/features.json` | Requirements list (Agent read-only, required for multi-person/multi-Agent setups) | Yes/Optional (depends on team size) |
| `docs/archive/` | Archive directory (prevents unbounded token growth) | Yes (generated alongside the above two) |

> **User expectation**: After initialization, running `bash init.sh` should display a summary of the current project status, indicating the Harness foundation is ready.

## Initialization Flow

### Phase 0: Detect Existing Harness

**Before asking any questions**, scan the project root for existing state:

```bash
# Step 1: Set the Claude Code config directory
TOOL_DIR=".claude"
echo "Config directory: $TOOL_DIR"

# Step 2: Detect memory file (priority: AGENTS.md > tool-specific file)
MEMORY_FILE=$([ -f "AGENTS.md" ] && echo "AGENTS.md" \
           || echo "CLAUDE.md")

# Step 3: Check whether key files already exist
ls "$MEMORY_FILE" "$TOOL_DIR/settings.json" "$TOOL_DIR/hooks/" init.sh 2>/dev/null
[ -f "$MEMORY_FILE" ] && wc -l "$MEMORY_FILE"
```

Based on the detection results, follow one of three paths:

| Scenario | Criteria | Action |
|----------|----------|--------|
| **Brand-new project** | Memory file does not exist | Proceed normally through Phases 1-6, generating from scratch |
| **Existing project (has memory file)** | Memory file exists with meaningful content | Enter "Existing Project Mode" (see below) |
| **Corrupted / empty file** | Memory file exists but is empty or <5 lines | Notify user, treat as brand-new project |

#### Existing Project Mode: Flow When a Memory File Already Exists

1. **Read and evaluate the existing memory file** (AGENTS.md / CLAUDE.md)
   - Is the line count <=60? How much does it exceed?
   - Does it have YAML frontmatter or structured sections?
   - Does it contain specific, verifiable rules (test commands, prohibitions)?
   - Does it contain vague, ineffective rules ("write good code", "keep things clean")?

2. **Report the evaluation to the user and explicitly ask their intent**:
   > "Detected an existing memory file `$MEMORY_FILE` (currently X lines). I can:
   > A) **Incremental addition** — keep existing content, fill in missing structure (Hooks, docs/, etc.)
   > B) **Optimize and consolidate** — streamline existing rules to <=60 lines while filling in structure
   > C) **Full rebuild** — back up the existing file as `$MEMORY_FILE.bak` and regenerate
   > Which approach do you prefer?"

3. **Mandatory backup before execution**:
   ```bash
   cp "$MEMORY_FILE" "${MEMORY_FILE}.bak"
   echo "Backed up to ${MEMORY_FILE}.bak"
   ```

4. **Execute based on selection**:
   - **Incremental addition**: Only append missing sections to the end of the existing file; do not modify existing content
   - **Optimize and consolidate**: Invoke the memory file streamlining logic from `harness:evolve`, then fill in structure
   - **Full rebuild**: Regenerate using templates, migrating valuable rules (test commands, etc.) from the original into the new file

> Similarly, check whether `$TOOL_DIR/settings.json`, `init.sh`, and `docs/architecture.md` already exist.
> Do not overwrite existing files — only replace after the user explicitly confirms.

---

### Phase 1: Information Gathering

Before generating any files, confirm the following information (proactively ask if the user has not provided it):

1. **Tech stack**: Primary programming language, framework, package manager
2. **Project type**: Web app / API service / CLI tool / Library / Monorepo
3. **Test framework**: Jest / Vitest / pytest / go test / other
4. **CI/CD**: GitHub Actions / GitLab CI / other
5. **Team size**: Solo / small team (2-5) / medium (5-15) / large (15+)

### Phase 2: Generate the Six-Layer Harness Structure

A Harness is not a single config file — it is six cooperating layers. Understanding each layer's responsibilities is the key to avoiding "more config, more confusion."

| Layer | Component | Core Responsibility |
|-------|-----------|---------------------|
| 1. Memory | `AGENTS.md` (universal) / `CLAUDE.md` | Static knowledge: architecture conventions, prohibited rules, test commands |
| 2. Rules | `$TOOL_DIR/settings.json` | Deterministic behavior: permissions, model, output config |
| 3. Skills | `$TOOL_DIR/skills/` + `$TOOL_DIR/commands/` | On-demand knowledge and manually triggered workflows |
| 4. Agents | `$TOOL_DIR/agents/` | Context-isolated specialized Subagents |
| 5. Hooks | Hooks (configured in settings.json) | Deterministic enforcement: does not depend on model judgment |
| 6. Tools | MCP Servers | Capability extension: external service integration |

> `$TOOL_DIR` = `.claude/`, exported by init.sh at session startup.

**Three-part synergy principle**: AGENTS.md rules alone are occasionally ignored; Hooks alone cannot handle judgment-based tasks; settings.json alone lacks context. All three working together is what makes the system truly effective.

### Phase 3: Generate Files by Tech Stack

Read the corresponding template directory to generate files. Template locations (`${CLAUDE_PLUGIN_ROOT}` is the plugin installation directory, automatically resolved in marketplace mode):

- TypeScript project -> read `${CLAUDE_PLUGIN_ROOT}/docs/templates/typescript/`
- Python project -> read `${CLAUDE_PLUGIN_ROOT}/docs/templates/python/`
- Go project -> read `${CLAUDE_PLUGIN_ROOT}/docs/templates/go/`
- Other -> read `${CLAUDE_PLUGIN_ROOT}/docs/templates/generic/`

#### Required File Manifest

```
project-root/
├── AGENTS.md                     <- Universal memory file (<= 60 lines), read by all tools
├── CLAUDE.md                     <- 2-line wrapper -> points to AGENTS.md (includes workflow Skill trigger rules)
├── init.sh                       <- Session startup script (exports $TOOL_DIR)
├── .claude/                      <- Claude Code config directory
│   ├── settings.json             <- Permissions + Hook registration (including SessionStart Hook)
│   └── hooks/                    <- Hook scripts (each hook provides .cmd + extensionless + .sh variants)
│       ├── session-start{,.cmd,.sh}  <- SessionStart: restore cross-session memory
│       ├── stop-typecheck{,.cmd,.sh} <- Stop Hook (language-adapted)
│       ├── pre-protect-env{,.cmd,.sh}<- PreToolUse: protect sensitive files
│       └── post-format{,.cmd,.sh}    <- PostToolUse: auto-format
├── $TOOL_DIR/
│   └── skills/
│       ├── plan/                 <- Pre-implementation planning (triggered when >30 min / 3+ files)
│       ├── tdd/                  <- TDD workflow (RED->GREEN->REFACTOR)
│       └── verify/               <- Pre-completion verification (triggered before declaring done)
├── docs/
│   ├── architecture.md           <- Architecture diagram (100-150 lines)
│   ├── decisions/
│   │   └── README.md             <- ADR index
│   └── claude-progress.json      <- Agent progress tracking (empty skeleton)
```

> **Note**: `AGENTS.md` is the single source of truth. `CLAUDE.md` is only 2 lines, directing users to `AGENTS.md`.

`init.sh` template is at: `${CLAUDE_PLUGIN_ROOT}/docs/templates/generic/init.sh.template`

#### AGENTS.md Writing Principles

AGENTS.md is the Agent's "worldview" — it defines the Agent's foundational understanding of the project, read by all AI tools.

**Good rules**: Specific, verifiable, corresponding to real past Agent failures
- "Never delete migration files"
- "All public APIs must have JSDoc comments"
- "Test command: `pnpm test`"

**Bad rules**: Vague, unverifiable, consuming tokens without producing constraints
- "Write high-quality code"
- "Keep code clean"

**<=60-line principle**: ETH Zurich research shows that overly long AI-auto-generated memory files degrade performance and consume 20% more tokens. Only hand-written, concise files are truly effective. Move excess content into `docs/` subdirectories and link to them from AGENTS.md.

#### architecture.md Writing Principles

The core goal is singular: enable the Agent to quickly build spatial awareness of the entire system at the start of a new session.

Must include:
1. **System-wide map**: One sentence explaining "what this system is and what its major components are"
2. **Directory structure description**: What each directory contains, more precise than a README
3. **Layer dependency rules**: The most important part — clearly state boundaries and automated verification mechanisms
4. **Key module descriptions**: One-sentence explanation of complex modules
5. **External dependency descriptions**: Service, purpose, integration point
6. **Further reading links**: Pointers to deeper documentation

Keep it to 100-150 lines — it is "a map, not an encyclopedia."

#### Hook Script Principles

**Decision criteria**: "Must this behavior always happen, regardless of Claude's judgment?" -> If yes, use a Hook.

**Silent on success, visible on failure**: 4000 lines of passing logs will cause the Agent to lose focus on its task.

**Exit code conventions**:
- `exit 0` — Success, continue
- `exit 2` — Failure, error message fed back to Agent, Agent continues to fix
- `exit other` — Failure, not fed back to Agent (non-blocking)

### Phase 4: Establish Initial ADRs

Create an ADR for each key technical decision already made in the project. Each ADR must include:
- Context (write the trigger conditions, not the conclusion)
- Options considered (including rejected ones, to prevent the Agent from repeating past mistakes)
- Decision and rationale
- Consequences (use the format "Prohibited: X, must use Y" — this is the most constraining format for Agents)

### Phase 5: Initialize Progress Tracking

Determine which files to generate based on team size:

| Scenario | `claude-progress.json` | `features.json` |
|----------|----------------------|-----------------|
| Solo, single Agent | Yes (required) | Optional |
| Multi-person or multi-Agent parallel | Yes (required) | Yes (required) |

> **Decision criteria**: If the user mentions "team", "multiple people", "multiple Agents in parallel", or "Sprint", `features.json` is upgraded to required.

Use JSON instead of Markdown: Agents respect structured data significantly more than plain text, and are less likely to accidentally overwrite or delete records.

#### Responsibilities of the Two Files

| Dimension | `claude-progress.json` | `features.json` |
|-----------|----------------------|-----------------|
| **Who writes** | Agent writes, human supervises | Human writes, Agent read-only |
| **What it records** | "Where we're at" | "What needs to be done" |
| **Update frequency** | End of each session | When requirements change (relatively stable) |
| **Multi-Agent conflict risk** | High (concurrent writes by multiple Agents) | Low (read-only) |
| **Token growth trend** | Continuous growth (requires archiving) | Relatively stable |

#### features.json Usage Rules

**Agent read-only principle**: `features.json` is maintained by humans; the Agent must never write directly to this file.
- The Agent may read features.json to understand requirements, priorities, and dependencies
- If the Agent discovers requirement changes or new requirements, record them in the `notes` field of `claude-progress.json` for human review before deciding whether to update features.json
- Violating this principle leads to a trust crisis of "AI silently changing requirements"

**Cancel, don't delete principle**: When a requirement is cancelled, change `status` to `"cancelled"` and fill in `cancelled_reason` — **never delete entries**.
- Deletion loses historical decision context; the Agent may re-propose the same direction in the future
- Cancelled entries represent "reasons not to do this" — they are valuable constraint information

**Extended fields for multi-person/multi-Agent setups** (can be omitted for solo use):

```json
{
  "id": "F-003",
  "title": "OAuth Login",
  "status": "in_progress",
  "priority": "high",
  "description": "Support GitHub / Google OAuth",
  "owner": "agent-alice",
  "depends_on": ["F-001"],
  "blocks": ["F-005"],
  "files_owned": ["src/auth/", "src/middleware/oauth.ts"],
  "worktree": "feature/oauth",
  "acceptance": "All OAuth tests pass, no hardcoded .env values"
}
```

Valid `status` values: `planned` -> `in_progress` -> `done` | `cancelled`

#### Token Growth and Archiving Mechanism

Warning: **Without an archiving mechanism, after 6 months each session will consume an extra ~8000 tokens** (the `completed` list grows unboundedly).

Write the following rules into AGENTS.md during initialization:

```markdown
## Progress File Archiving Rules
- When claude-progress.json's completed_features exceeds 10 entries,
  move the oldest records to docs/archive/progress-YYYY-QN.json, keeping only the 5 most recent in the main file
- Compress features.json entries with status=done each quarter (keep only id + title + done_at),
  archive full records to docs/archive/features-done.json
- Agent reads only the in_progress, blockers, and notes sections of claude-progress.json each session,
  no need to read the full completed_features history
```

Also generate the archive directory skeleton:

```
docs/
├── features.json              <- Active requirements (planned + in_progress)
├── claude-progress.json       <- Current progress (in_progress + blockers)
└── archive/                   <- Archive directory (Agent does not proactively read)
    ├── .gitkeep
    └── README.md              <- Describes the archiving strategy
```

### Phase 6: Verification and Delivery

After completing initialization, run verification checks:

1. CLAUDE.md line count <= 60
2. All Hook scripts have execute permissions (`chmod +x`)
3. Hook registration in settings.json is correct
4. architecture.md includes dependency rules
5. docs/decisions/README.md index is complete

Output an initialization summary including:
- List of generated files
- Suggested "Week 1-2 observation items" (run the Agent on real work for two weeks first, recording failure patterns)
- Follow-up iteration suggestions (pointing to harness:audit and harness:evolve)

## Permission Enforcement vs. Model Reasoning Separation

Pay special attention to this architectural principle during initialization:

- **CLAUDE.md** = Explains "why you cannot do this", helping the Agent understand intent
- **settings.json + Hooks** = Enforces "you cannot do this under any circumstances", independent of Agent understanding

Both are needed, each serving its own role. CLAUDE.md alone is a soft constraint; Hooks alone are hard constraints but lack contextual explanation. The combination of both provides complete protection.

## Anti-Pattern Reminders

Avoid the following anti-patterns when generating:

| Anti-Pattern | Correct Approach |
|--------------|-----------------|
| Bloated CLAUDE.md (>100 lines) | Trim to <60 lines, move complex rules into Hooks |
| Putting all conventions in CLAUDE.md | "Must execute" = Hook; "Should follow" = CLAUDE.md |
| Not listing rejected options | ADRs must list rejected options to prevent the Agent from re-proposing them |
| Hook outputting logs on success | Completely silent on success, only produce output on failure |
