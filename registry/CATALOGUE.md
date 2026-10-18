# Agent and plugin catalogue

The canonical record is `public.registry_items` in Project GPT OS. Do **not** create a second table just for agents and plugins.

## Required fields
- `item_type`: `agent` or `plugin`
- `item_code`: stable internal code, never reuse or change after assignment
- `name`, `description`, `status`, `version`, `project_id`
- `metadata`: include `lifecycle`, `capabilities`, `repository`, `deployment_status`, `last_verified_at` as applicable

Use `registry_external_refs` for verified provider resource IDs and URLs. Never infer a deployed agent ID from a GitHub folder, a chat title or a planned specification.

## Lifecycle
Proposed → Designed → Building → Testing → Ready → Released → Retired.

`Ready` requires tests; `Released` requires an independently verified deployment identifier and access path. Use `status` values supported by the existing database; record finer lifecycle stages in metadata if needed.

## Registration protocol
1. Search existing `registry_items` by stable code, matching external reference and known alias.
2. If a record already exists, extend it; do not create another.
3. Resolve `project_id` using the existing `projects.project_code`.
4. Insert only after a code and ownership are confirmed.
5. Store build source URLs and Dropbox deliverables as external references with provider-scoped identifiers.
6. Test a second ingestion run; expected new items = 0.

## ChatGPT threads
Use `public.threads` only for verified conversation identifiers or URLs, with an existing project UUID. Never fabricate thread identifiers and never infer an exact thread from its topic alone.

## Export format for offline dashboard
Create a **private, redacted, read-only** JSON export of the form:
```json
{
  "projects": [{"project_code":"GOODTURN","name":"Goodturn","status":"Discovery"}],
  "sources": [{"provider":"github","external_id":"1415950693","name":"goodturn-brand","external_url":"https://github.com/OurChappy/goodturn-brand"}],
  "catalogue": [{"item_type":"agent","item_code":"AGT-0001","name":"Example only","status":"Design"}],
  "threads": []
}
```
All rows above are illustrative except the explicitly verified existing project/repository example. Do not publish live exports from a private workspace to a public repository.
