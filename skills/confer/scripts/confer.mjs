#!/usr/bin/env bun
// confer — consult a peer AI model (claude / codex) with resumable threads.
// State: ~/.confer/threads.json (registry) + ~/.confer/threads/<name>.md (transcripts)
// Locks: ~/.confer/locks/ — per-thread operation lock (held across the provider call)
//        + short registry transaction lock. See references/providers.md.

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import { spawn } from "node:child_process";

const CONFER_HOME = process.env.CONFER_HOME || path.join(os.homedir(), ".confer");
const REG = path.join(CONFER_HOME, "threads.json");
const TDIR = path.join(CONFER_HOME, "threads");
const LOCKDIR = path.join(CONFER_HOME, "locks");
const TIMEOUT_MS = (parseInt(process.env.CONFER_TIMEOUT, 10) || 300) * 1000;
const NAME_RE = /^[A-Za-z0-9_-]+$/;

const PREAMBLE =
  "[confer] You are consulted as an independent peer model by another AI agent. Give your own analysis in plain text. Do not modify files or run destructive commands. This thread may continue for multiple rounds.";

class ConferError extends Error {}
class ProviderError extends Error {
  constructor(provider, message, { exitCode = null, stderr = "", timedOut = false } = {}) {
    super(`${provider}: ${message}`);
    Object.assign(this, { provider, exitCode, stderr, timedOut });
  }
}

const die = (msg) => { throw new ConferError(msg); };

function now() {
  const d = new Date(), p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

function initHome() {
  fs.mkdirSync(TDIR, { recursive: true });
  fs.mkdirSync(LOCKDIR, { recursive: true });
  if (!fs.existsSync(REG)) fs.writeFileSync(REG, "{}\n");
}

function readReg() {
  try { return JSON.parse(fs.readFileSync(REG, "utf8")); } catch { return {}; }
}

function validName(name) {
  if (!NAME_RE.test(name)) die(`invalid thread name '${name}' (allowed: letters, digits, - and _)`);
  return name;
}

function splitArgs(v) { return (v || "").split(/\s+/).filter(Boolean); }

// ---- locks -----------------------------------------------------------------
// O_EXCL lock files containing {pid, nonce, ts}. Stale (owner pid dead) locks
// are stolen once. Thread locks fail fast on contention; the registry lock
// retries briefly (it is only ever held across a read-modify-write-rename).

function tryLock(file) {
  const token = { pid: process.pid, nonce: crypto.randomBytes(8).toString("hex"), ts: Date.now() };
  try {
    fs.writeFileSync(file, JSON.stringify(token), { flag: "wx" });
    return token.nonce;
  } catch (e) {
    if (e.code !== "EEXIST") throw e;
    let owner = null;
    try { owner = JSON.parse(fs.readFileSync(file, "utf8")); } catch {}
    const alive = owner && (() => { try { process.kill(owner.pid, 0); return true; } catch { return false; } })();
    if (!alive) {
      try { fs.unlinkSync(file); } catch {}
      try {
        fs.writeFileSync(file, JSON.stringify(token), { flag: "wx" });
        return token.nonce;
      } catch { return null; }
    }
    return owner ? { busyPid: owner.pid } : null;
  }
}

function unlock(file, nonce) {
  try {
    const owner = JSON.parse(fs.readFileSync(file, "utf8"));
    if (owner.nonce === nonce) fs.unlinkSync(file);
  } catch {}
}

function lockThread(name) {
  const file = path.join(LOCKDIR, `thread-${name}.lock`);
  const r = tryLock(file);
  if (typeof r !== "string")
    die(`thread '${name}' busy${r?.busyPid ? ` (pid ${r.busyPid})` : ""} — another confer operation is running; retry when it finishes`);
  return () => unlock(file, r);
}

async function withRegistry(mutate) {
  const file = path.join(LOCKDIR, "registry.lock");
  let nonce = null;
  for (let i = 0; i < 50 && typeof nonce !== "string"; i++) {
    nonce = tryLock(file);
    if (typeof nonce !== "string") await new Promise((r) => setTimeout(r, 100));
  }
  if (typeof nonce !== "string") die("registry lock timeout (~/.confer/locks/registry.lock)");
  try {
    const reg = readReg();
    mutate(reg);
    const tmp = path.join(CONFER_HOME, `.threads.json.tmp.${process.pid}`);
    fs.writeFileSync(tmp, JSON.stringify(reg, null, 2) + "\n");
    fs.renameSync(tmp, REG); // same-dir rename: atomic
  } finally {
    unlock(file, nonce);
  }
}

function regSet(name, provider, session, rounds, model) {
  return withRegistry((reg) => {
    reg[name] = { provider, session, rounds, ...(model ? { model } : {}), updated: now(), created: reg[name]?.created ?? now() };
  });
}

function transcript(name, round, dir, who, text, metaStr = "") {
  fs.appendFileSync(path.join(TDIR, `${name}.md`), `\n## R${round} ${dir} ${who}  (${now()}${metaStr})\n\n${text}\n`);
}

const fmtTok = (n) => (n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n));

// ---- child process runner (D5: process-tree contract) ----------------------
// Detached spawn (own process group); stdout/stderr drained concurrently;
// stdin ignored (prompts travel via argv); on timeout SIGTERM the group,
// grace 2s, then SIGKILL; settle exactly once.

function run(cmd, args, { timeoutMs = TIMEOUT_MS } = {}) {
  return new Promise((resolve, reject) => {
    let child;
    try {
      child = spawn(cmd, args, { detached: true, stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) { return reject(e); }
    let settled = false, timedOut = false;
    const out = [], err = [];
    child.stdout.on("data", (c) => out.push(c));
    child.stderr.on("data", (c) => err.push(c));
    const killGroup = (sig) => { try { process.kill(-child.pid, sig); } catch {} };
    const timer = setTimeout(() => {
      timedOut = true;
      killGroup("SIGTERM");
      setTimeout(() => killGroup("SIGKILL"), 2000).unref();
    }, timeoutMs);
    child.on("error", (e) => {
      if (settled) return; settled = true; clearTimeout(timer);
      reject(e);
    });
    child.on("close", (code) => {
      if (settled) return; settled = true; clearTimeout(timer);
      resolve({ code, stdout: Buffer.concat(out).toString(), stderr: Buffer.concat(err).toString(), timedOut });
    });
  });
}

async function runOrThrow(provider, cmd, args) {
  let r;
  try {
    r = await run(cmd, args);
  } catch (e) {
    if (e.code === "ENOENT") throw new ProviderError(provider, `'${cmd}' CLI not found (run: confer.mjs doctor)`);
    throw new ProviderError(provider, e.message);
  }
  if (r.timedOut)
    throw new ProviderError(provider, `timed out after ${TIMEOUT_MS / 1000}s`, { stderr: r.stderr.trim(), timedOut: true });
  if (r.code !== 0)
    throw new ProviderError(provider, `exited ${r.code}`, { exitCode: r.code, stderr: r.stderr.trim() });
  return r;
}

// ---- provider adapters -----------------------------------------------------
// Contract: ask(prompt, session|null) -> {reply, session}. Failures throw
// ProviderError. Missing session on success is a protocol error (resumable
// threads are the core contract; see providers.md before relaxing this).

const providers = {
  claude: {
    async ask(prompt, session) {
      const args = ["-p", ...(session ? ["--resume", session] : []), "--output-format", "json",
                    ...splitArgs(process.env.CONFER_CLAUDE_ARGS), "--", prompt];
      const r = await runOrThrow("claude", "claude", args);
      let j;
      try { j = JSON.parse(r.stdout); } catch { throw new ProviderError("claude", `unparseable JSON output: ${r.stdout.slice(0, 200)}`); }
      const newSession = j.session_id;
      if (!newSession) throw new ProviderError("claude", "no session_id in response (protocol error)");
      // Provenance (best-effort): dominant modelUsage entry + API-equivalent cost + wall time.
      const mu = j.modelUsage && Object.entries(j.modelUsage).sort((a, b) => (b[1]?.costUSD ?? 0) - (a[1]?.costUSD ?? 0))[0];
      const model = mu?.[1]?.canonicalModel ?? mu?.[0] ?? null;
      const parts = [
        model,
        j.total_cost_usd != null ? `$${j.total_cost_usd.toFixed(2)}` : null,
        j.duration_ms != null ? `${Math.round(j.duration_ms / 1000)}s` : null,
      ].filter(Boolean);
      return { reply: j.result ?? j.error ?? "(empty reply)", session: newSession, meta: { model, parts } };
    },
  },
  codex: {
    // Verified against codex-cli 0.145.0: --sandbox is exec-level only (resume has
    // no --sandbox); --skip-git-repo-check keeps the consultant CWD-independent.
    // Provenance: the event stream carries no model/effort — read config.toml
    // (CONFER_CODEX_ARGS -m / -c model_reasoning_effort= take precedence).
    config() {
      const extra = splitArgs(process.env.CONFER_CODEX_ARGS);
      let model = null, effort = null;
      const mi = extra.findIndex((a) => a === "-m" || a === "--model");
      if (mi >= 0) model = extra[mi + 1] ?? null;
      effort = extra.find((a) => a.includes("model_reasoning_effort="))?.split("=").pop()?.replace(/"/g, "") ?? null;
      if (!model || !effort) {
        try {
          const s = fs.readFileSync(path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "config.toml"), "utf8");
          const g = (k) => s.match(new RegExp(`^${k}\\s*=\\s*"([^"]+)"`, "m"))?.[1] ?? null;
          model ??= g("model"); effort ??= g("model_reasoning_effort");
        } catch {}
      }
      return model ? (effort ? `${model}/${effort}` : model) : null;
    },
    async ask(prompt, session) {
      const replyFile = path.join(os.tmpdir(), `confer-codex-${process.pid}-${crypto.randomBytes(4).toString("hex")}.txt`);
      const base = ["exec", "--sandbox", "read-only", "--skip-git-repo-check"];
      const tail = ["--json", "--output-last-message", replyFile, ...splitArgs(process.env.CONFER_CODEX_ARGS), "--", prompt];
      const args = session ? [...base, "resume", session, ...tail] : [...base, ...tail];
      try {
        const r = await runOrThrow("codex", "codex", args);
        let threadId = null, usage = null;
        for (const line of r.stdout.split("\n")) {
          if (!line.trim()) continue;
          let evt;
          try { evt = JSON.parse(line); } catch { throw new ProviderError("codex", `malformed JSONL event: ${line.slice(0, 200)}`); }
          if (evt.type === "thread.started" && evt.thread_id) {
            if (threadId && threadId !== evt.thread_id)
              throw new ProviderError("codex", `conflicting thread ids: ${threadId} vs ${evt.thread_id}`);
            threadId = evt.thread_id;
          }
          if (evt.type === "turn.completed" && evt.usage) usage = evt.usage;
        }
        const sessionId = session ?? threadId;
        if (!sessionId) throw new ProviderError("codex", "no thread.started event with thread_id (protocol error)");
        let reply;
        try { reply = fs.readFileSync(replyFile, "utf8"); } catch { throw new ProviderError("codex", "no --output-last-message file written (protocol error)"); }
        const model = this.config();
        const parts = [
          model,
          usage ? `${fmtTok(usage.input_tokens ?? 0)}→${fmtTok(usage.output_tokens ?? 0)}tok` : null,
        ].filter(Boolean);
        return { reply, session: sessionId, meta: { model, parts } };
      } finally {
        try { fs.unlinkSync(replyFile); } catch {}
      }
    },
  },
};
const PROVIDERS = Object.keys(providers);

// ---- rounds ----------------------------------------------------------------
// The outbound "→" block is written before the call. On success: "←" block +
// registry commit (rounds counts completed rounds only). On failure: "✗" block,
// no registry change — a retry reuses the same round number. A "→" with neither
// "←" nor "✗" means we died mid-call: peer context may be one round ahead
// (documented ambiguity, see providers.md).

async function runRound(name, provider, prompt, session, round) {
  transcript(name, round, "→", provider, prompt);
  let res;
  try {
    res = await providers[provider].ask(prompt, session);
  } catch (e) {
    transcript(name, round, "✗", provider, e.message);
    throw e;
  }
  const metaStr = res.meta?.parts?.length ? ` · ${res.meta.parts.join(" · ")}` : "";
  transcript(name, round, "←", provider, res.reply, metaStr);
  await regSet(name, provider, res.session, round, res.meta?.model);
  return `${res.reply}\n\n[confer] thread=${name} provider=${provider} round=${round} — continue: confer.mjs reply ${name} "..."`;
}

function readPrompt(args) {
  const prompt = args[0] === "-" ? fs.readFileSync(0, "utf8") : args.join(" ");
  if (!prompt.trim()) die("empty prompt");
  return prompt;
}

function autoName(provider) {
  const d = new Date(), p = (n) => String(n).padStart(2, "0");
  return `${provider}-${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

// ---- commands --------------------------------------------------------------

async function openThread(provider, name, prompt, { preamble = true } = {}) {
  if (!providers[provider]) die(`unknown provider '${provider}' (have: ${PROVIDERS.join(" ")})`);
  initHome();
  const release = lockThread(name); // before the existence check: closes the duplicate-open race
  try {
    if (readReg()[name]) die(`thread '${name}' already exists (use: reply ${name})`);
    const full = preamble ? `${PREAMBLE}\n\n${prompt}` : prompt;
    return await runRound(name, provider, full, null, 1);
  } finally { release(); }
}

async function cmdOpen(args) {
  const provider = args.shift() || die("usage: confer.mjs open <provider> [-t name] <prompt|->");
  let name = null;
  if (args[0] === "-t") { args.shift(); name = validName(args.shift() || die("-t needs a name")); }
  const prompt = readPrompt(args);
  console.log(await openThread(provider, name ?? autoName(provider), prompt));
}

async function cmdReply(args) {
  const name = validName(args.shift() || die("usage: confer.mjs reply <thread> <prompt|->"));
  const prompt = readPrompt(args);
  initHome();
  const release = lockThread(name);
  try {
    const t = readReg()[name]; // fresh read under the lock
    if (!t) die(`no thread '${name}' (see: confer.mjs list)`);
    if (!t.session) die(`thread '${name}' has no session id — not resumable`);
    console.log(await runRound(name, t.provider, prompt, t.session, t.rounds + 1));
  } finally { release(); }
}

async function cmdAll(args) {
  const prompt = readPrompt(args);
  const results = await Promise.allSettled(
    PROVIDERS.map((p) => openThread(p, autoName(p), prompt)),
  );
  let ok = 0;
  results.forEach((r, i) => {
    console.log(`════ ${PROVIDERS[i]} ════`);
    if (r.status === "fulfilled") { ok++; console.log(r.value); }
    else console.error(`confer: ${PROVIDERS[i]} failed: ${r.reason.message}`);
  });
  if (ok === 0) die("all providers failed");
}

function cmdList() {
  initHome();
  const rows = Object.entries(readReg())
    .sort((a, b) => (a[1].updated < b[1].updated ? 1 : -1))
    .map(([k, v]) => [k, v.provider, `r${v.rounds}`, v.updated]);
  if (!rows.length) return;
  const w = rows[0].map((_, i) => Math.max(...rows.map((r) => r[i].length)));
  for (const r of rows) console.log(r.map((c, i) => c.padEnd(w[i])).join("  ").trimEnd());
}

function cmdShow(args) {
  const name = validName(args[0] || die("usage: confer.mjs show <thread>"));
  const f = path.join(TDIR, `${name}.md`);
  if (!fs.existsSync(f)) die(`no transcript for '${name}'`);
  process.stdout.write(fs.readFileSync(f, "utf8"));
}

async function cmdDoctor(args) {
  let ok = true;
  for (const c of PROVIDERS) {
    const r = await run(c, ["--version"], { timeoutMs: 15000 }).catch(() => null);
    if (r && r.code === 0) console.log(`ok   ${c} ${r.stdout.trim().split("\n")[0]}`);
    else { console.log(`MISS ${c}`); ok = false; }
  }
  initHome();
  console.log(`ok   state ${CONFER_HOME} (threads: ${Object.keys(readReg()).length})`);
  if (args[0] === "--live") {
    const mine = []; // clean up exactly the threads this run creates, in finally
    try {
      for (const p of PROVIDERS) {
        console.log(`── live: ${p} (open + resume) ──`);
        const name = `doctor-${p}-${process.pid}-${crypto.randomBytes(3).toString("hex")}`;
        try {
          console.log(await openThread(p, name, "Reply with the single word OK."));
          mine.push(name);
          const t = readReg()[name];
          const release = lockThread(name);
          try { console.log(await runRound(name, p, "Reply with the single word AGAIN.", t.session, t.rounds + 1)); }
          finally { release(); }
        } catch (e) {
          console.error(`confer: ${p} live check failed: ${e.message}`);
          ok = false;
          if (readReg()[name]) mine.push(name);
        }
      }
    } finally {
      if (mine.length) {
        await withRegistry((reg) => { for (const n of mine) delete reg[n]; });
        for (const n of mine) { try { fs.unlinkSync(path.join(TDIR, `${n}.md`)); } catch {} }
        console.log("── doctor threads cleaned ──");
      }
    }
  }
  if (!ok) process.exitCode = 1;
}

const HELP = `confer.mjs — consult a peer AI model, with resumable threads
  open <provider> [-t name] <prompt|->   start a thread (${PROVIDERS.join("|")}); '-' reads prompt from stdin
  ask  <provider> <prompt|->             alias of open (auto thread name)
  reply <thread> <prompt|->              continue a thread (session resumed provider-side)
  all <prompt|->                         fan the same question out to every provider (concurrent)
  list | show <thread>                   registry / full transcript
  doctor [--live]                        check CLIs; --live does a real open+resume per provider
env: CONFER_TIMEOUT (s, default 300) · CONFER_CLAUDE_ARGS / CONFER_CODEX_ARGS · CONFER_HOME`;

const [cmd, ...rest] = process.argv.slice(2);
try {
  switch (cmd) {
    case "open": case "ask": await cmdOpen(rest); break;
    case "reply": await cmdReply(rest); break;
    case "all": await cmdAll(rest); break;
    case "list": cmdList(); break;
    case "show": cmdShow(rest); break;
    case "doctor": await cmdDoctor(rest); break;
    default: console.log(HELP);
  }
} catch (e) {
  if (e instanceof ConferError || e instanceof ProviderError) {
    console.error(`confer: ${e.message}`);
    process.exit(1);
  }
  throw e;
}
