# Development OS v4.0 — offline export M1/M2
This isolated prototype reads the 20 real PDF form fields of OurChappy Interactive Workbook v3.0 (two fields for stages 01–10) and emits a 10-stage draft cycle JSON and Markdown. No GitHub issues, registry rows, Work/Codex jobs or production records are created. Current PDF fields are free text, not validated IDs or trustworthy evidence. Unknown supplementary fields are ignored; missing expected fields fail closed.

Requires Python 3.11+ and PyMuPDF. From this directory: `python -m unittest discover -p 'test_exporter.py' -v`; then `python exporter.py /path/to/filled.pdf --cycle-id OC-001 --output-dir /tmp/oc-export`.

Cycle and artefact contracts are proposals, not migrations. Match real source identities against existing GitHub and Project GPT OS Supabase records before any posting or completion claims. Integration with draft PRs #2 (dispatcher), #8 (ownership), #9 (workflow) and #14 (intake) requires separate review. Tested locally on matching offline prototype: 7 unit tests passed and actual unfilled v3.0 workbook exported 10 stages with zero external writes. Published PR-head CI must be verified separately.
