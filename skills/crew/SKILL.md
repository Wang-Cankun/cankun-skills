---
name: crew
compatibility: Requires Herdr (run from inside a Herdr pane, HERDR_ENV=1) and the agent CLIs used by the chosen agents (Claude Code, Pi, Codex); python3 for the optional ledger and watcher. GPT Pro joins through the confer skill.
metadata:
  group: models
  personal: true
  summary: >-
    Resident agents in Herdr panes that the user and other windows reach by
    name: a side agent to consult, a table of models converging on a
    judgement, or an executor and reviewer pair to watch.
description: "Keep resident agents in Herdr panes that the user and other windows reach by name: a side agent to consult, a table of different models converging on a judgement, or an executor and reviewer pair the user wants to watch. Use when the user invokes /crew or asks for side agents, panes that discuss with each other, or a coordinator in Herdr."
---

# Crew

A crew is one or more **resident** agents: each keeps its own context across turns, and the
user and other windows reach it by name. That is what separates a crew from a delegated
workflow, whose stages start fresh and end once their result comes back.

Use the shape the user names, or the smallest that fits:

- **Side**: one resident agent to consult, or to serve other windows as a resource.
- **Table**: several models, usually from different families, converging on a judgement such
  as a design or a plan.
- **Team**: an executor and a reviewer from another model family, for building the user wants
  to watch or steer.

Invoking this skill authorizes opening the panes for that shape.

**The user decides**: whether to open a crew; the question a table works on and what counts as
converged; the points the user settles personally; which models sit at the table; when converged
work moves to delegated execution; and anything destructive or outward-facing.
**This skill holds**: pane mechanics, the records each shape keeps, and the defaults below.

## Open panes

Check `test "${HERDR_ENV:-}" = 1`. `herdr --help` and its group help are the syntax authority;
the `herdr` skill covers pane mechanics.

- A side agent or table participant: split a pane, then start the agent in it.

  ```bash
  herdr pane split --pane <source-pane> --direction right --cwd "<cwd>" --no-focus
  herdr agent start <name> --kind <claude|codex|pi> --pane <pane-id> -- <native-args...>
  ```

- A team executor: its own worktree and branch, which returns the lane's root pane.

  ```bash
  herdr worktree create --cwd "<repo>" --branch "<branch>" --base "<base>" --label "<name>" --no-focus
  ```

Pass the user's launch preferences after `--`. Agent kind alone does not select a model; confirm
the model on the agent's status line at startup. Name agents for what they hold
(`side-provenance`, `table-gpt`), because the name is how other windows find them. An agent
that edits files works in its own worktree, never in a checkout another session uses.

Startup and reset gotchas:

- A new folder may open a trust dialog; inspect `herdr agent read <name> --source recent-unwrapped
  --lines 40` and answer it under the user's trust choices.
- A Codex agent that must commit in a worktree needs a permission mode that allows Git metadata
  writes; when the user has authorized it, start with `--cd "<worktree>"
  --dangerously-bypass-approvals-and-sandbox`. `workspace-write` with approvals `never` can
  edit source yet fail to commit.
- Codex `/new` may open a "where should the new conversation run" picker, and drops a prompt
  sent while it is still resetting. After `/new` or `/clear`, wait until `herdr agent get <name>`
  shows `idle` before the next prompt.

## Side

Prime the agent with what it should hold (files, a branch, a design) and have it reply with a
one-line summary of what it read and its as-of: commit, plus "uncommitted changes" when the
working tree is dirty, or a date. Record it in the served
repository's `.work/crew/residents.md`: name, pane, model, what it holds, as-of.

Another window asks it:

```bash
herdr agent get <name>          # ask when idle or done; --wait can match a busy agent's current turn
herdr agent prompt <name> "<question>" --wait --timeout <ms>
herdr agent read <name> --source recent-unwrapped --lines <n>
```

The pane read includes the agent's tool output and status lines; for anything longer than a
few lines, ask the side agent to write the answer to a file and reply with the path. Each answer
states the as-of of the material it rests on, so the asker can judge staleness. Refresh a stale
side agent by prompting it to re-read what changed, or restart it. Answers are quiet: no
notification to the user unless the user asks for one.

## Table

Run the table from a directory Git ignores (`.work/crew/<topic>/`) holding:

- the question and what counts as converged, in the user's words;
- one versioned main document (`model.md`, then a new version per round);
- `thread.md`: each participant's position, attributed and in their own words;
- **Settled by the user**: the points the user has decided, kept apart from open points.

A coordinator (normally this session) drafts each version and prompts each participant with
its path. Each participant answers `AGREE` or `DISAGREE` with reasons. Keep disagreement visible
and attributed; consensus is reached only when every participant writes `AGREE`. A dispute that
evidence can settle may get a small, recorded experiment. A participant without file access,
such as GPT Pro through `confer`, gets the material inline, and its replies go into
`thread.md` verbatim.

Bring the user the points that need their judgement as they arise. At convergence, hand the
understanding back with
[common-ground's "Hand the understanding back"](../common-ground/SKILL.md#hand-the-understanding-back),
and offer the converged result as a brief for delegated execution.

## Team

Write a short card at `.work/crew/<run>/card.md`: goal and finish line, each agent's name,
model, pane and branch, who may commit, merge or push, and what goes to the user. Show it to the
user unless they already said to go.

1. The executor works on its branch, runs the project's checks in its worktree, and writes
   `handoff-<unit>.md`: branch, commits, checks and results, open items.
2. The coordinator gives the reviewer the handoff path and commit range. The reviewer reads the
   diff, runs the checks itself, and writes `review-<unit>.md` with a verdict `accept` or
   `fix` and its findings; later rounds use new filenames (`-r2`).
3. On `fix`, the executor gets the review path. On `accept`, the coordinator merges within the
   card's boundaries and sends any conflict or failing check back to the executor.

Messages carry file paths, not pasted reports. Agents keep their context; compact or reset one
when its context has grown large or its next unit is unrelated, as a judgement call. To see cost
and progress, use the optional ledger and watcher in [references/observe.md](references/observe.md).

## Close

Close only panes and worktrees the crew opened, once their work is merged or recorded. Side
agents stay until the user retires them; then remove their line from `residents.md`.

## Use a different skill when

- The brief is settled and units have checks: delegate to a Claude Code Workflow, or to
  `gpt-workflow` for GPT producing stages.
- One opinion from another model, with no resident agent: `confer`.
- Which version of the work to do: `ambition`; what it is for and where it ends: `common-ground`.
