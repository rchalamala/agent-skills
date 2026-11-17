# Engineering

A curated skill plugin for Claude Code, Codex and Cursor. Work stays in the
native agent loop; focused design, debugging and verification skills load when
needed. Independent work and review can use subagents without making every
implementation step a separate agent.

## Install

Claude Code:

```text
/plugin marketplace add rchalamala/agent-skills
/plugin install engineering@rchalamala
```

Codex:

```text
codex plugin marketplace add rchalamala/agent-skills
codex plugin add engineering@rchalamala
```

Cursor: import `rchalamala/agent-skills` as a GitHub marketplace in Customize,
then install `engineering`.

Load `engineering` for software work, or add this to your agent instructions:

```text
For engineering work, load the engineering skill.
```

The plugin has no startup hooks, credentials, personal memory or model defaults.
It does not activate another pack's orchestration. The engineering skill owns
workflow and testing policy; its focused skills supply reusable practices.
Project instructions and explicit user requests take precedence.

## Included skills

- Native-loop workflow: `engineering`.
- Design and testing: `codebase-design`, `domain-modeling`, `prototype`, `tdd`.
- Explicit interviews/surveys: `grill-me`, `grill-with-docs`,
  `improve-codebase-architecture`, with their `grilling` dependency.
- Transfer: `handoff`.
- Diagnosis and quality: `systematic-debugging`,
  `verification-before-completion`, `receiving-code-review`.

Matt Pocock's skills and Superpowers are MIT-licensed. Their licenses are in
`licenses/`; `upstream.lock.json` records source revisions, selected directories,
namespace transformations and hashes. Copies retain supporting files. Manual
skills also include Codex's explicit-invocation policy. Upstream references to
`superpowers:` are translated to this plugin's `engineering:` namespace; its
TDD dependency resolves to Matt's `tdd`. Recorded per-file patches make generic
project paths explicit and remove repeated test-seam approval prompts.

## Maintenance

The source lives in `dotfiles/agent-plugin/` in the monorepo. The public repository
is a generated mirror, not an editing destination. Machine configuration loads
this same source. Exported history replaces monorepo messages and identities;
only this directory's contents are published.

To update an upstream, inspect the diff from its locked revision, recopy only
selected skill directories and their references, apply the recorded namespace
transformation, preserve explicit-invocation policies, and update the file
hashes and revision. Review dependencies before accepting new skill calls.
Bump the version in all plugin manifests together.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --requirement tests/requirements.txt
.venv/bin/python scripts/check.py
.venv/bin/python -m unittest discover -s tests
```

This checks distribution integrity, not agent effectiveness. Compare the native
agent with and without the plugin on identical tasks in isolated workspaces.
Test activation and non-activation, behavior, integration, interruption recovery,
and delivery. Run each task repeatedly. Keep correctness separate from time and
cost; an unavailable check is untested, never a pass.
