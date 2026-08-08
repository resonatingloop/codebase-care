# Codebase Care

> **Status:** experimental V1
> **Role:** public front door

Codebase Care is a Claude Code plugin for conversation-driven maintenance of
existing software. It turns ordinary requests such as “add this,” “fix that,”
or “remove this feature” into one automatic lifecycle:

```text
orient -> classify risk -> choose the bounded change -> implement
       -> verify behavior -> explain evidence and remaining uncertainty
```

The user does not need to remember separate prompts for planning, security,
testing, documentation, and handoff. One `maintain-codebase` skill routes those
concerns internally and escalates work whose consequences exceed an ordinary
feature change.

Codebase Care is deliberately separate from Repository Continuity. Repository
Continuity preserves durable project truth across sessions. Codebase Care owns
the safety and legibility of changing functionality. It may consume existing
project documentation, but it does not install a documentation system or write
a work log by default.

## What it does

- orients to repository instructions, current state, tests, and affected flows;
- classifies work as green, amber, or red risk;
- inventories an unfamiliar or heavily accreted codebase using five
  dispositions: **keep**, **keep dormant**, **repair**, **refactor**, or
  **retire**;
- keeps red-risk audit and remediation as separate operations;
- runs project-owned proof and an advisory deterministic change classifier;
- gives a short handoff that distinguishes evidence, inference, and unverified
  behavior.

It does not certify software as secure, replace a qualified security reviewer,
operate production systems, or make a model version into a safety boundary.

## Start here

The [Codebase Care user guide](docs/USER_GUIDE.md) walks a Claude Code user
through installing the plugin in VS Code, opening the correct project, running
a five-disposition baseline, requesting ordinary changes, performing a
read-only security audit, and remediating one named red finding at a time. The
terminal path is retained for plugin development and unpublished local testing.

## Install in VS Code

1. Open the project you want Claude to work on in VS Code.
2. Open the Claude Code panel and type `/plugins`.
3. In **Marketplaces**, add `resonatingloop/codebase-care`.
4. In **Plugins**, install **Codebase Care** for your user account.
5. Restart Claude Code or type `/reload-plugins`.

The plugin contributes `/codebase-care:maintain-codebase`. Its skill remains
model-invocable, and a minimal SessionStart hook reminds Claude to enter the
lifecycle automatically for repository-changing requests. See the
[user guide](docs/USER_GUIDE.md) for the orientation smoke test and working
prompts.

## Try an unpublished clone locally

From the clone's parent directory on Windows Command Prompt:

```text
claude --plugin-dir .\codebase-care
```

From the clone's parent directory on macOS or Linux:

```text
claude --plugin-dir ./codebase-care
```

Validate the package without starting a working session on Windows Command
Prompt:

```text
claude plugin validate .
py -3 -m unittest discover -s tests -v
py -3 scripts\check_package.py .
```

On macOS or Linux:

```text
claude plugin validate .
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py .
```

## Risk lanes

- **Green:** narrow presentational or inert changes with local proof.
- **Amber:** behavior, state, dependencies, compatibility, and ordinary data
  flow.
- **Red:** authentication, authorization, secrets, untrusted execution or
  rendering, database policy, admin/moderation, deployment, money-bearing
  systems, or incident response.

Uncertainty raises the lane. A deterministic scan may raise the minimum lane;
it never lowers a reasoned classification.

## Documentation map

| Document | Authority | Owns |
|---|---|---|
| `README.md` | operational/current | public purpose, use, and map |
| `STATUS.md` | operational/current | verified checkpoint and next action |
| `AGENTS.md` | behavioral/current | contribution and authorization rules |
| `PROJECT_BRIEF.md` | durable intent | users, goals, scope, and non-goals |
| `CONTRACTS.md` | normative | safety and behavior invariants |
| `DECISIONS.md` | historical | accepted rationale and supersession |
| `docs/USER_GUIDE.md` | operational/current | end-user setup, prompts, and review gates |
| `docs/ARCHITECTURE.md` | descriptive/current | implemented package and runtime flow |
| `docs/DEVELOPMENT.md` | operational/current | local development and validation |
| `specs/001-codebase-care-v1.md` | planning | accepted V1 transition |

## Publication boundary

The canonical source contains only generic workflows, scripts, and sanitized
tests. Audit reports and project-specific inventories stay with their source
repositories.

The source now has a Git repository and a public
[GitHub remote](https://github.com/resonatingloop/codebase-care). No license has
been selected; license terms remain an unresolved owner decision.
