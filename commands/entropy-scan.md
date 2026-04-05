---
description: 检测代码库熵增，发现死代码、重复实现、过度耦合，生成健康度报告
---

# /entropy-scan — 代码熵增检测

**运行频率**：每月一次，或在大规模重构后手动触发。

用 explore-agent subagent 执行以下检测，保持主线程干净：

## 检测步骤

### Step 1：死代码检测

根据技术栈选择合适的工具：

**TypeScript/JavaScript**：
```bash
# 检测未被调用的导出
npx ts-prune --error 2>/dev/null | grep -v "used in module" | head -30

# 或使用 knip（更现代的替代方案）
npx knip --reporter compact 2>/dev/null | head -30
```

**Python**：
```bash
# 检测未使用的导入和变量
python -m vulture . --min-confidence 80 2>/dev/null | head -30
```

**Go**:
```bash
# 检测未使用的函数
deadcode ./... 2>/dev/null | head -30
```

**通用**（回退方案）：
```bash
# 找出最近 90 天没有被 git log 触碰到的文件（候选死代码区域）
git log --since="90 days ago" --name-only --format="" | sort -u > /tmp/active_files.txt
find src -name "*.ts" -o -name "*.py" -o -name "*.go" 2>/dev/null | sort > /tmp/all_files.txt
comm -23 /tmp/all_files.txt /tmp/active_files.txt | head -20
```

### Step 2：重复代码检测

```bash
# JavaScript/TypeScript
npx jscpd src --threshold 10 --reporters console 2>/dev/null | tail -30

# Python
pip install pylint --quiet && pylint --disable=all --enable=duplicate-code src/ 2>/dev/null | head -20

# 通用：找相似函数名（同一逻辑可能有多个实现）
grep -rn "^function \|^def \|^func " src/ 2>/dev/null | \
  awk -F'[( ]' '{print $NF}' | sort | uniq -d | head -20
```

### Step 3：过度耦合检测

```bash
# 找被超过 3 个不同模块引用的文件（潜在的「上帝文件」）
for f in $(find src -name "*.ts" -o -name "*.py" 2>/dev/null | head -50); do
  count=$(grep -rl "$(basename $f .ts)" src/ 2>/dev/null | wc -l)
  if [ "$count" -gt 3 ]; then
    echo "$count refs: $f"
  fi
done | sort -rn | head -10
```

### Step 4：测试质量评估

```bash
# 找重测试实现细节的测试（过度 mock 是信号）
grep -rn "jest.mock\|unittest.mock\|gomock" tests/ 2>/dev/null | wc -l
grep -rn "spy\|stub\|mock" tests/ 2>/dev/null | wc -l

# 找没有 assert/expect 的测试文件（空测试）
for f in $(find tests -name "*.test.*" -o -name "*_test.*" 2>/dev/null); do
  if ! grep -q "expect\|assert\|should" "$f" 2>/dev/null; then
    echo "空测试：$f"
  fi
done
```

## 评估与产出

根据上述检测结果：

1. **评估严重程度**：
   - 🔴 严重：死代码 > 20 个文件，重复代码块 > 10 处，「上帝文件」被引用 > 10 次
   - 🟡 警告：死代码 5-20 个，重复代码 3-10 处
   - 🟢 健康：低于以上阈值

2. **生成健康度报告**，更新 `docs/quality.md`：
```markdown
## 代码健康度报告 — [YYYY-MM-DD]

### 熵增指标
| 类型 | 数量 | 趋势 | 严重程度 |
|------|------|------|---------|
| 死代码文件 | N | ↑/→/↓ | 🔴/🟡/🟢 |
| 重复代码块 | N | ... | ... |
| 过耦合文件 | N | ... | ... |

### 最严重的 3 个问题
1. [具体文件/模块，影响描述]
2. ...

### 建议行动
- 立即：[当前 Sprint 内处理]
- 计划：[下个 Sprint 排期]
- 跟踪：[记录为 Tech Debt，暂不处理]
```

3. **为最严重的 3 个问题各创建 GitHub Issue**（如有 gh CLI）：
```bash
gh issue create --title "tech-debt: [具体问题]" \
  --body "entropy-scan 发现，影响：..." \
  --label "tech-debt,entropy-scan"
```

## 注意事项

- 这是**观测**任务，不要在同一会话内直接修复发现的问题
- 把修复拆分为独立的 PR，每个 PR 只处理一类熵增
- 对工具报告的误报保持批判性思考——不是所有「未使用」都是真的死代码
