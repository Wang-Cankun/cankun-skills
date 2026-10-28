# Model notes

How to seat each model family in a crew, what to give it and what to watch for. Tendencies
change with versions, so each note carries the month it was observed. When a model behaves
otherwise, write the observation in the run's card, and bring the lasting ones to the user to
record here.

| Family | Seat | Reads files | Strongest at |
| --- | --- | --- | --- |
| Claude | `--kind claude`; model and effort as native args (`--model opus --effort xhigh`) | yes | building, and the review the project's rules give Claude |
| GPT-6.1 Sol | `--kind pi` on Pi's default model | yes | a second review, beside the project's own, of a unit whose wrong accept would cost most; a sharp voice at a table |
| GPT-6 Luna | `--kind pi -- --model <Luna's id on the provider of Pi's default model>` (`pi --list-models`) | yes | volume where cost and wall time count: eval runs, simulated users, bulk checks |
| Gemini (Argon) | `--kind agy -- --model <id from agy models> --dangerously-skip-permissions` when the user allows it | yes | the whole run against its goal: drift, gaps between parts |

## Claude

- Confirm both the model and the effort on the status line; a pane started without them runs
  the CLI's defaults.

## GPT, 2026-10

- The user's GPT is a ChatGPT education subscription, with no GPT Pro: Sol and Luna only. A
  deep one-shot opinion goes to Sol through `confer`'s Pi route.
- Luna is the fast, cheaper tier below Sol. The user prefers it where cost and wall time count
  and Sol where judgement does.
- Sol is strict to a fault: it tends to propose more gates and tests than the change needs.
  Ask for findings ranked by severity, each naming the invariant it breaks; weigh each extra
  gate or test against the cost it adds before taking it.
- Sol is at its best with the diff, the design and the unit's acceptance; its findings come
  with concrete failing inputs, which makes them quick to check.
- Pi's default model is Sol on the user's subscription route; name Luna on that same provider.
  A GPT id on another provider can bill elsewhere or be refused at the first prompt.

## Codex

- To commit in a worktree it needs a permission mode that allows Git metadata writes; when the
  user has authorized it, start with `--cd "<worktree>" --dangerously-bypass-approvals-and-sandbox`.
  `workspace-write` with approvals `never` can edit source yet fail to commit.
- `/new` may open a "where should the new conversation run" picker and drops a prompt sent while
  it is still resetting. After `/new` or `/clear`, wait until `herdr agent get <name>` shows
  `idle` before the next prompt.

## Gemini (Argon), 2026-10

- Sees the big picture well, and it hallucinates and is overconfident. Ask for `file:line` with
  every claim and check each one; expect to reject a good share.
- Give it the whole rather than a unit: the goal and rules, the rendered prompt and tool
  definitions beside the code, and ask broadly and openly.
- In agy's print mode, `--mode plan` has no effect together with `--disable-slash-commands`.
