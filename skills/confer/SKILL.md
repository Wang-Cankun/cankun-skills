---
name: confer
compatibility: Requires `bun` and at least one provider CLI; Pi models must be configured locally; Oracle requires version 0.21.4 or newer and a signed-in ChatGPT browser profile.
metadata:
  group: models
  summary: >-
    Resumable cross-model consultation with peers that read the caller's
    repository themselves: GPT-6 Pro through Oracle by default, Claude or Codex
    directly, Gemini 4 Argon through agy, and any Pi model (GPT, Gemini Flash,
    GLM), with saved preferences, per-round provenance, and concurrency-safe state.
description: "Consult another model (GPT, Claude, Codex, Gemini or GLM) for an independent opinion or review, and resume earlier consultation threads. Use when the user asks for a second model's view or to continue a peer discussion; not when another model should do the work itself."
---

# Confer — cross-model consultation with resumable threads

Requires `bun` plus at least one provider CLI (`claude`, `codex`, `pi`, `agy`, or Oracle >= 0.21.4 with an authenticated ChatGPT browser profile).

You talk to a peer model through **threads**: open one with a question, the peer's session id is stored, and any later round — today or next week, from any host session — resumes the same peer-side context. All mechanics live in `scripts/confer.mjs` (single source of truth); use it instead of assembling provider CLI calls.

```
scripts/confer.mjs ask [provider] [-t name] <prompt|->    # saved preference, otherwise GPT-6 Pro
scripts/confer.mjs open <provider> [-t name] <prompt|->   # explicit claude|codex|pi|oracle
scripts/confer.mjs config [provider|pi-model|oracle-profile [value]]  # show or save defaults
scripts/confer.mjs reply <thread> <prompt|->              # continue with full peer-side context
scripts/confer.mjs all [--with-oracle] <prompt|->         # default claude+codex; flag explicitly adds GPT Pro
scripts/confer.mjs list | show <thread>                   # registry / transcript
scripts/confer.mjs doctor [--live [provider]]             # live defaults to claude+codex
```

Pass `-` as the prompt and pipe stdin for anything long or containing quotes.

A round can take minutes. When you expect a long consultation and have other work, run the call in the background and pick the reply up when notified — never relay a peer through a subagent: the peer's own words must reach the user undiluted. Each `←` transcript header records which model answered (and cost/tokens where the CLI reports them).

## Steps

1. **Resolve the target.** An explicit user choice takes precedence. For a new consultation with no model/provider preference, use `ask` to resolve the saved default; without a saved preference it uses GPT-6 Pro through Oracle. `ask pi` uses Pi's selected default: Gemini 3.8 Flash unless configured otherwise. A Gemini 4 Argon request is `open agy` (model and effort through `CONFER_AGY_ARGS`, e.g. `--model gemini-4-argon-high --effort high`). An explicit Gemini Flash or GLM request routes through Pi with `CONFER_PI_MODEL=gemini-3.8-flash` or `CONFER_PI_MODEL=glm-5.3`, even when the saved Pi default differs. For another named Pi model, check `pi --list-models` and pass its full `provider/model` identifier. For Claude Fable 5.1, pass `CONFER_CLAUDE_ARGS='--model claude-fable-5-1'` to `open claude` or `ask claude`. The `fable` alias currently resolves to that model, but can move; `fable5.1` is rejected by Claude Code. Confirm the model in the `←` transcript header. When resuming, run `list` and match the existing thread; `reply` keeps that thread's provider and model even if defaults have changed. Name threads you expect to revisit (`-t zhang-pe-review`); let one-shots auto-name. Done when: provider/model + new or existing thread decided.

   Save a requested preference with `config provider oracle|pi|agy|claude|codex` or `config pi-model gemini-3.8-flash|glm-5.3`; full Pi identifiers also work. When Oracle's Chrome holds several accounts, `config oracle-profile <dir>` pins the ChatGPT account to use (a Chrome profile directory such as `Default`). `config` shows effective defaults. For new consultations, precedence is explicit provider / per-call environment override, then saved config, then built-in defaults. `all` remains the Claude + Codex panel; `all --with-oracle` adds GPT-6 Pro. `doctor --live` checks Claude + Codex; name `pi`, `agy` or `oracle` to test that provider.

2. **Point the peer at the material.** The peer sees none of your conversation. Every provider but Oracle runs read-only in your working directory and opens files itself, so run confer from the repository or worktree the question is about, and name the paths, the commit or branch, and what to check. Inline only what is not on disk there: facts from your conversation, another machine's data, output you already have. Copies go stale and hide the rest of the repository. State the question precisely; for review requests, ask for a verdict plus reasoning, not vibes. Let the substance determine response length and the number of findings. Add word, character, or output-token budgets, numbered-finding caps, or requests for a short answer only when the user explicitly requests them; display limits in the calling tool are not a reason to shorten the peer's answer. Long material → heredoc via stdin (`... <<'EOF' | scripts/confer.mjs open codex -t name -`).

   **Oracle reads GitHub, not your disk.** GPT-6 Pro through Oracle can open the user's GitHub repositories, so write the repository as `owner/name`, the branch or commit, and the paths; push first what it must see, because it sees only pushed content (inline uncommitted changes, unpushed commits, worktree-only files, ignored folders such as `.work/`, and anything kept outside Git). Done when: the peer could answer from what you sent plus the files it can read where it runs.

3. **Run, then relay faithfully.** Report the peer's position as the peer's — quote the load-bearing sentences, keep disagreements between you and the peer visible instead of silently merging into consensus, and state your own verdict separately when you have one. Always surface the thread name so the dialogue can continue later. Done when: the user has seen the peer's answer, your position, and the thread id.

4. **Resolve feedback and return to the task.** For consequential findings, distinguish accepted findings and their fix or check, rejected findings and the evidence for rejection, and unresolved evidence gaps with the next useful check. Keep this in the task's existing record or conversation; a separate review report is not required. Apply supported changes within the original authorization, then verify them through the project's own method.

   Continue the consultation only when another answer could change a still-unresolved substantive decision and existing evidence or a simpler direct check cannot settle it, or when the user explicitly requests another round. A new commit, revised wording, additional evidence, or the absence of an “APPROVE” verdict alone does not justify asking again. State what the next round must resolve before sending it. Otherwise close the consultation and resume the original task. An unresolved product or verification gap remains open even when no further model round is useful.

## Guardrails

- The peer is **advisory and read-only**: it must never be asked to edit files or run state-changing commands. Codex runs in a read-only sandbox, Claude without its writing tools or shell, Pi with only its read tools, and agy in plan mode, which denies writes. If the peer proposes changes, you apply them under your own judgment.
- Never send secrets, API keys, or credentials in a prompt — transcripts persist in plaintext under `~/.confer/`; Oracle browser/account configuration remains machine-local under `~/.oracle/`.
- A peer's agreement is not verification. Treat "the other model also thinks so" as one signal, not proof; a peer that refutes you is the more valuable outcome.

Adding a provider, CLI/session mechanics, and known version caveats: `references/providers.md`.

## Use a different skill when

- The other model should stay resident, holding context that you or other windows return to
  (a side agent, a table of models discussing over rounds): a pane-based setup such as `crew`.
- The other model should do delegated work whose result comes back: GPT stages inside a
  workflow such as `gpt-workflow`.
- The question is which version of a task is worth doing: `ambition`. A peer's opinion on one
  of its versions is still a confer round.
