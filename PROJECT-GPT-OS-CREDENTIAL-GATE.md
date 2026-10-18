# Project GPT OS — Read-only credential security gate

Date: 2026-10-18

## Verified facts
- Registry tables have `authenticated` SELECT/INSERT/UPDATE/DELETE grants, but row-level policies restrict access to a record's owner.
- `registry_items_owner_policy` requires `owner_id = auth.uid()` and, for attached projects, a matching `project_owner(project_id)`.
- `registry_refs_owner_policy` requires that the referenced registry item is owned by `auth.uid()`.
- A service-role key bypasses RLS and is **not** a least-privilege read-only credential.
- The bootstrap currently uses `SUPABASE_SERVICE_ROLE_KEY`; its lack of a write command does not make that credential read-only.
- A publishable/anon key by itself is not a safe alternative. An authenticated bearer might see only its own registry rows; don't interpret incomplete results as a fully reconciled inventory.

## Mandatory gate before unattended use
1. Establish a principal allowed to read *all and only* the intended canonical registry source rows. Audit ownership of all 50 refs first.
2. Issue short-lived credentials for that principal, or implement a server-side read-only endpoint guarded by explicit authentication, scope and rate limits.
3. Confirm the principal cannot INSERT, UPDATE, DELETE or run privileged RPCs; RLS alone may not enforce this because existing policies allow ALL for row owners.
4. Test a full count against the trusted baseline (35 Dropbox + 15 GitHub) and verify zero-write enforcement with negative tests.
5. Rotate and remove privileged service-role secret from the read-only bootstrap after migration.
6. Only then approve authenticated workflow execution and later controlled writes. Keep production schedule disabled throughout.

## Existing bootstrap
Manual-only workflow exists on main and is pinned to a reviewed commit. It has **not** been proven to run end-to-end with credentials. Do not record it as production ready.

## Repository status
PR #1 is draft and unmerged. No Railway deployments are approved.
