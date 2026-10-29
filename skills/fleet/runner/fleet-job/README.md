# fleet-job

Run Pi (GPT) or agy (Gemini) as a background worker from Claude Code (main session or a
Workflow stage) and collect a reliable result. Both exit 0 when the model call fails, so success
is judged from their JSON output, not the exit code: Pi's event stream, agy's final object
(`status`, `response`, `structured_output`, `denied_actions`).

## Files

- `fleet_job.py`: `start`, `wait`, `result`, `status`, `cancel`, `list` (see `--help`).
  `test_fleet_job.py` pins each engine's invocation against fake CLIs.
- `submit_result.ts`: Pi extension loaded automatically when a job has a `schema`. It
  registers `submit_result` with that JSON Schema as its parameters, so Pi validates the
  submission and returns errors for a retry. If the run completes without a submission it
  appends a reminder and continues, at most twice.
- `~/.claude/agents/fleet-runner.md`: thin Workflow stage that runs one job via this script.
- Jobs: `~/.claude/fleet-jobs/<job-id>/` (`spec.json`, `prompt.md`, `events.jsonl`,
  `stderr.log`, `state.json`, `result.json`, `session/`). Override with `FLEET_JOB_HOME`.

## Use

```bash
J=~/.claude/tools/fleet-job/fleet_job.py
$J start --name review-01 --thinking xhigh \
   --tools readonly --cwd ~/repo --prompt-file prompt.md --schema-file schema.json
$J start --name whole-run --engine agy --model gemini-4-argon-high \
   --tools readonly --cwd ~/repo --prompt-file prompt.md
$J wait <job_id> --timeout 540   # exit 0 finished, 3 still running
$J result <job_id>               # full JSON; --text or --structured for one field
$J result <job_id> --outcome     # only status, error and the output path
```

Statuses: `completed`, `no_result` (schema given but nothing submitted, or no text and no
structured result at all; agy's `denied_actions` stay in the result), `failed` (non-zero exit,
no `agent_settled`, or final `stopReason` error/aborted), `cancelled`, `timeout`
(`max_minutes`, default 60).

Two spec fields make `fleet-job` write what a stage must keep, so no one copies it by hand:

- `output`: a file path, relative to `cwd`. When the job ends, whatever its status, the tool
  writes the outcome there (atomically, parent directories created) and `result` reports the
  path as `output`. `completed` with a schema: `structured` as indented JSON. `completed`
  without one: `text` as it is. Any other status: `{"status", "error"}` as JSON for a schema
  job, or the lines `status: ...` and `error: ...` for a text job. `--output` sets it from the
  command line.
- `diff`: `{"base": "<ref>", "dir": "<path>", "parts": {"<file>": ["<pathspec>", ...]}}`
  (`parts` optional; `dir` relative to `cwd`). Before the engine runs, `start` writes
  `<dir>/stat.txt` and `<dir>/full.diff` from `git diff <base>...HEAD`, and `<dir>/<file>` for
  each part, limited to its pathspecs. Writes are atomic, so jobs that share a `dir` are safe.
  If git fails (unknown ref, `cwd` outside a repository), `start` exits non-zero with git's
  error and no job starts.

Tool presets: `readonly` (read, grep, find, ls), `research` (plus `web_search`,
`fetch_content`, `get_search_content` from pi-web-access, `agent_browser`, `codemode`, and
`subagent`, `subagent_supervisor`, `bg_wait` from pi-subagents), `write` (plus edit, write, bash),
`full` (write plus everything `research` adds). A tool an extension registers is
available only when the preset or list names it. Tools are an allowlist, not a sandbox: `bash` can write anywhere, so
give write-capable jobs a worktree as `cwd`. Installed Pi packages load normally.
`--model` is optional: without it Pi uses its configured default, and `result` reports the
model that actually answered; agy defaults to `gemini-4-argon-high`. Run Claude models as
native Claude Code agents instead.

agy takes a preset, not a tool list: `readonly` and `research` run in plan mode, where every
write is denied; `write` and `full` skip permissions, shell included, so give those a worktree.
A read-only agy prompt gets a closing paragraph saying so: a shell or write attempt ends the
job with no answer. `thinking` becomes agy's `--effort`. Pi-only fields (`append_system_prompt`, `extensions`,
`no_extensions`, `approve`) are refused for agy. Its conversation id is the result's
`session_id`; continue it with `agy --conversation <id>`. agy reports tokens but no cost.

Pi sessions are kept under the job directory; continue one interactively with
`pi --session <session_file>`.

## Notes

- `pi -p` waits for stdin when it is not a TTY; the supervisor gives it `/dev/null`.
  Close stdin yourself if you run `pi -p` directly.
- A continuation from `agent_before_settle` works after a completed run even though
  `context.canContinue` reports false before the reminder entry is appended.
