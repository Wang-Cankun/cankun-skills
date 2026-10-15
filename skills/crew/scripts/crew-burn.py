#!/usr/bin/env python3
"""Print a burn alert only when a full window has no handoff or review update.

Uses crew-ledger.py's accounting. --until replays a historical window using the
current artifact mtimes; --home selects a log archive. No files are written.
"""

import argparse
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import subprocess
import sys


def updated(run_dir, start, end):
    return any(path.is_file() and start <= path.stat().st_mtime < end
               for pattern in ("handoff-*.md", "review-*.md") for path in run_dir.glob(pattern))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roles", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--window-seconds", type=int, default=600)
    parser.add_argument("--threshold", type=float, default=1_000_000)
    parser.add_argument("--until", help="ISO timestamp with timezone; defaults to now")
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    try:
        if args.window_seconds <= 0 or not math.isfinite(args.threshold) or args.threshold <= 0:
            raise ValueError("window and threshold must be positive and finite")
        end = datetime.fromisoformat(args.until.replace("Z", "+00:00")) if args.until else datetime.now(timezone.utc)
        if end.tzinfo is None:
            raise ValueError("--until must include a timezone")
        start = end - timedelta(seconds=args.window_seconds)
        if not args.run_dir.is_dir():
            return
        if updated(args.run_dir, start.timestamp(), end.timestamp()):
            return
        result = subprocess.run([
            sys.executable, str(Path(__file__).with_name("crew-ledger.py")),
            "--roles", str(args.roles), "--home", str(args.home),
            "--since", start.isoformat(), "--until", end.isoformat(), "--json",
        ], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        if report["warnings"]:
            raise ValueError("; ".join(report["warnings"]))
        # A handoff can land while the ledger scans large session logs.
        if not args.run_dir.is_dir():
            return
        checked_until = end if args.until else datetime.now(timezone.utc)
        if updated(args.run_dir, start.timestamp(), checked_until.timestamp()):
            return
        total = report["total"]["equivalent_input_estimate"]
        if total > args.threshold:
            top = sorted(report["roles"], key=lambda r: r["equivalent_input_estimate"], reverse=True)[:3]
            sources = ", ".join(f'{r["role"]}={r["equivalent_input_estimate"]:,.0f}' for r in top)
            print(f"{total:,.0f} equivalent input (estimate) in {args.window_seconds}s "
                  f"without a handoff/review update; threshold >{args.threshold:,.0f}. "
                  f"Top roles: {sources}. Diagnose; agents are still running.")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        if args.run_dir.is_dir():
            parser.exit(2, f"crew-burn: {getattr(error, 'stderr', None) or error}\n")


if __name__ == "__main__":
    main()
