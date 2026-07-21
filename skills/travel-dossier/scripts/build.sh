#!/bin/bash
# Travel Dossier 构建：HTML → PDF（headless Chrome）
# Usage:  ./build.sh <source.html> <output.pdf>
set -euo pipefail
SRC="${1:?usage: build.sh <src.html> <out.pdf>}"
OUT="${2:?usage: build.sh <src.html> <out.pdf>}"

CHROME=""
for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
  if [[ -x "$c" ]]; then CHROME="$c"; break; fi
done
[[ -z "$CHROME" ]] && { echo "error: no Chrome/Chromium found" >&2; exit 1; }

"$CHROME" --headless --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")" \
  "file://$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")" 2>/dev/null

echo "✓ built $OUT ($(du -h "$OUT" | cut -f1)) from $SRC"
# 构建后必做：pypdf 验证页数与 148.2×209.9mm；然后跑 check_overflow.py
