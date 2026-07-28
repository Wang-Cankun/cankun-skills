# Flagship promotion — and demotion — checklist

Promotion is a rare, deliberate event — a skill leaves the collection for its
own repo when it has earned independent distribution. Demotion is the exact
inverse: the skill folds back when independent distribution stopped paying for
its upkeep.

## New repo (`Wang-Cankun/<name>`)

- [ ] Layout: `skills/<name>/SKILL.md` (+ `agents/`, `references/`, `scripts/`)
      — the nested `skills/` path is the `npx skills add` discovery convention,
      keep it even for a single-skill repo.
- [ ] Root: `README.md` (what/why/install/usage), `README_CN.md` when the skill
      serves Chinese-language use, `LICENSE` (MIT unless noted), `.gitignore`.
- [ ] Copy the skill directory verbatim; note the origin commit of
      `cankun-skills` in the first commit message (history stays in the old repo).

## Back in `cankun-skills`

- [ ] Move the skill's row from **Collection** to **Flagship**: link goes to the
      new repo, install becomes `npx skills@latest add Wang-Cankun/<name>`.
- [ ] Delete `skills/<name>/` in the same commit; the commit message must state
      that the old `--skill <name>` install command breaks and where users go now.

## Local skillshelf

- [ ] `skl link <name> --from <new-repo>/skills/<name> --force` — repoint the
      LINKED entry to the new dev repo.
- [ ] `skl where <name>` — confirm every deployment still resolves.

## cankun.me

- [ ] Update the entry's `href` in `cankun-blog/app/data.ts` to the flagship
      pattern `https://github.com/Wang-Cankun/<name>/blob/main/skills/<name>/SKILL.md`,
      then build, deploy, and smoke-test per [`cankun-blog.md`](cankun-blog.md).

## Demotion (fold a flagship back)

- [ ] Copy `skills/<name>/` from the flagship repo into `cankun-skills/skills/`
      verbatim, uncommitted revisions included; bring `LICENSE` along if the
      collection lacks one.
- [ ] Repoint skillshelf: `skl link <name> --from cankun-skills/skills/<name>
      --force`, then `skl where <name>` to confirm every deployment resolves.
- [ ] Remove the **Flagship** row; retire the whole Flagship section when it
      empties. The skill rejoins the Collection table through normal
      convergence (step 2).
- [ ] Update the cankun-blog `href` to the collection pattern and redeploy.
- [ ] Archive the flagship repo on GitHub — until archived, `npx skills@latest
      add Wang-Cankun/<name>` silently serves stale content.
