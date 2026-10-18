# Repository health (read-only)

Run manually in **Actions → Repository health inventory → Run workflow**, or use its weekly UTC schedule after this PR is merged and enabled. This draft PR does not schedule anything on the default branch.

## Token scope
Create a fine-grained GitHub token available as repository Actions secret `GH_PORTFOLIO_TOKEN`, with **Metadata: read**, **Contents: read**, and **Pull requests: read** for *all intended OurChappy repositories*. The default `GITHUB_TOKEN` is not used as a fallback: the dedicated read-only secret is mandatory. This workflow never writes repository contents, issues, PRs, settings or registry data. The token is never printed.

## Outputs
Download the `repository-health` workflow artifact for `report.json` (machine-readable) and `README.md` (table). Per repository: default-branch SHA, file count, tracked bytes, GitHub reported size, ten largest files, open PR count, CI-workflow and test file discovery, basic documentation indicators. An inaccessible or truncated repository is reported as unassessed and causes a nonzero exit.

## Limitations / future gates
The Git Trees API may truncate extremely large trees. A fallback traversal must be added before those repositories can be scored. GitHub size is a GitHub-reported metadata figure, not a local disk measurement. CI outcomes, duplication, security posture, ownership correctness and historical Git size are **not assessed**. GitHub APIs only expose repositories visible to the supplied token; compare coverage against a separately maintained expected repository list before claiming full portfolio coverage. Enumeration uses authenticated `/user/repos` with owner filtering, and refuses fewer than `EXPECTED_REPO_COUNT` repositories (default 15). This minimum guards against gross access loss but is not proof of full exact membership; reconcile repository IDs against the ownership directory. PR-triggered runs only execute offline unit tests; token access and inventory remain excluded from PR runs.

Do not label absent checks as failing or award health-score points without evidence. The workflow uses an isolated report artifact and never commits results.
