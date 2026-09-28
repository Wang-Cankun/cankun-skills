---
name: repo-wayfinder
metadata:
  group: internal
  summary: >-
    Designs or repairs a repository's documentation system: project identity,
    document ownership rules, task-to-authority routes, and the smallest justified
    file set for a new or existing project.
description: "Design or repair a repository's documentation system — README, AGENTS.md, CLAUDE.md, docs/ — deciding which document owns each question, how agents reach it, and how it stays current. Use when setting a repository's documentation rules, or when its documents have grown bloated, scattered, stale or conflicting."
---

# Repo Wayfinder

Treat documentation as a **wayfinder**, not proof. Give each document one owning question,
an update trigger, and routes to the sources that own its claims. Current behavior belongs to
code, types, schemas, configuration or another executable contract; tests and probes verify
that owner without becoming a second one.

Stop at the decision surface (step 5) unless the user asked for the change itself — the
repair, or a new project's documents. Then carry on through step 6, taking your step-4
dispositions as accepted; the stops are the questions in steps 1 and 2, deleting or retiring
a whole document, and any change to a policy the repository has declared — each waits for the
user.

## 1. Pin identity and observation

Record the repository root, branch, exact commit and dirty paths; the scope; package or
service boundaries; and the instruction chain that applies to each scoped directory.

Before designing any route, state the project's **identity contract**: purpose and intended
users; central model, when one exists; non-goals and replacement-versus-support boundaries;
what exists now versus what is only intended. Derive it from the request, entry documents,
code and live journeys — for a new project, from the accepted goal, plan and design. The
current README is one candidate among these. When they imply materially different
identities, ask which one is declared.

**Complete when:** the work names the exact state and scope it describes, and one identity
contract is accepted or the conflict is put to the user.

## 2. Inventory authority

Discover every document that carries authority with `git ls-files`, and every agent
instruction file: `AGENTS.md` and `AGENTS.override.md`, `CLAUDE.md`, `.claude/rules/`,
`.github/copilot-instructions.md` and `.github/instructions/`, `.cursor/rules/`, `GEMINI.md`,
repository skills, and ignored local files such as `CLAUDE.local.md`, which `git ls-files`
misses. For a new project, inventory the goal, plan, design,
configuration, code skeleton and commands, and record the owning questions still unanswered.

Two kinds of unit carry authority:

- a **living document**, edited in place to stay current — classify each one;
- a **record family**, a folder of dated records written once (meeting notes, reviews,
  reports) — classify the family once, with its index.

Read [`references/archetypes.md`](references/archetypes.md), then give each unit a primary
role — an archetype, or unclassified — and a lifecycle tag: current, proposed or historical.
Record the **observed** role the content performs and the **declared** role it is meant to
carry; a filename decides neither. **A mismatch is itself a primary finding.** When the
declared role is unstated and two readings would produce materially different documents, ask.
Classify sections or claims separately when one file mixes roles or time domains. A unit with
no owning question is **sediment**, and so is an instruction written for a weaker model — read
X before every edit, always run the tests, a boundary stated more strongly than its risk — which
makes a current model over-read, over-test or stop early.

Measure what readers pay. The instruction chain and skill descriptions load on every task:
measure them against the tools' loading limits in
[`references/topology.md`](references/topology.md). Every other document is paid when a route
sends an agent to it: measure words per document and per lead, and how many files restate one
current claim.

Keep a **document rules table** throughout; for a new project its rows are proposed.

| path | observed role | declared role | owning question / audience | owns | must not own | update trigger | proof boundary | lifecycle |
|---|---|---|---|---|---|---|---|---|

**Complete when:** every living document and record family has both roles and a lifecycle
tag, or is explicitly unclassified; every mismatch and mixed block is recorded; the costs are
measured; and every proposed document has a complete row.

## 3. Walk real journeys

Take two to four representative tasks from the request, the issue surface or real entry
points, and trace each:

```text
task -> first route -> next pointer -> owning source -> test or probe
```

Inspect the owning source before accepting a document's present-tense claim about a command,
field, lifecycle or boundary; when a test and its implementation disagree, report the
conflict. Mark claims you cannot check `needs evidence`. For a new project, a journey may end
at an accepted plan: mark it `proposed` and name the evidence that will accept it.

Keep time domains apart: contracts and runbooks say what holds now, plans what is proposed,
decisions and records what was believed or observed then.

**Complete when:** every journey ends at an owner and a verification path, or at a named
unknown.

## 4. Adjudicate the map

Give each authority-bearing unit one disposition — the whole document when it is homogeneous,
a section or claim when it is mixed:

- **Keep** — it owns a distinct question and has a credible update trigger.
- **Point** — replace copied facts with a route to their owner.
- **Co-locate** — move a local rule beside the code it governs.
- **Enforce** — move a rule that must always hold into a lint, test, hook or CI check; the
  instruction file keeps at most a pointer.
- **Retire** — move displaced text out of a living document to where history lives: a record
  that already holds it, or version control unless the repository declares otherwise. The
  document's single retirement line names the successor and where the old text is.
- **Delete** — it has no unique evidence, history or owning question.
- **Needs evidence** — its authority cannot yet be judged.

Placement rules:

- **Evergreen.** A document carries facts whose change trigger matches its owning question —
  not "never changes": a map changes when a directory's purpose does, a plan when work
  completes, and the on-ramp and instruction file stay put. Judge by trigger, not by whether a
  number appears.
- **One owner, many pointers** for every current claim. Copied code facts — versions,
  exhaustive lists, error strings — are **mirrors** unless the repository declares them a
  contract; explanation that builds a mental model stays.
- **Contextual routes.** Each route names the task that fires it — schema changes →
  `docs/database.md` — so an agent reads what its task needs. What every task needs is written
  into the root instruction file; what one kind of task needs moves to the document that task
  opens, a repository skill or a path-scoped rule, leaving a route.
- **Short leads.** A document that carries state opens with it, under a bound in words as well
  as items that the repository states in its maintenance rules. Completed and earlier material
  retires.
- **Records stay; living documents shed.** Records keep their lifecycle — age alone is not
  staleness — and are corrected by an attached dated note. A living document keeps what is
  current, plus the history that still changes an action, such as a refutation that stops a
  dead end being proposed again.
- **Earned files.** Each proposed file states its owning question, non-ownership boundary,
  update trigger and proof boundary.
- **Automate syntax**, generated coupling and link integrity where useful; semantic authority
  stays with source-grounded review.

When agents keep adding to the documents, the rules for adding go into the root instruction
file as a short maintenance section.

Before proposing, creating, splitting or materially rewriting a document, read
[`references/document-templates.md`](references/document-templates.md) for its shape; before
proposing a new topology or instruction layer, also read
[`references/topology.md`](references/topology.md). Re-derive every shape from the target
repository. Before writing any line an agent will read — a maintenance section in step 5,
every edit in step 6 — load the `writing-for-agents` skill when it is installed; otherwise
hold each line to step 6's completion test.

**Complete when:** every authority-bearing unit and duplicate has exactly one disposition, and
every proposed file survives the owning-question test.

## 5. Return a decision surface

Lead with the decision. Keep items 1–6 within about 1,000 words, so the user can accept them
in one reading.

1. **Verdict** — what is broken, the mechanism that keeps producing it, and the smallest
   useful correction.
2. **Decisions for the user** — each choice only the user can make, with your
   recommendation.
3. **Identity contract.**
4. **Document rules table** — the rows that change; the full table goes to the appendix.
5. **Wayfinder** — a compact `task -> start -> authority -> verification` table.
6. **Change set** — dispositions summarized by document and pattern; ordered edits,
   deletions and pointers before additions; each created or rewritten document's archetype
   and path; the text of any maintenance section.
7. **Verification appendix** — exact commit, full rules table, per-claim dispositions, source
   anchors, probes and residual unknowns, for someone who wants to challenge the verdict.

**Complete when:** items 1–6 are counted and within the bound, the user can accept the
identity, rules, file set and edits without reading the appendix, and a verifier can retrace
the evidence.

## 6. Apply

Revalidate the premise at the current `HEAD`, then edit the fewest files that realize the
accepted dispositions.

A rule written into one document and then the next lives in both, and a correction that lands
in one copy leaves the pair issuing opposite instructions. Finish with four **sweeps** across
the whole set:

- **owner** — for each mutable claim, name its owner, then classify every other occurrence as
  pointer, evidence citation or second assertion. Grep only generates candidates: a pointer is
  a legitimate second hit, and a rephrased restatement is not greppable at all.
- **evergreen** — in guidance documents, find facts whose change trigger does not match the
  owning question, and route them to the owner whose trigger does.
- **reference** — after any move, renumber or rename, resolve every identifier: section
  labels, numbered items, paths, heading anchors, renamed symbols, routing destinations.
  Search identifiers, not old headings. Run the repository's documentation build or link check
  when it has one.
- **cold-start** — re-walk two step-3 journeys from the entry document; they prove navigation
  only if they still land after the edits, and the reads each needed show whether the edits
  cut cost. Report whether the walk ran in a fresh context or in the authoring one; only a
  fresh context is independent.

**Complete when:** each changed path implements an accepted disposition, all four sweeps are
clean, every affected journey still reaches its owner, and every changed line serves its
document's owning question — in an instruction file, by changing an action, a judgment or a
route.
