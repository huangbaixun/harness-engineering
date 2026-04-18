---
description: Evaluate which rules in CLAUDE.md are no longer necessary and trim it to within 60 lines
---

Evaluate each rule in CLAUDE.md one by one:

Question 1: Does Claude naturally follow this rule even without it being stated?
  → Try executing the related task without this rule and observe the behavior

Question 2: Has this rule been superseded by a Hook or Linter?
  → If the same constraint already has a deterministic checking mechanism, the text version is just redundant tokens

Question 3: Does this rule correspond to a real failure mode that still exists?
  → Check recent Agent usage records — has this rule been triggered?

List the rules that can be removed, noting the reason for each removal.
Wait for user confirmation before executing the deletions.
Goal: Keep CLAUDE.md within 60 lines.
