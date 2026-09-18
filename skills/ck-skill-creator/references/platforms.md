# Platform-specific details

The authoring and evaluation method is portable. Discover the current host's
skill locations, supported metadata, available runners, and permissions before
using platform mechanics. Relative references and declared script runtimes keep
the package self-contained; user-specific paths belong in local configuration.

## Codex

Keep `name` and `description` in `SKILL.md`. Optional `agents/openai.yaml` holds
UI metadata and invocation policy. Automatic discovery is the normal default;
when the user requests explicit-only invocation, the policy is:

```yaml
policy:
  allow_implicit_invocation: false
```

Consult the installed official skill-creator's metadata reference or current
host documentation for other fields. Preserve unrelated policy and dependency
fields when changing UI values. A generator that replaces the whole file may
discard them. The official skill is optional authoring assistance, not a
runtime dependency of skills generated here.

## Other hosts

Confirm how the actual host handles frontmatter, explicit invocation,
subagents, and discovery. Fields such as `disable-model-invocation` are not a
universal permission or invocation mechanism. Keep the semantic description
and translate requested invocation policy into the supported host format.

Claude CLI-based trigger optimization measures that CLI's discovery behavior.
Its result does not establish Codex or another host's trigger accuracy. A
headless host can still inspect saved artifacts or a static HTML viewer.

## Registration and replacement

Keep one canonical source. If a manager such as `skl` is available, use its
documented commands for registration, activation, and retirement. Plugins can
provide another active copy that a skill manager may not enumerate: inspect
the host's installed package as well as standalone links.

When the user authorizes replacement, verify the installed replacement's
entrypoint and referenced resources first, then remove old active deployments
and retire their library entries reversibly. Check remaining callers so a
retired path does not become a broken dependency. System-managed built-ins
remain under the host's management; replacing personal skills does not require
removing a built-in with a similar purpose.
