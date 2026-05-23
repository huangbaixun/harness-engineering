#!/usr/bin/env bash
# PreToolUse Hook — 拦截危险改动
# 演示重点：当 AI 试图改 server.js 的存储层、tokens.css 变量、或 package.json 加新依赖时阻止

set -euo pipefail

INPUT="${CLAUDE_TOOL_INPUT:-}"

# 1. 拦截存储层改动
if echo "$INPUT" | grep -qE 'localStorage|sessionStorage|sqlite|redis|mongodb|postgres|mysql' ; then
  echo "PRE-PROTECT: 检测到试图引入持久化存储 — CLAUDE.md 明确禁止改动存储层。" >&2
  echo "如需要持久化请先开 ADR 走架构评审。" >&2
  exit 2
fi

# 2. 拦截全局 CSS 变量改名
if echo "$INPUT" | grep -qE 'tokens\.css|style\.css' ; then
  if echo "$INPUT" | grep -qE '^\s*(\+|\-).*--[a-z-]+\s*:' ; then
    echo "PRE-PROTECT: 检测到 :root 变量改动 — 请确认这不是组件级样式调整。" >&2
    exit 2
  fi
fi

# 3. 拦截 package.json 新依赖
if echo "$INPUT" | grep -qE 'package\.json' ; then
  if echo "$INPUT" | grep -qE '"(dependencies|devDependencies)"' ; then
    echo "PRE-PROTECT: 检测到 dependencies 改动 — CLAUDE.md 禁止引入新依赖。" >&2
    exit 2
  fi
fi

exit 0
