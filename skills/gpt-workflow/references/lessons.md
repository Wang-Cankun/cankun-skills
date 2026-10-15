# Lessons from earlier runs

Things that went wrong in real GPT workflow runs, each with what worked instead.

- **The card is the spec.** The worst bugs began as one unchecked sentence in Claude's task
  card: an invented data shape, a wrong library behaviour, "remove the temp dir unless --keep".
  GPT built them faithfully, and every review that read the card agreed. Cards that cite where
  each claim was checked, and reviewers who never see the card, caught them.
- **Reviews drift both ways.** Left alone, a review hunts worst cases (pathological nesting,
  exotic environments) and adds hardening nobody needs. Told to keep only realistic inputs, a
  review filed real failure paths as rare notes, and no fix round saw them. Point the review at
  what the change must survive in real use, including its failure and abort paths.
- **Read the review's notes between rounds.** In a replay with a known answer key, the two
  failure-path bugs `/code-review` later fixed sat in a review's notes the whole time, and a
  memory leak noted in one round became a must-fix the next. Notes reach no fix round unless
  the main loop promotes them.
- **Accept the failure path too.** A harness accepted on a clean faux run deleted all its
  evidence the first time a live run timed out. When accepting a script or harness, run one
  failure and look at what it leaves behind.
- **`/code-review` after the workflow still finds bugs**, mostly in failure and abort paths
  (an exception outside `try`, a commit that blocks a result's receipt, a hook restored
  unconditionally).
- **GPT over-builds in a recognisable shape**: restrictions, enums, config and "governance"
  nobody asked for; `try`/`except` with fallback defaults and `getattr`/`isinstance` checks on
  data it produced itself; the old path kept beside the new one; tests that mirror the
  implementation; new files no caller uses. Ponytail cuts most of it; the acceptance still looks
  for it, and the fix is deletion.
- **Its own tests can encode the drift.** A context-assembly change passed about 800 tests
  while breaking the project's stable prompt-cache prefix, because GPT wrote the contract and
  the tests asserted the new behaviour. Accept against the project's invariants and design
  records, not against the diff's own tests.
- **Look before trusting the checks.** A slice that passed 800 tests was unusable at first
  sight of its screen. Before reading test results, look at one realistic result as its user
  would see it. Process grows into its own goal (checksums, smoke test plus dry run plus matrix
  around a small reversible change); each check should name the real failure it prevents.
- **Prompts set the size.** Ponytail cuts what nobody asked for, never what the card or the fix
  prompt requires; "a test for each fix" and long must-fix lists grew one diff by half.
- **Measurement code fails silently**: a wrong count gives a wrong number, not an error.
- **Before building a runner or harness, look for one in the repository.**
- **A tool missing from the preset is invisible to the job.** An audit sent with a preset that
  had no shell could not run `sqlite3` or `shasum`: five of six jobs stopped blocked and wrote
  nothing, and the sixth left every hash "unverified". Give any job that must run a command a
  preset with bash (`write` or `full`).
- **Records**: a Herdr-pane worker reports no cost, and files in a session scratchpad have been
  deleted mid-session; keep worker output in the worktree's `.work/`. Text for `gh` goes
  through `--body-file`; an inline `--body` with backticks runs the commands.
