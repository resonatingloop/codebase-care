# Codebase Care status

> **Role:** operational checkpoint
> **Status:** current experimental V1
> **Last verified:** 2026-08-08

## Verified checkpoint

Codebase Care now contains a Claude-native plugin with one model-invocable
`maintain-codebase` skill, a minimal non-mutating and interpreter-free
SessionStart instruction, progressively loaded lifecycle references, and a
dependency-free advisory change classifier. A GitHub-backed marketplace catalog
exposes the plugin to the Claude Code extension's VS Code plugin manager.

Observed validation:

```text
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py .
claude plugin validate .
python3 <skill-creator>/scripts/quick_validate.py skills/maintain-codebase
```

Results:

- Ten unit tests passed, including collection and classification of a real
  temporary Git diff.
- The package checker reported zero errors.
- Claude Code plugin validation passed without warnings.
- The skill validator reported `Skill is valid!`.
- Green, amber, and red representative classifier runs returned the expected
  floors.
- The SessionStart hook contains only the intended static, non-mutating entry
  instruction and has no interpreter or plugin-path dependency.
- The marketplace and plugin manifests validate together and declare matching
  version `0.2.0` metadata.

## Working now

- Automatic entry instruction for ordinary repository-changing requests.
- Green, amber, and red routing with uncertainty escalating the floor.
- Five-disposition read-only baseline inventory.
- Separate red audit and named-fix operations.
- Concise proof and uncertainty handoff.
- Advisory detection of representative runtime, database, auth, dynamic-code,
  and HTML-sink change signals.
- A VS Code-first user guide for marketplace installation, baseline review,
  ordinary changes, red audits, named red fixes, updating, and troubleshooting.
- CLI loading retained as a development and unpublished-testing path.
- A public GitHub source repository tracking `origin/master`.

## Incomplete or unverified

- Automatic invocation has not been forward-tested in a fresh disposable Claude
  session against a target repository.
- Marketplace discovery, install, reload, and hook execution have not yet been
  forward-tested in the VS Code extension on a Windows machine.
- Red routing has not been exercised against a sanitized end-to-end audit
  fixture.
- The new marketplace path has not yet been installed outside validation.
- No license has been selected.

## Explicitly excluded

- License selection and project- or organization-managed installation.
- Any modification of the repositories that motivated this skill.

## Next useful action

After version 0.2.0 is pushed, have a Windows VS Code user add
`resonatingloop/codebase-care` through `/plugins`, install Codebase Care for
their user account, reload, and run the orientation smoke test. Then
forward-test one ordinary change, one baseline audit, and one red audit against
fresh disposable fixtures. Select a license before treating the GitHub
repository as a finished public distribution.
