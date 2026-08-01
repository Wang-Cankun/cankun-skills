# Document templates

Use these as **section menus, not forms**. Select the smallest shape that answers the
document's owning question. Omit an inapplicable section; never write `N/A` to satisfy a
template. A section is admitted only when you can name its reader, their question, and
what they do differently after reading it.

The worked pattern below is distilled from a real repository whose final system used an
on-ramp, agent rules, architecture map, decisions, roadmap, measurements, and one nested
agent guide. That is evidence that the separation can work, not a required file list for
the next repository.

## Contents

- Document rules table
- README / on-ramp
- Root AGENTS.md / agent rules
- Architecture map: package, service, or data pipeline
- Decisions / rationale
- Roadmap / plan
- Measurements / evidence
- Current contract
- Runbook

## Document rules table

Set the rules before writing prose:

| path | role | owning question / audience | owns | must not own | update trigger | proof boundary | lifecycle |
|---|---|---|---|---|---|---|---|
| `README.md` | on-ramp | What is this and where do I start? / newcomer | identity, entry, routes | status, rules, architecture detail | identity or entry changes | quickstart runs | current |
| `AGENTS.md` | agent rules | How do I work here safely? / contributor or agent | non-inferable constraints, verification, routing, hazards | state, implementation behavior, design essays | a rule, command, or hazard changes | commands and observed friction | current |
| `docs/architecture.md` | map | Where does anything live and connect? / contributor | system shape, stable structure, boundaries, formats, system terms | reasons, roadmap, copied commands | a directory purpose or boundary changes | current code and live paths | current |
| `docs/decisions.md` | rationale | Why is it shaped this way? / future maintainer | structural bets, decisions, assumptions, refutations | rules, measurements, repair steps | a decision changes or assumption resolves | links to rules and evidence | current + historical |
| `docs/roadmap.md` | plan | What next, in what order? / person choosing work | current state, ordered phases, exit proofs | architecture, rationale, benchmark detail | a phase completes or order changes | command or observable exit | proposed |
| `docs/measurements.md` | evidence | What was measured and what did it change? / challenger | decision-changing results and reproduction | current guarantees, general logs | a measurement changes a decision | dated environment, subject, method | historical evidence |
| `<scope>/AGENTS.md` | local agent rules | What differs in this subtree? / contributor in scope | materially different local rules and hazards | root rules, general architecture | a local rule or hazard changes | local commands and observed friction | current |

Those rows are examples. Add, change, or remove rows from evidence in the target
repository.

## README / on-ramp

Candidate shape:

```markdown
# <project>

<identity in one or two sentences>

<central idea or structural bet, only if it changes how a newcomer understands it>

## Where to go
| you want | read |
|---|---|
| change the repository safely | AGENTS.md |
| understand the system shape | docs/architecture.md |

## Quickstart
<smallest command or example that works>
```

Admit status, licence, support policy, or installation sections only when newcomers need
them. Route live progress to a plan. Route detailed architecture, rules, and history to
their owners.

## Root AGENTS.md / agent rules

Candidate shape:

```markdown
# <project> — agent guide

<one-line orientation, only if rules are otherwise easy to misread>

## Constraints
<repo-wide, non-inferable, decision-changing rules>

## Verification
<exact build, test, lint, and driven-probe commands>

## Routing
| touching | read first |
|---|---|
| <area or question> | <owning source> |

## Hazards
<only hazards that have bitten or are independently established>
```

Add a nested `AGENTS.md` only where local rules materially differ. Keep reasoning in
decisions, state in the plan, and current behavior in code or executable contracts.

## Architecture map

An architecture document answers: *where does anything live, and how does it connect?*
Choose one dominant shape below and combine sections only while that question remains the
owner.

### Package or small application

```markdown
# Architecture
> A map. Why → decisions; what next → plan; rules → AGENTS.md.

## System shape or live call path
<entry → modules → output>

## Project structure
<stable directories and file groups, each with one responsibility>

## Components and boundaries
| component | responsibility | dependencies | must not know |
|---|---|---|---|

## Glossary
<only contested or deliberately unconventional system terms>
```

### Service or web system

```markdown
# Architecture
## Context and data flow
<users, frontends, services, stores, external systems>

## Components and boundaries
| component | responsibility | interface | owner |
|---|---|---|---|

## Data stores
<what is persisted, where, and why it matters to navigation>

## External integrations
<trust and failure boundaries, not a vendor census>

## Deployment and security surfaces
<only when they exist and a reader must find them>
```

### Data, research, or build pipeline

```markdown
# Architecture
## Pipeline shape
INPUT → transform/build → artifact → analysis/service/consumer

## Current live path
<show this separately when the target shape is not implemented yet>

## Project structure
<stable stage, package, script, data, and output groups>

## Formats and provenance boundaries
<what crosses stages; where identity, validation, and reproducibility are established>

## Components and ownership
| stage | owns | consumes | produces | verifies |
|---|---|---|---|---|
```

Candidate sections from broader architecture templates include project structure, system
diagram, core components, data stores, external integrations, deployment, monitoring,
security, development environment, and glossary. Each is optional. Put future work in a
plan, reasons in decisions, exact operating procedures in a runbook, and contacts or
repository identity in the on-ramp or repository metadata. List stable groups rather than
an exhaustive file census.

## Decisions / rationale

```markdown
# Decisions
> Owns why. Rules → AGENTS.md; numbers → evidence; repair steps → plan.

## Structural bet
<the choice that explains several downstream choices>

## Principles, and why each holds
<reasoning that connects evidence to a rule; point to both owners>

## Decisions and assumptions
| decision or assumption | status | evidence or consequence |
|---|---|---|

## Refuted or historical
<dead ends worth preventing from recurring>

## Open or deliberately deferred decisions
<choices not yet made; no invented resolution>
```

A deliberately deferred choice belongs here. An accepted defect with repair steps and an
exit proof belongs in the plan; keep only a pointer in decisions.

## Roadmap / plan

```markdown
# Roadmap
> Owns what next and in what order. Does not own where, why, rules, or evidence.

## Current state
<the asymmetry or constraint that determines the route>

## Goal or milestone
<observable outcome, not a theme>

## Ordered phases
### <phase>
<actions, dependencies, stop conditions>
**Exit proof:** <command or observation>

## Open questions
<questions whose answers may reorder the plan>
```

This is the legitimate home for state. Move completed reasoning worth preserving to
decisions; remove completed task detail that changes no future action.

## Measurements / evidence

```markdown
# Measurements
> Owns numbers that change a decision and how to re-measure them.

## Results that matter
| observation | measured result | decision consequence |
|---|---|---|

## Detail and reproduction
<date, environment, subject, method, command or script>
```

Lead with consequences, then detail, then reproduction. A dated number is evidence, not
a guarantee. Exclude results that change no decision or next action.

## Current contract

```markdown
# <contract>
<scope and version>
<inputs, outputs, invariants, errors, compatibility>
<source schema or generator>
```

Prefer generation from code, schema, or types. A hand-written contract must name its
executable owner and update trigger.

## Runbook

```markdown
# <operation> runbook
<when to use this procedure>
<prerequisites and access>
<steps with expected observations>
<health check, rollback, escalation>
```

Concrete commands, versions, endpoints, and recovery values belong here when operators
need them under time pressure. Keep architecture explanations and design history out.
