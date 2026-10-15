#!/usr/bin/env python3
"""CLI fixtures protect accounting across streaming, repeated snapshots and windows."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("crew-ledger.py")


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.roles = self.home / "roles.txt"
        self.run = self.home / "run"
        self.run.mkdir()

    def log(self, relative, events):
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(json.dumps(e) for e in events) + "\n")
        return path

    def ledger(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), "--home", str(self.home),
                                 "--json", *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_three_formats_and_run_aggregation(self):
        self.roles.write_text('lead claude session=c1\nworker codex cwd=/work\nreview pi session=p1\n')
        t = lambda minute: f"2026-10-15T10:{minute:02}:00Z"
        def claude(mid, minute, output, content=None):
            return dict(type="assistant", cwd="/lead", timestamp=t(minute), requestId="r" + mid,
                        message=dict(id=mid, model="claude", usage=dict(input_tokens=10,
                        cache_creation_input_tokens=20, cache_read_input_tokens=100,
                        output_tokens=output), content=content or []))
        parent_log = self.log('.claude/projects/project/c1.jsonl', [
            dict(type="user", cwd="/lead", timestamp=t(0), message=dict(content="work")),
            claude("a", 1, 1, [dict(type="tool_use", name="Write", input=dict(file_path="x"))]),
            dict(type="user", timestamp=t(1), message=dict(content=[dict(type="tool_result", content="ok")])),
            claude("a", 1, 4), claude("b", 2, 6),
            dict(type="user", timestamp=t(3), message=dict(content="status")),
            claude("c", 4, 8),
            dict(type="assistant", timestamp=t(4), message=dict(id="fake", model="<synthetic>",
                 usage=dict(input_tokens=0, output_tokens=0))),
            claude("e", 10, 1, [dict(type="tool_use", name="Write", input=dict(file_path="later"))]),
        ])
        os.utime(parent_log, (1, 1))
        self.log('.claude/projects/project/c1/subagents/workflows/w/agent-child.jsonl', [
            claude("d", 5, 2)])
        # A mirrored workflow event must not add a second call.
        self.log('.claude/projects/project/c1/subagents/agent-mirror.jsonl', [claude("d", 4, 1)])
        def codex(minute, inp, cached, output):
            return dict(type="event_msg", timestamp=t(minute), payload=dict(type="token_count", info=dict(
                total_token_usage=dict(input_tokens=inp, cached_input_tokens=cached, output_tokens=output),
                last_token_usage=dict(input_tokens=inp if minute == 0 else 80)),
                rate_limits=dict(primary=dict(used_percent=12))))
        self.log('.codex/sessions/2026/10/15/rollout-x.jsonl', [
            dict(type="session_meta", payload=dict(id="x1", cwd="/work")),
            codex(0, 100, 80, 10), codex(0, 100, 80, 10), codex(2, 180, 140, 20),
            codex(2, 180, 140, 20), codex(9, 250, 200, 25)])
        self.log('.pi/agent/sessions/project/pi.jsonl', [
            dict(type="session", id="p1", cwd="/review", timestamp=t(0)),
            dict(type="message", id="m1", timestamp=t(2), message=dict(role="assistant", model="gpt",
                content=[], usage=dict(input=30, cacheWrite=5, cacheRead=50, output=7)))])
        review = self.run / 'review-U1.md'
        review.write_text('Verdict: fix\n')
        review2 = self.run / 'review-U1-r2.md'
        review2.write_text('- 结论：**accept**\n')
        review3 = self.run / 'review-U2.md'
        review3.write_text('Verdict: **accept**\n')
        os.utime(review, (1792058460, 1792058460))
        os.utime(review2, (1792058520, 1792058520))
        os.utime(review3, (1792058580, 1792058580))
        data = self.ledger('--roles', str(self.roles), '--since', t(0), '--until', t(9),
                           '--run-dir', str(self.run), '--include-calls')
        lead, worker, review = data['roles']
        self.assertEqual([lead[k] for k in ('calls', 'uncached_input', 'cache_write', 'cache_read', 'output')],
                         [4, 40, 80, 400, 20])
        self.assertEqual(lead['equivalent_input_estimate'], 160)
        self.assertEqual(lead['idle_equivalent_estimate'], 80)
        self.assertEqual(lead['mean_context'], 130)
        self.assertEqual([worker[k] for k in ('calls', 'uncached_input', 'cache_read', 'output')], [2, 40, 140, 20])
        self.assertEqual(worker['peak_context'], 100)
        self.assertEqual(worker['mean_context'], 90)
        self.assertEqual(worker['rate_limits'][0]['value']['primary']['used_percent'], 12)
        self.assertEqual([review[k] for k in ('calls', 'uncached_input', 'cache_write', 'cache_read', 'output')],
                         [1, 30, 5, 50, 7])
        self.assertEqual(data['total']['equivalent_input_estimate'], 254)
        self.assertEqual(data['total']['accepted_units'], 2)
        self.assertEqual(data['total']['equivalent_per_accepted_unit_estimate'], 127)
        self.assertEqual(len(data['calls']), 7)
        main = self.ledger('--claude-session', 'c1', '--main-only', '--until', t(9))
        self.assertEqual(main['total']['calls'], 3)
        # The pre-window cumulative value is subtracted; end is exclusive.
        window = self.ledger('--roles', str(self.roles), '--since', t(2), '--until', t(5))
        self.assertEqual(window['roles'][1]['uncached_input'], 20)
        self.assertEqual(window['roles'][1]['cache_read'], 60)
        self.assertEqual(window['roles'][1]['calls'], 1)

    def test_latest_review_and_bad_input_visibility(self):
        self.roles.write_text('review pi session=p1\n')
        path = self.log('.pi/agent/sessions/project/pi.jsonl', [
            dict(type='session', id='p1', cwd='/review', timestamp='2026-10-15T10:00:00Z'),
            dict(type='message', id='m', timestamp='2026-10-15T10:01:00Z', message=dict(
                role='assistant', usage=dict(input=10, output=2)))])
        with path.open('a') as f:
            f.write('{truncated\n')
        review = self.run / 'review-U1.md'
        review.write_text('Verdict: accept\n')
        later = self.run / 'review-U1-r2.md'
        later.write_text('Verdict: request changes\n')
        os.utime(review, (1792058400, 1792058400))
        os.utime(later, (1792058500, 1792058500))
        data = self.ledger('--roles', str(self.roles), '--run-dir', str(self.run))
        self.assertEqual(data['total']['accepted_units'], 0)
        self.assertIsNone(data['total']['equivalent_per_accepted_unit_estimate'])
        self.assertEqual(data['total']['calls'], 1)
        self.assertTrue(any('malformed JSON' in w for w in data['warnings']))

    def test_resumed_claude_history_counts_once_per_role(self):
        def call(mid, minute, output, content=None):
            return dict(type='assistant', cwd='/lead', timestamp=f'2026-10-15T10:0{minute}:00Z',
                        requestId='r' + mid, message=dict(id=mid, model='claude', content=content or [],
                        usage=dict(input_tokens=10, cache_creation_input_tokens=20,
                                   cache_read_input_tokens=100, output_tokens=output)))
        self.log('.claude/projects/project/c1.jsonl', [call('a', 1, 1, [
            dict(type='tool_use', name='Write', input=dict(file_path='x'))])])
        self.log('.claude/projects/project/c2.jsonl', [call('a', 2, 4), call('b', 3, 6)])
        self.roles.write_text('lead claude cwd=/lead\n')
        args = ['--roles', str(self.roles), '--since', '2026-10-15T10:00:00Z', '--include-calls']
        data = self.ledger(*args)
        self.assertEqual(data['total']['calls'], 2)
        self.assertEqual(data['total']['cache_read'], 200)
        self.assertEqual(data['total']['output'], 10)
        self.assertEqual(data['total']['idle_equivalent_estimate'], 40)
        self.assertEqual(data['roles'][0]['sessions'], ['c1', 'c2'])
        self.assertTrue(data['calls'][0]['source'].endswith('c2.jsonl'))
        self.assertEqual(data['warnings'], [])
        self.roles.write_text('first claude session=c1\nsecond claude session=c2\n')
        data = self.ledger(*args)
        self.assertTrue(any('first' in w and 'second' in w and 'shared' in w for w in data['warnings']))

    def test_review_formats_and_missing_latest_verdict(self):
        self.roles.write_text('lead claude session=c1\n')
        self.log('.claude/projects/project/c1.jsonl', [dict(type='user', cwd='/lead')])
        formats = ['**Verdict:** accept', 'Verdict: `accept`', '## Verdict\naccept',
                   'REVIEW U3 accept', 'Verdict: **accept**', '**Verdict: accept**',
                   '- 结论：`accept`', '## Verdict\n\n**accept**']
        for index, text in enumerate(formats):
            (self.run / f'review-U{index}.md').write_text(text + '\n')
        first = self.run / 'review-latest.md'
        first.write_text('Verdict: accept\n')
        os.utime(first, (1792058400, 1792058400))
        later = self.run / 'review-latest-r2.md'
        later.write_text('Stopped before the review was complete.\n')
        os.utime(later, (1792058500, 1792058500))
        data = self.ledger('--roles', str(self.roles), '--run-dir', str(self.run))
        self.assertEqual({r['unit'] for r in data['accepted_reviews']},
                         {f'U{i}' for i in range(len(formats))})
        self.assertTrue(any(str(later) in w and 'verdict' in w for w in data['warnings']))

    def test_ambiguous_and_overlapping_roles_do_not_double_count(self):
        self.log('.claude/projects/project/c1.jsonl', [dict(type='user', cwd='/lead')])
        self.log('.claude/projects/project/c2.jsonl', [dict(type='user', cwd='/lead')])
        specs = ['a claude session=c\n', 'a claude session=c1\nb claude session=c1\n',
                 'a claude cwd=/lead\n']
        for spec in specs:
            with self.subTest(spec=spec):
                self.roles.write_text(spec)
                result = subprocess.run([sys.executable, str(SCRIPT), '--home', str(self.home),
                                         '--roles', str(self.roles), '--json'], capture_output=True)
                self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
