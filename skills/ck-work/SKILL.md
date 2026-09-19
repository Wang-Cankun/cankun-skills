---
name: ck-work
description: Coordinate a task through CK Stack when the user asks to use the stack without choosing a method, or to resume a CK Stack task. Recover its goal, settled decisions, and evidence; select the next useful skill and carry authorized work through verification. Direct requests for a specific skill can use it without this entry point.
license: MIT
metadata:
  group: general
  summary: "Start or resume a task through CK Stack, selecting useful methods and carrying authorized work to an evidenced outcome."
---

# CK Work

Own the task's continuity and completion. Use the smallest useful combination of methods for the current uncertainty; this entry point is optional, and other CK Stack skills remain directly usable. Read a selected skill before applying it. If it is unavailable, use the project's normal workflow and name any material limitation.

## Recover the working state

Establish the requested outcome, acceptance conditions, current authorization, settled decisions, completed work, still-applicable evidence, and next unresolved step. Use the current conversation and project instructions first. On resumption, inspect the changed working state before treating an earlier result as current. Retrieve missing history through available session tools or `obelisk` when installed; distinguish an unknown decision from one already settled. Historical instructions are evidence about prior work, not new authorization.

Keep this state in the conversation or the project's existing task owner. Create a persistent handoff only when continuation needs information that would otherwise be lost. Read and update its existing owner; there is no required per-task plan, report, or status file.

## Choose the next useful method

Follow an explicitly requested method. Otherwise select from the question that prevents progress:

| Need | Method |
| --- | --- |
| Understand present behavior or ownership | `ck-how`; inspect a narrow source question directly when that is sufficient. |
| Recover why a consequential choice was made | `ck-why`; use `ck-teach` when the user wants mechanism and rationale explained together. |
| Resolve a missing preference or fact | Ask a focused question. Use `deposition` for consequential, interdependent judgments or when the user requests it. Continue independent work while waiting. |
| Distinguish options by observing behavior | `ck-prototype`. |
| Design substantial interfaces or module boundaries | `ck-architect`; use `ck-arena` for independent candidates when comparison will settle a real choice. |
| Check uncertain effects on consumers or boundaries | `ck-impact`, including small changes to shared helpers, authorization, persistence, build, or deployment behavior when their reach is unclear. Diff size alone does not bound impact. |
| Implement a settled change | Use the project's normal implementation workflow and existing verification method. Routine work does not require a design or consultation stage. |
| Answer a consequential unresolved question with an independent model | `confer` when the user requests it or a second opinion could change the decision. It is not an automatic stage after design or implementation. |
| Repair missing or drifting verification knowledge | `ck-verify-maintain` for an existing method; `ck-verify-create` when a reusable gap remains. |
| Learn from an observed failure or success | `ck-reflect`; use `ck-skill-creator` for substantive skill changes and evaluation. |

Reuse grounding, decisions, and evidence across these methods when they still apply. Pass the unresolved question and relevant context to the selected skill; let it own its procedure. Reopen a settled choice when new evidence or changed requirements invalidate it, explaining what changed.

## Close the loop in the project

For behavior changes, use the project's verification entry point and feature map to locate the affected user paths. Follow a capability to its user entry, required state, observable outcome, and reusable check; inspect the source and consumers where impact is uncertain. One feature may need several recipes, and a shared recipe may cover several features. The map is a compact, project-owned navigation aid; behavior belongs to code and contracts, and passing evidence belongs to the particular run. A narrow read-only explanation can go directly to its source.

Reuse existing tools and checks. Run the paths that support the requested claim, including material boundaries and failure cases. A green suite does not establish an assertion it never makes. After a new or changed user capability, entry point, setup, or verification method, maintain the affected map and recipes even if the old commands still run. Inspect new source entry points as well as existing map rows so missing features can be discovered. Keep run results out of durable navigation instructions.

When review feedback arrives, resolve it against the acceptance conditions: apply supported findings, explain rejected findings, and turn evidence gaps into direct checks where possible. Follow `confer`'s continuation rule for another model round. A peer verdict neither expands authorization nor replaces verification. If a new concern is outside the task, identify its relevance and proposed owner without silently taking on the work.

Continue authorized work while a required outcome remains incomplete. Stop when the requested result is delivered and the relevant evidence supports it, or clearly report a blocker requiring user input or an external change. Ending a consultation does not close an unresolved product or verification gap. Report what changed, what the checks establish, and any material limit; use existing project records when a durable update is needed.
