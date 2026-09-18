# Rationale template

Use this alongside the sketch. Aim for one concise page; replace the italic
guidance with task-specific content. Read the usage section first and write it
before designing the shape.

## Problem

*State the intended outcome and what makes the shape non-obvious. Name grounded
constraints such as callers to preserve, input contracts, ownership boundaries,
and assumptions that remain to be checked.*

## Usage (caller's view)

*Write the quickstart the consumer would read, plus two or three realistic calls
or workflow invocations. Show inputs, returned values or produced artifacts, and
observable failure behavior. Derive the shape from this experience.*

## Shape

*Start with data structures or artifact schemas, then trace data flow through
interfaces and modules. Name the decisions that determine the structure, their
evidence, the invariants encoded in types or schemas, and the remaining
validation boundaries. Explain which complexity the public surface hides, what
callers still need to understand, and why the interface is no larger than needed.
Include output ownership and retry behavior when relevant.*

## Synthesis decision

*The ck-arena orchestrator fills this after comparing candidates: name the base
and why it won, the ideas adapted from other candidates, and rejected ideas with
their reasons. Candidate runners leave this pending. Record checks applied to
the synthesized package rather than assuming its parts compose correctly.*

## Tradeoffs accepted

*One bullet per meaningful tradeoff: "we accept X in exchange for Y." Include
choices a future maintainer might otherwise mistake for an oversight.*

## Alternatives considered

*Describe at least one concrete alternative shape and why it loses under the
actual constraints. Compare the complexity it hides and exposes to callers,
not just how easy it is to implement. These are design alternatives considered
by this package, separate from the orchestrator's candidate comparison. When
only one shape is viable, give the constraints that exclude the alternative.*

## Open questions and risks

*Separate unresolved human judgments, missing facts, and known risks. For each
material item, state the consequence and the observation or decision that would
resolve it. Keep predictions and scientific assumptions distinct from observed
results. Write "None material" when that is supported.*

## Next implementation step

*Name the first coherent unit to build and its observable success criterion. For
a design-only request, leave this as a recommendation; it is not authorization
to implement.*
