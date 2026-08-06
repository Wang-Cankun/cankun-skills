# Report structure

The report answers one question: what would someone who missed the meeting need in order to act? Not what was said in order, but what it means and what to do.

## Skeleton

Adapt section names to the subject; keep the order and keep the first and last sections exactly.

| § | Section | Holds |
|---|---|---|
| head | Title block | Subject, session date and duration, host, format, the documents or topics covered, participants as introduced, one line stating the source is a recording and machine transcription |
| 1 | **Bottom Line** | Three to five paragraphs. The single hardest constraint, the live ambiguity, the thing that carries schedule risk, and any statement that contradicts a published document. A reader who stops here has the decisions. |
| 2 | Parameters | Table. Every number stated: budgets, durations, counts, deadlines, eligibility. One column per option when the meeting compared two things. |
| 3–n | Topic sections | One per substantive area. Bullets for enumerated requirements, tables when two things are compared on the same axes, prose when the point is an argument. |
| n+1 | Pre-submitted Q&A | Two-column table, question compressed to its operative clause, answer stating what was decided. |
| n+2 | Live Q&A | Same shape. Separate table — questions asked live carry different weight from curated ones. |
| n+3 | **Action Items** | Numbered. Each is an action with its trigger and its reason, not a topic. "Confirm X with Y before Z, because the recorded answer does not close the loop" — not "Budget". |
| n+4 | **Assessment** | Bolded lead clause per paragraph, then the evidence chain. This is judgment: what breaks, what it costs, what the asymmetry is. Not summary. |
| n+5 | **Sourcing and Caveats** | Mandatory. See below. |

## Sourcing and Caveats

The section that makes the rest usable. It names, as bullets with a bolded lead:

- **Coverage.** Whether any block was dropped and recovered, which time ranges, and what the recovered content turned out to contain. If a recovered block held something material, say so — that is the reader's evidence that the gap mattered.
- **Speaker attribution.** That labels are chunk-local and unreconciled, that statements are attributed by role, and which names were spoken on the recording versus inferred. Flag every name spelling as unverified against the audio.
- **Transcription distortion.** The acronyms and proper nouns the model mangled, with the normalisation applied. Readers who search the transcript for a term need to know it appears three other ways.
- **Provisional answers.** Anything a speaker marked as to-be-confirmed, deferred to a follow-up, or answered on instinct. These read like decisions in a table and are not.
- **Internal inconsistency.** Where the recording contradicted itself, what the two versions were, and which one the report used.
- **Authority.** That this records what was said, not what any governing document says.

## Fidelity rules

**Quote the decisive statements verbatim, in italics.** A criterion described as *"non-negotiable"* is evidence; "the criterion is strict" is a claim. Paraphrase everything else — a report that quotes constantly is a transcript with headings.

**Flag inconsistency, never resolve it silently.** When a speaker gives two different figures within a minute, print both, say which one other evidence corroborates, and tell the reader to verify. Picking one and moving on hides the only signal that the number is unreliable.

**Every number carries its unit and basis.** Direct versus total cost, per year versus per project, cap versus expectation. Most recorded budget confusion is a unit collision, and the report is where it gets caught.

**Attribute by role.** "Program staff", "an attendee", "the moderator". Names appear only when a speaker states their own, and then flagged as unverified.

**Mark what was not answered.** Meetings run out of time. A question raised and dropped is information — it tells the reader what to chase.

**Assessment states asymmetries.** The useful judgment is rarely "this is hard". It is "this is free and most people skip it", or "this is stated once, in passing, and silently disqualifies you", or "this looks like latitude and is actually risk transfer".

## Writing

Direct statements. Conclusions before support. No metaphor, no em dash, no "not X but Y", no three-item lists as a reflex, no repeated sentence shapes. Add a space between CJK and Latin text when the report is in Chinese.

Prose sections carry the argument; tables carry the enumerable. A section that is neither an argument nor an enumeration usually should not exist.

## Rendering

Write the report as Markdown, then:

```bash
scripts/render.py <report>.md [--out <stem>]
```

Pipe tables, `**bold**`, `*italic*`, `#`/`##` headings, and ordered and unordered lists all survive to DOCX. Nested tables, footnotes, and raw HTML do not — keep the Markdown plain.
