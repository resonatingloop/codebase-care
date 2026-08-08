from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOOKS = json.loads((ROOT / "hooks/hooks.json").read_text(encoding="utf-8"))


class SessionContextTests(unittest.TestCase):
    def test_context_is_short_and_non_mutating(self) -> None:
        handler = HOOKS["hooks"]["SessionStart"][0]["hooks"][0]
        command = handler["command"]
        self.assertEqual(handler["type"], "command")
        self.assertTrue(command.startswith("echo "))
        context = command.removeprefix("echo ")
        self.assertLess(len(context.split()), 90)
        self.assertIn("invoke /codebase-care:maintain-codebase", context)
        self.assertIn("Keep audits read-only", context)
        self.assertNotIn("permission", context.lower())
        self.assertNotIn("python", command.lower())
        self.assertNotIn("CLAUDE_PLUGIN_ROOT", command)

        completed = subprocess.run(
            command,
            cwd=ROOT,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.stdout.strip(), context)
        self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
