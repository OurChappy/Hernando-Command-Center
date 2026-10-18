# Project GPT OS — bootstrap runbook

This guide applies to the **manual-only** GitHub Actions workflow in `.github/workflows/project-gpt-os-bootstrap.yml` on `main`. It is not the production synchronisation workflow.

## What is already safe
- No `schedule` event or `--apply` option.
- Workflow checks out a reviewed, pinned source commit.
- Python compilation and the registry test suite run before credential access.
- Missing credentials result in a failed run, without echoing values.
- No private JSON snapshots are committed or uploaded as Actions artifacts.

## One-time account setup
In repository Settings → Secrets and variables → Actions, configure:
1. `REGISTRY_GITHUB_TOKEN`: fine-grained token with read-only metadata access to the intended private repositories, if the inventory includes private repositories.
2. `DROPBOX_ACCESS_TOKEN`: OAuth access token with permission to **list** the intended /Workspace hierarchy. For a long-lived workflow, use secure token refresh rather than relying on an expiring token.
3. `SUPABASE_URL`: Project GPT OS API URL, not a secret.
4. `SUPABASE_SERVICE_ROLE_KEY`: currently required by the existing registry script. This key is highly privileged. Prefer a narrowly scoped read-only Supabase access route before scheduling or broader automation. Never share it in chat, tickets or commit history.

## Run and interpret
Open Actions → Project GPT OS — Manual Dry Run Bootstrap → Run workflow → main.
- If **Compile and test** fails: fix the test/bootstrap problem; do not proceed.
- If **Validate secret presence** fails: configure the missing secret(s) by name in GitHub settings; do not paste their values into an issue or discussion.
- If **Read-only inventory reconciliation** fails: check provider scope, Dropbox token expiry and Supabase table read policy.
- A successful run reports discovered and new source counts. Compare with the verified baseline of 15 GitHub repos and 35 Dropbox folders before allowing writes. Inventory can change legitimately; investigate unexpected differences.
- A successful dry run does not mean that live writes have been verified.

## Release gates
1. CI pass on the PR.
2. Authenticated read-only bootstrap success.
3. Review source identities and new candidates; avoid any fabricated IDs.
4. Independent, explicitly approved controlled-write test.
5. Rerun to prove zero duplicates.
6. Validate repository rules and merge only with the user's approval.
7. Scheduling remains disabled until every gate passes.

**Do not use Railway.** No production deployment is performed by this workflow.
