"""Contract tests for private export schema and offline dashboard.

Do not commit actual registry exports into a public repository.
"""
import pathlib
import unittest
from registry.export import build_export

ROOT=pathlib.Path(__file__).resolve().parents[1]

class DashboardContract(unittest.TestCase):
    def test_dashboard_has_all_sections_and_file_input(self):
        page=(ROOT/"registry"/"dashboard.html").read_text(encoding="utf-8")
        for marker in ('data-tab="projects"','data-tab="sources"','data-tab="catalogue"','data-tab="threads"','type="file"','replaceChildren','textContent'):
            with self.subTest(marker=marker):
                self.assertIn(marker,page)
    def test_dashboard_has_no_live_credentials_or_network_requests(self):
        page=(ROOT/"registry"/"dashboard.html").read_text(encoding="utf-8")
        for forbidden in ("SUPABASE_SERVICE_ROLE_KEY","service_role","fetch(","XMLHttpRequest","localStorage"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden,page)
    def test_export_contract_with_realistic_records(self):
        payload=build_export(
            [{"project_code":"GOODTURN","name":"Goodturn","status":"Discovery"}],
            [{"id":"a","item_type":"source","item_code":"github:123","name":"Example","status":"Active","version":"1"}],
            [{"registry_item_id":"a","provider":"github","external_id":"123","external_url":"https://github.com/org/example","source_path":None}],
            [])
        self.assertEqual(set(("projects","sources","catalogue","threads"))-set(payload),set())
        self.assertEqual(tuple(len(payload[k]) for k in ("projects","sources","catalogue","threads")),(1,1,0,0))
        self.assertEqual(payload["sources"][0]["external_id"],"123")

if __name__=="__main__":
    unittest.main()
