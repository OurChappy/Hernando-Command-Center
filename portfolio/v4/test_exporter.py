import tempfile, unittest
from pathlib import Path
import fitz
from exporter import export_pdf
class ExporterTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/"synthetic.pdf";doc=fitz.open()
        for i in range(1,11):
            page=doc.new_page()
            for j,n in enumerate(("problem_or_source","evidence_links")):
                w=fitz.Widget();w.field_name=f"stage_{i:02d}_{n}";w.field_type=fitz.PDF_WIDGET_TYPE_TEXT
                w.rect=fitz.Rect(20,20+j*40,300,50+j*40);w.field_value=f"case-{i}-{j}";page.add_widget(w)
        doc.save(self.p);doc.close()
    def tearDown(self):self.tmp.cleanup()
    def test_ten_stages(self):self.assertEqual(len(export_pdf(self.p,"OC-001")[0]["stages"]),10)
    def test_no_external_writes(self):self.assertEqual(export_pdf(self.p,"OC-001")[0]["external_writes"],0)
    def test_deterministic(self):self.assertEqual(export_pdf(self.p,"OC-001"),export_pdf(self.p,"OC-001"))
    def test_values(self):self.assertEqual(export_pdf(self.p,"OC-001")[0]["stages"][0]["input_text"],"case-1-0")
    def test_markdown(self):self.assertIn("## Stage 10",export_pdf(self.p,"OC-001")[1])
    def test_reject_cycle(self):
        with self.assertRaises(ValueError):export_pdf(self.p,"wrong")
    def test_missing_field(self):
        doc=fitz.open(self.p);page=doc[0];page.delete_widget(next(page.widgets()))
        p=Path(self.tmp.name)/"missing.pdf";doc.save(p);doc.close()
        with self.assertRaisesRegex(ValueError,"Missing required"):export_pdf(p,"OC-001")
if __name__=="__main__": unittest.main()
