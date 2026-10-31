#!/bin/bash
# Install the fleet-runner subagent and the fleet-job tool this skill's GPT and Gemini stages run through.
# Usage: install-runner.sh [--force]   (without --force, existing files are left alone)
# FLEET_PYTHON, when set, becomes fleet_job.py's interpreter; it needs Python 3.10 or newer.
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
agent=~/.claude/agents/fleet-runner.md
tool=~/.claude/tools/fleet-job
if [ "${1:-}" != --force ] && { [ -e "$agent" ] || [ -e "$tool" ]; }; then
  echo "fleet-runner or fleet-job already installed; rerun with --force to replace them"
  exit 0
fi
mkdir -p ~/.claude/agents ~/.claude/tools
cp "$here/runner/fleet-runner.md" "$agent"
rm -rf "$tool"
cp -R "$here/runner/fleet-job" "$tool"
rm -rf "$tool/test_fleet_job.py" "$tool/__pycache__"
if [ -n "${FLEET_PYTHON:-}" ]; then
  { printf '#!%s\n' "$FLEET_PYTHON"; tail -n +2 "$tool/fleet_job.py"; } > "$tool/fleet_job.py.new"
  mv "$tool/fleet_job.py.new" "$tool/fleet_job.py"
fi
chmod +x "$tool/fleet_job.py"
echo "installed $agent and $tool ($(head -1 "$tool/fleet_job.py"))"
