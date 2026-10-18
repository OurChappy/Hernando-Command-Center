#!/usr/bin/env python3
"""Read-only GitHub repository health inventory. Standard library only."""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"

def api(path, token):
    request = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "User-Agent": "ourchappy-repository-health",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def pages(path, token, maximum=20):
    output = []
    for page in range(1, maximum + 1):
        separator = "&" if "?" in path else "?"
        batch = api(f"{path}{separator}per_page=100&page={page}", token)
        if not isinstance(batch, list):
            raise ValueError("Expected paginated list")
        output.extend(batch)
        if len(batch) < 100:
            return output
    raise ValueError("Pagination limit reached; result incomplete")

def evaluate(repo, token):
    name = repo["full_name"]
    default = repo["default_branch"]
    branch = api(f"/repos/{name}/branches/{urllib.parse.quote(default, safe='')}", token)
    sha = branch["commit"]["sha"]
    tree = api(f"/repos/{name}/git/trees/{sha}?recursive=1", token)
    if tree.get("truncated"):
        raise ValueError("Git tree truncated; cannot assert exact counts")
    blobs = [item for item in tree["tree"] if item["type"] == "blob"]
    sizes = sorted(
        ({"path": item["path"], "bytes": item.get("size", 0)} for item in blobs),
        key=lambda item: item["bytes"], reverse=True)
    paths = {item["path"] for item in blobs}
    prs = pages(f"/repos/{name}/pulls?state=open", token)
    workflows = [p for p in paths if p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml"))]
    tests = [p for p in paths if
             "/test" in "/" + p.lower() or p.lower().endswith((".test.js", ".test.ts", ".test.tsx", "_test.go"))]
    return {
        "repository": name, "default_branch": default, "head_sha": sha,
        "visibility": "private" if repo.get("private") else "public",
        "github_size_kib": repo.get("size"), "tracked_files": len(blobs),
        "tracked_bytes": sum(item["bytes"] for item in sizes),
        "largest_files": sizes[:10], "open_prs": len(prs),
        "workflow_files": workflows, "test_file_count": len(tests),
        "has_readme": any(p.lower() == "readme.md" for p in paths),
        "has_gitignore": ".gitignore" in paths,
        "has_license": any(p.lower().startswith("license") and "/" not in p for p in paths),
        "has_codeowners": any(p in paths for p in ("CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS")),
        "assessment": "inventory_only", "ci_status": "not_assessed",
        "duplicate_files": "not_assessed", "security": "not_assessed",
    }

def render(report):
    rows = ["# OurChappy repository health snapshot", "",
        f"Generated (UTC): {report['generated_at']}", "",
        "Read-only inventory. Presence of tests and workflows does not imply tests pass.",
        "Sizes are GitHub-reported KiB; tracked bytes are current-head blob sums, not Git history size.",
        "", "| Repository | Files | Tracked MB | GitHub MB | Open PRs | Workflows | Tests |",
        "|---|---:|---:|---:|---:|---:|---:|"]
    for r in report["repositories"]:
        rows.append(f"| {r['repository']} | {r['tracked_files']} | {r['tracked_bytes']/1048576:.2f} | {(r['github_size_kib'] or 0)/1024:.2f} | {r['open_prs']} | {len(r['workflow_files'])} | {r['test_file_count']} |")
    if report["errors"]:
        rows.extend(["", "## Unassessed repositories", ""])
        for item in report["errors"]:
            rows.append(f"- {item['repository']}: {item['error']}")
    rows.extend(["", "Do not treat this inventory as a code-quality score or complete coverage if errors exist."])
    return "\n".join(rows) + "\n"

def main():
    token = os.environ.get("GH_PORTFOLIO_TOKEN") or os.environ.get("GITHUB_TOKEN")
    owner = os.environ.get("AUDIT_OWNER", "OurChappy")
    if not token:
        raise SystemExit("GH_PORTFOLIO_TOKEN or GITHUB_TOKEN required")
    repos = pages("/user/repos?affiliation=owner,organization_member&visibility=all", token)
    # Organization names also supported where accessible via org endpoint.
    repos = [r for r in repos if r.get("owner", {}).get("login", "").lower() == owner.lower()]
    if not repos:
        raise SystemExit("No repositories visible to token; check permissions and owner")
    result = {"owner": owner, "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
              "repositories": [], "errors": []}
    for repo in sorted(repos, key=lambda r: r["full_name"].lower()):
        try:
            result["repositories"].append(evaluate(repo, token))
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError) as error:
            result["errors"].append({"repository": repo["full_name"], "error": str(error)})
    os.makedirs("reports/repository-health", exist_ok=True)
    with open("reports/repository-health/report.json", "w") as output:
        json.dump(result, output, indent=2)
    with open("reports/repository-health/README.md", "w") as output:
        output.write(render(result))
    print(f"Audited {len(result['repositories'])} repositories; {len(result['errors'])} errors")
    if result["errors"]:
        sys.exit(2)

if __name__ == "__main__":
    main()
