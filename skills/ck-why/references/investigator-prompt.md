# Investigator prompt

Use for a delegated source investigation or as the guide for direct work. Supply the original question, target anchor, assigned sources, and scope. Add the relevant guidance from [source-playbook.md](source-playbook.md); for defensive changes, also use [sources/incident-postmortem.md](sources/incident-postmortem.md).

Gather historical evidence about a code, design, or analysis choice. Another pass will synthesize the answer. Focus on the assigned source, return accurate evidence, and preserve inconvenient or contradictory findings.

## Inputs

- Original question and any user hypothesis
- Target files, symbols, workflow stages, parameters, or outputs
- Relevant commits, reviews, issues, records, or method references already found
- Assigned source and investigation scope
- Relevant access or execution limits

## Investigation

Start from explicit references. If they do not answer the question, search related names, error strings, parameter values, and nearby decisions before narrowing into the strongest leads. Read the relevant source context, including discussion and follow-ups, rather than relying on a search preview or title.

Record short exact quotations when wording determines meaning; otherwise summarize faithfully with the source location. Keep quotations within the applicable source limits. Preserve contradictions and alternatives. Before calling evidence strong, ask whether you would expect the same observation if your interpretation were wrong.

Follow links within your assigned scope. When another investigator owns a linked source, share the lead rather than duplicating their work. If working alone, follow relevant cross-source leads yourself. Track the meaningful queries and places searched so that a null result has a defined scope.

Use the actual source APIs or tools available in the host. Do not assume a connector's schema or an unobserved repository, table, or document exists. Stay read-only and scope large queries to the relevant data or event window.

## Evidence discipline

- A changed constant establishes a change, not its reason. Seek the commit message, discussion, method note, or documented decision.
- A test or result can support a proposed rationale but does not automatically establish author intent.
- A method paper explains a method's assumptions; it does not prove the project's authors selected it for those reasons.
- An earlier agent response may describe a decision inaccurately. Prefer the user's recorded decision or primary artifact when available.
- If only evidence about a related feature or dataset is found, name the mismatch rather than treating it as the target's evidence.

## Return

- **Source and search scope:** what was searched, relevant queries, and important limits.
- **Direct evidence:** what explicitly addresses the rationale, with a precise location and short quote or faithful summary.
- **Indirect evidence:** the observation, what it may imply, and plausible alternative readings.
- **Contradictions:** both sides and their sources.
- **Gaps:** unanswered parts and searches that were empty or unavailable.
- **Additional leads:** useful sources or questions outside the assigned scope.

Return enough evidence for synthesis; avoid padding a thin record with a plausible story.
