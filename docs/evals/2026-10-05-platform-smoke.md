# Platform smoke evidence — 2026-10-05

## Codex CLI 0.158.0

- Local app-server skills/list: 19 harness skills, zero discovery errors. Repeated discovery after the final upstream sibling-layout fix, with the same result.
- Local app-server plugin/read: manifest version 2.3.0, 19 skills and separate hooks returned. No installation, trust bypass or global edits. Plugin namespace is automatically added by Codex (`harness:harness:<name>`); project skills use `harness:<name>`.
- Actual ephemeral CLI execution in an isolated fixture used approved planning, TDD, verification and archive skills: RED seven failures (missing clamp implementation), GREEN seven behavioral tests, explicit configured verification exit 0, exact steering checkpoint, completed spec/plan archive. Source skills/resources remained unchanged.
- The first execution used prefixed project folders; independent review subsequently exposed Native helper dependencies. Final layout discovery plus actual task-start/task-done regression in a disposable Git repo verifies the correction. We do not imply the original smoke exercised Git-based helpers.
- CLI trace reported 48,324 tokens for that run; this is a CLI trace figure, not a comprehensive token/cost benchmark. Monetary cost and paired-eval timings remain unknown. Raw traces and local paths are not committed.
- Protocol fixtures cover bounded SessionStart, Stop failure blocking once, malformed inputs, path containment and manual checks. Native trusted hook lifecycle execution is **not verified**. Project installation does not register hooks. App/Cloud parity is **not verified**.

## Claude Code

Native plugin/marketplace validation passed; plugin validation warns that root CLAUDE.md is not loaded as plugin project context. Existing skills provide context and the hook registrations remain unchanged. All nine original shell regression files pass with stubs; no real Issue operations were run. A new live Claude model workflow and hook lifecycle were not exercised; structural/regression preservation is the demonstrated boundary.

## Independent review

Fresh-context reviewer found four functional defects, all accepted and fixed RED→GREEN: companion sibling layout, executable bits, plugin runtime paths, regular-file ancestor preflight. Re-review: no remaining important defect, 11 initializer tests and full 14 regression files passed. Minor routing pointer corrected. A subsequent twelfth initializer regression verifies compatible custom configuration preservation; CRLF byte-preservation variant passes after explicit byte decoding. Compatible configuration is preserved rather than reset when restoring skills.

Review exclusions accepted: trusted hooks, App/Cloud, general reliability/cost claims and pending human viewer review are outside demonstrated evidence. AIDC checks were subsequently completed below.

## AIDC project adoption

Previewed 183 delivery files before writing. Original AGENTS bytes remain intact; portable configuration uses exactly npm run check and npm test. No dist/ changes. Skill/runtime files stay local under the project's existing .agents ignore rule; portable config and setup instructions are reviewable project source. Progress and verification reports are ignored local state.

- npm run check: 89/89 syntax checks.
- npm test: 33/33 test modules.
- Native Chrome/WebGL: campus → A-POD01 → R096 → NPU-01 → return. Device model rendered and official reference links/simulation disclaimers remained visible.
- Simulated return-liquid alarm on A-POD01/R096 does not appear in A-POD03; switching back preserves the original alarm. Cleared the disposable alarm afterward.
- 390×844 viewport: campus model, building/POD controls and inspector visible; viewport restored. This is responsive emulation, not physical mobile-device testing.
- Console: no errors observed, one existing Three.js PCFSoftShadowMap removal warning. No third-party rewrite performed.
- Does not establish physical GPU compatibility, real telemetry, fire compliance, engineering certification or all 16 POD combinations.

## Limits

This is bounded representative verification. GPT-6 model routing remains host/user controlled; prompt caching, compaction and asynchronous execution are not implemented by this framework. Human review of the paired skill viewer remains pending. Local CLI/project scope is delivered; native trusted automatic lifecycle remains an explicit capability gap.

## Completion / archival review

Documentation matches the shared-core and separate-adapter implementation; required scripts are present, versions align at 2.3.0 and ADR-0013 is accepted. New implementation scripts are below 300 lines. Upstream large companions remain exact source artifacts. No reverse-direction dependency was introduced. Active design and execution plan remain linked by ADR/features/evaluation evidence, so they are retained; historical F001–F005 archival and shared living-doc changes belong outside F007 (F006). No documents were silently moved. F007 remains building pending integration into main; local implementation and acceptance are complete. No merge, push, global installation or deployment was performed.

## Main integration — 2026-10-05

User explicitly requested pushing the Harness changes to GitHub main. Fetched origin/main at 2b6bc0261901ed6ab5fc23ddf051e968d530843a; it was an ancestor of the reviewed implementation. Fast-forwarded local main to the implementation and reran the complete offline validator. F007 transitions to done for the demonstrated local CLI/project scope. Previously noted native hook and App/Cloud limits remain. Active linked design/plan remain available; F006 and historical archival are unchanged. AIDC is not part of this push.
