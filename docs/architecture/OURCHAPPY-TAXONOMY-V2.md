# OurChappy taxonomy v2 — repository topics and work labels

**State: DRAFT / NOT APPLIED** · 2026-11-23 · [Machine-readable catalogue](./ourchappy-taxonomy-v2.json)

## Purpose
Provide one practical classification system for OurChappy's 19 audited GitHub repositories without confusing product ownership, code lifecycle, production health, and PR approval. No GitHub settings or existing labels were changed.

## Two layers, not one giant label list

### Layer A: GitHub repository **topics** (stable identity)
| Dimension | Prefix | Meaning | Cardinality |
| --- | --- | --- | --- |
| Domain | `domain-` | Operating context | Exactly 1 |
| Product | `product-` | Product family only when confirmed | 0–1 |
| Role | `role-` | Canonical bounded responsibility | Exactly 1 |
| Lifecycle | `lifecycle-` | Portfolio classification, NOT uptime | Exactly 1 |

For each of 19 repositories, see the JSON. Examples:
- `Hernando-Command-Center`: `domain-operations`, `product-rosie`, `role-control-plane`, `lifecycle-review`. Rosie branding is a **proposal** and may need owner confirmation.
- `Script-Station`: `domain-operations`, `product-rosie`, `role-execution`, `lifecycle-active`.
- `goodturn-brand`: `domain-education`, `product-goodturn`, `role-brand`, `lifecycle-active`.
- `EducationDataProduct-au`: `domain-education`, `role-application`, `lifecycle-review`; **do not assert Goodturn ownership** until verified.
- `stripe-python`: `domain-reference`, `role-upstream-reference`, `lifecycle-reference`.

**Lifecycle meanings:** active = intended maintained portfolio asset; review = ownership/dependency/retirement decision unresolved; reference = intentionally tracked upstream or educational source. None proves a service is healthy or deployed. Do not tag a repository `archived` until the actual GitHub archive state is confirmed.

### Layer B: Issue & PR **labels** (mutable work metadata)
32 labels in six dimensions (full names, descriptions and hex colours in JSON):

| Dimension | Values | Selection |
| --- | --- | --- |
| `type:` | bug, feature, enhancement, refactor, docs, test, chore, security | Exactly one per PR |
| `area:` | registry, automation, integration, app, data, ci, docs | One or more |
| `priority:` | p0, p1, p2, p3 | At most one |
| `risk:` | low, medium, high, production | One for high-impact changes; production indicates live impact rather than a point on a severity scale |
| `state:` | needs-evidence, blocked, ready-for-review, approved | At most one; must not override GitHub native review or merge state |
| `migration:` | assess, consumer-check, parity, cutover-proposed, rollback-ready | Only for consolidation and migration work |

**Important:** `state:approved` must be applied only with independently recorded explicit approval. It is not an instruction to merge or deploy. `risk:low` never waives branch protections.

## Visual display guidance

```text
OurChappy / ROSIE / Script Station                 [Portfolio: active]
Operations · Execution service
Mac automation | Housekeeping
--------------------------------------------------
PR: Registry read-only adapter
type:refactor   area:registry   priority:p2
risk:medium     state:needs-evidence
```

In a dashboard, show the product + repository identity prominently; render topics as human-readable subtitles and display PR labels only for work items. Do not expose private operational repositories on a public portfolio page without an approved privacy review.

## Examples for actual draft PRs (illustrative only)
- Script-Station #83 (inventory): `type:docs` `area:docs` `priority:p2` `risk:low` `state:ready-for-review`
- Script-Station #84 (registry boundaries): `type:docs` `area:registry` `risk:low` `migration:assess`
- EducationDataProduct-au #2 (TAFE ownership): `type:docs` `area:integration` `risk:low` `migration:consumer-check`
- Hernando-Command-Center #53 (architecture): `type:docs` `area:docs` `risk:low`
- Hernando-Command-Center #54 (first label proposal): `type:docs` `area:docs` `risk:low`

These are examples, not applied labels or assertions that any PR has passed review.

## Existing labels & backward compatibility
Keep repository-specific labelers. In particular `Chatgpt/.github/labeler.yml` contains legacy path-based `area/apps`, `area/packages`, etc., while this standard proposes `area:app` and related labels. DO NOT delete legacy labels or change automated labeler workflows until all affected PRs and mappings are checked.

The v1 draft uses `status:` and `migration:assessment`; v2 uses `state:` and `migration:assess`. Treat this as a **proposal** not an automated migration. v1 PR is https://github.com/OurChappy/Hernando-Command-Center/pull/54.

## Safe rollout checklist
1. Approve taxonomy semantics and owner associations; compare with the already drafted portfolio redesign PR #53.
2. Enumerate existing topics and all issue/PR labels in each repository; document collision and automation impact.
3. Verify permissions to create/modify labels and repository topics and snapshot current metadata.
4. Pilot one repo with approval; check search filters, existing automation and native PR state.
5. Apply in batches only after verification; document before/after/rollback; avoid public leakage of private repo metadata.
6. Use change review gates for production risk; never automatically merge, rename, deploy, schedule or archive based on label values.

## Explicit non-actions
No repository names, topics, labels, workflow files, deployment configurations, schedules or branch rules were modified by this proposal.
