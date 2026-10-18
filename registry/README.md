# Project GPT OS registry synchronisation

Existing Supabase project: `sbdzvjqwslwaqdqyrbfn`.

## Design
Keep `public.projects`, `public.registry_items`, and `public.registry_external_refs` as canonical tables. Match discovered sources by (`provider`, `external_id`). Do not create project duplicates, rewrite IDs, or delete absent sources.

## Authentication
Configure Actions secrets `REGISTRY_GITHUB_TOKEN`, `DROPBOX_ACCESS_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`. Never expose the service-role key in a static dashboard or client app. Rotate Dropbox OAuth tokens as required.

## Operations
Run `python -m unittest discover -s tests -v`, then `python -m registry.sync` (dry run). After inspecting the report, use `python -m registry.sync --apply`, or Actions workflow dispatch with apply=true. Scheduling is disabled pending verified credential-backed dry-run and controlled write validation. The job never deletes sources.

## Dashboard
Open `registry/dashboard.html` locally and load a JSON source export. It works offline and makes no network requests. A sync report lists proposed additions, not the entire registered inventory. ChatGPT threads and agent/plugin deployment IDs must be ingested only when authoritative identifiers and ownership are verified.

## Limitations
GitHub source listing is scoped to `OurChappy`; Dropbox listing to `/Workspace`. Live workflow execution requires secrets and was not tested as part of the local unit tests.

## Validation record — 2026-10-18
Connector-level credential-free comparison: 15 GitHub repositories + 35 Dropbox folders = 50 registered external references; duplicate external IDs: 0.
Controlled database conflict write: attempted reinsert of known GitHub source `1415950693` using `ON CONFLICT DO NOTHING`; inserted 0, original retained as 1, total remained 50.
Scheduled trigger removed pending live GitHub Actions credential-safe dry run. PR test jobs do not receive credentials.
Remaining gates: confirm GitHub Actions secrets, run manual `apply=false` to completion and inspect report; stage and verify one authoritative new source with `apply=true`; re-run and verify zero further inserts. Do not schedule writes before these pass.
These connector-side checks do NOT establish that the GitHub-hosted workflow authenticated successfully.

## Private dashboard export
Run `python -m registry.export --output reports/registry-private.json` from the repository root with `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` provided by secure local environment variables or a trusted secret manager. No secret values are written to JSON. Open `registry/dashboard.html` and select the file manually. `reports/` is gitignored. Never publish the exported inventory, upload it as a public Actions artifact, or serve the service-role key to the browser. Exports are a one-time snapshot, not live sync.
