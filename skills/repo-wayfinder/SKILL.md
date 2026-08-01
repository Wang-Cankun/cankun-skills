---
name: repo-wayfinder
metadata:
  group: internal
  summary: >-
    Audits repository documentation by walking real tasks to the code that owns
    each claim, then returns a decision surface: a wayfinder table, per-document
    dispositions (keep, point, co-locate, mark historical, delete), and the
    minimal change set.
description: Wayfind repository documentation by tracing real tasks to code-owned authority. Use when the user wants to audit scattered, stale, duplicated, or mixed-role docs; decide whether README, AGENTS.md, architecture, runbook, or protocol documents should exist and where they belong; or apply an accepted documentation-topology repair.
---

# Repo Wayfinder

Treat documentation as a **wayfinder**, not proof. A wayfinder earns its place by
helping a task reach the source that owns the answer. Current behavior usually
belongs to code, types, schemas, configuration, or another executable contract.
Tests and driven probes verify that owner; they do not become a second owner.

Default to a read-only diagnosis. Enter the apply branch only when the user
explicitly asks to change files.

## 1. Pin the observation

Read every applicable instruction file before judging the repository. Record:

- repository root, branch, exact commit, and dirty paths;
- the user-selected scope;
- package or service boundaries;
- the instruction chain that applies to each scoped directory.

Preserve unrelated work. Treat an uncommitted tree as observable state, not as a
reason to clean it.

**Complete when:** the audit names the exact state and scope it is describing.

## 2. Inventory authority

Use fast repository-native discovery such as `rg --files` and `git ls-files`.
Include root and nested instruction files, READMEs, `docs/`, runbooks, protocol
documents, decisions, proposals, measurements, generated references, and issue
templates in scope.

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

**Complete when:** every document in scope has an observed role, a declared role, and
a lifecycle tag or is explicitly unclassified; every observed/declared mismatch is
recorded as a finding; and every mixed-role or mixed-time block is identified.

## 3. Walk real journeys

Select two to four representative tasks from the user's request, current issue
surface, or actual package entry points. Trace each journey:

```text
task -> first route -> next pointer -> owning source -> test or probe
```

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
is homogeneous, and a section or claim when it is mixed.

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
- Create no document merely to complete a taxonomy. Require every proposed file
  to state its owning question, non-ownership boundary, update trigger, and
  proof boundary.
- Automate syntax, generated coupling, and link integrity where useful. Leave
  semantic authority to code-grounded review.

Before creating, splitting, or materially rewriting any document, read
[`references/archetypes.md`](references/archetypes.md) and admit only the sections
the repository actually justifies. Before proposing a new document topology or a new
`AGENTS.md` layer, read [`references/topology.md`](references/topology.md). Re-derive
every shape from the target repository; never paste a template blind.

**Complete when:** every authority-bearing unit and duplicate has exactly one
disposition, and every proposed file survives the owning-question test.

## 5. Return a decision surface

Lead with the decision rather than an evidence dump. Return:

1. **Verdict** — what is actually broken and the smallest useful correction.
2. **Wayfinder** — a compact `task -> start -> authority -> verification` table.
3. **Disposition table** — current path plus section or claim when needed,
   owning question, disposition, and why.
4. **Minimal change set** — ordered edits, including deletions and pointers
   before additions. For every document that will be created, split, or rewritten,
   name its **archetype and destination path here**, where the user can accept or
   reject them. Deciding either while writing changes an accepted topology without
   consent.
5. **Verification appendix** — exact commit, source anchors, probes, and residual
   unknowns for someone who wants to challenge the verdict.

Make the main decision legible without reading source. Put its retraceable source
trail in the verification appendix for refutation, not self-certification.

**Complete when:** the user can decide what to change from the first four
sections, while a verifier can independently retrace the fifth.

## 6. Apply only on explicit request

Revalidate the premise at the current `HEAD`, then edit the fewest files that
realize the accepted dispositions. Preserve user changes and repository-specific
lifecycles. Run the relevant link, build, test, and driven-flow checks. Follow any
repository-required independent review; if a fresh refuter is unavailable, mark
that verification as outstanding rather than silently self-certifying.

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
- **cold-start** — re-walk two journeys from the entry document without the author's
  memory. Step 3 walked them before the edits; they prove navigation only if they
  still land after.

Do not commit, push, open issues, or publish unless the user asks.

**Complete when:** each changed path implements an accepted disposition, all four
sweeps are clean, every affected journey still reaches its owner, and every surviving
line changes an action, a judgment, or a route, or supports independent verification.
