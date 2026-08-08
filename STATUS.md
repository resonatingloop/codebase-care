# Codebase Care status

> **Role:** operational checkpoint
> **Status:** current experimental V1
> **Last verified:** 2026-08-08

## Verified checkpoint

Codebase Care now contains a Claude-native plugin with one model-invocable
`maintain-codebase` skill, a minimal non-mutating and interpreter-free
SessionStart instruction, progressively loaded lifecycle references, and a
dependency-free advisory change classifier. A GitHub-backed marketplace catalog
exposes the plugin to Claude Code's plugin managers. Claude Desktop's Code tab
is now the primary documented user surface.

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
  version `0.2.1` metadata.
- The owner observed successful marketplace discovery and installation in the
  Claude Code VS Code extension on Windows.

## Working now

- Automatic entry instruction for ordinary repository-changing requests.
- Green, amber, and red routing with uncertainty escalating the floor.
- Five-disposition read-only baseline inventory.
- Separate red audit and named-fix operations.
- Concise proof and uncertainty handoff.
- Advisory detection of representative runtime, database, auth, dynamic-code,
  and HTML-sink change signals.
- A Claude Desktop-first user guide for marketplace installation, baseline
  review, ordinary changes, red audits, named red fixes, updating, and
  troubleshooting.
- Terminal CLI registration and local loading retained as fallback and
  development paths; VS Code is retained as a tested alternative surface.
- A public GitHub source repository tracking `origin/master`.

## Incomplete or unverified

- Automatic invocation has not been forward-tested in a fresh disposable Claude
  session against a target repository.
- Marketplace discovery and installation succeeded in the VS Code extension on
  Windows, but reload and hook execution have not yet been owner-verified.
- Marketplace discovery, installation, and skill invocation have not yet been
  forward-tested in a local Claude Desktop Code session on Windows.
- Red routing has not been exercised against a sanitized end-to-end audit
  fixture.
- No license has been selected.

## Explicitly excluded

- License selection and project- or organization-managed installation.
- Any modification of the repositories that motivated this skill.

## Next useful action

After version 0.2.1 is pushed, open a local Claude Desktop Code session on
Windows in a disposable repository. Check **+ → Plugins → Manage plugins**, use
**Add plugin** if needed, and run the orientation smoke test. If the
`resonatingloop` marketplace is not visible, register it once through the
terminal CLI and retry Desktop. Then forward-test one ordinary change, one
baseline audit, and one red audit against fresh disposable fixtures. Select a
license before treating the GitHub repository as a finished public
distribution.
