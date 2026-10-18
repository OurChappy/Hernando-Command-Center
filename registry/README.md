# Project GPT OS registry synchronisation

Existing Supabase project: `sbdzvjqwslwaqdqyrbfn`.

## Design
Keep `public.projects`, `public.registry_items`, and `public.registry_external_refs` as canonical tables. Match discovered sources by (`provider`, `external_id`). Do not create project duplicates, rewrite IDs, or delete absent sources.

## Authentication
Configure Actions secrets `REGISTRY_GITHUB_TOKEN`, `DROPBOX_ACCESS_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`. Never expose the service-role key in a static dashboard or client app. Rotate Dropbox OAuth tokens as required.

## Operations
Run `python -m unittest discover -s tests -v`, then `python -m registry.sync` (dry run). After inspecting the report, use `python -m registry.sync --apply`, or Actions workflow dispatch with apply=true. Scheduled runs are dry-run only. The job never deletes sources.

## Dashboard
Open `registry/dashboard.html` locally and load a JSON source export. It works offline and makes no network requests. A sync report lists proposed additions, not the entire registered inventory. ChatGPT threads and agent/plugin deployment IDs must be ingested only when authoritative identifiers and ownership are verified.

## Limitations
GitHub source listing is scoped to `OurChappy`; Dropbox listing to `/Workspace`. Live workflow execution requires secrets and was not tested as part of the local unit tests.