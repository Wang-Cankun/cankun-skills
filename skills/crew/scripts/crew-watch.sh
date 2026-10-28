#!/bin/bash
# Usage: crew-watch.sh <run-dir> [--roles <ledger-roles-file>] [--files <regex>] <role-name>...
# Run in the background from the coordinator. Exits, with a Herdr notification, when a file in
# the run directory whose name matches --files (default: handoff-*.md and review-*.md) is new or
# rewritten and no named role is working or unknown, a role is blocked, or every role has sat idle
# for 30 minutes (a role waiting on its own background job looks idle too, so a short idle limit
# wakes the coordinator for nothing). Exits quietly once the run directory is gone.
# The file event waits on every named role: to hear from one agent while others keep working,
# run one watcher per agent.
# With --roles, burn notifications leave this watcher and all agents running.
# CREW_BURN_WINDOW_SECONDS (600) and CREW_BURN_THRESHOLD (1000000) override estimates.
dir=$1; shift
roles=
pattern='^(handoff|review)-.*\.md$'
while :; do
  case "${1:-}" in
    --roles|--files) ;;
    *) break;;
  esac
  [ $# -ge 2 ] || { echo "$1 needs a value" >&2; exit 2; }
  if [ "$1" = --roles ]; then roles=$2; else pattern=$2; fi
  shift 2
done
scripts=$(cd "$(dirname "$0")" && pwd)
window=${CREW_BURN_WINDOW_SECONDS:-600}
threshold=${CREW_BURN_THRESHOLD:-1000000}
if ! [[ "$window" =~ ^[1-9][0-9]*$ ]]; then echo "Burn window must be positive seconds" >&2; exit 2; fi
# files() hides Python errors, so a bad pattern would silence file events for the whole run.
if ! python3 -c 'import re, sys; re.compile(sys.argv[1])' "$pattern" 2>/dev/null; then
  echo "--files is not a valid regular expression" >&2; exit 2
fi
files() {
  python3 - "$dir" "$pattern" 2>/dev/null <<'PY' | sort
import os, re, sys
run, pattern = sys.argv[1], re.compile(sys.argv[2])
for name in os.listdir(run):
    path = os.path.join(run, name)
    try:
        if pattern.search(name) and os.path.isfile(path):
            print(f"{name}\t{os.stat(path).st_mtime_ns}")
    except FileNotFoundError:
        pass
PY
}
before=$(files)
idle=0
last_burn=0
status() {
  herdr agent list | python3 -c '
import sys, json
names = set(sys.argv[1:])
for a in json.load(sys.stdin)["result"]["agents"]:
    if a.get("name") in names: print(a["name"] + "=" + a["agent_status"])' "$@"
}
notify() { herdr notification show "$1" --body "$2" --sound "$3" >/dev/null 2>&1; echo "$1: $2"; }
note() { notify "$@"; exit 0; }
while [ -d "$dir" ]; do
  sleep 30
  [ -d "$dir" ] || exit 0
  st=$(status "$@" | tr '\n' ' ')
  case "$st" in *blocked*) note "Crew blocked" "$st" request;; esac
  now=$(files)
  if [ "$now" != "$before" ] && ! echo "$st" | grep -qE '=(working|unknown)'; then
    new=$(comm -13 <(echo "$before") <(echo "$now") | cut -f1 | tr '\n' ' ')
    [ -d "$dir" ] || exit 0
    [ -n "$new" ] && note "Crew file" "$new" done
    before=$now
  fi
  if echo "$st" | grep -qE '=(working|unknown)'; then idle=0; else idle=$((idle + 1)); fi
  [ $idle -ge 60 ] && note "Crew idle" "$st" request
  tick=$(date +%s)
  if [ -n "$roles" ] && [ $((tick - last_burn)) -ge "$window" ]; then
    burn=$(python3 "$scripts/crew-burn.py" --run-dir "$dir" --roles "$roles" --files="$pattern" \
      --window-seconds "$window" --threshold "$threshold")
    [ -d "$dir" ] || exit 0
    if [ -n "$burn" ]; then
      notify "Crew burn" "$burn" request
      last_burn=$tick
    fi
  fi
done
