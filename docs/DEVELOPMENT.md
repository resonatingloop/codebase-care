# Codebase Care development

> **Role:** operational development procedure
> **Status:** current

## Requirements

- Python 3.10 or newer for deterministic scripts and tests.
- Claude Code with plugin validation support.

The SessionStart hook has no language-runtime dependency. Python is needed only
for deterministic scripts and their tests; no third-party Python package is
required.

## Validate

From the repository root:

Windows Command Prompt:

```text
py -3 -m unittest discover -s tests -v
py -3 scripts\check_package.py .
claude plugin validate .
```

macOS or Linux:

```text
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py .
claude plugin validate .
```

Exercise representative classifier paths:

Windows Command Prompt uses `py -3` and backslashes; for example:

```text
py -3 scripts\classify_change.py --paths README.md styles\site.css
py -3 scripts\classify_change.py --paths src\profile.js
py -3 scripts\classify_change.py --paths supabase\migrations\001_auth.sql
```

On macOS or Linux:

```text
python3 scripts/classify_change.py --paths README.md styles/site.css
python3 scripts/classify_change.py --paths src/profile.js
python3 scripts/classify_change.py --paths supabase/migrations/001_auth.sql
```

## Test interactively

### Claude Desktop marketplace path

After the target revision is available on GitHub:

1. Open the Claude Desktop **Code** tab and start a local session in a
   disposable project.
2. Select **+ → Plugins → Manage plugins** and check whether the user-scope VS
   Code installation is already visible.
3. If it is absent, select **+ → Plugins → Add plugin** and find Codebase Care
   in the configured `resonatingloop` marketplace.
4. Install it for the test user.
5. If the marketplace is missing, register it once from a terminal Claude Code
   session with `/plugin marketplace add resonatingloop/codebase-care`, then
   return to Desktop.
6. Run the orientation smoke test from `docs/USER_GUIDE.md`.

The owner has separately observed successful marketplace discovery and
installation through the VS Code extension on Windows. That result does not
prove Desktop loading or skill invocation.

### Local clone path

From the clone's parent directory:

Windows Command Prompt:

```text
claude --plugin-dir .\codebase-care
```

macOS or Linux:

```text
claude --plugin-dir ./codebase-care
```

In a disposable target repository, ask for a normal feature change without
naming the skill. Confirm that Claude enters the lifecycle, explains the risk
floor, runs appropriate proof, and does not manufacture a documentation system.

For red-work testing, use sanitized synthetic fixtures. Never point a test at a
live service or include real credentials.

## Next release gate

Before the next public release:

1. Obtain an explicit license decision.
2. Run all validation and private-content review.
3. Forward-test the Claude Desktop marketplace install and skill invocation
   path in a local Code session on native Windows.
4. Forward-test behavior on native Windows and a POSIX system against fresh
   disposable repositories without leaking expected answers into the prompts.
5. Confirm the intended branch and GitHub remote before pushing it.
