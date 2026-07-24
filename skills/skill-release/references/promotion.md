# Flagship promotion checklist

Promotion is a rare, deliberate event — a skill leaves the collection for its
own repo when it has earned independent distribution. Template: the
[`known-unknowns`](https://github.com/Wang-Cankun/known-unknowns) repo.

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
      pattern `https://skills.sh/wang-cankun/<name>`, then build, deploy, and
      smoke-test per [`cankun-blog.md`](cankun-blog.md).
