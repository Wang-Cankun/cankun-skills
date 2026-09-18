# Investigate skill selection

Use this when the skill is missed for relevant requests or selected for nearby
tasks it should not own. Behavioral execution and automatic discovery are
different questions: explicitly naming a skill tests the former.

First inspect registration, duplicate active copies, description visibility,
and any explicit-only policy in the actual host. A broken deployment is not a
reason to broaden the description.

Build a small set of natural user requests covering distinct positive branches
and plausible near misses. Include the request that exposed the problem. Label
expected selection with a reason, keep those labels out of runner prompts, and
ensure they reflect the intended capability rather than keyword presence.

When a real host runner is available, use fresh sessions with the skill
installed in its supported discovery location. Give the plain request without
naming the skill, preserve ordinary neighboring skills, and record whether the
host actually loaded it. Keep model and settings fixed for comparisons. Repeat
ambiguous cases to distinguish variability from a stable routing problem.

Improve only descriptions or pointers implicated by evidence. Prefer distinct
intent boundaries over a growing list of synonyms or catchall trigger phrases.
Compare precision as well as missed invocations. Keep a fresh final set apart
from examples used to tune or select the description.

An optional provider CLI optimizer must use a model that provider supports,
explicit resource limits, isolated registration, and cleanup of its temporary
entries. Check its current behavior before relying on it; no provider-specific
optimizer is required by this skill.

When the host cannot expose or isolate discovery, review likely routing against
neighboring descriptions and label the result an editorial review. A simulated
chooser or explicit invocation does not measure automatic trigger accuracy.
