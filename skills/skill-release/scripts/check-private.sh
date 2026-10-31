#!/bin/bash
# Fail when a tracked file in this repository carries a machine-local path or a private token.
# Private tokens come from a list kept outside the repository, one fixed string per line
# (# starts a comment), so the list itself is never published:
#   ${SKILL_RELEASE_PRIVATE_TOKENS:-~/.config/skill-release/private-tokens.txt}
# Without the list, only the machine-local path check runs.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
list=${SKILL_RELEASE_PRIVATE_TOKENS:-$HOME/.config/skill-release/private-tokens.txt}
patterns=$(mktemp)
trap 'rm -f "$patterns"' EXIT
printf '%s\n' /Users/ /home/ > "$patterns"
if [ -f "$list" ]; then
  grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$list" >> "$patterns" || true
else
  echo "no private token list at $list; checking machine-local paths only" >&2
fi
# This script holds the path patterns itself.
if git grep -n -I -i -F -f "$patterns" -- . ':!*.lock' ':!skills/skill-release/scripts/check-private.sh'; then
  echo "private or machine-local text above; remove it before publishing" >&2
  exit 1
fi
echo "no private or machine-local text in tracked files"
