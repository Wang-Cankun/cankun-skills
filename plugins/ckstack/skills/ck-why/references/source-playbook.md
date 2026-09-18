# Source playbook

Choose sources by what could answer the question and what is actually available. Follow explicit leads first, expand when needed, and adapt searches to the host's tools. These categories are options, not a required sweep.

## Source history and local records

Commits, reviews, issues, comments, tests, decision records, notebooks, configuration history, and pipeline reports often provide the closest link to the target. Use [sources/code-archaeology.md](sources/code-archaeology.md) for history commands and pitfalls.

Look for the introduction of a behavior as well as its latest edit. Tests and outputs show the cases the change addressed; an explanation in a review or method note is stronger evidence of why.

## Issue trackers

Start with linked issues, then search target names and symptoms. Read the discussion, parent initiative, and duplicate chains where relevant. Product requirements, performance incidents, review feedback, or a missing analysis capability can supply the forcing function.

Check whether scope changed before implementation. Labels and templates are clues; a filled-in “Why” field containing only generic boilerplate is weak evidence. Retain the issue identifier, relevant statement, and link.

## Documents and methods records

Search design documents, decision records, meeting notes, protocols, analysis plans, method notes, and supplied papers using the feature, stage, parameter, or author. Read alternatives and consequences, not only the current summary.

Distinguish a draft plan from the adopted decision, and compare the document with the implementation version at issue. For analytical choices, identify data assumptions and any stated reason for a method or threshold. A published default alone does not establish why this project adopted it.

## Conversations and session history

Search relevant team discussions or available prior agent sessions when the rationale may not have reached a formal document. Search explicit links, feature or project terms, participants, and the decision's surrounding context. Read the whole relevant thread instead of quoting a message without its replies.

An available history retrieval tool, including `obelisk`, can locate earlier user decisions, alternatives, and experiment records. Inspect the underlying record when possible. Separate user choices from an agent's suggestions and unverified summaries. Missing retention, inaccessible conversations, and incomplete session exports limit the claim a null search supports.

## Runtime and operational evidence

Metrics, dashboards, scheduler logs, resource reports, traces, and incident records can explain the conditions around a change. Identify the relevant service, job, or stage before querying. Inspect units, aggregation, sampling, and retention. Bound queries to the relevant events or runs and return concise summaries rather than log dumps.

A performance or memory spike followed by a corrective change supports a hypothesis; it does not establish causation by itself. Check neighboring changes and explicit rationale. An alert threshold shows what was monitored, not necessarily why code used the same number.

## Error and failure history

Search matching error strings, affected versions, stack traces, failed jobs, and issue discussion. Confirm that the failure passes through the target and inspect the releases or workflow revisions around the correction.

An error disappearing may reflect sampling, renamed grouping, upstream changes, or retention rather than a fix. A “resolved” issue is a status marker until linked evidence shows what happened. Treat automated root-cause narratives as hypotheses and actual logs or events as the primary record.

## Data, experiments, and analytical evidence

Inspect the actual schemas, run manifests, experiment records, and data lineage before querying. Use bounded read-only summaries appropriate to the question, such as counts, distributions, missingness, exposure groups, or resource measurements. Record the query or calculation, input scope, units, filters, and result needed to reproduce the finding.

Distinguish raw and transformed data, deduplication, refresh lag, changing instrumentation, and versioned reference inputs. An observed percentile matching a threshold is circumstantial evidence unless a record links the decision to that measurement. Scientific suitability needs evidence about the study question, assumptions, and data; a successful run alone is not enough.

For correction or defensive behavior, add the cross-cutting [incident guide](sources/incident-postmortem.md) to the sources that carry relevant records.
