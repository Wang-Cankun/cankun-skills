# cankun-skills [![skills.sh](https://skills.sh/b/wang-cankun/cankun-skills)](https://skills.sh/wang-cankun/cankun-skills)

Agent skills by [Cankun Wang](https://github.com/Wang-Cankun). Flagship skills live in their own repos; the rest are hosted directly in this repo under [`skills/`](./skills). This page is the index.

A skill is a `SKILL.md` playbook that an AI agent loads to follow a specific process — these work with Claude Code and any runtime that supports the convention.

## Flagship

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [known-unknowns](https://github.com/Wang-Cankun/known-unknowns) | Guided discussions on the Rumsfeld Matrix: lends you words for preferences you can't articulate, tours options you don't know exist, and ends with a paste-ready brief. | `npx skills@latest add Wang-Cankun/known-unknowns` |

## Collection (hosted in this repo)

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [cankun-blog-preview](./skills/cankun-blog-preview) | Generates and integrates exactly one Franklin Booth-inspired, white-background preview image for a Cankun blog article, then validates its optimized WebP and full-resolution link. | `bunx skills@latest add Wang-Cankun/cankun-skills --skill cankun-blog-preview` |
| [confer](./skills/confer) | Cross-model consultation with resumable threads: ask Codex from Claude Code (or vice versa), keep multi-round peer-review dialogues alive across sessions, fan one question out to every provider concurrently. Single-file bun CLI; records per-round model/cost provenance; safe under concurrent use from multiple agent hosts. Requires `bun` + the `claude`/`codex` CLIs. | `npx skills@latest add Wang-Cankun/cankun-skills --skill confer` |
| [skill-release](./skills/skill-release) | Publishes and syncs this collection: derives the index README from each skill's own metadata, checks publish hygiene, and guides flagship promotion. | `npx skills@latest add Wang-Cankun/cankun-skills --skill skill-release` |
| [travel-dossier](./skills/travel-dossier) | Turns a tour-agency itinerary PDF plus tickets into a phone-first A5 travel dossier (Swiss-minimal HTML→PDF), with a truth-sourcing discipline: every number in the booklet traces to a source. (中文) | `npx skills@latest add Wang-Cankun/cankun-skills --skill travel-dossier` |

## License

Each skill carries its own license (MIT unless noted).
