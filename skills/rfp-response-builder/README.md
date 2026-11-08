# RFP Response Builder

Turn RFPs, tenders and security questionnaires into tailored, submission-ready responses built only from your company's approved content. Nothing is invented, and nothing is missed.

## What you get

- **Proposal (.docx)**: executive summary, narrative sections, and an answer to every requirement in the RFP's own order. Items that need checking are highlighted.
- **Compliance matrix (.xlsx)**: every requirement with mandatory flag, compliance, status, sources and owner, plus a Gaps sheet for your experts.
- **Filled questionnaires**: answers written straight into the client's own spreadsheet, keeping their layout.
- **Bid/no-bid assessment**: knock-out checks and a weighted score before you invest a week of writing.
- **Your answer library**: built from your past proposals in minutes, and it grows with every bid.

## Quick start

1. **Build your library (once).** Put 3–10 past proposals in a folder and ask:
   > "Set up our RFP library from these old proposals."

   Claude creates `./rfp-library/`, extracts your company facts, certifications, standard answers, case studies, team profiles and rates, resolves conflicts in favor of the newest source, and tells you which topics are still missing.
2. **Respond to an RFP.**
   > "Here's the tender from Acme, draft our proposal and a compliance matrix."
3. **Fill a questionnaire.**
   > "Fill in this security questionnaire from our library. Answers go in column E."
4. **Qualify first.**
   > "Should we even bid on this?"

Outputs go to `./rfp-output/<client>/`.

## Why it is safe to submit

- Every fact comes from your library and is traceable to an entry ID.
- What the library can't support becomes a `[VERIFY: …]` item with a named owner. Missing certifications, references, service levels and prices are never invented.
- Requirements you can't fully meet are stated as exceptions, never quietly agreed to.
- Out-of-date entries, internal-only notes and leftover names of other clients are caught before you send.

## Requirements

Python 3.9+ with `python-docx`, `openpyxl` and `pypdf` (`python3 -m pip install -r requirements.txt`). Claude installs them on first use. Without Python, the skill still works and produces markdown and CSV instead of Word and Excel.

No network access, no external services: your content stays in your folder.
