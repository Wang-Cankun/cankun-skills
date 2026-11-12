---
name: ambition
metadata:
  group: thinking
  summary: Widen the thinking on a task through speed, altitude, depth and range, and say what the wider view changes.
description: "Widen the thinking on a task through four kinds of ambition (speed, altitude, depth, range): what a higher, deeper or wider view sees that the current framing misses. Use when the user asks to think bigger, go deeper or aim higher (更有野心, 拔高, 做深), or when a task may be aimed too low. Skip small or fully specified tasks, and requests that only want it faster."
---

# Ambition

Based on Felix Rieseberg's [How to be more ambitious: a tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).
It sorts ambition into four kinds:

- **Speed**: the same work in less time.
- **Altitude**: aim at the outcome beyond the task.
- **Depth**: see the task the way a field-leading expert would, down to the raw data and tools.
- **Range**: draw on fields the task does not obviously need.

They are lenses on one task. The reply is thinking: it widens how the user sees the task, and
the user decides what, if anything, to act on.

## Think it through

Write the reply as a short argument applied to this task, in this order.

1. **Turn the noun into a verb.** The deliverable is a noun: a deck, a pipeline, release notes.
   Say what it must do, to whom: a quarterly review is getting busy people to believe a
   cause-and-effect story and decide under uncertainty. When the verb shows the real problem is
   elsewhere, open the reply with that reframe in one sentence.
2. **Speed as the reference.** One line: what the task as framed now reaches, and what it
   leaves unseen. The other lenses are measured against it.
3. **Altitude, depth, range.** A lens earns a short paragraph only when it shows something the
   current framing misses, named concretely: the data, the field, the outcome. Put the
   remaining lenses together in one line that says why they add nothing here.
   - **Altitude.** Ask what the deliverable is for, then what that serves. Say what the higher
     outcome reveals about the task: a different question, a different audience, a standing
     problem behind a one-off request.
   - **Depth.** A deeper view, not a bigger one. Say what a top practitioner would do here that
     the user is not asking for, the rawest material they would start from instead of the
     digested version, the methods and instruments they would use, and how they would know it
     was right. New vocabulary is not a new method.
   - **Range.** From the verb, find the fields that do that action well, beyond the obvious one.
     For each, name what its people would actually see or do here (an editor cuts what does not
     change the decision), including one field whose trade is finding what is wrong (a forensic
     accountant traces each number to its record). Their work, not their voices.
4. **What it changes.** A few lines: what the wider view shows that the task as framed misses,
   and which of the user's current assumptions it questions. Then hand the turn back.

## Examples

A light task, where one lens is enough:

> **Task:** email a collaborator asking for their RNA-seq data.
>
> **Verb:** get files you can actually reanalyse, with one reply from a busy person.
>
> **Speed:** a polite request usually returns their normalised table.
>
> **Depth:** an analyst would want the raw counts, the sample sheet and the pipeline version,
> so the collaborator's processing choices do not silently become yours. **Altitude, range:**
> nothing here; one email is the whole job.
>
> **What it changes:** the ask is for inputs you can redo the analysis from, not for "the data".

A task others will rely on:

> **Task:** write release notes for version 2.4 of a library.
>
> **Reframe:** the notes are for people deciding whether to upgrade, so the risk lies in
> breaking changes that the PR titles hide.
>
> **Speed:** a draft from merged PR titles; vague titles hide breaking changes.
>
> **Depth:** a maintainer would read the public-API diff between 2.3 and 2.4, not the titles,
> and would trust the notes once a real project upgrades by following them alone.
>
> **Range:** a support engineer sees which open issues touch the changed APIs; a tester reads the
> migration guide literally and finds where it breaks.
>
> **Altitude:** behind the notes is the cost of every user's upgrade; a codemod would remove
> most of it.
>
> **What it changes:** the notes are a migration aid, so their quality is measured by upgrades
> that succeed, and the titles are the weakest source for them.
