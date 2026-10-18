"""Offline checks for repository-health inventory."""
import importlib.util
import pathlib
import unittest
from unittest.mock import patch

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "repository_health.py"
spec = importlib.util.spec_from_file_location("repository_health", MODULE_PATH)
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class InventoryTests(unittest.TestCase):
    def test_full_tree_and_pr_count(self):
        repository = {"full_name": "OurChappy/example", "default_branch": "main",
                      "size": 12, "private": True}
        tree = {"truncated": False, "tree": [
            {"type": "blob", "path": "README.md", "size": 10},
            {"type": "blob", "path": "src/index.py", "size": 20},
            {"type": "blob", "path": ".github/workflows/ci.yml", "size": 30},
            {"type": "tree", "path": "src"},
        ]}
        def fake_api(path, token):
            if "/branches/" in path:
                return {"commit": {"sha": "abc123"}}
            if "/git/trees/" in path:
                return tree
            raise AssertionError(path)
        with patch.object(health, "api", side_effect=fake_api), patch.object(
                health, "pages", return_value=[{"number": 3}]):
            result = health.evaluate(repository, "unused")
        self.assertEqual(result["tracked_files"], 3)
        self.assertEqual(result["tracked_bytes"], 60)
        self.assertEqual(result["open_prs"], 1)
        self.assertEqual(result["head_sha"], "abc123")
        self.assertEqual(len(result["workflow_files"]), 1)
        self.assertTrue(result["has_readme"])
        self.assertEqual(result["ci_status"], "not_assessed")

    def test_truncated_tree_is_not_a_false_complete_count(self):
        repo = {"full_name": "OurChappy/example", "default_branch": "main"}
        with patch.object(health, "api", side_effect=[
                {"commit": {"sha": "abc123"}},
                {"truncated": True, "tree": []}]):
            with self.assertRaisesRegex(ValueError, "truncated"):
                health.evaluate(repo, "unused")

    def test_report_does_not_claim_health_score(self):
        report = {"generated_at": "2026-10-18T00:00:00Z",
                  "repositories": [], "errors": [
                      {"repository": "OurChappy/private", "error": "403 Forbidden"}]}
        rendered = health.render(report)
        self.assertIn("Unassessed repositories", rendered)
        self.assertIn("403 Forbidden", rendered)
        self.assertNotIn("100/100", rendered)


if __name__ == "__main__":
    unittest.main()
