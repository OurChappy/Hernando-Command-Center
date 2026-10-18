# Goodturn Moodle — implementation register v1.0

Status: **Proposed; execution pending**. Source repository intended: `OurChappy/goodturn-moodle` (not yet created). This file is an intake and delivery plan, **not evidence of Moodle implementation**.

## Delivery rules
- Local development before cloud; non-accredited pilot with synthetic learners.
- Keep upstream Moodle unmodified; pin supported Moodle and moodle-docker revisions after validating current compatibility.
- No credentials, production DB, learner PII, submissions or backups in Git.
- Draft PRs for changes; no merge, public deployment, spending, rights modifications or production data writes without approval.
- Record exact tested commit SHA, commands, outputs, gaps and independent reviewer decision.
- Each task requires a separate acceptance proof; parent milestone closes only after all proof and its gate.
- Proposed architecture: GitHub-managed config + official development Docker; separate production VPS, PostgreSQL, private moodledata and offsite backups.

## Estimated engineering effort
M0 5–8h; M1 10–16h; M2 6–10h; M3 10–16h; M4 12–20h; M5 15–25h; M6 12–20h; M7 12–24h; M8 12–20h; M9 15–25h; M10 10–18h; M11 15–25h; M12 10–20h. Total **144–255h** excluding extensive content authoring, custom AI and recurring operations. All are planning estimates.

## Milestone task breakdown
### M0 — Architecture & intake
Dependencies: none
- [ ] **M0-01** Confirm users/course pilot and non-accredited status. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M0-02** Inventory OurChappy repos and potential reuse. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M0-03** Document ownership and boundaries. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M0-04** Choose Moodle supported version and pin strategy. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M0-05** Specify privacy/data classification and threat model. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M0-06** Define issue/PR conventions and definition of done. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M0-07** Approve architecture decision records. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Scope approved; no duplicate app owner.

### M1 — Reproducible local environment
Dependencies: previous milestone gate
- [ ] **M1-01** Pin moodle-docker commit and Moodle release. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M1-02** Add .env.example without secrets. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M1-03** Set PostgreSQL and PHP compatibility matrix. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M1-04** Document arm64 and amd64 handling. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M1-05** Create make setup/start/stop/reset targets. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M1-06** Add local SMTP sink and isolated volumes. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M1-07** Validate compose config and supply-chain provenance. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Fresh clone configuration validates in CI.

### M2 — Mac runtime validation
Dependencies: previous milestone gate
- [ ] **M2-01** Install Docker Desktop Apple Silicon. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M2-02** Clone approved project. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M2-03** Boot containers with local-only ports. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M2-04** Run Moodle CLI installation. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M2-05** Check database persistence and cron. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M2-06** Exercise login/logout and mail sink. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M2-07** Verify cold restart and reset procedure. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Mac M3 Pro smoke test evidenced.

### M3 — CI & software quality
Dependencies: previous milestone gate
- [ ] **M3-01** Add shellcheck and yamllint. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M3-02** Validate env key completeness. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M3-03** Add PHP syntax/config checks. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M3-04** Add secret scan and dependency alerting. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M3-05** Build ephemeral DB integration smoke test. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M3-06** Publish SHA and test evidence. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M3-07** Introduce PR gating and maintenance owners. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Required CI passing on tested commit.

### M4 — Learner experience
Dependencies: previous milestone gate
- [ ] **M4-01** Configure course taxonomy and enrolment. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M4-02** Set admin/trainer/learner role matrix. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M4-03** Create accessible branding prototype. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M4-04** Configure navigation and dashboard. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M4-05** Document learner invitation flow. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M4-06** Check mobile and keyboard interaction. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M4-07** Test privilege boundaries. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Roles and learning portal accepted.

### M5 — Course pilot
Dependencies: previous milestone gate
- [ ] **M5-01** Define learning outcomes and target persona. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M5-02** Write course map and lesson plans. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M5-03** Prepare accessible content assets. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M5-04** Build four learning activities. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M5-05** Produce five-question diagnostic quiz. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M5-06** Enrol synthetic students. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M5-07** Test learner journey and collect defects. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Pilot course usable end-to-end.

### M6 — Assessment & progress
Dependencies: previous milestone gate
- [ ] **M6-01** Map outcomes to questions and rubric. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M6-02** Configure question bank and quiz attempts. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M6-03** Add assignments with feedback. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M6-04** Test completion criteria and gradebook. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M6-05** Add reattempt/recovery pathways. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M6-06** Check trainer/student grade visibility. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M6-07** Export test completion evidence. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Grading and progress tests pass.

### M7 — Analytics & integration
Dependencies: previous milestone gate
- [ ] **M7-01** Inventory native Moodle reports and APIs. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M7-02** Define data contracts and consent basis. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M7-03** Specify service-account least privilege. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M7-04** Build read-only sample reporting export. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M7-05** Validate schema, IDs and timezone. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M7-06** Add error/retry and audit logs. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M7-07** Document Goodturn boundary and no direct DB writes. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Read-only export verified on synthetic data.

### M8 — Security/privacy/recovery
Dependencies: previous milestone gate
- [ ] **M8-01** Conduct threat model and data inventory. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M8-02** Set data retention and deletion policy. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M8-03** Verify MFA and access controls. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M8-04** Define patching vulnerability response. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M8-05** Automate encrypted offsite DB+files backups. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M8-06** Restore into isolated environment. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M8-07** Review Australian Privacy Principles applicability. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Documented restore and security review.

### M9 — Production infrastructure
Dependencies: M0–M8 and explicit paid-host approval
- [ ] **M9-01** Approve budget region and domain. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M9-02** Select supported VM and sizing. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M9-03** Provision Ubuntu and locked-down access. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M9-04** Configure Nginx TLS PHP PostgreSQL cron. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M9-05** Configure email DNS SPF DKIM DMARC. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M9-06** Set monitoring alerting and log controls. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M9-07** Provision independent backup destination. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Secure cloud staging built after approval.

### M10 — Release engineering
Dependencies: previous milestone gate
- [ ] **M10-01** Pin tested build artefacts. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M10-02** Create staging rehearsal and synthetic migration. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M10-03** Verify staging production parity. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M10-04** Run performance and accessibility checks. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M10-05** Test rollback and upgrade scripts. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M10-06** Publish release notes and risk register. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M10-07** Obtain deployment change approval. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Release candidate signed off.

### M11 — Invited pilot
Dependencies: previous milestone gate
- [ ] **M11-01** Define small cohort and invitation criteria. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M11-02** Publish pilot privacy/consent notice. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M11-03** Invite only approved users. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M11-04** Observe course completion and feedback. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M11-05** Evaluate errors performance and accessibility. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M11-06** Prioritise and remediate launch blockers. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M11-07** Document pilot findings and go/no-go. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Pilot report and exit gate approved.

### M12 — Launch & maintenance
Dependencies: previous milestone gate
- [ ] **M12-01** Approve public launch and domain cutover. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M12-02** Verify backups monitoring alerts on production. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M12-03** Publish learner guidance and support process. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M12-04** Document incident escalation and recovery objectives. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M12-05** Schedule patching and upgrade cadence. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M12-06** Establish analytics and course quality reviews. Evidence: linked PR/test transcript or approved decision record.
- [ ] **M12-07** Conduct 30-day postlaunch assessment. Evidence: linked PR/test transcript or approved decision record.
**Exit gate:** Named owner and operations evidence.

## Release stop conditions
Any unresolved critical vulnerability; real personal data in development or Git; untested restore; unsupported dependency; missing course/role security checks; unapproved hosting/domain expenditure; absent incident owner.

## Handoffs
**GitHub-only first:** M0, portions of M1/M3, templates, documentation, offline validation.
**Requires owner's Mac:** M2 and device-specific M1 checks.
**Requires cloud account and explicit approval:** M9/M10.
**Requires real consented participants and operational owner:** M11/M12.

## Dependency and reuse investigation
2026-10-19 initial connector checks: repository search `org:OurChappy moodle` returned no matching repository; issue search `moodle org:OurChappy` returned no issues. Existing `OurChappy/goodturn-brand` is private and `OurChappy/Hernando-Command-Center` is public; neither is designated as the LMS codebase. Further inventory/reuse assessment remains required.
