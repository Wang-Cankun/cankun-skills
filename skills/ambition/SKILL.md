---
name: ambition
metadata:
  group: thinking
  summary: Rethink a clear task through speed, altitude, depth and range, and recommend the version worth doing.
description: "Rethink a clear task through four kinds of ambition (speed, altitude, depth, range) and recommend the version worth doing. Use when a task may be aimed too low, when the user asks to think bigger or go deeper, or before committing to substantial work."
---

# Ambition

Based on Felix Rieseberg's [How to be more ambitious: a tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).
It sorts ambition into four kinds:

- **Speed**: the same work in less time.
- **Altitude**: aim at the outcome beyond the task.
- **Depth**: do the task the way a field-leading expert would, down to the raw data and tools.
- **Range**: draw on fields the task does not obviously need.

They are lenses on one task, not a menu: the recommendation combines whichever earn their place.

## Think it through

Start from a task whose purpose is clear; if it is not, settle the purpose first. Write the
reply as a short argument applied to this task, in this order.

1. **Turn the noun into a verb.** The deliverable is a noun: a deck, a pipeline, release notes.
   Say what it must do, to whom: a quarterly review is getting busy people to believe a
   cause-and-effect story and decide under uncertainty. Done when the sentence names the person
   and the change in them, and the original format is no longer the only answer. When the verb
   shows the real problem is elsewhere, open the reply with that reframe in one sentence.
2. **Speed as the reference.** One line: what doing the task as given, faster, would produce,
   and what it leaves unsolved. The other three lenses are measured against it.
3. **Altitude, depth, range.** A short paragraph each, concrete to this task: name the data,
   tool, field or step. When a lens adds nothing worth its cost, say why in one line.
   - **Altitude.** Ask what should happen after the deliverable, then what that serves. Climb
     to an outcome the agent can act on and check. It fits work headed for a meeting or a
     decision, and fits creative work less. A recurring task can become a standing
     responsibility once the agent can observe the problem and verify its own fixes.
   - **Depth.** Say what a top practitioner would do here that the task does not ask for: the
     rawest material they would start from, the methods and instruments they would use (new
     vocabulary is not a new method), the belief they would try to reproduce from raw data, and
     what other than the model would show the result is right. A demanding target is fair;
     treat difficulty as a reason to keep going.
   - **Range.** From the verb, find the fields that do that action well, beyond the obvious one.
     For each, name what its people would actually do here (a forensic accountant traces each
     number to its record; an editor cuts what does not change the decision), including one
     field that attacks the result. Ask for their work, not their voices.
4. **Recommend one version.** Combine the lenses that earned their place and say why the result
   beats the reference. Prefer the smallest version that captures the gain, with cheap,
   reversible steps first. If a bigger version is tempting but premature, name it and the
   evidence that would justify it later. Name the data and tool access it needs that is not
   already at hand.
5. **Say how you will know.** Match the check to the stakes: one line on what the user will see
   for a light task; for work where a wrong result is costly, a first proof point, what would
   falsify the version, and an outside judge, ideally a check the agent can run itself.

End by offering the cheapest first step that tests the recommendation, and wait for the user's
yes before starting.

## Example

Task: write release notes for version 2.4 of a library.

> **Reframe:** the notes are for people deciding whether to upgrade, so the risk lies in
> breaking changes that the PR titles hide.
>
> **Verb:** let users decide in a few minutes whether to upgrade, and migrate without surprises.
>
> **Speed:** a draft from merged PR titles in minutes; vague titles hide breaking changes.
>
> **Altitude, deferred:** a codemod that performs the migration. Worth it only if the trial
> migrations below repeat the same mechanical edit across projects.
>
> **Depth:** diff the public API between 2.3 and 2.4 instead of reading titles, and run two
> sample projects' test suites against 2.4.
>
> **Range:** a support engineer maps open issues to the changed APIs; a tester follows the
> migration guide literally on the sample projects and records where it breaks.
>
> **Recommendation:** depth and range together: notes built from the API diff, with a
> migration guide proven on the two samples. **Check:** both samples upgrade by following the
> notes alone. **First step:** the API diff, read-only and minutes long. Start there?
