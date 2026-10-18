"""Idempotent GitHub/Dropbox to Supabase source reconciliation. Stdlib only."""
import argparse,json,os,urllib.request,urllib.parse,urllib.error

def api(url,token,method="GET",body=None,extra=None):
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",**(extra or {})}
    if body is not None: headers["Content-Type"]="application/json"
    req=urllib.request.Request(url,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
    with urllib.request.urlopen(req,timeout=30) as res:
        raw=res.read()
        return json.loads(raw) if raw else []

def github(token,owner):
    out=[]
    for page in range(1,101):
        batch=api(f"https://api.github.com/user/repos?affiliation=owner,collaborator,organization_member&per_page=100&page={page}",token,extra={"X-GitHub-Api-Version":"2022-11-28"})
        out += [{"provider":"github","external_id":str(r["id"]),"name":r["name"],"external_url":r["html_url"],"source_path":None} for r in batch if r["owner"]["login"].lower()==owner.lower()]
        if len(batch)<100: break
    return out

def dropbox(token):
    endpoint="https://api.dropboxapi.com/2/files/"
    r=api(endpoint+"list_folder",token,"POST",{"path":"/Workspace","recursive":True})
    out=list(r["entries"])
    while r.get("has_more"):
        r=api(endpoint+"list_folder/continue",token,"POST",{"cursor":r["cursor"]})
        out.extend(r["entries"])
    return [{"provider":"dropbox","external_id":x["id"],"name":x["name"],"external_url":None,"source_path":x.get("path_display") or x.get("path_lower")} for x in out if x.get(".tag")=="folder"]

def reconcile(existing,discovered):
    seen={(x["provider"],str(x["external_id"])) for x in existing}
    unique={(x["provider"],str(x["external_id"])):x for x in discovered}
    return [v for k,v in sorted(unique.items()) if k not in seen]

def main(apply=False):
    names=["REGISTRY_GITHUB_TOKEN","DROPBOX_ACCESS_TOKEN","SUPABASE_URL","SUPABASE_SERVICE_ROLE_KEY"]
    missing=[n for n in names if not os.getenv(n)]
    if missing: raise RuntimeError("Missing "+", ".join(missing))
    base=os.environ["SUPABASE_URL"].rstrip("/")+"/rest/v1/"
    key=os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    def read(table,select):
        return api(base+table+"?select="+urllib.parse.quote(select)+"&limit=10000",key,extra={"apikey":key})
    def insert(table,record,conflict):
        url=base+table+"?on_conflict="+urllib.parse.quote(conflict)
        return api(url,key,"POST",record,{"apikey":key,"Prefer":"resolution=ignore-duplicates,return=representation"})
    def find_one(table,field,value):
        url=base+table+"?"+urllib.parse.quote(field)+"=eq."+urllib.parse.quote(str(value))+"&select=id&limit=1"
        return api(url,key,extra={"apikey":key})
    items=read("registry_items","id,item_code")
    refs=read("registry_external_refs","provider,external_id")
    discovered=github(os.environ["REGISTRY_GITHUB_TOKEN"],os.getenv("GITHUB_OWNER","OurChappy"))+dropbox(os.environ["DROPBOX_ACCESS_TOKEN"])
    new=reconcile(refs,discovered)
    # GitHub Actions artifacts must never contain private paths, names or external IDs.
    report={"dry_run":not apply,"discovered":len(discovered),"existing_refs":len(refs),"new":len(new),
            "proposed_counts":{provider:sum(x["provider"]==provider for x in new)
                               for provider in ("github","dropbox")}}
    os.makedirs("reports",exist_ok=True)
    with open("reports/registry-sync.json","w") as f: json.dump(report,f,indent=2)
    if apply:
        known={x["item_code"]:x["id"] for x in items}
        for x in new:
            code=x["provider"]+":"+x["external_id"]
            item_id=known.get(code)
            if item_id is None:
                added=insert("registry_items",{"item_type":"source","item_code":code,"name":x["name"],"status":"Active"},"item_type,item_code")
                item_id=added[0]["id"] if added else (find_one("registry_items","item_code",code) or [])[0]["id"]
                known[code]=item_id
            insert("registry_external_refs",{"registry_item_id":item_id,"provider":x["provider"],"external_id":x["external_id"],"external_url":x["external_url"],"source_path":x["source_path"]},"provider,external_id")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    main(p.parse_args().apply)
