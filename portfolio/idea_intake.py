"""Offline idea-to-issue proposals. Never connects to providers or writes records."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def propose(idea, inventory):
    if not isinstance(idea, dict) or not isinstance(inventory, dict):
        raise ValueError("Objects required")
    for field in ("title", "outcome", "repository_id", "repository", "project_id", "registry_item_id", "evidence", "tasks"):
        if field not in idea:
            raise ValueError("Missing " + field)
    if not isinstance(idea["title"], str) or not idea["title"].strip() or not isinstance(idea["outcome"], str) or not idea["outcome"].strip():
        raise ValueError("Title and outcome required")
    if not isinstance(idea["tasks"], list) or not idea["tasks"]:
        raise ValueError("Nonempty tasks required")
    if not isinstance(idea["evidence"], list) or not all(isinstance(e, dict) and e.get("url") and e.get("classification") in ("verified", "reported", "hypothesis") for e in idea["evidence"]):
        raise ValueError("Evidence records must carry URL and classification")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", str(idea["repository"])):
        raise ValueError("Invalid repository")
    ids = [task.get("id") for task in idea["tasks"]]
    if not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Missing/duplicate task ids")
    task_by_id = {task["id"]: task for task in idea["tasks"]}
    visiting, done = set(), set()
    def visit(task_id):
        if task_id in visiting:
            raise ValueError("Dependency cycle")
        if task_id in done:
            return
        visiting.add(task_id)
        for dependency in task_by_id[task_id].get("depends_on", []):
            if dependency not in task_by_id:
                raise ValueError("Unknown dependency")
            visit(dependency)
        visiting.remove(task_id)
        done.add(task_id)
    for task_id in ids:
        visit(task_id)
    matches = [r for r in inventory.get("repositories", []) if str(r.get("id")) == str(idea["repository_id"]) and r.get("full_name") == idea["repository"]]
    mapping_ok = (len(matches) == 1 and matches[0].get("project_id") == idea["project_id"]
                  and matches[0].get("registry_item_id") == idea["registry_item_id"]
                  and all(idea.get(k) for k in ("project_id", "registry_item_id", "repository_id")))
    duplicates = [x for x in inventory.get("existing_issues", [])
                  if x.get("repository") == idea["repository"]
                  and x.get("title", "").casefold().strip() == idea["title"].casefold().strip()]
    stable = json.dumps(idea, sort_keys=True, separators=(",", ":"))
    key = hashlib.sha256(stable.encode()).hexdigest()[:16]
    status = "hold_mapping" if not mapping_ok else ("reuse_or_review" if duplicates else "proposal_only")
    tasks = []
    for task in idea["tasks"]:
        if not isinstance(task.get("title"), str) or not task["title"].strip() or not isinstance(task.get("acceptance"), list) or not task["acceptance"]:
            raise ValueError("Each task needs title and acceptance")
        tasks.append({"id": task["id"], "proposal_key": key + ":" + task["id"], "title": task["title"],
                      "depends_on": task.get("depends_on", []), "acceptance": task["acceptance"]})
    markdown = ("# " + idea["title"] + "\n\n## Outcome\n" + idea["outcome"] + "\n\n## Evidence\n"
                + "".join("- [" + e["classification"] + "] " + e["url"] + "\n" for e in idea["evidence"])
                + "\n## Tasks\n" + "".join("- **" + t["id"] + "** " + t["title"] + " — " + "; ".join(t["acceptance"]) + "\n" for t in tasks))
    return {"schema_version": 1, "mode": "dry_run", "status": status, "proposal_key": key,
            "repository": idea["repository"], "matches": duplicates, "tasks": tasks,
            "issue_markdown": markdown, "external_writes": 0}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--idea", required=True)
    p.add_argument("--inventory", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    output = propose(json.loads(Path(a.idea).read_text()), json.loads(Path(a.inventory).read_text()))
    Path(a.output).write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "task_count": len(output["tasks"]), "external_writes": 0}))

if __name__ == "__main__":
    main()
