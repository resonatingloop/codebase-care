# Codebase Care architecture

> **Role:** implemented system model
> **Status:** current

## Runtime flow

```text
Claude Code session
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
| Plugin manifest | `.claude-plugin/plugin.json` | identity and non-default Claude component paths; auto-discovered hooks are not redeclared |
| Marketplace catalog | `.claude-plugin/marketplace.json` | installation through Claude Code's CLI, Desktop, and editor plugin managers; its `./` source reuses the fetched marketplace checkout |
| Automatic context hook | `hooks/hooks.json` | emit a static, shell-neutral reminder to enter the lifecycle without user prompting |
| Skill router | `skills/maintain-codebase/SKILL.md` | authorization, operation selection, risk escalation, finish contract |
| Detailed procedures | `skills/maintain-codebase/references/` | lifecycle, risk, baseline, red work, and verification |
| Advisory classifier | `scripts/classify_change.py` | deterministic path/diff signals and risk floor |
| Package checker | `scripts/check_package.py` | required files, links, placeholders, and manifest structure |
| Tests | `tests/` | classifier, hook, and package behavior |

## Boundaries

- The hook contributes context but performs no target-repository inspection or
  mutation and requires no language interpreter.
- The skill makes contextual judgments; deterministic scripts only report
  structured signals.
- Target repositories own their behavior, tests, documentation, and findings.
- A red audit terminates with evidence. A later named-finding operation may
  implement a fix but cannot certify its own deployment.
- Plugin source remains generic; no motivating repository is encoded as a
  fixture or example.
