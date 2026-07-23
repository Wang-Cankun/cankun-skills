#!/usr/bin/env bash
# confer.sh — compat shim; all mechanics live in confer.mjs. Kept one round so
# agents holding the old SKILL.md and existing permission allowlists keep working.
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/confer.mjs" "$@"
