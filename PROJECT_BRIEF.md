# Codebase Care project brief

> **Role:** durable intent
> **Status:** current

## Purpose

Codebase Care gives Claude Code and Codex one automatic maintenance discipline
for existing repositories, especially where maintainers work primarily through
natural-language requests and cannot be expected to remember a suite of audit,
planning, verification, and documentation prompts.

## Intended users

- Maintainers building or repairing software through Claude Code or Codex.
- Capable readers who may not have deep implementation or security expertise.
- Teams inheriting rapidly accreted, unfamiliar, or heavily AI-generated code.

## Goals

- Enter one maintenance lifecycle automatically for repository-changing work.
- Ground changes in current behavior rather than model-authored assumptions.
- Match autonomy and proof to green, amber, and red risk.
- Make feature retention, repair, refactor, and retirement explicit.
- Explain consequential data flow and enforcement in compact plain language.
- Turn repeatable mechanical signals into deterministic checks without
  overstating what those checks prove.

## Non-goals

- Guarantee that Claude invokes a skill or follows instructions perfectly.
- Certify a codebase as secure or replace specialist review.
- Operate production, deploy, rotate credentials, move funds, or run live
  migrations.
- Generate an exhaustive documentation system or duplicate Repository
  Continuity.
- Teach general programming from first principles.
- Support coding-agent products other than Claude Code and Codex in V1.
- Maintain behaviorally divergent lifecycle forks for different hosts.

## Success

- An ordinary “add/fix/change/remove” request enters the lifecycle without a
  special user prompt.
- A cold run identifies the affected behavior and assigns a justified risk
  floor before editing.
- A baseline review classifies substantial functionality into the five agreed
  dispositions without modifying the target repository.
- Red audits stop before remediation; named fixes receive separate regression
  proof and cannot self-certify deployment readiness.
- Final output remains short enough to be read while clearly naming proof and
  uncertainty.
