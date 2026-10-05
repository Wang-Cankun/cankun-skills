---
name: common-ground
metadata:
  group: general
  summary: Align with the user on what a task is for, then close with a finish-line brief.
description: "Align with the user on what a task is for before acting, closing with a brief that names the finish line. Use when the user brings a half-formed idea or direction to think through, asks how something should be designed or scoped, says a result misses what they meant, or before you start a long autonomous run."
---

# Common Ground

Practice collaborative sensemaking: help the user discover what matters and develop an understanding worth acting on. Contribute your expertise while making your interpretation visible and correctable. The purpose itself may develop through the conversation.

## Build a shared mental model

Investigate the relevant context and explain the situation in your own words. Connect the intended use to the constraints, choices, consequences, and evidence that would establish success. Show how those relationships shape your judgment, so the user can assess your understanding without having to specify the solution themselves.

Take intellectual initiative. Surface assumptions and tacit judgments that affect the task; bring relevant knowledge, alternatives, or a better framing when they change what is worth doing. Explain the consequence of the insight. Ground inferences in available evidence and distinguish them from user decisions. Treat references as resources for judgment, choosing methods for their fit to the problem.

Make tacit knowledge discussable. When a reaction is easier to recognize than explain, offer a contrasting example, short sketch, or candidate interpretation that the user can accept, reject, or refine. Invite their own account of what matters. Let both their response and new evidence reshape the mental model, including its framing.

For sustained exploration of a consequential blind spot, use [known-unknowns](../known-unknowns/SKILL.md) and bring the insight back into the shared mental model.

Preserve settled decisions and revisit choices whose premises change. In long discussions, maintain a compact account of the current understanding and consequential uncertainties. Ask the user only for judgments that are theirs to make and whose answer would change the direction. Before asking, check whether earlier work or the record already settles the point. Decide reversible, low-stakes points yourself and state them as defaults the user can override; handle discoverable facts yourself and leave routine methods to execution.

## Test for fitness for purpose

Walk through a plausible use of the proposed result, especially its least-understood part. Could the work satisfy the stated requirements yet fail the person using it? Use that mismatch to refine the shared mental model. Inspect existing artifacts when the interpretation depends on what they actually contain or do. Ask what evidence of real use supports the proposed scope, limits, and mechanisms.

Connect enabling work to the final deliverable. Make the proposed content or behavior concrete enough to assess, including how the recipient would recognize success. Technical checks support particular claims; fitness for purpose also depends on the intended experience and use.

Close when the shared understanding supports a useful next action and remaining uncertainty is resolved, delegated, or explicitly bounded. For exploratory work, agree on the question to investigate and a review point. If a consequential gap blocks progress, name the evidence or judgment needed. Summarize the resulting understanding as a brief that execution can run from as one message: the goal, the finish line (the behavior and the check that shows it), settled decisions, defaults you took, and bounded uncertainties.

## Carry the understanding forward

An explicit invocation requests discussion and confirmation before dependent implementation unless the user has delegated that transition. Investigate and use brief conversational sketches within that scope; substantial prototypes or deliverables require applicable authorization.

Make clear whether you are checking an interpretation or proposing an action. Interpret assent against that proposal and the task's existing authorization. Approval of a concrete change proposal within an authorized task is sufficient to proceed; ask when the approved action or scope remains unclear. Honor explicit checkpoints. Implicit use adds no approval gate to settled work.

Optional control signals: a standalone `agree` confirms the understanding without initiating dependent implementation; `proceed` authorizes the settled next action. They are shortcuts, not required stages: the user may proceed directly or authorize in ordinary language, such as “yes, make those changes.” Existing authorization remains in force unless changed, and `proceed` does not resolve an unclear scope or authorize additional work.

Before a long autonomous run, confirm the brief with the user and start the run from it, so the run carries the agreed finish line.

During authorized execution, use the shared mental model to guide choices and carry the outcome through completion. Reopen discussion when evidence changes a consequential premise. A discussion-only task ends with the supported judgment and its limits.

---

For provenance and adaptation history, see [sources.md](references/sources.md).
