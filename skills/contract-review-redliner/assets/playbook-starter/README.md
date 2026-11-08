# Your contract playbook

This folder holds your company's negotiating positions. The contract review compares every contract against it, so the better it reflects how *you* negotiate, the better the redlines.

The starter entries are sensible market-standard positions for small and mid-sized businesses. They are a starting point, not legal advice. Before relying on them, go through the `must-have` entries with whoever signs your contracts and adjust the numbers: caps, payment days, notice periods.

## Format

One entry per topic:

```
## PB-PAY-001: Payment terms
applies_to: msa, saas, services, sow, freelance
role: vendor            # customer | vendor | discloser | recipient | any
priority: must-have     # must-have | important | nice-to-have
last_reviewed: 2026-01-15
owner: Finance lead

**Standard:** what you ask for and accept without discussion.
**Fallback:** what you will concede if pushed. INTERNAL: never shown to the other side.
**Walk-away:** the point where you escalate or don't sign. INTERNAL.
**Red flags:** wording that should always be caught.
**Preferred language:** clause text you like to propose.
```

- `applies_to` lists contract types: nda, msa, saas, sow, dpa, services, consulting, freelance, supply, vendor, reseller, partnership, licence, or `all`.
- `role` says which side the position is for. Use `any` when it's the same for both.
- Add, delete or rewrite entries freely. IDs just need to be unique. Use a new prefix, such as `PB-XYZ-001`, for your own topics.
- Fallback and Walk-away are internal. The review uses them to judge how much to push, but they never appear in a redline, a comment or an email to the counterparty.

## Files

| File | Topics |
|---|---|
| `commercial.md` | Payment, price changes, renewal, termination, suspension, order of precedence, unilateral changes |
| `risk.md` | Liability caps, indemnities, warranties, SLAs, insurance, force majeure |
| `ip-data.md` | IP ownership, licences, feedback and AI training, confidentiality, data protection, security, data return |
| `general.md` | Governing law, assignment, non-solicit and non-compete, publicity, audit, exclusivity |
| `nda.md` | NDA-specific points: definition, mutuality, term, residuals, hidden obligations |
| `freelance.md` | Freelancers and small agencies selling services: acceptance, revisions, kill fee, portfolio, late payment |
