# Codex adaptation and GPT-6 workflow evaluation

## Scope and method

User requested Codex compatibility and then the OpenAI GPT-6 family guide as optimization input. Applied the skill-creator baseline/with-skill workflow to harness-original using-harness and init. Four fresh-context agent runs: two cases, one old-skill and one new-skill run each. Read-only scenario responses; no production edits, external effects or model switching. Inline assertion grading; human viewer review remains pending.

| Case | Old skill | Updated skill | Finding |
|---|---:|---:|---|
| Approved Native work with GPU steering | 4/4 | 4/4 | Both preserve user scope. New routing provides platform references and checkpoint continuity; this case does not establish superiority. |
| Codex adoption with existing AGENTS | 2/4 | 4/4 | Old skill proposes an ad-hoc wrapper; new skill references the implemented dry-run initializer and a single discoverable skill delivery. |

[Actual response comparison viewer](codex-adaptation/review.html), [benchmark](codex-adaptation/benchmark.json). Single samples and manual grades are diagnostic; do not treat 100% as general reliability. Agent interface did not supply wall time, token use or cost; those measurements are unknown, not zero. Aggregator defaults and delta direction were corrected in the stored benchmark to avoid misleading measurements.

Behavioral evaluation exposed trimming of existing AGENTS trailing whitespace. Added a failing byte-preservation test, fixed initializer, then observed GREEN. Already-existing project rules now retain all bytes outside the managed block. Twelve initialization tests pass, including reuse of the project-bundled initializer and preservation of the upstream license.

## Upstream reconciliation

All 13 vendored workflows moved from superpowers 6.3.0 to release 6.4.2, pinned at commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d. Body comparison after the two permitted edits reports zero differences; companion files match upstream bytes. Removed the obsolete plan reviewer companion per upstream release. Upstream MIT notice preserved under third_party/superpowers/LICENSE.

Changes reviewed: lean interface-based planning; Native execution with per-task ledger and final review; tool/context adaptation; first-class task-start/task-done helpers. No new upstream skills are implicitly added to the 19-skill catalog. Local platform rules stay in sidecars/references. This report does not claim exhaustive behavioral benchmarking of all 13 workflows or all existing eval cases.

## GPT-6 guide application

| Guide principle | Delivered behavior |
|---|---|
| Clear task, decision boundaries and persistence | Narrow routing, existing approvals respected, no automatic global changes; done includes running and inspecting checks |
| Progressive disclosure | Load relevant references; SessionStart emits bounded state, not the entire routing skill |
| Long-task steering and compaction | Explicit atomic checkpoint retains task, next action and steering; neutral progress with read-only legacy fallback |
| Workload-based model/effort choice | Guidance preserves host/user selection; no automatic maximum effort or global model edits |
| Representative evaluations and measurements | Paired response evidence plus real tests; explicit verification report records success/time and leaves cost/tokens unknown |
| Async/parallel work with dependencies | Independent reads may overlap; mutations and dependent checks remain ordered; Native implementation plus final independent review |

These are local workflow adaptations. API caching, compaction, asynchronous execution and pricing are host capabilities, not implemented by this repository.

Sources:
- https://openai.com/index/practical-guide-building-gpt-6/
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/hooks

## Independent review corrections

Four functional findings accepted and fixed with regression tests: preserve upstream sibling directory names and executable modes so Native helper scripts work; render delivery-specific plugin runtime paths; reject regular-file ancestors during conflict preflight. Original harness: skill names remain unchanged. This deliberately adjusts the plan's proposed harness- directory prefixes without changing upstream bytes. Actual task-start/task-done execution now passes in a disposable Git fixture.

Review-only exclusions accepted: native hook trust/lifecycle and App/Cloud parity remain unverified; human review of the skill response viewer remains pending; these limits do not imply functional test success. No broad reliability or cost improvement is claimed.

Portable project configuration may be checked in independently of local skills. Reinitialization preserves compatible existing configuration, including verification commands and extension fields; incompatible tool/schema/delivery conflicts before writes. Added RED→GREEN regression for this adoption path.
