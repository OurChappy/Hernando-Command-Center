"""Offline, deterministic schema-to-dictionary reconciliation. No database access."""
import argparse
import json
from pathlib import Path

KEYS = ("schema", "table", "column")

def key(row):
    return tuple(str(row[k]) for k in KEYS)

def compare(physical, catalogued):
    a = {key(x): x for x in physical}
    b = {key(x): x for x in catalogued}
    if len(a) != len(physical) or len(b) != len(catalogued):
        raise ValueError("Duplicate schema/table/column identity")
    missing = sorted(set(a) - set(b))
    stale = sorted(set(b) - set(a))
    changes = []
    for k in sorted(set(a) & set(b)):
        for field in ("type", "nullable"):
            if field in a[k] and field in b[k] and a[k][field] != b[k][field]:
                changes.append({"key": list(k), "field": field, "actual": a[k][field], "catalogued": b[k][field]})
    return {"physical_columns": len(a), "catalogued_columns": len(b),
            "missing_in_dictionary": [list(x) for x in missing],
            "stale_in_dictionary": [list(x) for x in stale],
            "attribute_drift": changes,
            "drift": bool(missing or stale or changes)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--physical", required=True)
    parser.add_argument("--catalogued", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fail-on-drift", action="store_true")
    args = parser.parse_args()
    physical = json.loads(Path(args.physical).read_text(encoding="utf-8"))
    catalogued = json.loads(Path(args.catalogued).read_text(encoding="utf-8"))
    if not isinstance(physical, list) or not isinstance(catalogued, list):
        parser.error("Both inputs must be JSON arrays")
    report = compare(physical, catalogued)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"physical={report['physical_columns']} catalogued={report['catalogued_columns']} missing={len(report['missing_in_dictionary'])} stale={len(report['stale_in_dictionary'])} altered={len(report['attribute_drift'])}")
    if args.fail_on_drift and report["drift"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
