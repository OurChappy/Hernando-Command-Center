"""Security contract for GitHub OIDC inventory Edge Function."""
from pathlib import Path
import unittest

SRC=Path(__file__).resolve().parents[1]/"supabase/functions/project-gpt-os-inventory/index.ts"

class OIDCContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=SRC.read_text(encoding="utf-8")
    def test_verifies_signature_issuer_audience_and_algorithm(self):
        for required in ("createRemoteJWKSet","jwtVerify(","token.actions.githubusercontent.com","project-gpt-os-registry-reader",'algorithms: ["RS256"]'):
            self.assertIn(required,self.source)
    def test_enforces_immutable_repository_and_main_workflow(self):
        for required in ('1366820544','project-gpt-os-bootstrap.yml@refs/heads/main','payload.repository_id','payload.ref','payload.workflow_ref'):
            self.assertIn(required,self.source)
    def test_read_only_surface(self):
        self.assertIn('req.method !== "GET"',self.source)
        self.assertNotIn('.insert(',self.source)
        self.assertNotIn('.delete(',self.source)
        self.assertNotIn('.update(',self.source)
    def test_credentials_do_not_enter_response(self):
        self.assertIn('Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")',self.source)
        self.assertNotIn("Response.json({ key",self.source)
if __name__=="__main__":
    unittest.main()
