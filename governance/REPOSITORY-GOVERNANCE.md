# OurChappy repository governance (review-only)

This is a navigation and management proposal for **15 existing repositories**. It changes no repository name, visibility, default branch, settings, ownership, production records or deployment. Use `repository-directory.json` as a **review manifest**, never as executable instructions for an automatic migration.

## Decisions
1. **Hernando-Command-Center** owns the cross-repository directory, canonical record references, operational documentation and registry governance.
2. **Script-Station** owns the Project GPT OS user experience and development tools, but not the canonical source record IDs held by the registry.
3. **Chatgpt** and **agentskills** own definitions/skills respectively; do not copy definitions into Script-Station without a documented reason.
4. Business/product applications live in their existing repos (Goodturn and education data); integrations such as TAFE MCP stay independently deployable.
5. Keep reference forks, prototypes and experiments until provenance and licences are reviewed. Size zero is **not** authorisation to delete or archive.
6. Never merge repository histories to solve catalogue navigation; link by verified provider ID `owner/repo` and stable GitHub numeric repository ID.

## PR workstreams
- REGISTRY: #55 and #56 — overlapping discovery proposals; source-bound reconciliation first.
- CONSOLE: #52, #53, #57 — verify whether the newer console supersedes earlier static explorer and adapter; leave the existing branches intact.
- AGENT_BUILDER: #22, #45, #50, #51 — document stacking and acceptance, don't bypass tests.
- EDUCAGEN: #19 and #20 — separate product lane; PR #20 is stacked.
- CI: #24 — assess workflow consolidation before modifying required checks.

The PR inventory is **partial** and statuses must be refreshed before any close, retarget or merge action.

## Review gates
- No automatic repository reassignment, archive, deletion, transfer or rename.
- Never rewrite Supabase UUIDs, repository IDs, external reference IDs or historical issue numbers.
- Approve project ownership and provenance separately, then update canonical records only under a separately authorised write plan.
- Verify code/tests/CI before promoting build items beyond `discovered` or `in_review`.
- Avoid creating more independent draft PRs for each catalogue tweak; iterate one focused workstream at a time after resolving bases.
