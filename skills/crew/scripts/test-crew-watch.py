#!/usr/bin/env python3
"""Exercise notifications through the watcher CLI and real archived usage logs."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPTS = Path(__file__).resolve().parent


class WatchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run = self.root / "run"
        self.run.mkdir()
        self.roles = self.root / "roles.txt"
        self.roles.write_text("worker claude session=fixture\n")
        self.now = time.time()
        self.log = self.root / ".claude/projects/project/fixture.jsonl"
        self.log.parent.mkdir(parents=True)
        self.usage(2_000_000)

    def usage(self, tokens):
        self.log.write_text(json.dumps(dict(type="assistant", cwd="/fixture",
            timestamp=datetime.fromtimestamp(self.now - 60, timezone.utc).isoformat(),
            requestId="r", message=dict(id="m", model="claude", content=[],
                usage=dict(input_tokens=tokens, output_tokens=1)))) + "\n")

    def artifact(self, name, when):
        path = self.run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("saved\n")
        os.utime(path, (when, when))

    def burn(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPTS / "crew-burn.py"),
            "--roles", str(self.roles), "--run-dir", str(self.run), "--home", str(self.root),
            "--until", datetime.fromtimestamp(self.now, timezone.utc).isoformat(), *extra],
            capture_output=True, text=True, timeout=10)

    def watch(self, event="", status="working", polls=4):
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        programs = {
            "herdr": '''import json, os, sys
from pathlib import Path
root = Path(os.environ["FIXTURE_ROOT"])
if sys.argv[1:3] == ["agent", "list"]:
    print(json.dumps({"result": {"agents": [{"name": "worker", "agent_status": os.environ["FIXTURE_STATUS"]}]}}))
elif sys.argv[1:3] == ["notification", "show"]:
    with (root / "notifications").open("a") as f: f.write(json.dumps(sys.argv[3:]) + "\\n")
else:
    raise SystemExit("unexpected Herdr action")
''',
            "sleep": '''import json, os, shutil, sys, time
from pathlib import Path
root = Path(os.environ["FIXTURE_ROOT"])
count = root / "polls"
with count.open("a") as f: f.write(sys.argv[1] + "\\n")
n = len(count.read_text().splitlines())
run = root / "run"
if n == 1 and os.environ["FIXTURE_EVENT"]:
    (run / os.environ["FIXTURE_EVENT"]).write_text("landed")
if n >= int(os.environ["FIXTURE_POLLS"]) and run.exists(): shutil.rmtree(run)
time.sleep(0.2)
''',
            "python3": '''import os, sys
args = sys.argv[1:]
if args[0].endswith("crew-burn.py"): args += ["--home", os.environ["FIXTURE_ROOT"]]
os.execv(sys.executable, [sys.executable, *args])
''',
        }
        for name, source in programs.items():
            path = bin_dir / name
            path.write_text(f"#!{sys.executable}\n" + source)
            path.chmod(0o755)
        env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ["PATH"],
            FIXTURE_ROOT=str(self.root), FIXTURE_EVENT=event, FIXTURE_STATUS=status,
            FIXTURE_POLLS=str(polls), CREW_BURN_WINDOW_SECONDS="600", CREW_BURN_THRESHOLD="1000000")
        result = subprocess.run(["bash", str(SCRIPTS / "crew-watch.sh"), str(self.run),
            "--roles", str(self.roles), "worker"], env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(set((self.root / "polls").read_text().splitlines()), {"30"})
        path = self.root / "notifications"
        notes = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        return result, notes

    def test_burn_notifies_once_keeps_watching_and_exits_when_removed(self):
        self.artifact("handoff-old.md", self.now - 601)
        self.artifact("scratch/review-not-a-handoff.md", self.now - 1)
        result, notes = self.watch()
        self.assertEqual([n[0] for n in notes], ["Crew burn"])
        self.assertIn("2,000,000 equivalent input", notes[0][2])
        self.assertIn("worker=2,000,000", notes[0][2])
        self.assertEqual(len((self.root / "polls").read_text().splitlines()), 4)

    def test_productive_window_stays_quiet(self):
        self.artifact("review-U1.md", self.now - 10)
        result, notes = self.watch()
        self.assertEqual(notes, [])
        self.assertEqual(result.stdout, "")

    def test_threshold_and_historical_window(self):
        self.usage(1_000_000)
        self.assertEqual(self.burn().stdout, "")
        self.usage(1_000_001)
        # A later artifact must not silence an earlier historical window.
        self.artifact("handoff-future.md", self.now + 60)
        result = self.burn()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1,000,001 equivalent input", result.stdout)
        self.artifact("review-U1.md", self.now - 1)
        self.assertEqual(self.burn().stdout, "")
        result = self.burn("--threshold", "nan")
        self.assertEqual(result.returncode, 2)

    def test_existing_events_keep_their_notifications(self):
        for event, status, title in [("handoff-U1.md", "working", "Crew file"),
                                      ("", "blocked", "Crew blocked"),
                                      ("", "idle", "Crew idle")]:
            with self.subTest(title=title):
                self.usage(1)
                result, notes = self.watch(event, status, polls=62)
                self.assertEqual([n[0] for n in notes], [title])
                for name in ("bin/herdr", "bin/sleep", "bin/python3", "polls", "notifications", "run/handoff-U1.md"):
                    (self.root / name).unlink(missing_ok=True)
                (self.root / "bin").rmdir()


if __name__ == "__main__":
    unittest.main()
