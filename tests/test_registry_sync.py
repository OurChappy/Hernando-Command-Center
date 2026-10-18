import unittest
from registry.sync import reconcile

class ReconcileTests(unittest.TestCase):
    def test_existing_ids_not_duplicated(self):
        before=[{"provider":"github","external_id":"123"}]
        candidates=[{"provider":"github","external_id":"123","name":"renamed"},{"provider":"github","external_id":"124","name":"new"}]
        self.assertEqual([x["external_id"] for x in reconcile(before,candidates)],["124"])
    def test_repeat_is_noop(self):
        found=[{"provider":"dropbox","external_id":"id:abc"}]
        self.assertEqual(reconcile(reconcile([],found),found),[])
    def test_duplicate_discovery_collapses(self):
        item={"provider":"github","external_id":"123"}
        self.assertEqual(len(reconcile([],[item,item])),1)
    def test_provider_part_of_identity(self):
        self.assertEqual(len(reconcile([], [{"provider":"github","external_id":"1"},{"provider":"dropbox","external_id":"1"}])),2)

if __name__=="__main__": unittest.main()
