---
name: deposition
metadata:
  group: general
  summary: >-
    Ground a plan, decision, or idea in evidence, then examine consequential
    choices through focused question rounds, concrete alternatives, and a
    visible decision tree.
description: Depose a plan, decision, or idea before commitment. Build a shared understanding of the problem, investigate uncertainties, and examine consequential choices through focused question rounds. Use when the user asks to stress-test their thinking, says "depose this", or asks to be grilled about a plan.
---

# Deposition

Reach a shared understanding that supports a real decision. Be relentless about consequential uncertainty; let the evidence and the user's answers determine the branches to explore.

## Ground the problem

Read the supplied material and inspect relevant evidence before proposing choices. For continuing work, retrieve relevant past decisions when available. Separate what is happening, what the user wants to achieve, and actual constraints from any proposed solution. Treat explanations of the cause as hypotheses until supported.

Restate the underlying problem in your own words and plain language: explain the mechanism as far as the evidence supports it, what a successful outcome would look like, and the uncertainty that matters next. Use a concrete example from the material where possible. Make assumptions and missing evidence visible.

If different interpretations would change the next step, resolve the most consequential ambiguity first. Otherwise proceed from the stated understanding. When the user corrects the framing, update it and reconsider dependent branches before continuing.

## Resolve uncertainty before asking for a choice

Choose the next move by the kind of uncertainty:

- **Discoverable fact:** inspect the files, tools, sources, or history yourself. Report the relevant evidence.
- **Empirical question:** use the smallest useful check, worked example, or disposable prototype within the authorized scope. Show what it established and what remains untested. If evidence is unavailable, retain the uncertainty and identify the check that would resolve it.
- **Human judgment:** ask about goals, priorities, lived experience, acceptable costs, or commitments the evidence cannot decide.
- **Routine implementation detail:** infer it from settled constraints and explain it only when it affects the user's decision. Bring material consequences back to the user.

Work backwards from a concrete use case or desired result. A usage sketch, sample output, or small experiment can expose a mistaken premise before an abstract design debate grows around it. Investigate enough to distinguish the live alternatives; keep exploration proportional to the decision.

For an empirical check, define the observable result that would support or challenge the explanation. Reuse available tools and verification procedures to exercise a representative real scenario. Record the setup, action, and observed result sufficiently for someone else to repeat the check. Preserve material evidence when disposing of scratch work. Keep observed results distinct from predictions and untested sketches.

## Ask focused questions

Organize each round around a coherent decision or information gap. Group a few related, independently answerable questions when the user can address them together. Ask dependent or demanding questions separately, letting each answer shape what follows. Wait for the user's response before advancing decisions that depend on it; continue independent investigation where useful.

Prioritize unresolved dependencies whose answers could change the direction, scope, or next investigation. Before asking, identify how different plausible answers would change what follows; if they would not, resolve or set aside that branch yourself. Incorporate partial answers and keep unanswered material questions visible.

Frame the question briefly: what is at stake, why it matters now, and how it appears in a concrete case. For missing experience or intent, ask an open question without supplying a preferred account of the user's experience. A recommendation belongs to a decision with enough context to support one.

Offer selections only when the decision space is understood:

- Derive alternatives from the problem, constraints, and evidence. Let their number and presentation follow the actual decision space. Explain the distinct viable approaches and why each deserves consideration. If only one is viable, recommend it with its basis. Use prose when a selection widget would distort the decision.
- Compare alternatives through the same concrete scenario, making their different outcomes and costs clear. Explain when each is attractive. Compatible ideas may be combined; separate independent decisions instead of forcing them into opposing packages.
- Give your recommendation with its basis and the condition that would change it. When evidence is insufficient, recommend the next investigation rather than inventing certainty.

## Keep the record in view

Before each question round, show a compact indented tree in a code fence, headed by `✓n · ?k · ~m`:

- `✓` settled conclusions or decisions, one phrase each. Ground factual conclusions in evidence; reserve user decisions for their answers or explicit delegation.
- `?` a pending question, under the branch that owns it. For grouped questions, use matching short labels in the tree and the questions; `k` counts all pending questions, including unanswered ones from earlier rounds.
- `~` relevant branches still to investigate, nested under their dependencies in likely walk order.

Collapse a fully settled branch into its parent's one-line conclusion. Count the visible markers; use `?0` when no question is pending. Keep explicitly deferred items visible as `deferred`, with their consequence and revisit condition. Deferred items are not settled.

Build the tree as understanding develops. Add branches when evidence or a concrete failure mechanism shows they could change the decision. Retire branches made irrelevant by an answer, with a brief reason; reopen settled conclusions when their supporting premise changes. Keep the tree focused on dependencies and material uncertainty.

## Close on a usable understanding

When no material branch remains open or unwalked, summarize the problem, agreed outcome, consequential decisions and their basis, plus any explicit deferrals. Distinguish what has been verified from what still needs checking, with an observable success criterion for the chosen direction. “Nothing further” means nothing material remains for this decision within its scope.

Then ask whether this captures the shared understanding. The final confirmation is the sole pending question; do not add it while other unresolved branches remain. An instruction to proceed from the settled summary counts as confirmation.

Implementation or commitments under examination wait for that confirmation. Evidence gathering and disposable experiments within the authorized scope can happen throughout the deposition; they do not authorize deploying changes or making external commitments.

---

*Forked from [mattpocock/skills](https://github.com/mattpocock/skills) `grilling`; the record and the closing gate are the fork. Grounding and verification informed by Lauren (@poteto), “The Complete Guide to pstack,” Parts 1–2, and [pstack's verification workflow](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md).*
