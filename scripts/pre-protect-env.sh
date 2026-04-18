#!/bin/bash
# PreToolUse Hook — Sensitive file & dangerous command protection
# Matches: Bash, Edit, Write
# Principle: block access to secrets and destructive operations
# Exit 2 = block with feedback to Agent; Exit 0 = allow

TOOL_INPUT=$(cat)
TOOL_NAME=$(echo "$TOOL_INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# ── 1. Sensitive file protection ──────────────────────────────────────────
if [[ -n "$FILE_PATH" ]]; then
  BASENAME=$(basename "$FILE_PATH" 2>/dev/null)
  LOWER_PATH=$(echo "$FILE_PATH" | tr '[:upper:]' '[:lower:]')

  # Secret / credential files
  case "$LOWER_PATH" in
    *.env|*.env.*|*/.env)
      echo "BLOCKED: cannot access .env file — $FILE_PATH" >&2; exit 2 ;;
    *.pem|*.key|*.p12|*.pfx|*.jks|*.keystore)
      echo "BLOCKED: cannot access key/certificate file — $FILE_PATH" >&2; exit 2 ;;
    *id_rsa*|*id_ed25519*|*id_ecdsa*|*id_dsa*)
      echo "BLOCKED: cannot access SSH private key — $FILE_PATH" >&2; exit 2 ;;
  esac

  # Pattern-based detection
  case "$BASENAME" in
    .netrc|.npmrc|.pypirc|.docker/config.json|credentials|credentials.json|secrets.json|secrets.yaml|secrets.yml)
      echo "BLOCKED: cannot access credentials file — $FILE_PATH" >&2; exit 2 ;;
    service-account*.json|*-credentials.json|*_credentials.json)
      echo "BLOCKED: cannot access service account credentials — $FILE_PATH" >&2; exit 2 ;;
    .htpasswd|shadow|passwd)
      echo "BLOCKED: cannot access system auth file — $FILE_PATH" >&2; exit 2 ;;
  esac

  # Directory-based protection
  case "$LOWER_PATH" in
    */.ssh/*|*/.gnupg/*|*/.aws/credentials*|*/.config/gcloud/*)
      echo "BLOCKED: cannot access protected config directory — $FILE_PATH" >&2; exit 2 ;;
  esac
fi

# ── 2. Dangerous command protection ──────────────────────────────────────
if [[ -n "$COMMAND" ]]; then
  # Destructive filesystem operations
  if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?/[^.]|rm\s+-rf\s+\*'; then
    echo "BLOCKED: destructive rm on root or wildcard detected" >&2; exit 2
  fi

  # Database destruction
  if echo "$COMMAND" | grep -qiE 'DROP\s+(DATABASE|TABLE|SCHEMA)|TRUNCATE\s+TABLE|DELETE\s+FROM\s+\S+\s*;?\s*$'; then
    echo "BLOCKED: destructive database operation detected" >&2; exit 2
  fi

  # Force push prevention
  if echo "$COMMAND" | grep -qE 'git\s+push\s+.*--force|git\s+push\s+-f\b'; then
    echo "BLOCKED: git force push detected — use --force-with-lease instead" >&2; exit 2
  fi

  # Hard reset prevention
  if echo "$COMMAND" | grep -qE 'git\s+reset\s+--hard'; then
    echo "BLOCKED: git reset --hard detected — this discards uncommitted work" >&2; exit 2
  fi

  # Branch deletion of main/master
  if echo "$COMMAND" | grep -qE 'git\s+branch\s+-[dD]\s+(main|master)\b'; then
    echo "BLOCKED: cannot delete main/master branch" >&2; exit 2
  fi

  # Chmod 777 (overly permissive)
  if echo "$COMMAND" | grep -qE 'chmod\s+777'; then
    echo "BLOCKED: chmod 777 is too permissive — use specific permissions" >&2; exit 2
  fi

  # Curl piped to shell (unsafe install pattern)
  if echo "$COMMAND" | grep -qE 'curl\s.*\|\s*(ba)?sh|wget\s.*\|\s*(ba)?sh'; then
    echo "BLOCKED: piping download to shell is unsafe — download first, inspect, then run" >&2; exit 2
  fi

  # Secret in command arguments
  if echo "$COMMAND" | grep -qiE '(api[_-]?key|api[_-]?secret|password|token|secret[_-]?key)\s*=\s*['\''"][^'\''"]+['\''"]'; then
    echo "BLOCKED: possible secret in command arguments — use environment variables instead" >&2; exit 2
  fi
fi

# All checks passed — silent success
exit 0
