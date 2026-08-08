# Codebase Care agent guide

This file governs work on the canonical Codebase Care source. Read it before
acting.

## Required reading

1. `README.md` for the public front door and document map.
2. `STATUS.md` for the verified checkpoint.
3. `CONTRACTS.md` before changing skill, hook, or classifier behavior.
4. The active accepted spec under `specs/`, when one exists.
5. `PROJECT_BRIEF.md` before changing product scope or intended users.

If these documents disagree, identify which one owns the disputed fact and
surface the conflict. Do not quietly make the prose agree with an implementation.

## Authorization

- Discussion, exploration, critique, planning, and audits are read-only unless
  the owner explicitly requests changes.
- A direct bounded implementation request authorizes that slice.
- Only the owner may accept a draft spec or change a normative contract.
- Do not initialize version control, assign a remote, publish, or select a
  license without explicit owner authorization.

## Boundaries

- This repository owns reusable, project-agnostic Claude Code infrastructure.
- Project-specific findings, reports, credentials, private code, and filled
  inventories remain in the project that produced them.
- `skills/maintain-codebase/SKILL.md` owns runtime routing.
- Direct files under `skills/maintain-codebase/references/` own detailed
  procedures and must remain progressively loaded.
- `scripts/classify_change.py` produces an advisory risk floor. It can escalate
  review; it can never certify safety or lower a reasoned classification.
- `hooks/hooks.json` may inject only the minimal automatic entry instruction.
  It must not edit target repositories or approve tool use.
- Installed client copies are projections. Edit this canonical source instead.
- Prefer the Python standard library. New runtime dependencies require owner
  approval.

## Validation

Run before closing a material change:

```text
python3 -m unittest discover -s tests -v
python3 scripts/classify_change.py --paths README.md styles/site.css
python3 scripts/check_package.py .
claude plugin validate .
```

Also inspect `git diff --check` and repository status after version control is
initialized.

## Working protocol

1. State the bounded surface and expected proof before editing.
2. Keep the automatic instruction short; route detail into direct references.
3. Test deterministic scripts against sanitized fixtures.
4. Keep audit and remediation separate for red-risk work.
5. Reconcile skill behavior, scripts, hooks, tests, contracts, and public docs.
6. Update `STATUS.md` only from observed validation results.

## Stop and ask

- A change would weaken a safety or authorization contract.
- A hook would execute project commands or modify a consuming repository.
- A fixture would contain project-specific or private material.
- Publishing, licensing, remote assignment, or live-system interaction is
  required.

