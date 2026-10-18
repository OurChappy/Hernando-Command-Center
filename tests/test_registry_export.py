import unittest
from registry.export import build_export

class ExportTests(unittest.TestCase):
    def test_redacts_internal_metadata_and_preserves_identity(self):
        projects=[{"project_code":"GOODTURN","name":"Goodturn","status":"Discovery","owner_id":"private-owner"}]
        items=[
            {"id":"uuid-source","item_type":"source","item_code":"github:123","name":"example","status":"Active","version":"1","metadata":{"secret":"never-export"}},
            {"id":"uuid-agent","item_type":"agent","item_code":"AGT-004","name":"Agent","status":"Design","version":"0.1","metadata":{"private":"no"}}
        ]
        refs=[{"registry_item_id":"uuid-source","provider":"github","external_id":"123","external_url":"https://github.com/owner/example","source_path":None}]
        threads=[{"name":"Verified","provider":"chatgpt","external_id":"confirmed-id","status":"Active","content":"private"}]
        snapshot=build_export(projects,items,refs,threads)
        self.assertEqual(len(snapshot["sources"]),1)
        self.assertEqual(snapshot["sources"][0]["external_id"],"123")
        self.assertEqual(snapshot["catalogue"][0]["item_code"],"AGT-004")
        self.assertEqual(snapshot["threads"][0]["external_id"],"confirmed-id")
        self.assertNotIn("private-owner",str(snapshot))
        self.assertNotIn("never-export",str(snapshot))
    def test_empty_sources_and_unmatched_refs(self):
        snap=build_export([],[],[{"registry_item_id":"unknown","provider":"github","external_id":"orphan"}],[])
        self.assertEqual(snap["sources"],[])
        self.assertEqual(snap["threads"],[])

if __name__=="__main__":
    unittest.main()
