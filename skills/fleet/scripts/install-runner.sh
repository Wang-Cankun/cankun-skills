#!/bin/bash
# Install the fleet-runner subagent and the fleet-job tool this skill's GPT and Gemini stages run through.
# Usage: install-runner.sh [--force]   (without --force, existing files are left alone)
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
rm -f "$tool/test_fleet_job.py"
chmod +x "$tool/fleet_job.py"
echo "installed $agent and $tool"
