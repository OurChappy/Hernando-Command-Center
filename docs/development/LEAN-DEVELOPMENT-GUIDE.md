# Lean Development Guide

Applies to Hernando-Command-Center. Adapted from the Script-Station lean development standard.

**Goal:** ship useful, small changes without duplicating workflows, tests, or governance.

1. Define one observable outcome per PR.
2. Inspect existing GitHub assets and Supabase registry records before creating anything new. Preserve stable identifiers.
3. Reuse existing workflows and components; avoid parallel registries and unnecessary abstractions.
4. Match verification to risk: docs use focused review; application/integration changes use relevant tests; database, credentials and production writes require targeted safety checks and explicit approval.
5. Run existing CI; don't introduce duplicate CI jobs solely to implement this guide.
6. Keep PRs small. State outcome, verification, risk and release impact.
7. Prefer idempotent, additive, reversible changes and dry runs before writes.
8. Stop when relevant checks and acceptance criteria pass; avoid redundant test cases and planning loops.
9. Never treat merging as authorisation to deploy, mutate production data or alter permissions.
10. Escalate only meaningful risks or business decisions.

## Minimal done criteria
- Outcome delivered and existing IDs/components reused
- Relevant verification performed and applicable CI green
- Review completed; meaningful risk/rollback noted
- Production-impacting actions separately approved

## Local constraints
- Keep the existing `career-artifact-publisher.yml` and `project-gpt-os-bootstrap.yml` workflows unchanged until their actual purpose and dependencies are audited.
- Do not introduce Railway.
- This document does not enable automatic merging, scheduled updates, deployment, or Supabase writes.

## Workflow
Inspect → Implement → Verify → Review → Merge → Release (only when authorised).
