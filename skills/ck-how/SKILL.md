---
name: ck-how
description: Explain how code, a system, or an analysis workflow operates by tracing its implementation. Use for runtime or data flow walkthroughs, subsystem onboarding, and placement or ownership questions. Use ck-why for historical rationale.
license: MIT
metadata:
  group: general
  summary: Trace implementation, inputs, outputs, and boundaries to build a working mental model.
---

# CK How

Explore the implementation to answer how something works. Produce enough explanation for the reader to follow the behavior and work in that area, without turning the answer into annotated source code. Investigation is read-only unless the task separately authorizes changes or experiments.

## Assess the question

Identify the target and the user's purpose from the request and available context. If the scope is ambiguous but exploration can resolve it, state the interpretation briefly and proceed.

- **Narrow question:** trace and explain directly. A single utility, pipeline stage, or ownership question usually needs no delegation.
- **Cross-cutting question:** divide the work into distinct angles such as entry points, data transformations, persistence, scheduling, or component boundaries. Use independent explorers when supported and useful; otherwise trace these angles yourself. Inherit the current model and configuration unless the user requests otherwise.

Match effort to the question. A full architecture inventory is unnecessary when one call path answers it.

## Trace the implementation

For delegated exploration, use [references/explorer-prompt.md](references/explorer-prompt.md), giving each explorer the original question, its angle, and the relevant workspace. The same guide applies to direct investigation.

Find the entry point, follow the execution and data flow, and identify the abstractions and boundaries that explain the behavior. Read implementations rather than guessing from names. For analysis workflows, follow the input contracts, configuration, transformations, intermediate outputs, and downstream consumers. Distinguish configured behavior from what a supplied run actually executed.

Read project instructions and existing environment configuration before invoking project tools. Prefer existing logs and small read-only checks when those resolve a gap. A code walkthrough does not require running an expensive workflow.

Keep supporting file locations and material uncertainties with the findings. Source code can establish mechanics; author intent needs historical evidence. Route a material rationale question to `ck-why` when available, or state the gap.

## Synthesize and explain

Use [references/explainer-prompt.md](references/explainer-prompt.md) to combine findings. Reconcile overlapping accounts and check contradictions against the implementation. Use a separate explainer when it offers useful independent review; otherwise synthesize directly. Do not claim independent investigation when it was unavailable.

Lead with what the system does, then explain the flow at the depth the user needs. A substantial explanation may include key concepts, how it works, where things live, and gotchas. Omit sections that add no value. Include concrete file or symbol references and a diagram when they help the reader follow the mechanism. Preserve gaps instead of smoothing them into a complete-looking account.

---

Adapted from Lauren Tan's [pstack how](https://github.com/cursor/plugins/tree/main/pstack/skills/how). Distributed under the [MIT license](LICENSE).
