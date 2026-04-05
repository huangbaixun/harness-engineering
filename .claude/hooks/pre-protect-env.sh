#!/bin/bash
# Template: PreToolUse Hook — 敏感文件保护
# 匹配工具：Bash, Edit, Write
# 原则：拦截对敏感文件的访问

TOOL_INPUT=$(cat)
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.tool_input.path // empty' 2>/dev/null)
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# 检查文件路径
if [[ -n "$FILE_PATH" ]]; then
  if [[ "$FILE_PATH" == *".env"* ]] || \
     [[ "$FILE_PATH" == *"secret"* ]] || \
     [[ "$FILE_PATH" == *"credential"* ]] || \
     [[ "$FILE_PATH" == *".pem"* ]] || \
     [[ "$FILE_PATH" == *"private_key"* ]]; then
    echo "拒绝：禁止访问敏感文件 $FILE_PATH" >&2
    exit 2
  fi
fi

# 检查 Bash 命令中的危险操作
if [[ -n "$COMMAND" ]]; then
  if [[ "$COMMAND" == *"rm -rf /"* ]] || \
     [[ "$COMMAND" == *"DROP DATABASE"* ]] || \
     [[ "$COMMAND" == *"DROP TABLE"* ]]; then
    echo "拒绝：检测到危险命令" >&2
    exit 2
  fi
fi

exit 0
