# Document roles

Each role names the question a reader arrives with, what the document must not own, and the
event that obliges an edit. Which roles a repository needs is re-derived per repository; one
document serving two roles is split, or declares its primary role and routes the rest. A
section earns its place when you can name its reader, their question, and what they do
differently having read it.

### on-ramp
*What is this, and where do I start?* Newcomer, read once.
**Must not own** status, architecture, rules, or history — it *points* at each.
**Trigger**: identity or entry point changes.
An on-ramp that starts explaining components has become a map and should route to one.

### rules / agent instruction
*How do I work here safely?* Contributor or agent, loaded on every task.
**Must not own** reasoning (rationale), state (plan), behavior (code), what only one kind
of task needs (the document that task opens), or a rule that must always hold (a check).
**Trigger**: a rule, grant, command, or hazard changes.
Every line is paid on every task. A **grant** names a workflow the agent may finish
without asking, such as a local test suite on disposable fixtures; a capable agent stops
early where a boundary is stated more strongly than the risk.

### map
*Where does anything live, and how does it connect?* Anyone orienting, read repeatedly.
**Must not own** why (rationale) or when (plan).
**Trigger**: a directory's purpose or a boundary changes.
List directories and stable file *groups*; a file census decays on the
next commit. A glossary defines the system's contested terms, not the domain's. Keep a map
only when a cross-boundary mental model cannot be recovered cheaply from the owning sources.

### current contract
*What may callers rely on?* Integrator.
**Must not own** rationale (decision) or usage walkthroughs (on-ramp or runbook).
**Trigger**: the contract changes — a version number here is correct, not a volatile fact.
Prefer generation from schema or code; hand-written contracts drift.

### runbook
*How do I operate it?* Operator, under time pressure.
**Must not own** why (decision) or whether a procedure may run now (plan).
**Trigger**: the procedure changes. Concrete values and versions belong here.

### rationale / decision
*Why is it this way?* Anyone questioning a design; also the future author.
**Must not own** the rule (guidance), the number (evidence), or repair steps (plan).
**Trigger**: a decision changes or an assumption resolves.
The document holds decisions in force, open choices and refutations, each with who decided,
when and on what source; superseded and completed entries retire. Advice — from a review, a
report or another agent — becomes a decision only when someone with authority records it
here. Refutations stay: an unrecorded dead end is proposed again.

### evidence
*What was measured, when, and how do I re-run it?* Anyone challenging a claim.
**Trigger**: a new measurement, or a dated correction to one.
A number here is dated, not guaranteed. A result that bears on no decision is a log.
Reproduction material stays: it is what makes independent verification possible.

### proposal / plan
*What next, in what order?* Anyone choosing the next task.
**Must not own** why (rationale) or where (map).
**Trigger**: an item completes or blocks, or the order changes.
The one place that carries state — a plan document, a plans folder or the issue tracker —
which frees the others from carrying any. A durable roadmap beside
short-lived delivery plans earns its place only when those plans are archived and nothing
else answers which capability comes next; each plan's end reconciles it.

### record
*What was asked, found, or advised then?* Anyone tracing how a decision was reached.
A folder of dated files — meeting notes, reviews, investigation reports, reading notes —
with an index of one row per record: date, subject, and where its outcome went.
**Must not own** current decisions, task order, or standing rules.
**Trigger**: a new record, or a dated correction attached to one.
Historical from birth: a record is never rewritten to match today. Classify the family
once; per-file metadata beyond date and subject is overhead.

### summary for readers
*What is the proposal or argument, for this reader, as of this date?* A proposal brief, a
paper draft, a status report.
Either a **dated snapshot**, written once for its occasion and then handled as a record, or
a **page of pointers** that states nothing its owners do not. A summary kept in sync by hand
is one more copy of every current claim.
**Trigger**: a new occasion calls for a new snapshot.

### generated reference
Owned by its generator. Regenerate instead of editing by hand. Documentation published for
other agents — an `llms.txt` index, Markdown mirrors of doc pages — is generated from the
docs it serves.
