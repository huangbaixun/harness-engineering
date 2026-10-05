#!/bin/bash
set -euo pipefail
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
# Legacy callers without stdin get a locally constructed event. Native hooks use stdin.
exec python3 "$ROOT/scripts/claude_hook.py" session-start "$@"
