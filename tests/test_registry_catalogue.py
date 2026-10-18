import unittest
from registry.catalogue_discovery import discover_candidates

class CandidateTests(unittest.TestCase):
    def test_verified_source_does_not_become_deployment(self):
        result=discover_candidates([{"provider":"github","external_id":"1351223629","external_url":"https://github.com/OurChappy/tafe-browser-mcp"}])
        self.assertEqual(len(result),1)
        self.assertIsNone(result[0]["deployed_identifier"])
        self.assertEqual(result[0]["registration_action"],"review_only")
    def test_unrelated_sources_ignored(self):
        self.assertEqual(discover_candidates([{"provider":"dropbox","external_id":"1351223629"},{"provider":"github","external_id":"other"}]),[])
    def test_stable_deterministic_candidates(self):
        data=[{"provider":"github","external_id":"1245312722"},{"provider":"github","external_id":"1351223629"}]
        self.assertEqual(discover_candidates(data),discover_candidates(list(reversed(data))))
if __name__=="__main__":unittest.main()
