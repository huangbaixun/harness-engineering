# harness-delta: writing-skills

## Upstream
superpowers v6.3.0 (commit SHA recorded in UPSTREAM.md)

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
- Individual SKILL.md ≤ 500 lines (project rule, per CLAUDE.md "Prohibited Practices") — applies to **harness-original** skills only.
  Vendored SKILL.md files are byte-for-byte upstream (ADR-0009), so their length is upstream's call, not ours: trimming one
  would be an edit outside the 2 allowed and would make every future sync a manual merge. As of the v6.3.0 sync,
  `writing-skills` (681 lines) and `subagent-driven-development` (570) exceed the cap by upstream's choice.

### Terminology: SDO, not CSO (renamed in v6.3.0)
Upstream renamed "Claude Search Optimization (CSO)" to **"Skill Discovery Optimization (SDO)"** and de-branded the surrounding
prose from "Claude" to "agent". Use SDO in new harness docs, evals, and commit messages. The substance is unchanged:
`description:` states triggering conditions only and never summarizes the workflow.

### Match the form to the failure before writing guidance (new in v6.3.0)
v6.3.0 added a section requiring you to classify the *baseline failure* before choosing a guidance form — prohibition +
rationalization table for discipline failures, positive recipe/contract for wrong-shaped output, a structural REQUIRED slot
for omissions, a conditional for context-dependent behavior. It also requires behavior-shaping wording to be **micro-tested
against a no-guidance control** (5+ reps, every flagged match read by hand) before the full pressure scenarios.

In this repo that sits *inside* step 3 of the ADR-0004 loop, it does not replace it: micro-tests verify wording, `evals/evals.json`
with-skill-vs-baseline runs remain the commit gate.

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
