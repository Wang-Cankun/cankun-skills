# Document templates

Use these as **section menus, not forms**: select the smallest shape that answers the
document's owning question. Each section passes the admission test, and each document's
ownership comes from its card, both in [`archetypes.md`](archetypes.md); this file holds only
shapes.

## Contents

- Document rules table
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

## Document rules table

Set the rules before writing prose:

| path | observed role | declared role | owning question / audience | owns | must not own | update trigger | proof boundary | lifecycle |
|---|---|---|---|---|---|---|---|---|
| `README.md` | on-ramp | on-ramp | What is this and where do I start? / newcomer | identity, entry, routes | status, rules, architecture detail | identity or entry changes | quickstart runs | current |
| `AGENTS.md` | agent rules | agent rules | How do I work here safely? / contributor or agent | repo-wide non-inferable constraints, grants, verification, routing, repo-wide hazards, maintenance rules | state, implementation behavior, design essays, single-task procedures and hazards | a rule, grant, command, or hazard changes | commands and observed friction | current |
| `docs/architecture.md` | map | map | Where does anything live and connect? / contributor | system shape, stable structure, boundaries, formats, system terms | reasons, roadmap, copied commands | a directory purpose or boundary changes | current code and live paths | current |
| `docs/decisions.md` | rationale | rationale | Why is it shaped this way? / future maintainer | current direction, decisions in force, open choices, refutations | rules, measurements, repair steps | a decision changes or assumption resolves | links to rules and evidence | current |
| `docs/roadmap.md` | plan | plan | What next, in what order? / person choosing work | current state, next items, ordered phases, exit proofs | architecture, rationale, benchmark detail | an item completes or blocks, or order changes | command or observable exit | current |
| `docs/measurements.md` | evidence | evidence | What was measured, and what does it bear on? / challenger | decision-bearing results and reproduction | current guarantees, the decisions themselves, general logs | a new measurement or a dated correction | dated environment, subject, method | current; entries historical |
| `docs/<records>/` | record family | record family | What was asked, found, or advised then? / anyone tracing a decision | dated records and their index | current decisions, task order, standing rules | a new record or a dated correction | the record itself | historical |
| `<scope>/AGENTS.md` | local agent rules | local agent rules | What differs in this subtree? / contributor in scope | materially different local rules and hazards | root rules, general architecture | a local rule or hazard changes | local commands and observed friction | current |

These rows are examples in which observed and declared roles agree; derive the real rows
from the target repository.

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
| touching | read first |
|---|---|
| <the task that fires the route> | <owning source> |

## Hazards
<repo-wide hazards that have bitten or are independently established>

## Document maintenance
<only when agents keep adding to the documents: a few rules, with the lead bounds>
```

A grant reads like: "The local tests use disposable fixtures and have no production
access. Run them, fix failures caused by the requested change, and rerun affected tests
without asking for approval at each step."

Maintenance rules, a menu to re-derive rather than copy:

- **Owner first** — update the owner named in the routing table; link from elsewhere.
- **Replace the slot, append the record** — the same question and scope revises the
  current entry in place, and version control keeps the old wording; a distinct result,
  decision or record is a new entry; a verbatim record gets a dated correction attached.
- **Short leads** — the bounds this repository's lead documents keep, in words and items.
- **Finish the update** — when work completes or direction changes, update each owner whose
  question changed (the plan's state, a decision's status) and repair anchors that moved;
  a pointer elsewhere needs no edit.


## Architecture map

Write one only when the map archetype admits it. Choose sections from: system shape or live
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
