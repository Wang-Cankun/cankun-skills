#!/bin/bash
# Send one tiny request to a fleet worker route and report what served it.
# Usage: preflight.sh [route]   (default: Pi's configured default model)
#   omp/<provider>/<id>, e.g. omp/openai-codex/gpt-6.1-sol or omp/google-antigravity/gemini-4-argon;
#     the account that served the request is printed.
#   GPT through Pi: magpie/<...> or openai-codex/<...>; the account that served it is printed.
#   Gemini through agy: agy/<model>, e.g. agy/gemini-4-argon-high.
# Any other route exits 1: it may bill outside the user's subscriptions.
# Set FLEET_DENY_ACCOUNT to a substring of an account that must never serve a batch; a match exits 1.
set -euo pipefail
py=python3
route=${1:-$("$py" -c "import json,os;s=json.load(open(os.path.expanduser('~/.pi/agent/settings.json')));print(s['defaultProvider']+'/'+s['defaultModel'])")}
provider=${route%%/*}
model=${route#*/}

if [ "$provider" = agy ]; then
  if ! out=$(agy --mode plan --model "$model" --output-format json -p "Reply with the word ok." </dev/null 2>/dev/null); then
    echo "{\"route\": \"$route\", \"error\": \"agy request failed\"}"
    exit 1
  fi
  "$py" - "$route" "$out" <<'EOF'
import json, sys
route, out = sys.argv[1], sys.argv[2]
final = next((json.loads(l) for l in reversed(out.splitlines()) if l.startswith("{")), {})
ok = final.get("status") == "SUCCESS" and bool((final.get("response") or "").strip())
print(json.dumps({"route": route, "status": final.get("status"), "seconds": final.get("duration_seconds")}))
sys.exit(0 if ok else 1)
EOF
  exit $?
fi

if [ "$provider" = omp ]; then
  # The flags are fleet-job's; omp reads a pipe forever, so stdin is /dev/null.
  provider=${model%%/*}
  if ! out=$(omp -p --mode json --no-session --no-skills --no-rules --no-extensions --no-title --no-lsp \
      --tools read --model "$model" --thinking low -- "Reply with the word ok." </dev/null 2>/dev/null); then
    echo "{\"route\": \"$route\", \"error\": \"omp request failed\"}"
    exit 1
  fi
  "$py" - "$route" "$provider" "$out" <<'EOF'
import json, os, sqlite3, sys
route, provider, out = sys.argv[1:4]
last = None
for line in out.splitlines():
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue
    message = event.get("message") or {}
    if event.get("type") == "message_end" and message.get("role") == "assistant":
        last = message
ok = bool(last) and last.get("stopReason") not in ("error", "aborted") and not last.get("errorMessage")
# Only identity_key is read: the data column holds the login's secret. The reply names the
# credential that served it; without that, every login of the provider is a candidate.
accounts = []
try:
    db = sqlite3.connect("file:" + os.path.expanduser("~/.omp/agent/agent.db") + "?mode=ro", uri=True)
    cid = (last or {}).get("credentialId")
    rows = db.execute("select identity_key from auth_credentials where id = ?", (cid,)) if cid is not None \
        else db.execute("select identity_key from auth_credentials where provider = ? and disabled_cause is null", (provider,))
    accounts = [r[0] for r in rows if r[0]]
except sqlite3.Error:
    pass
print(json.dumps({"route": route, "served_by": accounts, "error": (last or {}).get("errorMessage")}))
deny = os.environ.get("FLEET_DENY_ACCOUNT")
sys.exit(0 if ok and accounts and not (deny and any(deny in a for a in accounts)) else 1)
EOF
  exit $?
fi

# Capture first: grep -q closing the pipe early would fail the pipeline under pipefail.
if ! listed=$(pi --list-models 2>/dev/null | awk '{print $1 "/" $2}'); then
  echo "{\"route\": \"$route\", \"error\": \"pi --list-models failed\"}"
  exit 1
fi
if ! grep -qxF "$route" <<<"$listed"; then
  echo "{\"route\": \"$route\", \"error\": \"Pi does not list this model; add it to the provider (magpie) and sync Pi\"}"
  exit 1
fi

case $provider in
magpie)
  key=$("$py" -c "import json,os;print(json.load(open(os.path.expanduser('~/.pi/agent/models.json')))['providers']['magpie']['apiKey'])")
  reply=$(curl -s -m 90 http://127.0.0.1:3425/v1/chat/completions -H "Authorization: Bearer $key" \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the word ok.\"}],\"max_tokens\":20}")
  "$py" - "$route" "$reply" <<'EOF'
import json, os, sys, time
route, reply = sys.argv[1], sys.argv[2]
try:
    body = json.loads(reply)
except json.JSONDecodeError:
    body = {"error": {"message": reply[:200]}}
err, rid = body.get("error"), body.get("id")
# The usage log names the account behind each response id; served.json lags by seconds, so a
# login's timestamp there cannot attribute one request.
log = os.path.expanduser("~/.config/magpie/usage.jsonl")
account = None
for _ in range(20):
    if err or not rid or not os.path.exists(log):
        break
    with open(log, "rb") as f:
        f.seek(max(0, os.path.getsize(log) - 500_000))
        for line in f.read().decode(errors="replace").splitlines():
            if rid in line:
                try:
                    account = json.loads(line).get("providerAccount")
                except json.JSONDecodeError:
                    pass
    if account:
        break
    time.sleep(0.5)
print(json.dumps({"route": route, "served_by": account, "error": err}))
deny = os.environ.get("FLEET_DENY_ACCOUNT")
sys.exit(0 if account and not err and not (deny and deny in account) else 1)
EOF
  ;;
openai-codex)
  # Pi's own sign-in serves whichever account last logged in; nothing records it per request,
  # so send one request through Pi to prove the token works, then read the signed-in email.
  if ! answer=$(pi -p "Reply with the word ok." --model "$route" --thinking low --no-session </dev/null 2>&1); then
    echo "{\"route\": \"$route\", \"error\": \"request failed\"}"
    exit 1
  fi
  "$py" - "$route" <<'EOF'
import base64, json, os, sys
token = json.load(open(os.path.expanduser("~/.pi/agent/auth.json")))["openai-codex"]["access"]
part = token.split(".")[1]
claims = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
email = claims.get("email") or claims.get("https://api.openai.com/profile", {}).get("email")
print(json.dumps({"model": sys.argv[1], "signed_in_as": email}))
deny = os.environ.get("FLEET_DENY_ACCOUNT")
sys.exit(0 if email and not (deny and deny in email) else 1)
EOF
  ;;
*)
  echo "{\"route\": \"$route\", \"error\": \"preflight knows omp/, magpie/, openai-codex/ and agy/ routes only\"}"
  exit 1
  ;;
esac
