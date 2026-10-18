---
description: Review a draft PR against acceptance and repository security gates
---
Read AGENTS.md, parent issue and PR #42 execution-plan entry. Fetch PR changed paths and latest head SHA; compare with issue boundaries and overlapping draft PRs. Require real test commands/logs and hosted check conclusions on *the same head SHA*. Check secrets, overbroad permissions, new dependencies, idempotency and negative tests. Distinguish VERIFIED, REPORTED, PROPOSED and UNKNOWN. Return PASS / HOLD / FAIL with evidence URLs, blocker severity and next smallest remediation. Never merge or deploy.
