# F006 archive trial — local acceptance evidence

The user selected reliable long-task completion by one developer and approved this
trial. Implementation and local acceptance are complete. On 2026-10-07 the user
authorized committing F006 to main and pushing it; the feature is marked done
for that integration. No Issue hooks, deployment or global configuration were invoked.
Pre-existing reference/deck/demo changes were preserved; this task added only its
own Unreleased changelog entry, feature record, skill changes and trial artifacts.

## Resulting behavior

Archive classifies candidates once, retains specs needed by active features or
living code/documentation, and moves verified execution plans with repairable
historical links. Reports identify all referring feature IDs and concrete consumers.
Moves preserve metadata, repair local references and require post-move checks.
Unknown completion/use or a conflicting destination causes retention and disclosure.
A retained live spec does not undo a verified feature's done status.

## Acceptance evidence

| F006 criterion | Evidence | Local conclusion |
|---|---|---|
| Shared spec stays until all referring features are done | Eval 6: F101 plan moves, shared design and F102 state/link stay; actual temporary files match saved snapshot | pass |
| Distinguish execution plans and living specs | Evals 7/8: source/guide-consumed API contract stays despite both features done; finished plan moves despite historical link | pass |
| Inspect inbound links and report required repairs | Evals 6/8: feature links and relative history link repaired; all saved Markdown targets resolve; reports list consumers | pass |
| Skill-creator baseline/with-skill evaluation | Two iterations, updated/old/no-skill runs; actual file outputs, independent-context assertion grading and generated viewer | pass; human review pending |

Sources: [final file checks](f006-archive/iteration-2/file-checks.json),
[benchmark](f006-archive/iteration-2/benchmark.json),
[review viewer](f006-archive/iteration-2/review.html).

## Behavioral evaluation and limits

| Iteration | Updated skill | Old skill baseline | No-skill control |
|---|---:|---:|---:|
| 1 | 11/12 | 9/12 | 7/12 |
| 2 | 12/12 | 9/12 | 7/12 |

Three isolated mode-specific agent contexts each executed the same three tasks in
fresh disposable Git repositories per iteration: 18 case executions total. Four
assertions per case combine file-state correctness and report specificity. The
first iteration exposed a missing shared co-owner in the updated report. The rule
was clarified and all modes rerun; original outputs and grades remain available.

Old-skill file behavior already succeeded on these samples. Its failed assertions
concern report specificity or explicit verification evidence. The no-skill control
relocated the living API contract while keeping links valid; other failures concern
archive conventions/metadata/reporting. These totals do not establish a general
success-rate gain. One run per case/mode is a small sample; modes reused their own
context across cases. The grader also executed old baselines, so those grades are
not blind independent re-execution. Root additionally checked updated snapshots
against live temporary files and resolved every saved Markdown link target.

Base source revision: 1eb4738f18a38d496cb48f4eea0ba22c2b5739e4, with an existing dirty
working tree. Final skill SHA256:
771845291f52c32cc293f81f23dd852ceec73a82628493eb6311dba5185e5609.
Exact old, initial updated and final skill snapshots are stored with the evaluation.
Timing, tokens, cost and exact executor model ID are unavailable; benchmark values
remain null/unknown rather than inferred from output length.

## Offline checks and remaining unknowns

`python3 scripts/validate.py` passed all 16 regression files after the final skill
change. `git diff --check` passed. No scripts, hook registration, dependencies,
vendored skills or architecture layers changed. Existing command-name provenance
in the archive skill is inherited; no new command dependency was introduced.

Disposable repos had staged files and no commits. `git mv` was executed, but
`git log --follow` history and recent-file age could not be demonstrated there.
Collision handling, unknown classification and multiple-feature archive metadata
are specified but not behaviorally exercised in this three-case trial. Native
Claude/Codex skill discovery, hook lifecycle, multi-session recovery, requirement
changes during execution and real long-task outcomes remain unknown. Human viewer
feedback has not been received.

## Local handoff

The spec and plan stay available as linked acceptance and evaluation context. Runtime
handoff is saved through scripts/harness_state.py, outside stable instructions.
No historical F001–F003 artifacts were moved. The user authorized main integration and push; human viewer feedback remains
pending and is not claimed as completed.

Commit preparation: response Markdown trailing whitespace was normalized; raw
state snapshots and grading evidence are unchanged. Fresh 2026-10-07 offline
validation passed all 16 regression files.
