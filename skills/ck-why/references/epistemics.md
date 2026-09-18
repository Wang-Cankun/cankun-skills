# Epistemics

Historical evidence is fragmentary and sometimes contradictory. Code establishes behavior; motivation is recorded in comments, commits, reviews, method notes, decisions, and conversations. Those records can be incomplete, biased, or wrong. Do not retrofit a clean rationale onto behavior that happens to make sense today.

## Confidence tiers

Use these distinctions to reason about the claims that carry the answer. Explicit labels are useful when several confidence levels coexist; they are not required on every sentence.

### Direct

A source explicitly states a rationale. Examples include a review explaining the bug being fixed, a decision record describing rejected alternatives, or an analysis plan explaining a method selection.

State what the source supports and cite it. “The analysis plan says this filter excludes samples below the assay's detection threshold” reports documented intent. It does not by itself establish that the filter worked or that the justification remains valid.

### Supported

Independent pieces of indirect evidence converge. No single source states the complete reason, but the combined record favors it over alternatives.

Use phrasing such as “The evidence points toward X” and identify what each source contributes. A commit, a review repeating that commit, and a generated summary of the review are not three independent sources.

### Inferred

A reasonable interpretation of the available context that remains weakly supported or lacks an explicit statement of intent.

Show the reasoning step: “Given A and B, C seems likely.” Terms such as “appears,” “suggests,” and “is consistent with” distinguish interpretation from the record. A familiar pattern or a default parameter is a clue, not proof of motivation.

### Speculative

A plausible hypothesis with thin evidence or equally plausible alternatives.

Say so directly: “One possibility is X, but we found no direct support.” Explain what evidence would distinguish it from alternatives. Do not force a winner to make the answer feel complete.

### Unknown

The available investigation cannot establish the answer.

Name the unanswered question and the meaningful search or access limit: “The repository history and linked issue explain the filter's purpose, but neither explains why this exact cutoff was selected.” An unavailable record is different from a searched record with no relevant result.

## Match language to evidence

“The team decided,” “was designed to,” and “the reason was” claim intent. Use them when the cited record supports that intent. “Fixed” or “validated” additionally claims an outcome; a statement that a change intended to fix something is insufficient evidence that it did.

“Likely,” “suggests,” “one reading is,” and “may have been” mark interpretation. Preserve these qualifications when another skill turns the findings into an explanation. They are findings, not filler to edit away.

Keep citations close to the consequential claims they support. A source supporting the present mechanics does not automatically support a historical causal statement in the same paragraph.

## Avoid rationalization and agreement bias

The user's suggested explanation is a candidate to investigate, not a conclusion to confirm. Check what would be expected if it were wrong as well as what supports it.

Do not assume an author chose correctly and work backward to justify them. A repeated pattern may be copied, a threshold may be inherited, and a rationale may no longer apply. Absence of a recorded concern does not prove nobody considered it.

For analytical methods, separate three questions: why it was chosen, what assumptions it requires, and whether those assumptions hold for the current data. A paper describing a method can answer the second without answering the first or third.

## Conflicting and missing records

Surface sources that disagree. A requirement can motivate the work while a review describes it as cleanup; both might be accurate. A later explanation may reinterpret an earlier choice. Investigate the differing scope or version when possible; otherwise preserve the conflict.

When evidence is missing, identify what further source or check could resolve the uncertainty. Avoid manufacturing a gap when a narrow question is fully answered, and avoid a complete-looking narrative when important evidence is inaccessible.

## Calibration before delivery

Check the substantive conclusions:

- Does the cited source support the rationale being claimed, or only the mechanics?
- Does the language preserve the distinction between documented intent, interpretation, and verified effect?
- Were contradictions, alternative readings, or limits discarded for a tidier story?
- Does a null result cover the relevant version and source, or was that material never available?

Revise claims whose phrasing is stronger than their evidence. The reader should know what is established, what remains an interpretation, and what could change the answer.
