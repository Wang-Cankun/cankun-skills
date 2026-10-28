---
name: crew
compatibility: Requires Herdr (run from inside a Herdr pane, HERDR_ENV=1) and the CLIs of the chosen models (Claude Code, Pi, Codex, agy); python3 for the optional ledger and watcher.
metadata:
  group: models
  personal: true
  summary: >-
    Resident agents of any model family in Herdr panes, orchestrated by the
    session that opens them: general rules for sizing, routing and accepting
    work, and how to seat each model.
description: "Run resident agents of any model family in Herdr panes, with this session as coordinator: it chooses how many agents, which models and how work and review flow, from general rules and the user's model roster. Use when the user invokes /crew or asks for side agents, several models working or discussing together, or a coordinator in Herdr."
---

# Crew

A crew is resident agents in Herdr panes: each keeps its context across turns, and the user
and other windows reach it by name. This session is the **coordinator**. It designs the crew for
the task in front of it and reshapes it as the work changes; this skill holds the rules every
crew keeps and how to seat each model, not a workflow.

**The user decides**: whether to open a crew; which models join, when the user names them; the
points the user settles personally; anything destructive, outward-facing, or costly beyond what
the card allows. Invoking this skill authorizes opening the panes the card lists.

## Rules for any crew

- **Earn the seat.** A resident agent joins when it brings what the coordinator lacks: a context
  to hold for later, a different model's eye, or work that runs in parallel on separate files.
  Work that needs none of these stays in this session or goes to a subagent or Workflow. Start
  from the smallest crew that covers the need; the coordinator can hold a seat itself, as the
  builder beside an outside reviewer or as one voice at a table. A model the user names gets
  the job it fits best; when none fits, say so before seating it.
- **One coordinator.** It holds the goal and finish line, assigns work, accepts results and
  merges. It keeps the card at `.work/crew/<run>/card.md`, with `.work/` in `.git/info/exclude`
  unless the repository already ignores it: goal and finish line, its own pane, each agent's
  name, model, pane and worktree, who may commit, merge or push, the budget and round cap when
  they matter, and what goes to the user. Show the card before starting unless the user already
  said go, and update it whenever the crew changes.
- **Independent lanes.** Parallel lanes touch separate files; an agent that edits works in its
  own worktree and branch. The coordinator orders dependent work and says which lane waits.
  Worktrees still share the machine: the card gives each lane its own ports or a turn at a
  shared service or heavy test run, and an agent kills only processes it started, by PID.
- **Families for judgement.** Seat a different model family where a shared blind spot costs
  most: a design, the review of a unit whose wrong accept is expensive, a check of the whole
  run against its goal. Throughput work goes to the model the project's rules name.
- **Evidence over reports.** A result counts when the coordinator can see it: a commit, a file,
  a finished check's log. Another family's findings are claims: check each against the code or
  source and record the ruling beside it before another agent acts on it.
- **Paths, not pastes.** Every model works on the repository or worktree itself; a copy of the
  material is only for a model that cannot read it, since copies go stale and hide the rest.
  Messages carry file paths. An answer longer than a few lines goes to a
  file the reply names. Residents write at full length; a length limit belongs only to an
  Agent-tool subagent, whose return lands in your own context.
- **Arm a wait.** A resident never messages back. After each prompt whose answer you need, arm a
  wait that notifies you: the prompt with `--wait` in the background, or a background loop until
  the expected file exists and `herdr agent get` shows `idle` or `done`. Tell the user you are
  waiting on it.
- **Address by roster.** Reach an agent by a name or pane that `herdr agent list` or the card
  shows; when they leave the target open, ask the user.
- **Fresh context when it pays.** Compact or reset an agent whose context has grown large or
  whose next work is unrelated. A coordinator whose own context is filling hands over through
  the card: it records there what is in flight and which waits are armed, stops its own
  watchers, and the fresh session starts from the card and re-arms them.
- **The user at decisions.** Bring each decision when it arises, with the options and a
  recommendation; report progress at milestones, quietly otherwise.
- **Close what you opened** once its work is merged or recorded. Side agents stay until the user
  retires them.

Shapes that have worked, to combine or change as the work goes:

- a side agent holding a context (a branch, a design) for other windows, listed with its as-of
  in the served repository's `.work/crew/residents.md`;
- a table of families on one versioned document, each answering `AGREE` or `DISAGREE` with
  reasons, positions attributed in `thread.md` and the user's settled points kept apart. It
  ends when all agree, handing the understanding back as `common-ground` does, or at the card's
  round cap, bringing the user each standing disagreement;
- an executor and a reviewer from another family, trading `handoff-<unit>.md` and
  `review-<unit>.md` (`accept` or `fix`; later rounds `-r2`);
- parallel lanes under one coordinator, each landing its own units ([how lanes ran](references/seating.md#lanes)).

## Models

Before choosing models, read the user's model roster (`~/.codex/agent-notes/models.md`, when
present): which model does what, what to give it and what to watch for. Name each model by its
full version (GPT-6.1 Sol, Gemini 4 Argon) on the card. When the project's rules name who works
and who reviews, they decide. To start each one in a pane: [references/seating.md](references/seating.md).

## Herdr

Check `test "${HERDR_ENV:-}" = 1`. `herdr --help` and its group help are the syntax authority;
the `herdr` skill covers pane mechanics.

```bash
herdr pane split --pane <source-pane> --direction right --cwd "<cwd>" --no-focus
herdr agent start <name> --kind <kind> --pane <pane-id> -- <native-args...>
herdr worktree create --cwd "<repo>" --branch "<branch>" --base "<base>" --label "<name>" --no-focus
herdr agent prompt <name> "<prompt>" --wait --timeout <ms>
herdr agent read <name> --source recent-unwrapped --lines <n>
```

Any kind `herdr agent start --help` lists can sit in a crew. Name agents for what they hold
(`side-provenance`, `table-gpt`); the name is how other windows find them. Pass the user's
launch preferences after `--`, and confirm the model on the agent's status line at startup,
since the kind alone selects no model. A new folder may open a trust dialog: read the pane and
answer it under the user's trust choices before the first prompt. Prime a side agent with what
it holds and have it confirm what it read and its as-of (a commit, plus "uncommitted changes"
when the tree is dirty). To see cost and progress, use the optional ledger and watcher in
[references/observe.md](references/observe.md).

## Use a different skill when

- The brief is settled and units have checks: `fleet`, a Workflow whose stages run on any of
  the roster's models.
- One opinion from another model, with no resident agent: `confer`.
- Which version of the work to do: `ambition`; what it is for and where it ends: `common-ground`.
