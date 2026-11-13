# Codebase Care status

> **Role:** operational checkpoint
> **Status:** current experimental V1
> **Last verified:** 2026-11-11

## Verified checkpoint

Codebase Care now reclassifies the realized diff before a material terminal
claim and produces a transient actual-change receipt containing authorization,
realized change shape, final risk, adversarial review dispositions, proof gaps,
departures, and durability. An available continuity close may consume the
receipt, but Codebase Care does not promote repository truth, retire specs, or
create a receipt ledger.

Observed validation:

```text
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py .
python3 <skill-creator>/scripts/quick_validate.py skills/maintain-codebase
claude plugin validate .
```

Evidence of success:

```text
14 tests OK; package check 0 errors; skill valid; plugin validation passed with an unrelated missing-icon warning
```

## Working now

- Automatic entry instruction for ordinary repository-changing requests
- Green, amber, and red routing with uncertainty escalating the floor
- Five-disposition read-only baseline inventory
- Separate red audit and named-fix operations
- Project-owned proof and advisory deterministic change classification
- Actual-change receipt before a material terminal claim
- Optional producer-side handoff to a repository continuity close
- Shared Claude Code and Codex package with public MIT-licensed source

## Incomplete or unverified

- The semantic terminal-claim trigger has not yet been forward-tested in a
  fresh session.
- The receipt has not yet completed an end-to-end handoff to a continuity seal.
- Automatic invocation has not been forward-tested in a fresh disposable
  Claude session against a target repository.
- Marketplace reload and hook execution remain unverified in Claude Desktop on
  Windows; Codex interactive hook trust and native Windows use remain untested.
- Red routing has not been exercised against a sanitized end-to-end audit
  fixture.
- The Claude validator reports an unrelated missing-icon warning.

## Explicitly excluded

- Project- or organization-managed installation
- Promotion of repository truth, spec retirement, or a persistent receipt log
- Any modification of the repositories that motivated this skill

## Next useful action

In the private evaluation workspace, run fresh-session terminal claims against
sanitized slices that should seal as `closed`, `partial`, and `divergent`.
Confirm that the receipt preserves epistemic status, stale review evidence
prevents `closed`, and the standalone handoff remains useful when no continuity
consumer is installed.
