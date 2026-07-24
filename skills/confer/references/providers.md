# Provider adapters

`scripts/confer.mjs` (single-file bun, zero deps) owns all provider mechanics. `scripts/confer.sh`
is a compat shim (`exec confer.mjs "$@"`) kept one round post-cutover for agents holding the old
SKILL.md and for existing permission allowlists; new references should use `confer.mjs`.

**Harness-blind invariant**: the script contains no harness detection, no harness-specific env or
paths, plain-text IO only, and state independent of CWD. It serves Claude Code, Codex, pi, and any
future host from one deployment; harness differences are absorbed by SKILL.md (policy) and skl
(packaging). Any harness-conditional added to confer.mjs is a design regression.

## Session mechanics (verified 2026-07-23, live)

| Provider | New thread | Resume | Session id source | Version verified |
|---|---|---|---|---|
| claude | `claude -p --output-format json -- "<prompt>"` | `claude -p --resume <id> --output-format json -- "<prompt>"` | `.session_id` in the JSON result (refreshed every round) | Claude Code 2.1.218 |
| codex | `codex exec --sandbox read-only --skip-git-repo-check --json --output-last-message <f> -- "<prompt>"` | `codex exec --sandbox read-only --skip-git-repo-check resume <id> --json --output-last-message <f> -- "<prompt>"` | `thread_id` of the `{"type":"thread.started"}` JSONL event | codex-cli 0.145.0 |

Caveats (each verified against the real CLI, not assumed):

- **`--sandbox` is exec-level only** — `codex exec resume --help` has no `--sandbox`. There is one
  correct call form (above); the old two-position fallback was removed because a blind retry after a
  partial remote failure can double-send a prompt.
- **`--skip-git-repo-check` is required**: without it codex refuses to run from any non-git CWD
  ("Not inside a trusted directory") — harnesses invoke from arbitrary project dirs, and a read-only
  consultant must not depend on the caller's git state.
- **stdin must be ignored** when the prompt travels via argv — codex otherwise announces "Reading
  additional input from stdin..." and reads it. The runner spawns every CLI with `stdio: ignore` on stdin.
- **claude read-only**: print mode cannot interactively approve permissions, so write tools fail
  closed — the intended consultant posture. Do not add `--dangerously-skip-permissions`.
- Extra per-provider flags: `CONFER_CLAUDE_ARGS` / `CONFER_CODEX_ARGS` (whitespace-split; **no glob
  expansion**, unlike the old bash — args containing spaces remain unsupported).

## Runtime contract

- **Timeout**: every provider call gets `CONFER_TIMEOUT` seconds (default 300). On expiry the child's
  whole **process group** is SIGTERMed, then SIGKILLed after 2s — descendants included.
- **Exit codes**: `0` success; `1` error. `all` exits `0` if ≥1 provider succeeded (failures named on
  stderr), `1` only when every provider failed.
- **Locks** (`~/.confer/locks/`, `O_EXCL` files with `{pid, nonce, ts}`; dead-owner locks stolen once):
  - *Per-thread operation lock* — held by `open`/`reply` across the whole provider call. Contention
    fails fast (`thread busy (pid N)`): retry when the other round finishes. This is what prevents two
    concurrent replies from forking the peer-side session.
  - *Registry transaction lock* — held only across read-modify-write; writes go to a same-directory
    temp file then atomic rename.
- **Failed rounds**: the outbound `→` transcript block is written before the call. Success appends `←`
  and commits the registry (rounds counts **completed** rounds; a retry reuses the number). Failure
  appends `✗` with the error. A `→` with neither `←` nor `✗` means the process died mid-call: the peer
  context may be one round ahead of the registry — a documented ambiguity, not silently repaired.
- **Provenance** (best-effort, audit-oriented): each `←` header carries ` · <model> · <cost/tokens> ·
  <duration>` where available, e.g. `(2026-07-24 09:00 · claude-fable-5 · $0.36 · 12s)` or
  `(… · gpt-5.6-sol/xhigh · 23.7k→5tok)`; the registry keeps the last round's `model` (additive key).
  Sources: claude = `modelUsage` (dominant entry) + `total_cost_usd` (API-equivalent — notional on a
  subscription) + `duration_ms`; codex = `$CODEX_HOME/config.toml` `model`/`model_reasoning_effort`
  (`-m` / `-c model_reasoning_effort=` in `CONFER_CODEX_ARGS` take precedence) + `turn.completed`
  usage tokens — the codex event stream itself names no model. Missing fields degrade to a shorter
  header; rounds written before this feature keep the old format.

## State

- Registry `~/.confer/threads.json`: `{name: {provider, session, rounds, created, updated}}`
- Transcripts `~/.confer/threads/<name>.md`: every round, both directions, timestamped. Plaintext —
  the reason for the no-secrets guardrail.
- Thread names: `[A-Za-z0-9_-]+`, enforced on `open`/`reply`/`show`.
- Override the state root with `CONFER_HOME` (tests always do; never point tests at the real registry).

## Adding a provider

1. Add an entry to the `providers` object in `confer.mjs`:
   `async ask(prompt, session) -> {reply, session}`. Use `runOrThrow` for spawning (it supplies the
   timeout/process-group contract). Throw `ProviderError` on any failure; **an exit-0 response with no
   session id is a protocol error, not a warning** — resumable threads are the core contract. Add a
   capability flag only when a genuinely non-resumable provider actually exists.
2. Verify: `bun scripts/confer-test.mjs` (extend the fakes if the CLI shape is new), then
   `CONFER_HOME=$(mktemp -d) confer.mjs doctor --live`.

Candidate stub — **pi** (owner has mentioned it; identity and CLI unconfirmed): do not add until its
non-interactive invocation and resume story are verified against a real install.

## Tests

`bun scripts/confer-test.mjs` — deterministic, zero live calls: fake claude/codex CLIs on a prepended
PATH, fresh `CONFER_HOME` per case. Covers fan-out isolation, total-failure exit, process-tree timeout
kill (heartbeat grandchild), malformed JSON / missing session protocol errors, the concurrent
same-thread reply race, duplicate-name opens, name validation, and stale-lock stealing. Run it after
any edit; `doctor --live` (under a temp `CONFER_HOME`) anchors the adapters against the real CLIs.
