# Observe a crew: ledger and watcher

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

Watch in the background with
`scripts/crew-watch.sh <run dir> --roles <run dir>/roles.txt [--files <regex>] <role-name>...`.
Herdr role names select active panes; the ledger spec also covers previous coordinators.
The watcher polls every 30 seconds and exits quietly when the run directory is gone.
It exits with a Herdr notification when a run file whose name `--files` matches (a Python
regex searched in the name; default `^(handoff|review)-.*\.md$`, and `^thread\.md$` for a
table) is new or rewritten and no named role is working or `unknown`, a role is `blocked`, or
every role has been idle for 30 minutes. Re-arm after those events. To hear from one agent
while others keep working, run one watcher per agent with `--files` matching its files, and
give `--roles` to only one watcher, whose `--files` covers every agent's files: each watcher
with `--roles` raises its own burn alerts for the whole run. Keep scratch files in a
subdirectory.

With `--roles`, it also notifies when equivalent input exceeds 1M in a trailing 600-second
window with no update to a matching run file. These are initial threshold estimates
from history, not proof of wasted work. Set `CREW_BURN_THRESHOLD` and
`CREW_BURN_WINDOW_SECONDS` from the run's measured pace and record overrides in the card.
A burn notification leaves agents and the watcher running; the watcher limits repeats to once per
window. Diagnose the leading roles before changing the plan. Ledger warnings, such as a role
with no session yet, ride along in the notification; ledger errors appear on stderr and
suppress that burn check, and the other events keep working.
Omitting `--roles` keeps file/status watching alone. For historical diagnosis, run
`scripts/crew-burn.py --roles <roles-file> --run-dir <run-dir> --until <ISO-timestamp>`
with the watcher's `--files`;
it prints only an eligible alert, using current artifact mtimes.
