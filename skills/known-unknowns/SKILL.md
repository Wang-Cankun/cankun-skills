---
name: known-unknowns
metadata:
  group: general
  summary: >-
    Guided deliberations on the Rumsfeld matrix: helps articulate tacit
    judgments, surfaces unrecognized patterns, tours unseen options, and ends
    with a paste-ready brief.
description: Orient a multi-turn “help me think this through” deliberation with a Rumsfeld matrix. Use when the user owns an open decision or judgment and wants a thinking partner — articulating a tacit judgment, surfacing an unrecognized assumption or pattern, or touring options around the choice they are weighing. A question seeking a direct answer (factual lookup, how-to, debugging) gets the answer, not this skill.
---

# Orientation through the Rumsfeld Matrix

Conduct the deliberation in the user's language.

Use the matrix to orient a multi-turn deliberation. The topic starts mostly dark; each turn enables one **aspect-seeing** by making one relevant part more nameable, visible, or testable.

|                   | they know it                        | they don't know it                          |
| ----------------- | ----------------------------------- | ------------------------------------------- |
| **aware of it**   | known knowns — stated and confirmed | known unknowns — named gaps                 |
| **unaware of it** | unknown knowns — operative but unrecognized | unknown unknowns — options they'd never ask about |

The matrix tracks awareness; tacitness tracks articulability. Classify each entry by awareness, and treat difficulty articulating an already-recognized judgment as a separate named gap. Split descriptions whose parts belong in different cells.

Use the marks as lifecycle shorthand: `✓` settled · `?` named question · `!` recognition candidate · `~` unexplored frontier. The map always renders as this 2×2 table — every entry sits in its cell with its mark inline; a flat mark list is not a map.

Choose the move by cell:

- **Known knowns → confirm and compress.** Restate what is settled, preserve only what matters downstream, and reopen it only when later evidence conflicts.
- **Known unknowns → investigate.** Name the gap and what would resolve it. When the gap is articulation, **externalize**: propose `!` candidate representations that another person or model could act on, then test them against the user's already-recognized judgment. Otherwise use evidence, reasoning, or experiment. Run whatever probe you can run yourself before asking the user.
- **Unknown knowns → surface for recognition.** Reflect patterns, assumptions, commitments, or practiced judgment already present in the user's words, behavior, or artifacts. Present grounded hypotheses as `!` candidates so the user can recognize, reject, or refine them. Recognition beats recall.
- **Unknown unknowns → give a tour.** Introduce an unmentioned region of the option space: what exists, when it fits, what it costs, and your own read.

Keep the move open-ended: the four cell moves are defaults, not a closed set. A turn may instead run a concrete probe such as a premortem or inversion, draw a distinction, offer a counterexample, or change scale — whatever best advances the chosen entry.

## Opening

Draft the full map from the topic and your domain knowledge, tagging every inference as `!`. A wrong map draws corrections faster than a blank interview draws answers. Choose the darkest useful entry, contribute an aspect-seeing, then end with one question that both advances that entry and invites correction of the map.

The opening is done when the full map is visible, every inference is marked, one cell received substantive contribution, and exactly one question is on the table.

## Each turn

1. **Redraw the full map**, compact enough to stay a card: keep the four-cell table skeleton and one phrase per entry. Promote whatever the user just recognized, answered, or corrected.
2. **Enable one aspect-seeing.** Choose one cell and contribute before asking. Make one relevant aspect more nameable, visible, or testable using the move suited to the topic.
3. **Ask exactly one question.** When seeking recognition, carry 2–4 named candidates; otherwise ask the single question that most advances the selected cell.

The turn is done when the map reflects the last answer, the contribution changed what can be named, seen, or tested, and exactly one new question is on the table.

## Closing

When the user calls it, close without another dig. Otherwise close only when no active mapped entry warrants another turn. Audit the map first: each `?` is answered or deferred; each `!` is recognized, rejected, or deferred; and each `~` is explored into something more concrete or retained as residual darkness.

Before an agent-proposed close, run one **frame-break**: test one plausible missing aspect that could change the conclusion. Continue if it matters. Otherwise deliver the **brief**: the vocabulary the user recognized, the choices they settled, the gaps they deferred, and the residual darkness, phrased so they can paste it verbatim into a future prompt. The map is the receipt; the brief is the asset they leave with.
