# Answer library format

The library is a folder of markdown files. Each file holds many **entries**. An entry is the smallest reusable, approved piece of content: one answer, one case study, one CV, or one pricing rule.

## Folder layout (recommended)

```
library/
├── company/        # profile, history, size, locations, financials, certifications, policies
├── answers/        # reusable Q&A grouped by topic: security.md, delivery.md, quality.md, support.md, hr.md …
├── case-studies/   # one entry per project reference
├── team/           # one entry per key-person CV summary
├── pricing/        # rate cards, pricing models, discount rules
└── boilerplate/    # standard proposal text: about us, closing, legal disclaimers
```

Any structure works. The search script reads every `*.md` file recursively and ignores `README.md` files.

## Entry format

```markdown
## ANS-SEC-004: Encryption of data at rest and in transit
tags: security, encryption, tls, aes, gdpr
last_reviewed: 2026-05-14
owner: Security lead
approved_for: external

All customer data is encrypted at rest with AES-256 … (the approved answer text)
```

- **Heading** `## <ID>: <title>`. The ID is unique and stable, and proposals cite it. Suggested prefixes: `CO-` company, `ANS-<TOPIC>-` answers, `CS-` case studies, `TEAM-` people, `PRC-` pricing, `BP-` boilerplate.
- **Metadata lines** directly under the heading, as `key: value`. Recognized keys: `tags`, `last_reviewed` (YYYY-MM-DD), `owner`, `approved_for` (`external` | `internal-only`), `expires` (YYYY-MM-DD, e.g. for a certificate).
- **Body**: everything until the next `## ` heading.

## Rules the skill follows

- Use only entries with `approved_for: external` (or no `approved_for`) in client-facing text. `internal-only` entries guide the writer but are never quoted.
- Treat an entry past `expires`, or with `last_reviewed` older than 12 months, as needing confirmation. The answer gets `[VERIFY]` and the gap list names the entry's owner.
- Case studies should state: client (or an anonymized description, if the client may not be named), industry, problem, solution, results with numbers, period, technologies, and whether the client agreed to be a reference.

## Harvesting new entries

When adding content from a finished proposal:
1. Generalize it: remove the client's name and specifics unless it is a case study.
2. Give it the next free ID in its prefix series. Check with `search_library.py --list`.
3. Set `last_reviewed` to today and `owner` to the role who approved it.
4. Show the user the proposed entries and write them only after approval.
