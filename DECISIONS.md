# Codebase Care decisions

> **Role:** accepted historical rationale
> **Status:** append-only

## D-001 — Separate functional stewardship from repository continuity

- Date: 2026-08-08
- Status: accepted

Repository Continuity already owns durable state across sessions and is in
active use. Codebase Care is a separate project whose object is changing
functionality safely and legibly. It may read continuity artifacts but does not
own or replace that protocol.

## D-002 — Expose one automatic maintenance lifecycle

- Date: 2026-08-08
- Status: accepted

Users should not need to remember separate planning, security, testing,
documentation, and handoff prompts. Ship one model-invocable
`maintain-codebase` skill and route detailed operations internally.

## D-003 — Use graded autonomy with non-self-certifying red work

- Date: 2026-08-08
- Status: accepted

Green and amber work may proceed from a bounded implementation request. Red
work separates audit from remediation, requires focused regression proof, and
cannot use the implementing model as its only release reviewer.

## D-004 — Make deterministic classification advisory

- Date: 2026-08-08
- Status: accepted

Path and diff scanning can reliably expose review signals but cannot certify
safety. The classifier therefore emits a risk floor and limitations. Its output
may escalate a lane and may never lower one.

## D-005 — Make the VS Code extension the primary user path

- Date: 2026-08-08
- Status: superseded by D-006

The intended first user works through the Claude Code extension in VS Code,
not a terminal-launched Claude session. Publish Codebase Care through a
GitHub-backed marketplace catalog so users can add and install it from the
extension's `/plugins` interface. Retain `--plugin-dir` as a development and
local-testing path rather than the main user workflow.

## D-006 — Make Claude Desktop the primary user path

- Date: 2026-08-08
- Status: accepted

The intended users work in Claude Desktop's Code tab rather than primarily in
VS Code. Document Desktop's native **+ → Plugins** browser first, with a
terminal Claude Code fallback for registering the third-party marketplace.
Retain VS Code as a supported and owner-tested alternative rather than treating
it as the product boundary. Keep the distribution itself interface-neutral so
the same plugin package can load in Desktop, the terminal CLI, or VS Code.

## D-007 — Add Codex as a thin host adapter

- Date: 2026-08-08
- Status: accepted

Support owner evaluation in Codex CLI without creating a second maintenance
workflow. Add Codex-native manifest and marketplace metadata around the same
`maintain-codebase` skill, progressive references, deterministic classifier,
and default SessionStart hook. Keep Claude Desktop as the primary friend-facing
path; Codex is an equally supported runtime for maintainers and evaluation.
