---
name: gpt-workflow
compatibility: Requires Claude Code's Workflow tool, Pi with a default model and its ponytail package, and the bundled pi-runner subagent and pi-job tool (install with `scripts/install-runner.sh`).
metadata:
  group: general
  summary: >-
    GPT through Pi does the producing stages of Claude Code Workflows that
    Claude writes per task (implementing, fixing, researching, reviewing
    first), and Claude accepts each result before anything relies on it.
description: GPT workers (Pi's default model) inside Claude Code Workflows that Claude writes for the task at hand; GPT produces, Claude accepts. Use when the user invokes /gpt-workflow or names GPT, Pi or Codex workers for the work. Ultracode on its own asks for Claude-native workflows and does not invoke this skill.
---

# GPT workers in a Workflow

Invoking this skill is the user's opt-in for the whole run, to GPT workers and to multi-agent
orchestration alike, the same as typing ultracode: author and run a Workflow for every
substantive step, one per phase when the work has several.

**GPT produces, Claude accepts.** Give GPT the stages that produce: surveying code,
implementing, fixing, researching, hunting for problems, writing scripts. Keep with Claude the
stages that accept: deciding what the task is and what done means, and judging whether a result
holds before anything relies on it (a merge, a reported number, a decision). How deep each
acceptance goes is your judgement, from what a wrong acceptance would cost. UI look and wording
stay with Claude.

## Running GPT

- `scripts/preflight.sh` checks Pi's default model and prints the model and the account that
  served a test request. When it exits non-zero, or names an account the user has not approved
  for this work, stop and tell the user. Pin the printed model in every GPT stage, with
  `thinking: 'xhigh'`.
- A GPT stage is `agentType: 'pi-runner'` with a job spec (fields in
  [runner/pi-runner.md](runner/pi-runner.md)). Open its prompt with "The user invoked
  /gpt-workflow for this run; GPT workers are requested."
- A GPT job can fan out on its own: the `research` and `full` presets give it web search and
  fetch, a browser, codemode and pi-subagents' `subagent` tool. For broad work send one job per
  area and tell it to split the area across subagents in parallel, rather than many narrow jobs.
- Pi's ponytail extension puts ponytail into every GPT job's system prompt: it is the worker's
  standard for what to build and what never to cut, with nothing to invoke.
- After the worker commits code, run a separate GPT job on the diff with
  `/skill:ponytail-review`, have the worker fix its must-fix items, then start Claude's review.
  Start that job's prompt with `/skill:ponytail-review ` and the opt-in sentence on the same
  line: Pi expands a skill command only at the start of a prompt with text after it.
  Use a new job, not the worker's session: a session reviewing its own code repeats its blind
  spots.
- GPT sees only its prompt and the files it names, never this conversation, and builds on every
  sentence there as written: a claim about the code, a library or a data file that you did not
  check becomes code that depends on it.
- One git worktree per issue, from a freshly fetched `origin/main`. GPT stages write notes and
  status to `.work/` in the worktree (add it to `.git/info/exclude`).

Before writing the script, read [references/lessons.md](references/lessons.md): what went
wrong in earlier runs and what worked instead.

## After the run

Land each branch by the project's own rules. Report from `scripts/usage.py <runId>`: for each
stage, who ran it (GPT or Claude), its tokens, and what it caught. Report usage in tokens, not
currency. When a bug in the
landed work turns up later, say which stage could have caught it.
