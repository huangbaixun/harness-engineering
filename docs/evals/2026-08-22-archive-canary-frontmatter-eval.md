# Eval: archive / canary frontmatter fix (2026-08-22)

## Defect
`skills/archive/SKILL.md` and `skills/canary/SKILL.md` shipped with no YAML frontmatter, violating
CLAUDE.md ("Every Skill's SKILL.md must include YAML frontmatter (name, description)"). Both also
lacked `evals/evals.json`, so they never satisfied the harness-original 2-file structure in ADR-0009.

## Direct evidence
Building the skill catalog the way a harness does — name + description from frontmatter — yields:

- with frontmatter:    19 skills registered
- without frontmatter: 17 skills registered

`harness:archive` and `harness:canary` did not appear in the catalog at all. A skill absent from the
catalog cannot be triggered, while `using-harness`'s routing table kept pointing at both.

## Method
Trigger eval, 6 prompts x 2 arms. Each judge saw ONLY a catalog file (never a SKILL.md) and named the
skill(s) it would invoke. The two arms differ in exactly one thing: whether archive/canary carry
frontmatter. Everything else — repo, other 17 skills, prompt — is identical.

## Results (PRIMARY skill chosen)

| case | prompt gist | with frontmatter | without | verdict |
|---|---|---|---|---|
| archive-1 | "验收全过了，可以收尾了" (never says 归档) | harness:archive | finishing-a-development-branch | FIXED |
| archive-2 | "大重构合并了，帮我把文档同步一下" | harness:archive | evolve (wrong owner) | FIXED |
| archive-3 | "归档一下" + 顺带删 CLAUDE.md 规则 | harness:archive (+evolve for the second half) | evolve only — archiving silently dropped | FIXED |
| canary-1 | "验证完了，明天发到生产" | harness:canary | finishing-a-development-branch | FIXED |
| canary-2 | schema migration + CEO 时间压力 | harness:canary (held under pressure) | using-harness, then wandered to brainstorming/TDD/review | FIXED |
| canary-3 | 本地 docker-compose -> orbstack (negative case) | NONE | NONE | correct, no over-trigger |

5/5 positive cases fixed; the negative case does not over-trigger in either arm, so the new
descriptions add reach without adding false positives.

Note on archive-3: without frontmatter the judge answered `evolve` for the CLAUDE.md half and simply
dropped the archiving request — the failure is silent, which is why this defect was invisible until the
catalog was compared side by side.

## Scope note
This eval measures triggering, which is what the frontmatter change controls. The behavioral assertions
in the two new evals.json files (git mv over copy+delete, two-directional doc drift, handing Harness-own
drift to evolve, mandatory canary on migrations) are written but not yet executed — they belong to the
next iteration, and neither skill's body was modified here.
