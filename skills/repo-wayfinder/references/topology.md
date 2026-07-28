# Topology guide

Read this before recommending a new document topology or another `AGENTS.md`
layer. Skip it when the task only classifies an existing, already declared
authority structure. The templates below are shapes to re-derive from the
target repository, never to paste blind.

## Where context lives

```text
one task -> prompt
durable repo-specific constraint or route -> applicable AGENTS.md
reusable cross-repository procedure -> skill
current executable behavior -> owning code, type, schema, config, or contract
conformance -> test or driven probe
```

The first three lines follow the official Codex boundary: a task prompt carries
the current goal and completion condition; `AGENTS.md` carries durable
repository guidance, discovered from the repository root toward the working
directory with local precedence, kept short and grounded in repeated friction;
a skill packages a reusable workflow through progressive disclosure and must
not become another copy of repository facts. Sources:
[best practices](https://learn.chatgpt.com/guides/best-practices) ·
[`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md) ·
[skills](https://learn.chatgpt.com/docs/build-skills). The last two lines are
this skill's own design judgment.

## The AGENTS.md layer

Root `AGENTS.md` shape:

```text
# <repo> — agent guide

Constraints — repo-wide, non-inferable rules only (safety walls, build/tool
choices, style decisions a reader cannot recover from the code).

Routing — a "touching X, read Y first" table naming the owner of each
question, never copying its answer:
| touching            | read first              |
| ------------------- | ----------------------- |
| <area>              | <owning doc or source>  |

Verification — the exact commands that prove a change (build, test, lint,
driven probe).
```

- Name distinct owners for architecture, development, environment, and release
  questions instead of answering them inline; they update on different
  triggers, so they live in different documents.
- Add a nested `AGENTS.md` only where a package's hazards or ownership
  boundaries materially differ from the root; local guidance takes precedence.
- Make co-change a review concern (a pull-request template asking whether the
  behavior change requires a documentation change). It reduces drift; it does
  not prove that prose matches code.

## CLAUDE.md as a thin re-export

When a repository serves Claude Code alongside other agents, `AGENTS.md` stays
the single owner of agent instruction at every level; each `CLAUDE.md` is only a
thin re-export of its sibling, never a second home for content. General shape:

```text
@AGENTS.md

Claude Code
Always keep these instructions — this file and the imported AGENTS.md — in
context; never compact them.

Extra conventions load automatically by scope: per-directory CLAUDE.md files
(each a thin @AGENTS.md re-export of its sibling) and path-scoped rules under
.claude/rules/*.md. These are Claude Code mechanisms; other tools read the
AGENTS.md files and the referenced rules directly.
```

- The `@AGENTS.md` import line does the routing; prose below it may only name
  Claude-specific loading mechanics, never repository facts.
- Mirror the layering: wherever a nested `AGENTS.md` exists and Claude Code is
  in use, its sibling `CLAUDE.md` is the same re-export.
- A `CLAUDE.md` that has grown its own constraints is a drift finding: move the
  content into the owning `AGENTS.md` and restore the re-export.

## Anti-patterns

- Volatile facts — protocol versions, issue identifiers, dependency behavior,
  implementation censuses — in an always-loaded instruction file.
- A routing layer that grows into a second architecture and tooling manual.
- A file created to complete a taxonomy. Prefer a pointer when the fact already
  has an owner, and no file when no distinct owning question exists.
