# Codebase Care architecture

> **Role:** implemented system model
> **Status:** current

## Runtime flow

```text
Claude Code manifest ----\
                         -> shared skill, references, classifier, and hook
Codex manifest ----------/
    -> SessionStart hook injects one non-mutating entry instruction
    -> user asks for repository work in ordinary language
    -> maintain-codebase skill orients and selects an operation
    -> risk-routing reference establishes green / amber / red floor
    -> operation reference shapes baseline, change, or red review
    -> advisory classifier may raise the floor from path/diff signals
    -> project-owned tests and review prove semantics
    -> verification reference produces a concise handoff
```

## Components

| Component | Path | Responsibility |
|---|---|---|
| Claude plugin manifest | `.claude-plugin/plugin.json` | Claude Code identity and shared skill path; auto-discovered hooks are not redeclared |
| Claude marketplace catalog | `.claude-plugin/marketplace.json` | installation through Claude Code's CLI, Desktop, and editor plugin managers; its `./` source reuses the fetched marketplace checkout |
| Codex plugin manifest | `.codex-plugin/plugin.json` | Codex identity, presentation metadata, and the same shared skill path |
| Codex marketplace catalog | `.agents/plugins/marketplace.json` | local or Git-backed Codex CLI installation with explicit installation and authentication policy |
| Automatic context hook | `hooks/hooks.json` | emit a static, shell-neutral reminder to enter the lifecycle without user prompting |
| Skill router | `skills/maintain-codebase/SKILL.md` | authorization, operation selection, risk escalation, finish contract |
| Detailed procedures | `skills/maintain-codebase/references/` | lifecycle, risk, baseline, red work, and verification |
| Advisory classifier | `scripts/classify_change.py` | deterministic path/diff signals and risk floor |
| Package checker | `scripts/check_package.py` | required files, links, placeholders, and manifest structure |
| Tests | `tests/` | classifier, hook, and package behavior |

## Boundaries

- The hook contributes context but performs no target-repository inspection or
  mutation and requires no language interpreter.
- Codex requires users to review and trust the exact non-managed plugin hook;
  changed hook content becomes untrusted again. Claude and Codex both discover
  the default `hooks/hooks.json` without a redundant manifest declaration.
- Host manifests are distribution adapters only. Runtime policy remains in the
  single shared skill and reference tree.
- The skill makes contextual judgments; deterministic scripts only report
  structured signals.
- Target repositories own their behavior, tests, documentation, and findings.
- A red audit terminates with evidence. A later named-finding operation may
  implement a fix but cannot certify its own deployment.
- Plugin source remains generic; no motivating repository is encoded as a
  fixture or example.
