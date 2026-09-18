---
name: ck-impact
description: >-
  Trace what a proposed or implemented change could break beyond its immediate
  callers, and test the assumptions its safety depends on. Use for impact
  analysis, compatibility questions, or a small-looking change with uncertain
  downstream effects.
license: MIT
metadata:
  group: general
  summary: >-
    Trace changes across contracts and boundaries, then support consequential
    safety claims with focused executable evidence.
---

# Assess a change's impact

Find the consequential effects outside the edited code and the evidence needed
to judge them. Work from a concrete diff or proposed behavior change. Keep the
review centered on that change; unrelated quality findings belong elsewhere.

## 1. Bound the change

Resolve the baseline, changed behavior, affected artifact, and intended contract
from the request and repository. Include relevant configuration, generated
outputs, and installed entry points when the change reaches them. If the change
is only proposed, distinguish the current implementation from the proposal.

Identify which downstream result matters to the user. A rename, default change,
or cleanup may alter behavior through a stored value or another consumer even
when its direct callers compile.

## 2. Trace the contracts

Follow direct callers, then the relevant boundaries a symbol search misses:
serialized data, persisted state, configuration defaults, dependency behavior,
lifecycle ordering, generated packages, or consumers in another language or
repository. Inspect the dependency version and local patches when its behavior
supports the conclusion. Follow only boundaries the change can plausibly reach.

For each consequential path, state the failure mechanism and its preconditions.
Identify the assumption that would make the path safe, such as an operation
being idempotent or a consumer accepting both representations. Cite the contract
and implementation that support it. Describe likelihood through concrete
conditions; use numerical probabilities only when evidence supports them.

Stop expanding a path when its contract is established and the change cannot
reach farther, or identify the exact unavailable consumer or evidence. A list
of possible hazards without a mechanism is not an impact finding.

## 3. Test the important assumptions

Choose the smallest check that can distinguish the safe case from the failure.
Reuse the project's existing tests, commands, fixtures, and evidence. Existing
evidence can support an unchanged path when its artifact, configuration, inputs,
and assertions still match; say what was reused and why it applies.

For an assumption changed by the proposal, call the real code or public entry
point with a representative case. Prefer an existing focused test or a temporary
script over new infrastructure. Use a running application when the claim
depends on its lifecycle or integration. Confirm the check observes the claimed
behavior, including relevant side effects, and would expose the failure.

Scale effort to the consequence and uncertainty. Reversible, local changes may
need one targeted check; changes to shared formats or state may require several
consumers. If execution needs unavailable data, services, or disproportionate
resources, report the assumption as unproven and name the next useful check.
Source inspection and agreement between reviewers are not executed proof.

Keep product changes outside an assessment-only request. Preserve existing
assertions; a failure is evidence to investigate, not a reason to weaken the
contract. Use isolated scratch state and retain useful evidence after cleaning
up only the processes and files the check created.

For analysis workflows, check input and output contracts, parameter meanings,
reference identities, and numerical expectations with justified tolerances.
Behavioral compatibility, computational correctness, and scientific validity
are separate claims and may require different evidence.

## 4. Report the decision

Give the user the changed behavior and its consequence first, followed by:

- Confirmed risks, each with its mechanism, affected consumer, and evidence.
- The assumptions that make the remaining paths safe, separating execution in
  this run, reused evidence, source-only support, and unproven claims.
- Checks that cleared a plausible risk, and the smallest remaining check or
  correction needed before relying on the change.

Use paths, commands, observed results, and explicit coverage limits. Keep the
report proportional to the decision; an inconclusive check remains inconclusive.

---

Adapted from Lauren Tan's [pstack blast-radius](https://github.com/cursor/plugins/tree/main/pstack/skills/blast-radius), under the [MIT License](LICENSE).
