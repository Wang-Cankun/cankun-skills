---
name: ambition
metadata:
  group: thinking
  summary: Propose more ambitious versions of a clear task (altitude, depth, range) against the speed baseline, and recommend one.
description: "Propose more ambitious versions of a clear task (altitude, depth, range) against the speed baseline, and recommend one. Use when a clear task may be aimed too low, when the user asks to think bigger or go deeper, or before committing to a plan for substantial work."
---

# Ambition

Inspired by [Felix Rieseberg's discussion of using models for more ambitious work](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

Start with a clear task; if its purpose is unclear, settle that first. Compare the kinds below
where they change the work. They can combine; they are not a quota of versions to produce. Each
section describes what a proposed version would ask for.

## Speed

The familiar task done faster: the baseline every other version must beat.

## Altitude

Altitude fits outcome-driven work and suits creative work poorly. A tell: the deliverable will be
discussed in a meeting or used for a decision. An open-ended wish ("grow revenue") is not yet an
objective anyone can act on.

Ask what should happen after the deliverable, and what that in turn serves. Climb one rung at a
time, and stop at the highest rung where the agent can still act and verify the result:

- the deliverable together with the explanation and recommendation it implies;
- the decisions it feeds: the most pressing ones, each with options argued for and against;
- the purpose the deliverable exists for: a better mechanism than the deliverable itself, tested
  against the user's own history and run alongside the current process before it replaces it.

When the same request keeps coming back, propose a standing responsibility the agent owns
("keep X healthy") in place of one task per occurrence.

## Depth

Use depth when the task should be done exceptionally well. Go deeper into the same assignment
rather than making it bigger, and set the bar where the field's best practitioners would learn
something from the result:

- Instruments: the tools, methods and least-processed inputs a leading practitioner would use.
  Switching to expert vocabulary is not switching method.
- An unreasonable goal, far past what was asked, stated as reasonable. When the work looks
  impossible, the version says it is solvable and the agent continues.
- Challenge assumptions: rebuild the working beliefs behind the task from the underlying data,
  and look for evidence against them.
- New knowledge: once inside that data, look for what nobody has noticed, and show that the
  finding predicts data held out from building it.
- An outside judge, ideally a check the agent can run for fast feedback, so the producing model
  never grades its own work.

## Range

Turn nouns into verbs: say what the deliverable must get which people to believe or do, and under
what constraints. Use those verbs to pick fields beyond the task's own, more of them than would
once have been worth the cost. For each specialty, name the method it brings and what it adds,
and include a red team that attacks the result. Each specialty does its actual work (a
fact-checker traces every figure to a source) instead of role-play. Where the agent can run
subagents, give each specialty its own.

## Example

Task: write release notes for version 2.4 of a library.

- **Speed:** draft the notes from the merged pull-request titles.
- **Altitude:** tell each user whether to upgrade and what they must change; one rung up, check
  every pull request for an upgrade note so release notes assemble themselves.
- **Depth:** classify each change from the diff rather than its title, run the old and new
  versions against sample projects, and let that run judge which changes break.
- **Range:** the verb is "let each user upgrade safely": add a support engineer who reads open
  issues for affected users, and a red team that upgrades a real project and reports what failed.

## Make the choice usable

Recommend a version, including speed if it best serves the user, and explain what changes in the
work. The comparison is ready when the user can choose and the recommendation includes a rewritten
task, the access it needs and evidence of success.

Versions beyond speed usually need a computer where the agent can install software and reach the
relevant data. For the recommended version, list that access concretely: data sources, tools to
install, and the machines or environments to reproduce and verify on.

Proposing a version does not authorize starting it. Carry the chosen task into execution within
existing authorization.
