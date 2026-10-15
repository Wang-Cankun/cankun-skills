#!/bin/bash
# Usage: crew-watch.sh <run-dir> <role-name>...
# Run in the background from the coordinator. Exits, with a Herdr notification, when a new
# handoff-*.md or review-*.md lands in the run directory (other files, such as a reviewer's
# scratch output, are ignored), a role is blocked, or every role has sat idle for 30 minutes (a role
# waiting on its own background job looks idle too, so a short idle limit wakes the coordinator
# for nothing). Exits quietly once the run directory is gone.
dir=$1; shift
files() { ls "$dir" | grep -E '^(handoff|review)-.*\.md$' | sort; }
before=$(files)
idle=0
status() {
  herdr agent list | python3 -c '
import sys, json
names = set(sys.argv[1:])
for a in json.load(sys.stdin)["result"]["agents"]:
    if a.get("name") in names: print(a["name"] + "=" + a["agent_status"])' "$@"
}
note() { herdr notification show "$1" --body "$2" --sound "$3" >/dev/null 2>&1; echo "$1: $2"; exit 0; }
while [ -d "$dir" ]; do
  sleep 30
  [ -d "$dir" ] || exit 0
  now=$(files)
  if [ "$now" != "$before" ]; then note "Crew file" "$(comm -13 <(echo "$before") <(echo "$now") | tr '\n' ' ')" done; fi
  st=$(status "$@" | tr '\n' ' ')
  case "$st" in *blocked*) note "Crew blocked" "$st" request;; esac
  if echo "$st" | grep -qE '=(working|unknown)'; then idle=0; else idle=$((idle + 1)); fi
  [ $idle -ge 60 ] && note "Crew idle" "$st" request
done
