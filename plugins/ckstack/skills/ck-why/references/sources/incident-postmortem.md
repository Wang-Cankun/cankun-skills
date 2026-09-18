# Incident and corrective-change context

This is a cross-cutting investigation angle, not another mandatory source. Use it when a guard, retry, resource limit, quality-control filter, or corrective step plausibly originated in a failure.

Search relevant records for the target's symbols, error strings, affected data, and linked issues:

- In history, look for a failing case, revert, follow-up guard, or regression test.
- In issues and documents, look for root-cause discussion and action items tied to the change.
- In conversations, read the full decision thread and follow links to the primary records.
- In logs and failure tracking, match the affected version, execution path, conditions, and recorded symptom.
- In data or run reports, compare the relevant cohorts or runs while checking for other changed inputs and instrumentation.

Read a linked postmortem or failed-analysis report beyond its summary. An action item that identifies the target is stronger evidence than temporal coincidence. A symptom decreasing after a change is circumstantial support until alternatives such as another fix, a changed dataset, or lost telemetry are considered.

Distinguish the motivating failure, the intended correction, and evidence that the correction actually worked. These can have different confidence levels. Do not infer a failure merely because a defensive check exists.
