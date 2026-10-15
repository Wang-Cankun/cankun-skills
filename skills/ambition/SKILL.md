---
name: ambition
metadata:
  group: thinking
  summary: Rethink a clear task through speed, altitude, depth and range, and recommend the version worth doing.
description: "Rethink a clear task through four kinds of ambition (speed, altitude, depth, range) and recommend the version worth doing. Use when a task may be aimed too low, when the user asks to think bigger, go deeper or aim higher (更有野心, 拔高, 做深), or before committing substantial work to an ask that names an artifact rather than the outcome behind it. Skip small or fully specified tasks, and requests that only want it faster."
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
3. **Altitude, depth, range.** A lens earns a short paragraph only when it changes what gets
   done, and then names the concrete data, tool, field or step. Put the remaining lenses
   together in one line that says why they are not used.
   - **Altitude.** Ask what should happen after the deliverable, then what that serves. Climb
     to an outcome the agent can act on and check. It fits work headed for a meeting or a
     decision, and fits creative work less. A recurring task can become a standing
     responsibility once the agent can observe the problem and verify its own fixes.
   - **Depth.** It fits when the value lies in doing this one thing exceptionally well. Name
     the rawest material a top practitioner would start from instead of the digested version,
     and the methods and instruments they would use; new vocabulary is not a new method. When
     the task rests on a belief the raw data can test, try to reproduce the belief from it.
   - **Range.** From the verb, find the fields that do that action well, beyond the obvious one.
     For each, name what its people would actually do here (an editor cuts what does not change
     the decision), including one field whose trade is finding what is wrong, applied to the
     result itself (a forensic accountant traces each number to its record). Ask for their
     work, not their voices.
4. **Recommend one version.** Combine the lenses that earned their place and say why the result
   beats the reference. Adding deliverables without raising what they show is bigger, not more
   ambitious. Prefer the smallest version that captures the gain. Write it as an assignment
   people can meet:
   - a specific, hard target, with a number where one fits; difficulty is a reason to look for
     the route, not to lower the target;
   - a precedent when one exists: someone who has done the equivalent;
   - room to fail: a new way runs beside the old one before replacing it, and the first step is
     small enough to lose;
   - the data and tool access it needs that is not at hand, as a request rather than a reason to
     aim lower.

   If a bigger version is tempting but premature, name it and the evidence that would justify
   it later.
5. **Say how you will know, in proportion to the cost of being wrong.** The default judge is
   the user reading a few concrete results: for reversible work, including the user's own
   tools, notes and agent setup, one line on what they will see. Build a check beyond that
   only when the result reaches people who cannot judge it themselves, or cannot be undone
   (published, data changed): then name a first proof point, what would falsify the version,
   and a judge other than the model, ideally a check the agent can run itself.

End by offering the cheapest first step that tests the recommendation, and wait for the user's
yes before starting. In an unattended run, do the task as given and attach the recommendation.

## Examples

A light task, where one lens is enough:

> **Task:** email a collaborator asking for their RNA-seq data.
>
> **Verb:** get the files you can actually reanalyse, with one reply from a busy person.
>
> **Speed:** a polite request, sent in a minute; it usually returns their normalised table.
>
> **Depth:** ask for raw counts plus the sample sheet and the pipeline version, listed by name,
> so their processing choices do not become yours. **Altitude, range:** not used; one email
> is the whole job.
>
> **Check:** the reply contains files you can load. **First step:** send it. Send?

A task others will rely on:

> **Task:** write release notes for version 2.4 of a library.
>
> **Reframe:** the notes are for people deciding whether to upgrade, so the risk lies in
> breaking changes that the PR titles hide.
>
> **Verb:** let users decide in a few minutes whether to upgrade, and migrate without surprises.
>
> **Speed:** a draft from merged PR titles in minutes; vague titles hide breaking changes.
>
> **Depth:** diff the public API between 2.3 and 2.4 instead of reading titles, and run two
> sample projects' test suites against 2.4.
>
> **Range:** a support engineer maps open issues to the changed APIs; a tester follows the
> migration guide literally on the sample projects and records where it breaks.
>
> **Altitude, deferred:** a codemod that performs the migration. Worth it only if the trial
> migrations repeat the same mechanical edit across projects.
>
> **Recommendation:** depth and range together: notes built from the API diff, with a
> migration guide proven on the two samples. **Check:** both samples upgrade by following the
> notes alone. **First step:** the API diff, read-only and minutes long. Start there?
