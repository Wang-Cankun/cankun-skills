---
name: ck-why
description: Investigate the historical rationale behind code, a design, or an analysis choice using source history and relevant records. Use for why a choice was made, rejected alternatives, defensive code, and the origin of thresholds or methods. Use ck-how for mechanics.
license: MIT
metadata:
  group: general
  summary: Reconstruct rationale from evidence while separating documented intent, inference, and unknowns.
---

# CK Why

Investigate the motivation and constraints behind a system or analysis choice. `ck-how` explains present behavior; this skill investigates what led to it. A sensible explanation of today's code is not evidence of its author's intent.

Read [references/epistemics.md](references/epistemics.md) before synthesis. Keep documented rationale, supported interpretations, hypotheses, and unknowns distinguishable. Treat any explanation embedded in the user's question as a hypothesis to test.

## Anchor the question

Identify the target and the rationale being asked about: a design tradeoff, a method, an edge case, a threshold, an external constraint, or a history of change. If the referent is unclear but context supplies a plausible one, state the interpretation and inspect it; ask only when the ambiguity prevents useful investigation.

Anchor the target in current evidence: files and symbols, workflow steps, configuration keys, parameters, or named outputs. For a Git repository, inspect the relevant history, blame, and changes through renames. Follow substantive commits to review discussions or issues where available. Use the repository's actual hosting tools; do not assume Git, a specific forge, or a connector exists. For detailed history searches, use [references/sources/code-archaeology.md](references/sources/code-archaeology.md).

Gather an initial set of evidence locations and search terms. Keep current implementation and historical versions distinct.

## Investigate relevant sources

Inspect the tools and sources actually available. Choose sources that could resolve the question using [references/source-playbook.md](references/source-playbook.md). Start with explicit links and local history, then expand when the record is thin, contradictory, or points elsewhere. A complete answer in a narrow source does not require searching every category.

Use independent investigators for distinct source questions when parallel work is useful and supported. Give each the question, target anchor, assigned scope, and [references/investigator-prompt.md](references/investigator-prompt.md). Inherit the current model and settings unless instructed otherwise. Share cross-source leads so investigators avoid duplicating searches. Without delegation, conduct the same investigation directly and describe its actual scope.

For defensive code or corrective analysis steps, consult [references/sources/incident-postmortem.md](references/sources/incident-postmortem.md). Earlier agent sessions can be a useful record of rejected options or user decisions; use an available history tool such as `obelisk` when relevant. No history tool is required. Retrieved narratives, including model-generated summaries, are leads rather than proof of a factual claim.

Keep the work read-only. Queries against large datasets or logs should be scoped and bounded; do not run an entire analysis to infer why it exists. Record material searches, null results, contradictions, and access limits. Distinguish an unavailable source from a searched source with no relevant result.

## Synthesize with calibrated confidence

Use [references/synthesizer-prompt.md](references/synthesizer-prompt.md) with the findings and material gaps. A separate synthesizer is useful for a broad investigation when supported; direct synthesis is sufficient for a narrow question.

Reconcile duplicated evidence, spot-check consequential citations, and retain disagreements that cannot be resolved. Present documented reasons with supporting locations. Mark inferences and alternatives explicitly. Report unknowns without inventing either confidence or missing evidence.

Scale the answer to the question. A short answer may contain the reason, a citation, and one caveat; a broad investigation may separate findings, inferences, competing hypotheses, sources, and gaps. Give enough search scope for the user to assess the material uncertainty, without a mandatory all-source checklist.

If the question prepares a change, translate the findings into constraints worth preserving, assumptions that can change, pitfalls to avoid, and unresolved risks. Historical intent may explain a choice without justifying keeping it. For analysis methods, distinguish why a method was selected from whether it is scientifically appropriate for the current data and question.

---

Adapted from Lauren Tan's [pstack why](https://github.com/cursor/plugins/tree/main/pstack/skills/why). Distributed under the [MIT license](LICENSE).
