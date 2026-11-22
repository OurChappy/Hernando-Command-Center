# OurChappy portfolio architecture — target v2

**Status:** DESIGN PROPOSAL — not deployed or approved for production changes. **Baseline:** 23 November 2026, 19 GitHub repositories.  
**Companion machine-readable register:** [ourchappy-repository-register.v1.json](./ourchappy-repository-register.v1.json).

## Executive decision

Keep product/service deployables isolated; consolidate *ownership, standards, duplicate implementations, evidence, dashboards and discoverability*. Do not optimise for a fixed repository count. The previous aspirational 10–12 target is NOT a verified achievable count and must not drive unnecessary mergers. External forks, learning repos and websites should not be combined with operational source.

## Layered target design

```text
OurChappy — GitHub organisation (existing)
│
├── CONTROL PLANE: Hernando-Command-Center (existing; optional rename only later)
│   ├── canonical source/project/agent registry (Supabase; controlled writer)
│   ├── repository catalogue, decisions and approval workflow
│   └── Rosie Chief of Staff read-only dashboard candidate
│       consumes explicit versioned reports; does not duplicate jobs
│
├── EXECUTION PLANE: Script-Station (existing)
│   ├── AppleScript / launchd Housekeeping, scripts, evidence
│   ├── internal script/resource metadata in 01-DATA
│   ├── registry-compatible read-only adapter and user-facing Project GPT OS candidate
│   └── isolated tests and operational runbooks
│
├── CONNECTOR PLANE: portalflow-ai (existing)
│   └── external action gateway and upload product (independent deploy/auth)
│
├── INDEPENDENT PRODUCTS
│   ├── pagesmith-agent
│   ├── EducationDataProduct-au -> contracted TAFE connector
│   ├── tafe-browser-mcp -> proposed standalone canonical implementation
│   ├── goodturn-moodle
│   └── pechakucha-studio-private
│
├── BUSINESS IP & PORTFOLIO
│   ├── goodturn-brand (strategy, brand, offer specs; no customer records)
│   ├── Portfolio (curated index / links, not binary duplicate)
│   ├── Advanced-Power-BI-Projects (large analytical assets)
│   └── acnc-nonprofit-analytics-study-case (independent case study)
│
├── DEVELOPMENT WORKSPACE: Chatgpt
│   └── preserve AI framework and independent Phoenix Investor;
│       evaluate Project GPT OS redundancy via feature/deployment comparison
│
└── REFERENCE / LEARNING / WEB
    ├── agentskills, ui, stripe-python (track upstream; do not bulk import)
    ├── skills-idea-to-merge-with-the-copilot-app
    ├── skills-copilot-codespaces-vscode (empty)
    └── LittleGrumble.github.io (CNAME/DNS check before archive)
```

This is *logical ownership*, not a confirmed deployed topology. Avoid new repos and renames until existing source is reconciled. If `Rosie` is introduced as a brand, use it as a UI layer/alias first, not a second central registry.

## Source of truth rules

| Capability | Canonical candidate | Consuming boundary | Forbidden duplicate |
| --- | --- | --- | --- |
| Projects, source identities, agents, external references | Command Center Supabase registry | Script Station v1 private read-only export | Script Station writing an independent central registry |
| Mac scripts, launchd definitions and Housekeeping evidence | Script-Station | Rosie health report/approval queue | Second launchd installer or duplicate scheduled job |
| Service/API connector operations | portalflow-ai | Approved client contracts | Copying connector secrets into application repos |
| TAFE student account MCP | tafe-browser-mcp | EducationDataProduct-au | Silent two-codebase production deployment |
| Project GPT OS app | Script-Station *candidate* | Command Center registry + legacy Chatgpt feature analysis | Auto-retiring Chatgpt app without feature parity and deploy check |
| Goodturn brand/IP | goodturn-brand | EducationDataProduct-au and goodturn-moodle | Copying original brand files without asset/version ownership |
| Public portfolio index | Portfolio | ACNC and Advanced-Power-BI-Projects via links | Duplicating datasets and PBIX binaries |

**Naming principle:** prefer stability. Retain current names during Sprint 03; introduce tags, repository description and owner metadata before any rename. An organisation rename can break documentation, CI, action references, domains, npm/Next integration and deploy links even if GitHub redirects many browser URLs.

## Proposed repo classifications — no destructive action
- **Keep active:** Script-Station, Hernando-Command-Center, portalflow-ai, Chatgpt, pagesmith-agent, EducationDataProduct-au, tafe-browser-mcp, goodturn-brand, goodturn-moodle, pechakucha-studio-private, Portfolio, Advanced-Power-BI-Projects, acnc-nonprofit-analytics-study-case.
- **Reference upstream:** agentskills, ui, stripe-python.
- **Review for archive only after dependencies checked:** LittleGrumble.github.io, skills-idea-to-merge-with-the-copilot-app, skills-copilot-codespaces-vscode.
- **Propose selective subdirectory migration, not cross-repo merge:** embedded TAFE MCP and unique Project GPT OS components after runtime checks.
- **Propose internal cleanup:** ACNC duplicate working trees and old feature branches only after PR/head reconciliation.

## Enablement plan (explicit conditions)

| Feature | Current evidence | Enable now? | Required checks |
| --- | --- | --- | --- |
| Read-only repository catalogue | This JSON register; GitHub metadata inspected | **Yes: draft document only** | PR review; publish/merge approval |
| Standard project metadata + PR templates | Existing templates in some repos | **Design only** | Respect repo-specific policy and CODEOWNERS |
| Read-only Rosie status aggregation | Existing Housekeeping/registry-compatible adapters | **After verification** | Mac evidence freshness, auth, privacy, cache and stale-state indicators |
| Command Center central registry sync | Manual gated apply design documented | **No** | Credentials-backed dry-run, one approved idempotent insert, audit & rollback |
| Mac launchd automatic recovery | Existing operational code | **No changes** | Live job inventory, rollback, safe maintenance window |
| TAFE Railway MCP service | railway.toml + Dockerfile in source | **No deployments** | Active SHA, MFA/session, smoke, health and privacy |
| Project GPT OS production cutover | Two divergent app implementations | **No** | Route/API matrix, Supabase/auth compatibility, deployment health |
| Autonomous PR auto-merge | Not required for this redesign | **No** | Branch protection, risk classification, human review |
| New scheduled portfolio scans | Existing separate jobs mentioned in repos | **No** | Inventory and dedupe existing schedules |
| Archiving / renaming legacy repos | Possible candidates identified | **No** | DNS, dependencies, licence, redirects and owner approval |

## Shared baseline to standardise incrementally
1. Each maintained repo: README purpose/owner, deployment/runtime mode (or explicit none), data sensitivity, working test command, support & rollback contact.
2. `docs/architecture/ownership.md`: canonical writer, readers, API/schema version and upstream/downstream dependencies.
3. `docs/operations/runbook.md` for deployed repos only: secrets as variable *names* (never values), health checks, recovery gates and restore path.
4. Repo-specific `AGENTS.md`, PR template and minimal CI; do not blindly copy CI triggers, nor grant write permissions for docs-only PRs.
5. Tags can be `domain:operations`, `domain:product`, `domain:portfolio`, `domain:reference`, and `status:active` / `status:review` after verifying repository settings permissions.
6. Publish cross-repo inventory through a redacted, read-only view, showing source timestamp, owner and provenance; avoid putting private repository metadata into public artifacts.

## Migration waves and acceptance
**Wave 0 — documentation (this PR):** machine-readable 19-repo matrix, target design, explicit non-goals. No code or workflow changes.

**Wave 1 — interfaces:** review [Script Station boundary proposal](https://github.com/OurChappy/Script-Station/pull/84) and [TAFE MCP boundary proposal](https://github.com/OurChappy/EducationDataProduct-au/pull/2). Verify v1 registry export contract and discover actual MCP consumers. Draft test-only contract PR if tests can run without live credentials.

**Wave 2 — identity and feature parity:** compare all Project GPT OS routes and deployment references; preserve standalone Phoenix Investor. Validate application tests in isolated branches. No data migration until backup and auth checks pass.

**Wave 3 — optional cutovers:** an explicit approved PR per bounded change; live smoke tests, rollback and post-cutover reconciliation. Only then consider renaming or archiving.

**Exit criteria per cutover:**
- Verified source+target commit SHAs, no unmerged PR functionality lost.
- Confirmed downstream consumers, CI trigger and workflow permission deltas.
- Licence/secret/data privacy check; no real private files committed.
- Repeatable tests for equivalence; independent runtime smoke.
- Before/after ownership registry and rollback proof.
- Explicit owner approval for every production edit.
- No accidental duplicate scheduled jobs.

## Evidence & uncertainty
- Sprint 01 inventory and read-only audit: [Script-Station draft #83](https://github.com/OurChappy/Script-Station/pull/83).
- Sprint 02 registry and Project GPT OS boundary: [Script-Station draft #84](https://github.com/OurChappy/Script-Station/pull/84).
- Sprint 02 duplicate TAFE MCP boundary: [EducationDataProduct-au draft #2](https://github.com/OurChappy/EducationDataProduct-au/pull/2).
- Default-branch source trees, selected package manifests/workflows and branch enumerations were inspected on 2026-11-23; *not* every open PR/branch diff, workflow run, secret permission, deployed SHA, or local Mac/Docker/Dify runtime was verified.
- Target repository count is NOT an acceptance criterion.
- This document does not claim that any roadmap component has been enabled, deployed, merged or tested end-to-end.
