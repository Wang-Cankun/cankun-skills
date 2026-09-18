# Count Summary verification map

Illustrative map for a fictional `count-summary` CLI. The command names and files below show the form of a recipe; discover actual project commands and acceptance criteria when generating a skill.

Count Summary sums gene counts for each sample. This map covers one small deterministic operation and its invalid-input behavior. It does not claim biological interpretation, scalability, normalization, or downstream statistical validity.

## Baseline preconditions

- Use the environment and public CLI identified by the project's verification skill.
- Run each recipe in a fresh workspace. Keep evidence in a separate directory named by the skill.
- Run the skill's read-only doctor checks before execution, confirming the CLI version and fixture inputs.
- Use this hand-checkable synthetic input, with genes in rows and samples in columns:

  ```csv
  gene,sample-a,sample-b
  gene-1,1,0
  gene-2,3,2
  gene-3,0,0
  ```

- Expected totals are `sample-a=4` and `sample-b=2`. Both samples have three input genes, including the all-zero row. These are exact integer expectations, so no numerical tolerance is needed.
- A second fixture replaces one count with `-1`. The documented input contract rejects negative counts.

## Driving conventions

- Exercise the public command with the same flags a project user would use.
- Reset output paths between cases so stale files cannot count as new results.
- Inspect parsed output values, sample identities, schema, and row count. An exit code and an existing file do not establish the result.
- Keep negative-case outputs separate from successful outputs.

## Proof and coverage reporting

- Capture the command, environment identity, input fixture, stdout, stderr, exit code, output table, and assertion result.
- Record the feature ID and case with each artifact. Retain the evidence after cleanup.
- Separate passed, failed, and unexecuted cases. Explain unavailable prerequisites.
- If real data requires reference resources, record the reference identity and parameters actually used. Synthetic evidence proves only the properties exercised by that fixture.

## Feature entry contract

Each feature file describes the user-visible behavior and uses four H2 sections: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. Each drive pairs an action with an observable assertion and evidence location.

## Features

- [Summarize counts](summarize-counts.md) covers exact per-sample totals and rejection of negative counts.
