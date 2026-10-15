---
name: ambition
metadata:
  group: thinking
  summary: Rewrite a clear task into one more ambitious assignment, combining the altitude, depth and range that fit, with access needs and evidence of success.
description: "Rewrite a clear task into one more ambitious assignment using every applicable lens: altitude, depth and range. Use when a task may be aimed too low, when the user asks to think bigger or go deeper, or before committing to substantial work."
---

# Ambition

Inspired by [Felix Rieseberg's discussion of using models for more ambitious work](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

Start with a clear task; settle its purpose first if needed. Use the lenses below to build one
rewritten assignment. Apply every lens that improves the task, and stack useful techniques
within each. Preserve the user's purpose and constraints.

## Speed

Briefly state what completing the original task faster would produce. Use that as a reference
for explaining what the rewrite adds; speed needs no separate creative treatment or proposal.

## Altitude

Altitude fits work aimed at an outcome, especially a deliverable used in a meeting or decision.
It is less useful when the creative artifact itself is the goal. An abstract wish such as
"grow revenue" still needs an actionable objective.

Ask what the deliverable enables, then what that next step serves. Climb toward an outcome the
agent can act on and verify. The rungs build on one another:

- explain the findings and recommend action alongside the requested artifact;
- identify the decisions those findings call for, with the case for and against possible actions;
- design a better way to achieve the underlying purpose, check it against past records, and
  trial it beside the existing process before proposing replacement.

For recurring requests, consider an ongoing responsibility, such as maintaining an app's
reliability, with the access needed to observe problems and verify fixes.

## Depth

Depth fits an assignment whose value comes from exceptional execution. Work further into its
foundations, with a standard high enough to teach a leading practitioner something:

- Use professional instruments: name the methods, tools and least-processed source material
  an expert would actually use. A change of vocabulary does not improve the method.
- Set a demanding concrete target beyond the initial request; treat apparent difficulty as a
  reason to investigate how to reach it.
- Reconstruct assumptions from source data and actively seek contradictory evidence.
- Extend that investigation into discovery: look for an unrecognized pattern, then test its
  predictions on observations excluded from developing it.
- Choose an independent judge, preferably an executable check that gives prompt feedback.

## Range

Range fits work where another discipline can improve the result. Describe the actions and
beliefs the artifact should enable, for whom and under which constraints. Use those verbs to
find useful disciplines beyond the obvious one. Name each discipline's method and contribution,
including an adversarial examination of the result. Specify real work, such as tracing numerical
claims to original records, rather than asking for a performance of an expert persona. Separate
specialists can do this work when the execution environment supports them.

## Deliver one rewritten task

Give a short line for each lens: speed as the reference, and why altitude, depth and range are
each used or skipped. Combine all applicable lenses into one prompt the user can approve, cut
or edit. The prompt should name the work to do, not merely describe how ambitious it sounds.
If no lens adds value, keep the original scope and explain why.

For every rewrite, specify the computer access needed to install software and reach relevant
data. Name the sources, tools and reproduction environments concretely, and distinguish
available access from access still needed. State what observable evidence would demonstrate
success, including the independent checks the proposed work will use.

End with the proposal for the user's approval. Proposing the rewritten task grants no permission
to begin it; wait for the user to approve the revised scope before execution.

## Example

Task: write release notes for version 2.4 of a library.

- **Speed reference:** drafting from merged pull-request titles would produce notes quickly.
- **Altitude used:** users need an upgrade decision and migration steps from those notes.
- **Depth used:** diffs and executable comparisons can reveal changes that titles miss.
- **Range used:** support analysis and adversarial migration trials expose affected users and
  failures that a release summary may overlook.

**Rewritten task:** Prepare the 2.4 release notes so users can decide whether to upgrade and
carry out the migration. Inspect the diffs, map relevant support issues to affected usage, and
compare the previous release with 2.4 on representative sample projects. Attempt migrations
that challenge the proposed guidance. Use the results to explain compatibility, required edits
and remaining uncertainties, with links from each claim to its source or reproduction.

**Access needed:** a computer with repository and issue access, both library versions, sample
projects, and permission to install their dependencies in an isolated test environment. Confirm
which of these are available before executing the approved task.

**Success evidence:** saved comparison results demonstrate the compatibility claims, the sample
migrations pass with the documented edits, and unresolved failures are visible in the notes.

**Approval:** Ask the user to approve, trim or edit this combined task before starting.
