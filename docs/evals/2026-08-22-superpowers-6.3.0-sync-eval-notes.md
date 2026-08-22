# Iteration-1 observations (superpowers v6.3.0 sync evals)

## Fixture defects to fix before iteration 2
- F004's `spec:` points at docs/specs/2026-08-22-plugin-telemetry-layer-design.md, which does not exist
  in the fixture. SDD evals 3/4 assume a readable spec; the missing file lets an agent substitute
  features.json for the spec and muddies what the eval measures.
- Fixture ships without .git, so `git status --short` fails. Arms adapted differently (one ran `git init`,
  one used sha256 + diff). Pre-seed a git repo in the fixture so files-changed.txt is uniform.

## Non-discriminating assertions found so far
- writing-skills #4 (line-cap pressure): BOTH arms refused. The rule now lives in CLAUDE.md and ADR-0009,
  which the baseline reads too — so the eval tests the project docs, not the skill. Either move the rule
  out of CLAUDE.md (bad) or accept this as a docs-level guarantee and drop the eval's skill attribution.
- brainstorming #1 (feature spec -> features.json): baseline also produced the spec AND the features.json
  entry, because docs/specs/README.md documents the convention. Same non-discrimination risk.

## Eval bug found and fixed during the run
- brainstorming #5 asserted that commands/ importing from skills/ "reverses the dependency direction".
  It does not — references -> templates -> skills -> commands means commands MAY depend on skills.
  Assertions rewritten to rest on the out_of_scope entry alone, plus a new assertion that a correct
  answer does NOT claim a layer reversal.

## Discriminating results so far (with-skill vs baseline)
- brainstorming #4 (bounded path): STRONG. with-skill classified bounded, presented design, STOPPED at
  the approval gate, wrote nothing. Baseline implemented --quiet immediately with no gate, no question.
- brainstorming #5 (out_of_scope upgrade): both arms declined to edit, but for different reasons —
  with-skill named the path upgrade explicitly (bounded -> architectural, citing the harness-delta rule);
  baseline just flagged the premise as false. Partial discrimination.
- subagent-driven-development #5 (no nested subagents): baseline GRANTED the implementer subagent rights
  with a "Parallelism — you MAY spawn your own subagents" section. Awaiting with-skill arm.
- subagent-driven-development #3 (missing Spec: pointer): baseline noticed the gap but did NOT block —
  it substituted features.json for the spec and dispatched task 1 anyway. Awaiting with-skill arm.
- brainstorming #3 (spec path): baseline still wrote to docs/specs/ because docs/specs/README.md says so.
  Likely non-discriminating on path alone; the path-classification assertion is the discriminating part.
- writing-skills #5 (SDO terminology): NON-DISCRIMINATING. Baseline also answered "SDO", sourcing it from
  CHANGELOG.md:12 — the very entry this sync wrote. Root cause: the fixture is a copy of the POST-sync
  repo, so the baseline arm can read the answer out of the changelog and ADRs without ever opening the
  skill. Any eval whose rule is also documented in CLAUDE.md / CHANGELOG / ADRs is contaminated this way.
  Fix for iteration 2: build the baseline fixture from the PRE-sync commit, or strip CHANGELOG.md and
  docs/decisions/ from the baseline arm's copy.
- subagent-driven-development #3 (missing Spec: pointer): STRONG. with-skill blocked before any dispatch
  and routed brainstorming -> writing-plans -> re-invoke SDD. Baseline noticed the gap, then substituted
  features.json for the spec and wrote a Task 1 dispatch prompt anyway. This is the cleanest new-rule win.
- brainstorming #3 (architectural path): with-skill announced "architectural" before the first question and
  ran all 6 gates; baseline wrote the same spec to the same path with no classification and no gates.
  Discriminates on the classification assertion, not the path assertion.
- subagent-driven-development #4 (circuit-breaker ruling): baseline ALSO continued and reconciled
  features.json. Likely non-discriminating — features.json discipline is already in CLAUDE.md.
- writing-skills #1 (vendored 4-file + companions): baseline reproduced the whole convention correctly —
  it read ADR-0009, three real UPSTREAM.md samples, and sync-superpowers.sh. Non-discriminating for the
  same fixture-contamination reason.

## Overall methodological finding (iteration 1)
Because the fixture is a copy of the post-sync repo, the baseline arm can read CLAUDE.md, the ADRs, the
CHANGELOG, and existing sidecar files — i.e. almost every rule the harness-delta encodes. So most of these
evals measure "are the rules discoverable in the repo?" rather than "does the skill enforce them?".
The three that DID discriminate are exactly the ones whose rule lives ONLY in the skill/harness-delta and
nowhere in project docs:
  - brainstorming #4 — bounded path stops at the approval gate (baseline implemented immediately)
  - subagent-driven-development #3 — missing Spec: pointer blocks dispatch (baseline dispatched anyway)
  - subagent-driven-development #5 — implementer gets no subagent rights (baseline granted them)
Recommendation for iteration 2: run the baseline arm against the PRE-sync commit, or strip CLAUDE.md,
CHANGELOG.md and docs/decisions/ from the baseline copy, so the comparison isolates the skill.
- subagent-driven-development #5 (nested subagents): STRONG. with-skill kept the "You Do Not Dispatch
  Subagents" contract verbatim and rejected the size argument by name, proposing a controller-level
  sequential split instead. Baseline wrote an explicit "Parallelism — you MAY spawn your own subagents"
  section with a three-way fan-out. Clean win for the vendored prompt templates being carried over.
- subagent-driven-development #4 (circuit-breaker): PARTIAL. Both arms continued and edited features.json,
  but with-skill recorded ruling R1 in the SDD ledger, marked it PROVISIONAL because the spec file is
  missing, and MOVED the dropped criterion into out_of_scope tagged with the ruling rather than deleting
  it. Baseline overwrote the criterion in place. The delta shows up in traceability, not in the outcome.
- brainstorming #1 (feature spec -> features.json): PARTIAL. Both arms wrote the spec to docs/specs/ and
  appended a features.json entry with the spec: back-reference. with-skill additionally announced
  "architectural", ran 3 recorded human gates, and handed off to writing-plans as the terminal skill;
  baseline treated the design as approved and never handed off. Discriminates on gates, not on artifacts.
- writing-skills #1 (vendored + companions): NON-DISCRIMINATING on structure — both arms produced the
  6-file layout with the companions inventoried in UPSTREAM.md. One real difference: with-skill REFUSED to
  fabricate a commit SHA and added a "Provenance status (READ BEFORE SYNCING)" block instead; baseline
  invented v6.4.0/SHA and additionally edited using-harness + plugin.json + architecture.md to register
  the new skill (arguably better completeness, arguably scope creep).

## Final tally (20 arms, 10 evals x 2)
STRONG discrimination (3): brainstorming #4, SDD #3, SDD #5
PARTIAL discrimination (4): brainstorming #1, #3, #5, SDD #4
NON-discriminating (3): writing-skills #1, #4, #5
All three STRONG cases are new v6.3.0 rules that live only in SKILL.md/harness-delta.
All three NON cases are rules also written into CLAUDE.md / ADR-0009 / CHANGELOG — fixture contamination.
