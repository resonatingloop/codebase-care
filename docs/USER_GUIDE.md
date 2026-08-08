# Codebase Care user guide

> **Status:** experimental V1
> **Audience:** maintainers using Claude Code to work on an existing project

This guide is the shortest safe path from downloading Codebase Care to using
it for ordinary maintenance, a baseline review, or a security audit. You do
not need to write a plan before every request or remember separate prompts for
testing and documentation. Codebase Care routes those concerns after it is
loaded.

Windows Command Prompt is the primary shell in this guide. Commands labeled
**Windows CMD** go into the `C:\...>` window before Claude starts. Blocks that
begin with `/codebase-care:maintain-codebase` go into Claude after its welcome
screen appears. macOS and Linux alternatives are provided separately.

Codebase Care does not make every proposed change safe. Keep Claude Code's
normal permission prompts enabled, read commands before approving them, and
keep deployment, live migrations, credentials, production data, and financial
operations under human control.

## Before you begin

You need:

- Claude Code installed and signed in;
- Git, with Git for Windows recommended on native Windows;
- optionally, Python 3.10 or newer for the advisory classifier and package
  checks;
- a local copy of Codebase Care; and
- a local copy of the project you want Claude to inspect or change.

The startup hook itself does not require Python. Anthropic supports native
Windows Command Prompt and recommends Git for Windows so Claude has a Bash
tool; see the official [Claude Code installation guide](https://code.claude.com/docs/en/installation).

Using Git for the target project is strongly recommended. Before a change,
`git status --short --branch` gives you a visible starting point and makes it
much easier to distinguish your existing work from Claude's edits. Do not ask
Claude to erase a dirty working tree just to make the status clean.

## 1. Get Codebase Care

You only need to clone Codebase Care. Fork it if you intend to develop or
publish your own version.

1. Open the [Codebase Care repository on GitHub](https://github.com/resonatingloop/codebase-care).
2. Select **Code**, select **HTTPS**, and copy the repository address.
3. Open Command Prompt in the directory where you keep development tools.
4. Type `git clone `, including the space, paste the copied address, and press
   Enter.
5. Enter the new directory.

### Windows CMD

```text
git clone https://github.com/resonatingloop/codebase-care.git
cd /d codebase-care
cd
```

The last `cd` prints the complete directory path. Save it for the next section.

Validate the clone:

```text
claude plugin validate .
py -3 --version
py -3 scripts\check_package.py .
```

If Windows says `py` is not recognized, try these instead:

```text
python --version
python scripts\check_package.py .
```

Python should report version 3.10 or newer. Both Codebase Care checks should
finish without errors.

### macOS or Linux

```text
git clone https://github.com/resonatingloop/codebase-care.git
cd codebase-care
pwd
claude plugin validate .
python3 --version
python3 scripts/check_package.py .
```

Python should report version 3.10 or newer. Both Codebase Care checks should
finish without errors.

## 2. Start Claude inside the project you want to work on

This distinction matters: Codebase Care lives in its own folder, but Claude
must start inside the project being inspected.

### Windows CMD

1. Open Command Prompt.
2. Replace both example paths below with the real paths to the target project
   and Codebase Care. Keep the quotation marks when a path contains spaces.
3. Enter the target project, inspect its starting state, and launch Claude:

   ```text
   cd /d "C:\replace\with\target-project"
   git status --short --branch
   claude --plugin-dir "C:\replace\with\codebase-care"
   ```

### macOS or Linux

```text
cd "/path/to/target-project"
git status --short --branch
claude --plugin-dir "/path/to/codebase-care"
```

If the project does not use Git, say so when you prompt Claude and make a
backup before authorizing edits.

Keep Claude Code's ordinary permission checks enabled. Do not add
`--dangerously-skip-permissions`.

The `--plugin-dir` option loads Codebase Care for this Claude session only. Use
the same option each time you start a new session until a permanent install
method is distributed.

## 3. Confirm the plugin loaded

For the first session in a project, paste this at the Claude prompt:

```text
/codebase-care:maintain-codebase Orient to this repository without changing anything. Tell me the repository root, its current Git state, the instructions you found, and the initial risk floor. Stop after the orientation.
```

This is a smoke test, not a code audit. Claude should inspect the repository
and report back without editing it. After this succeeds, ordinary maintenance
requests should enter Codebase Care automatically; you do not normally need to
name the skill.

If an ordinary request does not show evidence of orientation and a green,
amber, or red risk floor, invoke `/codebase-care:maintain-codebase` explicitly.

## 4. Run the first read-only baseline

Use a baseline when the repository is unfamiliar, heavily AI-generated, or
has accumulated features faster than anyone has reviewed them. Paste:

```text
/codebase-care:maintain-codebase Run a read-only baseline inventory of this repository. Do not edit files, install packages, or change Git state. Map the main user-visible features and supporting subsystems, then propose one disposition for each: KEEP, KEEP DORMANT, REPAIR, REFACTOR, or RETIRE. Cite file paths and available tests. Separate verified evidence, inference, and unknowns. End with a small queue of independent next steps. Stop after the report.
```

Read the report before authorizing work. The five labels are proposals:

- **KEEP:** active and sufficiently supported;
- **KEEP DORMANT:** intentionally retained but not in ordinary use;
- **REPAIR:** intended behavior is broken, insecure, or drifted;
- **REFACTOR:** useful behavior works, but its structure obstructs safe work;
- **RETIRE:** the feature no longer earns its complexity or attack surface.

Do not answer a baseline with “do all of that.” Choose one independently
verifiable slice. Reachable dormant routes, integrations, and admin actions
still count as attack surface even when the interface no longer links to them.

## 5. Request an ordinary change

Ask normally, but bound one behavior clearly. This template is enough:

```text
Fix [one behavior]. Current behavior: [what happens now]. Expected behavior: [what should happen]. Keep [important unaffected behavior] unchanged. Use the repository's existing checks and tell me exactly what remains unverified.
```

Codebase Care should orient, state the risk floor and bounded surface, make the
change when authorized, run appropriate proof, and give a compact handoff.

Before accepting the result, check that the handoff tells you:

- what changed;
- the green, amber, or red risk floor;
- the consequential behavior or data path;
- the exact checks run and their results;
- anything still unverified; and
- the next safe action, if one exists.

“Looks correct,” “should work,” and “is secure” are not test results. If Claude
cannot run a relevant test or inspect the rendered behavior, that claim should
remain unverified.

## 6. Run a read-only security audit

Security-sensitive work is red. Start with a report, not a request to “find and
fix everything.” Paste:

```text
/codebase-care:maintain-codebase Run an authorized, local, read-only red-risk security audit of this repository. Do not modify files, install packages, use or print secret values, probe deployed services, or begin remediation. Map trust boundaries, privileged actions, enforcement points, and important lifecycle states. Trace untrusted input to HTML, URL, CSS, template, SQL, shell, file, and code-execution sinks; trace client requests to server-side authorization; and review authentication, sessions, database grants and policies, admin or moderation paths, deployment boundaries, and any payment, wallet, signing, or cryptocurrency functionality. For each finding, provide an ID, CONFIRMED/LIKELY/UNVERIFIED status, exact code evidence, prerequisites, impact, existing controls, remediation direction, and a future regression test. State coverage gaps and stop after the report.
```

The report may identify serious-looking code without proving it is exploitable.
It should say what was observed, what was inferred, and what could not be
verified. A clean static audit also does not prove the deployed system is
secure.

If compromise is suspected, stop treating the task as an ordinary code fix.
Preserve the available evidence and use a human-owned incident process for
containment, credential handling, affected services, and financial systems.

## 7. Fix one security finding in a separate operation

Do not continue directly from “audit everything” to “fix everything.” Review
the audit, choose one finding, and start a new Claude operation. A fresh session
is the easiest boundary. From the target project, start Claude again with the
same platform-specific command.

**Windows CMD:**

```text
claude --plugin-dir "C:\replace\with\codebase-care"
```

**macOS or Linux:**

```text
claude --plugin-dir "/path/to/codebase-care"
```

Then paste the exact finding into this template:

```text
/codebase-care:maintain-codebase Re-verify and fix only finding [finding ID and summary]. Treat this as a named red fix. Establish the expected security invariant, add a focused regression test when practical, implement the smallest complete fix, run the relevant project checks, and inspect the final diff for new sinks, widened permissions, fallback paths, and migration or recovery consequences. Do not fix adjacent findings, deploy, run live migrations, rotate credentials, access production data, or perform financial operations. Report what remains unverified and stop before release.
```

Repeat this process one finding at a time. Before release, have the completed
red fix reviewed independently by a qualified person or a separate review
agent that did not implement it. The implementing session's self-review is
useful evidence, but it is not independent approval.

## 8. Review before merging or deploying

For any material change:

1. Read Claude's summary and the actual diff.
2. Confirm that unrelated files and features stayed outside the change.
3. Confirm that every claimed test appears under **Verified** with an observed
   result.
4. Treat **Unverified** as work still owed, not a footnote.
5. Run any owner-only visual, device, staging, migration, backup, or recovery
   checks.
6. For red work, obtain independent review.
7. Merge or deploy through the project's normal human-controlled process.

Codebase Care never authorizes production access, deployment, live migrations,
credential rotation, or movement of funds on your behalf.

## 9. Update Codebase Care

If you cloned Codebase Care with Git, update it from its own directory, not
from the target project.

**Windows CMD:**

```text
cd /d "C:\replace\with\codebase-care"
git status --short --branch
git pull --ff-only
claude plugin validate .
py -3 scripts\check_package.py .
```

**macOS or Linux:**

```text
cd "/path/to/codebase-care"
git status --short --branch
git pull --ff-only
claude plugin validate .
python3 scripts/check_package.py .
```

If the first command shows local edits, stop and understand them before
pulling. Restart Claude with `--plugin-dir` after a successful update so the new
plugin files are loaded.

## Troubleshooting

### Claude says the skill is unknown

End the session, confirm the Codebase Care path, and restart Claude from the
target project with `claude --plugin-dir "C:\replace\with\codebase-care"` on
Windows CMD or `claude --plugin-dir "/path/to/codebase-care"` on macOS/Linux.
Then run `claude plugin validate .` inside the Codebase Care directory if the
problem continues.

### Windows reports that `py` is not recognized

Try `python --version`. If that also fails, install Python 3.10 or newer and
open a new Command Prompt. Claude can still receive the automatic startup
instruction without Python, but it cannot run Codebase Care's deterministic
classifier or package checker.

### Claude starts editing during a baseline or audit

Reject the write or command permission and tell Claude to stop. Inspect
`git status --short` and `git diff` before doing anything else. A baseline or
red audit is read-only; start a fresh session if that boundary was lost.

### The automatic lifecycle is not obvious

Invoke `/codebase-care:maintain-codebase` explicitly at the beginning of the
request. Model invocation is helpful automation, not a guarantee.

### The repository has no useful tests

Claude should report the affected behavior as unverified and propose the
smallest relevant proof. Do not treat unrelated linting, a successful build,
or model confidence as a substitute for a behavior-specific check.

### A command or permission request is unclear

Do not approve it until Claude explains what the command reads or changes, why
it is needed, and how the result will be checked. You can always say no and ask
for a narrower operation.
