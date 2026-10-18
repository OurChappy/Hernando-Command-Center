# Idea-to-Delivery Workflow v1 — proposed governance contract

Status: DRAFT. Scope: OurChappy repositories. GitHub remains the source of truth for code, issues, PRs and CI; existing Project GPT OS Supabase records remain the structured registry. This document does not enable execution or write to Supabase.

## Stages and gates

| Stage | Input | Artifact / action | Owner | Exit gate |
|---|---|---|---|---|
| 0. Capture | Idea, problem, or observed failure | Idea record, provenance, desired outcome, non-goals | Portfolio owner | Evidence vs hypothesis marked |
| 1. Discover | Idea | Read-only source/registry/PR scan, collision check | ChatGPT Work | Existing work and canonical IDs cited |
| 2. Decompose | Validated intent | Epic, independently testable tasks, dependency DAG, acceptance tests | Director | Each task scoped to one repo |
| 3. Register | Approved breakdown | GitHub issue(s) linking registry project/item IDs; no new IDs inferred | Director | Exact source link, priority and blocker owner |
| 4. Admit | Candidate issues | Read-only portfolio plan with repo lock, lane and CI evidence | Dispatcher | Max 3 lanes, distinct repos, verified mappings |
| 5. Implement | Admitted build/repair task | Codex branch, constrained file scope, commits, draft PR | Codex | Local command outputs and exact SHA |
| 6. Validate | Draft PR | Unit/integration/synthetic/security tests, PR reviews, CI links | Verify lane | Required checks pass on PR head SHA |
| 7. Decide | Evidence packet | Human decision: revise, hold, approve merge or release separately | Owner | Explicit action-specific approval |
| 8. Reconcile | Reviewed outcome | Issue status, PR refs, registry change proposal, dashboard | Director | No claim of completion without evidence |

## Canonical task contract

Each task must have: existing `project_id`, `registry_item_id`, GitHub `repository_id`, repository full name, GitHub issue number/URL (once created), task ID, title, objective, evidence links, hypothesis/verified classification, lane (`repair`, `build`, `verify`), priority, dependencies, blocking reasons, acceptance criteria, test commands, expected outputs, security/scope boundary, current head SHA and freshness timestamp. Leave unknown identifiers NULL and hold admission. Never synthesize registry IDs.

Task lifecycle: `idea -> discovery -> scoped -> issue_ready -> admitted -> in_progress -> draft_pr -> testing -> review -> completed`. Alternative outcomes: `blocked`, `cancelled`, `superseded`. Only mark completed after passing tests, review evidence and approved disposition; no production deployment implied.

One GitHub issue represents one independently testable deliverable; an epic groups issues. A pull request links its issue(s), changed scope, exact commit SHA, CI runs, test commands/results, rollback, risks and outstanding blockers. Do not create an issue or PR when an existing canonical one already serves the scope.

## Parallel execution contract

At most three admitted tasks, one per lane and one per repository across the entire batch. A task's dependencies must be *already completed*, not selected simultaneously. Shared files, migrations, cross-repository consumers, missing registry mapping, uncertain CI, untrusted task instructions or outstanding security findings force HOLD. Prefer work that unblocks the next steps. Deterministic order: repair before build before verify, then priority and stable task ID.

Work handles substantive audits, PR reconciliation and evidence gathering. Codex handles bounded changes only after a handoff with precise files, tests and rollback. Independent verification must examine actual PR-head test runs rather than infer success from an issue, plan or preview status.

PR #2 already implements an **offline plan-only** three-lane dispatcher and synthetic parallel matrix. It does NOT claim tasks or launch actual workers. Before live parallel execution, implement and test durable task claims, expiry, global repository locks, idempotent retries, stale-SHA rejection, least-privilege worker identity and audit trails in an isolated environment. Never feed arbitrary task text into shell execution.

## First cohort — proposed only

1. Script-Station / REPAIR: unblock PR CI validation and inspect release/security issues #28/#29; check PR #24 and newest head/checks. No merge or workflow bootstrap to main without owner approval.
2. Hernando-Command-Center / VERIFY: assess PR #2 planner and issue #5 provider-backed dry-run requirements; read-only only. Do not treat green synthetic CI as live authentication evidence.
3. goodturn-brand / BUILD (planning/reconciliation first): scope issue #24 Course Clarity PR consolidation. Implementation blocked until overlap and native Excel QA are established; no client-ready or release claim.

## Cycle reports and stop rules

Dashboard fields: cycle timestamp, source freshness, three selected/held lanes, project, repo, issue, PR, exact SHA, tests/run URLs, blocker/owner, next action and approval required. Label every statement VERIFIED (direct evidence), REPORTED (issue/PR text), PROPOSED, or UNKNOWN.

STOP on attempted production writes, merges, deployments, permission/secret changes, Railway use, unexpected provenance, failing required checks, stale evidence, conflicting files, or uncertain repository ownership. Escalate to owner with a decision record.

## Verification checklist for this governance-only PR

- [ ] Review against PR #2 dispatcher semantics, including max-three and distinct repo gates.
- [ ] Verify any proposed task has a real repository ID and registry item/project mapping.
- [ ] Confirm no code execution, Supabase write, worker dispatch or release is implied.
- [ ] Confirm all GitHub issue and PR links are real before publishing a status assertion.

Reference: https://github.com/OurChappy/Hernando-Command-Center/pull/2
