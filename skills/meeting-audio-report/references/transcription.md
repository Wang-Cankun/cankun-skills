# Transcription mechanics

## The coverage manifest

`transcribe.py` writes three files beside the transcript:

| File | Holds |
|---|---|
| `<stem>-transcript.md` | the transcript the report is written from |
| `<stem>-coverage.json` | one row per block: `index`, `start`, `end`, `label`, `status`, `chars` |
| `<stem>-blocks.json` | the same rows plus each block's text, so `--retry-missing` can splice without re-running the blocks that succeeded |

`status` is `ok` or the error string that killed the block. A failed block is written into the transcript as a visible `> **MISSING — <error>.**` callout carrying its time range, so a gap is impossible to read past.

The script exits non-zero when any block failed. That exit code is the coverage gate.

## Recovery

```bash
scripts/transcribe.py <audio> --retry-missing [--out-dir DIR]
```

Re-runs only the failed blocks. Each recovered block starts `--overlap` seconds early so the model has lead-in context, then gets stamped:

```
_[recovered — re-transcribed from source audio with overlap into neighbouring blocks; a sentence may repeat at the boundary]_
```

Boundary repetition is the price of that context. Leave it; the marker explains it, and editing it out invites the removal of a sentence that only appears once.

Recovery needs `<stem>-blocks.json`. It is written on every run, including the failing one.

## Why blocks fail

Every observed failure has been transport, not audio: gateway 5xx, TLS resets, rate limits, empty completions. The script already retries three times with backoff inside a block, so a block that reaches the manifest as failed has failed four times. Recovery still usually succeeds, because the failures are transient and uncorrelated.

A block that fails repeatedly is worth listening to before assuming the model is at fault.

## Speaker labels

`[Speaker N]` numbering is **local to each block**. The model sees one 190-second segment and numbers speakers in order of first appearance within it. `[Speaker 1]` in block 3 and `[Speaker 1]` in block 9 are not necessarily the same person.

This skill does not reconcile them, and does not map them to real names. Both are LLM guesses over partial evidence, and both have produced confident, wrong attributions — including substituting an unrelated person's name over a correctly transcribed one. A report that attributes by role ("program staff", "an attendee") is accurate; one that attributes by name on the strength of a guess is not.

Names reach the report only through **fidelity**: a speaker states their own name on the recording, and it is quoted as heard, with the spelling flagged as unverified in Sourcing and Caveats.

## Cost and speed

`google/gemini-3.1-flash-lite-preview` runs about $0.0003 per audio-minute — roughly $0.02 for an hour-long meeting. Five parallel workers transcribe an hour in two to three minutes.

`--model` accepts any OpenRouter model that takes `input_audio`. Larger models cost more and are rarely more accurate on clear conference audio; they help on heavy accents, crosstalk, and poor microphones.

## Tuning

| Flag | Default | Raise it when |
|---|---|---|
| `--block-len` | 180 | Long uninterrupted monologue; fewer boundaries means fewer repeated sentences |
| `--overlap` | 10 | Speakers talk over each other at boundaries |
| `--workers` | 5 | Never above 8 — rate limiting starts costing more than the parallelism returns |
| `--timeout` | 180 | Blocks time out on a slow link |

Long blocks trade against the model's audio context window. Above roughly 300 seconds, output starts truncating silently, which shows up as a short `chars` count rather than an error.
