# Codebase Care status

> **Role:** operational checkpoint
> **Status:** current experimental V1
> **Last verified:** 2026-08-08

## Verified checkpoint

Codebase Care now contains native Claude Code and Codex plugin adapters around
one model-invocable `maintain-codebase` skill, a minimal non-mutating and
interpreter-free SessionStart instruction, progressively loaded lifecycle
references, and a dependency-free advisory change classifier. Host-specific
marketplace catalogs expose the same package without duplicating its runtime
policy. Claude Desktop remains the primary friend-facing surface; Codex CLI is
supported for maintenance and evaluation.

Observed validation:

```text
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py .
claude plugin validate .
CLAUDE_CONFIG_DIR=<temporary-directory> claude plugin install codebase-care@resonatingloop
python3 <skill-creator>/scripts/quick_validate.py skills/maintain-codebase
python3 <plugin-creator>/scripts/validate_plugin.py .
codex plugin marketplace add . --json
codex plugin add codebase-care@resonatingloop --json
codex plugin list --json
codex exec --ephemeral --sandbox read-only --dangerously-bypass-hook-trust <orientation prompt>
```

Results:

- Fourteen unit tests passed, including collection and classification of a real
  temporary Git diff and rejection of both redundant self-cloning and duplicate
  auto-discovered hook declarations. New coverage rejects divergent Claude and
  Codex versions and a Codex marketplace source that would not reuse this root.
- The package checker reported zero errors.
- Claude Code plugin validation passed without warnings.
- Codex plugin validation passed.
- The skill validator reported `Skill is valid!`.
- Green, amber, and red representative classifier runs returned the expected
  floors.
- The SessionStart hook contains only the intended static, non-mutating entry
  instruction and has no interpreter or plugin-path dependency.
- The Claude and Codex manifests validate and declare matching version `0.3.0`
  metadata around the same `./skills/` directory.
- The marketplace entry uses the fetched repository root as its plugin source,
  avoiding a redundant second GitHub clone during installation.
- Both host manifests leave the standard `hooks/hooks.json` path to automatic
  discovery, avoiding duplicate-hook load failures.
- The owner observed successful marketplace discovery and installation in the
  Claude Code VS Code extension on Windows.
- A clean isolated Claude configuration added the local marketplace, installed
  version 0.2.2 at user scope, and reported the plugin enabled with one skill
  and one SessionStart hook.
- Codex registered this clone as the local `resonatingloop` marketplace,
  installed and enabled `codebase-care@resonatingloop` version `0.3.0`, and
  reported the expected local source and explicit install/authentication policy.
- A fresh ephemeral Codex session explicitly invoked the installed skill and
  loaded its lifecycle references from the plugin cache.
- A second fresh ephemeral Codex session, prompted only for ordinary read-only
  orientation, automatically selected the Codebase Care workflow and loaded the
  installed skill. The vetted static hook was allowed for those automated runs
  with Codex's hook-trust bypass; normal interactive trust remains an owner
  check.

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
- A Codex CLI evaluation appendix with native installation, new-session,
  explicit skill invocation, and hook-trust instructions.
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
- Codex plugin installation and routing passed on Linux, but the ordinary
  interactive `/hooks` review/trust flow has not yet been owner-tested, nor has
  the package been tested through Codex CLI on native Windows.
- Red routing has not been exercised against a sanitized end-to-end audit
  fixture.
- No license has been selected.

## Explicitly excluded

- License selection and project- or organization-managed installation.
- Any modification of the repositories that motivated this skill.

## Next useful action

Open a new interactive Codex CLI session in the intended target repository,
review and trust the exact Codebase Care hook through `/hooks`, and run the
read-only baseline before authorizing any changes. After version `0.3.0` is
committed and pushed, retain the pending Claude Desktop Windows checks and
forward-test one ordinary change, one baseline audit, and one red audit against
fresh disposable fixtures. Select a license before treating the GitHub
repository as a finished public distribution.
