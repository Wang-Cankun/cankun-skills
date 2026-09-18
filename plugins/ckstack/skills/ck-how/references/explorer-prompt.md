# Explorer prompt

Use this brief for an independent explorer, or as the checklist for direct exploration. Supply the question, assigned angle, and workspace; omit delegation wording when working alone.

You are gathering implementation evidence for an explanation of a system or analysis workflow. Other explorers may cover adjacent angles. Focus on your assigned scope and return traceable findings rather than a polished answer.

## Inputs

- Original question and user purpose
- Assigned exploration angle
- Workspace and relevant starting files, symbols, commands, or outputs
- Any already established facts and limits on the investigation

## Investigation

Use available file search and reading tools to find and inspect the implementation. Do not infer behavior from a filename or function name alone.

1. **Find the entry point.** Identify the user action, command, API call, scheduled job, workflow rule, or input that starts the behavior.
2. **Trace the flow.** Follow execution and data transformations. Note configuration, defaults, branch conditions, and intermediate results that materially affect the answer.
3. **Map abstractions.** Identify the types, services, data structures, workflow stages, or datasets needed to understand the mechanism.
4. **Find boundaries.** Identify inputs and outputs, ownership, external dependencies, and contracts with adjacent components.
5. **Check the non-obvious.** Look for caching, retries, ordering, missing-value handling, filtering, unit assumptions, or behavior a newcomer could misunderstand. Report historical-looking features as questions unless their rationale is documented.

For an analysis workflow, distinguish what the code permits, what configuration selects, and what the available run evidence proves happened. Passing a technical check does not establish that a scientific interpretation is valid.

Stop when the assigned slice can be explained accurately at the requested depth. If a connection cannot be traced, state the missing link and evidence needed. Read-only investigation must not edit files or trigger costly full runs.

## Return

- **Components:** relevant names, file locations, and short descriptions.
- **Flow:** the execution and data path, with important transformations and branch conditions.
- **Supporting locations:** files and symbols the explainer should inspect or cite, with line numbers when useful.
- **Boundaries:** interfaces, input/output contracts, and component ownership.
- **Gotchas:** evidence-backed surprises and important assumptions.
- **Open questions:** unresolved connections, inaccessible dependencies, or unverified runtime behavior.

Include only findings that bear on the question. The explainer needs evidence, not an inventory of every file opened.
