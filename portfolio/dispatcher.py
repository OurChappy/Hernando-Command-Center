"""Offline, deterministic portfolio planning. No network, execution or database writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path

LANES = ("repair", "build", "verify")


def indexed(rows, key):
    out = {}
    for row in rows:
        value = row[key]
        if not isinstance(value, str) or not value or value in out:
            raise ValueError("Missing or duplicate " + key)
        out[value] = row
    return out


def plan(snapshot, tasks, completed=()):
    """Preserve canonical IDs; hold incomplete evidence rather than guessing."""
    if snapshot.get("schema_version") != 1:
        raise ValueError("Unsupported registry snapshot version")
    projects = indexed(snapshot["projects"], "id")
    items = indexed(snapshot["registry_items"], "id")
    task_by_id = indexed(tasks, "id")
    refs = {}
    for ref in snapshot["registry_external_refs"]:
        if ref["registry_item_id"] not in items:
            raise ValueError("Dangling external reference")
        key = (ref["provider"], str(ref["external_id"]))
        if key in refs:
            raise ValueError("Duplicate provider identity")
        refs[key] = ref["registry_item_id"]
    dependencies = {i: [] for i in items}
    for edge in snapshot["registry_dependencies"]:
        if edge.get("dependency_type", "depends_on") != "depends_on":
            raise ValueError("Unsupported dependency semantics")
        source, target = edge["source_item_id"], edge["target_item_id"]
        if source not in items or target not in items:
            raise ValueError("Dangling registry dependency")
        dependencies[source].append(target)

    # Detect registry cycles, including paths outside the selected tasks.
    visiting, visited = set(), set()
    def visit(item):
        if item in visiting:
            raise ValueError("Registry dependency cycle")
        if item in visited:
            return
        visiting.add(item)
        for target in dependencies[item]:
            visit(target)
        visiting.remove(item)
        visited.add(item)
    for item in items:
        visit(item)

    for task in tasks:
        if task.get("lane") not in LANES:
            raise ValueError("Unknown lane")
        if type(task.get("priority", 100)) is not int:
            raise ValueError("Priority must be an integer")
        if not isinstance(task.get("depends_on", []), list):
            raise ValueError("Task dependencies must be a list")
    completed = set(completed)
    if not completed <= task_by_id.keys():
        raise ValueError("Unknown completed task")
    visiting, visited = set(), set()
    def visit_task(task_id):
        if task_id in visiting:
            raise ValueError("Task dependency cycle")
        if task_id in visited:
            return
        visiting.add(task_id)
        for target in task_by_id[task_id].get("depends_on", []):
            if target in task_by_id:
                visit_task(target)
        visiting.remove(task_id)
        visited.add(task_id)
    for task_id in task_by_id:
        visit_task(task_id)

    selected, used_lanes, used_repos, rows = [], set(), set(), []
    for task in sorted(tasks, key=lambda t: (LANES.index(t["lane"]), t.get("priority", 100), t["id"])):
        reason = None
        repo = str(task.get("repository_id", ""))
        item_id = refs.get(("github", repo))
        item = items.get(item_id, {})
        project = task.get("project_id")
        deps = task.get("depends_on", [])
        if task["id"] in completed:
            reason = "completed"
        elif item_id is None:
            reason = "repository_not_registered"
        elif project not in projects or item.get("project_id") != project:
            reason = "project_mapping_unverified"
        elif any(d not in task_by_id for d in deps):
            reason = "dependency_unknown"
        elif any(d not in completed for d in deps):
            reason = "dependency_pending"
        elif any(items[d].get("status") != "verified" for d in dependencies[item_id]):
            reason = "registry_dependency_unverified"
        elif not task.get("head_sha"):
            reason = "head_sha_missing"
        elif task["lane"] != "repair":
            ci = task.get("ci", {})
            required = task.get("required_checks", [])
            checks = ci.get("checks", {})
            if not required or ci.get("sha") != task["head_sha"] or any(checks.get(c) != "success" for c in required):
                reason = "ci_unverified"
        if reason is None and repo in used_repos:
            reason = "repository_busy"
        if reason is None and task["lane"] in used_lanes:
            reason = "lane_capacity"
        row = {"task_id": task["id"], "project_id": project,
               "registry_item_id": item_id, "repository_id": repo,
               "lane": task["lane"], "head_sha": task.get("head_sha"),
               "status": "selected" if reason is None else ("completed" if reason == "completed" else "held"),
               "reason": reason}
        rows.append(row)
        if reason is None:
            selected.append(row)
            used_lanes.add(task["lane"])
            used_repos.add(repo)
    canonical = json.dumps({"snapshot": snapshot, "tasks": tasks, "completed": sorted(completed)}, sort_keys=True, separators=(",", ":"))
    return {"schema_version": 1, "mode": "plan_only", "input_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
            "source_observed_at": snapshot.get("observed_at"),
            "selected": selected, "tasks": rows,
            "counts": {"selected": len(selected), "held": sum(r["status"] == "held" for r in rows),
                       "completed": len(completed)},
            "warnings": ["Snapshot evidence requires refresh before any execution.",
                         "No durable claim or task execution is performed."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    snapshot = json.loads(Path(args.registry).read_text())
    batch = json.loads(Path(args.tasks).read_text())
    result = plan(snapshot, batch["tasks"], batch.get("completed", []))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Private output even if an existing file had broader permissions.
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result["counts"]))


if __name__ == "__main__":
    main()
