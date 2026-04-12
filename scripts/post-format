#!/bin/bash
# Template: PostToolUse Hook — 自动格式化
# 匹配工具：Edit, Write
# 关键原则：成功完全静默，只有失败才产生输出
# 4000 行通过日志会使 Agent 失去任务焦点

cd "$CLAUDE_PROJECT_DIR" || exit 0

# === 根据技术栈取消注释对应的格式化 ===

# --- TypeScript (Biome) ---
# FORMAT_OUTPUT=$(npx biome check --write . 2>&1)

# --- TypeScript (ESLint + Prettier) ---
# FORMAT_OUTPUT=$(npx eslint --fix . 2>&1 && npx prettier --write . 2>&1)

# --- Python (Black + isort) ---
# FORMAT_OUTPUT=$(python -m black . 2>&1 && python -m isort . 2>&1)

# --- Python (Ruff) ---
# FORMAT_OUTPUT=$(python -m ruff format . 2>&1 && python -m ruff check --fix . 2>&1)

# --- Go ---
# FORMAT_OUTPUT=$(gofmt -w . 2>&1 && goimports -w . 2>&1)

# 通用错误处理
# if [ $? -ne 0 ]; then
#   echo "格式化失败：" >&2
#   echo "$FORMAT_OUTPUT" | head -30 >&2
# fi
# 成功 = 完全静默
exit 0
