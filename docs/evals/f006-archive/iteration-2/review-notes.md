# F006 scoped review and grading

Reviewed the final archive skill, F006 design/plan, original assertions, and actual response/state evidence for all nine runs in each iteration. Implementation and fixtures were not changed by this review.

| Iteration | Updated skill | Old skill | No skill |
| --- | --- | --- | --- |
| 1 | 11/12 | 9/12 | 7/12 |
| 2 | 12/12 | 9/12 | 7/12 |

Each run has a sibling grading.json with assertion verdicts and concrete evidence. Tokens, costs and native host timings are unknown. The grader also executed the old-skill baselines; these grades are assertion-based and separately performed after execution, but are not blind or from a different evaluator for that baseline. Iteration 2 reused the same fixture prompts after feedback; it is a targeted rerun, not an unseen holdout.

## Concrete findings

No must-fix implementation defect was established in the reviewed change. The final skill makes selected-feature scope, shared versus living retention, historical-plan relocation, unknown evidence, destination conflicts, reference repair, preserved frontmatter and no implied external effects explicit. The evaluated updated-skill file states and all saved relative Markdown links are correct. F102 remains building and unchanged; the API contract stays active; F301 retains its owner metadata and traceable local move.

The old baseline also gets the substantive file behavior right in all three fixtures. Its 9/12 total reflects report specificity and verification evidence: case 6 does not identify F101 as another shared-spec owner, case 7 says user guide without the concrete docs/guide.md path, and case 8 does not document execution of repaired inbound-target checks. Do not describe these scores as three destructive or unsafe file outcomes.

No-skill runs repair valid links and preserve statuses, but move the living API contract. Two other failures are exact destination convention mismatches (archive/plans instead of archive root), and one is omitted archive metadata. Their 7/12 score therefore mixes convention, metadata and substantive living-contract policy.

## Inherited limitations

- The old skill already said shared/live documents stay in place. This trial primarily establishes more explicit classification, scoped instructions and better reporting; it does not demonstrate a new shared/live retention capability absent from the old baseline.
- The inherited description triggers archive before a status moves to done, while the workflow targets completed features. Conservative retention is available through Unknown, but the fixture prompts already establish completion and do not exercise this boundary.
- The inherited seven-day architecture check needs Git history. These intentionally uncommitted disposable repositories cannot provide it. Updated runs record the git log exit 128 and disclose the resulting gap; this is an expected evidence limitation.

## New evaluation and instruction limitations

- The three fixtures do not discriminate target-collision handling, unknown completion/reference evidence, unrelated completed-feature scope, multiple completed owners of a moved artifact, or existing archive metadata keys. Newly documented protections for these conditions remain untested.
- Case 8's internal ../architecture.md stays correct automatically because plans and archive have equal depth. It verifies link validity, not a required internal-link rewrite. Inbound history repair is meaningfully exercised.
- Case 7's timestamp assertion has a conditional antecedent (nothing moves). A no-skill relocation with no timestamp still passes its timestamp/status/link assertion. The separate retention assertion catches the wrong move; score summaries must retain that distinction.
- The report example in the final skill names only one retained-feature owner. The operative instruction now explicitly requires every referring feature ID; iteration 2 follows it. Expanding the example could reinforce the rule, but this is not a demonstrated blocker.
- Preserving existing frontmatter does not spell out collision policy for pre-existing archived_at/feature_id keys. It should not be interpreted as permission for duplicate keys; the current fixture only has owner metadata and cannot settle that edge case.
- Execution evidence consists of agent-created local operation scripts and saved outputs, not a separately instrumented native-host benchmark. All comparative conclusions are limited to these three fixtures and two runs; no long-task, cross-session, statistical, cost or latency improvement is established.
