#!/usr/bin/env python3
"""Exercise crew-burn.py's alert through the CLI and a fixture usage log."""

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


class BurnTest(unittest.TestCase):
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

    def test_burn_without_progress_alerts(self):
        self.artifact("handoff-old.md", self.now - 601)
        self.artifact("scratch/review-not-a-handoff.md", self.now - 1)
        result = self.burn()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2,000,000 equivalent input", result.stdout)
        self.assertIn("worker=2,000,000", result.stdout)

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

    def test_a_role_with_no_log_yet_leaves_the_alert_on(self):
        self.roles.write_text("worker claude session=fixture\nlater pi cwd=/not-started\n")
        result = self.burn()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2,000,000 equivalent input", result.stdout)
        self.assertIn("later", result.stdout)

    def test_a_watched_pattern_counts_as_progress(self):
        self.artifact("thread.md", self.now - 10)
        self.assertIn("equivalent input", self.burn().stdout)
        result = self.burn("--files", r"^thread\.md$")
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_bad_pattern_is_refused(self):
        result = self.burn("--files", "(")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
