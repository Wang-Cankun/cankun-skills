# fleet-job

Run omp, Pi (GPT) or agy (Gemini) as a background worker from Claude Code (main session or a
Workflow stage) and collect a reliable result. Pi and agy exit 0 when the model call fails, so
success is judged from their JSON output, not the exit code: the event stream of Pi and omp
(omp is a fork of Pi's coding agent and prints the same events), agy's final object (`status`,
`response`, `structured_output`, `denied_actions`).

## Files

- `fleet_job.py`: `start`, `wait`, `result`, `status`, `cancel`, `list` (see `--help`).
  `test_fleet_job.py` pins each engine's invocation against fake CLIs.
- `submit_result.ts`: extension loaded automatically into a Pi or omp job that has a `schema`.
  It registers `submit_result` with that JSON Schema as its parameters, so the engine validates
  the submission and returns errors for a retry. Under Pi, a run that completes without a
  submission gets a reminder and continues, at most twice; omp has no `agent_before_settle`
  event, so there a run that never submits ends `no_result`.
- `~/.claude/agents/fleet-runner.md`: thin Workflow stage that runs one job via this script.
- Jobs: `~/.claude/fleet-jobs/<job-id>/` (`spec.json`, `prompt.md`, `events.jsonl`,
  `stderr.log`, `state.json`, `result.json`, `session/`). Override with `FLEET_JOB_HOME`.

## Use

```bash
J=~/.claude/tools/fleet-job/fleet_job.py
$J start --name review-01 --thinking xhigh \
   --tools readonly --cwd ~/repo --prompt-file prompt.md --schema-file schema.json
$J start --name build-01 --engine omp --model openai-codex/gpt-6.1-sol --thinking xhigh \
   --tools write --cwd ~/repo-worktree --prompt-file prompt.md
$J start --name whole-run --engine agy --model gemini-4-argon-high \
   --tools readonly --cwd ~/repo --prompt-file prompt.md
$J wait <job_id> --timeout 540   # exit 0 finished, 3 still running
$J result <job_id>               # full JSON; --text or --structured for one field
$J result <job_id> --outcome     # only status, error and the output path
```

Statuses: `completed`, `no_result` (schema given but nothing submitted, or no text and no
structured result at all; agy's `denied_actions` stay in the result), `failed` (the engine did
not start, non-zero exit, no `agent_settled` (omp: no `agent_end`), final `stopReason`
error/aborted, or `output` could not be written), `cancelled`, `timeout` (`max_minutes`, default 60). Every status but
`completed` carries an `error`. A job is over only once its `result.json` exists: until then
`status` and `wait` report it `running`, so `output` is on disk when `wait` returns.

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
`--model` is optional for Pi: without it Pi uses its configured default, and `result` reports
the model that actually answered; agy defaults to `gemini-4-argon-high`. Run Claude models as
native Claude Code agents instead.

agy takes a preset, not a tool list: `readonly` and `research` run in plan mode, where every
write is denied; `write` and `full` skip permissions, shell included, so give those a worktree.
A read-only agy prompt gets a closing paragraph saying so: a shell or write attempt ends the
job with no answer. `thinking` becomes agy's `--effort`. Pi-only fields (`append_system_prompt`, `extensions`,
`no_extensions`, `approve`) are refused for agy. Its conversation id is the result's
`session_id`; continue it with `agy --conversation <id>`. agy reports tokens but no cost.

omp runs as `omp -p --mode json --session-dir <job dir>/session --no-skills --no-rules
--no-extensions --no-title --no-lsp --model <model> [--thinking <level>] [--tools <list>] --
<prompt>`, in the job's `cwd`, with stdin from `/dev/null`. Context files (`AGENTS.md` and the
like) stay on, as for Pi. Its presets are `readonly` (read, grep, find, glob), `research` (plus
`web_search`) and `write` (`readonly` plus edit, write, bash); `full` passes no `--tools`, so the
job gets every tool omp's settings enable. A list passes through; a tool that omp's settings
disable (`ast_grep` by default) makes omp refuse to start, and the job `failed` with that
message. `model` (`provider/id`) is required, because omp's configured default can be any
model. A job is `completed` when omp exits 0 after `agent_end` and the last assistant message
did not stop on an error or an abort; otherwise `failed`, with the message's `errorMessage` or
the tail of stderr. Usage is summed over the assistant messages. `append_system_prompt` and
`extensions` pass through; `no_extensions` and `approve` are refused.

Pi sessions are kept under the job directory; continue one interactively with
`pi --session <session_file>`.

## Notes

- `pi -p` and `omp -p` wait for stdin when it is not a TTY; the supervisor gives them
  `/dev/null`. Close stdin yourself if you run either directly.
- A continuation from `agent_before_settle` (Pi only) works after a completed run even though
  `context.canContinue` reports false before the reminder entry is appended.
