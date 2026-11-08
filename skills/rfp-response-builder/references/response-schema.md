# response.json schema

`response.json` is the single source of truth for a bid. Every script reads it, so keep it valid JSON (UTF-8) and update it as you work.

```json
{
  "rfp": {
    "client": "City of Example",
    "title": "Citizen Services Portal Modernisation",
    "reference": "CoE-2026-114",
    "deadline": "2026-12-01 12:00 CET",
    "submission": "PDF via e-tender portal, max 30 pages excl. appendices",
    "page_limit": 30,
    "language": "en",
    "evaluation_criteria": [
      {"name": "Technical approach", "weight": 40},
      {"name": "Price", "weight": 30},
      {"name": "Experience", "weight": 30}
    ],
    "client_goals": ["Reduce call-centre volume", "WCAG 2.1 AA compliance"],
    "assumptions": ["Pricing to be supplied by the user"]
  },
  "bid": {
    "decision": "go",
    "score": 72,
    "rationale": "Strong fit on public-sector portals; price pressure likely.",
    "risks": ["Tight 4-month timeline"]
  },
  "win_themes": [
    "Proven public-sector delivery",
    "Accessibility built in from day one"
  ],
  "sections": [
    {"title": "Executive summary", "body": "Markdown text…"},
    {"title": "Understanding of your needs", "body": "…"}
  ],
  "requirements": [
    {
      "id": "4.2a",
      "section": "Technical approach",
      "text": "Describe your approach to accessibility testing.",
      "type": "question",
      "mandatory": true,
      "word_limit": 300,
      "status": "answered",
      "compliance": "comply",
      "answer": "Markdown answer text…",
      "sources": ["ANS-DEL-007", "CS-003"],
      "confidence": "high",
      "owner": "",
      "notes": ""
    }
  ]
}
```

## Field rules

| Field | Values | Notes |
|---|---|---|
| `requirements[].id` | string | The RFP's own numbering. Use `R<n>` only if the RFP has none. Must be unique. |
| `text` | string | Verbatim from the RFP. |
| `type` | `question`, `requirement`, `form`, `pricing`, `instruction` | `instruction` = a submission rule such as a format or page limit. |
| `mandatory` | bool | True for must/shall/required/pass-fail. |
| `word_limit` | int or null | Checked by `check_response.py`. |
| `status` | `answered`, `partial`, `gap`, `not-applicable` | `partial` = drafted, but contains `[VERIFY]` items or needs expert input. |
| `compliance` | `comply`, `partial`, `exception`, `n/a` | Honest compliance statement shown in the matrix. |
| `answer` | markdown | Simple markdown only: paragraphs, `-` bullets, `1.` lists, `**bold**`, `*italic*`, pipe tables. |
| `sources` | list of library IDs | Required whenever the answer states facts. Use `"USER"` for facts the user gave in this conversation. |
| `confidence` | `high`, `medium`, `low` | How sure you are that the answer is complete and correct. |
| `owner` | string | The role who must fill or confirm a gap. |
| `notes` | string | For a gap: exactly what is needed. |

Placeholders the checker detects: `[VERIFY…]`, `[TBD…]`, `[TODO…]`, `XXX`, `{{…}}`, `<insert…>`. Use `[VERIFY: what to check]`. That's the one reviewers search for.
