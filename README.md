# cankun-skills

Agent skills by [Cankun Wang](https://github.com/Wang-Cankun). Flagship skills live in their own repos; the rest are hosted directly in this repo under [`skills/`](./skills). This page is the index.

A skill is a `SKILL.md` playbook that an AI agent loads to follow a specific process — these work with Claude Code and any runtime that supports the convention.

## Flagship

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [known-unknowns](https://github.com/Wang-Cankun/known-unknowns) | Guided discussions on the Rumsfeld Matrix: lends you words for preferences you can't articulate, tours options you don't know exist, and ends with a paste-ready brief. | `npx skills@latest add Wang-Cankun/known-unknowns` |

## Collection (hosted in this repo)

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [polanyi](./skills/polanyi) | Michael Polanyi as a thinking OS: a persona skill distilled from his books and papers — tacit knowledge, skill acquisition, and philosophy of science, answered in his voice. (中文) | `npx skills@latest add Wang-Cankun/cankun-skills --skill polanyi` |
| [travel-dossier](./skills/travel-dossier) | Turns a tour-agency itinerary PDF plus tickets into a phone-first A5 travel dossier (Swiss-minimal HTML→PDF), with a truth-sourcing discipline: every number in the booklet traces to a source. (中文) | `npx skills@latest add Wang-Cankun/cankun-skills --skill travel-dossier` |

## License

Each skill carries its own license (MIT unless noted).
