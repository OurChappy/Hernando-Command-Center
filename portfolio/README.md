# Three-lane portfolio dispatcher — read-only planning release

This additive component produces a dashboard-ready task selection plan. It does
not execute tasks, call providers, claim durable work, merge, deploy or write to
Supabase. It has no package dependencies beyond Python 3.12+ standard library.
The workflow runs synthetic tests on pull requests and manual dispatch only.

## Lanes and admission

| Lane | Work | CI admission |
| --- | --- | --- |
| repair | Diagnose and repair foundation/CI blockers | A known repository and head are required; failed CI is allowed |
| build | Prepare a scoped implementation branch/PR | All required checks must pass for the supplied head SHA |
| verify | Test and review evidence for a completed change | Same SHA and required-check gate as build |

One selection per lane, at most three selections per plan. Repair is considered
first, then build, then verify; integer priority and task ID break ties. A
repository selected in any lane is unavailable in the other lanes. Pending tasks
remain in the input backlog. Task dependencies unlock only on explicit completed
IDs, never because another task was selected in the same plan. Cycles and duplicate
identities reject the input. Unknown dependency IDs hold the task. Registry
dependencies require exact `verified` status; unknown relation semantics reject
the snapshot. Missing CI, checks, project mapping or repository identity hold work.

## Reuse the existing registry

`registry-snapshot.sql` is a SELECT-only export contract over the existing
`projects`, `registry_items`, `registry_external_refs`, `registry_dependencies`.
Match repositories by (`github`, numeric repository ID as text), then retain the
existing item UUID and its project UUID. Never match by name or generate replacements.
No schema changes, migrations or records are introduced. Null project mappings
require an independently reviewed mapping correction, not inference.

The dashboard exporter in the separate registry synchronisation PR omits IDs
needed for dispatch; its v1 export is deliberately not accepted. Use this explicit
snapshot projection instead. The four arrays are mandatory even when empty.

Run the SELECT through an existing authorized read connection and save only the
single `snapshot` JSON value privately. Completeness must be checked against trusted
counts: RLS-filtered results are not necessarily the whole portfolio. No production
snapshot belongs in this public repository, public logs or Actions artifacts.

```bash
python3 -m unittest discover -s tests -p 'test_portfolio_dispatcher.py' -v
python3 -m portfolio.dispatcher --registry portfolio/synthetic-registry.json --tasks portfolio/synthetic-tasks.json --output /tmp/portfolio-plan.json
```

For a local private plan, replace the two input paths with privately held files.
Task input is `{ "tasks": [...], "completed": [] }`. Each task requires a stable
ID (prefer the existing GitHub issue node ID), lane, repository_id, project_id and
head_sha. Build/verify also require required_checks and ci.sha/ci.checks. Optional
depends_on lists task IDs; priority defaults to 100 (smaller goes first).
Do not treat completion labels or task-supplied CI as trusted execution authority.
Outputs include immutable identifiers, lane, selected/held/completed, reason,
input hash and observation time. They are snapshots, not live dashboard state.

## CI reconciliation and production gates

Keep the existing manual bootstrap and registry synchronisation PR unchanged.
A green registry unit-test job with reconcile skipped is not a credential-backed
integration success. Service-role credentials are not read-only credentials.
Follow `PROJECT-GPT-OS-CREDENTIAL-GATE.md` before any unattended registry read.
Existing application quality gates and preview requirements continue to apply to
their own repositories; this stdlib-only planner has its own acceptance suite.

The next implementation must obtain current head/check evidence from an allowlisted
GitHub API reader, verify snapshot scope/freshness, and add transactional task claims
and expiry in an isolated test database before workers execute anything. Reuse
existing issue IDs and registry relationships; do not invent a competing registry.
Test replay, duplicate delivery, retries, timeouts and claim races before proposing
production writes. Workers must have fixed commands per lane, no arbitrary shell
from task content, and may only create reviewable branches/PRs.

GitHub Actions concurrency here protects synthetic runs in this repository only.
It is not a durable queue or a global lock across repositories. A subsequent
worker design needs durable claims plus a shared repository lock in the existing
registry domain. No schedule or production execution is enabled by this PR.

## Rollback

Close the unmerged PR to abandon it. After a separately approved merge, revert
only these additive files. There is no database rollback because no database
changes are part of this component. No deployment is needed to test this release.
