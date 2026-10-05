#!/usr/bin/env bash
# Read-only upstream comparison. Explicit CACHE_BASE / --source take precedence.
set -euo pipefail
exec python3 "$(dirname "$0")/sync_superpowers.py" "$@"
