"""Synthetic positive, negative and regression tests; never needs credentials."""
import unittest
from tools.data_dictionary.drift import compare

def row(schema="public", table="projects", column="id", type="uuid", nullable=False):
    return dict(schema=schema, table=table, column=column, type=type, nullable=nullable)

class DriftTests(unittest.TestCase):
    def test_equal(self):
        self.assertFalse(compare([row()], [row()])["drift"])
    def test_missing(self):
        self.assertEqual(compare([row()], [])["missing_in_dictionary"], [["public", "projects", "id"]])
    def test_stale(self):
        self.assertEqual(compare([], [row()])["stale_in_dictionary"], [["public", "projects", "id"]])
    def test_type_change(self):
        self.assertEqual(len(compare([row(type="text")], [row()])["attribute_drift"]), 1)
    def test_nullable_change(self):
        self.assertEqual(len(compare([row(nullable=True)], [row()])["attribute_drift"]), 1)
    def test_duplicate_identity_fails(self):
        with self.assertRaises(ValueError):
            compare([row(),row()], [])
    def test_order_independent(self):
        a=[row(),row(column="name",type="text")]
        self.assertFalse(compare(a,list(reversed(a)))["drift"])

if __name__ == "__main__":
    unittest.main()
