#!/bin/bash
# Template: Stop Hook — 质量门禁
# 使用方式：复制到目标项目 .claude/hooks/ 并根据技术栈调整
# 原则：成功静默，失败反馈给 Agent（exit 2）

cd "$CLAUDE_PROJECT_DIR" || exit 0

# === 根据技术栈取消注释对应的检查 ===

# --- TypeScript ---
# biome check --write . > /dev/null 2>&1 || true
# TYPECHECK=$(npx tsc --noEmit 2>&1)
# if [ $? -ne 0 ]; then
#   echo "TypeScript 类型检查失败，请修复以下错误：" >&2
#   echo "$TYPECHECK" | head -50 >&2
#   exit 2
# fi

# --- Python ---
# TYPECHECK=$(python -m mypy src/ 2>&1)
# if [ $? -ne 0 ]; then
#   echo "mypy 类型检查失败：" >&2
#   echo "$TYPECHECK" | head -50 >&2
#   exit 2
# fi

# --- Go ---
# TYPECHECK=$(go vet ./... 2>&1)
# if [ $? -ne 0 ]; then
#   echo "go vet 检查失败：" >&2
#   echo "$TYPECHECK" | head -50 >&2
#   exit 2
# fi

# --- 通用：运行测试 ---
# TEST_OUTPUT=$({{TEST_COMMAND}} 2>&1)
# if [ $? -ne 0 ]; then
#   echo "测试失败：" >&2
#   echo "$TEST_OUTPUT" | head -50 >&2
#   exit 2
# fi

exit 0
