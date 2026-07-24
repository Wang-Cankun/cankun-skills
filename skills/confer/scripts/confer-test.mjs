#!/usr/bin/env bun
// Deterministic test suite for confer.mjs — zero live calls.
// Fake claude/codex CLIs on a prepended PATH + temp CONFER_HOME per test.
// Covers the failure modes live probes can't: hangs (process-tree kill),
// malformed output, protocol errors, and lock races (concurrent same-thread
// reply, duplicate open). Run: bun scripts/confer-test.mjs

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawn } from "node:child_process";

const MJS = path.join(import.meta.dir, "confer.mjs");
const ROOT = fs.mkdtempSync(path.join(os.tmpdir(), "confer-test-"));
const BIN = path.join(ROOT, "bin");
fs.mkdirSync(BIN);

const FAKE_CLAUDE = `#!/bin/bash
[[ -n "$FAKE_CLAUDE_SLEEP" ]] && sleep "$FAKE_CLAUDE_SLEEP"
case "\${FAKE_CLAUDE_MODE:-ok}" in
  ok)        echo '{"session_id":"sess-claude-1","result":"claude-fake-reply","total_cost_usd":0.12,"duration_ms":3000,"modelUsage":{"claude-fake-model":{"costUSD":0.12,"canonicalModel":"claude-fake-model"}}}' ;;
  fail)      echo 'boom' >&2; exit 1 ;;
  badjson)   echo 'this is not json' ;;
  nosession) echo '{"result":"reply-without-session"}' ;;
  hang)      ( while :; do echo tick >> "$FAKE_HEARTBEAT"; sleep 0.2; done ) & sleep 600 ;;
esac
`;

const FAKE_CODEX = `#!/bin/bash
[[ "$1" == "--version" ]] && { echo codex-fake 0.0.0; exit 0; }
[[ -n "$FAKE_CODEX_SLEEP" ]] && sleep "$FAKE_CODEX_SLEEP"
reply=""; prev=""
for a in "$@"; do [[ "$prev" == "--output-last-message" ]] && reply="$a"; prev="$a"; done
case "\${FAKE_CODEX_MODE:-ok}" in
  ok)   echo '{"type":"thread.started","thread_id":"thread-codex-1"}'
        echo '{"type":"turn.completed","usage":{"input_tokens":1234,"output_tokens":56}}'
        [[ -n "$reply" ]] && printf 'codex-fake-reply' > "$reply" ;;
  fail) echo 'boom' >&2; exit 1 ;;
esac
`;

fs.writeFileSync(path.join(BIN, "claude"), FAKE_CLAUDE, { mode: 0o755 });
fs.writeFileSync(path.join(BIN, "codex"), FAKE_CODEX, { mode: 0o755 });

let n = 0, failed = 0;

function freshHome() {
  const h = fs.mkdtempSync(path.join(ROOT, "home-"));
  return h;
}

function confer(args, { home, env = {}, timeoutMs = 20000 } = {}) {
  return new Promise((resolve) => {
    const child = spawn("bun", [MJS, ...args], {
      // CODEX_HOME defaults to ROOT (no config.toml) so provenance stays hermetic
      env: { ...process.env, PATH: `${BIN}:${process.env.PATH}`, CONFER_HOME: home, CODEX_HOME: ROOT, ...env },
      stdio: ["ignore", "pipe", "pipe"],
    });
    const out = [], err = [];
    child.stdout.on("data", (c) => out.push(c));
    child.stderr.on("data", (c) => err.push(c));
    const t = setTimeout(() => child.kill("SIGKILL"), timeoutMs);
    child.on("close", (code) => {
      clearTimeout(t);
      resolve({ code, stdout: Buffer.concat(out).toString(), stderr: Buffer.concat(err).toString() });
    });
  });
}

const reg = (home) => JSON.parse(fs.readFileSync(path.join(home, "threads.json"), "utf8"));
const tx = (home, name) => fs.readFileSync(path.join(home, "threads", `${name}.md`), "utf8");

function check(name, cond, detail = "") {
  n++;
  if (cond) console.log(`ok ${n} - ${name}`);
  else { failed++; console.log(`FAIL ${n} - ${name}${detail ? `\n     ${detail}` : ""}`); }
}

// 1. open ok: exit 0, registry entry, transcript both directions
{
  const home = freshHome();
  const r = await confer(["open", "claude", "-t", "t1", "hello"], { home });
  check("open ok exits 0", r.code === 0, r.stderr);
  check("open ok registers round 1", reg(home).t1?.rounds === 1 && reg(home).t1?.session === "sess-claude-1");
  const t = tx(home, "t1");
  check("open ok transcript has → and ←", t.includes("## R1 → claude") && t.includes("## R1 ← claude"));
  check("claude provenance in ← header", t.includes("· claude-fake-model · $0.12 · 3s"), t.split("\n").find((l) => l.includes("← claude")));
  check("claude provenance in registry", reg(home).t1?.model === "claude-fake-model");
}

// 1b. codex provenance: model/effort from CODEX_HOME config, tokens from turn.completed
{
  const home = freshHome();
  const codexHome = fs.mkdtempSync(path.join(ROOT, "codexhome-"));
  fs.writeFileSync(path.join(codexHome, "config.toml"), 'model = "fake-sol"\nmodel_reasoning_effort = "xhigh"\n');
  const r = await confer(["open", "codex", "-t", "cx", "q"], { home, env: { CODEX_HOME: codexHome } });
  check("codex provenance open ok", r.code === 0, r.stderr);
  const t = tx(home, "cx");
  check("codex provenance in ← header", t.includes("· fake-sol/xhigh · 1.2k→56tok"), t.split("\n").find((l) => l.includes("← codex")));
  check("codex provenance in registry", reg(home).cx?.model === "fake-sol/xhigh");
  const noCfg = await confer(["open", "codex", "-t", "cx2", "q"], { home });
  check("codex provenance degrades gracefully without config", noCfg.code === 0 && tx(home, "cx2").includes("· 1.2k→56tok"));
}

// 2. all: one provider fails → other still answers, exit 0, stderr names loser
{
  const home = freshHome();
  const r = await confer(["all", "q"], { home, env: { FAKE_CLAUDE_MODE: "fail" } });
  check("all partial: exit 0", r.code === 0, `code=${r.code} stderr=${r.stderr}`);
  check("all partial: codex answer present", r.stdout.includes("codex-fake-reply"));
  check("all partial: stderr names claude", r.stderr.includes("claude failed"));
}

// 3. all: every provider fails → exit 1
{
  const home = freshHome();
  const r = await confer(["all", "q"], { home, env: { FAKE_CLAUDE_MODE: "fail", FAKE_CODEX_MODE: "fail" } });
  check("all total failure exits 1", r.code === 1, `code=${r.code}`);
}

// 4. timeout kills the whole process tree (heartbeat grandchild dies)
{
  const home = freshHome();
  const hb = path.join(home, "heartbeat");
  const t0 = Date.now();
  const r = await confer(["open", "claude", "-t", "hung", "q"], {
    home, env: { FAKE_CLAUDE_MODE: "hang", FAKE_HEARTBEAT: hb, CONFER_TIMEOUT: "1" },
  });
  const elapsed = Date.now() - t0;
  check("timeout: caller fails fast", r.code === 1 && elapsed < 6000, `code=${r.code} elapsed=${elapsed}ms`);
  check("timeout: error mentions timeout", r.stderr.includes("timed out"));
  await new Promise((s) => setTimeout(s, 2600)); // SIGTERM grace is 2s; then heartbeat must be dead
  const size1 = fs.existsSync(hb) ? fs.statSync(hb).size : 0;
  await new Promise((s) => setTimeout(s, 700));
  const size2 = fs.existsSync(hb) ? fs.statSync(hb).size : 0;
  check("timeout: grandchild heartbeat stopped (tree dead)", size1 === size2, `${size1} -> ${size2}`);
  check("timeout: no registry entry (rounds = completed only)", !reg(home).hung);
  check("timeout: transcript has ✗ round", tx(home, "hung").includes("## R1 ✗ claude"));
}

// 5-6. adapter protocol errors
{
  const home = freshHome();
  const r1 = await confer(["open", "claude", "-t", "bj", "q"], { home, env: { FAKE_CLAUDE_MODE: "badjson" } });
  check("malformed JSON is a typed failure", r1.code === 1 && r1.stderr.includes("unparseable"), r1.stderr);
  const r2 = await confer(["open", "claude", "-t", "ns", "q"], { home, env: { FAKE_CLAUDE_MODE: "nosession" } });
  check("missing session is a protocol error", r2.code === 1 && r2.stderr.includes("session"), r2.stderr);
}

// 7. concurrent same-thread reply: one proceeds, loser exits busy, rounds +1 once
{
  const home = freshHome();
  await confer(["open", "claude", "-t", "race", "seed"], { home });
  const [a, b] = await Promise.all([
    confer(["reply", "race", "r1"], { home, env: { FAKE_CLAUDE_SLEEP: "2" } }),
    confer(["reply", "race", "r2"], { home, env: { FAKE_CLAUDE_SLEEP: "2" } }),
  ]);
  const codes = [a.code, b.code].sort();
  const busy = [a, b].find((r) => r.code === 1);
  check("same-thread race: exactly one wins", codes[0] === 0 && codes[1] === 1, `codes=${a.code},${b.code}`);
  check("same-thread race: loser says busy", busy?.stderr.includes("busy"), busy?.stderr);
  check("same-thread race: rounds incremented once", reg(home).race.rounds === 2, `rounds=${reg(home).race.rounds}`);
  const retry = await confer(["reply", "race", "r3"], { home });
  check("same-thread race: retry after release succeeds", retry.code === 0 && reg(home).race.rounds === 3);
}

// 8. concurrent distinct opens: registry lock protects RMW, both land
{
  const home = freshHome();
  const [a, b] = await Promise.all([
    confer(["open", "claude", "-t", "c1", "q"], { home, env: { FAKE_CLAUDE_SLEEP: "1" } }),
    confer(["open", "codex", "-t", "c2", "q"], { home, env: { FAKE_CODEX_SLEEP: "1" } }),
  ]);
  check("distinct concurrent opens both succeed", a.code === 0 && b.code === 0, `${a.stderr}${b.stderr}`);
  check("distinct concurrent opens both registered", !!reg(home).c1 && !!reg(home).c2);
}

// 9. duplicate-name concurrent open: second is refused (busy or exists), one entry
{
  const home = freshHome();
  const [a, b] = await Promise.all([
    confer(["open", "claude", "-t", "dup", "q"], { home, env: { FAKE_CLAUDE_SLEEP: "1" } }),
    confer(["open", "claude", "-t", "dup", "q"], { home, env: { FAKE_CLAUDE_SLEEP: "1" } }),
  ]);
  check("duplicate concurrent open: exactly one wins", [a.code, b.code].sort().join() === "0,1", `codes=${a.code},${b.code}`);
  check("duplicate concurrent open: single round-1 entry", reg(home).dup.rounds === 1);
}

// 10. name validation on every entry point
{
  const home = freshHome();
  for (const args of [["open", "claude", "-t", "../evil", "q"], ["reply", "../evil", "q"], ["show", "../evil"]]) {
    const r = await confer(args, { home });
    check(`name validation refuses on '${args[0]}'`, r.code === 1 && r.stderr.includes("invalid thread name"));
  }
}

// 11. stale lock from a dead process is stolen, not fatal
{
  const home = freshHome();
  fs.mkdirSync(path.join(home, "locks"), { recursive: true });
  fs.writeFileSync(path.join(home, "locks", "thread-stale.lock"), JSON.stringify({ pid: 999999, nonce: "x", ts: 0 }));
  const r = await confer(["open", "claude", "-t", "stale", "q"], { home });
  check("stale lock (dead pid) is stolen", r.code === 0, r.stderr);
}

console.log(failed ? `\n${failed}/${n} FAILED` : `\nall ${n} passed`);
fs.rmSync(ROOT, { recursive: true, force: true });
process.exit(failed ? 1 : 0);
