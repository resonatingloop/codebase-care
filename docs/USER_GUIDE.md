# Codebase Care user guide

> **Status:** experimental V1
> **Audience:** maintainers using Claude Code to work on an existing project

This guide is the shortest safe path from installing Codebase Care in VS Code
to using it for ordinary maintenance, a baseline review, or a security audit.
You do not need to write a plan before every request or remember separate
prompts for testing and documentation. Codebase Care routes those concerns
after it is loaded.

The Claude Code extension in VS Code is the primary interface in this guide.
Anything beginning with `/plugin`, `/plugins`, `/reload-plugins`, or
`/codebase-care:maintain-codebase` goes into the Claude prompt box inside VS
Code. No Command Prompt window is required for ordinary installation or use.

Codebase Care does not make every proposed change safe. Keep Claude Code's
normal permission prompts enabled, read commands before approving them, and
keep deployment, live migrations, credentials, production data, and financial
operations under human control.

## Before you begin

You need:

- VS Code 1.98 or newer;
- the Claude Code extension installed and signed in;
- the target project's folder opened in VS Code;
- Git for the target project, strongly recommended;
- optionally, Python 3.10 or newer for the advisory classifier and package
  checks.

You do not need to clone Codebase Care to use it. The VS Code extension installs
its own cached copy. If you already cloned the repository, you may keep it for
inspection or development, but opening that clone does not install the plugin.

The startup hook itself does not require Python. See Anthropic's official
[Claude Code VS Code guide](https://code.claude.com/docs/en/ide-integrations)
for extension requirements and interface basics.

Using Git for the target project is strongly recommended. Before a change,
`git status --short --branch` gives you a visible starting point and makes it
much easier to distinguish your existing work from Claude's edits. Do not ask
Claude to erase a dirty working tree just to make the status clean.

## 1. Open the project you actually want Claude to work on

1. In VS Code, select **File → Open Folder**.
2. Choose the root folder of the application or website being maintained.
3. Check the Explorer sidebar. It should show that project, not the cloned
   `codebase-care` repository.
4. Open Claude Code using the Spark icon in the editor toolbar or Activity Bar.

Each Claude conversation uses the folder or workspace currently open in VS
Code. Opening the wrong folder means Claude will inspect the wrong repository.
If the target project does not use Git, tell Claude and make a backup before
authorizing edits.

Keep Claude Code's ordinary permission checks enabled. Leave automatic edit
acceptance off until you are comfortable reviewing its diffs.

## 2. Install Codebase Care inside the Claude panel

1. Type `/plugins` in the Claude prompt box and press Enter.
2. Open the **Marketplaces** tab.
3. Add this GitHub repository as a marketplace:

   ```text
   resonatingloop/codebase-care
   ```

4. Return to the **Plugins** tab and search for **Codebase Care**.
5. Select **Install for you**. This makes it available in all of your projects
   without adding plugin settings to the target repository.
6. When prompted, restart Claude Code. You can instead type:

   ```text
   /reload-plugins
   ```

If the graphical marketplace flow is unavailable, enter these commands one at
a time in the Claude prompt box:

```text
/plugin marketplace add resonatingloop/codebase-care
/plugin install codebase-care@resonatingloop
/reload-plugins
```

These are Claude slash commands, not Windows shell commands.

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
is the easiest boundary. In the Claude Code Activity Bar, start a new
conversation while the same target project remains open.

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

1. Type `/plugins` in the Claude prompt box.
2. Open **Marketplaces** and refresh the `resonatingloop` marketplace.
3. Return to **Plugins**. If Codebase Care shows an update, install it.
4. Type `/reload-plugins` or restart Claude Code.

Pulling a separate Git clone does not update the extension's installed copy.
Marketplace plugins are cached separately by Claude Code.

## Troubleshooting

### Claude says the skill is unknown

Type `/plugins`, confirm that `codebase-care@resonatingloop` appears under
installed plugins and is enabled, then type `/reload-plugins`. Start a new
conversation after reloading.

### Codebase Care does not appear in the plugin list

Open `/plugins`, switch to **Marketplaces**, confirm that
`resonatingloop/codebase-care` is present, and use its refresh control. If it
is absent, add it again and reload plugins.

### You cloned the repository but Claude cannot see the skill

A clone is source code, not an installed VS Code plugin. Install it through
`/plugins`; you may delete or keep the clone independently.

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

This appendix is not required for ordinary VS Code installation.
