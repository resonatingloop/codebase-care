# Codebase Care user guide

> **Status:** experimental V1
> **Audience:** maintainers using Claude Code, plus Codex CLI evaluators

This guide is the shortest safe path from installing Codebase Care to using it
for ordinary maintenance, a baseline review, or a security audit. You do not
need to write a plan before every request or remember separate prompts for
testing and documentation. Codebase Care routes those concerns after it is
loaded.

This guide uses **Claude Desktop's Code tab** as the primary interface. Claude
Code also has other interfaces with different plugin controls:

- **Claude Desktop:** you are in the Claude app's **Code** tab. Use the **+**
  button beside the prompt and select **Plugins**.
- **Terminal CLI:** Claude is running inside Command Prompt, PowerShell, Windows
  Terminal, Terminal, or another shell. Use the `/plugin` slash commands below.
- **VS Code:** Claude appears in a panel inside VS Code. Use that panel's plugin
  manager or the same slash commands when they are available.

Commands beginning with `/` go into Claude's prompt, after Claude Code has
started. They do not go directly into Command Prompt, PowerShell, bash, or zsh.
Do not use Claude Desktop's ordinary Chat or Cowork surface for this setup. Use
a local or SSH session in the **Code** tab; this marketplace plugin is not
available in a Desktop cloud or WSL session.

Codebase Care does not make every proposed change safe. Keep Claude Code's
normal permission prompts enabled, read commands before approving them, and
keep deployment, live migrations, credentials, production data, and financial
operations under human control.

## Before you begin

You need Claude Code signed in and a local copy of the target project. Git is
strongly recommended. Python 3.10 or newer is optional and is used only by the
advisory classifier and package checks.

You do not need to clone Codebase Care to use it. Claude Code installs a cached
copy through the marketplace. If you already cloned this repository, you may
keep it for inspection or development, but cloning or opening it does not
install the plugin.

The startup hook itself does not require Python. See Anthropic's official
[plugin guide](https://code.claude.com/docs/en/discover-plugins) and
[Desktop guide](https://code.claude.com/docs/en/desktop) for the current
interface behavior.

Using Git for the target project is strongly recommended. Before a change,
`git status --short --branch` gives you a visible starting point and makes it
much easier to distinguish your existing work from Claude's edits. Do not ask
Claude to erase a dirty working tree just to make the status clean.

## 1. Open the project you actually want Claude to work on

- **Claude Desktop:** open **Code**, start a local session, and select the root
  folder of the application or website. An SSH session also supports plugins;
  a cloud or WSL session does not.
- **Terminal CLI:** open a shell in the root folder of the application or
  website, then run `claude`.
- **VS Code:** open the target project's root folder, then open the Claude Code
  panel.

Check the working folder before continuing. It should be the project being
maintained, not the cloned `codebase-care` repository. Opening the wrong folder
means Claude will inspect the wrong repository. If the target project does not
use Git, tell Claude and make a backup before authorizing edits.

Keep Claude Code's ordinary permission checks enabled. Leave automatic edit
acceptance off until you are comfortable reviewing its diffs.

## 2. Install Codebase Care

### Claude Desktop Code tab

1. Use a local or SSH Code session in the target project.
2. Click **+** beside the prompt box.
3. Select **Plugins → Manage plugins** and check whether **Codebase Care** is
   already present from the user-scope VS Code installation on this computer.
4. If it is absent, select **Plugins → Add plugin**.
5. Find **Codebase Care** in the configured `resonatingloop` marketplace and
   install it at user scope.

If `resonatingloop` is not among the configured marketplaces, use the terminal
fallback immediately below. If the **+** button or plugin browser is absent,
confirm that this is a local or SSH Code session rather than Chat, Cowork,
cloud, or WSL.

### Terminal fallback for adding the marketplace

Open Command Prompt, PowerShell, or another terminal in the target project and
run `claude`. After Claude Code has started, enter these at Claude's prompt one
at a time:

```text
/plugin marketplace add resonatingloop/codebase-care
/plugin install codebase-care@resonatingloop
/reload-plugins
```

Choose **User scope** during installation so the plugin is available across
your projects. If the install summary says the plugin is already active, the
reload is optional.

### VS Code

Open the Claude Code panel in the target project. Use its plugin manager to add
the marketplace `resonatingloop/codebase-care`, install **Codebase Care** at
user scope, and reload plugins if prompted. The marketplace install path has
been owner-tested in VS Code on Windows.

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
is the easiest boundary. Start a new Claude Code conversation or session while
keeping the same target project as its working folder.

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

In the terminal CLI, enter:

```text
/plugin marketplace update resonatingloop
/reload-plugins
```

In Claude Desktop or VS Code, use the plugin manager to refresh the
`resonatingloop` marketplace and apply the update, then reload or restart if
prompted. Pulling a separate Git clone does not update Claude Code's installed
copy; marketplace plugins are cached separately.

## Troubleshooting

### Claude says the skill is unknown

In the terminal CLI, type `/plugin`, open **Installed**, and confirm that
`codebase-care@resonatingloop` is enabled. Check the **Errors** tab, then run
`/reload-plugins` if needed. In Desktop or VS Code, use that interface's plugin
manager. Start a new conversation after reloading.

### Codebase Care does not appear in the plugin list

In the terminal CLI, type `/plugin`, switch to **Marketplaces**, and confirm
that `resonatingloop/codebase-care` is present. If it is absent, run
`/plugin marketplace add resonatingloop/codebase-care` again. Desktop users
who cannot see the marketplace should use that one-time terminal route.

### You cloned the repository but Claude cannot see the skill

A clone is source code, not an installed Claude Code plugin. Install it through
the marketplace; you may delete or keep the clone independently.

### Claude reports that Python is unavailable

The automatic lifecycle still works. Claude should report the deterministic
classifier as unavailable rather than treating it as proof. Install Python
3.10 or newer only if you want that advisory check.

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

## Maintainer and local-development appendix

Cloning is useful when changing Codebase Care itself or testing an unpublished
version. From the parent directory, load the clone for one terminal session:

**Windows CMD:**

```text
claude --plugin-dir .\codebase-care
```

**macOS or Linux:**

```text
claude --plugin-dir ./codebase-care
```

This appendix is not required for ordinary marketplace installation.

## Codex CLI evaluation appendix

This is the maintainer/evaluator path. The friend-facing instructions above
remain Claude Desktop-first, but Codex runs the same skill and lifecycle.

From the Codebase Care clone, run these as terminal commands:

```text
codex plugin marketplace add .
codex plugin add codebase-care@resonatingloop
codex plugin list --json
```

Then open a new terminal in the target repository and run `codex`. Inside the
new Codex session:

1. Enter `/plugins` and confirm `codebase-care@resonatingloop` is enabled.
2. Enter `/hooks`, inspect the static Codebase Care SessionStart command, and
   trust it only if it matches the installed source.
3. Run this smoke test:

```text
$codebase-care:maintain-codebase Orient to this repository without changing anything. Tell me the repository root, its current Git state, the instructions you found, and the initial risk floor. Stop after the orientation.
```

For the longer prompts in this guide, replace the Claude prefix
`/codebase-care:maintain-codebase` with the Codex skill prefix
`$codebase-care:maintain-codebase`; the rest of each prompt is unchanged.

Installing or updating a plugin does not retrofit it into the current Codex
conversation, so start a new session. Codex plugins currently load in the CLI,
not the IDE extension.
