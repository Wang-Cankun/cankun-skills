# Seating

How to start each model in a Herdr pane, what a Pi worker there needs, and how lanes ran. Which model does what, and what to watch for, is the
user's model roster (`~/.codex/agent-notes/models.md`, when present); name every model by its
full version, since a note about one version can be false of the next.

| Model | Seat |
| --- | --- |
| Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 | `--kind claude -- --model claude-opus-5-5 --effort xhigh` (or `claude-sonnet-5-5`, `claude-haiku-5-5`) |
| GPT-6.1 Sol | `--kind pi`: Pi's default model on the user's machines |
| GPT-6 Luna | `--kind pi -- --model <route>/gpt-6-luna`, the route the roster gives this machine (`magpie/codex` or `openai-codex`) |
| Gemini 4 Argon | `--kind agy -- --model gemini-4-argon-high` (or `-medium`, `-low`); add `--dangerously-skip-permissions` for a pane that edits, in its own worktree, when the user allows it |
| Codex | `--kind codex`; see below |

A GPT id on a route the roster does not give this machine can bill elsewhere or be refused at
the first prompt. Self-hosted models join only when the user enables one for the task.

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

- Start Pi with `--kind pi --pane <id> -- --thinking xhigh`. In a folder it has not seen, Pi
  asks whether to trust it; choose "Trust (this session only)".
- The worker's brief is a file in its working directory: goal, rules (commit locally, push or
  post only if told), how to get review (a second GPT job through `fleet`'s job tool), done
  criteria, and a short status file to write when finished. Report from that status file.
- When `herdr agent get` still shows `idle` after a prompt, the text sits in the input box: send
  `herdr agent send-keys <name> Enter`. A further `agent prompt` reaches Pi as a follow-up.

## Lanes

An issue batch with done criteria is delegated work for `fleet`; run lanes as resident panes
only when the user wants to watch or steer them. The coordinator owns `main`, merges,
deploys, pushes and closes issues; each lane lead is Claude Code in its own worktree and may
run `/fleet` on its queue. `scripts/lane-watch.sh <handoff-dir> <lead>...`, run in the
background, wakes the coordinator when a handoff file appears, a lead is blocked, or every lead
has sat idle for 30 minutes.

- Two lanes per machine was the practical limit; give a shared hotspot file (a UI's main
  component, a release writer) one writer.
- A lead costs roughly 150k to 500k Claude tokens per issue on top of GPT (estimate). Between
  issues compact it with `herdr agent prompt <lead> /compact --wait`; a lead cannot run a slash
  command on itself.
