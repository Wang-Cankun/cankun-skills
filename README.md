# cankun-skills [![skills.sh](https://skills.sh/b/wang-cankun/cankun-skills)](https://skills.sh/wang-cankun/cankun-skills)

Agent skills by [Cankun Wang](https://github.com/Wang-Cankun), hosted in this repo under [`skills/`](./skills). This page is the index.

A skill is a `SKILL.md` playbook that an AI agent loads to follow a specific process — these work with Claude Code and any runtime that supports the convention.

## Collection

Grouped as on [cankun.me/skills](https://cankun.me/skills): general use, then design, then internal workflow.

### General use

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [confer](./skills/confer) | Cross-model consultation with resumable threads: ask Claude, Codex, or explicitly requested GPT Pro through Oracle; continue peer-review dialogues across sessions; fan out concurrently while keeping Claude + Codex as the default set. Single-file bun CLI with per-round provenance and concurrency-safe state. Requires `bun` + at least one provider CLI; Oracle routes require Oracle >= 0.16.2 and an authenticated ChatGPT browser profile. | `npx skills@latest add Wang-Cankun/cankun-skills --skill confer` |
| [deposition](./skills/deposition) | Relentless one-question-at-a-time deposition of a plan, decision, or idea: keeps a visible record (✓ settled · ? open · ~ unwalked) and closes only through a nothing-further gate. | `npx skills@latest add Wang-Cankun/cankun-skills --skill deposition` |
| [known-unknowns](./skills/known-unknowns) | Guided deliberations on the Rumsfeld matrix: helps articulate tacit judgments, surfaces unrecognized patterns, tours unseen options, and ends with a paste-ready brief. | `npx skills@latest add Wang-Cankun/cankun-skills --skill known-unknowns` |
| [meeting-audio-report](./skills/meeting-audio-report) | Turns a meeting recording into a verbatim transcript plus an evidence-graded DOCX/PDF report, gated on block-level coverage so dropped audio surfaces instead of vanishing. Requires `ffmpeg`, `pandoc`, LibreOffice, Python 3.10+ with `requests` and `python-docx`, and an `OPENROUTER_API_KEY`. | `npx skills@latest add Wang-Cankun/cankun-skills --skill meeting-audio-report` |
| [travel-dossier](./skills/travel-dossier) | Turns a tour-agency itinerary PDF plus tickets into a phone-first A5 travel dossier (Swiss-minimal HTML→PDF), with a truth-sourcing discipline: every number in the booklet traces to a source. (中文) Requires headless Chrome + Python (`pypdf`). | `npx skills@latest add Wang-Cankun/cankun-skills --skill travel-dossier` |

### Design

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [art-photo-quiet-light](./skills/art-photo-quiet-light) | Plans, directs, generates, and edits slow-travel and lifestyle photography in the quiet-light visual language associated with Roberta Mazzone: architectural composition, natural light, warm restraint, and quiet cinematic narrative. | `npx skills@latest add Wang-Cankun/cankun-skills --skill art-photo-quiet-light` |
| [art-poster-mondo](./skills/art-poster-mondo) | Researches, art-directs, creates, and critiques alternate pop-culture posters in the Mondo screen-print tradition: source-grounded concepts, integrated typography, collectible-object craft, and print-ready variants. | `npx skills@latest add Wang-Cankun/cankun-skills --skill art-poster-mondo` |

### Internal workflow

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [cankun-blog-preview](./skills/cankun-blog-preview) | Generates and integrates exactly one Franklin Booth-inspired, white-background preview image for a Cankun blog article, then validates its optimized WebP and full-resolution link. Requires `bun` + a local cankun-blog checkout. | `npx skills@latest add Wang-Cankun/cankun-skills --skill cankun-blog-preview` |
| [repo-wayfinder](./skills/repo-wayfinder) | Designs or repairs a repository's documentation system: project identity, document ownership rules, task-to-authority routes, and the smallest justified file set for a new or existing project. | `npx skills@latest add Wang-Cankun/cankun-skills --skill repo-wayfinder` |
| [skill-release](./skills/skill-release) | Publishes and syncs this collection: derives the index README and the cankun.me skills page from each skill's own metadata, checks publish hygiene, and guides flagship promotion. Requires `bun` + `curl` + the `skl` CLI. | `npx skills@latest add Wang-Cankun/cankun-skills --skill skill-release` |

## License

Each skill carries its own license (MIT unless noted); see [`LICENSE`](./LICENSE).
