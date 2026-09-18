---
name: ck-prototype
description: Build disposable prototypes or small experiments to settle a design or behavioral question through observation. Use when the user asks to prototype, mock up, try competing approaches, or compare layouts, interactions, methods, or workflow behavior before implementation.
license: MIT
metadata:
  group: general
  summary: "Build disposable prototypes and small experiments to compare approaches through observable behavior, measurements, and concrete tradeoffs."
---

# CK Prototype

Use a disposable artifact to make a decision cheaply. The output is a supported direction and the experiment that informed it. Production implementation follows the user's chosen scope.

## 1. Name the decision

Identify the uncertainty the prototype will resolve: layout, interaction, behavior, timing, interface shape, or an analysis method's suitability. State the input conditions and observations that would distinguish the live alternatives. Use the user's settled goals and constraints.

If the task is already a straightforward implementation request with no decision to explore, proceed with that request instead of manufacturing an experiment.

## 2. Explore plausible directions

When the design space is open, inspect relevant existing work and references. Offer useful variations beyond the first idea when they address the decision. If a consequential user preference is missing, clarify it; otherwise build from the supplied direction and stated assumptions.

Choose enough variants to expose the actual tradeoff. A focused experiment can also answer one hypothesis without a comparison set.

## 3. Build the smallest useful experiment

Work in a clearly named scratch directory, separate from production source and original data. Use the project's available runtime and the lightest implementation that can demonstrate the behavior. Favor speed and observability over reusable abstractions or production polish.

- **Visual or interaction questions:** make variants easy to switch between and label them. Reuse existing rendering and control tools where available.
- **Behavior or performance questions:** use a small executable harness with the same inputs and comparable conditions for each variant. Record setup, outputs, and measurements.
- **Analysis questions:** use a representative small dataset or a clearly labeled synthetic fixture. Carry over relevant data structure and constraints; identify which conclusions cannot transfer to the full dataset. Methods and thresholds come from the task's evidence, not convenient assumptions.

Keep expensive compute proportional to the decision. Repeated experiments may justify a short helper script; a one-off sketch does not need a production framework or a new test suite.

## 4. Observe the behavior

Run each variant on the surface that matters. Drive interactions and inspect screenshots for visual questions. Inspect actual output, timing, error behavior, or data invariants for computational questions. Use available project verification procedures when appropriate.

Keep measurements reproducible: preserve commands or steps, input conditions, and material evidence. Include repeats or a baseline when noise could reverse the comparison. A mockup supports claims about the mocked interaction, not the performance of the eventual implementation. A successful analysis run alone does not establish a scientific conclusion.

If you cannot execute a check, describe the artifact as an untested sketch and state the missing evidence. Update or discard an approach when observations contradict its premise.

## 5. Recommend and hand off

Present the variants, observed differences, tradeoffs, and a recommendation tied to the decision criteria. Explain what would change that recommendation. Include the scratch path and enough evidence to revisit the comparison.

Label the artifacts as disposable. Preserve useful evidence when cleaning up instances or scratch state you created. Continue to implementation when already requested, or hand the chosen direction to a design or implementation task. For a substantial interface or workflow boundary, `ck-architect` can use the result as grounding when available.

---

Adapted from Lauren Tan's [pstack prototype playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/prototype.md). See [LICENSE](LICENSE).
