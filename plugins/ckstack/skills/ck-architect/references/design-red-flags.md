# Design red flags

Screen every candidate before synthesis. A red flag is a reason to inspect,
revise, or reject the shape based on the concrete task.

## Shallow module

A shallow module exposes a large interface while hiding little complexity.
Judge depth by the capability and policy hidden behind the public surface
relative to its size. Prefer a simple interface backed by substantial behavior.

A deep module concentrates capability behind one interface; a deep call chain
scatters understanding across layers. Look for these signs:

- Callers coordinate several methods to complete one operation.
- Public options expose internal stages or implementation choices.
- Learning the interface still requires learning the implementation.

## Information leakage

Information leakage makes multiple modules depend on the same internal
representation, policy, or protocol decision, so changing it needs coordinated
edits. Parse external representations into domain concepts behind the interface.
Keep private storage and framework details private.

For analysis workflows, distinguish an intentional public artifact schema from
an incidental intermediate file layout. A shared public schema can be a useful
contract; each consumer guessing its interpretation is leakage. Give identifiers,
units, missing-value rules, and reference versions one authoritative definition
when they are part of that contract.

## Temporal decomposition

Temporal decomposition organizes modules by execution order instead of the
knowledge they own. Separate load, validate, transform, and save modules can
repeat the same representation and invariants across boundaries.

Group behavior around domain knowledge and ownership. Pipeline stages can still
be legitimate boundaries when they support independent restart, scheduling,
resource allocation, or reproducible artifacts. Check what each stage owns and
what its boundary enables; the existence of ordered stages alone is not a flaw.

## Pass-through method

A pass-through method forwards the same arguments in the same shape, adding a
layer without hiding complexity. Remove it or move responsibility to a module
that can complete the operation. Keep forwarding boundaries that add policy,
adaptation, or a distinct abstraction.
