# Behavioral trials and comparisons

## Design before running

State the behavior under investigation and observable success criteria before
reading candidate outputs. Use realistic requests and inputs, including a
boundary case when relevant. Literal expected values, independent references,
and user-visible outcomes make stronger checks than matching headings or the
skill's own wording. For subjective work, name the dimensions for human or
independent judgment; arbitrary percentages do not make them objective.

An independent trial asks whether the skill can handle a representative task.
A paired comparison asks whether a change improves it. For the latter, fix the
model, settings, task, inputs, tools, permissions, and resource limits as far as
the host permits; vary the skill. Test other models separately when portability
is the question. Randomness remains: repeat an unstable or close result before
making a stronger claim. A few cases are evidence about those cases.

For an existing skill use the saved old version; for a new skill a no-skill
baseline can show the value it adds. Both sides must receive the same ordinary
project context. Keep the new skill out of the baseline's loaded context and
filesystem view where possible. Record any isolation limitation; renaming a
folder does not remove inherited conversation context or installed skills.

## Execute independently

Create fresh, separate workspaces outside the source and distributable. Each
candidate sees a natural user request, necessary raw inputs, its own available
skill, and where to save the requested output. Keep comparative labels,
expected answers, grading criteria, and prior author reasoning with the
coordinator. Ordinary task terms such as "test" need not be censored.

Use a fresh-context subagent or supported isolated runner. Give each worker its
own writable state and the same side-effect limits. Parallel execution is
useful when resources are independent; bounded batches or sequential fresh
runs are valid. A tool or capacity limit changes the schedule, not the evidence
standard. Do not request private reasoning traces: inspect visible actions,
tool records, and artifacts.

The coordinator keeps the mapping from anonymous labels to variants. Candidate
brief, for example:

```text
Use the supplied project and available skill to complete this request:
<ordinary user request>
Inputs: <raw artifacts>
Work only in <isolated workspace>. Save <requested artifacts> in outputs/.
```

For a dialogue skill, use an actual interaction or a stated simulated-user
fixture. The simulator supplies consistent user facts and responses, without
feeding the desired conclusion to the candidate.

## Judge evidence

Check actual outputs and material side effects first. Then inspect whether the
agent read the necessary resources and followed the relevant path. Self-report
alone does not prove either. Distinguish a skill failure, evaluator/fixture
failure, missing prerequisite, and untested behavior.

For comparisons, give an independent judge the original request, anonymized
artifacts, and the same predeclared criteria for both sides. Hide author, model,
and version identity. Read the artifacts yourself before accepting a verdict.
Allow a tie, insufficient evidence, or both failing; selecting the less bad
output does not establish that it is ready to ship.

Keep assertion pass/fail evidence separate from qualitative judgment. Never
replace a missing measurement with zero, estimate tokens from character count,
or treat a format check as proof of useful behavior. Compare like denominators
and report missing runs explicitly. If quantitative aggregation is useful,
compute it from the recorded outcomes with a small script, rather than copying
scores from a model's summary.

## Records and optional review viewer

For a small trial, an output path and concise evidence notes suffice. For
multiple artifacts or user comparison, use the bundled Apache-licensed review
viewer. Collect outputs into a coordinator-owned directory after the candidates
finish, so its labels and grading are not visible during execution:

```text
review/
  case-1/
    A/
      eval_metadata.json
      outputs/
      grading.json          # optional
    B/
      eval_metadata.json
      outputs/
      grading.json
```

`eval_metadata.json` contains `eval_id` and the original `prompt`.
Optional `grading.json` uses:

```json
{
  "expectations": [
    {"text": "The requested consumer reads the output", "passed": true,
     "evidence": "commands.txt and outputs/result.json"}
  ],
  "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0}
}
```

Include only executed assertions in that summary. Put blocked and untested
cases in accompanying evidence notes; do not count them as passes. For an
entirely unexecuted run, omit grading and explain its status in the output.
Capture time and token counts only if the runner actually reports them.

Run from the skill directory, choosing the project's Python interpreter:

```sh
python eval-viewer/generate_review.py /absolute/path/to/review \
  --skill-name target-skill --static /absolute/path/to/review.html
```

The static file displays nested outputs and any grading, and exports
`feedback.json` without a server. Binary formats such as XLSX are downloadable
attachments. Feedback remains in the browser tab until exported; unvisited
outputs have `reviewed: false`, so empty feedback alone is not acceptance.
Read feedback when the user's judgment is needed or they provide it; producing
a viewer does not require another approval cycle. For large or sensitive files,
use selected local artifacts rather than embedding every input in the viewer.

## Iterate with a stopping condition

Fix demonstrated causes, rerun affected cases, and retain consequential passing
cases. Freeze criteria during a comparison; if the criteria were wrong, revise
them openly and reassess both sides. Use fresh cases to check generalization
after tuning. A set used to choose the best revision is development evidence,
not an untouched final test set.

Stop when the scoped behavior is supported, the subjective result is accepted,
or further progress needs new inputs or resources. Report the result and limit
of the chosen evidence level. Neither an independent trial nor a numeric score
establishes reliability for all future requests.
