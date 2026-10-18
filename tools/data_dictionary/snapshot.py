"""Validate and normalize *pre-exported* metadata snapshots. No network or credentials."""
import argparse
import json
from pathlib import Path

ALLOWED_SCHEMAS = frozenset(("public", "acnc", "analytics", "cricos", "metadata", "raw", "staging"))
KEYS = ("schema", "table", "column")

def normalize(rows, *, source):
    if not isinstance(rows, list):
        raise ValueError("snapshot must be an array")
    output = []
    seen = set()
    for item in rows:
        if not isinstance(item, dict):
            raise ValueError("each row must be an object")
        if set(item) - set(KEYS + ("type", "nullable")):
            raise ValueError("unexpected field in snapshot")
        if any(not isinstance(item.get(k), str) or not item[k] for k in KEYS):
            raise ValueError("invalid metadata identity")
        if item["schema"] not in ALLOWED_SCHEMAS:
            raise ValueError("schema not allowed")
        identity = tuple(item[k] for k in KEYS)
        if identity in seen:
            raise ValueError("duplicate metadata identity")
        seen.add(identity)
        if not isinstance(item.get("type"), str) or not item["type"]:
            raise ValueError("invalid column type")
        if not isinstance(item.get("nullable"), bool):
            raise ValueError("nullable must be a boolean")
        output.append({k: item[k] for k in KEYS + ("type", "nullable")})
    return sorted(output, key=lambda x: tuple(x[k] for k in KEYS))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--source", choices=("physical", "catalogued"), required=True)
    a = p.parse_args()
    result = normalize(json.loads(Path(a.input).read_text(encoding="utf-8")), source=a.source)
    dest = Path(a.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"validated {a.source} columns: {len(result)}")

if __name__ == "__main__":
    main()
