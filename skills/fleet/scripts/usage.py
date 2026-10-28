#!/usr/bin/env python3
"""Per-stage token use of one workflow run: Claude stages from their transcripts, fleet jobs from theirs.

usage.py <runId> [--project-dir ~/.claude/projects/<slug>]

The workflow's own usage line counts input plus output and leaves out cache reads, which are most
of what an agentic stage processes; this prints all four counts so the stages compare honestly.
"""
import argparse
import json
import re
from pathlib import Path

JOB_ID = re.compile(r"\d{8}-\d{6}-[a-z0-9-]+-[0-9a-f]{6}")
KEYS = ("input", "output", "cache_read", "cache_write")


def claude_usage(transcript):
    # One API message spans several transcript lines that repeat its usage; count each id once.
    seen, total = {}, dict.fromkeys(KEYS, 0)
    for line in transcript.read_text().splitlines():
        try:
            msg = json.loads(line).get("message") or {}
        except json.JSONDecodeError:
            # A stage still running when this is read leaves a truncated last line.
            continue
        if msg.get("role") == "assistant" and msg.get("usage"):
            seen[msg.get("id") or len(seen)] = msg["usage"]
    for u in seen.values():
        total["input"] += u.get("input_tokens", 0)
        total["output"] += u.get("output_tokens", 0)
        total["cache_read"] += u.get("cache_read_input_tokens", 0)
        total["cache_write"] += u.get("cache_creation_input_tokens", 0)
    return total, len(seen)


JOBS = Path.home() / ".claude/fleet-jobs"


def job_usage(job):
    r = json.loads((JOBS / job / "result.json").read_text())
    t = r.get("tokens", {})
    return {"input": t.get("input", 0), "output": t.get("output", 0), "cache_read": t.get("cacheRead", 0),
            "cache_write": t.get("cacheWrite", 0)}, r.get("cost_usd", 0.0), r.get("model", "")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run")
    p.add_argument("--project-dir", type=Path)
    a = p.parse_args()
    roots = [a.project_dir] if a.project_dir else list((Path.home() / ".claude/projects").iterdir())
    dirs = [d for r in roots for d in r.glob(f"*/subagents/workflows/{a.run}")]
    if not dirs:
        raise SystemExit(f"no transcripts for {a.run}")

    rows = []
    for meta in sorted(dirs[0].glob("*.meta.json")):
        info = json.loads(meta.read_text())
        transcript = meta.with_name(meta.name.replace(".meta.json", ".jsonl"))
        u, turns = claude_usage(transcript)
        rows.append((info["description"], info.get("model") or "inherit", turns, u, None))
        for job in sorted(set(JOB_ID.findall(transcript.read_text()))):
            if (JOBS / job / "result.json").exists():
                pu, cost, model = job_usage(job)
                rows.append((f"  └ {job}", model, None, pu, cost))

    print(f"{'stage':44} {'model':26} {'turns':>5} {'input':>9} {'output':>8} {'cache_rd':>10} {'cache_wr':>9} {'total':>10} {'usd':>6}")
    for name, model, turns, u, cost in rows:
        total = sum(u.values())
        print(f"{name:44} {model:26} {turns if turns is not None else '':>5} {u['input']:>9} {u['output']:>8} "
              f"{u['cache_read']:>10} {u['cache_write']:>9} {total:>10} {f'{cost:.2f}' if cost is not None else '':>6}")
    jobs = sum(c for *_, c in rows if c is not None)
    print(f"Pi jobs' cost_usd (API-equivalent; billed to the ChatGPT subscription; agy reports none): {jobs:.2f}")


if __name__ == "__main__":
    main()
