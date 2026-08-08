#!/usr/bin/env python3
"""Validate Codebase Care's portable package structure without dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Sequence


REQUIRED_FILES = (
    ".claude-plugin/plugin.json",
    "hooks/hooks.json",
    "scripts/session_context.py",
    "scripts/classify_change.py",
    "skills/maintain-codebase/SKILL.md",
    "skills/maintain-codebase/references/lifecycle.md",
    "skills/maintain-codebase/references/risk-routing.md",
    "skills/maintain-codebase/references/baseline.md",
    "skills/maintain-codebase/references/red-work.md",
    "skills/maintain-codebase/references/verification.md",
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\{\{[^}]+\}\}"),
)

PRIVATE_MARKERS = (
    "/home/",
    "/Users/",
)


def _markdown_targets(path: Path, text: str) -> list[Path]:
    targets: list[Path] = []
    for raw in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        target = raw.split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def check_package(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    manifest_path = root / ".claude-plugin/plugin.json"
    hooks_path = root / "hooks/hooks.json"

    for label, path in (("plugin manifest", manifest_path), ("hooks", hooks_path)):
        if not path.is_file():
            continue
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid {label} JSON: {error}")
            continue
        if label == "plugin manifest" and parsed.get("name") != "codebase-care":
            errors.append("plugin manifest name must be codebase-care")
        if label == "hooks" and "SessionStart" not in parsed.get("hooks", {}):
            errors.append("hooks configuration must define SessionStart")

    skill_path = root / "skills/maintain-codebase/SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        if not skill.startswith("---\n"):
            errors.append("skill must begin with YAML frontmatter")
        if "name: maintain-codebase" not in skill:
            errors.append("skill frontmatter must name maintain-codebase")
        if "description:" not in skill:
            errors.append("skill frontmatter must include a description")

    public_suffixes = {".md", ".json", ".py"}
    policy_source = Path(__file__).resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in public_suffixes:
            continue
        if any(part in {"__pycache__", ".git"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"non-UTF-8 public file: {path.relative_to(root)}: {error}")
            continue

        relative = path.relative_to(root)
        if path.resolve() != policy_source:
            for marker in PRIVATE_MARKERS:
                if marker in text:
                    errors.append(
                        f"private/project-specific marker {marker!r} in {relative}"
                    )

            if "assets" not in path.parts and "tests" not in path.parts:
                for pattern in PLACEHOLDER_PATTERNS:
                    if pattern.search(text):
                        errors.append(
                            f"unresolved placeholder {pattern.pattern!r} in {relative}"
                        )

        if path.suffix == ".md":
            for target in _markdown_targets(path, text):
                try:
                    target.relative_to(root)
                except ValueError:
                    errors.append(f"link escapes package from {relative}: {target}")
                    continue
                if not target.exists():
                    errors.append(f"broken local link from {relative}: {target.relative_to(root)}")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = check_package(args.root)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Checked Codebase Care package: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
