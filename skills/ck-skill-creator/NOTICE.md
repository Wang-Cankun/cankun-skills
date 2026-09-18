# Sources and licensing

CK Skill Creator combines independently written guidance informed by:

- Matt Pocock's [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills): instruction hierarchy, completion criteria, and pruning.
- Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), including the locally maintained `claude-skill-creator` adaptation: behavioral trials, comparisons, and artifact review.
- OpenAI's installed [skill-creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator): scoped authoring, progressive disclosure, and independent forward testing.
- Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/main/pstack), especially its Eval playbook: candidate isolation and evidence-based judging.

The CK instructions and validation helper use the repository's MIT license,
included as [LICENSE](LICENSE). Upstream invocation mechanics are treated as
platform-specific; these sources are not installation dependencies.

`eval-viewer/generate_review.py` and `eval-viewer/viewer.html` are distributed
from the local Anthropic skill-creator adaptation, copyright Anthropic, PBC,
under [Apache-2.0](LICENSE-APACHE-2.0). The viewer is optional and runs with the
Python standard library. Any local changes to those files are noted in their
headers.
