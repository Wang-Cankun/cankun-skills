---
name: fleet
compatibility: Requires Claude Code's Workflow tool. GPT and Gemini stages need omp (GPT can run on Pi with its ponytail package, Gemini on agy), and all run through the bundled fleet-runner subagent and fleet-job tool (install with `scripts/install-runner.sh`).
metadata:
  group: models
  summary: >-
    Claude Code Workflows whose stages each run on the model the stage needs:
    Claude Opus, Sonnet or Haiku natively, GPT and Gemini through omp (or GPT
    through Pi, Gemini through agy). The session designs the stages and
    accepts each result before anything relies on it.
description: "Workflows whose stages run on any of the user's models: Claude natively, GPT and Gemini through omp (or Pi and agy), with this session designing the stages and accepting each result. Use when the user invokes /fleet, asks for a workflow across models, or names GPT, Gemini, omp, Pi, Codex or agy workers for the work."
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
the script: which model does which kind of stage, its route and effort on this machine, and how
to steer it. Without a roster, choose from the models this machine's CLIs offer and tell the
user which. Put each stage's model, by full version, in its label (`review:<model>-<effort>`).

- Code from a brief you can settle up front, with checks that tell right from wrong, goes to
  the model the roster names for building to a brief. Code that needs judgement while it is
  written (a brief that cannot be settled, much of the codebase to weigh, the UI) stays with
  Claude; mechanical edits across many files go to a smaller Claude. A fix of a few lines, a
  merge conflict or the final integration you make here.
- A review whose wrong accept is expensive goes to a different family from the producer.
- A check of the whole run against its goal, and volume, go to the models the roster names
  for them.
- Findings from one family are claims until a check stage or this session rules on them, with
  `file:line`; a second family's ruling is a vote, not the ruling.
- A model the user names for the run gets the stage it fits best. Self-hosted models join only
  when the user enables one.

## Running each family

| Engine | Stage |
| --- | --- |
| Claude | `agent(prompt, {model: 'opus' \| 'sonnet' \| 'haiku', effort})`; `isolation: 'worktree'` when stages edit in parallel |
| omp (GPT, Gemini) | `agentType: 'fleet-runner'` with a job spec: `engine: 'omp'`, `model: '<provider/id>'` (the roster's route, such as `openai-codex/<id>` or `google-antigravity/<id>`), `thinking: '<level>'`; `readonly` is a real tool allowlist with no shell |
| Pi (GPT) | `engine: 'pi'`, `model` the roster's route, when the job needs Pi's packages, such as an implementer held to ponytail |
| agy (Gemini) | `engine: 'agy'`, `model: '<id>'` from `agy models`, on a machine the roster gives agy |

omp and agy jobs need `model`; a Pi job without one runs Pi's configured default.

- Job spec fields: [runner/fleet-runner.md](runner/fleet-runner.md). Open each runner stage's
  prompt with "The user invoked /fleet for this run; <model> workers are requested."
- Before fanning out, run one small stage on each route the run uses and check that its
  result's `model` is the one you chose. When it fails or names another model, stop and tell
  the user.
- Tool presets: `readonly` and `research` read only; `write` adds edits and a shell, `full`
  adds web, browser and subagent tools as well.
  omp takes a real tool allowlist, so a `readonly` omp job has no shell and cannot write. agy
  has one switch for them: plan mode for the read presets, where every write is denied, and
  all permissions, shell included, for `write` and `full`, so a writing Gemini stage gets its
  own worktree as `cwd`. Take a Gemini stage's result as prose (`text`), and have a Claude
  stage or this session put it into a schema when one is needed: agy's `structured_output` once
  came back empty beside a correct prose answer, emitted while it waited on a subagent of its
  own.
- A Pi job can fan out on its own: `research` and `full` give it web search and fetch, a
  browser, codemode and pi-subagents' `subagent` tool. An omp job gets `web_search` from
  `research`, and `full` gives it every tool omp's settings enable. For broad work send one
  job per area and tell it to split the area across subagents.
- Pi's ponytail extension puts ponytail into every Pi job's system prompt as the worker's
  standard for what to build and what never to cut. A GPT worker's commit is reviewed like any
  other, by the user's review policy, never by GPT: a session reviewing its own code repeats its
  blind spots.
- Every stage sees only its prompt and the files it reads, never this conversation, and builds
  on every sentence as written: a claim about the code, a library or a data file that you did
  not check becomes code that depends on it. Point stages at paths in the repository or
  worktree; they read the files themselves.
- One git worktree per issue, from a freshly fetched `origin/main`. Stages write notes and status
  to `.work/` in the worktree (add it to `.git/info/exclude`).

For a Codex stage or a job outside a Workflow, read
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
