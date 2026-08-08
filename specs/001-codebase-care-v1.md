# Spec: Codebase Care V1

status: retired

> **Role:** accepted transition
> **Owner:** repository owner
> **Created:** 2026-08-08
> **Acceptance evidence:** the owner instructed the agent to continue building the scoped Claude-native distribution and selected `codebase-care` as its name

## Context

Conversation-driven maintainers may receive plausible feature implementations
without orientation, threat modeling, proof, or a readable handoff. Requiring
them to remember several specialized prompts moves the safety boundary onto the
least reliable part of the workflow. This slice builds one automatic Claude
Code lifecycle that routes those concerns internally.

## In scope

- A Claude plugin named `codebase-care`.
- One model-invocable `maintain-codebase` skill.
- Minimal SessionStart context that asks Claude to enter the skill for
  repository-changing requests.
- Green, amber, and red risk routing.
- A read-only five-disposition baseline inventory.
- Separation of red audit and remediation.
- Compact evidence-centered opening and closing explanations.
- A dependency-free advisory path/diff classifier and sanitized unit tests.
- Canonical project documentation and local validation instructions.

## Out of scope

- Git initialization, GitHub remote creation, publication, and license choice.
- Modifying or auditing any motivating project.
- Live-system operations, deployment, credential rotation, or financial action.
- Security certification or replacement of a qualified reviewer.
- Non-Claude agent packaging.
- Automated installation into consuming repositories.

## Change shape

| Dimension | Changed? | Owner | Proof |
|---|---:|---|---|
| User-visible behavior | yes | skill and hook | plugin validation and review |
| Persisted runtime state | no | none | architecture review |
| Security/authorization | yes | contracts and risk references | tests and direct review |
| Setup and operation | yes | README and development guide | commands run locally |
| Normative behavior | yes | CONTRACTS.md | owner-accepted scope and review |
| External systems | no | excluded | no integration configuration |

## Done when

- `claude plugin validate .` succeeds.
- Unit tests cover risk escalation and minimal startup context.
- Package checks find every required component and no unresolved placeholders.
- The classifier labels representative docs/style, ordinary code, and
  auth/SQL/dynamic-execution changes at the expected floors.
- Public artifacts contain no project-specific reports or secrets.
- `STATUS.md` records the observed checkpoint and remaining owner decisions.

## Completion

Retired on 2026-08-08 after:

- ten unit tests passed, including a real temporary Git-diff integration test;
- the package checker reported zero errors;
- Claude Code plugin validation passed without warnings;
- the official skill validator passed;
- representative green, amber, and red classifier runs returned their expected
  floors; and
- `STATUS.md` recorded forward-testing, licensing, Git initialization, and
  publication as separate future transitions.
