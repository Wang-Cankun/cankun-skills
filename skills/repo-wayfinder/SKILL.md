---
name: repo-wayfinder
metadata:
  group: repos
  summary: >-
    Checks or designs a repository's documentation system: which document owns each
    question, how agents reach it, and how it stays current.
description: "Check or design a repository's documentation system (README, AGENTS.md, CLAUDE.md, docs/): which document owns each question and how agents reach it. Use when existing docs have drifted, conflict or keep needing sync passes, or to design or rebuild a project's documentation set."
---
# Repo Wayfinder

Documentation routes; it does not prove. Every current claim has one **owner** — code, a
type, a schema, configuration, or one living document — and every other mention is a
**pointer** to it. Tests and probes verify the owner without becoming a second one.

A **cache** is a sentence that restates the code, so a refactor that keeps the design would
make it false: a constant, a field name, a page size, which file does what, the order of
queries. It is a second owner, edited with every change or left stale. A living document states
what the code cannot: the job and the boundary, the invariant a caller relies on, the hazard
that bit, the reason. When a document drifts again after each fact check, cut its cache
instead of checking it again.

A sentence is **stale** when its owner now says otherwise: a present-tense claim the code
contradicts, a decision a later one superseded, a link to a moved or removed target, a status
or next step shown as current that is done or dropped. The aim is no stale sentence, not a
length: cache goes because it goes stale, and a long document of owned, true sentences stays.

- A **living document** is edited in place to stay current. It owns one question and changes
  when that question's answer changes: its update trigger.
- A **record** is dated and written once (a review, report, meeting note), kept in a folder
  with an index, and corrected by an attached dated note, never rewritten.

## Quick pass (default)

1. Pin the commit agents actually load (the primary checkout's branch: a rule changed on an
   unmerged branch still loads from the trunk), the scope and the instruction chain
   (`AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, `GEMINI.md`, tool rule folders, an agent
   memory index, ignored local files), and measure the chain against the loading limits.
2. Walk two to four real tasks from a cold start:
   `task -> first route -> next pointer -> owner -> test or probe`. Check every present-tense
   claim and stated decision on the way against its owner; each stale one is a finding (when a
   test and its implementation disagree, report it). Count the files and words each walk read.
   Where agent session transcripts exist, also count which documents agents actually opened in
   recent sessions: a historical file opened at all is a finding.
3. For each code-adjacent document the walks read, measure over the last month or two the
   share of its code's changes that also edit it, and the changes that only re-sync it; count
   from the module's first build, per merged change. A document
   that changes with most of them, or whose stated update trigger is "the implementation
   changes", is a cache: report that, with sample cache sentences, rather than its stale facts.
4. In the instruction chain and the documents the walks read, find current claims stated in
   more than one place (versions, commands, behaviours, limits) and name each one's owner.
   Also flag sections with no owning question, and rules written for a weaker model (read X
   before every edit, always run every test, a boundary stated more strongly than its risk).
5. Report the findings, each with evidence and one disposition, and the choices only the user
   can make.

Done when every walk ends at an owner and a check, or at a named unknown, and every finding
has a disposition.

## Full pass (designing or rebuilding a documentation system)

The quick pass, plus:

- State the project's identity: purpose and users, non-goals, what exists now versus what is
  intended. When the request, entry documents and code imply different identities, ask which
  one is declared.
- Give every living document and record family a row:
  `path | role | owning question | update trigger | lifecycle (current, proposed, historical)`.
  An observed role that differs from the declared one is a finding; a file that mixes roles or
  time frames (now, next, then) is classified by section.
- Check every living document for stale sentences, not only those the walks read.
- For a new project, take the identity and tasks from the accepted goal, plan and code
  skeleton; rows are `proposed`, and a walk may end at a planned owner, naming the evidence
  that will accept it.
- Report within about 1,000 words: the verdict and the mechanism that
  keeps producing it; the user's decisions with a recommendation each; the changed rows; a
  `task -> start -> owner -> check` table; the ordered change set, with edits, pointers and
  retirements before additions. Evidence goes in an appendix.

Done when every living document and record family has a row or is marked unclassified, every
role mismatch is a finding, and the report body is within the bound.

## Dispositions

- **Keep** — owns a distinct question and has a credible update trigger.
- **Point** — copied facts become a link to their owner.
- **Co-locate** — a local rule moves beside the code it governs.
- **Enforce** — a rule that must always hold becomes a lint, test, hook or CI check; the
  document keeps at most a pointer.
- **Retire** — displaced text moves to where history lives (a record, version control, or an
  archive the repository declares), leaving one line that names the successor and where the
  old text is. The archive sits outside agents' default search (an `.ignore` or `.rgignore`
  entry for ripgrep-based search, or a Read deny rule); a status label does not stop an agent
  from reading a file, and a superseded plan that still reads fluent and on-topic is the
  costliest distractor.
- **Delete** — no unique evidence, history or owning question.
- **Needs evidence** — its authority cannot be judged yet.

## Placement

- A fact sits where its change trigger matches the document's owning question; judge by the
  trigger, not by whether a number appears: a port an operator types belongs in a runbook.
  Copied versions, lists and error strings point to their owner; explanation that builds a
  mental model stays unless it is cache.
- Cache goes to its owner: a constant or bound → Point to the named constant; a hazard local to
  one function → Co-locate it as a comment at the site; a restated test assertion → Point to
  the test; narration of control flow, query shape, or which file does what below the
  directory level → Delete. A pointer names a path, anchor or symbol that a link or symbol
  check resolves (Enforce).
- Each route names the task that fires it (schema change → `docs/database.md`). What every
  task needs goes in the root instruction file; what one kind of task needs goes in the
  document, skill or path-scoped rule that task opens.
- A document that carries state opens with it, and completed material retires. Agent memory
  points to that document; a copy of project state in memory is one more owner going stale.
- Living documents keep what is current plus history that still changes an action, such as a
  refutation that stops a dead end from being proposed again. Records keep their lifecycle.
- A new file states its owning question, what it must not own, its update trigger and what it
  proves versus only routes to.
- A brief or handover gives the goal, the open question and the settled decisions, and links
  earlier designs for comparison after the reader has stated its own model; a reading order
  through them makes the old answer the starting point ([roles](references/roles.md)).

## Applying

Report and stop unless the user asked for the change itself. Deleting or retiring a whole
document, or changing a policy the repository declares, waits for the user. Re-pin the
commit, apply the dispositions with the fewest files, then sweep:

- **owner** — every other occurrence of a changed claim is a pointer, an evidence citation or
  a second assertion to fix; grep finds candidates, rephrasings need reading;
- **reference** — resolve every moved path, anchor, numbered item and renamed symbol, and run
  the repository's link check when it has one;
- **content** — after a split or move, every paragraph and table row of the original appears
  in the new files, unless the change deliberately retires it; a cache cut keeps every hazard
  and caller-facing invariant it held, in the document or co-located at the code;
- **claims** — cut cache by deleting it, and keep the surviving sentences as they stand: a
  deletion adds no claim, while every written or reworded sentence is a new one. A reader that
  did not write those checks them against the code; a claim that holds only with its
  qualifiers goes to its owner rather than into a shorter sentence;
- **cold start** — re-walk two journeys from the entry document, compare the reads, and say
  whether the walk ran in a fresh context.

Done when each changed path implements a disposition, the sweeps are clean, and every changed
line in an instruction file changes an action, a judgement or a route.

## Where things are

- [`references/roles.md`](references/roles.md) — document roles (on-ramp, agent rules, map,
  module guide, contract, runbook, decision, evidence, plan, record, brief, summary,
  generated), each with its owning question, what it must not own and its update trigger.
- [`references/document-templates.md`](references/document-templates.md) — section shapes
  for a README, AGENTS.md, map, module guide, decisions, plan, evidence, record index,
  contract, runbook and retirement line.
- [`references/topology.md`](references/topology.md) — instruction-chain loading limits,
  nested and cross-tool instruction layers, and the `AGENTS.md` / `CLAUDE.md` layouts.
