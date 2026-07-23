# Provider adapters

`scripts/confer.sh` owns all provider mechanics. This file documents how each adapter works and how to add one.

## Session mechanics (verified 2026-07-23)

| Provider | New thread | Resume | Session id source | Version tested |
|---|---|---|---|---|
| claude | `claude -p --output-format json -- "<prompt>"` | `claude -p --resume <id> --output-format json -- "<prompt>"` | `.session_id` in the JSON result | Claude Code 2.1.218 |
| codex | `codex exec --json --sandbox read-only --output-last-message <f> -- "<prompt>"` | `codex exec resume <id> --output-last-message <f> -- "<prompt>"` | first `thread_id`/`session_id` in `--json` event stream | codex-cli 0.145.0 |

Caveats:

- **codex flag placement** differs across versions (exec-level vs resume-subcommand-level); the adapter tries subcommand-level first, then falls back. If both fail after a codex upgrade, run `doctor --live` and fix the one call site in `ask_codex`.
- **claude read-only**: print mode cannot interactively approve permissions, so write tools fail closed — that is the intended consultant posture. Do not add `--dangerously-skip-permissions`.
- Extra per-provider flags: `CONFER_CLAUDE_ARGS` / `CONFER_CODEX_ARGS` env vars (e.g. model pins).

## State

- Registry `~/.confer/threads.json`: `{name: {provider, session, rounds, created, updated}}`
- Transcripts `~/.confer/threads/<name>.md`: every round, both directions, timestamped. Plaintext — the reason for the no-secrets guardrail.

## Adding a provider

1. Write `ask_<name>() { # prompt [session] ... }` in `confer.sh`: print the reply to stdout, set `$SESSION` to the provider-side session/thread id (empty string = thread not resumable, a warning not an error).
2. Add the name to the `PROVIDERS` array.
3. Verify with `doctor --live` (does a real open + resume per provider).

Candidate stub — **pi** (owner has mentioned it; identity and CLI unconfirmed): do not add until its non-interactive invocation and resume story are verified against a real install.
