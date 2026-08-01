# Archetypes

Read before creating, splitting, or materially rewriting a document. These are
**selection cards, not templates**: each names an owning question and an admission
test, and the shapes are candidates to choose among. A heading admitted because the
archetype lists it — rather than because this repository justifies it — becomes an
N/A section that spends attention and returns nothing.

Two documents may share an archetype. One document may not serve two: split it, or
declare the primary role and route the rest.

## Selecting

For every document, settle six things before writing:

| | |
|---|---|
| **owning question** | the one question a reader arrives with |
| **audience** | a newcomer, a contributor mid-task, an agent, an operator |
| **must not own** | the neighbouring questions, each named with its owner |
| **update trigger** | what event obliges an edit — and nothing else may |
| **proof boundary** | what the document asserts vs what it only routes to |
| **lifecycle** | current, proposed, or historical |

**Admission test for any section**: name the reader, their question, and what they do
differently having read it. A section that cannot answer all three is not admitted.

## The archetypes

### on-ramp
*What is this, and where do I start?* Newcomer, read once.
Identity in a sentence or two · the central idea · a routing table to everything
else · a quickstart that runs.
**Must not own** status, architecture, rules, or history — it *points* at each.
**Trigger**: identity or entry point changes. Not progress.
Distinct from a map: same subject, different depth and audience. An on-ramp that
starts explaining components has become a map and should route to one instead.

### rules / agent instruction
*How do I work here safely?* Contributor or agent, read before acting.
Non-inferable constraints · verification commands · routing table · hazards that
have actually bitten.
**Must not own** reasoning (rationale), state (plan), or behavior (code).
**Trigger**: a rule, command, or hazard changes.
Inferable advice is a no-op. Each hazard earns its place by having cost something.

### map
*Where does anything live, and how does it connect?* Anyone orienting, read repeatedly.
System shape · directory structure · components and boundaries · storage or data
formats · glossary · a live call path when the shape diagram shows a target state.
**Must not own** why (rationale) or when (plan).
**Trigger**: a directory's purpose or a boundary changes.
List directories and stable file *groups*; an exhaustive file census is a mirror
that decays on the next commit. A glossary earns its place where vocabulary is
contested or deliberately unconventional — define the system's terms, not the
domain's.
Admit *storage formats* only where persistence materially affects navigation;
*deployment*, *security*, *monitoring* only where such a surface exists and a reader
must find it. Absent, they are omitted, not marked N/A.

### current contract
*What may callers rely on?* Integrator.
**Trigger**: the contract changes — and a version number here is correct, not a
volatile fact. Prefer generation from schema or code; hand-written contracts drift.

### runbook
*How do I operate it?* Operator, under time pressure.
**Trigger**: the procedure changes. Concrete values and versions belong here.
Worth creating once there is something to operate — secrets, rollback, health checks.

### rationale / decision
*Why is it this way?* Anyone questioning a design; also the future author.
The structural bet · principles, each compressed to the reasoning that connects a
rule to its evidence · decisions and assumptions with status, **including refuted
ones** · open decisions.
**Must not own** the rule (that is guidance) or the number (that is evidence).
**Trigger**: a decision changes or an assumption resolves.
Record refutations: an unrecorded dead end is proposed again. Prefer this name over
"argument", which invites essays.
A deliberately deferred choice remains a decision. Once a defect has an accepted repair
order and exit proof, its active owner is the plan; leave at most a pointer here.

### evidence
*What was measured, when, and how do I re-run it?* Anyone challenging a claim.
Decision-changing results first · detail below · reproductions last · date,
environment, and subject on every entry.
**Trigger**: a new measurement changes a decision. A result that would alter nobody's
next action is not evidence, it is a log.
A number here is dated, not guaranteed. Reproduction material stays even though it
changes no action on its own — it is what makes independent verification possible.

### proposal / plan
*What next, in what order?* Anyone choosing the next task.
Ordered phases, each with an exit proof that is a command or an observation.
**Must not own** why (rationale) or where (map).
**Trigger**: a phase completes or the order changes.
This is the document that legitimately carries state, which is what frees the others
from carrying any.
Own accepted defects here once their repair is planned; do not duplicate their action
steps in the decision record.

### generated reference
Owned by its generator. Never hand-edited; regenerate instead.

## Anti-patterns

- A section admitted because the archetype lists it.
- An exhaustive file, symbol, or dependency census in a map — a mirror with a decay
  rate.
- A rationale document that restates its rules instead of pointing at the guidance
  that owns them.
- One repository's document set copied whole into another. The archetypes are stable;
  which ones a repository needs is not.
