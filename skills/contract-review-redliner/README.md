# Contract Review & Redliner

Review any contract against your own negotiating positions. You get a Word file with real tracked changes and comments, ready to send back, plus an internal summary that says whether to sign.

## What you get

- **Redline (.docx)**: your changes as genuine Word tracked changes, with a margin comment explaining each one. Only the words that change are marked. It's built on a copy of the original, keeping its formatting and numbering.
- **Internal review summary (.docx)**:
  - a verdict: sign, sign with changes, negotiate, escalate to a lawyer, or don't sign;
  - key terms and key dates;
  - every issue ranked by risk, with your fallback positions. These stay internal and never appear in the redline.
- **Negotiation email**: the must-haves first, written so you can send it.
- **Counter-redline check**: when the other side sends their version back, you see every change, including edits they made **without** Track Changes.
- **Signed-contract summary**: renewal and notice deadlines, obligations and risks to watch.

## Quick start

1. **(Optional) Set up your playbook.**
   > "Set up our contract playbook. We're a 20-person agency; we mostly sign client MSAs and SaaS tools."

   This creates `./contract-playbook/` from a starter set of 42 market-standard positions (buyer and seller side), adjusted to your answers. Without it, the review uses the starter positions.
2. **Review a contract.**
   > "Review this MSA from Acme. We're the customer. Mark it up and tell me if we can sign."
3. **Quick check.**
   > "Can I sign this NDA? Anything weird in it?"
4. **Next round.**
   > "Acme sent their markup back. Here's what we sent and what they returned. What changed?"

Outputs go to `./contract-reviews/<counterparty>/`.

## What it checks

- Every topic in your playbook for this contract type and side, including protections that are **missing**.
- Asymmetric caps and termination rights, automatic renewal traps, uncapped price increases, sole-remedy service credits, IP grabs, data use and AI training, hidden non-competes, terms incorporated from websites, and unilateral changes.
- Mechanical errors: unfilled blanks, "thirty (60) days", cross-references to clauses that don't exist, and defined terms that don't match.
- Before anything is built, a check that no fallback or internal note has leaked into the redline or the email.

## Formats

`.docx` is best: the redline keeps your formatting. `.pdf` and `.txt` work too, with the redline rebuilt as a plain Word document.

## Requirements

Python 3.9+ with `python-docx` (1.2 or later) and `pypdf`: `python3 -m pip install -r requirements.txt`. Claude installs them on first use. Without Python, the skill still works and produces a markdown redline instead of Word.

No network access, no external services: your contracts stay in your folder.

## Important

This is a first-pass review to help you decide and negotiate faster. It is not legal advice. For high-value, regulated or unusual contracts, or questions about enforceability under a specific law, have a qualified lawyer review it. The summary flags the points where that matters.
