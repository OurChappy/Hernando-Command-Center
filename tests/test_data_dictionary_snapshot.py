import unittest
from tools.data_dictionary.snapshot import normalize

GOOD = {"schema":"public","table":"projects","column":"id","type":"uuid","nullable":False}

class SnapshotTests(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(normalize([GOOD], source="physical"), [GOOD])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            normalize([GOOD,GOOD],source="physical")
    def test_unknown_schema_rejected(self):
        with self.assertRaises(ValueError):
            normalize([{**GOOD,"schema":"auth"}],source="physical")
    def test_value_payload_rejected(self):
        with self.assertRaises(ValueError):
            normalize([{**GOOD,"secret":"password"}],source="physical")
    def test_nullable_type_rejected(self):
        with self.assertRaises(ValueError):
            normalize([{**GOOD,"nullable":"NO"}],source="physical")
    def test_missing_field_rejected(self):
        with self.assertRaises(ValueError):
            normalize([{k:v for k,v in GOOD.items() if k!="type"}],source="physical")
    def test_normalizes_order(self):
        another={**GOOD,"column":"name","type":"text"}
        self.assertEqual(normalize([another,GOOD],source="catalogued")[0]["column"],"id")

if __name__ == "__main__":
    unittest.main()
