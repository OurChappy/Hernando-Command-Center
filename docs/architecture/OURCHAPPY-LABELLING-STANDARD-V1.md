# OurChappy classification & labelling standard v1.0

**Status: PROPOSED / NOT APPLIED.** Audit context 2026-11-23. Use with [ourchappy-labels.v1.json](./ourchappy-labels.v1.json) covering all 19 existing repositories and 22 standard issue/PR labels.

## Three distinct metadata layers

1. **Repository name** identifies durable product/capability, e.g. `Script-Station` (rename candidates are handled separately).
2. **GitHub topics** classify repository domain, product family, responsibility, lifecycle; topics are searchable on repository discovery and use lower-case kebab-case.
3. **Issue/PR labels** classify work type, impacted area, risk, review state and migration stage. These are NOT GitHub topics.

Do not use issue labels to imitate a repository directory tree; do not create a label for every repository or every agent. GitHub topics are not permission boundaries.

## Repo topics
Each repo may carry a compact set (usually 3–5):
- `domain-operations`, `domain-platform`, `domain-engineering`, `domain-education`, `domain-product`, `domain-portfolio`, `domain-research`, `domain-web`, `domain-reference`, `domain-learning`
- Product family only when evidence supports it: `product-rosie`, `product-portalflow`, `product-pagesmith`, `product-goodturn`, `product-pechakucha`
- Responsibility: `role-control-plane`, `role-execution`, `role-integration`, `role-workspace`, `role-application`, `role-brand`, `role-showcase`, `role-case-study`, `role-website`, `role-upstream-reference`, `role-training`
- Lifecycle: `lifecycle-active`, `lifecycle-review`, `lifecycle-reference`

**Interpretation:** `lifecycle-active` denotes a current portfolio asset, NOT verified production health or commit activity. `lifecycle-review` is an assessment state, NOT approval to archive. Product family tags on conditional ownership (e.g. EducationDataProduct-au) require review before applying.

## Issue and PR labels
Adopt 22 standard labels from the JSON catalogue:
- Work type (choose exactly one): `type:bug`, `type:feature`, `type:docs`, `type:refactor`, `type:security`, `type:chore`.
- Area (choose one or more): `area:registry`, `area:automation`, `area:integration`, `area:app`, `area:ci`, `area:data`.
- Risk (one, subject to revision after review): `risk:low`, `risk:medium`, `risk:high`, `risk:production`. Never treat label alone as merge permission.
- Status (at most one current state): `status:needs-evidence`, `status:blocked`, `status:ready-for-review`. GitHub native draft/open/merged state remains authoritative.
- Migration (optional and relevant only for consolidation): `migration:assessment`, `migration:consumer-check`, `migration:cutover-proposal`.

Example PR classification for [Script Station #84](https://github.com/OurChappy/Script-Station/pull/84) would be `type:docs`, `area:registry`, `risk:low`, `migration:assessment`. This is an illustrative mapping; NO labels have been attached by this change.

## Proposed rollout and gates
1. Review machine-readable topic assignments for all 19 repositories, particularly private repo metadata and product association.
2. Inspect existing topics and labels in each repository; preserve custom labels, avoid duplicate or colliding names, compare exact color/description conflicts.
3. Pilot in one low-risk repository. Repo topics require repository metadata write capability; issue/PR labels require label creation/admin rights. Do not assume the current connector supports these operations.
4. Record before/after metadata for rollback; apply only with explicit approval to change GitHub repository settings.
5. Avoid running automated labelers or adding workflows simply to standardise labels. Existing `Chatgpt/.github/labeler.yml` includes `area/apps`, `area/packages`, etc.; these are legacy path-based labels and must be mapped carefully before any replacement. Do not remove them without confirming their workflow.
6. Check topic visibility and privacy; public topics should never reveal private project/customer information.

## Explicit non-actions
No GitHub topics, issue/PR labels, repository names, visibility, workflows, branch protection, CI schedules or deployments were changed. This documentation is not operational enablement.

## Acceptance criteria
- [ ] 19 repo assignments reviewed against ownership register
- [ ] Existing GitHub topics and label inventories captured
- [ ] Topic/label collisions reconciled
- [ ] One pilot applied and verified with before/after metadata
- [ ] Rollback instructions recorded
- [ ] Wider rollout separately approved and reviewed
