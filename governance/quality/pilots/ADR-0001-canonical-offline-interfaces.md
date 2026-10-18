# ADR-0001 — Canonical offline portfolio module interfaces (PROPOSED)

Parent: issue #20; programme #10; quality pilot PR #45. Observed from exact draft heads: PR #2 `916b2786db26`, PR #14 `7d1b5785faf3`, PR #15 `023f0da6af4a`. None of these modules was found on `main` during inspection. This ADR is a **proposal**, not accepted architecture or executed integration.

## Decision proposal

| Capability | Existing owner and function | Input contract | Output contract | Decision |
|---|---|---|---|---|
| Idea intake | PR #14 `portfolio/idea_intake.py:propose(idea, inventory)` | `idea` with `title,outcome,repository_id,repository,project_id,registry_item_id,evidence,tasks`; inventory with `repositories,existing_issues` | `schema_version:1,mode:dry_run,status,proposal_key,tasks,issue_markdown,external_writes:0` | Reuse as the single issue-proposal generator |
| Task admission | PR #2 `portfolio/dispatcher.py:plan(snapshot,tasks,completed=())` | `snapshot.schema_version=1`, registry `projects,registry_items,registry_external_refs,registry_dependencies`; tasks with lane/priority/repository_id/project_id/head_sha/CI | `schema_version:1,mode:plan_only,selected,tasks,counts,warnings,input_sha256` | Reuse as the single **offline** selector, not a durable lock |
| PDF worksheet | PR #15 `portfolio/v4/exporter.py:export_pdf(path,cycle_id)` | PDF with 20 expected field names and regex-valid cycle ID | `schema_version:"1.0.0",mode:offline_dry_run,cycle_id,source,stages,external_writes:0` plus Markdown | Reuse as independent worksheet draft importer |
| Artefact envelope | PR #15 `portfolio/v4/schemas/artefact-v1.schema.json` | `schema_version,cycle_id,artefact_type,status,source_refs,payload` | Structured payload with evidence classes | Adopt as **candidate export envelope**, not automatically the dispatcher task contract |

## Compatibility risks (evidence-backed)

1. **Schema-version mismatch:** dispatcher/intake use integer `schema_version=1`; PDF cycle and artefact envelopes use string `"1.0.0"`. Keep **versioned bounded contexts**, with explicit adapters rather than silently coercing data.
2. **Task-shape mismatch:** intake tasks are `id,title,depends_on,acceptance,proposal_key`; dispatcher additionally needs `lane,repository_id,project_id,head_sha,ci/required_checks`. A verified admission enrichment step is mandatory.
3. **Repository identity:** intake validates repository ID **and** full name using inventory; dispatcher resolves provider external identity. An adapter must preserve canonical provider identifiers and require registry snapshot timestamp.
4. **Evidence semantics differ:** intake classes `verified,reported,hypothesis`; exported workbook evidence is unverified free text; dispatcher CI requires exact SHA and `success` checks. Never promote worksheet text into verified CI.
5. **No persistence or execution:** all three advertise offline/no provider writes. Cycle export is **not** cycle registry storage; task selection is **not** a durable repository claim.
6. **Failure behavior:** draft status `proposal_only`, `hold_mapping`, `reuse_or_review` must be mapped to explicit HOLD/admission policy; no new issue created just because proposal exists.

## Safe integration boundary (proposed)

`export_pdf` -> **unverified worksheet draft** -> explicit human/evidence mapping -> `propose` -> **issue proposal** -> approved registry identity and task enrichment -> `plan` -> **non-executing lane suggestions**. Any actual GitHub write, durable claim, execution or production migration requires a separately approved service boundary.

## Required tests before accepting issue #20

- [ ] Negative test mismatched integer vs string schema versions must yield an explicit validation error.
- [ ] Reject intake proposal lacking verified mapping, or with duplicate title; no external issue writes.
- [ ] Reject dispatcher lane admission for missing head SHA, missing CI checks, unknown repository ID or unsatisfied dependency.
- [ ] Reject invalid/colliding PDF field names, malformed cycle ID and encrypted PDF.
- [ ] Provide real compatibility fixtures and run commands on a *single reconciled test branch*; record tested SHA and actual GitHub CI outcome.
- [ ] Record source-level interface matrix, updated base/head SHAs and owner architecture sign-off.

## Status

**HOLD.** The source interfaces have been inspected read-only, but combined compatibility tests, approval, merge readiness and exact-head CI checks for PRs #2/#14/#15 have not been established in this step. Do not merge/deploy/change production records or permissions or use Railway.
