# Offline idea intake M1

Issue: https://github.com/OurChappy/Hernando-Command-Center/issues/11

Run from repository root:

```bash
python3 -m unittest discover -s portfolio -p 'test_idea_intake.py' -v
python3 -m portfolio.idea_intake --idea /path/to/idea.json --inventory /path/to/verified-inventory.json --output /tmp/issue-proposal.json
```

Input idea contains title, outcome, repository_id, repository, project_id, registry_item_id, evidence (url and classification), and nonempty tasks with stable IDs, title, acceptance and optional depends_on. Inventory contains verified repositories and known existing issues. Output is dry-run issue Markdown and JSON only. Never import a fabricated repo/project/item identity into a live registry; missing or inconsistent mapping emits HOLD. An issue title match flags review rather than writing anything. This is not a comprehensive semantic duplicate search: obtain live GitHub candidate issues before using the result. No Codex/Work dispatch or production writes.

The generator does not post GitHub issues or modify Supabase and must not be interpreted as a live orchestrator. Synthetic-only unit tests; hosted CI and integration are separate gates.
