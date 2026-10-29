# Seating

How to start each model in a Herdr pane, keep its context fresh, and how lanes ran. Which model
does what, and what to watch for, is the user's model roster (`~/.codex/agent-notes/models.md`,
when present); name every model by its full version, since a note about one version can be
false of the next.

| Model | Seat |
| --- | --- |
| Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 | `--kind claude -- --model claude-opus-5-5 --effort xhigh` (or `claude-sonnet-5-5`, `claude-haiku-5-5`) |
| GPT-6.1 Sol, GPT-6 Luna | `--kind pi -- --provider <provider> --model <id> --thinking xhigh`, splitting the roster's route for this machine at its first `/` (`magpie/codex/gpt-6.1-sol` is `--provider magpie --model codex/gpt-6.1-sol`) |
| Gemini 4 Argon | `--kind omp -- --model google-antigravity/gemini-4-argon --thinking high` (or `medium`, `low`); on a machine without omp, `--kind agy -- --model gemini-4-argon-high --dangerously-skip-permissions` (or `-medium`, `-low`) |
| Codex | `--kind codex`; see below |

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

## omp

- Herdr does not see omp working (Herdr 0.9.5, omp 18.13.3): `herdr agent get` shows `idle`
  while the pane reads "Working…". `herdr agent prompt --wait` therefore fails with
  `agent_prompt_stalled` although omp took the prompt. Send without `--wait`, and wait on the
  file the prompt names, ending with a `DONE` line.

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
