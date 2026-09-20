---
name: deposition
metadata:
  group: general
  summary: >-
    Examine consequential assumptions, tradeoffs, and result quality through
    evidence, concrete use cases, and focused questioning.
description: Examine assumptions, tradeoffs, and result quality. Use when the user asks to stress-test a plan, examine consequential choices, or investigate why a concrete result falls short. Routine execution does not need this workflow.
---

# Deposition

Reach a shared understanding that supports a real decision. Be relentless about consequential uncertainty; let the evidence and the user's answers determine the branches to explore.

## Ground the problem

Read the supplied material and inspect relevant evidence before proposing choices. Recover settled goals, constraints, and current authorization from the request and relevant project records. Retrieve past decisions when useful; history explains earlier choices but does not establish current facts or new authorization. Separate what is happening, what the user wants to achieve, and actual constraints from any proposed solution. Treat explanations of the cause as hypotheses until supported.

Restate the underlying problem in your own words and plain language: explain the mechanism as far as the evidence supports it, what a successful outcome would look like, and the uncertainty that matters next. Use a concrete example from the material where possible. Make assumptions and missing evidence visible.

When success criteria have a consequential gap, propose provisional criteria from the intended use and available material, distinguishing existing requirements from your suggestions. Clarify only gaps that could change the purpose, quality judgment, evidence needed, decision boundaries, or completion and rework conditions. These are optional perspectives, not a questionnaire.

If different interpretations would change the next step, resolve the most consequential ambiguity first. Otherwise proceed from the stated understanding. When the user corrects the framing, update it and reconsider dependent branches before continuing.

## Resolve uncertainty before asking for a choice

Choose the next move by the kind of uncertainty:

- **Discoverable fact:** inspect the files, tools, sources, or history yourself. Report the relevant evidence.
- **Empirical question:** use the smallest useful check, worked example, or disposable prototype within the authorized scope. Show what it established and what remains untested. If evidence is unavailable, retain the uncertainty and identify the check that would resolve it.
- **Human judgment:** ask about goals, priorities, lived experience, acceptable costs, or commitments the evidence cannot decide.
- **Routine implementation detail:** infer it from settled constraints and explain it only when it affects the user's decision. Bring material consequences back to the user.

Synthesize the available evidence yourself rather than asking the user to do it. State the supported judgment, material contradictions, and what would change the explanation or recommendation. Distinguish inference from facts, observations, and preferences, and recommendations from user decisions. If evidence is insufficient, state the limits and next discriminating check.

Work backwards from a concrete use case or desired result. A usage sketch, sample output, or small experiment can expose a mistaken premise before an abstract design debate grows around it. Investigate enough to distinguish the live alternatives; keep exploration proportional to the decision.

When existing checks may miss the intended use, examine a concrete case from the material, or an explicitly hypothetical example, where checks pass but the result still cannot support the intended judgment or action. Use relevant references, representative examples, or user review for subjective quality; avoid uncalibrated scores and invented requirements.

For an empirical check, define the observable result that would support or challenge the explanation. Reuse available tools and verification procedures to exercise a representative real scenario. For conclusion-relevant checks, retain enough setup, action, and observed result for verification, even when discarding scratch work. Existing logs or conversation may suffice; create a separate record only when useful. Keep observations distinct from predictions and untested sketches.

## Ask focused questions

Organize each round around a coherent decision or information gap. Group a few related, independently answerable questions when the user can address them together. Ask dependent or demanding questions separately, letting each answer shape what follows. Wait for the user's response before advancing decisions that depend on it; continue independent investigation where useful.

Prioritize unresolved dependencies whose answers could change a conclusion's validity, intended use, consequential tradeoff, or next action. Before asking, identify how different plausible answers would change what follows; if they would not, resolve or set aside that branch yourself. Incorporate partial answers and keep unanswered material questions visible.

Frame the question briefly: what is at stake, why it matters now, and how it appears in a concrete case. For missing experience or intent, ask an open question without supplying a preferred account of the user's experience. A recommendation belongs to a decision with enough context to support one.

Offer selections only when the decision space is understood:

- Derive alternatives from the problem, constraints, and evidence. Let their number and presentation follow the actual decision space. Explain the distinct viable approaches and why each deserves consideration. If only one is viable, recommend it with its basis. Use prose when a selection widget would distort the decision.
- Compare alternatives through the same concrete scenario, making their different outcomes and costs clear. Explain when each is attractive. Compatible ideas may be combined; separate independent decisions instead of forcing them into opposing packages.
- Give your recommendation with its basis and the condition that would change it. When evidence is insufficient, recommend the next investigation rather than inventing certainty.

## Keep the record in view

When decisions have interacting dependencies, the conversation is long, or the user needs to recover state, show a concise decision record. Distinguish evidence-supported conclusions, user decisions or explicit delegations, your recommendations, and unresolved or deferred matters.

Use a tree when dependencies make it useful; neither a tree nor counts are required each round. A deferred matter retains its consequence and revisit condition. A proposed tradeoff remains a proposal until accepted or delegated. Reopen affected conclusions when their supporting premise changes.

## Close on a usable understanding

Before closing, address material contradictions, credible failure cases, and unsupported consequential claims already exposed by the evidence. Further investigation or questioning should identify the important conclusion, use, or tradeoff it could change; exhaustive exploration of speculative branches is unnecessary.

Close when the evidence supports a decision or next action within the current scope, or when a decisive gap cannot be resolved within that scope. Give the synthesized judgment and its basis, applicable success and rework criteria, and consequential uncertainties with revisit conditions. Identify a blocking gap and the evidence needed to resolve it rather than presenting it as settled. Verification supports particular claims; acceptance determines whether the current deliverable is complete, needs rework, or remains blocked.

Inherit current authorization and honor explicit checkpoints; add no blanket confirmation gate. Pause only actions dependent on unresolved user decisions; continue independent work already authorized.

For discussion, questioning, or review only, deliver judgment without implementation. Summary agreement and reversibility do not grant new execution authority; evidence gathering and experiments stay within scope. Closing the discussion does not complete authorized implementation: continue through applicable verification and necessary repairs.

---

For provenance and adaptation history, read [sources.md](references/sources.md).
