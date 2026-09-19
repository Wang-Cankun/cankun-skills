---
name: confer
compatibility: Requires `bun` and at least one provider CLI; Pi models must be configured locally; Oracle requires version 0.21.1 or newer and a signed-in ChatGPT browser profile.
metadata:
  group: general
  summary: >-
    Resumable cross-model consultation: GPT-6 Pro through Oracle by default,
    Claude or Codex directly, and Gemini 3.8 Flash or GLM 5.3 through Pi,
    with saved preferences, per-round provenance, and concurrency-safe state.
description: Consult GPT Pro by default, or a chosen Claude, Codex, or Pi model, and keep the dialogue resumable. Use for a second opinion from another model, named model consultations (including Gemini or GLM), multi-round peer reviews, or resuming an earlier consultation.
---

# Confer — cross-model consultation with resumable threads

Requires `bun` plus at least one provider CLI (`claude`, `codex`, `pi`, or Oracle >= 0.21.1 with an authenticated ChatGPT browser profile).

You talk to a peer model through **threads**: open one with a question, the peer's session id is stored, and any later round — today or next week, from any host session — resumes the same peer-side context. All mechanics live in `scripts/confer.mjs` (single source of truth); use it instead of assembling provider CLI calls.

```
scripts/confer.mjs ask [provider] [-t name] <prompt|->    # saved preference, otherwise GPT-6 Pro
scripts/confer.mjs open <provider> [-t name] <prompt|->   # explicit claude|codex|pi|oracle
scripts/confer.mjs config [provider|pi-model [value]]    # show or save defaults
scripts/confer.mjs reply <thread> <prompt|->              # continue with full peer-side context
scripts/confer.mjs all [--with-oracle] <prompt|->         # default claude+codex; flag explicitly adds GPT Pro
scripts/confer.mjs list | show <thread>                   # registry / transcript
scripts/confer.mjs doctor [--live [provider]]             # live defaults to claude+codex
```

Pass `-` as the prompt and pipe stdin for anything long or containing quotes.

A round can take minutes. When you expect a long consultation and have other work, run the call in the background and pick the reply up when notified — never relay a peer through a subagent: the peer's own words must reach the user undiluted. Each `←` transcript header records which model answered (and cost/tokens where the CLI reports them).

## Steps

1. **Resolve the target.** An explicit user choice takes precedence. For a new consultation with no model/provider preference, use `ask` to resolve the saved default; without a saved preference it uses GPT-6 Pro through Oracle. `ask pi` uses Pi's selected default: Gemini 3.8 Flash unless configured otherwise. An explicit Gemini or GLM request routes through Pi with `CONFER_PI_MODEL=gemini-3.8-flash` or `CONFER_PI_MODEL=glm-5.3`, even when the saved Pi default differs. For another named model, check `pi --list-models` and pass its full `provider/model` identifier. When resuming, run `list` and match the existing thread; `reply` keeps that thread's provider and model even if defaults have changed. Name threads you expect to revisit (`-t zhang-pe-review`); let one-shots auto-name. Done when: provider/model + new or existing thread decided.

   Save a requested preference with `config provider oracle|pi|claude|codex` or `config pi-model gemini-3.8-flash|glm-5.3`; full Pi identifiers also work. `config` shows effective defaults. For new consultations, precedence is explicit provider / per-call environment override, then saved config, then built-in defaults. `all` remains the Claude + Codex panel; `all --with-oracle` adds GPT-6 Pro. `doctor --live` checks Claude + Codex; name `pi` or `oracle` to test that provider.

2. **Compose a self-contained prompt.** The peer sees none of your conversation, files, or context — only what you send. Inline the code, text, or claims under discussion; state the question precisely; for review requests, ask for a verdict plus reasoning, not vibes. Let the substance determine response length and the number of findings. Add word, character, or output-token budgets, numbered-finding caps, or requests for a short answer only when the user explicitly requests them; display limits in the calling tool are not a reason to shorten the peer's answer. Long material → heredoc via stdin (`... <<'EOF' | scripts/confer.mjs open codex -t name -`). Done when: the peer could answer with zero access to your session.

3. **Run, then relay faithfully.** Report the peer's position as the peer's — quote the load-bearing sentences, keep disagreements between you and the peer visible instead of silently merging into consensus, and state your own verdict separately when you have one. Always surface the thread name so the dialogue can continue later. Done when: the user has seen the peer's answer, your position, and the thread id.

4. **Resolve feedback and return to the task.** For consequential findings, distinguish accepted findings and their fix or check, rejected findings and the evidence for rejection, and unresolved evidence gaps with the next useful check. Keep this in the task's existing record or conversation; a separate review report is not required. Apply supported changes within the original authorization, then verify them through the project's own method.

   Continue the consultation only when another answer could change a still-unresolved substantive decision and existing evidence or a simpler direct check cannot settle it, or when the user explicitly requests another round. A new commit, revised wording, additional evidence, or the absence of an “APPROVE” verdict alone does not justify asking again. State what the next round must resolve before sending it. Otherwise close the consultation and resume the original task. An unresolved product or verification gap remains open even when no further model round is useful.

## Guardrails

- The peer is **advisory and read-only**: it must never be asked to edit files or run state-changing commands. Codex opens sandboxed, Claude print mode cannot approve writes, and Pi runs with tools, context files, skills, and extensions disabled. If the peer proposes changes, you apply them under your own judgment.
- Never send secrets, API keys, or credentials in a prompt — transcripts persist in plaintext under `~/.confer/`; Oracle browser/account configuration remains machine-local under `~/.oracle/`.
- A peer's agreement is not verification. Treat "the other model also thinks so" as one signal, not proof; a peer that refutes you is the more valuable outcome.

Adding a provider, CLI/session mechanics, and known version caveats: `references/providers.md`.
