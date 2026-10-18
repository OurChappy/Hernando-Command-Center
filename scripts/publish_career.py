#!/usr/bin/env python3
"""Publish the four approved career artifacts to Dropbox using the Dropbox HTTP API."""
import hashlib
import json
import os
from pathlib import Path
from urllib import request, error

ROOT = Path("artifacts/career")
BASE = "/Workspace/02-Career-and-Learning/06-Career-Planning"
FILES = [
    ("Career_Market_Research_Sydney_Oct2026_v3.xlsx", "Current Workbooks"),
    ("Senior_Career_Action_Planner_Project_One_v3.xlsx", "Current Workbooks"),
    ("Career_Market_Research_Sydney_Oct2026_v3.pdf", "PDF Reading Copies"),
    ("Senior_Career_Action_Planner_Project_One_v3.pdf", "PDF Reading Copies"),
]
REPORT = Path("publishing-report.json")

def dbx_hash(data):
    """Dropbox content hash: SHA256 of concatenated SHA256 hashes of 4 MiB blocks."""
    blocks = (hashlib.sha256(data[i:i+4*1024*1024]).digest()
              for i in range(0, len(data), 4*1024*1024))
    return hashlib.sha256(b"".join(blocks)).hexdigest()

def upload(token, data, destination):
    args = {"path": destination, "mode": "add", "autorename": False, "mute": True}
    req = request.Request(
        "https://content.dropboxapi.com/2/files/upload",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": json.dumps(args),
        },
        method="POST",
    )
    with request.urlopen(req, timeout=90) as response:
        return json.load(response)

def main():
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    token = os.getenv("DROPBOX_ACCESS_TOKEN", "")
    results = []
    failed = False
    try:
        for filename, folder in FILES:
            source = ROOT / filename
            destination = f"{BASE}/{folder}/{filename}"
            entry = {"file": filename, "destination": destination}
            results.append(entry)
            if not source.is_file():
                entry["status"] = "missing_source"
                failed = True
                continue
            data = source.read_bytes()
            entry["bytes"] = len(data)
            entry["content_hash"] = dbx_hash(data)
            if not data:
                entry["status"] = "empty_file"
                failed = True
                continue
            if dry_run:
                entry["status"] = "validated_dry_run"
                continue
            if not token:
                entry["status"] = "missing_secret"
                failed = True
                continue
            try:
                result = upload(token, data, destination)
                entry["dropbox_id"] = result.get("id")
                entry["dropbox_rev"] = result.get("rev")
                entry["status"] = ("verified" if result.get("content_hash") == entry["content_hash"]
                                   and result.get("path_display", "").casefold() == destination.casefold()
                                   else "verification_failed")
                if entry["status"] != "verified":
                    failed = True
            except error.HTTPError as exc:
                entry["status"] = "upload_failed"
                entry["http_status"] = exc.code
                entry["error"] = exc.read(2000).decode("utf-8", "replace")
                failed = True
            except Exception as exc:
                entry["status"] = "upload_failed"
                entry["error"] = str(exc)
                failed = True
    finally:
        REPORT.write_text(json.dumps({"dry_run": dry_run, "results": results}, indent=2))
        print(REPORT.read_text())
    if failed:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
