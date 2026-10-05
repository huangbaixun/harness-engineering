# GPT-6 workflow guidance

Apply when maintaining harness instructions or configuring a long-running coding workflow. This is a local adaptation of the OpenAI guide, not a claim that this package implements API services.

## Assignment and autonomy

State outcome, constraints and observable completion criteria. Continue already-authorized local work: inspect, edit, run disposable-data tests, fix failures, and validate. Ask when a missing answer changes scope or an action crosses the user's authorization boundary. A completed design/plan approval does not need to be requested again for the same scope. Do not replace project permission rules.

Select only relevant skills and supporting references. Keep descriptions discriminating; generic new-project mentions do not authorize installing a harness. Do not load every skill or enforce unrelated steps solely because the task resembles a keyword. Keep determinism where it matters: source provenance, schema checks, test exit codes, no secret/config overwrite.

## Long-running work

Preserve objective, latest steering, accepted decisions, blockers, next action and pointers to verification evidence in a small checkpoint. Treat a new user correction as steering of the current task unless they cancel it. Read this checkpoint after compaction; do not replay completed tasks or replace the original goal silently. Use `scripts/harness_state.py checkpoint --project . --task F007 --next-action 'run regression' --steering 'latest accepted correction'` explicitly; never persist secrets or full session transcripts.

Keep stable project instructions separate from changing state. SessionStart emits a bounded state snapshot rather than injecting the entire skill catalog. Native compaction, caching and asynchronous tools are host/API capabilities; this package does not claim to implement them. Independent reads/checks may run concurrently when supported; wait for dependencies before mutation. Delegate bounded independent work only when authorized and available; shared-file implementation stays sequential.

## Model and effort

Preserve the user's selected model and the host's model/effort defaults. For an explicit routing configuration, use workload-based recommendations: difficult architecture/review may justify Astra; complex coding commonly fits Sol; bounded repeatable tasks may fit Luna. Confirm names and availability from the actual tool allowlist. Raise effort only when evidence shows quality needs it. Do not automatically force every task to maximum effort or change global settings. These are recommendations, not capability guarantees or an automatic router.

## Evidence and cost

Done means implementation, execution, inspection of results and resolution of relevant failures. Check the behavior the user needs; static validation is not a substitute for UI/runtime checks. Report changes, checks and limits concisely. `scripts/codex_hook.py verify --project . --report .harness/verification.json` measures local verification success and wall time. Token usage and monetary cost remain null unless supplied by a real host measurement; do not infer model cost from elapsed time. Compare representative baseline/with-skill tasks, noting small samples and uncertainty.

Sources, checked 2026-10-05:
- https://openai.com/index/practical-guide-building-gpt-6/
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
