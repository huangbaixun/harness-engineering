#!/usr/bin/env bash
# scripts/sync-superpowers.sh
# Periodic reconciliation helper for vendored superpowers skills.
# Reads each skill's UPSTREAM.md, compares its recorded commit SHA against
# the currently installed superpowers cache, and emits a diff summary.
# Does NOT auto-apply changes. See docs/specs/2026-05-23-superpowers-integration-design.md §11.

set -euo pipefail

CACHE_BASE="${CACHE_BASE:-$HOME/.claude/plugins/cache/claude-plugins-official/superpowers}"
SKILLS_DIR="${SKILLS_DIR:-skills}"

# Locate latest installed superpowers version
if [[ ! -d "$CACHE_BASE" ]]; then
  echo "[sync-superpowers] superpowers cache not found at $CACHE_BASE" >&2
  exit 1
fi

LATEST_VERSION="$(ls -1 "$CACHE_BASE" | sort -V | tail -1)"
LATEST_PATH="$CACHE_BASE/$LATEST_VERSION/skills"

if [[ ! -d "$LATEST_PATH" ]]; then
  echo "[sync-superpowers] no skills found at $LATEST_PATH" >&2
  exit 1
fi

echo "Comparing vendored skills against superpowers $LATEST_VERSION"
echo "==============================================================="

found_any=0
for upstream_path in "$LATEST_PATH"/*/; do
  upstream_name="$(basename "$upstream_path")"
  vendored_path="$SKILLS_DIR/$upstream_name"

  if [[ ! -d "$vendored_path" ]]; then
    # Skip skills we deliberately do not vendor (e.g., using-superpowers)
    continue
  fi
  found_any=1

  upstream_skill_md="$upstream_path/SKILL.md"
  vendored_skill_md="$vendored_path/SKILL.md"

  if [[ ! -f "$upstream_skill_md" || ! -f "$vendored_skill_md" ]]; then
    echo "[$upstream_name] missing SKILL.md (upstream or vendored)"
    continue
  fi

  # Compare upstream SKILL.md to vendored SKILL.md (ignoring the two allowed edits)
  # The allowed edits: (1) name: line in frontmatter, (2) "harness local rules" pointer line
  # diff exits 1 when files differ (normal case) — absorb with || true so set -e doesn't kill us
  diff_lines="$( (diff <(grep -v -E '^name:|harness local rules' "$upstream_skill_md") \
                       <(grep -v -E '^name:|harness local rules' "$vendored_skill_md") \
               || true) | wc -l | tr -d ' ')"

  upstream_md="$vendored_path/UPSTREAM.md"
  if [[ -f "$upstream_md" ]]; then
    # grep exits 1 when no match (transitional state) — absorb with || true, default below
    last_synced="$(grep -E '^- \*\*Last synced:\*\*' "$upstream_md" | sed 's/^- \*\*Last synced:\*\* //' || true)"
    if [[ -z "$last_synced" ]]; then
      last_synced="(not recorded)"
    fi
  else
    last_synced="(UPSTREAM.md missing)"
  fi

  echo "[$upstream_name] diff-lines=$diff_lines  last-synced=$last_synced"

  # Companion files: vendored byte-for-byte with ZERO allowed edits (ADR-0009, amended 2026-08-22).
  # Report three states: changed upstream, present upstream but missing here, present here but gone upstream.
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    if [[ ! -f "$vendored_path/$rel" ]]; then
      echo "  companion MISSING locally: $rel"
    elif ! cmp -s "$upstream_path/$rel" "$vendored_path/$rel"; then
      echo "  companion CHANGED upstream: $rel"
    fi
  done < <(cd "$upstream_path" && find . -type f ! -name SKILL.md | sed 's|^\./||' | sort)

  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    case "$rel" in
      SKILL.md|harness-delta.md|UPSTREAM.md|evals/*) continue ;;
    esac
    if [[ ! -f "$upstream_path/$rel" ]]; then
      echo "  companion GONE upstream (ours is orphaned): $rel"
    fi
  done < <(cd "$vendored_path" && find . -type f | sed 's|^\./||' | sort)
done

if [[ $found_any -eq 0 ]]; then
  echo "(no vendored skills found)"
fi

echo "==============================================================="
echo "Done. Review per-skill diffs manually before applying changes."
echo "SKILL.md must differ from upstream by exactly the 2 allowed edits; companions must be byte-identical."
