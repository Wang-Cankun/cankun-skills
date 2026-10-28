#!/usr/bin/env python3
"""Fake pi and agy CLIs pin each engine's invocation and how its output becomes a job status."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("fleet_job.py")

FAKE_AGY = r"""#!/bin/bash
printf '%s\n' "$@" > "$FAKE_CALLS"
schema=""; prev=""
for a in "$@"; do [[ "$prev" == "--json-schema" ]] && schema="$a"; prev="$a"; done
structured=""
[[ -n "$schema" && "${FAKE_MODE:-ok}" == ok ]] && structured=',"structured_output":{"verdict":"take"}'
case "${FAKE_MODE:-ok}" in
  ok)      echo "{\"conversation_id\":\"conv-1\",\"status\":\"SUCCESS\",\"response\":\"agy reply\",\"num_turns\":2,\"usage\":{\"input_tokens\":1200,\"output_tokens\":34}$structured}" ;;
  denied)  echo 'jetski: no output produced'
           echo '{"conversation_id":"conv-1","status":"SUCCESS","response":"","denied_actions":[{"action":"write_file"}]}' ;;
  error)   echo '{"conversation_id":"conv-1","status":"ERROR","response":""}' ;;
  nojson)  echo 'not json' ;;
esac
"""

FAKE_PI = r"""#!/bin/bash
printf '%s\n' "$@" > "$FAKE_CALLS"
echo '{"type":"session","id":"pi-session"}'
echo '{"type":"message_end","message":{"role":"assistant","provider":"route","model":"gpt-6.1-sol","content":[{"type":"text","text":"pi reply"}],"usage":{"input":10,"output":2}}}'
echo '{"type":"agent_settled"}'
"""


class FleetJobTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        for name, body in (("agy", FAKE_AGY), ("pi", FAKE_PI)):
            (bin_dir / name).write_text(body)
            (bin_dir / name).chmod(0o755)
        self.calls = self.root / "calls"
        self.env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}",
                        FLEET_JOB_HOME=str(self.root / "jobs"), FAKE_CALLS=str(self.calls))

    def job(self, spec, mode="ok"):
        spec_file = self.root / "spec.json"
        spec_file.write_text(json.dumps({"cwd": str(self.root), **spec}))
        env = dict(self.env, FAKE_MODE=mode)
        start = subprocess.run([sys.executable, SCRIPT, "start", "--spec", spec_file],
                               env=env, capture_output=True, text=True)
        self.assertEqual(start.returncode, 0, start.stderr)
        job_id = json.loads(start.stdout)["job_id"]
        wait = subprocess.run([sys.executable, SCRIPT, "wait", job_id, "--timeout", "30"],
                              env=env, capture_output=True, text=True)
        self.assertEqual(wait.returncode, 0, wait.stderr)
        result = subprocess.run([sys.executable, SCRIPT, "result", job_id], env=env,
                                capture_output=True, text=True)
        return json.loads(result.stdout), self.calls.read_text().splitlines()

    def refused(self, spec):
        spec_file = self.root / "spec.json"
        spec_file.write_text(json.dumps({"cwd": str(self.root), **spec}))
        return subprocess.run([sys.executable, SCRIPT, "start", "--spec", spec_file],
                              env=self.env, capture_output=True, text=True)

    def test_agy_read_only_runs_in_plan_mode_with_the_prompt_last(self):
        result, args = self.job({"engine": "agy", "prompt": "review it", "thinking": "xhigh"})
        self.assertEqual(args, ["--mode", "plan", "--model", "gemini-4-argon-high", "--effort", "xhigh",
                                "--output-format", "json", "-p", "review it"])
        self.assertEqual((result["status"], result["text"], result["session_id"]), ("completed", "agy reply", "conv-1"))
        self.assertEqual(result["tokens"], {"input": 1200, "output": 34, "cacheRead": 0, "cacheWrite": 0})

    def test_agy_write_preset_skips_permissions(self):
        _, args = self.job({"engine": "agy", "prompt": "fix it", "tools": "write"})
        self.assertIn("--dangerously-skip-permissions", args)
        self.assertNotIn("plan", args)

    def test_agy_schema_returns_structured_output(self):
        schema = {"type": "object", "properties": {"verdict": {"type": "string"}}}
        result, args = self.job({"engine": "agy", "prompt": "rule", "schema": schema})
        self.assertEqual(args[args.index("--json-schema") + 1], str(Path(result["dir"]) / "schema.json"))
        self.assertEqual((result["status"], result["structured"]), ("completed", {"verdict": "take"}))

    def test_agy_failures_carry_their_reason(self):
        for mode, error in (("denied", "plan mode denied write_file"), ("error", "agy status ERROR"),
                            ("nojson", "agy printed no JSON result")):
            with self.subTest(mode=mode):
                result, _ = self.job({"engine": "agy", "prompt": "q"}, mode)
                self.assertEqual((result["status"], result["error"]), ("failed", error))

    def test_agy_refuses_what_only_pi_supports(self):
        for spec in ({"tools": ["read", "bash"]}, {"extensions": ["x.ts"]}, {"append_system_prompt": "x"},
                     {"approve": False}):
            with self.subTest(spec=spec):
                self.assertEqual(self.refused({"engine": "agy", "prompt": "q", **spec}).returncode, 2)

    def test_pi_model_is_pinned_to_its_provider(self):
        _, args = self.job({"prompt": "q", "model": "magpie/codex/gpt-6-luna", "tools": "write"})
        self.assertEqual(args[args.index("--tools") + 1], "read,grep,find,ls,edit,write,bash")
        self.assertEqual(args[args.index("--provider"):args.index("--provider") + 4],
                         ["--provider", "magpie", "--model", "codex/gpt-6-luna"])

    def test_pi_is_the_default_engine(self):
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}}
        result, args = self.job({"prompt": "build it", "schema": schema})
        self.assertEqual(args[args.index("--tools") + 1], "read,grep,find,ls,submit_result")
        self.assertTrue(args[args.index("-e") + 1].endswith("submit_result.ts"))
        self.assertEqual(args[-3:], ["-p", "--", "build it"])
        self.assertEqual((result["engine"], result["model"]), ("pi", "route/gpt-6.1-sol"))


if __name__ == "__main__":
    unittest.main()
