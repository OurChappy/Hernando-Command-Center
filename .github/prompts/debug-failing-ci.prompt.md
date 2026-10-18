---
description: Evidence-backed diagnosis of an actual failing GitHub check
---
Read AGENTS.md. Inputs: repository, draft PR, exact current head SHA and failing workflow/run URL. Retrieve the actual failing step/logs. First confirm the check belongs to the current PR head; otherwise HOLD (stale CI).

Identify the smallest reproducible cause, failing test name, file scope and a safe fix with negative regression. Do not infer PASS from missing checks. Provide a Codex-ready bounded handoff, or if explicitly authorised execute the fix on an isolated branch and report command/results/SHA. No merge/deploy/production writes or Railway.
