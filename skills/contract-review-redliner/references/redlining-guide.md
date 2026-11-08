# Redlining and negotiation guide

A redline is a negotiation document. The other side reads every strike-through as a demand, so each one should be worth asking for and easy to agree to.

## Decide what to raise

- **Rank first, then draft.** Mark each finding as must-have, important or nice-to-have, using the playbook's `priority` and the deal size.
- **Redline the must-haves and the important points.** Raise nice-to-haves as comments or leave them out. A contract covered in red reads as "we rejected your paper" and slows the deal. More than about 15–20 edits to a short contract is usually too many.
- **Match the effort to the deal.** On a $2,000 freelance job, fix the payment trigger, IP and non-compete, and let the rest go. On a multi-year platform deal, go through every must-have.
- **Things you need not redline:** formatting, defined-term style, harmless boilerplate, and clauses that are slightly off-market but low risk.

## How to draft a redline

- **Minimal edits.** Change the fewest words that fix the problem. Keep the other side's drafting style, defined terms and sentence structure. `redline.py` only marks words that change, so write the full new sentence and let the script work out the difference.
- **Use their defined terms exactly**: "Supplier", not "Vendor"; "Customer Data", not "your data". Use their clause numbering in cross-references.
- **Make it mutual where that's fair.** "Each party" in place of "Customer" is the easiest redline to accept because it costs a reasonable counterparty nothing.
- **Write numbers as the contract does**, e.g. "thirty (30) days" in a contract that uses words and digits, and keep the two consistent.
- **Insert missing protections as new clauses**, anchored after the last paragraph of the clause they belong to. Use the playbook's preferred language, adapted to their terms.
- **Don't fix one clause and break another.** If you change a cap, check the indemnity and exclusions clauses that refer to it. If you add a termination right, check what happens to fees.
- **Never add facts you don't know**: company numbers, addresses, insurance amounts, dates. Use a comment that asks for them.

## Comments for the counterparty

- One or two sentences, giving the principle, not your position: *"Caps should apply to both parties."* not *"We can't accept unlimited liability but could live with 24 months."*
- Courteous and non-accusatory: *"Please could you share the AUP referred to here? We need to review it before signing."*
- Never mention internal positions, the playbook, fallbacks, budgets, other deals or how much you want the deal. `check_review.py` blocks the common phrasings, but write carefully anyway.

## Internal notes (`### internal`)

Each issue explains for your own team:
- the risk in money or practical terms;
- the fallback and the walk-away (from the playbook, adjusted to this deal);
- what you'd trade it for;
- whether a lawyer should look at it.

## Draft email to the counterparty (`email-draft.md`)

```
Subject: <Contract title>: our comments

Hi <name>,

Thanks for sending the <contract>. We're keen to move ahead. Our marked-up version is attached. The main points:

1. <must-have, one line, principle-based>
2. <must-have>
3. <important>

The remaining changes are minor clarifications. Happy to discuss on a call if that's quicker.

Best regards,
<name>
```

- List the must-haves first, then up to two or three important points. Leave the rest to the markup.
- No fallbacks, no "we could accept", no internal reasoning. Run `check_review.py --email email-draft.md`.
- Write in the contract's language if the counterparty works in it.

## When the other side sends their markup back

Run `compare_versions.py <what-we-sent>.docx <their-version>.docx`, then go through it:

1. **Untracked changes come first.** Any edit not shown as a tracked change has to be raised. It may be an accident, but you need to find it before signing.
2. **For each tracked change of theirs**, decide whether to accept, reject or counter. Judge it against the playbook, and note what they conceded and what they rejected from our last round.
3. **For each of our points they rejected**, decide whether to hold (a must-have), trade, or drop it.
4. **Comments**: answer their questions.

Then write a new `review.md` for the round (`round: 2` in `# Contract`), with `file:` pointing at **their** returned version. Its issues are the counter-proposals on their text.
