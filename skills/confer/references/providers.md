# Provider adapters

`scripts/confer.mjs` (single-file bun, zero deps) owns all provider mechanics.

**Harness-blind invariant**: the script contains no harness detection, no harness-specific env or
paths, plain-text IO only, and state independent of CWD. It serves Claude Code, Codex, pi, and any
future host from one deployment; harness differences are absorbed by SKILL.md (policy) and skl
(packaging). Any harness-conditional added to confer.mjs is a design regression.

## Session mechanics (verified 2026-07-28)

| Provider | New thread | Resume | Session id source | Version verified |
|---|---|---|---|---|
| claude | `claude -p --output-format json -- "<prompt>"` | `claude -p --resume <id> --output-format json -- "<prompt>"` | `.session_id` in the JSON result (refreshed every round) | Claude Code 2.1.218 |
| codex | `codex exec --sandbox read-only --skip-git-repo-check --json --output-last-message <f> -- "<prompt>"` | `codex exec --sandbox read-only --skip-git-repo-check resume <id> --json --output-last-message <f> -- "<prompt>"` | `thread_id` of the `{"type":"thread.started"}` JSONL event | codex-cli 0.145.0 |
| oracle | `oracle --engine browser --model gpt-5.6 --browser-thinking-time heavy --browser-timeout 60m --wait --no-notify --browser-archive never --write-output <f> --prompt "<prompt>"` | same flags plus `--followup <id>` | stdout `Session: <id>` (a new child id every round) | Oracle >= 0.16.2 required |

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
- **Oracle is explicit-only**: route to it only when the user explicitly asks for GPT Pro or Oracle.
  Bare `all` and bare `doctor --live` remain Claude + Codex; `all --with-oracle` and
  `doctor --live oracle` are the explicit forms. Do not infer this route from task difficulty.
- **Oracle's CLI model shape is deliberate**: GPT-5.6 Pro is
  `--model gpt-5.6 --browser-thinking-time heavy`, not a `gpt-5.6-pro` model id. Require Oracle
  >= 0.16.2 before submitting any prompt; older versions fail closed because their browser model
  picker does not reliably select this model.
- **Oracle followups fork child sessions**: pass the stored id with `--followup`, parse the single
  `Session: <id>` line, and replace the registry value with that new child id. A missing or
  conflicting id and a missing/empty `--write-output` file are protocol errors.
- **Oracle browser state is machine-local**: select the authenticated Chrome profile with
  `browser.chromeProfile` in `~/.oracle/config.json`. Never hardcode a profile, account, cookies, or
  credentials in this repository. `--wait`, `--no-notify`, and `--browser-archive never` keep output
  deterministic and avoid retained prompt archives.
- Extra per-provider flags: `CONFER_CLAUDE_ARGS` / `CONFER_CODEX_ARGS` / `CONFER_ORACLE_ARGS`
  (whitespace-split; **no glob
  expansion**, unlike the old bash — args containing spaces remain unsupported).

## Runtime contract

- **Timeout**: Claude and Codex calls get `CONFER_TIMEOUT` seconds (default 1200). Oracle gets
  `CONFER_ORACLE_TIMEOUT` seconds (default 3900) around a pinned 60-minute browser timeout. On expiry
  the child's whole **process group** is SIGTERMed, then SIGKILLed after 2s — descendants included.
- **Exit codes**: `0` success; `1` error. `all` exits `0` if ≥1 provider succeeded (failures named on
  stderr), `1` only when every selected provider failed. The default selected set is Claude + Codex;
  `--with-oracle` adds Oracle.
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
  usage tokens — the codex event stream itself names no model; Oracle = pinned `gpt-5.6/pro` +
  adapter wall time. Oracle provenance intentionally excludes browser profile, account, and cost.
  Missing fields degrade to a shorter header; rounds written before this feature keep the old format.

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
2. Verify: `bun scripts/confer-test.mjs` (extend the fakes if the CLI shape is new), then run the
   relevant best-effort live probe under a temporary `CONFER_HOME`; use `doctor --live oracle` only
   when Oracle was explicitly requested. A live probe is diagnostic, not a merge gate.

Candidate stub — **pi** (owner has mentioned it; identity and CLI unconfirmed): do not add until its
non-interactive invocation and resume story are verified against a real install.

## Tests

`bun scripts/confer-test.mjs` — deterministic, zero live calls: fake Claude, Codex, and Oracle CLIs
on a prepended PATH, fresh `CONFER_HOME` per case. Covers explicit Oracle routing, version/output/
session gates, child-session refresh, provider-specific timeout, fan-out isolation, total-failure
exit, process-tree timeout kill (heartbeat grandchild), malformed output, concurrent same-thread
reply, duplicate-name opens, name validation, doctor cleanup, and stale-lock stealing. Run it after
any edit; provider-specific `doctor --live` probes under a temp `CONFER_HOME` remain best-effort
diagnostics against real CLIs.
