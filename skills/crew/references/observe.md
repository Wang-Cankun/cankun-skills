# Observe a crew: ledger and burn check

Optional tools for a team or table whose cost or progress you want to see. Paths are relative to the skill directory.

Measure the run with `scripts/crew-ledger.py` (Python 3.9+, standard library only).
Put a roles spec in `<run dir>/roles.txt`, one `NAME TOOL SELECTOR` per line; use shell quoting
for paths with spaces and `#` for comments. Tools are `claude`, `codex`, and `pi`; an agent of
another kind, such as `omp` or `agy`, has no reader, so its usage is missing from the totals. Select by `session=ID`
(an unambiguous prefix works) or `cwd=/absolute/worktree`. Include the coordinator and any
replacement sessions. Keep roles disjoint; Claude session accounting includes its subagents
and workflows. Record the run's UTC start time in the card. For example:

```text
coordinator claude session=<session-id>
executor codex cwd=/absolute/worktree
reviewer claude session=<review-session-id>
```

Have a worker save a snapshot at each accepted unit and budget checkpoint:

```bash
python3 scripts/crew-ledger.py --roles "<run dir>/roles.txt" \
  --since "<run-start-ISO-timestamp-with-timezone>" --run-dir "<run dir>"
```

Output is Markdown; `--json` emits structured totals, and `--include-calls` adds timestamped
usage for replay. `--until` bounds the reporting window; `--home` selects a log archive. Use
`--claude-session <ID>` instead of `--roles` for one Claude session tree; `--main-only`
excludes descendants. Cwd selection requires `--since`. Equivalent input is an estimate:
uncached input + cache writes + cache reads / 10, excluding output. The estimate measures neither money nor
provider quota. Accepted units use the latest review verdict and current file mtimes,
not merge status. The ledger prints its idle activity proxy; read-only work can count idle.
Resolve warnings about missing or overlapping sessions before using totals for a decision.
Read only the worker's budget summary and paths in the coordinator. At the card's budget or
projected overrun, follow its stop/escalation rule before assigning more work.

Check the burn at each wait check-in, or at the card's budget checkpoints:

```bash
python3 scripts/crew-burn.py --roles "<run dir>/roles.txt" --run-dir "<run dir>" [--files <regex>]
```

It prints an alert only when equivalent input over the trailing window (`--window-seconds`,
default 600) exceeds `--threshold` (default 1M) with no update to a run file whose name
`--files` matches (a Python regex searched in the name; default `^(handoff|review)-.*\.md$`,
and `^thread\.md$` for a table); otherwise it prints nothing. The defaults are initial
estimates from history, not proof of wasted work: set them from the run's measured pace and
record overrides in the card. An alert leaves every agent running; diagnose the leading roles
before changing the plan. Ledger warnings, such as a role with no session yet, ride along in the
alert. `--until` replays a historical window using current artifact mtimes; `--home` selects a
log archive.
