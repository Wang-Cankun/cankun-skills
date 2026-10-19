# Topology guide

Sources for the layering below:
[Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md) ·
[Codex skills](https://learn.chatgpt.com/docs/build-skills) ·
[Claude Code memory](https://code.claude.com/docs/en/memory) ·
[rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) ·
[Claude Code in large codebases](https://code.claude.com/docs/en/large-codebases) ·
[context rot: a single on-topic distractor lowers accuracy](https://www.trychroma.com/research/context-rot).

## Loading limits

The instruction chain loads on every task, so it is the one layer with hard budgets. As
documented in October 2026 — recheck the sources before relying on a number:

- Claude Code targets under 200 lines per `CLAUDE.md`; its docs say longer files reduce
  adherence.
- Codex stops adding instruction files once the combined chain reaches 32 KiB by default.
- Claude Code loads only the first 200 lines or 25 KB of the auto-memory `MEMORY.md`.
- Loading is eager or lazy by mechanism: `@` imports expand at launch (a thin `@AGENTS.md`
  re-export costs the whole file); a subdirectory `CLAUDE.md` loads when a file there is read;
  a `.claude/rules/` file with `paths:` frontmatter loads when matching files are touched;
  block HTML comments in `CLAUDE.md` are stripped before injection. A rule only one kind of
  task needs belongs in a lazy layer.

Measured effects of a context file on task success are small and mixed: developer-written
files gained about 4% and generated ones lost a little, at 19–23% more cost, and repository
overviews did not lead agents to the right files sooner
([Gloaguen et al., 2026](https://arxiv.org/abs/2602.11988)); route to a map instead. File
length showed no detectable effect on adherence, while adherence fell as a session went on
([McMillan, 2026](https://arxiv.org/abs/2605.10039)): treat line targets as cost heuristics,
and make a rule that must hold a check (Enforce).

## The AGENTS.md layer

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
