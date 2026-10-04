# Document templates

Section menus, not forms: pick the smallest shape that answers the document's owning
question. Each document's role is in [`roles.md`](roles.md).

## Contents

- README / on-ramp
- Root AGENTS.md / agent rules
- Architecture map
- Decisions / rationale
- Roadmap / plan
- Measurements / evidence
- Record family index
- Current contract
- Runbook
- Retirement line

## README / on-ramp

Candidate shape:

```markdown
# <project>

<identity in one or two sentences>

<the central idea in one sentence, linking to the decisions that own it; only if it changes
 how a newcomer understands the project>

## Where to go
| you want | read |
|---|---|
| change the repository safely | AGENTS.md |
| understand the system shape | docs/architecture.md |

## Quickstart
<smallest command or example that works>
```

Admit status, licence, support or installation sections only when newcomers need them;
route progress, architecture, rules and history to their owners.

## Root AGENTS.md / agent rules

Candidate shape:

```markdown
# <project> — agent guide

<one-line orientation, only if rules are otherwise easy to misread>

## Commands
<exact build, test, lint, and driven-probe commands>

## Constraints
<repo-wide, non-inferable, decision-changing rules, and the grants beside them:
 workflows the agent may carry through without asking>

## Routing
| touching | owner |
|---|---|
| <the task that fires the route> | <owning source> |

## Hazards
<repo-wide hazards that have bitten or are independently established>

## Document maintenance
<only when agents keep adding to the documents: a few rules, with the word and item limits
 this repository sets for documents that open with state>
```

A grant reads like: "The local tests use disposable fixtures and have no production
access. Run them, fix failures caused by the requested change, and rerun affected tests
without asking for approval at each step."

Maintenance rules, a menu to re-derive rather than copy:

- **Owner first** — update the owner named in the routing table; link from elsewhere.
- **Replace the slot, append the record** — the same question and scope revises the
  current entry in place, and version control keeps the old wording; a distinct result,
  decision or record is a new entry; a verbatim record gets a dated correction attached.
- **Short openings** — the word and item limits for documents that open with state.
- **Finish the update** — when work completes or direction changes, update each owner whose
  question changed (the plan's state, a decision's status) and repair anchors that moved;
  a pointer elsewhere needs no edit.


## Architecture map

Write one only when the map role earns its place. Choose sections from: system shape or live
call path (`entry → modules → output`, or `input → stage → artifact → consumer` for a
pipeline) · stable directories and file groups, each with one responsibility · components and
boundaries (`component | responsibility | interface | must not know`) · data stores and
formats, where persistence affects navigation · external integrations as trust and failure
boundaries · contested system terms.

## Decisions / rationale

```markdown
# Decisions
> Owns why. Rules → AGENTS.md; numbers → evidence; repair steps → plan.

## Current direction
| decision or assumption | status | decided by, when, source | evidence → |
|---|---|---|---|
<the structural bet first, then each decision in force, one line each>

## Principles, and why each holds
<reasoning that connects evidence to a rule; point to both owners>

## Open or deferred
<choices not yet made; no invented resolution>

## Refuted
<dead ends, each with the evidence that closed it>

## Course of the work
<a few dated lines on how the direction changed and why; only once it has changed>
```

## Roadmap / plan

```markdown
# Roadmap
> Owns what next and in what order. Why → decisions; numbers → evidence.

## Current state
<within the stated bound: the stage, and the constraint that determines the route>

## Next
<a few items, each a short paragraph: action, owner, the decision it informs, exit>

## Ordered phases
### <phase>
<actions, dependencies, stop conditions>
**Exit proof:** <command or observation>

<one retirement line: where displaced plans live>
```

Procedures sit behind whatever a Next item links to. Completed reasoning worth keeping moves
to decisions; completed task detail retires.

## Measurements / evidence

```markdown
# Measurements
> Owns numbers that change a decision and how to re-measure them.

## Results that matter
| observation | measured result | bears on → |
|---|---|---|

## Detail and reproduction
<date, environment, subject, method, command or script>
```

The decision a result bears on lives in decisions, reached by the link.

## Record family index

```markdown
# <Meeting notes | Reviews | Reports>
> Dated records. Current decisions → decisions; active work → roadmap.

| date | record | who or what | question | outcome → |
|---|---|---|---|---|
```

One row per record, added when the record is. The outcome column points to where the
result went — a decision, an evidence entry, or nowhere yet.

## Current contract

Scope and version · inputs, outputs, invariants, errors, compatibility · the schema or
generator it comes from. Prefer generating it; a hand-written contract names its executable
owner.

## Runbook

When to use it · prerequisites and access · steps with expected observations · health check,
rollback, escalation. Concrete commands and values belong here.

## Retirement line

A document that retired whole sections keeps one dated line, at the point where they stood,
naming what replaced them and where the old text is; a later retirement updates that line to
the newer commit. An in-place revision of a current entry needs no line.

```markdown
> Earlier plans retired <date>: `git show <commit>:docs/roadmap.md`. Current work → [Next](#next).
```

The line says where to go now. The caveats it might list — what the old text no longer
authorizes, which scoped decisions still stand — already live in the owner it points to.
