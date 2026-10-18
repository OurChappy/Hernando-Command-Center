# Career Artifact Publisher

GitHub Actions workflow to publish local repository artifacts to Dropbox. This does not pull files directly from ChatGPT Library.

## Setup
1. Add repository secret `DROPBOX_ACCESS_TOKEN` (short-lived token may expire; use a refreshed token or implement OAuth refresh).
2. Add the four V3 files under `artifacts/career/` using GitHub's upload UI. Keep the repository private if files contain personal information.
3. Open Actions > Career Artifact Publisher > Run workflow. Choose `dry_run=true` first.
4. Review the job log, then run with `dry_run=false`.
5. Confirm all four files in Dropbox.

The script verifies Dropbox upload response and file hash, refuses overwrite by default, and writes a JSON report to the Actions run artifacts. The Dropbox destination folder must exist.

Never commit credentials. GitHub Actions does not automatically access ChatGPT Library.
