# Seating

How to start each model in a Herdr pane, keep its context fresh, and how lanes ran. Which model
sits where, by which CLI and route on this machine, and at what effort is the user's model roster
(`~/.codex/agent-notes/models.md`, when present); name every model by its full version, since a
note about one version can be false of the next.

| CLI | Seat |
| --- | --- |
| claude | `--kind claude -- --model <alias> --effort <level>` (aliases `opus`, `sonnet`, `haiku`; a full id only where the roster says an alias resolves wrongly) |
| omp | `--kind omp -- --model <provider/id> --thinking <level>`, with the roster's route (`openai-codex/<id>`, `google-antigravity/<id>`) |
| pi | `--kind pi -- --provider <provider> --model <id> --thinking <level>`, splitting the roster's route for this machine at its first `/` (`openai-codex/<id>` is `--provider openai-codex --model <id>`) |
| agy | `--kind agy -- --model <model> --dangerously-skip-permissions` |
| codex | `--kind codex`; see below |

Pi reads a `provider/id` model as a hint and can fall back to another provider that lists the
same id, so a GPT seat names its provider apart. A GPT id on a route the roster does not give
this machine can bill elsewhere or be refused at the first prompt. Self-hosted models join only
when the user enables one for the task.

To compact a resident, send `herdr agent prompt <name> /compact --wait`; an agent cannot run a
slash command on itself. To reset one: `/clear` for Claude and agy, `/new` for Pi and omp,
`/new` or `/clear` for Codex.

## Claude

- Confirm both the model and the effort on the status line; a pane started without them runs
  the CLI's defaults.

## Codex

- To commit in a worktree it needs a permission mode that allows Git metadata writes; when the
  user has authorized it, start with `--cd "<worktree>" --dangerously-bypass-approvals-and-sandbox`.
  `workspace-write` with approvals `never` can edit source yet fail to commit.
- `/new` may open a "where should the new conversation run" picker and drops a prompt sent while
  it is still resetting. After `/new` or `/clear`, wait until `herdr agent get <name>` shows
  `idle` before the next prompt.

## Pi

- In a folder it has not seen, Pi asks whether to trust it; choose "Trust (this session only)".
- The worker's brief is a file in its working directory: goal, rules (commit locally, push or
  post only if told), done criteria, and a short status file to write when finished. Report
  from that status file.
- A prompt can stay in Pi's input box: `herdr agent prompt --wait` then fails with
  `agent_prompt_stalled`, and `herdr agent get` shows `idle`. Send
  `herdr agent send-keys <name> Enter`. A further `agent prompt` reaches Pi as a follow-up.

## agy

- `--dangerously-skip-permissions` lets it write files and run commands without asking: the
  card names what it may write, and an agy pane that edits code works in its own worktree like
  any other.

## Lanes

Lanes ran when the user wanted to watch or steer an issue batch; a batch with done criteria
and nobody watching went to `fleet`. The coordinator owned `main`, merges, deploys, pushes and
closing issues; each lane lead was Claude Code in its own worktree and ran `/fleet` on its
queue. A background watcher ([observe](observe.md)) woke the coordinator when a handoff
landed, a lead was blocked, or every lead had sat idle for 30 minutes.

- Two lanes per machine was the practical limit; a shared hotspot file (a UI's main component,
  a release writer) had one writer.
- A lead cost roughly 150k to 500k Claude tokens per issue on top of GPT (estimate), and was
  compacted between issues.
