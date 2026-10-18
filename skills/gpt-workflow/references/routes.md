# Other routes and Herdr workers

Read when a GPT stage runs on a route other than Pi's default model, or when GPT workers run
in Herdr panes.

## Routes

- `magpie/codex/<model>`: the user's Codex subscription through magpie, when the user names it.
  `scripts/preflight.sh <route>` reports which account served a test request. On a machine that
  runs a batch, keep any login that must not serve the run turned off in magpie: while it is on,
  one 503 from the intended account moves new sessions to it for the rest of the session. After
  the batch, count `providerAccount` in `~/.config/magpie/usage.jsonl` over the batch window.
- `magpie/claude/<model>`: the user's Claude subscription through magpie, for example as the
  model under test in an evaluation. It reports cache reads and writes.
- A Codex CLI sign-in to the same account can invalidate Pi's or magpie's token (401).
- **Codex stage**: run `codex-companion.mjs task --background` (read-only unless editing),
  confirm the job ID with `status`, poll `status <id> --wait --timeout-ms 540000`, and save
  `result <id>` to a file.
- Outside a Workflow, start a Pi job with `pi_job.py start --spec <file>`.

## Herdr workers

Run a GPT worker in a Herdr pane when the user should watch or steer long, multi-step work;
keep Pi jobs and Workflow stages for results Claude needs back in the session. The `crew` skill
holds pane mechanics. GPT-specific facts:

- Start Pi with `--kind pi --pane <id> -- --thinking xhigh`. In a folder it has not seen, Pi
  asks whether to trust it; choose "Trust (this session only)".
- The worker's brief is a file in its working directory: goal, rules (commit locally, push or
  post only if told), how to get review (a second GPT job through `pi_job.py`), done criteria,
  and a short status file to write when finished. Report from that status file.
- When `herdr agent get` still shows `idle` after a prompt, the text sits in the input box: send
  `herdr agent send-keys <name> Enter`. A further `agent prompt` reaches Pi as a follow-up.

## Lanes

An issue batch with done criteria is delegated work; run lanes as resident panes only when the
user wants to watch or steer them, as a `crew` team. The coordinator owns `main`, merges,
deploys, pushes and closes issues; each lane lead is Claude Code in its own worktree and may
run `/gpt-workflow` on its queue.

- Two lanes per machine was the practical limit; give a shared hotspot file (a UI's main
  component, a release writer) one writer.
- A lead costs roughly 150k to 500k Claude tokens per issue on top of GPT (estimate). Between
  issues compact it with `herdr agent prompt <lead> /compact --wait`; a lead cannot run a slash
  command on itself.
