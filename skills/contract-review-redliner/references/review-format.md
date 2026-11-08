# review.md format

`review.md` is the working file for one contract review. The scripts read it to build the redline, the internal summary and the checks. Keep it in `./contract-reviews/<counterparty-slug>/review.md`.

It contains top-level `# ` blocks. Keys are `key: value` lines at the top of a block; longer text goes under `### ` sub-headings. Block order doesn't matter, but this order reads best.

## `# Contract` (required)

```
# Contract
file: contracts/acme-msa-v3.docx     # path to the ORIGINAL contract; never edited
title: Master Services Agreement
type: saas                           # nda | msa | saas | sow | dpa | services | consulting | freelance |
                                     # supply | vendor | reseller | partnership | licence | employment | lease | other
counterparty: Acme Cloud Ltd
our_party: Northwind Ltd             # as named in the contract
our_role: customer                   # customer | vendor | discloser | recipient | mutual | licensee | licensor | ...
author: Northwind Ltd                # name shown on tracked changes and comments (a company or person, never "Claude")
playbook: ./contract-playbook        # or: starter (the skill's defaults)
governing_law: England and Wales
term: 3 years from the Effective Date
renewal: auto-renews for 12-month terms unless notice 90 days before the end of the term
value: about GBP 48,000 a year
documents: MSA v3; Order Form; DPA (referenced but not provided)
assumptions: Effective Date is assumed to be the signature date (1 Dec 2026).
```

## `# Verdict` (required)

```
# Verdict
overall: negotiate        # sign | sign-with-changes | negotiate | escalate | do-not-sign | summary-only
summary: Commercially workable, but three must-haves need fixing before signature: the one-sided liability cap, uncapped price increases and the 90-day renewal notice. Data terms are fine.
```

- `sign`: nothing material.
- `sign-with-changes`: only minor points that you'd sign without.
- `negotiate`: must-haves need fixing.
- `escalate`: a lawyer must look at it before going further. Use this for high stakes, regulated areas, unusual risk, or a jurisdiction you can't judge.
- `do-not-sign`: walk-away terms that the other side is unlikely to move on.
- `summary-only`: a signed contract that is only being summarised.

## Free sections (optional; rendered in the summary in this order)

`# Key terms` and `# Key dates` come first, then any others (`# Checklist`, `# Open questions`, `# Next steps`, `# Not reviewed`). Write them in normal markdown; tables are fine.

```
# Key dates
| Date | What | Action |
|---|---|---|
| 2029-09-02 | Last day to give non-renewal notice (90 days before 2029-12-01) | Diary reminder 2029-08-01 |
```

**`# Checklist`** lists every playbook topic that applies to this contract type and role, each with a status. `check_review.py` warns about any topic missing from it.

```
# Checklist
- PB-LIAB-001 Limitation of liability: issue I-01
- PB-DATA-002 Data return and deletion: missing from the contract, issue I-05
- PB-LAW-001 Governing law: ok (clause 18, England and Wales)
- PB-AUDIT-001 Audit: n/a (no audit clause, none needed)
```

## `# Issue <ID>: <title>` (one per point you raise)

```
# Issue I-01: Liability cap applies to us only
clause: 9.2
topic: PB-LIAB-001
risk: high                 # high | medium | low
priority: must-have        # must-have | important | nice-to-have (drives the negotiation email)
action: replace            # replace | delete | insert-after | comment
position: Mutual cap at 12 months' fees    # one line for the summary table (optional)
lawyer: no                 # yes = flag for lawyer review
occurrence: 2              # only if the find text appears more than once

### find
Customer's liability under this Agreement shall be unlimited.

### replace
Customer's total liability under this Agreement shall not exceed the fees paid and payable in the twelve (12) months preceding the claim.

### comment
Liability caps should apply equally to both parties.

### internal
Why it matters: an uncapped exposure on a GBP 48k contract. Fallback: 18 months' fees. Walk-away: any uncapped liability for us beyond the legal minimum.
```

### Rules for each field

- **find**: text copied **exactly** from the contract, inside **one paragraph**. Quote and dash styles and spacing don't matter; everything else does. Use the smallest span that is unique, usually a sentence. **Don't include clause numbers**: Word auto-numbering isn't part of the text. If the text appears more than once, add more words or set `occurrence:`.
- **replace**:
  - For `replace`: the full new version of the `find` text. The script redlines only the words that differ, so rewrite the sentence naturally, keeping the parts you don't change.
  - For `insert-after`: the new clause(s), added after the paragraph that contains `find`. Separate paragraphs with a blank line. The new paragraph copies the anchor paragraph's style and numbering, so anchor on the last paragraph of the clause it belongs after, not on a heading. Add `numbered: no` to drop the numbering.
  - Not used for `delete` or `comment`.
- **comment**: goes **into the Word file**, visible to the counterparty. Keep it to one or two sentences, courteous, explaining the principle ("caps should be mutual"). Never mention fallbacks, limits, internal views or the playbook.
- **internal**: never leaves review.md and the internal summary. Put here why it matters, the fallback, the walk-away, who should decide, and what to concede.

`check_review.py` treats the following in `replace` or `comment` as a **leak** error:
- internal wording ("we could accept", "fallback", "walk-away", "if they push back")
- text copied from `### internal` or from the playbook's Fallback or Walk-away
- playbook IDs
- placeholders

### Choosing the action

| Situation | action |
|---|---|
| Change wording: numbers, a cap, a notice period, mutuality | `replace` (minimal edit of the sentence) |
| A whole sentence or clause is unacceptable and nothing replaces it | `delete` |
| Something is missing: a data-return clause, carve-outs, a cure period | `insert-after` |
| A question, a request for a missing document, a low-risk point, or anything you'd rather discuss than redline | `comment` |
