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
    ".claude-plugin/marketplace.json",
    "hooks/hooks.json",
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
    marketplace_path = root / ".claude-plugin/marketplace.json"
    hooks_path = root / "hooks/hooks.json"
    parsed_json: dict[str, object] = {}

    for label, path in (
        ("plugin manifest", manifest_path),
        ("marketplace", marketplace_path),
        ("hooks", hooks_path),
    ):
        if not path.is_file():
            continue
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid {label} JSON: {error}")
            continue
        parsed_json[label] = parsed
        if label == "plugin manifest" and parsed.get("name") != "codebase-care":
            errors.append("plugin manifest name must be codebase-care")
        if label == "plugin manifest" and "hooks" in parsed:
            errors.append(
                "plugin manifest must not redeclare auto-discovered hooks/hooks.json"
            )
        if label == "marketplace" and parsed.get("name") != "resonatingloop":
            errors.append("marketplace name must be resonatingloop")
        if label == "hooks":
            session_start = parsed.get("hooks", {}).get("SessionStart")
            if not session_start:
                errors.append("hooks configuration must define SessionStart")
                continue
            try:
                handler = session_start[0]["hooks"][0]
            except (IndexError, KeyError, TypeError):
                errors.append("SessionStart must contain a hook handler")
                continue
            command = handler.get("command", "")
            if handler.get("type") != "command" or not command.startswith("echo "):
                errors.append("SessionStart must emit static context with a shell-neutral echo")
            if "python" in command.casefold() or "CLAUDE_PLUGIN_ROOT" in command:
                errors.append("SessionStart context must not depend on an interpreter or path")

    manifest = parsed_json.get("plugin manifest")
    marketplace = parsed_json.get("marketplace")
    if isinstance(manifest, dict) and isinstance(marketplace, dict):
        plugins = marketplace.get("plugins")
        entry = plugins[0] if isinstance(plugins, list) and len(plugins) == 1 else None
        if not isinstance(entry, dict) or entry.get("name") != "codebase-care":
            errors.append("marketplace must contain exactly one codebase-care plugin")
        else:
            source = entry.get("source")
            if source != "./":
                errors.append(
                    "marketplace plugin source must reuse the marketplace root with './'"
                )
            if entry.get("version") != manifest.get("version"):
                errors.append("marketplace and plugin versions must match")

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
