#!/usr/bin/env bash
# confer — consult a peer AI model (claude / codex) with resumable threads.
# State: ~/.confer/threads.json (registry) + ~/.confer/threads/<name>.md (transcripts)
set -euo pipefail

CONFER_HOME="${CONFER_HOME:-$HOME/.confer}"
REG="$CONFER_HOME/threads.json"
TDIR="$CONFER_HOME/threads"
PROVIDERS=(claude codex)

PREAMBLE='[confer] You are consulted as an independent peer model by another AI agent. Give your own analysis in plain text. Do not modify files or run destructive commands. This thread may continue for multiple rounds.'

die()  { echo "confer: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "'$1' CLI not found (run: confer.sh doctor)"; }
now()  { date '+%Y-%m-%d %H:%M'; }
init_home() { mkdir -p "$TDIR"; [[ -f "$REG" ]] || echo '{}' >"$REG"; }

reg_field() { jq -r --arg t "$1" --arg f "$2" '.[$t][$f] // empty' "$REG"; }
reg_set() { # name provider session rounds
  local tmp; tmp=$(mktemp)
  jq --arg t "$1" --arg p "$2" --arg s "$3" --argjson r "$4" --arg ts "$(now)" \
     '.[$t] = {provider:$p, session:$s, rounds:$r, updated:$ts, created:(.[$t].created // $ts)}' \
     "$REG" >"$tmp" && mv "$tmp" "$REG"
}

transcript() { # name round direction(→|←) who text
  { printf '\n## R%s %s %s  (%s)\n\n%s\n' "$2" "$3" "$4" "$(now)" "$5"; } >>"$TDIR/$1.md"
}

# ---- provider adapters -----------------------------------------------------
# ask_<provider> <prompt> [session]  -> sets $REPLY and $SESSION
# (must run in the current shell, never in $(...): the assignments must survive)

ask_claude() {
  need claude; local out
  if [[ -n "${2:-}" ]]; then
    out=$(claude -p --resume "$2" --output-format json ${CONFER_CLAUDE_ARGS:-} -- "$1")
  else
    out=$(claude -p --output-format json ${CONFER_CLAUDE_ARGS:-} -- "$1")
  fi
  SESSION=$(jq -r '.session_id // empty' <<<"$out")
  REPLY=$(jq -r '.result // .error // "(empty reply)"' <<<"$out")
}

ask_codex() {
  need codex; local reply events; reply=$(mktemp); events=$(mktemp)
  if [[ -n "${2:-}" ]]; then
    # flag placement differs across codex versions; try subcommand-level, then exec-level
    codex exec resume "$2" --output-last-message "$reply" ${CONFER_CODEX_ARGS:-} -- "$1" >"$events" 2>&1 \
      || codex exec --output-last-message "$reply" resume "$2" ${CONFER_CODEX_ARGS:-} -- "$1" >"$events" 2>&1 \
      || { cat "$events" >&2; rm -f "$reply" "$events"; die "codex resume failed"; }
    SESSION="$2"
  else
    codex exec --json --sandbox read-only --output-last-message "$reply" ${CONFER_CODEX_ARGS:-} -- "$1" >"$events" 2>&1 \
      || { cat "$events" >&2; rm -f "$reply" "$events"; die "codex exec failed"; }
    SESSION=$(grep -oE '"(thread_id|session_id)"[[:space:]]*:[[:space:]]*"[^"]+"' "$events" \
              | head -1 | sed -E 's/.*"([^"]+)"$/\1/') || SESSION=""
  fi
  REPLY=$(cat "$reply"); rm -f "$reply" "$events"
}

run_round() { # name provider prompt session('' for round1) round
  local name="$1" provider="$2" prompt="$3" session="$4" round="$5"
  transcript "$name" "$round" "→" "$provider" "$prompt"
  SESSION=""; REPLY=""
  "ask_$provider" "$prompt" "$session"
  transcript "$name" "$round" "←" "$provider" "$REPLY"
  [[ -n "$SESSION" ]] || echo "confer: warning — no session id captured; thread '$name' is not resumable" >&2
  reg_set "$name" "$provider" "${SESSION:-}" "$round"
  printf '%s\n\n[confer] thread=%s provider=%s round=%s — continue: confer.sh reply %s "..."\n' \
    "$REPLY" "$name" "$provider" "$round" "$name"
}

read_prompt() { # remaining args; '-' reads stdin
  if [[ "${1:-}" == "-" ]]; then cat; else echo "$*"; fi
}

# ---- commands --------------------------------------------------------------

cmd_open() { # provider [-t name] prompt...
  local provider="${1:?usage: confer.sh open <provider> [-t name] <prompt|->}"; shift
  [[ " ${PROVIDERS[*]} " == *" $provider "* ]] || die "unknown provider '$provider' (have: ${PROVIDERS[*]})"
  local name=""
  if [[ "${1:-}" == "-t" ]]; then name="$2"; shift 2; fi
  [[ -n "$name" ]] || name="$provider-$(date +%m%d-%H%M%S)"
  init_home
  [[ -z "$(reg_field "$name" provider)" ]] || die "thread '$name' already exists (use: reply $name)"
  local prompt; prompt=$(read_prompt "$@")
  [[ -n "$prompt" ]] || die "empty prompt"
  run_round "$name" "$provider" "$PREAMBLE"$'\n\n'"$prompt" "" 1
}

cmd_reply() { # name prompt...
  local name="${1:?usage: confer.sh reply <thread> <prompt|->}"; shift
  init_home
  local provider session rounds
  provider=$(reg_field "$name" provider); [[ -n "$provider" ]] || die "no thread '$name' (see: confer.sh list)"
  session=$(reg_field "$name" session);   [[ -n "$session"  ]] || die "thread '$name' has no session id — not resumable"
  rounds=$(reg_field "$name" rounds)
  local prompt; prompt=$(read_prompt "$@")
  [[ -n "$prompt" ]] || die "empty prompt"
  run_round "$name" "$provider" "$prompt" "$session" $((rounds + 1))
}

cmd_all() { # prompt... — fan out one question to every provider
  local prompt; prompt=$(read_prompt "$@"); [[ -n "$prompt" ]] || die "empty prompt"
  local p
  for p in "${PROVIDERS[@]}"; do
    printf '════ %s ════\n' "$p"
    cmd_open "$p" "$prompt" || echo "confer: $p failed" >&2
  done
}

cmd_list() {
  init_home
  jq -r 'to_entries | sort_by(.value.updated) | reverse[]
         | "\(.key)\t\(.value.provider)\tr\(.value.rounds)\t\(.value.updated)"' "$REG" \
    | column -t -s $'\t'
}

cmd_show() { # name
  local f="$TDIR/${1:?usage: confer.sh show <thread>}.md"
  [[ -f "$f" ]] || die "no transcript for '$1'"
  cat "$f"
}

cmd_doctor() {
  local ok=0
  for c in jq claude codex; do
    if command -v "$c" >/dev/null 2>&1; then echo "ok   $c $("$c" --version 2>/dev/null | head -1)"
    else echo "MISS $c"; ok=1; fi
  done
  init_home && echo "ok   state $CONFER_HOME (threads: $(jq 'length' "$REG"))"
  if [[ "${1:-}" == "--live" ]]; then
    # run via "$0" subprocesses so a die() in one probe cannot kill the loop
    local p self="${BASH_SOURCE[0]}"
    for p in "${PROVIDERS[@]}"; do
      echo "── live: $p (open + resume) ──"
      "$self" open "$p" -t "doctor-$p-$$" 'Reply with the single word OK.' || { ok=1; continue; }
      "$self" reply "doctor-$p-$$" 'Reply with the single word AGAIN.' || ok=1
    done
    local tmp; tmp=$(mktemp)
    jq 'with_entries(select(.key | startswith("doctor-") | not))' "$REG" >"$tmp" && mv "$tmp" "$REG"
    rm -f "$TDIR"/doctor-*.md
    echo "── doctor threads cleaned ──"
  fi
  exit $ok
}

case "${1:-}" in
  open)    shift; cmd_open "$@" ;;
  ask)     shift; cmd_open "$@" ;;       # alias: one-shot is just a thread you may never resume
  reply)   shift; cmd_reply "$@" ;;
  all)     shift; cmd_all "$@" ;;
  list)    cmd_list ;;
  show)    shift; cmd_show "$@" ;;
  doctor)  shift || true; cmd_doctor "${1:-}" ;;
  *) cat <<'EOF'
confer.sh — consult a peer AI model, with resumable threads
  open <provider> [-t name] <prompt|->   start a thread (claude|codex); '-' reads prompt from stdin
  ask  <provider> <prompt|->             alias of open (auto thread name)
  reply <thread> <prompt|->              continue a thread (session resumed provider-side)
  all <prompt|->                         fan the same question out to every provider
  list | show <thread>                   registry / full transcript
  doctor [--live]                        check CLIs; --live does a real open+resume per provider
EOF
     ;;
esac
