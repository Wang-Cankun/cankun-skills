---
name: repo-wayfinder
metadata:
  group: internal
  summary: >-
    Designs or repairs a repository's documentation system: project identity,
    document ownership rules, task-to-authority routes, and the smallest justified
    file set for a new or existing project.
description: Design, bootstrap, audit, or repair repository documentation systems by assigning every document an owning question and tracing real tasks to code-owned authority. Use when the user wants to establish documentation rules for a new project; organize or create README, AGENTS.md, architecture, decisions, roadmap, measurements, runbook, or contract documents; audit scattered, stale, duplicated, or mixed-role docs; or apply an accepted documentation-topology repair.
---

# Repo Wayfinder

Treat documentation as a **wayfinder**, not proof. Design a documentation system for a
new project or repair one for an existing project by giving each document one owning
question, an update trigger, and routes to the sources that own its claims. Current
behavior usually belongs to code, types, schemas, configuration, or another executable
contract. Tests and driven probes verify that owner; they do not become a second owner.

Default to a read-only diagnosis. Enter the apply branch only when the user
explicitly asks to change files.

## 1. Pin identity and observation

Read every applicable instruction file before judging the repository. Record:

- repository root, branch, exact commit, and dirty paths;
- the user-selected scope;
- package or service boundaries;
- the instruction chain that applies to each scoped directory.

Before designing the on-ramp or topology, state the project's **identity contract**:

- purpose and intended users;
- central model or structural bet, when one exists;
- explicit non-goals and replacement-versus-support boundaries;
- what exists now versus what is only intended.

For an existing project, derive candidates from the user request, entry documents, code,
and live journeys. For a new project, use the accepted goal, plan, design, and code
skeleton as provisional authority. If the user, documentation, and implementation imply
materially different identities, stop the topology decision and ask which one is
declared. Do not let the current README silently decide intent.

Preserve unrelated work. Treat an uncommitted tree as observable state, not as a
reason to clean it.

**Complete when:** the work names the exact state and scope it describes, and one
identity contract is accepted or the unresolved conflict is explicit.

## 2. Inventory authority

For an existing project, use fast repository-native discovery such as `rg --files` and
`git ls-files`. Include root and nested instruction files, READMEs, `docs/`, runbooks,
protocol documents, decisions, proposals, measurements, generated references, and issue
templates in scope. For a new project, inventory the available goal, plan, design,
configuration, code skeleton, commands, and package or service boundaries; record
missing owning questions instead of inventing answers.

Assign every discovered document a primary role:

- on-ramp — what this is, where to start;
- routing or agent instruction;
- map — where components live and how they connect;
- current contract;
- operational runbook;
- measurement or evidence;
- rationale or decision;
- proposal or plan;
- generated reference;
- unclassified.

Tag lifecycle — current, proposed, historical — separately from role.

Record two roles, not one: the **observed** role the content performs, and the
**declared** role it is intended to carry. A filename decides neither, and existing
content is not evidence of intent — `ARCHITECTURE.md` is a map in one repository and
a rationale in the next. **A mismatch is itself a primary finding.** Where the
declared role is unstated and two readings would produce materially different
documents, ask.

For each document, identify its **owning question**, audience, update trigger,
proof boundary, and any current claims it duplicates. Classify sections or claims
separately when one file mixes roles or time domains; do not force a heterogeneous
file into one authority class. A document with no owning question is a sediment
candidate.

Maintain a **document rules table** throughout the run:

| path | role | owning question / audience | owns | must not own | update trigger | proof boundary | lifecycle |
|---|---|---|---|---|---|---|---|

For a new project, rows are proposed rather than observed. Omit a row when no distinct
owning question justifies the document.

**Complete when:** every existing document in scope has an observed role, a declared
role, and a lifecycle tag or is explicitly unclassified; every mismatch and mixed block
is recorded; and every proposed document has a complete rules-table row.

## 3. Walk real journeys

Select two to four representative tasks from the user's request, current issue surface,
or actual or planned package entry points. Trace each journey:

```text
task -> first route -> next pointer -> owning source -> test or probe
```

For a new project, a journey may end at an accepted goal, design, plan, or proposed code
owner. Mark that route `proposed` and name the future acceptance evidence; do not describe
planned behavior in the present tense.

Inspect the owning code before accepting a document's present-tense verb, field,
command, lifecycle, or boundary. Use types, schemas, configuration, manifests,
and public exports as applicable executable owners. Use tests and direct probes
as conformance evidence. When they disagree, report the conflict; a green test
does not override its implementation, and failing conformance does not reveal
the intended repair by itself. Mark inaccessible or unresolved claims
`needs evidence`; do not fill the gap from convention or memory.

Keep unlike time domains separate:

- code-backed contracts answer what callers may rely on now;
- runbooks answer how to operate now;
- issues answer what work is currently proposed;
- decisions, bets, and measurements preserve what was believed or observed.

**Complete when:** every journey ends at an owner and a verification path, or at
a named unknown.

## 4. Adjudicate the map

Give each authority-bearing unit one disposition: use the whole document when it
is homogeneous, and a section or claim when it is mixed. Use dispositions for existing
material; use a proposed rules-table row for a new document.

- **Keep** — it owns a distinct question and has a credible update trigger.
- **Point** — replace copied facts with a route to their owner.
- **Co-locate** — move a genuinely local rule beside the code it governs.
- **Mark historical** — preserve it while removing present-tense authority.
- **Delete** — it has no unique evidence, history, or owning question.
- **Needs evidence** — its authority cannot yet be judged.

Apply these topology rules:

- **Guidance is evergreen**: a document carries facts whose change trigger matches
  its owning question. Not "never changes" — a map updates when a directory's purpose
  changes, which is its trigger; but finishing a planned phase must not drag the
  on-ramp and the instruction file with it. Route live state to its owner: counts and
  benchmarks to evidence, what-exists-yet to the plan, behavior to the code. Judge by
  trigger, not by whether a number appears — a version inside a versioned contract or
  a runbook is where it belongs.
- Give each current claim one authoritative owner; allow many pointers.
- Keep root `AGENTS.md` to repo-wide, non-inferable constraints, verification,
  and task routing. Add nested instructions only where local rules materially
  differ.
- Keep README as the public or package on-ramp, not an architecture and policy
  landfill.
- Keep an architecture document only when a cross-boundary mental model cannot
  be recovered cheaply from the owning sources.
- Let runbooks own operations. Let executable sources own behavior and use tests
  or probes to verify conformance.
- Keep necessary explanation that gives a human or agent a mental model, minimal
  usage example, or deliberate boundary. Treat precise version numbers,
  exhaustive implementation lists, internal lifecycle detail, and error strings
  as mirrors unless the repository explicitly declares them as a code-backed
  public contract.
- Preserve evidence and historical ledgers under their recorded lifecycle; age
  alone is not staleness.
- Keep a deliberately deferred choice in rationale or decisions. Put an accepted defect
  with an ordered repair and exit proof in the plan; the decision document may point to
  it but must not own the repair twice.
- Add a durable roadmap only when short-lived delivery plans are intentionally archived and no
  current owner answers which product or system capability horizon remains eligible for later
  work. Let that roadmap own capability ordering, promotion evidence, and the remainder after a
  plan closes—not implementation tasks or execution authority. Keep commissioned work in the
  active goal or issue, require plan completion or abandonment to reconcile the roadmap, and omit
  the roadmap when an existing current plan already owns this question.
- Create no document merely to complete a taxonomy. Require every proposed file
  to state its owning question, non-ownership boundary, update trigger, and
  proof boundary.
- Automate syntax, generated coupling, and link integrity where useful. Leave
  semantic authority to code-grounded review.

Before proposing, creating, splitting, or materially rewriting a document, read
[`references/archetypes.md`](references/archetypes.md) and
[`references/document-templates.md`](references/document-templates.md). Treat the
templates as section menus: admit a section only when the repository justifies its
reader, question, and resulting action. Before proposing a new topology or `AGENTS.md`
layer, also read [`references/topology.md`](references/topology.md). Re-derive every
shape from the target repository; never paste a template blind.

**Complete when:** every authority-bearing unit and duplicate has exactly one
disposition, and every proposed file survives the owning-question test.

## 5. Return a decision surface

Lead with the decision rather than an evidence dump. Apply the same attention test to the
response as to the documents: keep the main surface to lines that change a decision,
action, or route; move challenge material to the appendix. Return:

1. **Verdict** — what is actually broken and the smallest useful correction.
2. **Identity contract** — purpose, users, central model, non-goals, and current versus
   intended boundary.
3. **Document rules table** — path, role, ownership and non-ownership, trigger, proof,
   and lifecycle for the proposed system.
4. **Wayfinder** — a compact `task -> start -> authority -> verification` table.
5. **Disposition and minimal change set** — for an existing project, current path plus
   section or claim, disposition, and why; then ordered edits, with deletions and pointers
   before additions. Name every created, split, or rewritten document's archetype and
   destination path here, where the user can accept or reject them.
6. **Verification appendix** — exact commit, source anchors, probes, and residual
   unknowns for someone who wants to challenge the verdict.

Make the main decision legible without reading source. Put its retraceable source
trail in the verification appendix for refutation, not self-certification.

**Complete when:** the user can accept the project identity, document rules, file set,
and edits without reading the appendix, while a verifier can retrace the evidence.

## 6. Apply only on explicit request

Revalidate the premise at the current `HEAD`, then edit the fewest files that
realize the accepted dispositions. Preserve user changes and repository-specific
lifecycles. Run the relevant link, build, test, and driven-flow checks. Follow any
repository-required independent review; if a fresh context or refuter is unavailable,
mark independent verification as outstanding rather than silently self-certifying.

Writing one document and then the next carries rules forward into both, and a
correction that lands in one copy leaves the pair issuing opposite instructions —
which a reader resolves by obeying whichever comes first. So finish with four
**sweeps** across the whole set:

- **owner** — for each mutable claim, name its owner, then classify every other
  occurrence as pointer, evidence citation, or a second assertion. Grep only
  generates candidates: a pointer is a legitimate second hit, and a rephrased
  restatement is not greppable at all.
- **evergreen** — in guidance documents, find facts whose change trigger does not
  match the owning question, and route them to the owner whose trigger does.
- **reference** — after any renumber or rename, resolve every identifier: phase and
  section labels, numbered principles, paths, heading anchors, renamed symbols,
  routing destinations. Search identifiers, not old headings — a renamed heading
  puts its own references out of reach of a heading search.
- **cold-start** — have a fresh context or refuter re-walk two journeys from the entry
  document. A same-context author may run a navigation smoke test, but cannot call it an
  independent cold start. Step 3 walked the journeys before the edits; they prove
  navigation only if they still land after.

Do not commit, push, open issues, or publish unless the user asks.

**Complete when:** each changed path implements an accepted disposition, all four
sweeps are clean, every affected journey still reaches its owner, and every surviving
line changes an action, a judgment, or a route, or supports independent verification.
