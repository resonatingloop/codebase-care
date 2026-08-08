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

