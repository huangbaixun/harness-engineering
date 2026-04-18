---
description: Detect codebase entropy — find dead code, duplicate implementations, and excessive coupling, then generate a health report
---

# /harness:scan-entropy — Code Entropy Detection

**Run frequency**: Once a month, or manually triggered after a large-scale refactor.

Use an explore-agent subagent to execute the following detections, keeping the main thread clean:

## Detection Steps

### Step 1: Dead Code Detection

Choose the appropriate tool based on the tech stack:

**TypeScript/JavaScript**:
```bash
# Detect uncalled exports
npx ts-prune --error 2>/dev/null | grep -v "used in module" | head -30

# Or use knip (a more modern alternative)
npx knip --reporter compact 2>/dev/null | head -30
```

**Python**:
```bash
# Detect unused imports and variables
python -m vulture . --min-confidence 80 2>/dev/null | head -30
```

**Go**:
```bash
# Detect unused functions
deadcode ./... 2>/dev/null | head -30
```

**Generic** (fallback):
```bash
# Find files not touched in git log for the past 90 days (candidate dead code areas)
git log --since="90 days ago" --name-only --format="" | sort -u > /tmp/active_files.txt
find src -name "*.ts" -o -name "*.py" -o -name "*.go" 2>/dev/null | sort > /tmp/all_files.txt
comm -23 /tmp/all_files.txt /tmp/active_files.txt | head -20
```

### Step 2: Duplicate Code Detection

```bash
# JavaScript/TypeScript
npx jscpd src --threshold 10 --reporters console 2>/dev/null | tail -30

# Python
pip install pylint --quiet && pylint --disable=all --enable=duplicate-code src/ 2>/dev/null | head -20

# Generic: find similar function names (same logic may have multiple implementations)
grep -rn "^function \|^def \|^func " src/ 2>/dev/null | \
  awk -F'[( ]' '{print $NF}' | sort | uniq -d | head -20
```

### Step 3: Excessive Coupling Detection

```bash
# Find files referenced by more than 3 different modules (potential "god files")
for f in $(find src -name "*.ts" -o -name "*.py" 2>/dev/null | head -50); do
  count=$(grep -rl "$(basename $f .ts)" src/ 2>/dev/null | wc -l)
  if [ "$count" -gt 3 ]; then
    echo "$count refs: $f"
  fi
done | sort -rn | head -10
```

### Step 4: Test Quality Assessment

```bash
# Find tests that test implementation details (excessive mocking is a signal)
grep -rn "jest.mock\|unittest.mock\|gomock" tests/ 2>/dev/null | wc -l
grep -rn "spy\|stub\|mock" tests/ 2>/dev/null | wc -l

# Find test files without assert/expect (empty tests)
for f in $(find tests -name "*.test.*" -o -name "*_test.*" 2>/dev/null); do
  if ! grep -q "expect\|assert\|should" "$f" 2>/dev/null; then
    echo "Empty test: $f"
  fi
done
```

## Assessment and Output

Based on the detection results above:

1. **Assess severity**:
   - 🔴 Critical: dead code > 20 files, duplicate code blocks > 10, "god file" referenced > 10 times
   - 🟡 Warning: dead code 5-20 files, duplicate code 3-10 blocks
   - 🟢 Healthy: below the above thresholds

2. **Generate a health report**, update `docs/quality.md`:
```markdown
## Code Health Report — [YYYY-MM-DD]

### Entropy Metrics
| Type | Count | Trend | Severity |
|------|-------|-------|----------|
| Dead code files | N | ↑/→/↓ | 🔴/🟡/🟢 |
| Duplicate code blocks | N | ... | ... |
| Over-coupled files | N | ... | ... |

### Top 3 Most Severe Issues
1. [Specific file/module, impact description]
2. ...

### Recommended Actions
- Immediate: [Handle within current Sprint]
- Planned: [Schedule for next Sprint]
- Track: [Record as tech debt, defer for now]
```

3. **Create a GitHub Issue for each of the top 3 issues** (if gh CLI is available):
```bash
gh issue create --title "tech-debt: [specific issue]" \
  --body "Found by entropy-scan, impact: ..." \
  --label "tech-debt,entropy-scan"
```

## Important Notes

- This is an **observation** task — do not directly fix discovered issues in the same session
- Split fixes into separate PRs, each PR addressing only one type of entropy
- Maintain critical thinking about tool-reported false positives — not every "unused" item is truly dead code
