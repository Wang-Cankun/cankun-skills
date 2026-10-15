---
name: crew
compatibility: Requires Herdr (run from inside a Herdr pane, HERDR_ENV=1), the agent CLIs used by the chosen roles (Claude Code, Pi, Codex), and python3 for the optional watcher. GPT Pro consultations go through the confer skill.
metadata:
  group: models
  personal: true
  summary: >-
    Runs a task with a crew of persistent agents in Herdr panes: a coordinator
    routes work between executors and independent reviewers, and brings the
    user only decisions.
description: "Run a task with a crew of persistent coding agents in Herdr panes: a coordinator writes the crew card, starts executors and reviewers, routes work between them through files, and brings the user only decisions and a debrief. Use when the user invokes /crew or asks for a coordinator, executor and reviewer setup in Herdr."
---

# Crew

The user decides; the crew routes. One line from the user (the work, optionally a shape such
as "two Claude executors and a GPT reviewer") should be enough to start. After that the user
appears only at the decision points the crew card names, and each time can decide from one
message.

Invoking this skill authorizes the multi-agent setup for the run. Use the role defaults below
unless the user names another shape; keep each executor and its reviewer in different model
families. Resolve a requested shape that conflicts with that independence before starting.

Requires Herdr inside a managed pane (`HERDR_ENV=1`), the CLIs used by the chosen roles, and
`python3` for the optional watcher. Check `test "${HERDR_ENV:-}" = 1` before controlling panes.
Pane mechanics are in the `herdr` skill. Read `herdr --help` and the relevant group help
(`herdr worktree`, `herdr pane`, `herdr agent`, `herdr tab`, `herdr notification`) before use;
the installed CLI is the syntax authority. This skill decides who does what.

## Roles

- **Coordinator**: normally this session. Owns the crew card, the routing, the integration of
  accepted work, and every message to the user. It does not implement, and it does not accept
  work on its executors' word.
- **Executor**: Claude by default; one per lane, in its own worktree and branch. Implements its
  queue, verifies its own work, and ends each unit with a handoff file. Never pushes, merges,
  posts, restarts services or touches production data unless the card says so.
- **Reviewer**: GPT by default, in a Codex or Pi pane; from a different model family than the
  executor it reviews, so the judge is outside the producer. Reads the diff and runs the checks
  itself; reads the executor's handoff only for what was claimed, never as evidence. Reports
  findings and a verdict; does not edit the executor's branch.
- **Consultant** (optional): GPT Pro through the `confer` skill, for a judgement no pane can
  settle (a design direction, a stubborn bug). Run the round in a visible pane
  (`herdr pane run <pane> "<confer command>"`) so the user can watch it; record the thread name
  in the card so any role can continue it.

Start with the fewest panes the work splits into. Add a lane only when its files do not overlap
another lane's; give a shared hotspot file one writer. Split the run when routing and integration
stop fitting the coordinator's available attention and context.

## Steps

1. **Brief.** Run from a brief that names the finish line: a `common-ground` brief, or an issue
   batch whose issues carry done criteria. Done when every unit of work has a check that shows
   it is done.
2. **Write the crew card**, the run's call sheet, at `<run dir>/card.md` in a directory Git
   ignores (for example `.work/crew/<run>/`):
   - goal and finish line;
   - roles: name, agent kind and model, pane, worktree and branch, queue, native CLI arguments
     and permission mode;
   - routing: who sends what to whom, and the round limit for review (two rounds by default);
   - escalations: what goes to the user: anything destructive or outward-facing, a scope
     change, a reviewer and executor who still disagree at the round limit, a spent budget;
   - boundaries: who may commit, push, merge, post, restart or deploy;
   - budget and stop condition;
   - current state: integration branch and head, each role's current unit, each unit's status and
     latest processed handoff and review paths, pending actions, active coordinator pane and session,
     watcher owner, and the coordinator handover interval from step 4.

   Show the card to the user in one message and start when they agree, unless they already
   said to go. Done when someone reading only the card knows who does what and when the user
   is called.
3. **Start the crew.** Create each executor's worktree from the card's repository and base:

   ```bash
   herdr worktree create --cwd "<repo>" --branch "<branch>" --base "<base>" --label "<role>" --no-focus
   ```

   For a reviewer or consultant, split an explicit source pane, preserving the intended cwd:

   ```bash
   herdr pane split --pane <source-pane> --direction right --cwd "<cwd>" --no-focus
   ```

   Choose `right` or `down` to keep the panes usable. Read the actual pane IDs and worktree path
   from the creation responses; use a shell pane that is ready for input. Start each agent with
   the native arguments recorded in the card, using the user's launch preferences and passing
   them after `--`. Agent kind alone does not select a model; confirm the card's model at startup,
   especially for a GPT reviewer in Pi.

   ```bash
   herdr agent start <role-name> --kind <kind> --pane <pane-id> -- <native-args...>
   ```

   For a Codex role that must commit in a worktree, record a permission mode that allows Git
   metadata writes. When the user has authorized bypassing the sandbox and approvals:

   ```bash
   herdr agent start <role-name> --kind codex --pane <pane-id> -- \
     --cd "<lane-worktree>" --dangerously-bypass-approvals-and-sandbox
   ```

   This disables both controls; use it only for the user's chosen mode. Otherwise preserve the
   selected sandbox and an approval path for protected Git writes. `workspace-write` with
   approvals set to `never` can edit source yet fail to commit, including in linked worktrees;
   `--add-dir` alone is not a general fix for protected Git metadata.

   If startup is blocked, inspect `herdr agent get <role-name>` and
   `herdr agent read <role-name> --source recent-unwrapped --lines 120` before handling the
   prompt under the user's trust and permission choices. Assign the first unit using step 4's
   context rule, then prompt the ready agent with
   `herdr agent prompt <role-name> "Read <card> and do <unit> in your role."`.
   Label its tab with `herdr tab rename <tab-id> "<run>"`. Done when every role is `working`
   or has acknowledged its role.
4. **Route each unit.**
   Start each executor and reviewer on a unit in a fresh context. A newly started agent already
   has one. When a role changes units, send `/clear` for Claude Code or `/new` for Codex and Pi
   as a separate prompt. Wait for the reset to finish and use `herdr agent get <role-name>` to
   confirm that the role has returned to `idle` before sending the unit prompt. Codex drops a
   prompt sent while it still processes `/new`; a successful send does not confirm reset completion.
   Keep context for consecutive review and fix rounds on the same unit. If a shared role returns
   to an earlier unit, reset again. Every round-2-or-later prompt names the earlier handoff and
   review paths, so correctness does not depend on retained context. The card records each role's
   current unit; handoff and review files carry state.

   Start each handoff and review with a routing summary: unit, branch, commit range, check status,
   and paths to details. Put the review verdict first.

   1. The executor rebases its branch onto the card's current integration base and runs the
      project's checks in its worktree. It writes `<run dir>/handoff-<unit>.md`: branch, checked
      base and head commits, check commands and results, and open items. It ends with `HANDOFF <unit>`.
   2. The coordinator prompts the reviewer with the handoff path and the commit range, after
      the context reset if the reviewer starts a different unit.
   3. The reviewer writes `<run dir>/review-<unit>.md`: verdict `accept` or `fix`, findings,
      and the checks it ran.
   4. On `fix`, the coordinator sends the review path to the executor. The executor fixes and
      writes a new handoff. Use new filenames for subsequent rounds, such as `handoff-<unit>-r2.md`
      and `review-<unit>-r2.md`. Repeat within the round limit, then escalate.
   5. On `accept`, the coordinator confirms that the checked base is still the integration head,
      then merges within the card's boundaries, by fast-forward or merge commit as allowed.
      If the base has advanced, return the unit to its executor to rebase and rerun checks.
      The executor records `git range-diff <old-base>..<old-head> <new-base>..<new-head>` in its
      handoff. Keep acceptance if every entry is `=` and the executor resolved no conflicts.
      Request a new review only if the reviewed patch changed or the executor resolved conflicts.
      This integration review does not count against the fix-round limit.
      Send merge conflicts or post-merge failures to an executor or a one-shot subagent, with
      the failing command or output path. That worker resolves and checks the result; changes
      return through review. The coordinator runs no test suite in its own context. Record the
      integration result in the card before assigning the next unit.

   Keep the coordinator's context bounded. Read only routing summaries, verdict lines, and paths;
   send detailed findings, diffs, and check output to the assigned worker or reviewer by path.
   Count each assignment, received handoff or review, and stall diagnosis as a routing event.
   Update the card's current state and event count after each event. Keep log entries to one
   line per event. After eight events since taking over (an initial interval estimate, recorded
   in the card), hand over before routing another event:

   1. Checkpoint the current state in the card. Append older log entries to `<run dir>/events.md`,
      leaving a path and the latest event in the card.
   2. Start a fresh coordinator in a new pane using step 3's split and agent-start commands,
      with the current coordinator's model, native arguments, permission mode, and integration cwd.
      Wait for readiness and record the new pane and session in the card.
   3. Stop the old coordinator's watcher job if it is still running. Transfer the active coordinator
      and watcher ownership in the card, then send the new agent an explicit prompt:
      `Read <card> and resume as coordinator. Arm the watcher in your session, reconcile unhandled
      handoff and review files against the card, then continue routing.`
   4. Stop routing in the old session after delivering the resume prompt. Leave workers running
      and preserve the user's conversation in the old session. The new coordinator owns subsequent
      watcher re-arming and resets the event count. The file reconciliation covers events during
      the handover gap. If prompt delivery fails, restore the old ownership in the card and re-arm
      the old watcher.

   Messages carry file paths, not pasted reports. Peers may talk directly
   (`herdr agent prompt <peer> ...`) to settle a question; whoever ends the exchange writes the
   conclusion into the unit's handoff or review file. Check `herdr agent get <peer>` first,
   and do not wait on a peer that is itself waiting. After a stalled submission or timeout,
   inspect the role before retrying; a failed wait does not prove the prompt was not delivered.

   Measure the run with `scripts/crew-ledger.py` (Python 3.9+, standard library only).
   Put a roles spec in `<run dir>/roles.txt`, one `NAME TOOL SELECTOR` per line; use shell quoting
   for paths with spaces and `#` for comments. Tools are `claude`, `codex`, and `pi`. Select by `session=ID`
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
   `scripts/crew-watch.sh <run dir> --roles <run dir>/roles.txt <role-name>...`.
   Herdr role names select active panes; the ledger spec also covers previous coordinators.
   The watcher polls every 30 seconds and exits quietly when the run directory is gone.
   It exits with a Herdr notification when a new `handoff-*.md` or `review-*.md` lands,
   a role is `blocked`, or every role has been idle for 30 minutes. Re-arm after those events.
   Keep scratch files in a subdirectory.

   With `--roles`, it also notifies when equivalent input exceeds 1M in a trailing 600-second
   window with no top-level handoff or review file update. These are initial threshold estimates
   from history, not proof of wasted work. Set `CREW_BURN_THRESHOLD` and
   `CREW_BURN_WINDOW_SECONDS` from the run's measured pace and record overrides in the card.
   A burn notification leaves agents and the watcher running; the watcher limits repeats to once per
   window. Diagnose the leading roles before changing the plan. Ledger errors
   appear on stderr and suppress that burn check; the existing events keep working.
   Omitting `--roles` keeps file/status watching alone. For historical diagnosis, run
   `scripts/crew-burn.py --roles <roles-file> --run-dir <run-dir> --until <ISO-timestamp>`;
   it prints only an eligible alert, using current artifact mtimes.
   Read a pane only to diagnose a stall. Done when every unit is accepted and integrated, or escalated.
5. **Debrief the user** only at an escalation and at the finish line, using
   [common-ground's "Hand the understanding back"](../common-ground/SKILL.md#hand-the-understanding-back).
   Link the card and unit files for detail. Done when the user can decide from that message.
6. **Wind down.** Tell each role there is no further work and ask for a last handoff with a
   Lessons section. Close the panes and worktrees this run created once their work is
   integrated or recorded; never close panes the run did not create. Done when the card records
   the outcome and nothing the run started is left running.

## Use a different skill when

- Which version of the work to do is still open: `ambition`; what it is for and where it ends:
  `common-ground`. Crew starts from a brief.
- One opinion from another model, with no pane that works on the task: `confer`.
- GPT stages inside a Claude Code Workflow whose results come back into this session:
  `gpt-workflow`. A crew lane lead may run it on its own queue.
