# response.md: the working file for a bid

`response.md` is the single source of truth for a bid. Every script reads it directly. It is plain markdown, so you can write long answers naturally without escaping. If another tool needs JSON, run `compile_response.py`; existing `response.json` files are still accepted everywhere.

## Structure

Each block starts with a line beginning `# ` (one hash and a space). Inside a block, `key: value` lines come first, then **one blank line**, then the markdown body. Inside bodies, use `###` or deeper for headings, never a single `#`.

```markdown
# RFP
client: City of Example
title: Citizen Services Portal Modernisation
reference: CoE-2026-114
deadline: 2026-12-01 12:00 CET
submission: PDF via e-tender portal, max 30 pages excl. appendices
page_limit: 30
language: en
evaluation_criteria: Technical approach=40; Price=30; Experience=30
client_goals: Reduce call-centre volume; WCAG 2.1 AA compliance
assumptions: Pricing to be supplied by the user; Response in English

# Bid
decision: go
score: 72
risks: Tight 4-month timeline; Price pressure

Strong fit on public-sector portals. Rationale continues as the body.

# Win themes
- Proven public-sector delivery
- Accessibility built in from day one

# Section: Executive summary
Markdown text of the section…

# Section: Understanding of your needs
…

# Requirement 4.2a
section: Technical approach
text: Describe your approach to accessibility testing.
type: question
mandatory: yes
word_limit: 300
status: answered
compliance: comply
sources: ANS-DEL-007, CS-003
confidence: high
owner:
notes:

Yes. We test accessibility in every sprint… (the answer, in markdown)
```

## Field rules (requirement blocks)

| Field | Values | Notes |
|---|---|---|
| id (after `# Requirement`) | text | The RFP's own numbering. Use `R<n>` only if the RFP has none. Must be unique. |
| `text` | one line | The requirement, verbatim from the RFP. |
| `type` | `question`, `requirement`, `form`, `pricing`, `instruction` | `instruction` = a submission rule such as a format or page limit. |
| `mandatory` | yes / no | Yes for must/shall/required/pass-fail. |
| `word_limit` | number | Checked by `check_response.py`. |
| `status` | `answered`, `partial`, `gap`, `not-applicable` | `partial` = drafted, but contains `[VERIFY]` items or needs expert input. |
| `compliance` | `comply`, `partial`, `exception`, `n/a` | Honest compliance statement, shown in the matrix. |
| `sources` | IDs, comma-separated | Required whenever the answer states facts. Use `USER` for facts the user gave in this conversation. |
| `confidence` | `high`, `medium`, `low` | How sure you are that the answer is complete and correct. |
| `owner` | role | The role who must fill or confirm a gap. |
| `notes` | one line | For a gap: exactly what is needed. |

The body after the blank line is the answer. Supported markdown: paragraphs, `-` bullets, `1.` lists, `**bold**`, `*italic*`, pipe tables.

Placeholders the checker detects: `[VERIFY…]`, `[TBD…]`, `[TODO…]`, `XXX`, `{{…}}`, `<insert…>`. Use `[VERIFY: what to check]`. That's the one reviewers search for, and the Word builder highlights it in yellow.

Writing tip: for a large RFP, append requirement blocks in batches as you work through the document, rather than writing the whole file in one go.
