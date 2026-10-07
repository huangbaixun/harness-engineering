# F006 implementation and verification plan

Upstream: docs/specs/2026-10-06-F006-archive-design.md

## Global constraints

references → templates → skills → commands; hooks silent on success;
{{PLACEHOLDER}} template syntax. Preserve user work and authority; no external effects.

## Tasks and acceptance mapping

1. Define shared/living spec vs completed plan classification in archive SKILL.md.
   Covers F006 acceptance criteria 1 and 2.
2. Require inbound-reference inspection, repair and post-move checks in the report.
   Covers criterion 3. Preserve frontmatter and avoid target overwrite.
3. Add evals 6–8 and run isolated updated/old/no-skill cases; inspect file states,
   grade assertions and generate the skill-creator viewer. Covers criterion 4.
4. Run python3 scripts/validate.py and git diff --check; inspect results and record
   the acceptance evidence, remaining unknowns and neutral handoff.

## Interfaces and completion

Inputs: root features.json, candidate specs/plans, inbound repository references.
Outputs: eligible docs/archive/ artifacts, repaired local links, report and checkpoint.
Archive does not change feature done status, commit or synchronize Issues.
Keep spec/plan available until verification and local completion are recorded.
