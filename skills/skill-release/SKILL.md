---
name: skill-release
compatibility: Requires `bun` + `curl` + the `skl` CLI.
metadata:
  group: internal
  summary: "Publishes and syncs this collection: derives the index README and the cankun.me skills page from each skill's own metadata, checks publish hygiene, and guides flagship promotion."
description: Release and sync skills in the cankun-skills collection. Use when the user wants to publish or release a skill, add a new skill to the index, sync or fix a drifted skills README or the cankun.me skills page, run publish-hygiene checks, or promote a skill to its own flagship repo (or fold one back).
---

# Skill Release — converge the publish surfaces

A release is **convergence**, not a pipeline: every publish surface derives from
the skill's own files, so running this at any time is safe and idempotent.
Surfaces: the collection index (repo `README.md`), per-skill interface metadata
(`agents/openai.yaml`), the [cankun.me/skills](https://cankun.me/skills) page,
and — rarely — a flagship repo.

**Write boundary**: this skill edits metadata surfaces only — frontmatter keys
(`metadata.summary`, `compatibility:`), `agents/*.yaml`, the index README, and
`cankun-blog/app/data.ts`.
The SKILL.md body belongs to the author: a content finding (weak description,
missing triggers) is a flag routed back, never an edit. The route starts at a
committed skill — moving a directory into `skills/` is the author's (or skl's)
move, not this skill's.

The human-facing summary of a skill resolves through one chain, highest first:

1. frontmatter `metadata.summary` in `SKILL.md`
2. `agents/openai.yaml` → `interface.short_description`
3. first sentence of the frontmatter `description`

Index prose is always derived through this chain, and convergence flows toward
the **better text in either direction**: when a row reads badly, fix the
skill's `metadata.summary` and reconverge; when existing row prose beats the
derived value, promote that prose into `metadata.summary` rather than
degrading the row.

## 1. Inventory

Enumerate `skills/*/SKILL.md` frontmatter (committed skills only — an untracked
skill is the author's work in progress, not a release candidate) and every row
of the README **Collection** table. Classify each skill and each row:

- **matched** — row text equals the derived summary (plus, when the skill
  sets `compatibility:`, that value appended verbatim);
- **stale** — row exists but differs from that derived cell text;
- **missing** — committed skill with no row;
- **orphan** — row whose skill directory is gone.

**Complete when:** every committed skill and every row carries exactly one
classification, shown to the user as a one-line-each table.

## 2. Converge the index

Collection rows are grouped by the frontmatter `metadata.group` key (`general`
| `design` | `internal`, default `general`) into three subsections — **General
use**, then **Design**, then **Internal workflow** — the same categories as
cankun.me; the cankun-blog `group` field derives from this same key. Within a group, regenerate rows
alphabetically by skill name:

| cell | derivation |
|------|------------|
| Skill | `[<name>](./skills/<name>)` |
| What it does | resolved summary (verbatim; if the skill sets `compatibility:`, append it verbatim) |
| Install | `npx skills@latest add Wang-Cankun/cankun-skills --skill <name>` |

Remove an orphan row and warn that its install command breaks for existing
users. A **Flagship** table exists only while a promoted skill does; it is
hand-owned, created and retired inside the promotion branch.

**Complete when:** the Collection table is reproducible from the skills' files
alone, and relative links resolve.

## 3. Hygiene check

Per skill being released:

- frontmatter passes the Agent Skills spec (agentskills.io): top-level keys
  limited to `name`, `description`, `license`, `compatibility`, `metadata`,
  `allowed-tools` — custom keys (`group`, `summary`) live under `metadata:`;
  Claude Code runtime keys (e.g. `disable-model-invocation`) are a known,
  accepted deviation;
- `agents/openai.yaml` present with `display_name`, `short_description`,
  `default_prompt` — a missing file is created, not merely flagged (it is a
  publish surface inside the write boundary);
- scripts carry the executable bit **in git** (`git ls-files -s` shows `100755`);
- every file the SKILL.md points to exists;
- examples are free of secrets and machine-local paths;
- a model-invoked `description` carries trigger branches (or the skill sets
  `disable-model-invocation: true` and keeps a one-line human description);
- a `design`-group skill's name follows the `art-<medium>-<style>` family, the
  filterable prefix convention;
- the skill has been dogfooded: `skl where <name>` shows at least one
  deployment — zero deployments flags "unused", non-blocking like every flag.

**Complete when:** each item is a pass or a named flag in the report — flags
block nothing, but every one is surfaced.

## 4. Ship

Invoking this skill is the request to publish: show the diff summary, then
commit and push the index and metadata changes (edits to a skill's body stay
the author's own commits).

**Complete when:** the push has landed.

## 5. Sync cankun.me

The `/skills` page of `~/Documents/GitHub/cankun-blog` is data-driven — the
only file to edit is `app/data.ts`. Derive `desc` from the resolved summary
(one plain human sentence), write `descZh` for mainland readers (natural
copy, not word-for-word), pick `group` and the tier-correct `href`. Entry
shape, site writing rules, link verification, build, deploy, smoke test, and
commit style: follow [`references/cankun-blog.md`](references/cankun-blog.md).
`href` targets the skill's GitHub source (live as soon as step 4's push
lands) — still curl-verify every link before shipping.

**Complete when:** production serves the entry (smoke test passes) and
cankun-blog is committed and pushed — or the step is explicitly deferred.

## 6. Promote to flagship — or fold back

Only when the user asks to move a skill into its own repo (or to fold a
flagship back into the collection), follow
[`references/promotion.md`](references/promotion.md) — repo layout, the index
row move, install-command breakage, skillshelf re-linking, and the demotion
checklist are all in there.

**Complete when:** every checklist item in the reference is done or explicitly
deferred.
