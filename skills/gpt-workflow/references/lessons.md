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
- **Accept the failure path too.** A harness accepted on a clean faux run deleted all its
  evidence the first time a live run timed out. When accepting a script or harness, run one
  failure and look at what it leaves behind.
- **`/code-review` after the workflow still finds bugs**, mostly in failure and abort paths
  (an exception outside `try`, a commit that blocks a result's receipt, a hook restored
  unconditionally).
- **Prompts set the size.** Ponytail cuts what nobody asked for, never what the card or the fix
  prompt requires; "a test for each fix" and long must-fix lists grew one diff by half.
- **Measurement code fails silently**: a wrong count gives a wrong number, not an error.
- **Before building a runner or harness, look for one in the repository.**
- **Records**: a Herdr-pane worker reports no cost, and files in a session scratchpad have been
  deleted mid-session; keep worker output in the worktree's `.work/`. Text for `gh` goes
  through `--body-file`; an inline `--body` with backticks runs the commands.
