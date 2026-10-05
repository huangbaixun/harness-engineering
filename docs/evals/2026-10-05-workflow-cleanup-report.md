# Harness workflow cleanup — local verification

User approved the preceding audit and P0 → P1 → P2 repair order. Work is isolated
on `codex/harness-workflow-cleanup`, based on main commit
663e8f31f3a8670b515aeb256b5bb779efdf7d57. No consuming AIDC changes, real Issue calls,
credentials, global settings, push or deployment occurred during verification.

## Delivered behavior

| Priority | Repair | Evidence |
|---|---|---|
| P0 | Retire default progress auto-commit, empty formatter and homemade telemetry registrations; shared real argv verifier | Disposable staged-work preservation; failure and empty-config regressions; explicit verifier report |
| P1 | Shared bounded context, neutral checkpoints, native compaction guidance and selected workflow review; narrow native-stdin direct-path guard | Claude/Codex protocol regressions, checkpoint tests, malformed-event and env-example tests; agent/sidecar review |
| P2 | Evidence-based audit/evolution, no universal line/token quotas or fixed model aliases; portable manifest with explicit OpenAI hook override; offline Claude adoption | Manifest/path/version tests, instruction/settings byte preservation, paired response evaluation and final independent review |

The default catalog retains 19 skills and progressive discovery. No unnecessary
second dispatcher or evaluation service was introduced. Compatibility manifests,
retired warning stubs, opt-in Issue sync and upstream licenses/provenance remain.
Existing installations require reviewed migration; conflict-first adoption does not
silently overwrite their runtime or hook settings.

## Executed checks

- Baseline: 14/14 offline regression files passed.
- Final: `python3 scripts/validate.py` passed 16/16 files: 55 Python cases and nine
  shell regression files (the latter include multiple scenarios).
- `harness_runtime.py verify --project . --report <local report>` executed the
  configured full suite successfully; inspected report shows success=true, exit=0,
  local duration 7630.149ms, tokens/cost=null. This is one local observation, not a
  latency improvement or native host usage measurement.
- Read-only reconciliation against pinned Superpowers 6.4.2 reports all 13 skill
  bodies unchanged after permitted normalization and no companion/mode differences.
- `git diff --check` passed. Successful runtime verification is silent.

Meaningful RED → GREEN evidence: retired-hook/default registration and native
adapter tests initially failed; manifest escape/missing-target/version/implicit
fallback tests failed before validation changes; independent review's legacy pull
regression failed before adding root→docs fallback. No network call was required.

## Skill behavior evaluation

Three independent mode-specific agents answered the same four advisory scenarios:
audit, evolve, init and archive. Each mode had one response per case (12 total),
with archive supplied as a follow-up in its mode-specific context. An independent
agent graded actual outputs using the same four assertions per case. These are
scenario responses, not real host/product execution or randomized repeated trials.

| Case | Prior skill | No-skill control | Updated skill |
|---|---:|---:|---:|
| Audit no-op hook / existing CI | 3/4 | 4/4 | 4/4 |
| Evolve quotas / compaction / review | 3/4 | 4/4 | 4/4 |
| Offline Claude adoption | 2/4 | 3/4 | 4/4 |
| Archive shared design / handoff | 3/4 | 4/4 | 4/4 |
| Total | 11/16 | 15/16 | 16/16 |

[Generated skill-creator review viewer](workflow-cleanup/review.html),
[benchmark](workflow-cleanup/benchmark.json),
[independent assertion evidence](workflow-cleanup/grading.json).
The control already succeeds on most criteria; these samples identify old-policy
drift and the concrete initializer interface, not general model superiority.
Personal filesystem prefixes in stored response artifacts are normalized; response
content and grades otherwise remain intact. Agent token/cost/duration are unavailable
and remain unknown. Human viewer review
is available but has not been performed by the user. Other catalog eval definitions
are not claimed as executed. Vendored sidecar corrections were reviewed against
actual code; exhaustive behavioral evaluation of all 13 workflows was not performed.

## Independent review and limits

Reviewer independently ran Claude hook/init tests and the full suite. Fixed its
legacy SessionStart pull regression and stale TDD/SDD sidecar rules. Root feature
configuration wins over legacy config; enabled legacy projects retain optional pull.
Reviewer confirmed corrections and found no remaining core must-fix issue.
Windows wrapper exit propagation was corrected, then changed to label-based return
handling to preserve literal exclamation marks without delayed expansion. Bash-path
protocol execution passes; native Windows execution remains unverified.

Native hook trust/loading/lifecycle and App/Cloud parity remain unverified. A Stop
request does not intercept commits, enforce all acceptance criteria or prove
completion; direct-path protection does not secure Bash. F008 remains building until
separately authorized integration; implementation and local acceptance are complete.

Sources: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Claude hooks](https://code.claude.com/docs/en/hooks),
[Claude agent model selection](https://code.claude.com/docs/en/sub-agents),
[GPT-6 skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
