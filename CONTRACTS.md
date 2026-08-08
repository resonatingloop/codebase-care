# Codebase Care contracts

> **Role:** normative invariants
> **Status:** current

A failing implementation is not authorization to weaken these contracts.

| ID | Invariant | Primary proof |
|---|---|---|
| `CC-001` | Repository-changing work begins with instruction/state orientation and a risk classification before editing. | skill and lifecycle review |
| `CC-002` | Baselines, audits, and exploratory reviews are read-only unless the user separately authorizes implementation. | skill and reference review |
| `CC-003` | Green, amber, and red are risk floors; uncertainty escalates and no automated result may lower reasoned risk. | classifier tests and risk reference |
| `CC-004` | A red audit cannot silently become remediation in the same operation. | skill and red-work review |
| `CC-005` | A red fix addresses one verified finding, adds focused proof, and is not its own sole release reviewer. | red-work and verification review |
| `CC-006` | The five baseline dispositions are keep, keep dormant, repair, refactor, and retire; reachable dormant surfaces remain attack surface. | baseline review |
| `CC-007` | Final reports distinguish verified evidence, inference, and unverified behavior and never describe generic checks as security certification. | verification review |
| `CC-008` | Model identity or tier may affect capability but never replaces risk controls or proof. | skill review |
| `CC-009` | Automatic startup context is minimal, non-mutating, and grants no tool permission. | hook test and direct review |
| `CC-010` | Public package material contains no private repository content, credentials, audit reports, or personalized rules. | publication review |

## Decision rights

- A direct bounded request authorizes green or amber implementation within its
  stated scope.
- Red audit requests authorize evidence gathering only.
- Live deployment, migrations, credential operations, financial operations,
  and incident containment require explicit human control outside this skill.
- A polished explanation or generic “yes” does not substitute for missing
  project-owned proof or required specialist review.

## Proof boundary

The classifier identifies path and diff signals. It does not establish
exploitability, correctness, effective database policy, deployed state, or
absence of vulnerabilities. Project tests and qualified review own those
semantic claims.

