---
name: ck-verify-maintain
description: >-
  Maintain a project's verification skill, harness, and feature map after a
  concrete change, or audit the full map against source and live behavior. Use
  when verification recipes drift or need a coverage audit.
license: MIT
metadata:
  group: general
  summary: >-
    Keep project verification instructions accurate with scoped repairs or a
    full live audit, identifying reused evidence and remaining coverage gaps.
---

# Maintain a verification skill

Keep the verification map useful as its project changes. Use the project's own interface: an application, CLI, service, public library, or analysis workflow. This skill maintains an existing verification method; project-specific commands and acceptance criteria belong to that method.

## Scope and outcomes

Choose the scope from the request before running checks:

- **Scoped maintenance:** a concrete change or stale recipe defines the affected paths. Trace shared setup, assertions, and helper consumers to include any paths the change can invalidate. Other recipes remain outside this pass.
- **Full-map audit:** the user requests a full audit or a verdict on the whole verification map. Inspect and exercise every mapped recipe and supported entry point, and check for material missing coverage.

When the request only names a concrete repair, use scoped maintenance. If it requests maintenance without identifying a scope, inspect recent changes to bound a useful pass; clarify only when choosing full or scoped would materially change the requested verdict or resource cost.

Report the chosen scope with one outcome:

- **clean** — the declared scope needs no correction and its required checks passed. A **full-map clean** verdict requires current source and live coverage of every mapped recipe, with no material coverage gap. A **scoped clean** verdict names the covered paths and makes no claim about the rest.
- **changed** — corrections within the declared scope are proved and no required check remains open there. A full-map result has the same complete live coverage requirement as full-map clean.
- **blocked** — a required in-scope check could not be completed, a product failure or material coverage gap remains, or a correction could not be proved. Retain useful repairs and identify each unresolved item and the next useful check. Untouched paths outside a scoped pass are coverage limits, not automatically blockers.

Edit only the verification skill's own directory: its instructions, feature map, and helpers it owns. If a referenced harness lives elsewhere, report the required change or follow explicit user authorization to change it. Classify changed behavior from source, intended contracts, and observed results: doc drift can be corrected; a product regression is reported and its expectation preserved. Keep product fixes separate from this maintenance task.

## Pass

### 1. Locate and index

Find the canonical project verification skill through repository instructions and skill conventions, including linked sources where applicable. Look for launch/drive instructions and a feature map; do not assume an agent-specific directory. Several plausible targets require disambiguation unless the user's context identifies one. With no target, point to `ck-verify-create` and report that maintenance has nothing to inspect.

Read the existing coverage index and its linked recipes, whether they live in one file or separate feature files. Repair in-scope missing, duplicate, or dead links. Build a compact scratch ledger of the recipes and entry points included in this pass, and name what remains outside it. Keep the ledger outside committed skill content.

### 2. Read source

Inspect each in-scope feature against source. Delegate independent source reviews when breadth makes that useful; a small repair can be reviewed directly. Source reviewers neither drive the system nor edit files. Each returns: source entry points, likely drift with citations or none, and the checks covering affected entry points and assertions.

Account for every in-scope recipe. Spot-check cited drift and reconcile overlapping recipes into as few environment states as practical. Sweep relevant changes for missing user-facing surfaces; call one missing only with a concrete source path. Add newly found material features to the map and ledger when they belong to this pass, or report the gap and its scope explicitly. A full audit includes every material gap found.

### 3. Exercise the required paths

For a full-map audit, live execution of every mapped recipe is required even when source appears consistent. For scoped maintenance, execute changed behavior and any recipe whose commands, setup, assertions, or helper behavior changed. Reuse evidence for unchanged paths only after checking that the tested artifact, inputs, configuration, and assertions still apply; record that rationale and distinguish reused evidence from this run's execution. Source inspection or a deterministic script alone does not establish a passing result.

Choose checks for the actual claim. A wording or link repair with unchanged execution can be proved by source and link checks plus applicable existing evidence. A visual behavior change needs visual evidence; an unrelated metadata correction does not automatically require rendering the product again.

One coordinator owns mutable sessions. Follow the skill's launch model: a serially driven long-lived instance for a server or UI, or isolated runs for CLI commands, library calls, and analysis jobs. Exercise the required entry points and meaningful assertions, sharing setup where possible. A result through one route does not prove another route. Track coverage at the recipe level without treating every explanatory bullet as a separate test.

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

Re-execute recipes whose execution or expectations changed and every affected path of a harness repair. For wording and link corrections, use the evidence rule in step 3. Re-read every changed file and verify its links. Complete final cleanup and confirm evidence retention. Unrelated passing features do not establish that a repair works.

### 5. Report and deliver

Report scope and outcome together, changed files, coverage by recipe or entry point, current versus reused evidence, observed product failures, unreachable prerequisites, evidence location, and cleanup status. For scoped maintenance, name untouched or unverified coverage explicitly. Keep concise run notes in the named evidence or scratch location; do not add transient run records to the maintained skill. State any remaining gap directly rather than counting it as a pass.

Local proved corrections are the default deliverable. Commit, push, open a PR, deploy, or schedule another pass only when included in the user's request. Use the project's normal workflow when those actions are authorized.

---

Adapted from Lauren Tan's [pstack maintain-verification-skill](https://github.com/cursor/plugins/tree/main/pstack/skills/maintain-verification-skill), under the [MIT License](LICENSE).
