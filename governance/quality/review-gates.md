# OurChappy risk-based independent review gates v1.1

Source: programme #10, milestones #16–#19, execution plan draft PR #42, Accelerator Kit PR #43.

| Change type | Risk | Before implementation | Before technical acceptance | Before release |
|---|---|---|---|---|
| Documentation/template only | Low | Product Challenger (as applicable) | QA & Security Reviewer + actual template tests | Evidence Auditor if published |
| Internal code with no external writes | Medium | Architecture Reviewer | QA & Security Reviewer + tests/CI | Evidence Auditor |
| UI or customer-facing behaviour | Medium | Product Challenger + Architecture Reviewer | QA & Security Reviewer + UX/accessibility human review | Evidence Auditor |
| Auth, secrets, external write, migrations | High | Product Challenger + Architecture Reviewer | QA & Security Reviewer + independent security signoff | Evidence Auditor + explicit owner approval |
| Merge, deploy, production writes, permissions, Railway | Protected | Design/review only | Evidence and tests required | Explicit owner authorisation for the *specific action* |

## Agent outcome contract
- PASS: evidence supports stated acceptance for the observed SHA, and no mandatory gates missing.
- HOLD: sources, CI or approval missing/stale; must not infer success.
- FAIL: substantive confirmed defect, violated requirement or unauthorised scope.
- Distinguish verified tests from proposed tests; release decision is always separate from successful CI.
- Agents may share a source snapshot but reviews should independently challenge each other's assumptions.
- Global maximum 3 independent repository-scoped work lanes; never run competing writers against one repo.
