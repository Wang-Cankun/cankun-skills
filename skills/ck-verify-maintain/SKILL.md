---
name: ck-verify-maintain
description: >-
  Audit and repair a project's existing verification skill, harness, and feature
  map against source and live behavior. Use when verification recipes drift or
  need a coverage audit; create a missing verification skill with ck-verify-create.
license: MIT
metadata:
  group: general
  summary: >-
    Keep project verification instructions accurate through source inspection,
    live recipe coverage, proved repairs, and explicit reporting of gaps.
---

# Maintain a verification skill

Keep the verification map useful as its project changes. Cover every mapped recipe from source and actual execution. Use the project's own interface: an application, CLI, service, public library, or analysis workflow. This skill maintains an existing verification method; project-specific commands and acceptance criteria belong to that method.

## Outcomes and edit scope

Report one outcome:

- **clean** — every mapped recipe has source and live coverage, expectations passed, no material coverage gap remains, and no corrections are needed.
- **changed** — every mapped recipe has passing source and live coverage, no material coverage gap remains, and doc, harness, or map corrections have been proved by re-execution.
- **blocked** — a recipe could not be exercised, a product failure or material coverage gap remains, or a correction could not be proved. This includes a newly discovered material feature that has not been mapped and exercised. Retain useful repairs but identify each unresolved item and the check needed to complete it.

Edit only the verification skill's own directory: its instructions, feature map, and helpers it owns. If a referenced harness lives elsewhere, report the required change or follow explicit user authorization to change it. Classify changed behavior from source, intended contracts, and observed results: doc drift can be corrected; a product regression is reported and its expectation preserved. Keep product fixes separate from this maintenance task.

## Pass

### 1. Locate and index

Find the canonical project verification skill through repository instructions and skill conventions, including linked sources where applicable. Look for launch/drive instructions and a feature map; do not assume an agent-specific directory. Several plausible targets require disambiguation unless the user's context identifies one. With no target, point to `ck-verify-create` and report that maintenance has nothing to inspect.

Read the feature index and enumerate its sibling files. Repair missing, extra, duplicate, or dead links. Build a compact scratch coverage ledger of the mapped recipes and entry points; keep it outside committed skill content.

### 2. Read source

Inspect each feature against source. When independent agents are available, assign one read-only source review per feature concurrently; otherwise perform the reviews sequentially. Source reviewers neither drive the system nor edit files. Each returns: feature summary, source entry points, likely drift with citations or none, and concise live recipes covering the entry points and assertions in that feature.

Require a returned summary for every feature file. Spot-check cited drift and reconcile overlapping recipes into as few environment states as practical. Sweep recent changes for missing user-facing surfaces; call one missing only with a concrete source path. Add newly found material features to the map and coverage ledger, or report them as an explicit coverage gap.

### 3. Exercise the map

Live execution is required even when the source appears consistent. One coordinator owns mutable sessions. Follow the skill's launch model: a serially driven long-lived instance for a server or UI, or isolated runs for CLI commands, library calls, and analysis jobs. Exercise each mapped entry point and meaningful assertion, sharing setup where possible. A result through one route does not prove another route. Track coverage at the recipe level without treating every explanatory bullet as a separate test.

Use representative fixtures and test profiles for expensive workflows. Record the actual parameters, environment and reference versions relevant to interpretation, and compare meaningful output values or invariants with justified expectations. Successful execution alone does not establish computational correctness, and computational correctness alone does not establish scientific validity. If a required check needs production-scale compute, unavailable data, or an external prerequisite outside the task's scope, keep it as a coverage gap.

Maintain these invariants throughout the run:

- **Healthy starting state:** doctor before the first drive, for each fresh session where sessions are the unit, and after any surprising result. If doctor cannot detect a wedged interactive state, reset or relaunch to a known state. A doctor failure caused by skill drift is repairable within scope; fix it and retry once, restarting what the change invalidates, before reporting blocked.
- **Durable evidence:** capture actions, assertions, observed results, and material side effects. Confirm collected evidence remains readable at its named location after every cleanup. Retain failure evidence as well as successful re-proofs.
- **Owned cleanup:** nothing started by a drive outlives its usefulness. Remove failed-attempt residue and stop only owned instances or jobs, using exact handles. Clean owned residue from a shared instance without stopping that instance. Perform final teardown after all re-proofs.

Record an unreachable route with the attempted action and concrete missing prerequisite, such as authentication, platform support, input data, or an external service. It remains unverified. If the prerequisite is missing from the map, repair that documentation too.

### 4. Triage and re-prove

- Wrong or missing user-facing description: correct doc drift with source and observed behavior as evidence.
- Working behavior the harness cannot drive: repair the owned harness or report the external harness gap. Helpers must be executable, with invocation and runtime requirements documented.
- Actual behavior violates its intended contract: report the product gap with reproduction evidence, retaining the expectation.

Re-execute every changed recipe and every affected path of a harness repair. Re-read every changed file and verify its links. Complete final cleanup and confirm evidence retention. Unrelated passing features do not establish that a repair works.

### 5. Report and deliver

Report outcome, changed files, coverage by recipe or entry point, observed product failures, unreachable prerequisites, evidence location, and cleanup status. Keep concise run notes in the named evidence or scratch location; do not add transient run records to the maintained skill. State any remaining gap directly rather than counting it as a pass.

Local proved corrections are the default deliverable. Commit, push, open a PR, deploy, or schedule another pass only when included in the user's request. Use the project's normal workflow when those actions are authorized.

---

Adapted from Lauren Tan's [pstack maintain-verification-skill](https://github.com/cursor/plugins/tree/main/pstack/skills/maintain-verification-skill), under the [MIT License](LICENSE).
