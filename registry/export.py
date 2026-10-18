"""Export a read-only Project GPT OS dashboard snapshot to a local JSON file.

No secrets enter the export. Uses server-side Supabase credentials only.
"""
import argparse
import json
import os
from pathlib import Path
from registry.sync import api

def fetch_rows(base, key, table, select, page_size=500):
    result = []
    for offset in range(0, 100000, page_size):
        url = base + table + "?select=" + select + "&limit=" + str(page_size) + "&offset=" + str(offset)
        batch = api(url, key, extra={"apikey": key})
        result.extend(batch)
        if len(batch) < page_size:
            return result
    raise RuntimeError("Export exceeds supported pagination limit")

def build_export(projects, items, refs, threads):
    by_id = {i["id"]: i for i in items}
    sources = []
    for ref in refs:
        item = by_id.get(ref.get("registry_item_id"), {})
        if item.get("item_type") == "source":
            sources.append({
                "provider": ref["provider"],
                "external_id": ref["external_id"],
                "name": item.get("name", ""),
                "external_url": ref.get("external_url"),
                "source_path": ref.get("source_path")
            })
    catalog = [
        {"item_type": i["item_type"], "item_code": i["item_code"],
         "name": i["name"], "status": i.get("status"),
         "version": i.get("version")}
        for i in items if i.get("item_type") in ("agent", "plugin")
    ]
    return {
        "schema_version": "1",
        "projects": [{"project_code": p["project_code"], "name": p["name"], "status": p.get("status")} for p in projects],
        "sources": sorted(sources, key=lambda x: (x["provider"], x["name"])),
        "catalogue": sorted(catalog, key=lambda x: x["item_code"]),
        "threads": [{"name": t["name"], "provider": t.get("provider"), "external_id": t.get("external_id"), "status": t.get("status")} for t in threads],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="reports/registry-private.json")
    args = parser.parse_args()
    for name in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        if not os.environ.get(name):
            parser.error(name + " is required")
    base = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/"
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    export = build_export(
        fetch_rows(base, key, "projects", "project_code,name,status"),
        fetch_rows(base, key, "registry_items", "id,item_type,item_code,name,status,version"),
        fetch_rows(base, key, "registry_external_refs", "registry_item_id,provider,external_id,external_url,source_path"),
        fetch_rows(base, key, "threads", "name,provider,external_id,status")
    )
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        target.chmod(0o600)
    except OSError:
        pass
    print(json.dumps({k: len(v) for k, v in export.items() if isinstance(v, list)}))

if __name__ == "__main__":
    main()
