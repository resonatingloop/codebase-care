# Codebase Care development

> **Role:** operational development procedure
> **Status:** current

## Requirements

- Python 3.10 or newer for deterministic scripts and tests.
- Claude Code with plugin validation support.

No third-party runtime dependency is required.

## Validate

From the repository root:

```text
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py .
claude plugin validate .
```

Exercise representative classifier paths:

```text
python3 scripts/classify_change.py --paths README.md styles/site.css
python3 scripts/classify_change.py --paths src/profile.js
python3 scripts/classify_change.py --paths supabase/migrations/001_auth.sql
```

## Test interactively

From the parent directory:

```text
claude --plugin-dir ./codebase-care
```

In a disposable target repository, ask for a normal feature change without
naming the skill. Confirm that Claude enters the lifecycle, explains the risk
floor, runs appropriate proof, and does not manufacture a documentation system.

For red-work testing, use sanitized synthetic fixtures. Never point a test at a
live service or include real credentials.

## Publication gate

Before public release:

1. Obtain an explicit license decision.
2. Initialize version control only with owner authorization.
3. Run all validation and private-content review.
4. Forward-test against fresh disposable repositories without leaking expected
   answers into the prompts.
5. Confirm the intended remote before assigning or pushing it.

