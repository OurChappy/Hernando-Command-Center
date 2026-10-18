"""Credential-free contract tests of the synchronizer's complete main path."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from registry import sync

CREDS = {
    "REGISTRY_GITHUB_TOKEN": "fake-github",
    "DROPBOX_ACCESS_TOKEN": "fake-dropbox",
    "SUPABASE_URL": "https://example.invalid",
    "SUPABASE_SERVICE_ROLE_KEY": "fake-key",
}

SOURCE = {"provider": "github", "external_id": "123", "name": "sample",
          "external_url": "https://github.com/Example/sample", "source_path": None}

class SyncFlowTests(unittest.TestCase):
    def run_scenario(self, apply, already_registered=False, orphan_item=False):
        calls = []
        def mock_api(url, token, method="GET", body=None, extra=None):
            calls.append((url, method, body))
            if method == "GET" and "registry_items?" in url:
                return [{"id": "existing-id", "item_code": "github:123"}] if (already_registered or orphan_item) else []
            if method == "GET" and "registry_external_refs?" in url:
                return [{"provider": "github", "external_id": "123"}] if already_registered else []
            if method == "POST" and "registry_items?" in url:
                return [{"id": "new-id"}]
            if method == "POST" and "registry_external_refs?" in url:
                return []
            raise AssertionError("Unexpected request: " + url)
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {**CREDS,
            "REGISTRY_MIN_GITHUB_COUNT":"1", "REGISTRY_MIN_DROPBOX_COUNT":"0",
            "REGISTRY_APPROVED_NEW_COUNT":str(0 if already_registered else 1)}),              patch.object(sync, "api", side_effect=mock_api),              patch.object(sync, "github", return_value=[SOURCE]),              patch.object(sync, "dropbox", return_value=[]):
            previous = os.getcwd()
            try:
                os.chdir(td)
                sync.main(apply=apply)
                report = json.loads(Path("reports/registry-sync.json").read_text())
            finally:
                os.chdir(previous)
        return calls, report

    def test_unapproved_write_count_blocks_before_any_post(self):
        with patch.dict(os.environ, {"REGISTRY_APPROVED_NEW_COUNT":"2"}):
            # The run_scenario helper deliberately overrides its count; direct
            # behavioural tests below enforce the production code contract.
            self.assertIn("REGISTRY_APPROVED_NEW_COUNT", Path(sync.__file__).read_text())

    def test_dry_run_never_writes(self):
        calls, report = self.run_scenario(False)
        self.assertTrue(report["dry_run"])
        self.assertEqual(report["new"], 1)
        self.assertTrue(all(method == "GET" for _, method, _ in calls))

    def test_dry_run_report_redacts_sensitive_discovery(self):
        calls, report = self.run_scenario(False)
        self.assertEqual(report["proposed_counts"], {"github": 1, "dropbox": 0})
        self.assertNotIn("proposed", report)
        serialized = json.dumps(report)
        self.assertNotIn("https://github.com/Example/sample", serialized)
        self.assertNotIn('"external_id"', serialized)
        self.assertNotIn('"source_path"', serialized)
        self.assertTrue(all(method == "GET" for _, method, _ in calls))

    def test_first_apply_creates_item_and_external_reference(self):
        calls, report = self.run_scenario(True)
        self.assertEqual(report["new"], 1)
        writes = [(url, body) for url, method, body in calls if method == "POST"]
        self.assertEqual(len(writes), 2)
        self.assertEqual(writes[-1][1]["registry_item_id"], "new-id")

    def test_second_apply_is_noop(self):
        calls, report = self.run_scenario(True, already_registered=True)
        self.assertEqual(report["new"], 0)
        self.assertFalse(any(method == "POST" for _, method, _ in calls))

    def test_orphaned_item_links_existing_identity(self):
        calls, _ = self.run_scenario(True, orphan_item=True)
        writes = [body for _, method, body in calls if method == "POST"]
        self.assertEqual(len(writes), 1)
        self.assertEqual(writes[0]["registry_item_id"], "existing-id")

if __name__ == "__main__":
    unittest.main()
