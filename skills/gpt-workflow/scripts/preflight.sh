#!/bin/bash
# Check that Pi lists a GPT worker route, send it one tiny request, and report the account that served it.
# Usage: preflight.sh [route]   (default: Pi's configured default model; magpie/<...> routes are also accepted)
# Set GPT_WORKFLOW_DENY_ACCOUNT to a substring of an account that must never serve a batch; a match exits 1.
set -euo pipefail
py=python3
route=${1:-$("$py" -c "import json,os;s=json.load(open(os.path.expanduser('~/.pi/agent/settings.json')));print(s['defaultProvider']+'/'+s['defaultModel'])")}
provider=${route%%/*}
model=${route#*/}

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
  served=~/.config/magpie/served.json
  key=$("$py" -c "import json,os;print(json.load(open(os.path.expanduser('~/.pi/agent/models.json')))['providers']['magpie']['apiKey'])")
  before=$(cat "$served")
  reply=$(curl -s -m 90 http://127.0.0.1:3425/v1/chat/completions -H "Authorization: Bearer $key" \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the word ok.\"}],\"max_tokens\":20}")
  sleep 1
  "$py" - "$route" "${model%%/*}" "$before" "$(cat "$served")" "$reply" <<'EOF'
import json, os, sys
route, login, before, after, reply = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), json.loads(sys.argv[4]), sys.argv[5]
# Only the login kind that serves this route counts: a concurrent Claude request must not vouch for Codex.
used = [k for k, v in after.items() if k.startswith(login + "@") and before.get(k) != v]
err = json.loads(reply).get("error") if reply.startswith("{") else {"message": reply[:200]}
print(json.dumps({"route": route, "served_by": used, "error": err}))
deny = os.environ.get("GPT_WORKFLOW_DENY_ACCOUNT")
sys.exit(0 if used and not err and not (deny and any(deny in u for u in used)) else 1)
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
deny = os.environ.get("GPT_WORKFLOW_DENY_ACCOUNT")
sys.exit(0 if email and not (deny and deny in email) else 1)
EOF
  ;;
*)
  echo "{\"route\": \"$route\", \"error\": \"preflight knows magpie/ and openai-codex/ routes only\"}"
  exit 1
  ;;
esac
