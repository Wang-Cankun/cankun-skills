---
name: meeting-audio-report
compatibility: Requires `ffmpeg`, `pandoc`, LibreOffice, Python 3.10+ with `requests` and `python-docx`, and an `OPENROUTER_API_KEY`.
metadata:
  group: general
  summary: >-
    Turns a meeting recording into a verbatim transcript plus an evidence-graded
    DOCX/PDF report, gated on block-level coverage so dropped audio surfaces
    instead of vanishing.
description: Transcribe a meeting recording and write a report from it. Use when the user has an audio or video file of a meeting, webinar, seminar, or Q&A session — .m4a/.mp3/.wav/.mp4/.mov — and wants a transcript, meeting notes, minutes, or a written report; also on 转录, 会议纪要, 会议记录, 会议报告, transcribe this, write up this meeting.
---

# Meeting audio report

A recording becomes two things: a **verbatim** transcript, and a report someone who missed the meeting can act on.

Two words govern the run.

**Coverage** — did every second of audio reach the transcript? Transcription drops blocks on transport errors, and the loss is silent. The one block lost is as likely as any other to hold the decisive sentence. Coverage is a gate, not a statistic.

**Fidelity** — does every name, number, and quote in the report trace to the audio? A transcription model guesses at proper nouns; a summarising model guesses at who said what. Both guesses arrive fluent and confident. The report carries what the recording supports and flags the rest.

## 1. Transcribe

```bash
scripts/transcribe.py <audio-or-video> [--out-dir DIR]
```

Writes `<stem>-transcript.md`, `<stem>-coverage.json`, and `<stem>-blocks.json` beside the input, or into `--out-dir`.

Done when the script has exited and the manifest exists.

## 2. Pass the coverage gate

The script exits non-zero when any block failed, and names each gap with its time range.

```bash
scripts/transcribe.py <audio> --retry-missing [--out-dir DIR]
```

Repeat until it exits zero. Failures are transport, not audio, so a second attempt usually lands.

Done when `blocks_ok` equals `blocks_total` in the manifest. Carry which blocks were recovered into step 5 — a recovered block that turned out to hold something material is itself a finding.

A gap that survives repeated recovery goes into the report as a stated gap, with its time range and what was being discussed either side of it. Never write around it silently.

`references/transcription.md` holds the manifest format, tuning flags, cost, and the speaker-label limits.

## 3. Read the whole transcript

Read it end to end before writing anything. An hour of meeting is 40 to 60 KB — read it in full, not in excerpts.

Done when you can state, without looking back: the subject, every number that was quoted, what was decided, what was deferred, and what a speaker said that contradicts a document.

## 4. Write the report

Author it as Markdown against `references/report-structure.md`, which carries the section skeleton and the fidelity rules.

Two things drive the report's value, and both live in the transcript rather than in a template:

- The **Assessment** section states asymmetries — what is free and commonly skipped, what is stated once in passing and silently disqualifying, what looks like latitude and is risk transfer.
- **Sourcing and Caveats** is mandatory. It carries coverage, speaker attribution limits, transcription distortion of acronyms and names, provisional answers, and internal inconsistencies.

Attribute by role. A name enters the report only when a speaker states their own on the recording, quoted as heard and flagged as unverified.

Done when every section of the skeleton is present and every number carries its unit and basis.

## 5. Render

```bash
scripts/render.py <report>.md [--out <stem>]
```

Markdown → pandoc → DOCX → LibreOffice → PDF, styled to match.

Done when the PDF exists and `pdfinfo` reports a non-zero page count.

## 6. Hand over

State: where the files are, the coverage result including any recovered or unrecoverable blocks, and the fidelity caveats a reader would otherwise take on trust.

Deliver the DOCX and PDF. The transcript stays alongside as the evidence the report was built from.
