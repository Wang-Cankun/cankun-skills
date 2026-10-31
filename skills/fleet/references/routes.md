# Other routes

Read when a stage runs as a Codex stage or a job runs outside a Workflow.

- A Codex CLI sign-in to the same account can invalidate Pi's token (401).
- **Codex stage**: run `codex-companion.mjs task --background` (read-only unless editing),
  confirm the job ID with `status`, poll `status <id> --wait --timeout-ms 540000`, and save
  `result <id>` to a file.
- Outside a Workflow, start a job with `~/.claude/tools/fleet-job/fleet_job.py start --spec <file>`.
