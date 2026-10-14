#!/bin/bash
# Usage: lane-watch.sh <handoff-dir> <lead-name>... 
# Run in the background from the coordinator. Exits, with a Herdr notification, when a new handoff
# file appears, a lead is blocked, or every lead has sat idle for 30 minutes (a lead waiting on its
# own background job is idle too, so a short idle limit wakes the coordinator for nothing).
dir=$1; shift
before=$(ls "$dir" | sort)
idle=0
status() {
  herdr agent list | python3 -c '
import sys, json
names = set(sys.argv[1:])
for a in json.load(sys.stdin)["result"]["agents"]:
    if a.get("name") in names: print(a["name"] + "=" + a["agent_status"])' "$@"
}
note() { herdr notification show "$1" --body "$2" --sound "$3" >/dev/null 2>&1; echo "$1: $2"; exit 0; }
while true; do
  sleep 30
  now=$(ls "$dir" | sort)
  if [ "$now" != "$before" ]; then note "Lane handoff" "$(comm -13 <(echo "$before") <(echo "$now") | tr '\n' ' ')" done; fi
  st=$(status "$@" | tr '\n' ' ')
  case "$st" in *blocked*) note "Lane blocked" "$st" request;; esac
  if echo "$st" | grep -qE '=(working|unknown)'; then idle=0; else idle=$((idle + 1)); fi
  [ $idle -ge 60 ] && note "Lanes idle" "$st" request
done
