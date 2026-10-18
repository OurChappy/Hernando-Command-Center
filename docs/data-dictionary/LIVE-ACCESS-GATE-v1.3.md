# Data Dictionary v1.3 — secure live monitoring gate

Status: **proposal; no live connectivity deployed**. Depends on draft PR #48 (v1.2); this branch is based on its head. Parent programme: Epic #10.

## Read-only inventory scope

Physical metadata: approved schemas only (public, acnc, analytics, cricos, metadata, raw, staging), column identity, SQL type, nullable flag. Dictionary: existing `metadata.tables` and `metadata.columns` joined by table_id, plus `metadata.data_dictionary_vw` for the business catalogue. No row contents, owner IDs, descriptions, example values, access tokens or credentials in export.

Proposed transport: administrator-approved, dedicated **read-only** Postgres principal restricted to specifically reviewed metadata views, with short-lived authentication or appropriately secured server-side gateway. Neither a Supabase service-role key nor a publishable key is adequate evidence of least privilege.

## Gate checklist before any live workflow

1. Approve access model and explicit schema/object allowlist; verify neither `information_schema` nor the underlying `metadata` catalogue inadvertently exposes confidential object names.
2. Create and scope access only in an independently approved change, outside this PR. SQL functions may execute with elevated rights; forbid privileged RPC execution.
3. Test SELECT coverage against approved baseline and deny INSERT/UPDATE/DELETE/CREATE/EXECUTE in an isolated database with synthetic records. Production negative write tests are forbidden.
4. Supply credentials exclusively from a protected secret manager to trusted workflow identity; never in PR jobs from forks. Restrict network destination, token life and rate/row limits. Disable logs of raw responses.
5. Build an authenticated exporter only after gates 1–4. Feed its output to `tools/data_dictionary/snapshot.py`, then to the v1.2 `drift.py`.
6. Review private artifact retention, masking, approvals and alert thresholds. Enable manual live run first; schedule and automatic draft PR creation require separate approval.
7. Verify fresh run SHA, count reconciliation, false-positive behaviour, and failure alerts before moving out of draft.

## Current concrete baseline

Read-only inspection on 2026-10-19: 2,119 physical columns, 1,468 catalogued, 651 unmatched across the seven approved schemas. This is not a live Actions scan.

## Data contract

Each **pre-exported** input consists strictly of `schema`, `table`, `column`, `type`, `nullable`. v1.3 rejects extra keys (including actual data values), unapproved schemas, duplicate keys, invalid field types. It cannot attest to privileges or source authenticity. Passing tests is not authorization to enable live access.

## Running locally

```sh
python -m unittest discover -s tests -p 'test_data_dictionary_*.py' -v
python -m tools.data_dictionary.snapshot --source physical --input physical.json --output normalized-physical.json
python -m tools.data_dictionary.snapshot --source catalogued --input catalogued.json --output normalized-catalogued.json
python -m tools.data_dictionary.drift --physical normalized-physical.json --catalogued normalized-catalogued.json --output drift.json --fail-on-drift
```

No changes to production Supabase permissions, tables, deployment or schedule are included.
