# Precedents for repository wayfinding

Read this reference before recommending a new document topology or another
`AGENTS.md` layer. Skip it when the task only classifies an existing, already
declared authority structure.

These sources are precedents, not inherited rules. Verify the target repository
before applying any pattern.

## Official Codex boundary

OpenAI's Codex documentation establishes three different homes for context:

- A task prompt carries the current goal, context, constraints, and completion
  condition.
- `AGENTS.md` carries durable repository guidance. Codex discovers it from the
  repository root toward the working directory, and more local guidance takes
  precedence. OpenAI recommends keeping it short, practical, and grounded in
  repeated friction.
- A skill packages a reusable workflow and loads through progressive disclosure.
  It should not become another copy of repository facts.

Sources:

- [Best practices: prompts and `AGENTS.md`](https://learn.chatgpt.com/guides/best-practices)
- [Custom instructions with `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)

The wayfinder synthesis is:

```text
one task -> prompt
durable repo-specific constraint or route -> applicable AGENTS.md
reusable cross-repository procedure -> skill
current executable behavior -> owning code, type, schema, config, or contract
conformance -> test or driven probe
```

The last line is a design judgment of this skill, not a quotation from OpenAI.

## LinkCode pattern

Inspected repository: `arcboxlabs/linkcode` at commit
`9de06705f68f7630ba5bc002f18297ad3d3c5544`.

Useful patterns:

- The root `AGENTS.md` names distinct owners for architecture, development,
  environment, and release questions.
- A “touching X, read Y first” table routes tasks instead of copying every
  downstream answer.
- Nested `AGENTS.md` files carry package-specific hazards and ownership
  boundaries.
- Architecture, operations, and release procedure are separate because they
  answer different owning questions.
- Thin compatibility files point to the shared agent instruction instead of
  restating it.
- The pull-request template asks whether behavior changes require documentation
  changes, making co-change a review concern.

Pinned sources:

- [Root `AGENTS.md`](https://github.com/arcboxlabs/linkcode/blob/9de06705f68f7630ba5bc002f18297ad3d3c5544/AGENTS.md)
- [`docs/ARCHITECTURE.md`](https://github.com/arcboxlabs/linkcode/blob/9de06705f68f7630ba5bc002f18297ad3d3c5544/docs/ARCHITECTURE.md)
- [`docs/DEVELOPMENT.md`](https://github.com/arcboxlabs/linkcode/blob/9de06705f68f7630ba5bc002f18297ad3d3c5544/docs/DEVELOPMENT.md)
- [Daemon-local `AGENTS.md`](https://github.com/arcboxlabs/linkcode/blob/9de06705f68f7630ba5bc002f18297ad3d3c5544/apps/daemon/AGENTS.md)
- [Agent-adapter `AGENTS.md`](https://github.com/arcboxlabs/linkcode/blob/9de06705f68f7630ba5bc002f18297ad3d3c5544/packages/host/agent-adapter/AGENTS.md)
- [Pull-request template](https://github.com/arcboxlabs/linkcode/blob/9de06705f68f7630ba5bc002f18297ad3d3c5544/.github/pull_request_template.md)

## What not to copy

LinkCode's root instruction file also demonstrates the risk:

- volatile protocol versions, issue identifiers, dependency behavior, and
  implementation census live in an always-loaded file;
- a routing layer can grow into a second architecture and tooling manual;
- co-change discipline reduces drift but does not prove that prose matches code.

Borrow the routing and authority split. Re-derive the file count, nesting, and
content from the target repository. Prefer a pointer when a fact already has an
owner, and prefer no file when no distinct owning question exists.
