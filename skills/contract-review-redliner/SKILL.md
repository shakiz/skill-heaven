---
name: contract-review-redliner
description: Reviews contracts against the user's own negotiating playbook and produces a Word redline with real tracked changes and margin comments, an internal risk summary and a negotiation email. Covers NDAs, MSAs, SaaS/subscription terms, SOWs, DPAs, consulting, freelance, supplier, reseller and partnership agreements. Rates every clause by risk, catches one-sided terms, auto-renewal traps, IP grabs, hidden non-competes, unfilled blanks and number mismatches, and keeps fallback positions out of anything the other side sees. Also compares a counterparty's returned markup with what was sent and detects untracked (silent) edits, summarises signed contracts with key dates and notice deadlines, and builds the playbook from the user's preferences or past contracts. Use this skill whenever the user shares or mentions a contract, agreement, NDA, terms and conditions, order form, SOW, DPA or "paper" from a client, supplier or partner, asks whether they can sign something, wants a contract checked, marked up, redlined, negotiated or summarised, or receives a counter-redline, even if they don't say "review".
---

# Contract Review & Redliner

Give the user what a careful commercial lawyer's first pass would give them:
- what's risky, ranked;
- what to ask for;
- a marked-up Word file ready to send;
- a clear verdict.

All of it is measured against **their** positions, not generic advice.

The value depends on four things. Protect them over speed or polish.

1. **The right side.** A clause that is good for a supplier is bad for a customer. Know which party the user is before judging anything.
2. **Nothing material missed.** Every playbook topic for this contract type gets a status, and the traps in `references/clause-checklist.md` are checked. What is *missing* from a contract matters as much as what is in it.
3. **A redline they can actually send.**
   - Surgical edits in the contract's own defined terms.
   - Only points worth negotiating.
   - Real tracked changes, never a rewritten document.
4. **Internal positions stay internal.** Fallbacks, walk-aways, budgets and reasoning go in the internal summary only. The Word redline and the email contain only what the counterparty may read.

This is a first-pass review to support the user's decision, not legal advice. Say so once in the summary, not in every message. Recommend a lawyer for high-stakes, regulated or unusual points. Never state that a clause is or isn't enforceable.

## Where things live

The skill folder may be read-only: **never store the user's files inside it.**
- **Playbook**: the user's positions. Look for it in this order:
  1. a path the user names;
  2. `./contract-playbook/`;
  3. a nearby folder with `## PB-...:` entries.
  If there is none, use the starter playbook in `<skill-dir>/assets/playbook-starter/` and say once that its positions are market-standard defaults. Offer **Setup** so they become the user's own.
- **Outputs**: `./contract-reviews/<counterparty-slug>/`, unless the user names another folder.
- **The contract**: never edit the original. `.docx` is best. `.pdf` and `.txt` work, but the redline is then rebuilt as a plain Word document. For `.doc`, `.pages` or `.rtf`, ask the user to save as `.docx`. A scanned PDF with no text needs a text version.

## First-time check

Install the script dependencies once: `python3 -m pip install -q -r <skill-dir>/requirements.txt` (use `python` if `python3` isn't found). Tell the user what you're installing if their environment asks for permission. If Python or the install isn't available, follow **Without scripts** at the end.

## Choose the mode

| User wants | Mode | Output |
|---|---|---|
| "Review / mark up / redline this", "what should we push back on" | **Full review** | `<name>-redline.docx`, `review-summary.docx`, `email-draft.md` |
| "Can I sign this?", "anything scary in here?", "quick look" | **Quick check** | Verdict and top issues in chat; offer the full redline |
| The other side sent back their markup or a new version | **Counter-redline** | Change report, then a round-2 review and redline |
| A contract already signed: "what did we agree to?", "when can we cancel?" | **Signed summary** | `review-summary.docx` with key terms, dates and obligations; no redline |
| "Set up our playbook", or the first use with no playbook | **Setup** | `./contract-playbook/` with the user's positions |

When the request is ambiguous, pick the most likely mode, say which one you picked, and proceed.

## Before judging anything: which side are we on?

Work out `our_role` (customer or vendor, recipient or discloser, mutual) from the user's words and their company name in the parties clause. If you genuinely can't tell (for example, the user pasted a contract with no context), **ask that one question before reviewing.** Also ask, only if it changes the review and you can't infer it:
- What was promised outside the contract (features, prices, service levels)? The entire-agreement clause will erase it.
- How big or important is the deal? This sets how hard to push.

If the user wants you to proceed without answers, record assumptions in `# Contract`.

## Full review workflow

### 1. Read and scan

```bash
python3 <skill-dir>/scripts/scan_contract.py <contract> -o contract-reviews/<slug>/contract.txt
```

This gives the text with paragraph and clause numbers, reconstructed from Word auto-numbering. The **SCAN** section lists:
- unfilled blanks
- word/digit mismatches ("thirty (60)")
- cross-references to clauses that don't exist
- unused or doubly-defined terms
- documents referenced but not attached (schedules, URLs, "as updated from time to time")
- renewal and notice language

Raise every blank and mismatch, and list everything not provided under `# Not reviewed`; you can't review what you can't see. If the scan says the file already contains tracked changes, it's a marked-up draft: use **Counter-redline** mode.

### 2. Fill in `# Contract` and the checklist

Create `contract-reviews/<slug>/review.md`. Read `references/review-format.md` first. Fill in `# Contract`: type, parties, role, author, governing law, term and renewal. Then list in `# Checklist` every playbook entry that applies to this type and role (by `applies_to` and `role`), each with a status (`ok`, `issue I-nn`, `missing`, `n/a`). Use `references/clause-checklist.md` for the reading order and the traps.

### 3. Find the issues

Go through the contract clause by clause against the playbook. For each problem, add a `# Issue` block with:
- the risk (high, medium or low) and priority;
- the action (`replace`, `delete`, `insert-after` or `comment`);
- the exact `find` text, a `replace` in the contract's own terms, a short `comment` for the counterparty and an `internal` note.

Read `references/redlining-guide.md` before drafting. In short:
- **Judge against the playbook's Standard. Draft at the Standard.** Fallback and Walk-away tell you how hard to push and what to put in `internal`. Never put them in `replace`, `comment` or the email.
- **Missing protections** (no data-return clause, no cap for the other side, no cure period) become `insert-after` issues.
- **Prioritise.** Redline the must-haves and important points. Turn minor points into comments or drop them. A short contract with 30 edits won't get signed.
- **Know your limits.** Points that depend on local law (employment, consumer, real estate, regulated sectors) or large exposure get `lawyer: yes`. When the whole contract is outside commercial contracts, set `overall: escalate`.

Then write `# Verdict`, `# Key terms`, `# Key dates` (with the actual non-renewal notice deadline, calculated) and `# Not reviewed`.

### 4. Validate

```bash
python3 <skill-dir>/scripts/check_review.py contract-reviews/<slug>/review.md --playbook <playbook-dir>
```

Errors must be fixed:
- `find` text not found or ambiguous;
- overlapping issues (merge them);
- missing facts;
- **LEAKS** of internal positions into counterparty-facing text.

Read every warning, for example a word like "Vendor" that the contract never uses, a cross-reference to a missing clause, or a checklist topic not covered. Fix it or make a conscious decision to leave it. Rerun until there are no errors.

### 5. Build the outputs

```bash
python3 <skill-dir>/scripts/redline.py contract-reviews/<slug>/review.md -o contract-reviews/<slug>/<contract-name>-redline.docx
python3 <skill-dir>/scripts/build_summary.py contract-reviews/<slug>/review.md -o contract-reviews/<slug>/review-summary.docx
```

`redline.py` writes real tracked changes (author = `author:` from `# Contract`) and margin comments into a **copy** of the contract, and leaves Track Changes switched on. It reports each issue as one of:
- `applied`
- `comment-fallback`: the text crosses a hyperlink, field or earlier revision, so the proposed wording went into a comment instead. Tell the user.
- a failure with a hint. Fix review.md and rerun against the **original** contract, never the redline.

Then write `email-draft.md` following `references/redlining-guide.md`, and run `check_review.py ... --email contract-reviews/<slug>/email-draft.md`.

### 6. Hand over

Tell the user, briefly:
- the verdict in one line;
- the top 3 issues in plain English, with what you asked for;
- the key dates, especially notice deadlines;
- what you didn't review (missing schedules, linked terms) and any lawyer flags;
- where the files are. The redline is ready to send, while the summary is internal and includes their fallbacks.

## Quick check

Scan the contract, read it against the playbook, and reply in chat:
- a verdict (sign, negotiate, or don't sign as drafted);
- the 3–5 issues that matter, each with the clause and a one-line fix;
- any key dates.

No files unless asked. Offer the full redline at the end.

## Counter-redline

```bash
python3 <skill-dir>/scripts/compare_versions.py <what-we-sent>.docx <their-version>.docx -o contract-reviews/<slug>/round-2-changes.md
```

If you don't have what was sent, use `--changes <their-version>.docx` to list their tracked changes and comments.

The report has three parts:
1. Everything that differs from our version.
2. **UNTRACKED changes**: edits made without Track Changes. Raise every one with the user first, because these are the changes that get missed.
3. Their new tracked changes and comments, by author.
4. What happened to each of our tracked changes: accepted, still pending, countered with their own tracked change, or **undone without tracking**.

For each change, recommend accept, reject or counter against the playbook. Track which of our must-haves they rejected. Then do a round-2 review with `file:` set to **their** version and `round: 2`. The redline goes on top of their markup.

## Signed summary

There is nothing to negotiate. Set `overall: summary-only` and fill in:
- `# Key terms`
- `# Key dates`: renewal, notice deadlines, price-review dates, minimum terms
- `# Obligations`: what each party must do, and by when
- `# Risks to watch`

Build only `review-summary.docx`. Make the notice deadline impossible to miss.

## Setup: the user's playbook

1. `python3 <skill-dir>/scripts/init_playbook.py ./contract-playbook` copies the starter playbook. Its README explains the format.
2. Ask who usually signs, what they buy and sell, and their typical deal size. Then tune the `must-have` entries first: liability cap, payment days, renewal and notice, IP, data, governing law. Use their answers, or past negotiated contracts if they give you some: a position they accepted before is a realistic Fallback, and their own templates show their Standard.
3. Mark positions you inferred as such in the entry. Never invent a company's risk appetite; ask.
4. Delete topics they don't need, and add their own (e.g. `PB-EXPORT-001`).

## Without scripts

If Python can't run, do the same review by hand:
- `review.md`, in the same format;
- `redline.md`: each changed clause with ~~deleted text~~ and **inserted text**, followed by the counterparty comment;
- `review-summary.md`: verdict, key terms, an issues table and internal notes, kept in a separate file from the redline;
- `email-draft.md`.

Tell the user the redline is markdown because the scripts couldn't run, so they'll need to apply it in Word with Track Changes on. Check leaks, defined terms and cross-references yourself.

## Reference files

- `references/review-format.md`: the `review.md` format and field rules. Read it before writing review.md.
- `references/clause-checklist.md`: reading order, traps to always check, focus by contract type, out-of-scope areas.
- `references/redlining-guide.md`: how to choose and draft redlines and comments, the negotiation email, and handling a counter-redline.
- `assets/playbook-starter/`: default positions (42 topics, both sides of the deal) and the playbook format.
