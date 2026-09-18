# Code and workflow archaeology

Use repository history and nearby records to locate when behavior appeared, what changed with it, and where the reason was documented. Source history can be incomplete; it is not automatically the authoritative account of intent.

## Search patterns

For a Git repository, adapt these commands to observed paths and symbols:

```bash
# Trace a file through renames.
git log --follow --oneline -- <file>

# Find introduction or removal of a specific string or pattern.
git log -S '<exact-string>' -- <file>
git log -G '<pattern>' -- <file>

# Find last-touch commits, then inspect their context.
git blame -L <start>,<end> -- <file>
git show <commit>

# Read changes between relevant versions.
git log <old>..<new> -p -- <file>
```

Follow substantive commits to review discussions and linked issues through the repository's hosting CLI or connector. A GitHub repository might use `gh pr view`; a GitLab repository may use `glab mr view`. Inspect the actual remote and available command interface before choosing. No hosting connection means a gap in review evidence, not proof that no discussion occurred.

Search nearby comments, tests, design records, method notes, notebooks, changelogs, run manifests, and configuration history. Inspect other files changed in the same commit where they explain the target. For a non-Git project, use the available versioned artifacts and records without inventing a commit history.

## Evidence and pitfalls

- **Last touch is not origin.** Formatting or refactoring commits can hide an older decision; trace the relevant introduction.
- **Squashed history:** the review body and discussion may preserve rationale missing from a single squash commit.
- **Misleading summaries:** a “small refactor” can change behavior. Read the diff.
- **Copied patterns:** investigate the original pattern if the current change merely repeats it; do not assume copying carried the original rationale.
- **Tests:** an added regression test identifies a defended case, but its existence alone does not establish the author's full motivation.
- **Workflow records:** a configuration default, notebook output, and recorded run may refer to different versions. Resolve which one the question concerns.

Return the relevant location, what it says or shows, and whether it directly addresses the rationale or only supports an inference. Prefer a short exact quotation when wording matters; avoid reproducing whole discussions.
