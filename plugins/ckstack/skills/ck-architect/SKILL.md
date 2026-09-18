---
name: ck-architect
description: >-
  Design interfaces, data contracts, and module boundaries before implementation.
  Use when designing a substantial feature, refactor, or analysis workflow whose
  structure needs comparison before coding; continue into implementation when
  the user has requested it.
license: MIT
metadata:
  group: general
  summary: >-
    Ground the system, compare independent design sketches, and implement within
    the requested scope, redesigning when evidence invalidates the shape.
---

# CK Architect

Sketch the caller's experience before the machinery behind it. Derive types,
function signatures, data contracts, and module boundaries from that usage, with
`not implemented` bodies and pseudocode. Compare structurally different designs,
then implement the chosen shape when implementation is in scope. If the work
reveals that shape is wrong, redesign around the new evidence.

## Dependencies and scope

Read **ck-how** for existing-system grounding, **ck-why** when changing ownership
or layering requires historical rationale, and **ck-arena** for candidate design
and synthesis. Resolve each by name in the available skill catalog, or read its
`SKILL.md` in the sibling skill folder. Read the resolved instructions before
using them; a skill name is not a tool call. If a required skill is unavailable,
identify the missing dependency and pause that phase while continuing useful
independent work.

Use the host's available tools and agents. Honor the user's task scope, settled
constraints, and decisions already reached through deposition or other planning.
A design-only request ends with a concrete design package. An implementation
request authorizes continuing through implementation; an explicit checkpoint
pauses before it. Record the applicable phases in the working plan:

1. Ground
2. Sketch
3. Agree
4. Implement, when requested
5. Scrap and redesign, when evidence calls for it

## Phase A: Ground the problem

Build a traced model of the systems the change touches using **ck-how**. Naming
files is not grounding: show the entry points, data flow, ownership, observable
behavior, and supporting evidence. Use **ck-why** when existing ownership or
layering is being reconsidered so its rationale becomes a constraint rather
than a guess.

For analysis workflows, trace inputs through transformations into output
artifacts. Identify the relevant schemas, identifiers, units, reference versions,
and validation boundaries from project evidence. Keep scientific assumptions
distinct from execution requirements; a pipeline completing does not establish
that its conclusions are sound.

Skip existing-system tracing only for genuinely greenfield work with no
surrounding system to integrate. In either case, finish grounding with the
desired outcome, representative usage, constraints, and unresolved facts that
could alter the architecture. Resolve consequential factual gaps before using
them as design premises.

## Phase B: Sketch

Run **ck-arena** with the design task, grounding evidence, scope, and output
location. Pass [references/runner-prompt.md](references/runner-prompt.md) to each
candidate runner and require the package in
[references/rationale-template.md](references/rationale-template.md).

Design it twice: require at least two structurally distinct candidates before
synthesis, even when the first seems sufficient. Explore whole shapes rather
than variations inside one shape. Use available independent runners; ck-arena
defines the fallback when independent execution is unavailable. Report the
actual degree of independence instead of claiming perspectives that were not
obtained.

Screen each candidate against
[references/design-red-flags.md](references/design-red-flags.md) before synthesis.
Revise or reject shallow modules, leaked internal decisions, unnecessary temporal
decomposition, and pass-through layers. Compare viable candidates on interface
depth: how much complexity is hidden behind a small public surface. A rich
capability behind one interface can keep callers simpler than a chain of narrow
wrappers.

Have arena synthesize one coherent package and record its base, adaptations, and
rejected ideas in the rationale's "Synthesis decision" section. Check the merged
usage examples against the merged contracts; individually compatible candidates
can produce an inconsistent synthesis. Finish with a package that lets a reader
trace representative input to output and identify what remains unverified.

## Phase C: Agree within the requested scope

Present the synthesized shape, reasons, tradeoffs, and unresolved decisions.

- **Design-only:** deliver the package and stop before production implementation.
- **Implementation requested or already authorized:** proceed using settled
  constraints. Ask only about consequential judgments the current authorization
  and evidence do not resolve.
- **Explicit design checkpoint:** present the concrete package and wait for the
  requested sign-off before implementation.

Reuse previous decisions instead of reopening them without new evidence. If the
user challenges the shape, treat the correction as Phase A evidence and revisit
dependent sketches. For adversarial design review, have an available reviewer
trace a representative and a failure case through the sketch, challenge its
assumptions, and screen the red flags. Model agreement is not execution evidence.

## Phase D: Implement against the sketch

Replace placeholders with code and pseudocode with logic. The selected sketch is
the contract; build in coherent increments that can be checked against the
representative usage and intended output. Use the project's existing validation
and execution procedures, with bounded representative inputs for costly analysis
workflows. Keep unimplemented scaffolds clearly labeled and outside active paths
until those paths are ready.

Surface meaningful deviations. When a function requires an unplanned parameter,
a data artifact needs an extra field, or callers must coordinate hidden stages,
determine whether the design was wrong, a requirement was missed, or the
implementation exceeds scope. Correct the contract and affected callers
together. Distinguish verified behavior from design claims and scientific
assumptions in the final result.

## Phase E: Scrap when the architecture is wrong

A repeated pattern is evidence against the shape:

- The same workaround appears in unrelated parts of the implementation.
- Independent edge cases repeatedly require the same special-case branches.
- Types or data contracts need escape hatches or fields that are optional only
  on paper.
- Shared writes require coordination the sketch assumed was unnecessary.
- Callers must understand an abstraction's internal rules to use it correctly.
- Multiple independent implementation deviations have the same shape.

Distinguish necessary domain complexity from avoidable design complexity. A few
edge cases alone do not condemn an architecture. When the pattern points to a
wrong premise:

1. Preserve useful evidence and user work, then rerun **ck-how** over what exists.
2. State the failed premise and treat the newly learned constraints as original
   requirements.
3. Remove unnecessary machinery before adding replacements.
4. Return to Phase B for fresh candidates and synthesis.

Scrapping a design means replacing its assumptions and affected implementation
within the authorized scope; it does not authorize discarding unrelated work.

## Outputs

For small changes, deliver one sketch of signatures, types or data contracts,
plus its rationale. For larger work, include a module or workflow map. The
caller's usage is written first and the structure derived from it. State whether
the result is design only, implemented, or implemented with remaining checks.

---

Adapted from Lauren Tan's [pstack architect](https://github.com/cursor/plugins/tree/main/pstack/skills/architect), under the [MIT license](LICENSE).
