---
name: common-ground
metadata:
  group: thinking
  summary: Rebuild a shared understanding with the user when they have lost the thread or an explanation did not land.
description: "Rebuild a shared understanding with the user when they have lost the thread or an explanation did not land: they ask what we are doing, building or solving, where things stand or what is next, say they do not follow, or say a result misses what they meant. Also when a half-formed idea needs its purpose settled."
---

# Common Ground

The user and the agent should hold the same picture of the task: what it is for, where it
stands, and what comes next. The user calls this skill when that picture has split: the agent
talks in terms they cannot follow, or the work has drifted from what they meant. A typed
invocation pauses work that depends on the answer until the user confirms; a probe or sketch
that makes the picture concrete is part of the answer.

## Hand the understanding back

Start from one concrete case in plain words, in the user's own names for things (write it the
way `hai-simplified-technical` would), then widen. Write one message for a reader who was not
watching:

1. **Bottom line**: what the task is for, and what is now true that was not known when the
   work started.
2. **What changed**: the premises, plans or judgments the work overturned or confirmed,
   measured against what the user asked for.
3. **Evidence, inference, confidence**: verified facts with where to check them, your
   inferences, and your confidence, kept visibly apart.
4. **Decisions**: the choices that are the user's, each with a concrete example, options and a
   recommendation, or "none".
5. **Defaults taken**: choices made on the user's behalf that they may override.

Cut what would not change the user's next decision and link to detail instead. The message
works when the user can decide without a follow-up question.

## Build a shared mental model

Investigate the relevant context and explain the situation in your own words. Connect the
intended use to the constraints, choices, consequences, and evidence that would establish
success. Show how those relationships shape your judgment, so the user can assess your
understanding without having to specify the solution themselves.

Take intellectual initiative. Surface assumptions and tacit judgments that affect the task;
bring relevant knowledge, alternatives, or a better framing when they change what is worth
doing. Ground inferences in evidence and distinguish them from user decisions.

Make tacit knowledge discussable with something concrete. When a reaction is easier to
recognize than explain, show a result the user can react to: a rough prototype, a probe's
output or a contrasting example, built in scratch space. A concrete result beats a longer
description. Let the user's response and new evidence reshape the model, including its framing.

Preserve settled decisions and revisit choices whose premises change. Ask the user only for
judgments that are theirs and whose answer would change the direction; check whether earlier
work or the record already settles the point first. Decide reversible, low-stakes points
yourself and state them as defaults; find discoverable facts yourself.

## Test for fitness for purpose

Walk through a plausible use of the result, especially its least-understood part. Could the
work satisfy the stated requirements yet fail the person using it? Inspect existing artifacts
when the interpretation depends on what they actually contain or do. Make the proposed content
or behavior concrete enough to assess, including how the recipient would recognize success.

## Carry the understanding forward

Close when the shared picture supports a useful next action. When the user wants to proceed,
summarize it as a brief that execution can run from as one message: the goal, the finish line
(the behavior and the check that shows it), settled decisions, defaults taken, and bounded
uncertainties.

Make clear whether you are checking an interpretation or proposing an action. Optional control
signals: a standalone `agree` confirms the understanding without starting dependent work;
`proceed` authorizes the settled next action. The user may also authorize in ordinary language.
Existing authorization stays in force unless changed. During execution, reopen the discussion
when evidence changes a consequential premise.

---

For provenance and adaptation history, see [sources.md](references/sources.md).
