#!/bin/bash
# Template: PostToolUse Hook — 基础遥测日志
# 记录每次工具调用，用于成本追踪和行为分析

TOOL_NAME=$(echo "$CLAUDE_TOOL_NAME" 2>/dev/null || echo "unknown")
SESSION_ID=$(echo "$CLAUDE_SESSION_ID" 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# 追加到结构化日志文件
TELEMETRY_DIR="${CLAUDE_PROJECT_DIR:-.}/docs"
TELEMETRY_FILE="$TELEMETRY_DIR/agent-telemetry.jsonl"

if [ -d "$TELEMETRY_DIR" ]; then
  echo "{\"timestamp\":\"$TIMESTAMP\",\"session\":\"$SESSION_ID\",\"tool\":\"$TOOL_NAME\"}" >> "$TELEMETRY_FILE" 2>/dev/null
fi

# 可选：发送到 OpenTelemetry Collector
# curl -s -X POST http://localhost:4318/v1/traces \
#   -H "Content-Type: application/json" \
#   -d "{\"tool\":\"$TOOL_NAME\",\"session\":\"$SESSION_ID\"}" > /dev/null

# 遥测 Hook 永远静默成功
exit 0
