"""Produce evidence-based catalogue candidates without inventing deployment identities."""
import json
from pathlib import Path

def discover_candidates(repository_records):
    profiles = {
        "1351223629": ("plugin", "TAFE Browser MCP", "source_verified", "README documents local stdio MCP and remote deployment is deferred"),
        "1245312722": ("plugin", "PortalFlow Connector Hub", "source_verified", "README advertises FastAPI gateway and deployment; endpoint health not verified"),
        "1340726659": ("application", "Project GPT OS Web App", "source_verified", "README says Next.js app deployed on Vercel; deployment not independently verified"),
    }
    candidates=[]
    for record in repository_records:
        repo_id=str(record.get("external_id",""))
        if record.get("provider")!="github" or repo_id not in profiles:
            continue
        kind,name,state,note=profiles[repo_id]
        candidates.append({"candidate_key":"github:"+repo_id,"kind":kind,"name":name,"evidence_url":record.get("external_url"),"verification":state,"notes":note,"deployed_identifier":None,"registration_action":"review_only"})
    return sorted(candidates,key=lambda x:x["candidate_key"])

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("snapshot",help="Private JSON snapshot: do not commit")
    p.add_argument("--output",default="reports/catalogue-candidates.json")
    args=p.parse_args()
    payload=json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    candidates=discover_candidates(payload.get("sources",[]))
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(candidates,indent=2),encoding="utf-8")
    print("Candidates requiring review:",len(candidates))

if __name__=="__main__":
    main()
