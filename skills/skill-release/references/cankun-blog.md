# Syncing the cankun.me skills page

Repo: `~/Documents/GitHub/cankun-blog`. Stack: Next.js 15 (App Router) via
Vinext, deployed on Cloudflare Workers. Runtime is **bun** — never npm.

## The one file

The `/skills` page is fully data-driven. For a list update the ONLY file to
edit is `app/data.ts`: the `skills` array at the bottom (type `Skill`).
Add / edit / remove entries there; order within a group = display order.

Rendering lives in `app/components/SkillsList.tsx` (two groups + EN/中文
toggle); styles in the `/* ---- skills ---- */` block of `app/globals.css`.
Do not touch either unless the layout itself is changing.

## Source of truth for the list

The skills live in the sibling repo `~/Documents/GitHub/cankun-skills`
(`skills/` folder, indexed in its README). Flagship skills live in their own
repos (e.g. known-unknowns). Diff that against the `skills` array to find
what changed.

## Shape of one entry

```ts
{
  name: "<slug>",              // CLI slug, always English
  desc: "...",                 // ONE plain sentence, what it does
  descZh: "...",               // 简体中文, written for mainland readers,
                               // not a word-for-word translation
  href: "<skills.sh page>",
  group: "general" | "internal",
}
```

Rules:

- Do NOT copy the SKILL.md frontmatter `description` — that text is an agent
  trigger ("Use when the user asks..."), not human-facing copy. Write one
  sentence from the resolved summary; the "What it does" column in
  cankun-skills' README is a good base.
- Never use an em dash (— or ——) in either language; restructure with
  commas, colons, or parentheses (site-wide writing rule).
- `href` patterns — verify each returns HTTP 200 with curl BEFORE shipping
  (skills.sh may lag a fresh push; on 404 defer the entry, never ship a dead
  link):
  - hosted in cankun-skills: `https://skills.sh/wang-cankun/cankun-skills/<slug>`
  - has its own repo: `https://skills.sh/wang-cankun/<slug>`
- `group`: `"general"` = useful to anyone; `"internal"` = tooling for
  Cankun's own workflow (e.g. cankun-blog-preview).

## Verify, deploy, commit

1. `bun run build` — must pass.
2. Optional visual check: a vinext dev server is often ALREADY running on
   localhost:3000 (do not kill it; HMR picks up the edit). Open
   http://localhost:3000/skills and check both EN and 中文.
3. `bun run deploy` — ships to Cloudflare (cankun.me + www.cankun.me).
4. Smoke-test production: `curl -s https://cankun.me/skills | grep "<new-slug>"`.
5. Commit and push so the repo matches production. Follow the existing
   gitmoji + conventional style, e.g.:
   `📝 docs(skills): add <slug> to skills page`
