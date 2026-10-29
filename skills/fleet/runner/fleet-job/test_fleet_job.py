#!/usr/bin/env python3
"""Fake omp, pi and agy CLIs pin each engine's invocation and how its output becomes a job status."""

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
if [[ -n "$schema" && "${FAKE_MODE:-ok}" == ok ]]; then
  payload='{"verdict":"take"}'; [[ -n "$FAKE_STRUCTURED" ]] && payload="$FAKE_STRUCTURED"
  structured=",\"structured_output\":$payload"
fi
case "${FAKE_MODE:-ok}" in
  ok)      echo "{\"conversation_id\":\"conv-1\",\"status\":\"SUCCESS\",\"response\":\"agy reply\",\"num_turns\":2,\"usage\":{\"input_tokens\":1200,\"output_tokens\":34,\"cache_read_tokens\":500}$structured}" ;;
  denied)  echo 'jetski: no output produced'
           echo '{"conversation_id":"conv-1","status":"SUCCESS","response":"","denied_actions":[{"action":"write_file"}]}' ;;
  empty)   echo '{"conversation_id":"conv-1","status":"SUCCESS","response":""}' ;;
  prose)   echo '{"conversation_id":"conv-1","status":"SUCCESS","response":"I would run git diff","denied_actions":[{"action":"run_command"}]}' ;;
  error)   echo '{"conversation_id":"conv-1","status":"ERROR","response":""}' ;;
  nojson)  echo 'not json' ;;
esac
"""

FAKE_PI = r"""#!/bin/bash
printf '%s\n' "$@" > "$FAKE_CALLS"
echo '{"type":"session","id":"pi-session"}'
reply="pi reply"; [[ "${FAKE_MODE:-ok}" == empty ]] && reply=""
echo '{"type":"message_end","message":{"role":"assistant","provider":"route","model":"gpt-6.1-sol","content":[{"type":"text","text":"'"$reply"'"}],"usage":{"input":10,"output":2}}}'
echo '{"type":"agent_settled"}'
"""


# Stdin is recorded as "closed" when it reads end-of-file at once: omp waits forever on a pipe.
FAKE_OMP = r"""#!/bin/bash
printf '%s\n' "$@" > "$FAKE_CALLS"
if read -r -t 2 _line; then echo "stdin had data" > "$FAKE_CALLS.stdin"; else echo "closed" > "$FAKE_CALLS.stdin"; fi
echo '{"type":"session","id":"omp-session"}'
echo '{"type":"agent_start"}'
text="omp reply"; stop=stop; extra=""
case "${FAKE_MODE:-ok}" in
  empty)   text="" ;;
  aborted) stop=aborted; extra=',"errorMessage":"Request was aborted"' ;;
  error)   stop=error; extra=',"errorMessage":"429 rate limited"' ;;
  crash)   echo "omp: model unavailable" >&2; exit 1 ;;
  cut)     echo '{"type":"message_end","message":{"role":"assistant","content":[{"type":"text","text":"half"}],"stopReason":"stop"}}'; exit 0 ;;
esac
echo '{"type":"message_end","message":{"role":"user","content":[{"type":"text","text":"q"}]}}'
echo '{"type":"message_end","message":{"role":"assistant","provider":"openai-codex","model":"gpt-6.1-sol","content":[{"type":"text","text":"early"}],"stopReason":"toolUse","usage":{"input":100,"output":10,"cacheRead":50,"cost":{"total":0.01}}}}'
if [[ -n "$FAKE_SUBMIT" ]]; then
  echo '{"type":"tool_execution_end","toolName":"submit_result","result":{"content":[],"details":{"verdict":"take"}},"isError":false}'
fi
echo '{"type":"message_end","message":{"role":"assistant","provider":"openai-codex","model":"gpt-6.1-sol","content":[{"type":"text","text":"'"$text"'"}],"stopReason":"'"$stop"'","usage":{"input":20,"output":5,"cacheRead":70,"cost":{"total":0.02}}'"$extra"'}}'
echo '{"type":"agent_end","messages":[]}'
"""


def prompt_of(args):
    # The fake CLI writes one argument per line, so a multi-line prompt spans lines.
    return "\n".join(args[args.index("-p") + 1:])


class FleetJobTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        for name, body in (("agy", FAKE_AGY), ("pi", FAKE_PI), ("omp", FAKE_OMP)):
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
        self.assertEqual(args[:args.index("-p") + 1], ["--mode", "plan", "--model", "gemini-4-argon-high",
                                                       "--effort", "xhigh", "--output-format", "json", "-p"])
        self.assertTrue(prompt_of(args).startswith("review it\n\n"))
        self.assertEqual((result["status"], result["text"], result["session_id"]), ("completed", "agy reply", "conv-1"))
        self.assertEqual(result["tokens"], {"input": 1200, "output": 34, "cacheRead": 500, "cacheWrite": 0})

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
        for mode, error in (("error", "agy status ERROR"), ("nojson", "agy printed no JSON result")):
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

    OMP = {"engine": "omp", "model": "openai-codex/gpt-6.1-sol"}

    def test_omp_invocation_is_pinned_and_stdin_is_closed(self):
        result, args = self.job({**self.OMP, "prompt": "look", "thinking": "low", "tools": "readonly"})
        self.assertEqual(args, ["-p", "--mode", "json", "--session-dir", str(Path(result["dir"]) / "session"),
                                "--no-skills", "--no-rules", "--no-extensions", "--no-title", "--no-lsp",
                                "--model", "openai-codex/gpt-6.1-sol", "--thinking", "low",
                                "--tools", "read,grep,find,glob", "--", "look"])
        self.assertEqual(Path(f"{self.calls}.stdin").read_text().strip(), "closed")

    def test_omp_tool_presets(self):
        for tools, expected in (("research", "read,grep,find,glob,web_search"),
                                ("write", "read,grep,find,glob,edit,write,bash"),
                                ("read,grep", "read,grep")):
            with self.subTest(tools=tools):
                _, args = self.job({**self.OMP, "prompt": "q", "tools": tools})
                self.assertEqual(args[args.index("--tools") + 1], expected)
        _, args = self.job({**self.OMP, "prompt": "q", "tools": "full"})
        self.assertNotIn("--tools", args)

    def test_omp_result_sums_usage_and_names_the_answering_model(self):
        result, _ = self.job({**self.OMP, "prompt": "q"})
        self.assertEqual((result["engine"], result["status"], result["text"], result["model"]),
                         ("omp", "completed", "omp reply", "openai-codex/gpt-6.1-sol"))
        self.assertEqual(result["tokens"], {"input": 120, "output": 15, "cacheRead": 120, "cacheWrite": 0})
        self.assertAlmostEqual(result["cost_usd"], 0.03)
        self.assertEqual(result["session_id"], "omp-session")

    def test_omp_failures_carry_their_reason(self):
        for mode, error in (("error", "429 rate limited"), ("aborted", "Request was aborted"),
                            ("crash", "omp: model unavailable"), ("cut", "omp exited before agent_end")):
            with self.subTest(mode=mode):
                result, _ = self.job({**self.OMP, "prompt": "q"}, mode)
                self.assertEqual(result["status"], "failed")
                self.assertIn(error, result["error"])

    def test_omp_empty_answer_is_no_result(self):
        result, _ = self.job({**self.OMP, "prompt": "q"}, "empty")
        self.assertEqual((result["status"], result["error"]), ("no_result", "omp returned nothing"))

    def test_omp_requires_a_model_and_refuses_pi_only_fields(self):
        self.assertEqual(self.refused({"engine": "omp", "prompt": "q"}).returncode, 2)
        for spec in ({"no_extensions": True}, {"approve": True}):
            with self.subTest(spec=spec):
                self.assertEqual(self.refused({**self.OMP, "prompt": "q", **spec}).returncode, 2)

    def test_omp_passes_extensions_and_the_system_prompt_suffix(self):
        _, args = self.job({**self.OMP, "prompt": "q", "extensions": ["x.ts"], "append_system_prompt": "be brief"})
        self.assertEqual(args[args.index("-e") + 1], "x.ts")
        self.assertEqual(args[args.index("--append-system-prompt") + 1], "be brief")

    # Probed on omp 18.13.3: it registers submit_result from submit_result.ts and reports the
    # call in tool_execution_end, as Pi does. It has no agent_before_settle, so nothing reminds.
    def test_omp_schema_is_supported_through_submit_result(self):
        schema = {"type": "object", "properties": {"verdict": {"type": "string"}}}
        self.env["FAKE_SUBMIT"] = "1"
        result, args = self.job({**self.OMP, "prompt": "q", "schema": schema})
        self.assertEqual(args[args.index("--tools") + 1], "read,grep,find,glob,submit_result")
        self.assertTrue(args[args.index("-e") + 1].endswith("submit_result.ts"))
        self.assertEqual((result["status"], result["structured"]), ("completed", {"verdict": "take"}))

    def test_omp_schema_without_a_submission_is_no_result(self):
        schema = {"type": "object", "properties": {"verdict": {"type": "string"}}}
        result, _ = self.job({**self.OMP, "prompt": "q", "schema": schema})
        self.assertEqual(result["status"], "no_result")
        self.assertIn("submit_result", result["error"])

    def git(self, repo, *args):
        done = subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t",
                               "-c", "commit.gpgsign=false", *args], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def repo(self):
        repo = self.root / "repo"
        (repo / "src").mkdir(parents=True)
        (repo / "docs").mkdir()
        (repo / "src" / "a.py").write_text("a = 1\n")
        (repo / "docs" / "b.md").write_text("b\n")
        self.git(repo, "init", "-q", "-b", "main")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", "base")
        self.git(repo, "switch", "-q", "-c", "work")
        (repo / "src" / "a.py").write_text("a = 2\n")
        (repo / "docs" / "b.md").write_text("b changed\n")
        self.git(repo, "commit", "-qam", "change")
        return repo

    def test_output_holds_a_schema_jobs_structured_result(self):
        schema = {"type": "object", "properties": {"note": {"type": "string"}}}
        self.env["FAKE_STRUCTURED"] = '{"note":"caf\u00e9"}'
        result, _ = self.job({"engine": "agy", "prompt": "rule", "schema": schema, "output": "out/rule.json"})
        path = self.root / "out" / "rule.json"
        self.assertEqual(result["output"], str(path))
        self.assertEqual(path.read_text(), '{\n  "note": "caf\u00e9"\n}\n')

    def test_output_holds_a_text_jobs_text_as_it_is(self):
        for spec in ({"engine": "agy"}, {"engine": "pi"}):
            with self.subTest(engine=spec["engine"]):
                result, _ = self.job({"prompt": "q", "output": "text.md", **spec})
                reply = "agy reply" if spec["engine"] == "agy" else "pi reply"
                self.assertEqual((self.root / "text.md").read_text(), reply)
                self.assertEqual(result["output"], str(self.root / "text.md"))

    def test_output_of_a_failed_job_names_the_status_and_error(self):
        result, _ = self.job({"engine": "agy", "prompt": "q", "output": "text.md"}, "error")
        self.assertEqual((self.root / "text.md").read_text(), "status: failed\nerror: agy status ERROR\n")
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}}
        self.job({"engine": "agy", "prompt": "q", "schema": schema, "output": "failed.json"}, "error")
        self.assertEqual(json.loads((self.root / "failed.json").read_text()),
                         {"status": "failed", "error": "agy status ERROR"})

    def test_diff_writes_stat_full_and_each_part(self):
        repo = self.repo()
        diff = {"base": "main", "dir": "review", "parts": {"src.diff": ["src"], "docs.diff": ["docs"]}}
        self.job({"engine": "agy", "prompt": "q", "cwd": str(repo), "diff": diff})
        out = repo / "review"
        self.assertIn("2 files changed", (out / "stat.txt").read_text())
        full = (out / "full.diff").read_text()
        self.assertTrue("src/a.py" in full and "docs/b.md" in full)
        src = (out / "src.diff").read_text()
        self.assertTrue("src/a.py" in src and "docs/b.md" not in src)
        docs = (out / "docs.diff").read_text()
        self.assertTrue("docs/b.md" in docs and "src/a.py" not in docs)

    def test_diff_with_an_unknown_ref_starts_no_job(self):
        repo = self.repo()
        done = self.refused({"prompt": "q", "cwd": str(repo), "diff": {"base": "nope", "dir": "review"}})
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("nope", done.stderr)
        self.assertFalse((self.root / "jobs").exists() and list((self.root / "jobs").iterdir()))
        self.assertFalse((repo / "review").exists())

    def test_read_only_agy_prompt_warns_about_shell_and_writes(self):
        for tools, warned in (("readonly", True), ("research", True), ("write", False)):
            with self.subTest(tools=tools):
                _, args = self.job({"engine": "agy", "prompt": "review it", "tools": tools})
                self.assertEqual("read-only mode" in prompt_of(args), warned)
                self.assertTrue(prompt_of(args).startswith("review it"))

    def test_an_empty_answer_is_no_result_for_each_engine(self):
        for engine in ("pi", "agy"):
            with self.subTest(engine=engine):
                result, _ = self.job({"engine": engine, "prompt": "q"}, "empty")
                self.assertEqual(result["status"], "no_result")
                self.assertIn("returned nothing", result["error"])

    def test_an_empty_agy_answer_carries_its_denied_actions(self):
        result, _ = self.job({"engine": "agy", "prompt": "q"}, "denied")
        self.assertEqual((result["status"], result["denied_actions"]), ("no_result", ["write_file"]))
        self.assertIn("write_file", result["error"])

    def test_result_outcome_prints_only_status_error_and_output_path(self):
        result, _ = self.job({"engine": "agy", "prompt": "q", "output": "o.md"}, "error")
        done = subprocess.run([sys.executable, SCRIPT, "result", result["job_id"], "--outcome"],
                              env=self.env, capture_output=True, text=True)
        self.assertEqual(json.loads(done.stdout),
                         {"status": "failed", "error": "agy status ERROR", "output": str(self.root / "o.md")})

    def fleet(self, *args, env=None):
        return subprocess.run([sys.executable, SCRIPT, *args], env=env or self.env,
                              capture_output=True, text=True)

    def finished_job(self, supervisor_pid):
        # A job whose engine has exited but whose result.json is not yet published.
        jdir = self.root / "jobs" / "20260101-000000-j-abc123"
        jdir.mkdir(parents=True)
        (jdir / "spec.json").write_text(json.dumps(
            {"engine": "agy", "cwd": str(self.root), "output": str(self.root / "o.md")}))
        (jdir / "state.json").write_text(json.dumps(
            {"status": "finished", "exit_code": 0, "supervisor_pid": supervisor_pid}))
        (jdir / "events.jsonl").write_text('{"conversation_id":"c","status":"SUCCESS","response":"hi"}\n')
        return jdir

    def test_wait_does_not_end_before_the_supervisor_publishes_the_output(self):
        jdir = self.finished_job(os.getpid())
        done = self.fleet("wait", jdir.name, "--timeout", "0")
        self.assertEqual((done.returncode, json.loads(done.stdout)["status"]), (3, "running"))
        self.assertFalse((self.root / "o.md").exists())

    def test_a_job_whose_supervisor_died_before_publishing_is_finalized(self):
        dead = subprocess.Popen(["true"])
        dead.wait()
        jdir = self.finished_job(dead.pid)
        done = self.fleet("result", jdir.name, "--outcome")
        self.assertEqual(json.loads(done.stdout),
                         {"status": "completed", "error": None, "output": str(self.root / "o.md")})
        self.assertEqual((self.root / "o.md").read_text(), "hi")

    def test_an_engine_that_cannot_start_still_writes_the_output(self):
        empty = self.root / "empty"
        empty.mkdir()
        spec_file = self.root / "spec.json"
        spec_file.write_text(json.dumps({"cwd": str(self.root), "engine": "agy", "prompt": "q",
                                         "output": "o.md"}))
        env = dict(self.env, PATH=str(empty))
        job_id = json.loads(self.fleet("start", "--spec", spec_file, env=env).stdout)["job_id"]
        self.assertEqual(self.fleet("wait", job_id, "--timeout", "30", env=env).returncode, 0)
        outcome = json.loads(self.fleet("result", job_id, "--outcome", env=env).stdout)
        self.assertEqual((outcome["status"], outcome["output"]), ("failed", str(self.root / "o.md")))
        self.assertIn("agy", outcome["error"])
        self.assertTrue((self.root / "o.md").read_text().startswith("status: failed\nerror: "))
        self.assertIn("agy", (self.root / "o.md").read_text())

    def test_an_output_that_cannot_be_written_fails_the_job(self):
        (self.root / "taken").mkdir()
        result, _ = self.job({"engine": "agy", "prompt": "q", "output": "taken"})
        self.assertEqual((result["status"], result["output"]), ("failed", None))
        self.assertIn("cannot write output", result["error"])

    def test_every_status_but_completed_says_why(self):
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}}}
        result, _ = self.job({"engine": "agy", "prompt": "q", "schema": schema}, "prose")
        self.assertEqual(result["status"], "no_result")
        self.assertIn("run_command", result["error"])
        result, _ = self.job({"engine": "pi", "prompt": "q", "schema": schema})
        self.assertEqual(result["status"], "no_result")
        self.assertIn("submit_result", result["error"])


if __name__ == "__main__":
    unittest.main()
