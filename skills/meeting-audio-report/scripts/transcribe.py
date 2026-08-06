#!/usr/bin/env python3
"""
Transcribe a meeting recording via OpenRouter, with a machine-checkable coverage manifest.

Every block of audio is accounted for. A block that fails to transcribe is written to the
manifest with its error and its time range, never dropped silently. Re-run with
--retry-missing to recover only those blocks.

No glossary, no name hints, no speaker-name mapping: the transcript carries the speaker
labels the model emitted and nothing else.
"""

import argparse
import base64
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-3.1-flash-lite-preview"
SECRETS_PATH = Path.home() / ".config" / "secrets" / "api-keys.env"

AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac", ".opus", ".aiff", ".wma"}
VIDEO_EXT = {".mov", ".mp4", ".avi", ".mkv", ".webm", ".flv"}

PROMPT = """Transcribe this audio segment verbatim.

1. Write exactly what is said. Do not summarise, paraphrase, correct grammar, or add commentary.
2. Keep the speaker's original language. Do not translate.
3. Mark speaker changes with [Speaker 1], [Speaker 2], ... in order of first appearance in THIS segment.
4. Transcribe proper nouns and acronyms as you hear them. If a name is unclear, write your best phonetic guess.
5. Where the audio is silent, inaudible, or noise, skip it.

Return JSON: {"transcript": "..."}"""


# --------------------------------------------------------------------------- key


def get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    if SECRETS_PATH.exists():
        for line in SECRETS_PATH.read_text().splitlines():
            m = re.match(r"^\s*(?:export\s+)?OPENROUTER_API_KEY\s*=\s*(.+?)\s*$", line)
            if m:
                return m.group(1).strip().strip("'\"")
    sys.exit(
        "OPENROUTER_API_KEY not found.\n"
        "  export OPENROUTER_API_KEY=sk-or-...\n"
        f"  or add it to {SECRETS_PATH}"
    )


# --------------------------------------------------------------------------- audio


def to_wav(src: Path, workdir: Path) -> Path:
    """Normalise any input to 16 kHz mono PCM WAV."""
    if src.suffix.lower() == ".wav":
        with wave.open(str(src), "rb") as w:
            if w.getnchannels() == 1 and w.getframerate() == 16000:
                return src
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found. Install it: brew install ffmpeg")
    out = workdir / f"{src.stem}.16k.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-ac", "1", "-ar", "16000", str(out)],
        check=True,
    )
    return out


def slice_wav(wav_path: Path, start: float, end: float, dest: Path) -> Path:
    """Cut [start, end) out of a WAV without re-encoding."""
    with wave.open(str(wav_path), "rb") as w:
        rate = w.getframerate()
        w.setpos(int(start * rate))
        data = w.readframes(int((end - start) * rate))
        with wave.open(str(dest), "wb") as out:
            out.setnchannels(w.getnchannels())
            out.setsampwidth(w.getsampwidth())
            out.setframerate(rate)
            out.writeframes(data)
    return dest


def wav_duration(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as w:
        return w.getnframes() / w.getframerate()


def plan_blocks(duration: float, block_len: int, overlap: int) -> list[dict]:
    """Fixed grid of blocks. Block i covers [i*block_len, i*block_len + block_len + overlap)."""
    blocks, start, idx = [], 0.0, 0
    while start < duration:
        blocks.append({
            "index": idx,
            "start": round(start, 3),
            "end": round(min(start + block_len + overlap, duration), 3),
            "label": fmt_time(start),
        })
        start += block_len
        idx += 1
    return blocks


def fmt_time(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


# --------------------------------------------------------------------------- model


def extract_transcript(content: str) -> str:
    content = content.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", content, re.S)
    if fence:
        content = fence.group(1).strip()
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict) and isinstance(parsed.get("transcript"), str):
            return parsed["transcript"].strip()
    except (json.JSONDecodeError, TypeError):
        pass
    return content


def transcribe_block(wav_path: Path, block: dict, workdir: Path, model: str,
                     api_key: str, timeout: int, retries: int) -> dict:
    """Transcribe one block. Returns the block dict with status/text filled in."""
    out = dict(block)
    seg = workdir / f"seg_{block['index']:03d}.wav"
    try:
        slice_wav(wav_path, block["start"], block["end"], seg)
        data = base64.b64encode(seg.read_bytes()).decode()
    except Exception as exc:  # noqa: BLE001 - report, do not crash the run
        out.update(status=f"slice failed: {exc}", text="", chars=0)
        return out

    payload = {
        "model": model,
        "messages": [
            {"role": "system",
             "content": "You are a transcription service. Output only the requested JSON."},
            {"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "input_audio", "input_audio": {"data": data, "format": "wav"}},
            ]},
        ],
        "max_tokens": 8000,
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "transcription",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {"transcript": {"type": "string"}},
                    "required": ["transcript"],
                    "additionalProperties": False,
                },
            },
        },
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    last = "unknown error"
    for attempt in range(retries):
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
        except requests.RequestException as exc:
            last = f"request failed: {exc}"
            time.sleep(2 * (attempt + 1))
            continue
        if resp.status_code == 200:
            body = resp.json()
            choices = body.get("choices") or []
            if not choices:
                last = f"no choices in response: {json.dumps(body)[:200]}"
                time.sleep(2 * (attempt + 1))
                continue
            text = extract_transcript(choices[0]["message"].get("content") or "")
            if not text:
                last = "empty transcript returned"
                time.sleep(2 * (attempt + 1))
                continue
            seg.unlink(missing_ok=True)
            out.update(status="ok", text=text, chars=len(text))
            return out
        if resp.status_code == 429:
            time.sleep(10 * (attempt + 1))
            last = "rate limited"
            continue
        last = f"HTTP {resp.status_code}: {resp.text[:200]}"
        time.sleep(2 * (attempt + 1))

    seg.unlink(missing_ok=True)
    out.update(status=last, text="", chars=0)
    return out


def run_blocks(blocks: list[dict], wav_path: Path, workdir: Path, args, api_key: str,
               note: str = "") -> list[dict]:
    results: list[dict] = []
    total = len(blocks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(transcribe_block, wav_path, b, workdir, args.model,
                        api_key, args.timeout, args.retries): b
            for b in blocks
        }
        for done, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            res = fut.result()
            results.append(res)
            state = "ok" if res["status"] == "ok" else f"FAILED — {res['status']}"
            print(f"  [{done}/{total}]{note} block {res['index']:>3} @ {res['label']}: {state}",
                  flush=True)
    return sorted(results, key=lambda r: r["index"])


# --------------------------------------------------------------------------- output


def write_transcript(path: Path, source: Path, duration: float, blocks: list[dict],
                     model: str) -> None:
    lines = [
        "---",
        f'source: "{source.name}"',
        f'duration: "{fmt_time(duration)}"',
        f'transcription_model: "{model}"',
        "speaker_labels: chunk-local",
        "type: meeting-transcript",
        "---",
        "",
        f"# {source.stem}",
        "",
        f"**Source:** `{source.name}`  ",
        f"**Duration:** {fmt_time(duration)}  ",
        f"**Model:** {model}",
        "",
        "> Speaker labels are local to each block. `[Speaker 1]` in one block and `[Speaker 1]`",
        "> in another are not necessarily the same person. No names have been substituted.",
        "",
        "---",
        "",
    ]
    for b in blocks:
        lines.append(f"### [{b['label']}]")
        lines.append("")
        if b["status"] == "ok":
            if b.get("recovered"):
                lines.append(
                    "_[recovered — re-transcribed from source audio with overlap into "
                    "neighbouring blocks; a sentence may repeat at the boundary]_"
                )
                lines.append("")
            lines.append(b["text"])
        else:
            lines.append(
                f"> **MISSING — {b['status']}.** Covers {fmt_time(b['start'])}–"
                f"{fmt_time(b['end'])}. Recover with `--retry-missing`."
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(path: Path, source: Path, duration: float, model: str,
                   blocks: list[dict]) -> None:
    path.write_text(json.dumps({
        "source": str(source),
        "duration_seconds": round(duration, 3),
        "model": model,
        "blocks_total": len(blocks),
        "blocks_ok": sum(1 for b in blocks if b["status"] == "ok"),
        "blocks": [
            {k: b[k] for k in ("index", "start", "end", "label", "status", "chars")
             if k in b} | ({"recovered": True} if b.get("recovered") else {})
            for b in blocks
        ],
    }, indent=2, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", help="audio or video file")
    ap.add_argument("--out-dir", "-d", default=None,
                    help="output directory (default: alongside the input file)")
    ap.add_argument("--model", "-m", default=DEFAULT_MODEL)
    ap.add_argument("--block-len", "-b", type=int, default=180, help="block length, seconds")
    ap.add_argument("--overlap", "-o", type=int, default=10, help="overlap, seconds")
    ap.add_argument("--workers", "-w", type=int, default=5)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--retry-missing", action="store_true",
                    help="re-transcribe only the blocks the manifest marks failed")
    args = ap.parse_args()

    src = Path(args.audio).expanduser().resolve()
    if not src.exists():
        sys.exit(f"not found: {src}")
    if src.suffix.lower() not in AUDIO_EXT | VIDEO_EXT:
        sys.exit(f"unsupported format: {src.suffix}")

    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = out_dir / f"{src.stem}-transcript.md"
    manifest_path = out_dir / f"{src.stem}-coverage.json"

    api_key = get_api_key()

    with tempfile.TemporaryDirectory(prefix="mar_") as tmp:
        workdir = Path(tmp)
        print(f"Preparing audio: {src.name}", flush=True)
        wav = to_wav(src, workdir)
        duration = wav_duration(wav)

        if args.retry_missing:
            if not manifest_path.exists():
                sys.exit(f"no manifest at {manifest_path} — run without --retry-missing first")
            prior = json.loads(manifest_path.read_text())
            by_index = {b["index"]: b for b in prior["blocks"]}
            missing = [b for b in prior["blocks"] if b["status"] != "ok"]
            if not missing:
                print("Coverage already whole — nothing to recover.")
                return 0
            print(f"Recovering {len(missing)} block(s), {fmt_time(duration)} source", flush=True)
            # widen each missing block by the overlap on the leading edge for context
            widened = [
                dict(b, start=max(0.0, b["start"] - args.overlap)) for b in missing
            ]
            recovered = run_blocks(widened, wav, workdir, args, api_key, note=" recover")
            for r in recovered:
                r["start"] = by_index[r["index"]]["start"]
                if r["status"] == "ok":
                    r["recovered"] = True
                by_index[r["index"]] = r
            # blocks that were already ok have no text in the manifest; re-read them
            # from the existing transcript is unreliable, so require a full text cache
            cache_path = out_dir / f"{src.stem}-blocks.json"
            if not cache_path.exists():
                sys.exit(f"block text cache missing: {cache_path}")
            cached = {b["index"]: b for b in json.loads(cache_path.read_text())}
            for i, b in by_index.items():
                if b["status"] == "ok" and "text" not in b:
                    b["text"] = cached.get(i, {}).get("text", "")
            blocks = [by_index[i] for i in sorted(by_index)]
        else:
            planned = plan_blocks(duration, args.block_len, args.overlap)
            print(f"{fmt_time(duration)} audio → {len(planned)} blocks "
                  f"({args.block_len}s + {args.overlap}s overlap), model {args.model}",
                  flush=True)
            blocks = run_blocks(planned, wav, workdir, args, api_key)

        (out_dir / f"{src.stem}-blocks.json").write_text(
            json.dumps(blocks, indent=2, ensure_ascii=False), encoding="utf-8")

    write_transcript(transcript_path, src, duration, blocks, args.model)
    write_manifest(manifest_path, src, duration, args.model, blocks)

    ok = sum(1 for b in blocks if b["status"] == "ok")
    print(f"\nCoverage: {ok}/{len(blocks)} blocks")
    print(f"  transcript: {transcript_path}")
    print(f"  manifest:   {manifest_path}")

    if ok < len(blocks):
        for b in blocks:
            if b["status"] != "ok":
                print(f"  MISSING block {b['index']} @ {b['label']} — {b['status']}")
        print(f"\nCoverage is not whole. Recover with:\n"
              f"  {sys.argv[0]} \"{src}\" --retry-missing"
              + (f" --out-dir \"{out_dir}\"" if args.out_dir else ""))
        return 1

    print("Coverage is whole.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
