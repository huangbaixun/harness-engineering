# ADR-0008: Vendor superpowers v5.1.0 into harness-engineering

## Status
Accepted — 2026-05-23

## Supersedes
The implicit fork strategy embedded in v1.9.x–v1.11.x, where four skills (`plan`, `tdd`, `verify`, `router`) were forked from `obra/superpowers @ 917e5f5` and renamed for shorter triggers.

## Context
The harness-engineering plugin diverged from `obra/superpowers` at commit `917e5f5`. Since then upstream released v5.1.0 with 14 skills — 4 corresponding to our forks plus 10 new ones (`brainstorming`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `using-git-worktrees`, `systematic-debugging`, `receiving-code-review`, `requesting-code-review`, `finishing-a-development-branch`, `writing-skills`).

The fork is stale, naming is divergent, and a per-skill maintenance contract for ongoing sync is missing.

## Decision
Vendor all 14 superpowers v5.1.0 skills into this plugin (13 with sidecar structure; `using-harness` as harness-original — see Section 4). End state: 19 skills under the `harness:` namespace.

## Considered alternatives
1. **Depend on the superpowers plugin** — rejected: introduces a runtime dependency on a separately-installed plugin and prevents harness from carrying its own localized rules.
2. **Git submodule of upstream** — rejected: automated sync conflicts with ADR-0004's requirement that each skill change go through the skill-creator eval loop. Each upstream diff is a judgment call, not a mechanical apply.
3. **Keep only the 4 existing forks; do not import the 10 new ones** — rejected: misses real capability (brainstorming, executing-plans, writing-skills are first-class needs of this plugin's workflow).

## Consequences
**Positive:**
- Single-source-of-truth: harness owns its skills regardless of upstream plugin availability
- Naming aligned with superpowers (same patterns, discoverable)
- Future sync is explicit and reviewable per ADR-0004

**Negative:**
- Breaking change: 4 old slash command names (`/harness:plan` etc.) are replaced
- Maintenance burden: each upstream release requires per-skill reconciliation

## Implementation
See `docs/specs/2026-05-23-superpowers-integration-design.md` (covers all phases) and `docs/plans/2026-05-23-phase-0-and-1-foundations-and-rename.md` (Phase 0 + Phase 1 execution).

## Related
- ADR-0004 (skill-creator methodology) — applies to all 14 reorganized skills' evals
- ADR-0009 (harness-delta sidecar 4-file convention) — sibling decision establishing per-skill structure
- ADR-0007 (Claude Code only) — namespace context
