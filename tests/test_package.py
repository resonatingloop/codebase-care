from __future__ import annotations

import importlib.util
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()

