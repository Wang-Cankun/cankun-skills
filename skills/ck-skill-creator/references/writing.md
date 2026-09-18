# Writing decisions

Use these criteria while drafting or restructuring. Apply them to the current
failure or use case rather than adding this checklist to every generated skill.

## Discovery

A description identifies a capability and the distinct requests that need it.
Keep separate branches; remove synonyms that merely repeat the same branch.
Add an exclusion when a neighboring capability would otherwise be confused
with this one. Avoid broad triggers whose ordinary tasks need no special skill.

Names and descriptions usually participate in selection, but hosts implement
explicit-only invocation differently. Preserve the requested policy and check
the host format instead of deleting required metadata based on an assumed rule.

## Guidance and completion

Give an ordered procedure when order protects a real dependency. Describe the
outcome and decision criteria when several approaches are sound. A reference
skill can consist of rules without an invented sequence.

At a consequential step, make completion observable: for example, identify the
consumer of a changed field and exercise its read path, rather than merely
"consider compatibility." Exhaustive coverage belongs where incompleteness
would invalidate the conclusion; a small repair does not require an entire
project audit.

When an agent rushes a step, first sharpen its completion condition. Split work
across a real context boundary only if the early exit persists and the split
helps. Moving text to a different heading does not create that boundary.

## Information placement

Inline what every invocation needs. Move conditional procedures, schemas, and
large examples into references. State the condition at the link: "For a version
comparison, read evaluation.md" is more actionable than "More resources."
Keep a concept's rules, caveats, and example together.

Give each maintained fact one owner. Link project configuration rather than
copying commands and versions into several documents. Keep non-obvious reasons
and operational constraints that cannot be recovered cheaply from those files.

Split a skill when an independently useful request needs its own entrypoint,
or an observed sequencing problem requires a separate context. Otherwise use
conditional references; each extra skill consumes discovery space and adds a
choice for the user.

## Pruning

For each instruction, ask what decision it changes. Remove generic competence
advice, stale workarounds, redundant meanings, and speculation unsupported by a
real task. A real but rarely used instruction may belong in a reference.

Use a familiar, precise term when it compresses a repeated concept without
hiding needed meaning. Prefer the intended action to a long list of prohibited
actions. Retain explicit prohibitions for concrete authorization or correctness
boundaries, with a usable alternative.

A local incident can expose a general mechanism; it does not establish a rule
for every future project. Explain the mechanism and its applicability. Check
whether a script, configuration field, or existing authoritative document would
enforce the correction more reliably than additional prose.
