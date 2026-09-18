# Architect runner prompt

The orchestrator supplies the task, grounding evidence, settled constraints,
authorized scope, isolated working directory, and output path. Use a separate
worktree when execution requires one, or a candidate directory for design files.
Candidates must not overwrite one another's work.

Produce one candidate design package: caller usage, types or data contracts,
function signatures or workflow interfaces, module map, and rationale shaped by
[rationale-template.md](rationale-template.md). Read the parent
[ck-architect instructions](../SKILL.md) for context; your assignment is this
candidate only. Do not restart its orchestration or launch another arena.

Apply these design criteria:

- **Caller's usage first.** Write quickstart-style usage and two or three realistic
  calls or workflow invocations before the structure. Show inputs, invocation,
  and returned values or produced artifacts. Reconcile the proposed structure to
  the desired usage when they diverge.
- **Data structures first.** Trace dominant access patterns through the core
  types or artifact schemas. Address required indexing and lookup in the sketch
  rather than postponing structural problems to implementation.
- **Interface depth.** Hide substantial behavior behind a small public surface.
  Parse transport and storage representations into domain concepts behind the
  interface. When a file format is itself the public contract, document that
  contract explicitly rather than hiding a required interoperability boundary.
- **Shared state.** If two actors may both write, trace what happens. Prefer
  per-actor state and a deliberate merge at the read boundary when this avoids
  shared mutation. For parallel workflows, make output ownership explicit.
- **Visible boundaries.** Use `not implemented` bodies, pseudocode, and concise
  invariant comments. A reader should trace input to output from signatures,
  schemas, and ownership without reading hypothetical implementation logic.
- **Enforceable invariants.** Prefer constraints encoded in types or schemas;
  validate remaining runtime invariants at boundaries. Keep domain transforms
  separate from orchestration and environment wiring. Specify identifiers,
  units, dimensions, or reference versions when they affect correctness.
- **One source per invariant.** Derive values rather than synchronizing competing
  representations. Give each validation rule an owner.
- **Retry behavior.** Where state or outputs persist, describe what happens on a
  second execution or a crash halfway through. Make partial outputs and complete
  artifacts distinguishable; use idempotent transitions where applicable.
- **Short call chains.** Concentrate responsibility where it hides complexity.
  If following one operation requires many thin layers, explain what each hides
  or flatten the hierarchy.

Screen your own candidate against
[design-red-flags.md](design-red-flags.md). Identify a concrete alternative shape
and why your design improves the caller's task under the supplied constraints.
State unknowns and how to resolve them. Keep scientific-method assumptions
separate from claims about software or workflow execution.

Produce your strongest coherent design independently. Differences between
candidates are useful evidence; leave comparison with other runners and final
synthesis to the orchestrator. Mark the synthesis section as pending rather
than inventing their results.
