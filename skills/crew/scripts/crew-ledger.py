#!/usr/bin/env python3
"""Read local agent logs and print a role ledger; never writes to log directories.

Roles file (shell quoting supported, one role per line):
    lead claude session=8e33239a
    executor codex cwd=/absolute/worktree
    reviewer pi cwd=/absolute/worktree

Examples:
    python3 crew-ledger.py --roles roles.txt --since 2026-10-15T07:38:00Z \\
        --until 2026-10-15T10:37:00Z --run-dir .work/crew/overnight
    python3 crew-ledger.py --claude-session d5983194 --json

Claude session mode includes subagents and workflows recursively. --main-only excludes
those descendants for comparison with a main-session-only reference. Time intervals
are [since, until); timestamps without a timezone are rejected. --home selects a
log archive instead of the current user's home. Python 3.9+; no third-party packages.
--include-calls adds timestamped usage (no prompt content) to JSON for burn-rate analysis.
Accepted units use the latest review verdict per unit, timed by current file mtime;
this counts review acceptance, not merged units. Idle share is an activity estimate.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex


IDLE_DEFINITION = (
    "Estimate: equivalent input in user turns with no observed mutation tool invocation "
    "(write/edit/patch or shell file-write/commit), divided by all equivalent input. "
    "Tool-result followups stay in the same turn; delegated sessions are assessed separately. "
    "Invocations are evidence of attempted work, not proof of a changed file; read-only "
    "analysis/review without a saved artifact is counted idle. Open turns are provisional. "
    "This is an activity proxy, not a judgement that the work was useless."
)
MUTATION = re.compile(
    r"\b(?:apply_patch|write_text|write_bytes)\b|"
    r"\bgit\s+(?:-C\s+\S+\s+)?commit\b|"
    r"\b(?:sed|perl)\s+-[^\s]*i|"
    r"\b(?:cp|mv|touch|mkdir|tee)\s|"
    r"(?<![>\d])>{1,2}\s*(?![&\s]|/dev/null)[\w./~'\"]|"
    r"\bopen\([^\n]*?,\s*['\"](?:w|a|x)"
)
FIELDS = ("uncached_input", "cache_write", "cache_read", "output")


def timestamp(value):
    if isinstance(value, (int, float)):
        return value / 1000 if value > 100_000_000_000 else value
    if not value:
        return None
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return result.timestamp()


def iso(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat() if value is not None else None


def events(path, warnings):
    try:
        with path.open(errors="replace") as handle:
            for number, line in enumerate(handle, 1):
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise ValueError("expected an object")
                except (ValueError, TypeError):
                    warnings.add(f"Skipped malformed JSON: {path}:{number}")
                    continue
                yield number, event
    except OSError as error:
        warnings.add(f"Cannot read {path}: {error}")


def metadata(tool, path, warnings):
    session = path.stem
    for number, event in events(path, warnings):
        payload = event.get("payload") or {}
        cwd = event.get("cwd")
        if tool == "codex" and event.get("type") == "session_meta":
            return payload.get("id") or payload.get("session_id"), payload.get("cwd")
        if tool == "pi" and event.get("type") == "session":
            return event.get("id"), cwd
        if tool == "claude" and cwd:
            return session, cwd
    return session, None


def mutates(name, arguments):
    if re.search(r"(?:^|__)(?:Write|Edit|MultiEdit|NotebookEdit|write|edit|apply_patch)$", name):
        return True
    if isinstance(arguments, dict):
        arguments = arguments.get("command", arguments.get("cmd", arguments.get("code", "")))
    return bool(MUTATION.search(str(arguments)))


def parse_log(tool, path, session, warnings, until):
    calls = {}
    productive = set()
    turn = 0
    previous = dict.fromkeys(FIELDS, 0)
    model = "unknown"
    limits = []
    for number, event in events(path, warnings):
        kind = event.get("type")
        payload = event.get("payload") or {}
        message = event.get("message") or {}
        content = message.get("content", [])
        ts = timestamp(event.get("timestamp") or message.get("timestamp"))
        if ts is not None and ts >= until:
            continue
        if tool == "claude":
            if kind == "user" and (isinstance(content, str) or any(
                b.get("type") == "text" for b in content if isinstance(b, dict)
            )) and not event.get("isMeta"):
                turn += 1
            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    if mutates(block.get("name", ""), block.get("input", {})):
                        productive.add(turn)
            usage = message.get("usage") if kind == "assistant" else None
            if not usage:
                continue
            key = (message.get("id") or f"{path}:{number}", event.get("requestId"))
            values = [usage.get(k, 0) or 0 for k in (
                "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"
            )]
            model = message.get("model") or "unknown"
            if model == "<synthetic>":
                continue
        elif tool == "pi":
            if message.get("role") == "user":
                turn += 1
            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "toolCall":
                    if mutates(block.get("name", ""), block.get("arguments", {})):
                        productive.add(turn)
            usage = message.get("usage") if message.get("role") == "assistant" else None
            if not usage:
                continue
            key = event.get("id") or f"line-{number}"
            values = [usage.get(k, 0) or 0 for k in ("input", "cacheWrite", "cacheRead", "output")]
            model = message.get("model") or "unknown"
        else:
            if kind == "turn_context":
                model = payload.get("model") or model
            if kind == "event_msg" and payload.get("type") == "task_started":
                turn += 1
            if kind == "response_item" and payload.get("type") in ("function_call", "custom_tool_call"):
                if mutates(payload.get("name", ""), payload.get("arguments", payload.get("input", ""))):
                    productive.add(turn)
            if kind != "event_msg" or payload.get("type") != "token_count":
                continue
            if payload.get("rate_limits") is not None:
                limits.append({"timestamp": iso(ts), "value": payload["rate_limits"]})
            info = payload.get("info") or {}
            total = info.get("total_token_usage")
            if not total:
                continue
            cached = total.get("cached_input_tokens", 0) or 0
            current = dict(zip(FIELDS, [
                (total.get("input_tokens", 0) or 0) - cached,
                total.get("cache_write_input_tokens", 0) or 0, cached,
                total.get("output_tokens", 0) or 0,
            ]))
            values = [current[k] - previous[k] for k in FIELDS]
            if any(v < 0 for v in values):
                warnings.add(f"Codex cumulative counter reset: {path}:{number}; counted new epoch")
                values = list(current.values())
            previous = current
            if not any(values):
                continue
            key = number
        usage = dict(zip(FIELDS, values))
        context = sum(values[:3])
        if tool == "codex":
            context = (info.get("last_token_usage") or {}).get("input_tokens", context)
        calls[key] = dict(timestamp=iso(ts), time=ts, session=session, source=str(path),
                          key=str(key), turn=turn, model=model, context=context, **usage)
    for call in calls.values():
        call["idle"] = call["turn"] not in productive
    return list(calls.values()), limits


def equivalent(row):
    return row["uncached_input"] + row["cache_write"] + row["cache_read"] / 10


def summarize(calls):
    totals = {k: sum(c[k] for c in calls) for k in FIELDS}
    eq = equivalent(totals)
    idle = sum(equivalent(c) for c in calls if c["idle"])
    contexts = [c["context"] for c in calls]
    return dict(calls=len(calls), **totals, equivalent_input_estimate=round(eq, 2),
                mean_context=round(sum(contexts) / len(contexts), 2) if contexts else None,
                peak_context=max(contexts, default=None), idle_equivalent_estimate=round(idle, 2),
                idle_share_estimate=round(idle / eq, 6) if eq else None,
                models=sorted({c["model"] for c in calls}))


def reviews(run_dir, since, until, warnings):
    accepted = {}
    if run_dir:
        for path in sorted(run_dir.glob("review-*.md"), key=lambda p: p.stat().st_mtime):
            ts = path.stat().st_mtime
            if not since <= ts < until:
                continue
            text = path.read_text()
            unit = re.sub(r"-r\d+$", "", path.stem.removeprefix("review-"))
            verdict = re.search(
                r"(?im)^[ \t]*(?:#{1,6}[ \t]+)?(?:[-*][ \t]*)?[*`]*(?:verdict|结论)"
                r"[*`]*[ \t]*(?:[:：]|\n)\s*([^\n]+)", text
            )
            if not verdict:
                verdict = re.search(r"(?im)^\s*REVIEW\s+" + re.escape(unit) + r"\s+(accept|fix)\b", text)
            value = verdict[1].strip(" \t*`") if verdict else ""
            if not value:
                warnings.add(f"No recognisable verdict: {path}; latest round is not counted as accepted")
            accepted[unit] = ("accept" if re.match(r"accept\b", value, re.I) else "other", str(path))
    return [dict(unit=k, review=v[1]) for k, v in sorted(accepted.items()) if v[0] == "accept"]


def build_report(args):
    since = timestamp(args.since) if args.since else float("-inf")
    until = timestamp(args.until) if args.until else datetime.now(timezone.utc).timestamp()
    if since >= until:
        raise ValueError("--since must precede --until")
    roles = []
    if args.claude_session:
        roles.append(("session", "claude", "session=" + args.claude_session))
    else:
        for line in args.roles.read_text().splitlines():
            parts = shlex.split(line, comments=True)
            if not parts:
                continue
            if len(parts) != 3 or parts[1] not in ("claude", "codex", "pi"):
                raise ValueError("roles: expected NAME {claude,codex,pi} {cwd=PATH,session=ID}")
            roles.append(tuple(parts))
    if not roles or len({r[0] for r in roles}) != len(roles):
        raise ValueError("roles must be nonempty with unique names")
    warnings = set()
    patterns = dict(claude=".claude/projects/*/*.jsonl", codex=".codex/sessions/**/rollout-*.jsonl",
                    pi=".pi/agent/sessions/*/*.jsonl")
    inventory = {}
    for tool in {r[1] for r in roles}:
        inventory[tool] = [(p, *metadata(tool, p, warnings)) for p in sorted(args.home.glob(patterns[tool]))]
    rows, all_calls, claimed = [], [], set()
    claude_owners = {}
    shared_keys = Counter()
    for name, tool, selector in roles:
        mode, sep, value = selector.partition("=")
        if not sep or not value or mode not in ("cwd", "session"):
            raise ValueError(f"invalid selector: {selector}")
        if mode == "cwd" and not args.since:
            raise ValueError("cwd matching requires --since to avoid counting unrelated runs")
        cwd = str(Path(value).expanduser().absolute()) if mode == "cwd" else None
        matches = [(p, sid) for p, sid, log_cwd in inventory[tool]
                   if (sid and sid.startswith(value) if mode == "session" else log_cwd == cwd)]
        if mode == "session" and len(matches) > 1:
            raise ValueError(f"ambiguous session prefix {value}; use a full session id")
        if not matches:
            warnings.add(f"No sessions matched role {name}")
        role_calls, rate_limits, sessions = [], [], []
        seen = {}
        for path, sid in matches:
            sources = [path]
            if tool == "claude" and not args.main_only:
                sources += sorted((path.parent / path.stem / "subagents").rglob("*.jsonl"))
            for source in sources:
                if source in claimed:
                    raise ValueError(f"overlapping roles claim {source}")
                claimed.add(source)
                calls, limits = parse_log(tool, source, sid, warnings, until)
                rate_limits += [r for r in limits if r["timestamp"] and since <= timestamp(r["timestamp"]) < until]
                for call in calls:
                    key = call["key"] if tool == "claude" else (str(source), call["key"])
                    old = seen.get(key)
                    if old:
                        idle = old["idle"] and call["idle"]
                        if (old["time"] or 0) > (call["time"] or 0):
                            call = old
                        call["idle"] = idle
                    seen[key] = call
            sessions.append(sid)
        for call in seen.values():
            if call["time"] is None:
                warnings.add(f'Usage without timestamp excluded: {call["source"]}')
            elif since <= call["time"] < until:
                call["role"] = name
                role_calls.append(call)
                if tool == "claude":
                    owner = claude_owners.setdefault(call["key"], name)
                    if owner != name:
                        shared_keys[(owner, name)] += 1
        row = dict(role=name, tool=tool, selector=selector, sessions=sessions,
                   **summarize(role_calls), rate_limits=sorted(rate_limits, key=lambda r: r["timestamp"])[-1:])
        row["sources"] = [dict(source=p, **summarize([c for c in role_calls if c["source"] == p]))
                          for p in sorted({c["source"] for c in role_calls})]
        rows.append(row)
        all_calls += role_calls
    for (first, second), count in shared_keys.items():
        warnings.add(f"{count} Claude usage keys shared by roles {first} and {second}; "
                     "per-role and run totals include both; choose disjoint roles")
    accepted = reviews(args.run_dir, since, until, warnings)
    total = summarize(all_calls)
    total["accepted_units"] = len(accepted)
    total["equivalent_per_accepted_unit_estimate"] = (
        round(total["equivalent_input_estimate"] / len(accepted), 2) if accepted else None
    )
    idle_sources = Counter()
    for call in all_calls:
        if call["idle"]:
            idle_sources[(call["role"], call["source"])] += equivalent(call)
    report = dict(window=dict(since=args.since, until=iso(until)), roles=rows, total=total,
                accepted_reviews=accepted, idle_definition=IDLE_DEFINITION,
                equivalent_definition="Estimate: uncached input + cache writes + cache reads / 10; excludes output. Not a price or quota conversion.",
                context_definition="Input including caches per call, excluding output; Codex uses last_token_usage.input_tokens. Other zero-usage assistant records count as calls; synthetic Claude messages are excluded.",
                top_idle_sources=[dict(role=k[0], source=k[1], equivalent_input_estimate=round(v, 2))
                                  for k, v in idle_sources.most_common(10)],
                warnings=sorted(warnings))
    if args.include_calls:
        report["calls"] = sorted(all_calls, key=lambda c: c["time"])
    return report


def markdown(report):
    print("| Role | Tool | Calls | Uncached | Cache writes | Cache reads | Output | Equivalent (est.) | Mean context | Peak context | Idle (est.) |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in report["roles"] + [dict(role="TOTAL", tool="", **report["total"])]:
        values = [row["role"].replace("|", "\\|"), row["tool"], row["calls"],
                  *[row[k] for k in FIELDS], row["equivalent_input_estimate"],
                  row["mean_context"], row["peak_context"],
                  f'{row["idle_share_estimate"]:.1%}' if row["idle_share_estimate"] is not None else "n/a"]
        print("| " + " | ".join(str(v) if v is not None else "n/a" for v in values) + " |")
    total = report["total"]
    per_unit = total["equivalent_per_accepted_unit_estimate"]
    print(f'\nWindow [since, until): {report["window"]}')
    print(f'\nAccepted units: {total["accepted_units"]}; equivalent per accepted unit (estimate): {per_unit if per_unit is not None else "n/a"}. Review timestamps use current file mtimes; latest verdict per unit wins.')
    print("\n" + report["equivalent_definition"] + "\n\n" + report["context_definition"])
    print("\nIdle definition: " + report["idle_definition"])
    for source in report["top_idle_sources"]:
        print(f'\n- {source["role"]}: {source["equivalent_input_estimate"]:,.1f} — `{source["source"]}`')
    for row in report["roles"]:
        print(f'\nSessions ({row["role"]}): ' + ", ".join(row["sessions"]))
        if row["rate_limits"]:
            print("\nCodex rate_limits: `" + json.dumps(row["rate_limits"]) + "`")
    for warning in report["warnings"]:
        print("\nWarning: " + warning)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--roles", type=Path)
    mode.add_argument("--claude-session")
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--main-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-calls", action="store_true", help="include timestamped usage for burn-rate analysis in JSON")
    args = parser.parse_args()
    try:
        report = build_report(args)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        markdown(report)


if __name__ == "__main__":
    main()
