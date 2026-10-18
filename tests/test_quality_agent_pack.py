"""Offline tests for quality agent pack; no external network or credentials."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ["product-challenger","architecture-reviewer","qa-security-reviewer","release-evidence-auditor"]
class QualityPack(unittest.TestCase):
    def test_agent_contracts(self):
        for name in AGENTS:
            with self.subTest(name=name):
                p=ROOT / ".github/agents" / (name+".md")
                self.assertTrue(p.is_file())
                s=p.read_text()
                for term in ("AGENTS.md","VERIFIED","HOLD","FAIL","Read-only"):
                    self.assertIn(term,s)
    def test_review_schema(self):
        schema=json.loads((ROOT/"governance/quality/review-report.schema.json").read_text())
        self.assertEqual(set(schema["properties"]["verdict"]["enum"]),{"PASS","HOLD","FAIL"})
        self.assertEqual(set(schema["properties"]["agent"]["enum"]),set(AGENTS))
        self.assertFalse(schema["additionalProperties"])
    def test_risk_matrix(self):
        s=(ROOT/"governance/quality/review-gates.md").read_text()
        for t in ("Low","Medium","High","Protected","owner approval"):
            self.assertIn(t,s)
    def test_workflow_is_read_only(self):
        s=(ROOT/".github/workflows/quality-agent-contract-ci.yml").read_text()
        self.assertIn("contents: read",s)
        self.assertNotIn("id-token: write",s)
        self.assertNotIn("secrets.",s)
        self.assertNotIn("schedule:",s)
if __name__=="__main__": unittest.main()
