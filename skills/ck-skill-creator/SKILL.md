---
name: ck-skill-creator
description: >-
  Create, revise, and evaluate reusable agent skills. Use for skill authoring,
  unreliable skill behavior, version comparisons, or trigger tuning; use a
  skill manager for installation and retirement.
license: MIT; bundled review viewer under Apache-2.0
compatibility: Optional helpers require Python >=3.10; metadata validation also requires PyYAML.
metadata:
  group: general
  summary: >-
    Write focused, portable skills and improve them through proportionate
    checks, independent trials, and evidence-grounded comparisons.
---

# Create and improve skills

Make the intended behavior easier for a fresh agent to produce. A useful skill
changes decisions or execution; its length, formatting, and number of rules do
not establish its quality.

## Ground the change

Read the requested skill and the resources its affected path uses. For new
work, start from the user's actual task or an existing example. Identify the
intended result, when the skill should apply, and the concrete behavior to
change. Recover settled choices from available context before asking questions.
Ask only for missing judgment that would change the work.

For a reported failure, distinguish an instruction that is missing or unclear
from one the agent ignored, an inaccessible resource, a tool defect, and a
one-off request. Repair the cause at its owner. A tool defect may need a script
fix; a discoverability problem may need a better description or reference
pointer. Neither automatically calls for a longer skill.

Use the canonical source and scope the user requested. Preserve an existing
skill's identity and unrelated content when revising it. A replacement or
retirement is a separate, explicit user decision. Before behavior-changing
edits that need comparison, retain the original outside the distributable.

## Write the smallest useful instruction set

Read [writing.md](references/writing.md) when drafting or restructuring the
skill. Keep shared purpose, decisions, and essential constraints in `SKILL.md`;
put substantial branch-specific detail behind a pointer that says when to read
it. A short skill can be one file.

Use valid YAML with a concrete `name` and a discriminating `description`.
Preserve supported metadata. Add scripts when they remove repeated work or
make a fragile operation reliable; add assets when the output actually uses
them. Each resource needs a caller and purpose.

Write for a fresh conversation. Carry required knowledge inside the skill or
derive it from the target project. Optional tools and other skills may improve
the workflow, but name a usable fallback when they are not essential. Keep
platform-specific registration, model selection, and execution mechanics in
conditional guidance; consult [platforms.md](references/platforms.md) when
those mechanics matter.

## Choose evidence proportional to the change

| Change or question | Useful default |
| --- | --- |
| Wording, a link, or a narrow factual correction | Inspect the affected path and validate the edited files or command. |
| New skill or substantive behavior change | Exercise a representative request with an independent agent when available; inspect its actual result and relevant actions. |
| Does the revision outperform the original? | Run matched old/new cases, or with/without the skill for a new capability; compare anonymized outputs. |
| Is the skill chosen for the right requests? | Investigate discovery separately using [trigger-checks.md](references/trigger-checks.md). |

Choose the smallest set of cases that distinguishes the behavior in question.
Cover a consequential boundary or near miss when it could change the judgment.
For a changed script, run a meaningful successful case and a relevant failure
case. Existing evidence can cover unchanged behavior when its inputs and
assumptions still apply. State the selected check briefly and proceed within
the authorized scope.

For independent trials or comparisons, read
[evaluation.md](references/evaluation.md). Use real raw inputs in an isolated
workspace; keep the author's intended answer and prior conclusions out of the
candidate's context. A simulated user or mocked service must be identified as
such. If no independent execution is available, a walkthrough can find defects
but remains a walkthrough, not a measured behavioral improvement.

Objective checks can proceed without repeated user review. Bring the user
concrete outputs when the decision needs their taste, domain judgment, or a
material tradeoff. A lengthy or externally mutating experiment needs the
appropriate task scope and resources; writing a skill does not authorize its
production actions.

## Improve, then stop on evidence

Read the output and relevant execution record, including wasted work and user
interruptions. For each failure, identify the smallest general correction and
rerun the affected case. Retain important passing cases when the correction
could regress them. Prefer a clear cause and correction over accumulating
instructions for every example.

Stop when the requested behavior has adequate evidence and material failures
are resolved, when the user is satisfied with a subjective result, or when
another round would need new evidence or resources. In the last case, state the
remaining uncertainty. Expand trials only for a new failure, instability, or a
requested stronger claim; a higher score on reused examples alone is not a
reason to keep optimizing.

## Validate and deliver

Run `scripts/validate_skill.py <skill-directory>` with Python and PyYAML when
available. This checks the portable frontmatter, directory identity, and local
resource links; it does not prove behavior or every platform's metadata.
Use the target host's own validation for host-specific fields. Inspect the
description's boundaries and any changed scripts as well.

Report the canonical path, consequential change, checks actually performed,
observed result, and remaining limits. Keep trial artifacts outside the skill
package. Registration, plugin rebuilding, installation, retirement, and release
follow the user's request and the available manager; they are not implied by
authoring. When replacement is authorized, verify the new installed entry and
its resources before withdrawing old deployments. Preserve system-managed
skills unless the user specifically requests a supported change to them.

Sources and bundled component licenses: [NOTICE.md](NOTICE.md).
