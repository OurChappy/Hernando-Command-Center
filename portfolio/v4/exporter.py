"""Offline interactive-PDF worksheet export. No provider calls."""
import argparse, hashlib, json, re
from pathlib import Path
import fitz
STAGES=[f"stage_{i:02d}" for i in range(1,11)]
EXPECTED={f"{s}_{suffix}" for s in STAGES for suffix in ("problem_or_source","evidence_links")}
def export_pdf(path,cycle_id):
    if not re.fullmatch(r"[A-Z][A-Z0-9-]{2,63}",cycle_id): raise ValueError("Invalid cycle ID")
    p=Path(path);doc=fitz.open(p)
    try:
        if doc.is_encrypted: raise ValueError("Encrypted PDF unsupported")
        fields={}
        for page in doc:
            for w in page.widgets() or ():
                if w.field_name in fields: raise ValueError("Duplicate field: "+w.field_name)
                fields[w.field_name]=w.field_value or ""
        missing=EXPECTED-fields.keys()
        if missing: raise ValueError("Missing required PDF fields: "+", ".join(sorted(missing)))
        stages=[{"stage":s,"input_text":fields[s+"_problem_or_source"].strip(),
                 "evidence_text":fields[s+"_evidence_links"].strip(),"status":"worksheet_draft"} for s in STAGES]
        payload={"schema_version":"1.0.0","cycle_id":cycle_id,
                 "source":{"type":"pdf_form","filename":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()},
                 "stages":stages,"mode":"offline_dry_run","external_writes":0}
        lines=[f"# Cycle {cycle_id}","","Status: WORKSHEET DRAFT — not verified or approved.",""]
        for i,s in enumerate(stages,1):
            lines += [f"## Stage {i:02d}","","Input / source:",s["input_text"] or "(not entered)","",
                      "Evidence references (unverified free text):",s["evidence_text"] or "(not entered)",""]
        return payload,"\n".join(lines)
    finally: doc.close()
def main():
    a=argparse.ArgumentParser()
    a.add_argument("pdf");a.add_argument("--cycle-id",required=True);a.add_argument("--output-dir",required=True)
    v=a.parse_args(); data,md=export_pdf(v.pdf,v.cycle_id)
    dest=Path(v.output_dir);dest.mkdir(parents=True,exist_ok=True)
    (dest/"cycle.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    (dest/"cycle.md").write_text(md,encoding="utf-8")
    print(json.dumps({"cycle_id":v.cycle_id,"stages":len(data["stages"]),"external_writes":0}))
if __name__=="__main__":main()
