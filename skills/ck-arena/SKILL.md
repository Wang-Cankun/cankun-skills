---
name: ck-arena
description: Generate independent candidates for the same task, compare them against explicit criteria, and synthesize a verified result. Use when the user asks to arena a task, explore competing designs, or compare multiple attempts before choosing an artifact.
license: MIT
metadata:
  group: general
  summary: "Generate independent candidates, compare them against shared criteria, and synthesize a verified artifact with a concise decision record."
---

# CK Arena

Fan out independent attempts at the same task. Read each candidate, choose a base, incorporate the strongest compatible ideas, and verify the resulting artifact. The artifact may be a design, implementation, document, or analysis workflow.

Track six phases: Frame, Fan out, Cross-judge, Pick, Graft, Verify. Use the host's available agent and execution capabilities; the workflow does not require a particular platform or model provider.

## A. Frame

The shared task is the candidates' contract.

1. State the artifact, constraints, input evidence, output location, and the observable result that will establish success. Accept caller-supplied grounding, candidate instructions, and output templates, such as a design package requested by `ck-architect`.
2. Derive a short rubric with concrete criteria for this task. The judge receives the rubric; candidates receive the same realistic task and necessary constraints. Keep candidate outputs and model identities out of one another's context.
3. Use the number of candidates requested, or start with two distinct attempts and expand only when the decision warrants it. Honor the user's model choices and the host's configured defaults. Different available model families can add perspective; multiple independent runs of the same model are also valid.
4. Give each candidate a separate output directory. Use isolated checkouts when candidates must modify a repository, or scratch directories for self-contained artifacts. Keep input data read-only and mutable state separate. Each runner owns its assigned artifact; it does not launch another arena.

Resolve a material ambiguity before spending effort on incompatible interpretations. Preserve settled requirements from the caller's brief.

## B. Fan out

Launch candidates concurrently when the host supports independent agents and resources permit it. Each gets the same task, the necessary grounding, its output location, and instructions to include a short rationale naming considered alternatives and rejected tradeoffs.

Wait for terminal results before judging a candidate. A progress message or existing output path is not completion. Record failures and inspect any usable output. If fewer than two viable candidates remain, retry a failed attempt or report that a comparative result is not yet available.

When only sequential execution is available, use fresh independent contexts where supported. If the current agent must generate every attempt in one context, disclose that limitation: these are alternate sketches, not independent reviewers. Preserve the comparison and verification steps without claiming independent confirmation.

## C. Cross-judge

After candidate outputs are complete, give a fresh reviewer the task, rubric, and candidates under neutral labels. Prefer a different available model family when the host supports that choice. The reviewer reads artifacts without editing them, scores the criteria, names failure modes, and recommends a base with reasons. Necessary content must be available to the reviewer, not merely mentioned by an inaccessible path.

The coordinator can read the completed candidates while this review runs. If an independent reviewer is unavailable, perform the rubric comparison directly and label it as coordinator review.

## D. Pick a base

Read every viable candidate end to end and examine the evidence it produced. Compare each criterion rather than judging by confidence or presentation. Reconcile your assessment with the reviewer's findings using the actual artifacts.

Prefer the candidate whose boundaries, assumptions, and invariants are easiest to understand and extend while meeting the task's requirements. A candidate failing a required constraint cannot win on a high average score. Record the chosen base and accepted tradeoffs in a short synthesis note.

## E. Graft

Inspect the remaining candidates for specific improvements worth carrying into the base. Adapt those ideas so the result has one coherent design; retain the base unchanged when nothing else improves it. Record what came from each candidate, what was rejected, and why.

Agreement between candidates is evidence of convergence, not proof of correctness. Divergent designs can expose useful tradeoffs. Reframe and rerun only when incompatible assumptions or missing constraints make the candidates incomparable.

## F. Verify

Check the synthesized artifact against the original task and the success criteria. Rerun relevant checks after grafting; the candidates' earlier results do not verify the new combination.

Exercise implementations and analysis workflows through their real entry points with representative inputs. Inspect outputs and invariants, not just exit status. For a design, trace concrete usage and failure cases against its interfaces or data contracts, using a small experiment when an empirical claim matters. For prose, check the requested content and its supporting evidence directly.

If verification fails, trace whether the problem came from the framing, a candidate, or synthesis, and repair that stage. Keep untested claims and unavailable checks explicit. In analysis work, computational behavior and scientific validity need separate evidence.

## Deliver

Return the synthesized artifact and its location, plus a short decision record: candidates considered, the base, incorporated ideas, rejected alternatives, failures or independence limits, and verification results. Keep evidence accessible after scratch cleanup. Applying, publishing, or running the result beyond the task's authorized scope remains a separate action.

---

Adapted from Lauren Tan's [pstack arena](https://github.com/cursor/plugins/tree/main/pstack/skills/arena). See [LICENSE](LICENSE).
