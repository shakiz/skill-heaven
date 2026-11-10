# Output format

## Link styles

| `link_style` | Use for | Ticket link | PR link |
|---|---|---|---|
| `slack` (default) | Posting to Slack through the connector, or pasting into Slack | `<https://acme.atlassian.net/browse/PAY-142\|PAY-142>` | `<https://github.com/acme/pay/pull/881\|PR #881>` |
| `markdown` | Teams, Discord, GitHub, Linear, Notion, email | `[PAY-142](https://acme.atlassian.net/browse/PAY-142)` | `[PR #881](https://github.com/acme/pay/pull/881)` |
| `plain` | Anywhere links aren't rendered; spoken | `PAY-142` | `PR #881` |

Note on pasting into Slack: the Slack composer doesn't turn `<url|text>` into a link when it's pasted by hand; it only renders when sent through the API. So when the user will **paste** the update into Slack themselves (no connector, or they said they'll paste it), use a bare URL after the key so Slack auto-links it:
`• Merged retry backoff for failed refunds PAY-142 https://acme.atlassian.net/browse/PAY-142`
When posting through the Slack connector, use `<url|text>`.

Headings: in Slack style use `*Yesterday*` (bold). In markdown style use `**Yesterday**`. Bullets: `•` for Slack, `-` for markdown.

## Shape

```
*Yesterday*
• <outcome> <ticket link> (<PR link>)
• Reviewed <whose> <what> <PR link>
*Today*
• <plan item> <ticket link>
• <notable meeting> (<time>)
*Blockers*
• Waiting on <who> for <what> <link>    ← or "None"
```

- Most significant item first in each section.
- One line per bullet. If it wraps past roughly 100 characters, cut words.
- A ticket that appears in both Yesterday and Today is fine ("Started X" / "Finish X") when work continues.

## Examples

### Good (Slack, posted through the connector)

```
*Yesterday*
• Shipped refund retry backoff <https://acme.atlassian.net/browse/PAY-142|PAY-142> (<https://github.com/acme/pay/pull/881|PR #881>)
• Reviewed Sam's webhook signature check <https://github.com/acme/pay/pull/877|PR #877>
• Helped support debug duplicate charge reports (root cause: client retry, not us)
*Today*
• Currency rounding fix <https://acme.atlassian.net/browse/PAY-150|PAY-150>: finish tests, open PR
• Demo refunds flow to support (2pm)
*Blockers*
• Waiting on @dana for staging DB credentials to test PAY-150
```

### Bad (the same day, unprocessed)

```
Yesterday:
- fix tests
- address review comments
- Merge branch 'main' into feature/PAY-142-retry
- PAY-142 rename variable
- standup
- 1:1 with manager
- slack: answered question in #support
Today: continue working
Blockers: none probably
```

What's wrong: commit messages instead of outcomes, the same ticket split into three lines, routine meetings listed, no links, a vague Today, and a hedged blocker line.

### Weekly summary (markdown)

```
**Shipped**
- Refund retry backoff [PAY-142](https://acme.atlassian.net/browse/PAY-142)
- Webhook signature verification (reviewed and co-owned) [PR #877](https://github.com/acme/pay/pull/877)
**In progress**
- Currency rounding fix [PAY-150](https://acme.atlassian.net/browse/PAY-150): PR next week
**Next week**
- Start partial refunds design [PAY-161](https://acme.atlassian.net/browse/PAY-161)
**Risks**
- Staging DB access still pending; blocks end-to-end tests for PAY-150
```

### Spoken

> Yesterday I shipped the refund retry backoff and reviewed Sam's webhook PR. Today I'm finishing the currency rounding fix and demoing refunds to support at two. I'm blocked on staging database credentials from Dana.
