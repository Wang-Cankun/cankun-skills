# cankun-skills [![skills.sh](https://skills.sh/b/wang-cankun/cankun-skills)](https://skills.sh/wang-cankun/cankun-skills)

Agent skills by [Cankun Wang](https://github.com/Wang-Cankun), hosted in this repo under [`skills/`](./skills). This page is the index.

A skill is a `SKILL.md` playbook that an AI agent loads to follow a specific process — these work with Claude Code and any runtime that supports the convention.

## Collection

Skills are grouped as on [cankun.me/skills](https://cankun.me/skills), by what you are trying to do: thinking, working with models, making things, then repos and publishing.

### Thinking

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [ambition](./skills/ambition) | Rewrite a clear task into one more ambitious assignment, combining the altitude, depth and range that fit, with access needs and evidence of success. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ambition` |
| [common-ground](./skills/common-ground) | Align with the user on what a task is for, close with a finish-line brief, and hand the understanding back after the work. | `npx skills@latest add Wang-Cankun/cankun-skills --skill common-ground` |
| [known-unknowns](./skills/known-unknowns) | Use the Rumsfeld matrix to articulate tacit judgment, connect dormant knowledge, and explore blind spots. | `npx skills@latest add Wang-Cankun/cankun-skills --skill known-unknowns` |
| [taste](./skills/taste) | Improves work that is correct but unsatisfying, using the principles of Paul Graham's "Taste for Makers": diagnose, find the organising idea, revise, test. | `npx skills@latest add Wang-Cankun/cankun-skills --skill taste` |

### Working with models

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [confer](./skills/confer) | Resumable cross-model consultation: GPT-6 Pro through Oracle by default, Claude or Codex directly, and Gemini 3.8 Flash or GLM 5.3 through Pi, with saved preferences, per-round provenance, and concurrency-safe state. Requires `bun` and at least one provider CLI; Pi models must be configured locally; Oracle requires version 0.21.4 or newer and a signed-in ChatGPT browser profile. | `npx skills@latest add Wang-Cankun/cankun-skills --skill confer` |
| [crew](./skills/crew) | Runs a task with a crew of persistent agents in Herdr panes: a coordinator routes work between executors and independent reviewers, and brings the user only decisions. Requires Herdr (run from inside a Herdr pane, HERDR_ENV=1), the agent CLIs used by the chosen roles (Claude Code, Pi, Codex), and python3 for the optional watcher. GPT Pro consultations go through the confer skill. | `npx skills@latest add Wang-Cankun/cankun-skills --skill crew` |
| [gpt-workflow](./skills/gpt-workflow) | GPT through Pi does the producing stages of Claude Code Workflows that Claude writes per task (implementing, fixing, researching, reviewing first), and Claude accepts each result before anything relies on it. Requires Claude Code's Workflow tool, Pi with a default model and its ponytail package, and the bundled pi-runner subagent and pi-job tool (install with `scripts/install-runner.sh`). | `npx skills@latest add Wang-Cankun/cankun-skills --skill gpt-workflow` |

### Making things

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [art-photo-quiet-light](./skills/art-photo-quiet-light) | Plans, directs, generates, and edits slow-travel and lifestyle photography in the quiet-light visual language associated with Roberta Mazzone: architectural composition, natural light, warm restraint, and quiet cinematic narrative. | `npx skills@latest add Wang-Cankun/cankun-skills --skill art-photo-quiet-light` |
| [art-poster-mondo](./skills/art-poster-mondo) | Researches, art-directs, creates, and critiques alternate pop-culture posters in the Mondo screen-print tradition: source-grounded concepts, integrated typography, collectible-object craft, and print-ready variants. | `npx skills@latest add Wang-Cankun/cankun-skills --skill art-poster-mondo` |
| [travel-dossier](./skills/travel-dossier) | Turns a tour-agency itinerary PDF plus tickets into a phone-first A5 travel dossier (Swiss-minimal HTML→PDF), with a truth-sourcing discipline: every number in the booklet traces to a source. (中文) Requires headless Chrome + Python (`pypdf`). | `npx skills@latest add Wang-Cankun/cankun-skills --skill travel-dossier` |

### Repos & publishing

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [cankun-blog-preview](./skills/cankun-blog-preview) | Generates and integrates exactly one Franklin Booth-inspired, white-background preview image for a Cankun blog article, then validates its optimized WebP and full-resolution link. Requires `bun` + a local cankun-blog checkout. | `npx skills@latest add Wang-Cankun/cankun-skills --skill cankun-blog-preview` |
| [repo-wayfinder](./skills/repo-wayfinder) | Checks or designs a repository's documentation system: which document owns each question, how agents reach it, and how it stays current. | `npx skills@latest add Wang-Cankun/cankun-skills --skill repo-wayfinder` |
| [skill-release](./skills/skill-release) | Publishes and syncs this collection: derives the index README and the cankun.me skills page from each skill's own metadata, checks publish hygiene, and guides flagship promotion. Requires `bun` + `curl` + the `skl` CLI. | `npx skills@latest add Wang-Cankun/cankun-skills --skill skill-release` |

## License

Each skill carries its own license (MIT unless noted); see [`LICENSE`](./LICENSE).
