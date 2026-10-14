# pi-job

Run Pi as a background worker from Claude Code (main session or a Workflow stage) and
collect a reliable result. Pi's JSON mode exits 0 even when the model call fails, so
success is judged from the event stream, not the exit code.

## Files

- `pi_job.py`: `start`, `wait`, `result`, `status`, `cancel`, `list` (see `--help`).
- `submit_result.ts`: Pi extension loaded automatically when a job has a `schema`. It
  registers `submit_result` with that JSON Schema as its parameters, so Pi validates the
  submission and returns errors for a retry. If the run completes without a submission it
  appends a reminder and continues, at most twice.
- `~/.claude/agents/pi-runner.md`: thin Workflow stage that runs one job via this script.
- Jobs: `~/.claude/pi-jobs/<job-id>/` (`spec.json`, `prompt.md`, `events.jsonl`,
  `stderr.log`, `state.json`, `result.json`, `session/`). Override with `PI_JOB_HOME`.

## Use

```bash
J=~/.claude/tools/pi-job/pi_job.py
$J start --name review-01 --model anthropic/claude-sonnet-5 --thinking medium \
   --tools readonly --cwd ~/repo --prompt-file prompt.md --schema-file schema.json
$J wait <job_id> --timeout 540   # exit 0 finished, 3 still running
$J result <job_id>               # full JSON; --text or --structured for one field
```

Statuses: `completed`, `no_result` (schema given but nothing submitted), `failed`
(non-zero exit, no `agent_settled`, or final `stopReason` error/aborted), `cancelled`,
`timeout` (`max_minutes`, default 60).

Tool presets: `readonly` (read, grep, find, ls), `research` (plus `web_search`,
`fetch_content`, `get_search_content` from pi-web-access), `write` (plus edit, write),
`full` (plus bash). Tools are an allowlist, not a sandbox: `bash` can write anywhere, so
give write-capable jobs a worktree as `cwd`. Installed Pi packages load normally.
`--model` is optional: without it Pi uses its configured default, and `result` reports the
model that actually answered. Use Pi workers for non-Claude models; run Claude models as
native Claude Code agents instead.

Sessions are kept under the job directory; continue one interactively with
`pi --session <session_file>`.

## Notes

- `pi -p` waits for stdin when it is not a TTY; the supervisor gives it `/dev/null`.
  Close stdin yourself if you run `pi -p` directly.
- A continuation from `agent_before_settle` works after a completed run even though
  `context.canContinue` reports false before the reminder entry is appended.
