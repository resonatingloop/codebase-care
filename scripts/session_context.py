#!/usr/bin/env python3
"""Emit the minimal automatic Codebase Care entry instruction."""

from __future__ import annotations


CONTEXT = (
    "Codebase Care is enabled. For any request that may modify repository "
    "code, configuration, schema, dependencies, tests, or observable behavior, "
    "invoke /codebase-care:maintain-codebase before editing and complete its "
    "verification stage before reporting success. Do not require the user to "
    "remember separate planning, security, testing, documentation, or handoff "
    "prompts. Keep audits read-only unless implementation is separately requested."
)


def main() -> int:
    print(CONTEXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

