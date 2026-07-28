---
name: confer
metadata:
  group: general
  summary: >-
    Cross-model consultation with resumable threads: ask Claude, Codex, or
    explicitly requested GPT Pro through Oracle; keep multi-round peer-review
    dialogues alive across sessions; fan out concurrently without changing the
    default Claude + Codex set. Single-file bun CLI with per-round provenance and
    concurrency-safe state.
description: Consult a peer AI model (Claude or Codex, plus GPT Pro through Oracle when explicitly requested) and keep the dialogue resumable across rounds. Use when the user wants a second opinion from another model ("ask codex", "问问 codex", "让 claude 看看", "gpt says…"), explicitly asks to use/ask GPT Pro or Oracle, wants a multi-round cross-model review, wants to resume or continue an earlier consultation thread, or when a conclusion needs independent-model verification.
---

# Confer — cross-model consultation with resumable threads

Requires `bun` plus at least one provider CLI (`claude`, `codex`, or Oracle >= 0.16.2 with an authenticated ChatGPT browser profile).

You talk to a peer model through **threads**: open one with a question, the peer's session id is stored, and any later round — today or next week, from any host session — resumes the same peer-side context. All mechanics live in `scripts/confer.mjs` (single source of truth); never assemble raw `claude -p`, `codex exec`, or `oracle` calls yourself.

```
scripts/confer.mjs open <provider> [-t name] <prompt|->   # start thread (claude|codex|oracle)
scripts/confer.mjs reply <thread> <prompt|->              # continue with full peer-side context
scripts/confer.mjs all [--with-oracle] <prompt|->         # default claude+codex; flag explicitly adds GPT Pro
scripts/confer.mjs list | show <thread>                   # registry / transcript
scripts/confer.mjs doctor [--live [provider]]             # live defaults to claude+codex
```

Pass `-` as the prompt and pipe stdin for anything long or containing quotes.

A round can take minutes. When you expect a long consultation and have other work, run the call in the background and pick the reply up when notified — never relay a peer through a subagent: the peer's own words must reach the user undiluted. Each `←` transcript header records which model answered (and cost/tokens where the CLI reports them).

## Steps

1. **Resolve the target.** Which provider, and new thread or continuation? Route to `oracle` only when the user explicitly asks to use/ask GPT Pro or Oracle; task difficulty alone is never enough. Bare `all` and bare `doctor --live` exclude Oracle; use `all --with-oracle` or `doctor --live oracle` only on explicit request. Otherwise prefer a peer that is **not your own model family** — a same-model consult is not an independent second opinion. When the user says 继续/上次/"what does it say now", run `list` and match — never open a fresh thread for what is semantically round N of an old one. Name threads you expect to revisit (`-t zhang-pe-review`); let one-shots auto-name. Done when: provider + thread decided.

2. **Compose a self-contained prompt.** The peer sees none of your conversation, files, or context — only what you send. Inline the code, text, or claims under discussion; state the question precisely; for review requests, ask for a verdict plus reasoning, not vibes. Long material → heredoc via stdin (`... <<'EOF' | scripts/confer.mjs open codex -t name -`). Done when: the peer could answer with zero access to your session.

3. **Run, then relay faithfully.** Report the peer's position as the peer's — quote the load-bearing sentences, keep disagreements between you and the peer visible instead of silently merging into consensus, and state your own verdict separately when you have one. Always surface the thread name so the dialogue can continue later. Done when: the user has seen the peer's answer, your position, and the thread id.

## Guardrails

- The peer is **advisory and read-only**: it must never be asked to edit files or run state-changing commands (codex threads open sandboxed; claude print-mode cannot approve writes). If the peer proposes changes, you apply them under your own judgment.
- Never send secrets, API keys, or credentials in a prompt — transcripts persist in plaintext under `~/.confer/`; Oracle browser/account configuration remains machine-local under `~/.oracle/`.
- A peer's agreement is not verification. Treat "the other model also thinks so" as one signal, not proof; a peer that refutes you is the more valuable outcome.

Adding a provider, CLI/session mechanics, and known version caveats: `references/providers.md`.
