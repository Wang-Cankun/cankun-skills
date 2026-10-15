---
name: ambition
metadata:
  group: thinking
  summary: Decide which version of a clear task is worth doing — higher, deeper or wider — before the work starts.
description: "Offer more ambitious versions of a task that is clear but may be aimed too low: the outcome beyond it, the expert-depth version, or the version another field would do. Use only when the user invokes it."
---

# Ambition

Adapted from Felix Rieseberg's ["How to be more ambitious: a tutorial for humans with models"](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

Ambition here is about the target and the depth of evidence, not the size of the build. A more
ambitious version still takes the simplest mechanism that meets it.

## Steps

1. **State the task as given** and the version that would be done by default. Done when the
   default is concrete enough to compare against.
2. **Turn the noun into a verb.** Rewrite the deliverable as what it must do to whom: a quarterly
   review becomes getting busy people to believe a cause-and-effect story. Done when the sentence
   names the person, the change in them (believe, decide, understand, reproduce), and the original
   format is no longer the only answer.
3. **Build the versions** that differ materially from the default; skip any that would not:
   - **Higher.** Work backward from the desired end state: what should happen beyond this task,
     and what would make it unnecessary next time. Compare with starting fresh to expose inherited
     constraints. Name the data and tool access the work would need.
   - **Deeper.** How the best practitioner would do it: their rawest inputs (raw data, not the
     summary table), their instruments, a claim to reproduce or a model to test on unseen data,
     and an outside judge of the result — never the model grading itself.
   - **Wider.** From the verb, list the fields that do that action well and what each would
     *do* here (an editor cuts, a short seller hunts for the weak claim, an auditor reconciles).
     Ask for their actions, not for role-play. Connect a familiar principle to this situation;
     use a counterexample or a different perspective to expose a premise that could change the
     target. Explain what the connection changes, without assuming the user already knew it.

   If a judgment is hard to express, offer a contrasting example or candidate formulation for
   the user to correct. Treat the interpretation as a hypothesis; follow it only while it could
   change the choice of version. Investigate gaps that could reverse the recommendation and
   name what evidence would settle them; keep unresolved claims provisional.

   Done when each version names its first proof point, what would falsify it, and its cost over
   the default.
4. **Check each inherited constraint** a version breaks. Real: a public contract, persisted
   data, a user promise, a deployment or compliance limit, an explicit instruction. Not enough:
   internal callers, old naming, existing partial work, a large diff. Name the actual obligation
   and evidence; if uncertain, name the check rather than declaring the constraint unreal.
   Treat migration cost separately from the target's value. Done when each challenged constraint
   has a reason to preserve it, remove it, or investigate it.
5. **Recommend one** (the default is allowed). Name what should be deleted, merged, split or
   reframed when it changes the target: deletion of a wrong concept is a design choice, not
   cleanup deferred to execution. Separate the chosen end state from any staged path to it.
   Explain the concrete pain removed or capability unlocked, its added cost, and when the gain
   would become visible. Mark uncertainty and the first irreversible commitment where relevant.
   Done when the user can pick, and the pick carries its finish line and proof point.

## Carry it forward

Hand the chosen version to [common-ground](../common-ground/SKILL.md) as the task to align on,
or straight to execution when the user says so. This skill proposes; it does not start the larger
version without the user's choice.

## Use a different skill when

- The purpose itself is unclear, or the finish line needs agreeing: `common-ground`. Ambition
  starts from a task that is already clear.
- The version is chosen and the question is who runs it in Herdr panes: `crew`.
- One judgement needs a second model's opinion: `confer`.
- The work is writing or revising a skill: the skill-authoring skill. Ambition can still pick
  which version of that skill is worth building.
