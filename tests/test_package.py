from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_package", ROOT / "scripts/check_package.py"
)
assert SPEC and SPEC.loader
check_package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_package)


class PackageTests(unittest.TestCase):
    def test_source_package_is_structurally_valid(self) -> None:
        self.assertEqual(check_package.check_package(ROOT), [])

    def test_rejects_redundant_remote_clone_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "codebase-care"
            shutil.copytree(
                ROOT,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            marketplace_path = package / ".claude-plugin/marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["source"] = {
                "source": "github",
                "repo": "resonatingloop/codebase-care",
            }
            marketplace_path.write_text(
                json.dumps(marketplace, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = check_package.check_package(package)

            self.assertIn(
                "marketplace plugin source must reuse the marketplace root with './'",
                errors,
            )

    def test_rejects_redeclared_auto_discovered_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "codebase-care"
            shutil.copytree(
                ROOT,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            manifest_path = package / ".claude-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["hooks"] = "./hooks/hooks.json"
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = check_package.check_package(package)

            self.assertIn(
                "plugin manifest must not redeclare auto-discovered hooks/hooks.json",
                errors,
            )

    def test_rejects_mismatched_host_versions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "codebase-care"
            shutil.copytree(
                ROOT,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            manifest_path = package / ".codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["version"] = "9.9.9"
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = check_package.check_package(package)

            self.assertIn("Claude and Codex plugin versions must match", errors)

    def test_rejects_nonlocal_codex_marketplace_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "codebase-care"
            shutil.copytree(
                ROOT,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__"),
            )
            marketplace_path = package / ".agents/plugins/marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["source"] = {
                "source": "local",
                "path": "./plugins/codebase-care",
            }
            marketplace_path.write_text(
                json.dumps(marketplace, indent=2) + "\n",
                encoding="utf-8",
            )

            errors = check_package.check_package(package)

            self.assertIn(
                "Codex marketplace plugin source must reuse the marketplace root with './'",
                errors,
            )


if __name__ == "__main__":
    unittest.main()
