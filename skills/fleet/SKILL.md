---
name: fleet
compatibility: Requires Claude Code's Workflow tool. GPT stages need Pi with its ponytail package, Gemini stages need agy, and both run through the bundled fleet-runner subagent and fleet-job tool (install with `scripts/install-runner.sh`).
metadata:
  group: models
  summary: >-
    Claude Code Workflows whose stages each run on the model the stage needs:
    Claude Opus, Sonnet or Haiku natively, GPT through Pi, Gemini through agy.
    The session designs the stages and accepts each result before anything
    relies on it.
description: "Workflows whose stages run on any of the user's models: Claude natively, GPT through Pi and Gemini through agy, with this session designing the stages and accepting each result. Use when the user invokes /fleet, asks for a workflow across models, or names GPT, Gemini, Pi, Codex or agy workers for the work."
---

# Fleet

Invoking this skill is the user's opt-in for the whole run, to multi-agent orchestration and to
every model in the roster, as ultracode is for Claude-only workflows: author and run a Workflow
for every substantive step, one per phase when the work has several.

**Stages produce; this session accepts.** Give stages the work that produces: surveying code,
implementing, fixing, researching, hunting for problems, first reviews, drafting prose. Keep
here the work that accepts: what the task is and what done means, and whether a result holds
before anything relies on it (a merge, a reported number, a decision). How deep each acceptance
goes is your judgement, from what a wrong acceptance would cost. UI look stays with Claude.

Read the user's crew preferences (`~/.codex/agent-notes/crew.md`, when present) before
writing the script: they set the coordinator's role, the flow of each unit and the
review policy, and win over this skill where they differ.

## Choosing models

Read the user's model roster (`~/.codex/agent-notes/models.md`, when present) before writing
the script: which model does what, its route on this machine, and how to steer it. Put each
stage's model, by full version, in its label (`review:gemini-4-argon-high`).

- Code from a brief you can settle up front, with checks that tell right from wrong, suits
  GPT-6.1 Sol: it builds the brief as written. Code that needs judgement while it is written
  (a brief that cannot be settled, much of the codebase to weigh, the UI) suits Claude Opus 5.5
  or Sonnet 5.5; mechanical edits across many files suit Sonnet 5.5 or Haiku 5.5. A fix of a few
  lines, a merge conflict or the final integration you make here.
- A review whose wrong accept is expensive goes to a different family from the producer.
- A check of the whole run against its goal suits Gemini 4 Argon; volume suits GPT-6 Luna or
  Claude Haiku 5.5.
- Findings from one family are claims until a check stage or this session rules on them, with
  `file:line`; a second family's ruling is a vote, not the ruling.
- A model the user names for the run gets the stage it fits best. Self-hosted models join only
  when the user enables one.

## Running each family

| Model | Stage |
| --- | --- |
| Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 | `agent(prompt, {model: 'opus' \| 'sonnet' \| 'haiku', effort})`; `isolation: 'worktree'` when stages edit in parallel |
| GPT-6.1 Sol, GPT-6 Luna | `agentType: 'fleet-runner'` with a job spec: `engine: 'pi'`, `model` the roster's route for this machine, `thinking: 'xhigh'` |
| Gemini 4 Argon | `agentType: 'fleet-runner'` with `engine: 'agy'`, `model: 'gemini-4-argon-high'` (or `-medium`, `-low`) |

- Job spec fields: [runner/fleet-runner.md](runner/fleet-runner.md). Open each runner stage's
  prompt with "The user invoked /fleet for this run; <model> workers are requested."
- Before the run, `scripts/preflight.sh <route>` for each GPT or Gemini route it uses
  (`agy/gemini-4-argon-high` for Gemini) sends one tiny request; for GPT it prints the account
  that served it. When it exits non-zero, or names an account the user has not approved for
  this work, stop and tell the user. `FLEET_DENY_ACCOUNT` names an account that must never
  serve the run.
- Tool presets: `readonly` and `research` read only; `write` adds edits and a shell, `full`
  adds web, browser and subagent tools as well.
  agy has one switch for them: plan mode for the read presets, where every write is denied,
  and all permissions, shell included, for `write` and `full`, so a writing Gemini stage gets
  its own worktree as `cwd`. Take a Gemini stage's result as prose (`text`), and have a Claude
  stage or this session put it into a schema when one is needed: agy's `structured_output` once
  came back empty beside a correct prose answer, emitted while it waited on a subagent of its
  own.
- A GPT job can fan out on its own: `research` and `full` give it web search and fetch, a
  browser, codemode and pi-subagents' `subagent` tool. For broad work send one job per area and
  tell it to split the area across subagents.
- Pi's ponytail extension puts ponytail into every GPT job's system prompt as the worker's
  standard for what to build and what never to cut. After a GPT worker commits code, run a
  separate GPT job on the diff with `/skill:ponytail-review` (the prompt starts with
  `/skill:ponytail-review ` and the opt-in sentence on the same line: Pi expands a skill
  command only at the start of a prompt with text after it), have the worker fix its must-fix
  items, then accept. A session reviewing its own code repeats its blind spots.
- Every stage sees only its prompt and the files it reads, never this conversation, and builds
  on every sentence as written: a claim about the code, a library or a data file that you did
  not check becomes code that depends on it. Point stages at paths in the repository or
  worktree; they read the files themselves.
- One git worktree per issue, from a freshly fetched `origin/main`. Stages write notes and status
  to `.work/` in the worktree (add it to `.git/info/exclude`).

For a Codex stage, another magpie route or a job outside a Workflow, read
[references/routes.md](references/routes.md). Before writing the script, read
[references/lessons.md](references/lessons.md): what went wrong in earlier runs and what worked
instead.

## After the run

Land each branch by the project's own rules. Report from `scripts/usage.py <runId>`: for each
stage, its model, tokens, and what it caught. Report usage in tokens, not currency. When a bug
in the landed work turns up later, say which stage could have caught it.

## Use a different skill when

- The other models should stay resident, holding context across turns or under the user's
  eye in panes: `crew`.
- One opinion from another model, with no work handed over: `confer`.
