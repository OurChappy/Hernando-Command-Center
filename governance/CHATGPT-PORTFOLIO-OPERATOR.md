# ChatGPT Portfolio Director — operator entrypoint

Status: draft; this is a **prompt-driven, user-invoked workflow**, not a persistent ChatGPT skill, custom app or autonomous Work/Codex dispatcher. Source of truth: GitHub issues, PRs, checks and commits, with read-only Project GPT OS Supabase registry. Companion: `IDEA-TO-DELIVERY-WORKFLOW.md` and PR #2 offline planner.

## Run inside ChatGPT

Keep a dedicated ChatGPT Project named **OurChappy Portfolio Command**. Put the following operating contract in its Project instructions (copy manually; this GitHub file does not update ChatGPT settings):

> Act as Portfolio Development Director. On a "Start development cycle: [idea]" message, run evidence-gated stages: capture; read-only discovery/deduplication across OurChappy GitHub and existing Project GPT OS Supabase records; requirements and repository-scoped issue proposals; dependency graph and max-three independent repository lane plan; scoped draft issue/PR artefacts if appropriate; Work/Codex handoff briefs; verify exact PR-head SHA, tests and CI run URLs; publish dashboard and decisions. Treat reports, drafts and synthetic tests as distinct from implemented/verified functionality. Do not merge, deploy, write production registry records, change permissions, use Railway or imply background/Work/Codex execution without explicit approval or real tool evidence.

Operator message:
`Start development cycle: <business outcome and problem>. Primary repository: <owner/repo>. Constraints: <optional>.`

Follow-up:
`Continue current cycle. Refresh GitHub evidence and latest Supabase registry read-only; advance only eligible tasks, max 3 independent repo lanes; provide actual issue/PR/check URLs, tested SHAs, blockers and next action.`

## ChatGPT orchestration boundaries

- ChatGPT conversation can use connected GitHub and Supabase tools when available; an explicit user message invokes each new cycle. GitHub can receive issues and draft PRs through connected tools. Respect user's specific no-write boundaries.
- ChatGPT Work is a separate mode for substantial, multi-step investigation. A chat preparing a Work brief has **not** started a Work run; handoff occurs only via actual Work experience.
- Codex execution is likewise a separate supported experience; a pasted Codex prompt is not proof a coding session was launched. Verify actual code, branch, draft PR and executed test logs independently.
- PR #2 uses synthetic parallel GitHub Actions and has no live workers or cross-repository durable task claims. Do **not** label it live parallel execution.
- Project instructions persist the operational prompt when the owner configures that Project. This repository file alone does not install a plugin or cause automatic triggers.

## Canonical eight-stage output contract

1. IDEA: explicit outcome, scope, evidence, assumptions, priority.
2. DISCOVER: citations to source issues/PRs, registry identifiers, duplicate/reuse findings, read-only audit timestamp.
3. BREAK DOWN: issue-ready acceptance criteria, per-repo task list, owner, dependency DAG, blockers.
4. REGISTER: existing issue reuse preferred; record newly created GitHub issue links only after successful tool response.
5. ADMIT: at most three repository-distinct repair/build/verify tasks; no unverified dependency, mapping, head or CI evidence.
6. IMPLEMENT: provide bounded Work investigation/Codex implementation handoff; mark **not dispatched** until real invocation is verified.
7. VERIFY: command outputs, exact SHA, run URL/conclusion, tests and outstanding risks; unknown is not pass.
8. DECIDE: user approval separately for merge/release; reconciliation proposals do not mutate production registry.

Every update must label VERIFIED, REPORTED, PROPOSED or UNKNOWN. Include evidence observation time and no-change statement.

## Existing cycle and ownership

- Umbrella epic: https://github.com/OurChappy/Hernando-Command-Center/issues/10
- Intake proposal generator: https://github.com/OurChappy/Hernando-Command-Center/issues/11
- Safe three-repo handoff/evidence: https://github.com/OurChappy/Hernando-Command-Center/issues/12
- Offline dispatcher: https://github.com/OurChappy/Hernando-Command-Center/pull/2
- Repository directory: https://github.com/OurChappy/Hernando-Command-Center/pull/8
- Operating contract: https://github.com/OurChappy/Hernando-Command-Center/pull/9
- Registry authentication gate: https://github.com/OurChappy/Hernando-Command-Center/issues/5

## Evidence and release checklist

Before claiming a stage complete, collect source URLs and source date, verify task dependency status, match live issue/PR and registry identities, inspect the exact PR head and required CI check conclusions, and distinguish local synthetic tests from hosted integration tests. CI or preview success alone is insufficient for production security or release. Never auto-close superseded work. Keep production database, permissions, merge, deploy and Railway operations behind new owner-specific approval.
