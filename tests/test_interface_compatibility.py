"""Issue #20 offline compatibility gates against draft-module contracts.

These tests are self-contained and deliberately do not import unmerged PR code.
They enforce explicit adapter boundaries, not functional integration acceptance.
"""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"governance"/"quality"/"interface-contract-v1.json"

def validate_boundary(intake, dispatcher, worksheet):
    if intake.get("schema_version") != 1:
        raise ValueError("intake_version")
    if dispatcher.get("schema_version") != 1:
        raise ValueError("dispatcher_version")
    if worksheet.get("schema_version") != "1.0.0":
        raise ValueError("worksheet_version")
    if intake.get("external_writes") != 0 or worksheet.get("external_writes") != 0:
        raise ValueError("external_writes")
    if not intake.get("repository") or intake.get("status") != "proposal_only":
        raise ValueError("intake_unverified")
    if not dispatcher.get("source_observed_at"):
        raise ValueError("source_provenance_missing")
    if any(t.get("status")=="selected" and not t.get("head_sha") for t in dispatcher.get("tasks", [])):
        raise ValueError("admitted_without_sha")
    return {"status":"contract_candidate","mode":"offline","writes":0}

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.c=json.loads(CONTRACT.read_text())
        self.intake={"schema_version":1,"external_writes":0,"repository":"OurChappy/Hernando-Command-Center","status":"proposal_only"}
        self.dispatcher={"schema_version":1,"source_observed_at":"2026-10-18T00:00:00Z","tasks":[]}
        self.worksheet={"schema_version":"1.0.0","external_writes":0}
    def test_contract_metadata(self):
        self.assertEqual(self.c["version"],"1.0")
        self.assertEqual(self.c["source_prs"],[2,14,15])
        self.assertEqual(self.c["integration_status"],"proposed")
    def test_good_boundary_is_only_candidate(self):
        self.assertEqual(validate_boundary(self.intake,self.dispatcher,self.worksheet)["status"],"contract_candidate")
    def test_schema_mismatch_rejected(self):
        for field in ("intake","dispatcher","worksheet"):
            with self.subTest(field=field):
                values=[dict(self.intake),dict(self.dispatcher),dict(self.worksheet)]
                index={"intake":0,"dispatcher":1,"worksheet":2}[field]
                values[index]["schema_version"]="1.0.0" if index!=2 else 1
                with self.assertRaises(ValueError):
                    validate_boundary(*values)
    def test_missing_provenance_rejected(self):
        self.dispatcher.pop("source_observed_at")
        with self.assertRaisesRegex(ValueError,"provenance"):
            validate_boundary(self.intake,self.dispatcher,self.worksheet)
    def test_unverified_intake_rejected(self):
        self.intake["status"]="hold_mapping"
        with self.assertRaises(ValueError):
            validate_boundary(self.intake,self.dispatcher,self.worksheet)
    def test_missing_sha_rejected(self):
        self.dispatcher["tasks"]=[{"status":"selected"}]
        with self.assertRaises(ValueError):
            validate_boundary(self.intake,self.dispatcher,self.worksheet)
    def test_external_write_rejected(self):
        self.worksheet["external_writes"]=1
        with self.assertRaises(ValueError):
            validate_boundary(self.intake,self.dispatcher,self.worksheet)

if __name__=="__main__":
    unittest.main()
