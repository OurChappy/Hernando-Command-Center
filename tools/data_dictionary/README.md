# Supabase Data Dictionary v1.2 — isolated offline prototype

Scope: compares **two JSON array snapshots** of column metadata, keyed by (schema, table, column), without any network access or database writes. Detects missing, stale, altered type and nullability. Deliberately does **not** export live data or issue PRs automatically.

## Run
```bash
python -m unittest discover -s tests -p 'test_data_dictionary_drift.py' -v
python -m tools.data_dictionary.drift --physical physical.json --catalogued catalogue.json --output reports/dictionary-drift.json --fail-on-drift
```

Each input is an array of objects: `{"schema":"public","table":"projects","column":"id","type":"uuid","nullable":false}`.

## Verified baseline (2026-10-19, read-only live SQL)
Across schemas public, acnc, analytics, cricos, metadata, raw and staging, 2,119 physical columns; 1,468 currently registered in `metadata.columns`; 651 not matched. Not a live CI execution result.

## Required gates for live automation
1. Reuse canonical `metadata.tables`, `metadata.columns` and `metadata.data_dictionary_vw`. Do not create competing tables.
2. Establish a **least-privilege read-only** database identity scoped to approved metadata views. Do not use `SUPABASE_SERVICE_ROLE_KEY`, owner credentials, or an unrestricted connection string.
3. Validate read capability and denial of INSERT/UPDATE/DELETE and privileged RPCs with controlled negative tests, using a disposable test database/role. Never try mutating production to prove read-only guarantees.
4. Design a separate snapshot exporter restricted to those views, with secrets masked, counts verified and private artifacts.
5. Only after those gates, add manual live scan, optional GitHub App PR automation, and a scheduled trigger. No cron trigger in this version.
6. Review privacy and authorization of catalogue descriptions before sharing reports.

## Known limitations
Synthetic fixture tests only. Not yet connected to Supabase; no CI results verified at PR head. Live snapshots and action-generated draft PRs remain **blocked** pending credential controls. Reports could reveal schema names and should remain private.
