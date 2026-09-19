# cankun-skills [![skills.sh](https://skills.sh/b/wang-cankun/cankun-skills)](https://skills.sh/wang-cankun/cankun-skills)

Agent skills by [Cankun Wang](https://github.com/Wang-Cankun), hosted in this repo under [`skills/`](./skills). This page is the index.

A skill is a `SKILL.md` playbook that an AI agent loads to follow a specific process — these work with Claude Code and any runtime that supports the convention.

## Collection

Grouped as on [cankun.me/skills](https://cankun.me/skills): general use, then design, then internal workflow.

### General use

| Skill | What it does | Install |
| ----- | ------------ | ------- |
| [ck-architect](./skills/ck-architect) | Ground the system, compare independent design sketches, and implement within the requested scope, redesigning when evidence invalidates the shape. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-architect` |
| [ck-arena](./skills/ck-arena) | Generate independent candidates, compare them against shared criteria, and synthesize a verified artifact with a concise decision record. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-arena` |
| [ck-how](./skills/ck-how) | Trace implementation, inputs, outputs, and boundaries to build a working mental model. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-how` |
| [ck-impact](./skills/ck-impact) | Trace changes across contracts and boundaries, then support consequential safety claims with focused executable evidence. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-impact` |
| [ck-prototype](./skills/ck-prototype) | Build disposable prototypes and small experiments to compare approaches through observable behavior, measurements, and concrete tradeoffs. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-prototype` |
| [ck-reflect](./skills/ck-reflect) | Turn observed experience into targeted improvements to skills, tools, and workflows. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-reflect` |
| [ck-skill-creator](./skills/ck-skill-creator) | Write focused, portable skills and improve them through proportionate checks, independent trials, and evidence-grounded comparisons. Optional helpers require Python >=3.10; metadata validation also requires PyYAML. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-skill-creator` |
| [ck-teach](./skills/ck-teach) | Combine mechanism and rationale into a clear explanation at the reader's pace. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-teach` |
| [ck-verify-create](./skills/ck-verify-create) | Reuse project checks and, where needed, generate and prove verification instructions with observable outcomes and cleanup that retains evidence. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-verify-create` |
| [ck-verify-maintain](./skills/ck-verify-maintain) | Keep project verification instructions accurate with scoped repairs or a full live audit, identifying reused evidence and remaining coverage gaps. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-verify-maintain` |
| [ck-why](./skills/ck-why) | Reconstruct rationale from evidence while separating documented intent, inference, and unknowns. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-why` |
| [ck-work](./skills/ck-work) | Start or resume a task through CK Stack, selecting useful methods and carrying authorized work to an evidenced outcome. | `npx skills@latest add Wang-Cankun/cankun-skills --skill ck-work` |
| [confer](./skills/confer) | Resumable cross-model consultation: GPT-6 Pro through Oracle by default, Claude or Codex directly, and Gemini 3.8 Flash or GLM 5.3 through Pi, with saved preferences, per-round provenance, and concurrency-safe state. Requires `bun` and at least one provider CLI; Pi models must be configured locally; Oracle requires version 0.21.1 or newer and a signed-in ChatGPT browser profile. | `npx skills@latest add Wang-Cankun/cankun-skills --skill confer` |
| [deposition](./skills/deposition) | Ground a plan, decision, or idea in evidence, then examine consequential choices through focused question rounds, concrete alternatives, and a visible decision tree. | `npx skills@latest add Wang-Cankun/cankun-skills --skill deposition` |
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

## CK Stack

CK Stack adapts [Lauren Tan’s pstack](https://github.com/cursor/plugins/tree/main/pstack) into portable workflows for software and analysis projects, alongside `deposition` and `confer`. Adapted skills retain their upstream MIT license and attribution. The instructions use the tools and agent capabilities available in the current environment; project paths, environments, reference data, and acceptance criteria belong in the consuming project.

| Need | Skills | Result |
| ---- | ------ | ------ |
| Start or resume | `ck-work` | Recovered task state, selective skill routing, and completion supported by project evidence |
| Understand | `ck-how`, `ck-why`, `ck-teach` | Traced mechanics, evidence for historical choices, and a clear explanation |
| Explore | `deposition`, `ck-prototype` | Settled decisions and small experiments that distinguish approaches |
| Design and build | `ck-arena`, `ck-architect` | Independent candidates, a coherent synthesis, and verification within the requested scope |
| Consult a peer | `confer` | A named model's advisory response and a resumable consultation thread |
| Assess impact | `ck-impact` | Downstream failure mechanisms and focused evidence for compatibility assumptions |
| Learn and improve skills | `ck-reflect`, `ck-skill-creator` | Evidence-grounded repairs and portable skills checked in representative tasks |
| Verify repeatedly | `ck-verify-create`, `ck-verify-maintain` | Reused checks or a project-owned verification method, maintained within a declared scope |

Use `ck-work` when you want the stack to coordinate a task or resume one from its existing state. It selects the next useful method, carries forward settled decisions and applicable evidence, and returns to the original acceptance conditions after review. Directly invoked skills remain independent; this is not a mandatory sequence. `ck-teach` composes `ck-how` and `ck-why`. `ck-architect` uses `ck-how`, `ck-arena`, and, when historical rationale matters, `ck-why`. Install those companions together when using a composed workflow. `obelisk` can supply historical leads when available; it is optional.

`ck-arena` produces and judges independent candidates for an artifact. `confer` asks a peer model for advice and preserves the dialogue across rounds. A peer's agreement does not replace the arena's comparison or the project's verification.

`ck-reflect` finds lessons and the owner of each repair; `ck-skill-creator` handles substantive authoring and evaluation. The creator integrates writing guidance, scoped authoring, independent trials, and blind comparisons without requiring the source skills to be installed. Wording fixes get focused checks, substantive behavior changes get representative trials, and claims of improvement get matched comparisons. Its optional static review viewer retains Anthropic's Apache-2.0 license; see [source and license notes](./skills/ck-skill-creator/NOTICE.md).

`ck-verify-create` first checks whether existing tests and documentation already give an agent a repeatable verification path. When a reusable gap remains, it generates a concrete skill such as `ck-verify-count-summary`. The name `ck-verify-<project>` is a template, not another global skill to install. The generated skill stays with its project and records that project's commands, inputs, expected outputs, and cleanup. Its Feature Map links user capabilities to entry points, required state, observable outcomes, and reusable verification recipes. Features and recipes can have a many-to-many relationship; source and entry-point discovery catch features not yet mapped. Keep this navigation current when capabilities change, and keep run-specific results with their evidence. `ck-verify-maintain` distinguishes a scoped repair from a full-map audit and reports only the coverage actually established. Computational checks and scientific validity remain distinct.

### Install and maintain the CK Stack plugin

The [CK Stack plugin](./plugins/ckstack) bundles the twelve `ck-*` skills, `deposition`, and `confer` into one installable package. It includes a portable `plugin.json` and a Codex compatibility manifest; no MCP server or hooks are required. `confer` additionally needs Bun and the selected provider CLI and authentication, as described in [its requirements](./skills/confer/SKILL.md). Keep editing the canonical files under `skills/`. The plugin directory is generated and contains real files so it remains complete when installed outside this checkout.

The package definition in [`packaging/ckstack.json`](./packaging/ckstack.json) owns membership, version, and presentation. Build and check the distributable with:

```sh
python3 scripts/build_plugins.py
python3 scripts/build_plugins.py --check
```

For a personal installation, first generate the source directory at `~/plugins/ckstack`:

```sh
python3 scripts/build_plugins.py --output-dir ~/plugins/ckstack
```

Register that existing package in `~/.agents/plugins/marketplace.json` using the built-in `plugin-creator`'s marketplace helper. This registration step runs once; it does not scaffold files over the generated package:

```sh
python3 -B - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path.home() / ".codex/skills/.system/plugin-creator/scripts"))
from create_basic_plugin import update_marketplace_json
update_marketplace_json(
    marketplace_path=Path.home() / ".agents/plugins/marketplace.json",
    marketplace_name=None,
    plugin_name="ckstack",
    install_policy="AVAILABLE",
    auth_policy="ON_INSTALL",
    category="Developer Tools",
    force=False,
)
PY
codex plugin add ckstack@personal
```

Use the marketplace's actual name if the existing personal catalog uses another name. During local iteration, regenerate the personal source directory and use `plugin-creator`'s cachebuster/reinstall flow. Its current helper updates the compatibility manifest only: copy that resulting version into the personal package's root `plugin.json` before reinstalling so both identities stay aligned. Test in a new conversation. For published package changes, update the version in the package definition and regenerate. Installing into a local marketplace is separate from publishing to a ChatGPT workspace or the public plugin directory.

The builder refuses unknown files in an existing output directory. When removing or renaming packaged files, inspect and move the obsolete output files before rebuilding; it never deletes them automatically.

After confirming that the installed plugin contains all fourteen skills and references, remove their individual Codex deployments to avoid loading both forms:

```sh
skl drop ck-work ck-how ck-why ck-teach ck-prototype ck-arena ck-architect ck-impact ck-reflect ck-skill-creator ck-verify-create ck-verify-maintain deposition confer --agent codex --global
```

This removes the deployment links, preserving the skillshelf library and canonical source. Individual skill installation remains available for hosts or projects that use it.

### Maintain individual skills with skillshelf

This repo is the canonical source. For local development, register a linked library entry for each desired skill, then activate the named skills in the consuming project:

```sh
# From this repo; repeat for the skills you want to maintain.
skl link --from "$PWD/skills/ck-how"
skl tag ck-how ck-stack

# From the consuming project; register the companions first.
skl use ck-how ck-why ck-teach --agent codex
```

Use `--agent claude` or the appropriate agent identifier for other supported hosts. The dedicated `ck-stack` tag groups the collection without adding it to a broad existing bundle. Registration and activation are separate; neither requires creating a project-specific verifier in advance. Update the source here and review upstream changes deliberately, because `skl update` skips linked entries.

## License

Each skill carries its own license (MIT unless noted); see [`LICENSE`](./LICENSE).
