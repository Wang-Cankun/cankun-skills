# Other routes

Read when a GPT stage runs on a route other than Pi's default model, as a Codex stage, or
outside a Workflow.

## Routes

- `magpie/codex/<model>`: the ChatGPT subscription through magpie, on a machine whose Pi has the
  magpie provider. `scripts/preflight.sh <route>` reports which account served a test request. On a machine that
  runs a batch, keep any login that must not serve the run turned off in magpie: while it is on,
  one 503 from the intended account moves new sessions to it for the rest of the session. After
  the batch, count `providerAccount` in `~/.config/magpie/usage.jsonl` over the batch window.
- `magpie/claude/<model>`: the user's Claude subscription through magpie, for example as the
  model under test in an evaluation. It reports cache reads and writes.
- A Codex CLI sign-in to the same account can invalidate Pi's or magpie's token (401).
- **Codex stage**: run `codex-companion.mjs task --background` (read-only unless editing),
  confirm the job ID with `status`, poll `status <id> --wait --timeout-ms 540000`, and save
  `result <id>` to a file.
- Outside a Workflow, start a job with `~/.claude/tools/fleet-job/fleet_job.py start --spec <file>`.
