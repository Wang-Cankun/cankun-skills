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
   - current state: integration branch and head, each role's current unit, latest handoff and
     review paths, pending actions, and the coordinator reset interval from step 4.

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
   context reset, then prompt the ready agent with
   `herdr agent prompt <role-name> "Read <card> and do <unit> in your role."`.
   Label its tab with `herdr tab rename <tab-id> "<run>"`. Done when every role is `working`
   or has acknowledged its role.
4. **Route each unit.**
   Before an executor or reviewer starts a unit, the coordinator sends `/clear` for Claude Code,
   or `/new` for Codex and Pi, as a separate prompt. Wait until the role is ready, then send the
   unit prompt with the card and file paths. Apply this reset to the first unit too. Keep the
   same context for review and fix rounds on that unit. Handoff and review files carry state
   between units; the card records each role's current unit so a resumed coordinator knows
   whether a reset is due.

   1. The executor rebases its branch onto the card's current integration base and runs the
      project's checks in its worktree. It writes `<run dir>/handoff-<unit>.md`: branch, checked
      base and head commits, check commands and results, and open items. It ends with `HANDOFF <unit>`.
   2. The coordinator prompts the reviewer with the handoff path and the commit range, after
      the context reset if the reviewer starts a different unit.
   3. The reviewer writes `<run dir>/review-<unit>.md`: verdict `accept` or `fix`, findings,
      and the checks it ran. Put the verdict first. Start each handoff and review with a routing
      summary: unit, branch, commit range, check status, and paths to details.
   4. On `fix`, the coordinator sends the review path to the executor. The executor fixes and
      writes a new handoff. Use new filenames for subsequent rounds, such as `handoff-<unit>-r2.md`
      and `review-<unit>-r2.md`. Repeat within the round limit, then escalate.
   5. On `accept`, the coordinator confirms that the checked base is still the integration head,
      then merges within the card's boundaries. If the base has advanced, return the unit to its
      executor to rebase, rerun checks, and submit the new commit range for review before merging.
      Send merge conflicts or post-merge failures to an executor or a one-shot subagent, with
      the failing command or output path. That worker resolves and checks the result; changes
      return through review. The coordinator runs no test suite in its own context. Record the
      integration result in the card before assigning the next unit.

   Keep the coordinator's context bounded. Read only routing summaries, verdict lines, and paths;
   send detailed findings, diffs, and check output to the assigned worker or reviewer by path.
   Count each assignment, received handoff or review, and stall diagnosis as a routing event.
   Update the card's current state and event count after each event. After eight events since
   its last reset (an initial interval estimate, recorded in the card), the coordinator checkpoints
   the card and starts a fresh coordinator context before routing another event. Use `/clear`
   for Claude Code or `/new` for Codex and Pi, then resume from the card and reset the count.
   Leave workers and the watcher running during this handover.

   Messages carry file paths, not pasted reports. Peers may talk directly
   (`herdr agent prompt <peer> ...`) to settle a question; whoever ends the exchange writes the
   conclusion into the unit's handoff or review file. Check `herdr agent get <peer>` first,
   and do not wait on a peer that is itself waiting. After a stalled submission or timeout,
   inspect the role before retrying; a failed wait does not prove the prompt was not delivered.

   Watch with `scripts/crew-watch.sh <run dir> <role-name>...` in the background: it exits with
   a Herdr notification when a new `handoff-*.md` or `review-*.md` lands in the run directory
   (roles keep scratch files in a subdirectory), a role is `blocked`, or
   every role has been idle for 30 minutes. Re-arm it after handling each event. Read a pane
   only to diagnose a stall. Done when every unit is accepted and integrated, or escalated.
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
