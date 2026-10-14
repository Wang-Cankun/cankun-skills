#!/bin/bash
# Install the pi-runner subagent and the pi-job tool this skill's GPT stages run through.
# Usage: install-runner.sh [--force]   (without --force, existing files are left alone)
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
agent=~/.claude/agents/pi-runner.md
tool=~/.claude/tools/pi-job
if [ "${1:-}" != --force ] && { [ -e "$agent" ] || [ -e "$tool" ]; }; then
  echo "pi-runner or pi-job already installed; rerun with --force to replace them"
  exit 0
fi
mkdir -p ~/.claude/agents ~/.claude/tools
cp "$here/runner/pi-runner.md" "$agent"
rm -rf "$tool"
cp -R "$here/runner/pi-job" "$tool"
chmod +x "$tool/pi_job.py"
echo "installed $agent and $tool"
