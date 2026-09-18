---
name: ck-verify-create
description: >-
  Establish a repeatable project verification method from real user paths,
  reusing existing checks and creating a skill only for a useful gap. Use when
  verification knowledge is missing or hard to reuse for an app, CLI, library,
  service, or analysis workflow.
license: MIT
metadata:
  group: general
  summary: >-
    Reuse project checks and, where needed, generate and prove verification
    instructions with observable outcomes and cleanup that retains evidence.
---

# Create a verification skill

Give the project a repeatable way to exercise its real interface and prove behavior. First determine what is missing from the existing verification method. When a skill is useful, write it for an agent arriving cold, mid-task. `ck-verify-<project>` is a naming pattern: replace `<project>` with a concrete project slug, such as `ck-verify-count-summary`.

Keep the generator reusable. Project commands, environment paths, reference versions, fixtures, and tolerances belong in its generated output, discovered from that project's evidence.

## 1. Identify the useful gap

Inspect the codebase and ask only for facts or judgments that cannot be found there:

- **Surface:** what does a user actually touch? Web or desktop UI, CLI/TUI, API, library calls, notebook, or workflow command? Identify the primary path and other supported entry points.
- **Run:** which project commands prepare and run it? Prefer documented scripts and declared environments. Identify readiness, required inputs, services, authentication, reference data, and expected resource cost.
- **Drive:** which existing harness can exercise that path? Reuse browser automation, CLI fixtures, PTY helpers, HTTP clients, integration tests, workflow test profiles, or public library examples. Choose available tools; neither an agent platform nor a particular connector is required.
- **Observe:** which meaningful results establish behavior? Consider screenshots, response values, terminal transcripts, stored state, output tables, numerical invariants, and logs. A successful exit or a file's existence alone rarely proves the feature.
- **Isolate:** can runs use separate ports, data directories, workspaces, profiles, or job identifiers? Record shared-resource restrictions so concurrent agents do not drive the same mutable instance.
- **Maintain:** where does this project keep reusable agent instructions? Follow its canonical source convention and requested scope. If none exists, use `skills/ck-verify-<project>/`; agent-specific deployment is a separate step. Inspect existing candidates before creating a duplicate or replacing files. If `skl` is in use, register/link the source and deploy only when that is part of the request.

Compare the requested verification with what the repository already provides. If existing scripts, tests, and instructions give an arriving agent a usable route to the required evidence, report those entry points and any limits. **No new skill needed** is a complete outcome. A one-off check may only need an existing command and a result. If an existing verification skill owns the gap, update it within scope or route to `ck-verify-maintain`.

Create a new skill when reusable knowledge is missing: how to select fixtures, drive the real interface, interpret results, or clean up safely. Wrap and link established checks. A verification skill is instructions for the existing product; a second application, service, or duplicate test framework needs a separately justified task. Add a helper only when it closes a concrete recurring gap.

Reuse relevant evidence for unchanged behavior after checking that the artifact, inputs, configuration, and assertions still match. Identify reused evidence explicitly. Determinism alone does not establish correctness; changed behavior or execution instructions need a focused new check. Choose evidence for the claim: rendering establishes visual behavior, while an existing build or data check may establish a different contract without another rendering pass.

Establish that the chosen path works before treating its instructions as proved. Diagnose startup failures; repair verification scaffolding within scope, and report product or environment blockers precisely. A temporary directory or sample config may be created as verification scaffolding when justified, named as such, and removed in cleanup. Changes to the product follow the user's task scope rather than being implied by skill creation.

For analysis workflows, start from a small representative fixture or existing test profile. Discover the environment, parameters, seeds where relevant, and reference identities needed to reproduce it. Derive expected values or invariants and justified tolerances from a documented contract, trusted reference, or hand-checkable case; do not infer correctness from matching the current implementation. Distinguish computational correctness from the scientific validity of the method or conclusion. Full production runs and large downloads require task scope and resources that actually support them.

## 2. Generate the skill

When step 1 establishes a useful gap, write the canonical `SKILL.md` with valid YAML frontmatter: the concrete `name` and a `description` naming the project, interface, and when to use it. Include the following details where the interface needs them, replacing template values with observed project facts:

- **Launch:** exact preparation and execution commands, working directory, readiness condition, and teardown. For a short-lived CLI or analysis, prepare the environment once and run each recipe in an isolated workspace. A library recipe uses its public interface. Document resource limits and external prerequisites.
- **Doctor:** read-only checks answering “is this environment or instance worth driving?” Include the relevant environment/build, available input or reference version, instance ownership, readiness, and authentication. Run these whenever behavior is surprising.
- **Drive:** actual commands, calls, or stable selectors from this repo, with input preparation and observable expectations. Prefer existing harnesses; add a small helper only for a recurring operation that the existing tools do not cover.
- **Evidence:** name a location outside disposable state and capture the setup, action, result, and comparison with expectations. Exercise the real user path, rather than internal setters or test-only endpoints. Verify material side effects alongside visible output. Use mocks at established external boundaries and state what remains untested. For a dry-run or test mode, observe which files, network calls, or external state it still touches instead of trusting the label.
- **Cleanup:** stop only processes/jobs started by the run, remove its scratch state, and restore its test fixtures. Track exact handles; avoid process-name-wide termination. Retain evidence independently of teardown. Record any shared instance that must remain running and clean only residue owned by the verification run.
- **Helpers:** scripts shipped by the skill have executable permissions, declared runtime assumptions, and explicit invocations in the body. Show how a failed assertion produces a failing result; a printed success message is not an assertion.

Write the skill in the user's requested language, with commands and identifiers preserved. Keep machine-specific deployment instructions outside the reusable verification method.

## 3. Seed the feature map

Use an existing coverage index when it already owns the recipes. Otherwise create `features/README.md`, with separate feature files only when they make the recipes easier to maintain. Start with the consequential paths that justify this skill; a small project may need only one. The index states this initial coverage and any known omissions. Include each mapped feature's supported entry points and meaningful cases, rather than implying that one convenient route proves all of them.

Use [the application example](references/feature-map-example/README.md), or [the analysis example](references/analysis-map-example/README.md) for a data workflow, when a map needs structure. Each entry explains what the feature does, how the user reaches it, how to drive it, and what observable result proves it works. Adapt the headings to the project and link existing contracts rather than imposing another documentation scheme.

Place shared preconditions, fixture reset rules, evidence conventions, and the feature index in the README. Link detailed project contracts rather than duplicating them. The feature map becomes the maintained source for verification coverage.

## 4. Prove the generated skill

Follow its own instructions end to end: launch, doctor, drive one representative mapped feature, assert the expected behavior, capture evidence, and clean up. Use all steps of that selected recipe. Confirm that evidence is still readable at the named location after cleanup. Also confirm that the run left no owned processes, jobs, or disposable state behind.

Fix verification instructions or harness failures and retry. Clean each failed attempt before moving on, retaining its relevant evidence. Product failures remain failures to report, not reasons to relax expected behavior. Mark mapped recipes not yet executed as untested; one proof establishes that the generated workflow is usable, not that all features pass.

Report the canonical skill path, the exercised recipe, observed result, evidence path, cleanup result, and untested coverage. If the environment cannot run the recipe, deliver the useful files explicitly as a **draft** with the concrete blocker and next check. An unexecuted skill is not a proved deliverable.

## 5. Offer the maintenance loop

Point to `ck-verify-maintain` to keep the skill and map aligned with the project. If that skill is unavailable, explain that maintenance compares affected recipes with source and exercises changed paths; a full audit covers the complete map. Scheduling, registration, deployment, commits, and publishing follow the user's request; generation does not imply them.

---

Adapted from Lauren Tan's [pstack create-verification-skill](https://github.com/cursor/plugins/tree/main/pstack/skills/create-verification-skill), under the [MIT License](LICENSE).
