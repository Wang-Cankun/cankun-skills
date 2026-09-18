---
name: ck-teach
description: Explain a body of code, a system, or an analysis workflow plainly by combining ck-how's implementation tracing with ck-why's investigation of rationale. Use when the user asks to learn or understand a change, subsystem, or workflow.
license: MIT
metadata:
  group: general
  summary: Combine mechanism and rationale into a clear explanation at the reader's pace.
---

# CK Teach

Explain what a thing is, how it works, and why it took its current shape in one plain account. The goal is understanding. Match the user's language, background, and requested depth.

## Gather the explanation's evidence

This skill composes `ck-how` and `ck-why`. Load their instructions from the available skill catalog or the sibling `ck-how/SKILL.md` and `ck-why/SKILL.md` directories. They own the investigation; use their findings rather than duplicating the work. If a companion is unavailable, say which investigation is limited and use the evidence you can inspect without claiming that skill ran.

1. Identify what the reader needs to understand from why they are asking: onboarding, reviewing, debugging, changing a workflow, or interpreting an output. Infer existing knowledge from the conversation instead of quizzing them. Put depth where their question is.
2. Orient briefly in the files or supplied material. Use `ck-how` for the mechanism and `ck-why` for the motivation. Scope each investigation to the actual question. A narrow mechanism question may need only `ck-how`; a rationale question may need only `ck-why` after the behavior is established.
3. Run independent investigations in parallel when the host supports it and the work benefits. Otherwise follow the needed companion workflows sequentially yourself. Inherit the current model and settings unless instructed otherwise. If earlier session decisions matter, an available history tool such as `obelisk` can supply leads; it is optional and its records still need evaluation against current evidence.
4. Combine the results into an explanation. Reword for clarity while preserving `ck-why`'s confidence distinctions: a likely motivation must remain likely, a missing rationale must remain unknown, and contradictory evidence must remain visible.

## Teach the mechanism and its purpose

Start with a plain definition and connect it to the project: what the thing is and what it does here. Then walk through a concrete action, input, or result. Explain the problem each important part addresses and how it operates. A list of functions or pipeline stages alone does not explain their relationship.

Lead with the smallest complete answer, then add the detail the request calls for. In a live discussion, leave room for follow-up rather than giving an unsolicited lecture. A request for a full walkthrough or a standalone artifact calls for a complete explanation in that response. Avoid quizzes or forced pacing rituals.

Show the relevant code, a small worked input, a before/after result, or a diagram when it makes the idea easier to grasp. For a complicated picture, build it in a few meaningful layers if that helps; a simple flow may fit one diagram. Choose a medium available in the environment. Images and interactive tools are optional, never a prerequisite for an explanation.

Use consistent names and concrete mechanisms. Keep file and source links near the claims they support without burying the explanation in the investigation log. Separate a workflow's technical behavior from the strength of any scientific interpretation it supports.

Reply with the explanation itself, not a report about running the skills. Preserve the important evidence and uncertainty, and leave deeper threads available for follow-up.

---

Adapted from Lauren Tan's [pstack teach](https://github.com/cursor/plugins/tree/main/pstack/skills/teach). Distributed under the [MIT license](LICENSE).
