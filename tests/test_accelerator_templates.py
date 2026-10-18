"""Offline contract checks for OurChappy AI Engineering Accelerator templates."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AcceleratorTemplates(unittest.TestCase):
    def test_expected_assets_exist(self):
        paths = ["AGENTS.md", ".github/copilot-instructions.md",
                 ".github/ISSUE_TEMPLATE/engineering-task.yml",
                 ".github/PULL_REQUEST_TEMPLATE.md",
                 ".github/prompts/implement-issue.prompt.md",
                 ".github/prompts/debug-failing-ci.prompt.md",
                 ".github/prompts/review-pr.prompt.md",
                 ".github/workflows/accelerator-template-ci.yml"]
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
                self.assertTrue((ROOT / path).read_text().strip())
    def test_prompt_contract(self):
        for name in ("implement-issue", "debug-failing-ci", "review-pr"):
            text = (ROOT / ".github/prompts" / (name + ".prompt.md")).read_text()
            self.assertTrue(text.startswith("---\n"))
            self.assertIn("AGENTS.md", text)
            self.assertIn("SHA", text)
            self.assertIn("deploy", text.lower())
    def test_safety_gates(self):
        agent = (ROOT / "AGENTS.md").read_text().lower()
        self.assertIn("three", agent)
        self.assertIn("production", agent)
        self.assertIn("no merge", agent)
        workflow = (ROOT / ".github/workflows/accelerator-template-ci.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertNotIn("id-token: write", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertNotIn("schedule:", workflow)
    def test_templates_require_evidence(self):
        pr = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text()
        issue = (ROOT / ".github/ISSUE_TEMPLATE/engineering-task.yml").read_text()
        self.assertIn("CI URLs", pr)
        for field in ("parent", "outcome", "dependencies", "acceptance", "evidence"):
            self.assertIn("id: " + field, issue)
if __name__ == "__main__":
    unittest.main()
