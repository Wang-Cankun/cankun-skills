# Topology guide

Read this before measuring an instruction chain, or before recommending a new document
topology or instruction layer. The section shapes for each file, `AGENTS.md` included, are in
[`document-templates.md`](document-templates.md).

## Where context lives

```text
one task -> prompt
durable repo-wide constraint or route -> root AGENTS.md
procedure or rule one kind of task needs -> repository skill, path-scoped rule, or the doc that task opens
rule that must always hold -> lint, test, hook, or CI check
reusable cross-repository procedure -> skill
current executable behavior -> owning code, type, schema, config, or contract
conformance -> test or driven probe
```

Grounding: a task prompt carries the current goal and completion condition; `AGENTS.md`
carries durable repository guidance, discovered from the root toward the working directory
with local precedence and kept short; a skill packages a workflow through progressive
disclosure; formatting and lint checks belong to CI; instructions are context, so a rule that
must hold regardless belongs in a hook. Sources:
[Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md) ·
[Codex skills](https://learn.chatgpt.com/docs/build-skills) ·
[Claude Code memory](https://code.claude.com/docs/en/memory) ·
[rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## Loading limits

The instruction chain loads on every task, so it is the one layer with hard budgets. As
documented in September 2026 — recheck the sources before relying on a number:

- Claude Code targets under 200 lines per `CLAUDE.md`; longer files reduce adherence.
- Codex stops adding instruction files once the combined chain reaches 32 KiB by default.

Repository overviews and directory tours in an instruction file raise cost without raising
task success ([Gloaguen et al., 2026](https://arxiv.org/abs/2602.11988)); route to a map
instead.

## The AGENTS.md layer

- **Name owners.** Each routing row names the owner of a question instead of answering it
  inline; architecture, development, environment and release answers update on different
  triggers, so they live in different documents.
- **Keep the layer a router.** When a row grows an explanation, the explanation belongs in
  the document the row points to.
- **Nested layers** only where a package's hazards or ownership boundaries materially differ
  from the root; local guidance takes precedence.
- **One owner across tools.** Content every agent needs lives in `AGENTS.md`. A tool-specific
  file (`.claude/rules/`, `.cursor/rules/`, `.github/instructions/`) is invisible to the other
  tools, so it holds only what that tool alone needs, or a pointer.
- **Co-change as review.** A pull-request template asking whether a behavior change needs a
  documentation change reduces drift; it does not prove that prose matches code.

## CLAUDE.md

Claude Code reads `AGENTS.md` directly when no `CLAUDE.md`, `.claude/CLAUDE.md` or
`CLAUDE.local.md` sits in the working directory or above it; any of them switches that off by
default. Choose one layout per repository:

- **`AGENTS.md` only** — no `CLAUDE.md` anywhere on the path. The default when every agent
  shares the same instructions.
- **Thin re-export** — each `CLAUDE.md` imports its sibling with `@AGENTS.md`, adding only
  Claude-specific loading mechanics. Use it where some sessions cannot read `AGENTS.md`
  directly, or where Claude needs something the other tools do not.

A `CLAUDE.md` holding only `@AGENTS.md` becomes removable once every Claude Code session in
use reads `AGENTS.md` directly; recommend removing it, stating that condition.
A `CLAUDE.md` that has grown its own repository constraints is a drift finding: move the
content into the owning `AGENTS.md` and restore the layout. The project-root `CLAUDE.md` is
re-read after compaction, so an instruction asking Claude to keep it in context is a no-op.
