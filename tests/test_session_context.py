from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "session_context", ROOT / "scripts/session_context.py"
)
assert SPEC and SPEC.loader
session_context = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(session_context)


class SessionContextTests(unittest.TestCase):
    def test_context_is_short_and_non_mutating(self) -> None:
        context = session_context.CONTEXT
        self.assertLess(len(context.split()), 90)
        self.assertIn("invoke /codebase-care:maintain-codebase", context)
        self.assertIn("Keep audits read-only", context)
        self.assertNotIn("permission", context.lower())


if __name__ == "__main__":
    unittest.main()

