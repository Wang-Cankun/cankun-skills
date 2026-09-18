# Summarize counts

The user supplies a gene-by-sample count table and receives one total per sample. Invalid counts are rejected before a successful output is published.

## Sub-features

- `summary-totals` returns exact totals for each sample in a valid table.
- `summary-negative` rejects a negative count with an actionable error and nonzero exit.

## How to get to it (user POV)

- Run `count-summary summarize --input counts.csv --output totals.csv` from the project environment.

## Driving it with the CLI

Preconditions:

- The verification skill's doctor passes for the declared environment.
- `counts.csv` and `negative-counts.csv` contain the fixtures defined in the index.
- `totals.csv` and `invalid-totals.csv` do not exist in this recipe's scratch workspace.

- **Compute totals.** Run `count-summary summarize --input counts.csv --output totals.csv`. Capture stdout, stderr, and exit code. Require exit `0`, then parse the output as CSV. Require exactly two rows, unique sample identifiers `sample-a` and `sample-b`, and numeric totals `4` and `2` associated with the correct identifiers. The expected schema is `sample,total`; compare by sample identity rather than incidental row order.
- **Reject invalid input.** Run `count-summary summarize --input negative-counts.csv --output invalid-totals.csv`. Require a nonzero exit and an error identifying the negative count. Require that no successful `invalid-totals.csv` was published, as specified by the input contract.
- **Proof.** Save both fixture files, commands, streams, exit codes, the valid output table, and machine-readable assertion results under the evidence location named by the skill. A generated recipe must use the project's real parser or a documented helper that fails when an assertion is false.
- **Cleanup.** Remove only the recipe's scratch workspace. Confirm that the retained evidence contains the expected output values and both assertion results.

## Gotchas

- Stale outputs can make a failed run look successful; each case begins with a fresh output path.
- Numeric columns need numeric comparison; quoted text or row order should not decide equality.
- Expected totals come from the explicit fixture arithmetic, not from a previous output of the same implementation.
- This case checks table handling and addition. It provides no evidence for an untested scientific inference or a full-scale performance claim.
