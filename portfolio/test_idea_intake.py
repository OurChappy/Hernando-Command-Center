import copy
import unittest
from idea_intake import propose

I = {"title":"Example idea","outcome":"Create proposals","repository_id":123,
"repository":"OurChappy/Hernando-Command-Center","project_id":"p","registry_item_id":"r",
"evidence":[{"url":"https://github.com/OurChappy/Hernando-Command-Center/issues/10","classification":"verified"}],
"tasks":[{"id":"T1","title":"Prepare","acceptance":["validated"]},
{"id":"T2","title":"Test","depends_on":["T1"],"acceptance":["passing"]}]}
INV = {"repositories":[{"id":123,"full_name":I["repository"],"project_id":"p","registry_item_id":"r"}],"existing_issues":[]}

class Tests(unittest.TestCase):
    def test_deterministic(self): self.assertEqual(propose(I,INV),propose(I,INV))
    def test_no_writes(self): self.assertEqual(propose(I,INV)["external_writes"],0)
    def test_task_count(self): self.assertEqual(len(propose(I,INV)["tasks"]),2)
    def test_unknown_mapping(self): self.assertEqual(propose(I,{"repositories":[]})["status"],"hold_mapping")
    def test_duplicate(self):
        inv=copy.deepcopy(INV)
        inv["existing_issues"]=[{"repository":I["repository"],"title":I["title"],"url":"https://github.com/example"}]
        self.assertEqual(propose(I,inv)["status"],"reuse_or_review")
    def test_cycle(self):
        i=copy.deepcopy(I); i["tasks"][0]["depends_on"]=["T2"]
        with self.assertRaisesRegex(ValueError,"cycle"): propose(i,INV)
    def test_missing_dependency(self):
        i=copy.deepcopy(I); i["tasks"][0]["depends_on"]=["absent"]
        with self.assertRaisesRegex(ValueError,"Unknown dependency"): propose(i,INV)
    def test_duplicate_task(self):
        i=copy.deepcopy(I); i["tasks"][1]["id"]="T1"
        with self.assertRaisesRegex(ValueError,"duplicate"): propose(i,INV)
    def test_invalid_repo(self):
        i=copy.deepcopy(I); i["repository"]="bad"
        with self.assertRaisesRegex(ValueError,"repository"): propose(i,INV)
    def test_empty_evidence(self):
        i=copy.deepcopy(I); i["evidence"]=[{"classification":"verified"}]
        with self.assertRaisesRegex(ValueError,"Evidence"): propose(i,INV)
    def test_string_dependency_rejected(self):
        i=copy.deepcopy(I); i["tasks"][1]["depends_on"]="T1"
        with self.assertRaisesRegex(ValueError,"dependencies"): propose(i,INV)
    def test_nonstring_acceptance_rejected(self):
        i=copy.deepcopy(I); i["tasks"][0]["acceptance"]=[12]
        with self.assertRaisesRegex(ValueError,"acceptance"): propose(i,INV)
    def test_missing_acceptance(self):
        i=copy.deepcopy(I); i["tasks"][0]["acceptance"]=[]
        with self.assertRaisesRegex(ValueError,"acceptance"): propose(i,INV)

if __name__=="__main__":
    unittest.main()
