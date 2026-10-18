"""Release-gate checks: controlled write stays disabled by default."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
class AcceptanceGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = (ROOT / ".github/workflows/project-gpt-os-registry.yml").read_text()
        cls.bootstrap = (ROOT / ".github/workflows/project-gpt-os-bootstrap.yml").read_text()
    def test_write_requires_disabled_by_default_repository_switch(self):
        self.assertIn("vars.REGISTRY_WRITE_ENABLED || 'false'", self.registry)
        self.assertIn('"$REGISTRY_WRITE_ENABLED" != "true"', self.registry)
    def test_write_requires_confirmation_phrase(self):
        self.assertIn('"$CONFIRMATION" != \'APPLY-REGISTRY\'', self.registry)
    def test_no_automatic_write_workflow(self):
        self.assertNotIn("\n  schedule:", self.registry)
        self.assertNotIn("\n  push:", self.registry)
    def test_oidc_bootstrap_has_no_database_write_path(self):
        self.assertIn("id-token: write", self.bootstrap)
        self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY", self.bootstrap)
        self.assertNotIn("--apply", self.bootstrap)
        self.assertNotIn("\n  schedule:", self.bootstrap)
if __name__ == "__main__": unittest.main()
