---
name: skill-release
summary: "Publishes and syncs this collection: derives the index README from each skill's own metadata, checks publish hygiene, and guides flagship promotion."
description: Release and sync skills in the cankun-skills collection. Use when the user wants to publish or release a skill, add a new skill to the index, sync or fix a drifted skills README, run publish-hygiene checks, or promote a skill to its own flagship repo.
---

# Skill Release — converge the publish surfaces

A release is **convergence**, not a pipeline: every publish surface derives from
the skill's own files, so running this at any time is safe and idempotent.
Surfaces: the collection index (repo `README.md`), per-skill interface metadata
(`agents/openai.yaml`), a blog handoff, and — rarely — a flagship repo.

The human-facing summary of a skill resolves through one chain, highest first:

1. frontmatter `summary:` in `SKILL.md`
2. `agents/openai.yaml` → `interface.short_description`
3. first sentence of the frontmatter `description`

Index prose is always derived through this chain. When a row reads badly, fix
the skill's `summary:` and reconverge.

## 1. Inventory

Enumerate `skills/*/SKILL.md` frontmatter (committed skills only — an untracked
skill is the author's work in progress, not a release candidate) and every row
of the README **Collection** table. Classify each skill and each row:

- **matched** — row text equals the derived summary;
- **stale** — row exists but differs from the derived summary;
- **missing** — committed skill with no row;
- **orphan** — row whose skill directory is gone.

**Complete when:** every committed skill and every row carries exactly one
classification, shown to the user as a one-line-each table.

## 2. Converge the index

Regenerate Collection rows from the chain, alphabetical by skill name:

| cell | derivation |
|------|------------|
| Skill | `[<name>](./skills/<name>)` |
| What it does | resolved summary (verbatim; append requirements only if the skill declares external CLIs) |
| Install | `npx skills@latest add Wang-Cankun/cankun-skills --skill <name>` |

Remove an orphan row and warn that its install command breaks for existing
users. The **Flagship** table is hand-owned — touch it only inside the
promotion branch.

**Complete when:** the Collection table is reproducible from the skills' files
alone, and relative links resolve.

## 3. Hygiene check

Per skill being released:

- `agents/openai.yaml` present with `display_name`, `short_description`,
  `default_prompt`;
- scripts carry the executable bit **in git** (`git ls-files -s` shows `100755`);
- every file the SKILL.md points to exists;
- examples are free of secrets and machine-local paths;
- a model-invoked `description` carries trigger branches (or the skill sets
  `disable-model-invocation: true` and keeps a one-line human description).

**Complete when:** each item is a pass or a named flag in the report — flags
block nothing, but every one is surfaced.

## 4. Ship

Invoking this skill is the request to publish: show the diff summary, then
commit and push the index and metadata changes (edits to a skill's body stay
the author's own commits). Hand off — never write — a blog stub: title,
resolved summary, install command, repo link.

**Complete when:** the push has landed and the stub is delivered or the user
declined it.

## 5. Promote to flagship

Only when the user asks to move a skill into its own repo, follow
[`references/promotion.md`](references/promotion.md) — repo layout modeled on
`known-unknowns`, the index row move, install-command breakage, and skillshelf
re-linking are all in there.

**Complete when:** every checklist item in the reference is done or explicitly
deferred.
