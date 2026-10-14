#!/usr/bin/env python3
"""Run Pi (pi.dev coding agent) as a background worker and collect its result.

Usage:
  pi_job.py start --spec SPEC.json            # or flags: --model --prompt-file --tools ...
  pi_job.py wait JOB [--timeout SECONDS]      # exit 0 when finished, 3 while still running
  pi_job.py result JOB [--text | --structured]
  pi_job.py status JOB
  pi_job.py cancel JOB
  pi_job.py list

Spec (JSON): prompt | prompt_file, model (optional; Pi's configured default otherwise), thinking, tools (list or preset name:
readonly, research, write, full), cwd, schema | schema_file, append_system_prompt,
extensions (list), no_extensions, session (default true), approve (true/false/null),
max_minutes (default 60), name.

Jobs live in $PI_JOB_HOME (default ~/.claude/pi-jobs/<job-id>/): spec.json, prompt.md,
events.jsonl (Pi JSON mode), stderr.log, state.json, result.json, session/.
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOBS_HOME = Path(os.environ.get("PI_JOB_HOME", Path.home() / ".claude" / "pi-jobs"))
SUBMIT_EXTENSION = HERE / "submit_result.ts"

TOOL_PRESETS = {
    "readonly": ["read", "grep", "find", "ls"],
    # Fan-out (subagent, its supervisor and bg_wait), codemode and the browser let one job
    # parallelise its own reading; a tool missing from this list is invisible to the job.
    "research": ["read", "grep", "find", "ls", "web_search", "fetch_content", "get_search_content",
                 "agent_browser", "subagent", "subagent_supervisor", "bg_wait", "codemode"],
    "write": ["read", "grep", "find", "ls", "edit", "write"],
    "full": ["read", "grep", "find", "ls", "edit", "write", "bash",
             "web_search", "fetch_content", "get_search_content", "agent_browser",
             "subagent", "subagent_supervisor", "bg_wait", "codemode"],
}
TERMINAL = {"completed", "failed", "no_result", "cancelled", "timeout"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.exit(code)


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, value) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False))
    tmp.replace(path)


def job_dir(job: str) -> Path:
    path = Path(job) if os.sep in job else JOBS_HOME / job
    if not (path / "spec.json").exists():
        die(f"unknown job: {job}")
    return path


def pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


# ---------------------------------------------------------------- spec handling


def build_spec(args) -> dict:
    spec = read_json(Path(args.spec), None) if args.spec else {}
    if spec is None:
        die(f"cannot read spec: {args.spec}")
    for key in ("model", "thinking", "cwd", "name", "prompt_file", "schema_file"):
        value = getattr(args, key, None)
        if value is not None:
            spec[key] = value
    if args.tools is not None:
        spec["tools"] = args.tools
    if args.prompt is not None:
        spec["prompt"] = args.prompt

    if "prompt" not in spec:
        if "prompt_file" not in spec:
            die("spec needs prompt or prompt_file")
        spec["prompt"] = Path(spec["prompt_file"]).expanduser().read_text()
    if "schema" not in spec and spec.get("schema_file"):
        spec["schema"] = read_json(Path(spec["schema_file"]).expanduser())
        if spec["schema"] is None:
            die(f"cannot read schema_file: {spec['schema_file']}")
    schema = spec.get("schema")
    if schema is not None and schema.get("type") != "object":
        die("schema root must be a JSON Schema object (type: object)")

    tools = spec.get("tools", "readonly")
    if isinstance(tools, str):
        tools = TOOL_PRESETS.get(tools, tools.split(","))
    tools = [t for t in tools if t]
    if schema is not None and "submit_result" not in tools:
        tools.append("submit_result")
    spec["tools"] = tools
    spec["cwd"] = str(Path(spec.get("cwd") or os.getcwd()).expanduser().resolve())
    if not Path(spec["cwd"]).is_dir():
        die(f"cwd does not exist: {spec['cwd']}")
    spec.setdefault("session", True)
    spec.setdefault("max_minutes", 60)
    return spec


def pi_command(spec: dict, jdir: Path) -> list[str]:
    cmd = ["pi", "--mode", "json", "--offline"]
    if spec.get("model"):
        cmd += ["--model", spec["model"]]
    if spec.get("thinking"):
        cmd += ["--thinking", spec["thinking"]]
    cmd += ["--tools", ",".join(spec["tools"])]
    if spec.get("session", True):
        cmd += ["--session-dir", str(jdir / "session")]
    else:
        cmd += ["--no-session"]
    if spec.get("no_extensions"):
        cmd += ["--no-extensions"]
    if spec.get("approve") is True:
        cmd += ["--approve"]
    elif spec.get("approve") is False:
        cmd += ["--no-approve"]
    for ext in spec.get("extensions", []):
        cmd += ["-e", str(Path(ext).expanduser())]
    if spec.get("schema") is not None:
        cmd += ["-e", str(SUBMIT_EXTENSION)]
    if spec.get("append_system_prompt"):
        cmd += ["--append-system-prompt", spec["append_system_prompt"]]
    if spec.get("name"):
        cmd += ["--name", spec["name"]]
    cmd += ["-p", "--", spec["prompt"]]
    return cmd


# ---------------------------------------------------------------- event parsing


def iter_events(path: Path):
    # Pi's JSONL is framed on LF only; U+2028/U+2029 may occur inside strings.
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return
    for raw in data.split(b"\n"):
        raw = raw.rstrip(b"\r")
        if not raw:
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue  # a partially written trailing record


def text_of(message: dict) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content
    return "".join(c.get("text", "") for c in content or [] if c.get("type") == "text")


def summarize(jdir: Path) -> dict:
    spec = read_json(jdir / "spec.json", {})
    state = read_json(jdir / "state.json", {})
    settled = False
    last_assistant = None
    session_id = None
    cost = 0.0
    tokens = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
    tool_calls: dict[str, int] = {}
    tool_errors: dict[str, int] = {}
    structured = None
    retries_failed = None
    actual_model = None
    for ev in iter_events(jdir / "events.jsonl"):
        kind = ev.get("type")
        if kind == "session":
            session_id = ev.get("id")
        elif kind == "agent_settled":
            settled = True
        elif kind == "message_end" and ev.get("message", {}).get("role") == "assistant":
            last_assistant = ev["message"]
            if last_assistant.get("model"):
                actual_model = f"{last_assistant.get('provider')}/{last_assistant.get('model')}"
            usage = last_assistant.get("usage") or {}
            cost += (usage.get("cost") or {}).get("total", 0) or 0
            for key in tokens:
                tokens[key] += usage.get(key, 0) or 0
        elif kind == "tool_execution_end":
            name = ev.get("toolName", "?")
            tool_calls[name] = tool_calls.get(name, 0) + 1
            if ev.get("isError"):
                tool_errors[name] = tool_errors.get(name, 0) + 1
            elif name == "submit_result":
                structured = (ev.get("result") or {}).get("details")
        elif kind == "auto_retry_end" and not ev.get("success", True):
            retries_failed = ev.get("finalError")

    stop_reason = last_assistant.get("stopReason") if last_assistant else None
    error_message = (last_assistant or {}).get("errorMessage") or retries_failed
    exit_code = state.get("exit_code")

    if state.get("status") in ("cancelled", "timeout"):
        status = state["status"]
    elif state.get("status") in ("starting", "running"):
        status = state["status"]
    elif exit_code not in (0, None):
        status = "failed"
    elif not settled:
        status = "failed"
        error_message = error_message or "Pi exited before agent_settled"
    elif stop_reason in ("error", "aborted"):
        status = "failed"
    elif spec.get("schema") is not None and structured is None:
        status = "no_result"
    else:
        status = "completed"

    sessions = sorted((jdir / "session").glob("**/*.jsonl")) if (jdir / "session").exists() else []
    stderr_tail = ""
    if status == "failed" and (jdir / "stderr.log").exists():
        stderr_tail = (jdir / "stderr.log").read_text(errors="replace")[-2000:]
    return {
        "job_id": jdir.name,
        "status": status,
        "model": actual_model or spec.get("model"),
        "requested_model": spec.get("model"),
        "name": spec.get("name"),
        "started_at": state.get("started_at"),
        "finished_at": state.get("finished_at"),
        "exit_code": exit_code,
        "stop_reason": stop_reason,
        "error": error_message,
        "text": text_of(last_assistant) if last_assistant else "",
        "structured": structured,
        "tool_calls": tool_calls,
        "tool_errors": tool_errors,
        "cost_usd": round(cost, 6),
        "tokens": tokens,
        "session_id": session_id,
        "session_file": str(sessions[-1]) if sessions else None,
        "dir": str(jdir),
        "stderr_tail": stderr_tail,
    }


# ---------------------------------------------------------------- commands


def cmd_start(args) -> None:
    spec = build_spec(args)
    JOBS_HOME.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    label = "".join(c if c.isalnum() or c in "-_" else "-" for c in (spec.get("name") or "job"))[:40]
    jdir = JOBS_HOME / f"{stamp}-{label}-{secrets.token_hex(3)}"
    jdir.mkdir()
    (jdir / "prompt.md").write_text(spec["prompt"])
    if spec.get("schema") is not None:
        write_json(jdir / "schema.json", spec["schema"])
    write_json(jdir / "spec.json", spec)
    write_json(jdir / "state.json", {"status": "starting", "created_at": now()})

    with open(jdir / "supervisor.log", "ab") as log:
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "_supervise", str(jdir)],
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            start_new_session=True, close_fds=True,
        )

    deadline = time.time() + 15
    while time.time() < deadline:
        state = read_json(jdir / "state.json", {})
        if state.get("status") == "running" and state.get("pid") and (jdir / "events.jsonl").exists():
            break
        if state.get("status") in TERMINAL:
            break
        time.sleep(0.2)
    state = read_json(jdir / "state.json", {})
    if state.get("status") == "starting":
        die(f"job did not start within 15 s; see {jdir / 'supervisor.log'}", 1)
    print(json.dumps({"job_id": jdir.name, "status": state.get("status"), "pid": state.get("pid"), "dir": str(jdir)}))


def cmd_supervise(args) -> None:
    jdir = Path(args.jdir)
    spec = read_json(jdir / "spec.json")
    env = dict(os.environ)
    if spec.get("schema") is not None:
        env["PI_JOB_SCHEMA"] = str(jdir / "schema.json")
    with open(jdir / "events.jsonl", "wb") as out, open(jdir / "stderr.log", "wb") as err:
        try:
            proc = subprocess.Popen(pi_command(spec, jdir), cwd=spec["cwd"], env=env,
                                    stdin=subprocess.DEVNULL, stdout=out, stderr=err)
        except OSError as exc:
            write_json(jdir / "state.json", {"status": "failed", "error": str(exc), "finished_at": now()})
            return
        write_json(jdir / "state.json", {"status": "running", "pid": proc.pid,
                                         "supervisor_pid": os.getpid(), "started_at": now()})
        timed_out = False
        try:
            exit_code = proc.wait(timeout=float(spec.get("max_minutes", 60)) * 60)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.terminate()
            try:
                exit_code = proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                proc.kill()
                exit_code = proc.wait()
    state = read_json(jdir / "state.json", {})
    cancelled = (jdir / "cancel-requested").exists()
    state.update({"exit_code": exit_code, "finished_at": now(),
                  "status": "cancelled" if cancelled else "timeout" if timed_out else "finished"})
    write_json(jdir / "state.json", state)
    write_json(jdir / "result.json", summarize(jdir))


def current_status(jdir: Path) -> dict:
    state = read_json(jdir / "state.json", {})
    if state.get("status") == "running" and not pid_alive(state.get("supervisor_pid")) \
            and not (jdir / "result.json").exists():
        state.update({"status": "finished", "exit_code": state.get("exit_code", -1), "finished_at": now()})
        write_json(jdir / "state.json", state)
        write_json(jdir / "result.json", summarize(jdir))
    if (jdir / "result.json").exists():
        return read_json(jdir / "result.json")
    return summarize(jdir)


def brief(result: dict) -> dict:
    keys = ("job_id", "status", "model", "name", "stop_reason", "error", "cost_usd", "tool_calls", "dir")
    out = {k: result.get(k) for k in keys}
    out["has_structured"] = result.get("structured") is not None
    return out


def cmd_status(args) -> None:
    print(json.dumps(brief(current_status(job_dir(args.job)))))


def cmd_wait(args) -> None:
    jdir = job_dir(args.job)
    deadline = time.time() + args.timeout
    while True:
        result = current_status(jdir)
        if result["status"] in TERMINAL:
            print(json.dumps(brief(result)))
            return
        if time.time() >= deadline:
            print(json.dumps(brief(result)))
            sys.exit(3)
        time.sleep(3)


def cmd_result(args) -> None:
    result = current_status(job_dir(args.job))
    if args.text:
        print(result.get("text", ""))
    elif args.structured:
        print(json.dumps(result.get("structured"), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] not in TERMINAL:
        sys.exit(3)


def cmd_cancel(args) -> None:
    jdir = job_dir(args.job)
    state = read_json(jdir / "state.json", {})
    (jdir / "cancel-requested").write_text(now())
    if pid_alive(state.get("pid")):
        os.kill(state["pid"], signal.SIGTERM)
    for _ in range(50):
        if (jdir / "result.json").exists():
            break
        time.sleep(0.2)
    print(json.dumps(brief(current_status(jdir))))


def cmd_list(args) -> None:
    if not JOBS_HOME.exists():
        return
    for jdir in sorted(JOBS_HOME.iterdir())[-args.limit:]:
        if (jdir / "spec.json").exists():
            print(json.dumps(brief(current_status(jdir))))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("start")
    p.add_argument("--spec")
    p.add_argument("--model")
    p.add_argument("--thinking")
    p.add_argument("--tools", help="preset (readonly, research, write, full) or comma list")
    p.add_argument("--cwd")
    p.add_argument("--name")
    p.add_argument("--prompt")
    p.add_argument("--prompt-file", dest="prompt_file")
    p.add_argument("--schema-file", dest="schema_file")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("_supervise")
    p.add_argument("jdir")
    p.set_defaults(func=cmd_supervise)

    for name, func in (("status", cmd_status), ("cancel", cmd_cancel)):
        p = sub.add_parser(name)
        p.add_argument("job")
        p.set_defaults(func=func)

    p = sub.add_parser("wait")
    p.add_argument("job")
    p.add_argument("--timeout", type=float, default=540)
    p.set_defaults(func=cmd_wait)

    p = sub.add_parser("result")
    p.add_argument("job")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--text", action="store_true")
    group.add_argument("--structured", action="store_true")
    p.set_defaults(func=cmd_result)

    p = sub.add_parser("list")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
