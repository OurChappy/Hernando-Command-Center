"""Real cross-module integration tests using the original unmerged source modules."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name, ROOT/path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

intake=load("candidate_intake","portfolio/idea_intake.py")
planner=load("candidate_dispatcher","portfolio/dispatcher.py")
exporter=load("candidate_exporter","portfolio/v4/exporter.py")

SNAPSHOT={"schema_version":1,"observed_at":"2026-10-18T00:00:00Z",
 "projects":[{"id":"project-1"}],
 "registry_items":[{"id":"item-1","project_id":"project-1","status":"verified"}],
 "registry_external_refs":[{"registry_item_id":"item-1","provider":"github","external_id":"101"}],
 "registry_dependencies":[]}
IDEA={"title":"Example","outcome":"Generate a verified proposal",
 "repository_id":101,"repository":"OurChappy/Hernando-Command-Center",
 "project_id":"project-1","registry_item_id":"item-1",
 "evidence":[{"url":"https://github.com/OurChappy/Hernando-Command-Center/issues/20","classification":"verified"}],
 "tasks":[{"id":"T1","title":"Prepare","acceptance":["verified tests"]}]}
INVENTORY={"repositories":[{"id":101,"full_name":IDEA["repository"],
 "project_id":"project-1","registry_item_id":"item-1"}],"existing_issues":[]}

def enrich(proposal, *, head_sha=None, checks=None):
    """Explicit synthetic-only handoff; never infer verification from proposal."""
    if proposal["status"]!="proposal_only":
        raise ValueError("proposal held or duplicated")
    return [{"id":t["id"],"lane":"build","project_id":"project-1",
      "repository_id":"101","head_sha":head_sha,"required_checks":["unit"],
      "ci":{"sha":head_sha,"checks":checks or {}},"depends_on":t["depends_on"]}
      for t in proposal["tasks"]]

class RealIntegration(unittest.TestCase):
    def test_intake_proposal_to_dispatcher_requires_ci(self):
        proposal=intake.propose(IDEA,INVENTORY)
        self.assertEqual(proposal["external_writes"],0)
        held=planner.plan(SNAPSHOT,enrich(proposal,head_sha="sha-1"))
        self.assertEqual(held["selected"],[])
        self.assertEqual(held["tasks"][0]["reason"],"ci_unverified")
        selected=planner.plan(SNAPSHOT,enrich(proposal,head_sha="sha-1",checks={"unit":"success"}))
        self.assertEqual(len(selected["selected"]),1)
        self.assertEqual(selected["selected"][0]["registry_item_id"],"item-1")
        self.assertEqual(selected["mode"],"plan_only")
    def test_missing_identity_blocks(self):
        broken=dict(INVENTORY,repositories=[])
        proposal=intake.propose(IDEA,broken)
        self.assertEqual(proposal["status"],"hold_mapping")
        with self.assertRaises(ValueError):enrich(proposal,head_sha="abc")
    def test_duplicate_proposal_blocks(self):
        existing=dict(INVENTORY,existing_issues=[{"repository":IDEA["repository"],"title":IDEA["title"]}])
        self.assertEqual(intake.propose(IDEA,existing)["status"],"reuse_or_review")
        with self.assertRaises(ValueError):enrich(intake.propose(IDEA,existing))
    def test_stale_ci_blocks(self):
        proposal=intake.propose(IDEA,INVENTORY)
        row=enrich(proposal,head_sha="sha-1",checks={"unit":"success"})
        row[0]["ci"]["sha"]="stale"
        self.assertEqual(planner.plan(SNAPSHOT,row)["tasks"][0]["reason"],"ci_unverified")
    def test_schema_and_pdf_real_exporter(self):
        import fitz
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"demo.pdf"
            doc=fitz.open()
            for stage in range(1,11):
                page=doc.new_page()
                for j,suffix in enumerate(("problem_or_source","evidence_links")):
                    w=fitz.Widget()
                    w.field_name=f"stage_{stage:02d}_{suffix}"
                    w.field_type=fitz.PDF_WIDGET_TYPE_TEXT
                    w.rect=fitz.Rect(20,20+40*j,300,50+40*j)
                    w.field_value=f"value-{stage}-{j}"
                    page.add_widget(w)
            doc.save(p);doc.close()
            cycle,md=exporter.export_pdf(p,"OC-001")
            self.assertEqual(cycle["schema_version"],"1.0.0")
            self.assertEqual(len(cycle["stages"]),10)
            self.assertEqual(cycle["external_writes"],0)
            self.assertIn("## Stage 10",md)
            self.assertEqual(planner.plan(SNAPSHOT,[])["schema_version"],1)
            self.assertEqual(intake.propose(IDEA,INVENTORY)["schema_version"],1)
    def test_pdf_rejects_bad_cycle(self):
        with self.assertRaises(ValueError):exporter.export_pdf("unused.pdf","wrong")

if __name__=="__main__":unittest.main()
