---
name: confer
compatibility: Requires `bun` + the `claude`/`codex` CLIs.
metadata:
  group: general
  summary: >-
    Cross-model consultation with resumable threads: ask Codex from Claude Code
    (or vice versa), keep multi-round peer-review dialogues alive across sessions,
    fan one question out to every provider concurrently. Single-file bun CLI;
    records per-round model/cost provenance; safe under concurrent use from
    multiple agent hosts.
description: Consult a peer AI model (Claude or Codex) and keep the dialogue resumable across rounds. Use when the user wants a second opinion from another model ("ask codex", "问问 codex", "让 claude 看看", "gpt says…"), wants a multi-round cross-model review, wants to resume or continue an earlier consultation thread, or when a conclusion needs independent-model verification.
---

# Confer — cross-model consultation with resumable threads

You talk to a peer model through **threads**: open one with a question, the peer's session id is stored, and any later round — today or next week, from any host session — resumes the same peer-side context. All mechanics live in `scripts/confer.mjs` (single source of truth); never assemble raw `claude -p` / `codex exec` calls yourself.

```
scripts/confer.mjs open <provider> [-t name] <prompt|->   # start thread (claude|codex)
scripts/confer.mjs reply <thread> <prompt|->              # continue with full peer-side context
scripts/confer.mjs all <prompt|->                         # fan one question out to every provider (concurrent)
scripts/confer.mjs list | show <thread>                   # registry / transcript
scripts/confer.mjs doctor [--live]                        # health check (run --live once after install)
```

Pass `-` as the prompt and pipe stdin for anything long or containing quotes.

A round can take minutes. When you expect a long consultation and have other work, run the call in the background and pick the reply up when notified — never relay a peer through a subagent: the peer's own words must reach the user undiluted. Each `←` transcript header records which model answered (and cost/tokens where the CLI reports them).

## Steps

1. **Resolve the target.** Which provider, and new thread or continuation? Prefer a peer that is **not your own model family** — a same-model consult is not an independent second opinion. When the user says 继续/上次/"what does it say now", run `list` and match — never open a fresh thread for what is semantically round N of an old one. Name threads you expect to revisit (`-t zhang-pe-review`); let one-shots auto-name. Done when: provider + thread decided.

2. **Compose a self-contained prompt.** The peer sees none of your conversation, files, or context — only what you send. Inline the code, text, or claims under discussion; state the question precisely; for review requests, ask for a verdict plus reasoning, not vibes. Long material → heredoc via stdin (`... <<'EOF' | scripts/confer.mjs open codex -t name -`). Done when: the peer could answer with zero access to your session.

3. **Run, then relay faithfully.** Report the peer's position as the peer's — quote the load-bearing sentences, keep disagreements between you and the peer visible instead of silently merging into consensus, and state your own verdict separately when you have one. Always surface the thread name so the dialogue can continue later. Done when: the user has seen the peer's answer, your position, and the thread id.

## Guardrails

- The peer is **advisory and read-only**: it must never be asked to edit files or run state-changing commands (codex threads open sandboxed; claude print-mode cannot approve writes). If the peer proposes changes, you apply them under your own judgment.
- Never send secrets, API keys, or credentials in a prompt — transcripts persist in plaintext under `~/.confer/`.
- A peer's agreement is not verification. Treat "the other model also thinks so" as one signal, not proof; a peer that refutes you is the more valuable outcome.

Adding a provider, CLI/session mechanics, and known version caveats: `references/providers.md`.
