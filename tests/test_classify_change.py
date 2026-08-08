from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "classify_change", ROOT / "scripts/classify_change.py"
)
assert SPEC and SPEC.loader
classify_change = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = classify_change
SPEC.loader.exec_module(classify_change)


class ClassifyChangeTests(unittest.TestCase):
    def test_docs_and_css_have_green_floor(self) -> None:
        result = classify_change.classify(["README.md", "styles/site.css"])
        self.assertEqual(result.risk_floor, "green")

    def test_ordinary_runtime_code_has_amber_floor(self) -> None:
        result = classify_change.classify(["src/profile.js"])
        self.assertEqual(result.risk_floor, "amber")

    def test_database_migration_has_red_floor(self) -> None:
        result = classify_change.classify(["supabase/migrations/001_profiles.sql"])
        self.assertEqual(result.risk_floor, "red")
        self.assertIn("database-change", {signal.category for signal in result.signals})

    def test_dynamic_execution_in_code_diff_has_red_floor(self) -> None:
        diff = """diff --git a/src/import.js b/src/import.js
+++ b/src/import.js
@@ -1,0 +2 @@
+const settings = eval(importedText)
"""
        result = classify_change.classify(["src/import.js"], diff)
        self.assertEqual(result.risk_floor, "red")
        self.assertIn(
            "dynamic-code-execution", {signal.category for signal in result.signals}
        )

    def test_html_sink_in_code_diff_has_red_floor(self) -> None:
        diff = """diff --git a/src/render.js b/src/render.js
+++ b/src/render.js
@@ -2 +2 @@
-node.textContent = phrase
+node.innerHTML = phrase
"""
        result = classify_change.classify(["src/render.js"], diff)
        self.assertEqual(result.risk_floor, "red")
        self.assertIn("html-execution-sink", {signal.category for signal in result.signals})

    def test_security_words_in_documentation_do_not_create_red_finding(self) -> None:
        diff = """diff --git a/docs/security.md b/docs/security.md
+++ b/docs/security.md
@@ -1,0 +2 @@
+Never pass untrusted text to eval() or innerHTML.
"""
        result = classify_change.classify(["docs/security.md"], diff)
        self.assertEqual(result.risk_floor, "green")

    def test_no_evidence_defaults_to_amber(self) -> None:
        result = classify_change.classify([])
        self.assertEqual(result.risk_floor, "amber")
        self.assertIn(
            "insufficient-change-evidence", {signal.category for signal in result.signals}
        )

    def test_collects_and_classifies_a_real_git_diff(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            source = repo / "src/render.js"
            source.parent.mkdir(parents=True)
            source.write_text("node.textContent = phrase;\n", encoding="utf-8")

            commands = (
                ("init", "-q"),
                ("config", "user.email", "fixture@example.invalid"),
                ("config", "user.name", "Fixture"),
                ("add", "."),
                ("commit", "-qm", "fixture baseline"),
            )
            for command in commands:
                subprocess.run(
                    ["git", "-C", str(repo), *command],
                    check=True,
                    capture_output=True,
                    text=True,
                )

            source.write_text("node.innerHTML = phrase;\n", encoding="utf-8")
            paths, diff_text, untracked = classify_change.collect_git_change(
                repo, base=None, staged=False
            )
            result = classify_change.classify(paths, diff_text)

            self.assertEqual(untracked, [])
            self.assertEqual(paths, ["src/render.js"])
            self.assertEqual(result.risk_floor, "red")
            self.assertIn(
                "html-execution-sink", {signal.category for signal in result.signals}
            )


if __name__ == "__main__":
    unittest.main()
