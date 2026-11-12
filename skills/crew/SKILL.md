---
name: crew
compatibility: Requires Herdr's herdr-core (`hc`), run from a terminal it manages ($HC_TERMINAL_ID set), and the CLIs of the chosen models (Claude Code, Pi, Codex, omp, agy); python3 for the optional ledger and burn check.
metadata:
  group: models
  personal: true
  summary: >-
    Resident agents of any model family in Herdr terminals, orchestrated by the
    session that opens them: general rules for sizing, routing and accepting
    work, and how to seat each model.
description: "Run resident agents of any model family in Herdr terminals, with this session as coordinator: it chooses how many agents, which models and how work and review flow, from general rules and the user's model roster. Use when the user invokes /crew or asks for side agents, several models working or discussing together, or a coordinator in Herdr."
---

# Crew

A crew is resident agents in Herdr terminals (`hc`): each keeps its context across turns, and the
user and other windows reach it by name. This session is the **coordinator**. It designs the crew for
the task in front of it and reshapes it as the work changes; this skill holds the rules every
crew keeps and how to seat each model, not a workflow.

Read the user's crew preferences (`~/.codex/agent-notes/crew.md`, when present) before
designing the crew: they set the coordinator's role, the flow of each unit and the
review policy, and win over this skill where they differ.

**The user decides**: whether to open a crew; which models join, when the user names them; the
points the user settles personally; anything destructive, outward-facing, or costly beyond what
the card allows. Invoking this skill authorizes starting the agents the card lists.

## Rules for any crew

- **Earn the seat.** A resident agent joins when it brings what the coordinator lacks: a context
  to hold for later, a different model's eye, or work that runs in parallel on separate files.
  Work that needs none of these stays in this session or goes to a subagent or Workflow. Start
  from the smallest crew that covers the need; the coordinator can hold a seat itself, as the
  builder beside an outside reviewer or as one voice at a table. A model the user names gets
  the job it fits best; when none fits, say so before seating it.
- **One coordinator.** It holds the goal and finish line, assigns work, accepts results and
  merges. It keeps the card at `.work/crew/<run>/card.md`, with `.work/` in `.git/info/exclude`
  unless the repository already ignores it: goal and finish line, its own address (`$HC_TERMINAL_ID`, written out), each
  agent's name, model, address and worktree, who may commit, merge or push, the budget and round cap when
  they matter, and what goes to the user. Show the card before starting unless the user already
  said go, and update it whenever the crew changes.
- **Stop rules with a floor.** A lane's stop rule names a minimum sample and both a count and a
  rate (more than 3 failures and more than 3% after 30 calls), and the lane classifies each
  failure before counting it: a provider refusal, a malformed answer and a bug in its own
  checker call for different rulings. Rules without a floor stopped one lane three times, twice
  on a single failure or a bug in its own checker.
- **Independent lanes.** Parallel lanes touch separate files; an agent that edits works in its
  own worktree and branch. The coordinator orders dependent work and says which lane waits.
  Worktrees still share the machine: the card gives each lane its own ports or a turn at a
  shared service or heavy test run, and an agent kills only processes it started, by PID.
- **Families for judgement.** Seat a different model family where a shared blind spot costs
  most: a design, the review of a unit whose wrong accept is expensive, a check of the whole
  run against its goal. Throughput work goes to the model the project's rules name.
- **Evidence over reports.** A result counts when the coordinator can see it: a commit, a file,
  a finished check's log. Another family's findings are claims: check each against the code or
  source and record the ruling beside it before another agent acts on it. When the claims are
  many, have each carry `path:line`, check the quotes and numbers against those lines with a
  script, and read what it flags.
- **Paths, not pastes.** Every model works on the repository or worktree itself; a copy of the
  material is only for a model that cannot read it, since copies go stale and hide the rest.
  Messages carry file paths. An answer longer than a few lines goes to a
  file the reply names. Residents write at full length; a length limit belongs only to an
  Agent-tool subagent, whose return lands in your own context.
- **Report and wait.** Every brief ends with the report line, the coordinator's address written
  out (`hc send t3 "<result or blocker>"`), since a resident that expands `$HC_TERMINAL_ID`
  gets its own. A report arrives as the coordinator's next input, tagged `<hc from=...>`; it
  is a claim, and the file it names is the result. Between reports, `hc wait --children any`
  waits on the seats this session started and `hc wait <name>` on any other (an inherited seat,
  a side agent). A wait returns `reason: timeout` every 180 seconds by default: a check-in,
  where you run the burn check when the card sets a budget, then wait again. hc tells the parent
  when a child is blocked, errors or exits; read its screen then. Tell the user what you are
  waiting on.
- **Address by roster.** Reach an agent by a name or address that `hc ls` or the card shows;
  when they leave the target open, ask the user.
- **Fresh context when it pays.** Compact or reset an agent whose context has grown large or
  whose next work is unrelated. A coordinator whose own context is filling hands over through
  the card: it records there what is in flight, and the fresh session starts from the card.
  When that session runs in a new terminal, it sends each seat its new report line and waits on
  them by name, and only seats started with `--outlive-parent` survived the handover; a
  `/compact` or `/clear` in the same terminal keeps the address and the children.
- **The user at decisions.** Bring each decision when it arises, with the options and a
  recommendation; report progress at milestones, quietly otherwise, naming each running seat
  and each wait by what it does or waits for.
- **Close what you opened** once its work is merged or recorded (`hc kill <name>`, then
  `hc rm <name>`). Side agents stay until the user retires them. When the user stops a crew,
  cancel the seats that just started, let a seat near its end finish without new model calls, start nothing new, and record on the card, per seat,
  what finished, what was cancelled and what is left undone.

Shapes that have worked, to combine or change as the work goes:

- a side agent holding a context (a branch, a design) for other windows, listed with its as-of
  in the served repository's `.work/crew/residents.md`;
- a table of families on one versioned document, each answering `AGREE` or `DISAGREE` with
  reasons, positions attributed in `thread.md` and the user's settled points kept apart. It
  ends when all agree, handing the user the settled understanding and its evidence, or at the card's
  round cap, bringing the user each standing disagreement;
- two families reading the same material blind to each other, then the coordinator checking
  both readings' citations and merging them into an outline whose claims it settles, from which
  one of them writes;
- an executor and a reviewer from another family, trading `handoff-<unit>.md` and
  `review-<unit>.md` (`accept` or `fix`; later rounds `-r2`);
- parallel lanes under one coordinator, each landing its own units ([how lanes ran](references/seating.md#lanes)).

## Models

Before choosing models, read the user's model roster (`~/.codex/agent-notes/models.md`, when
present): which model does what, what to give it and what to watch for. Name each model by its
full version (GPT-6.1 Sol, Gemini 4 Argon) on the card. When the project's rules name who works
and who reviews, they decide. To start each one: [references/seating.md](references/seating.md).

## Herdr (hc)

`hc --skill` is the manual and `hc <command> --help` the syntax authority; `herdr-app --skill`
covers the window. Check `test -n "${HC_TERMINAL_ID:-}"` and record that address on the card.

```bash
git worktree add -b "<branch>" "<worktree>" "<base>"
hc run --bg --name <name> --cwd "<worktree>" [--outlive-parent] -- <cli> <launch args...>
hc wait <name>                # until it is idle; then read its status line
hc send <name> "<prompt>"
hc wait --children any        # or: hc wait <name>
hc read --lines <n> <name>    # --lines 0: the visible screen
hc kill <name>; hc rm <name>
```

A seat ends with the session that started it unless it has `--outlive-parent`: give that to a
side agent and to any seat that should outlive this session (a handover, a pause for the user).
hc starts the program directly, not through the shell, so the shell's functions and aliases do
not apply: pass the user's launch preferences (permission mode, model, effort) as arguments
([seating](references/seating.md)). Start the seat without its task, so it cannot run before you
check it: when `hc wait <name>` returns, read the screen. A new folder may show a trust dialog,
answered under the user's trust choices (`hc keys <name> down enter`); once the seat is idle,
confirm the model and effort on its status line, then send the first task. Read before
resending, since a failed send may still have arrived. hc reads
the status (idle, working, done, blocked, error) that Claude Code, Codex, Pi and omp report; for
a CLI that reports none, `hc wait <name>` waits for its exit, so rely on its report and its
screen. Name agents for what they hold (`side-provenance`, `table-gpt`); the name is how other
windows find them. Prime a side agent with what it holds and have it confirm what it read and
its as-of (a commit, plus "uncommitted changes" when the tree is dirty). For the user to watch a
seat: `herdr-app do terminal.peek --terminal <address>`, or `herdr-app do terminal.keep
--terminal <address>` to give it a tab. To
see cost and progress, use the optional ledger and burn check in
[references/observe.md](references/observe.md).

## Use a different skill when

- The brief is settled and units have checks: `fleet`, a Workflow whose stages run on any of
  the roster's models.
- One opinion from another model, with no resident agent: `confer`.
- A wider view of the task before choosing: `ambition`.
