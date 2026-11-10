# Saving standups to a doc

The user chose a destination once; it's in `save_to` in the config. This file covers creating the log the first time and adding each approved standup to it. Connector tool names vary by host: look for the tool that does what's described. If a docs skill exists for the destination (e.g. a Claude Docs or Google Workspace skill), load it before the first call. It knows the connector's exact rules.

## Contents
- What an entry looks like
- New Google Doc
- New Claude doc
- Existing doc link
- Local only
- Reading the log back

## What an entry looks like

One section per day, newest first, under a short header:

```markdown
# Standup log

## Tue 10 Nov 2026

**Yesterday**
- Merged exponential backoff for failed refund retries [PAY-142](https://acme.atlassian.net/browse/PAY-142)
- Built the price range filter for search [WEB-77](https://acme.atlassian.net/browse/WEB-77)

**Today**
- Finish the search filters [WEB-77](https://acme.atlassian.net/browse/WEB-77)

**Blockers**
- Waiting on Priya for design sign-off on the date filter
```

- Convert links to normal markdown/rich links. Slack `<url|text>` and bare pasted URLs become `[text](url)`.
- Use the approved wording exactly. Don't re-summarise.
- Same day twice → replace that day's section.
- Don't add anything the update didn't contain (no skipped-sources notes, no internal remarks).

## New Google Doc

Using the Google Docs / Drive connector:
1. Create a doc titled `Standup log – <user's first name if known, else "My standups">`, containing the `# Standup log` heading.
2. Save its URL to `save_to` (`{"type": "google_doc", "url": "...", "title": "..."}`) immediately, before writing the first entry, so a failure later doesn't cause a second doc to be created next time.
3. Insert each new entry directly under the title, so the newest is on top. If the connector can only append, append at the end and say "newest at the bottom" in the first confirmation.

## New Claude doc

Using the Claude Docs connector (or the docs skill, if listed):
1. Create a doc titled `Standup log`, with the `# Standup log` heading.
2. Save its link to `save_to` (`{"type": "claude_doc", "url": "...", "title": "Standup log"}`) right away.
3. For each entry, edit the doc to insert the new dated section under the title. Read the doc first if you need to find an existing section for today.
4. If the host has an Artifact tool that can open the doc, there's no need to open it every day. Just give the link in the confirmation line.

## Existing doc link

The user pasted a link. Work out the kind from the URL and check that a connector can write to it before you accept it:

| URL looks like | type | Write with |
|---|---|---|
| `docs.google.com/document/...` | `google_doc` | Google Docs connector |
| `claude.ai/.../artifact/...` | `claude_doc` | Claude Docs connector (a Claude doc link is an artifact link) |
| `notion.so/...` / `notion.site/...` | `notion` | Notion connector: append blocks to the page |
| `*.atlassian.net/wiki/...` | `confluence` | Atlassian connector: get page, update page with the new section prepended, incrementing the version |

- Read the doc first. If it already has dated entries in another format, match their format rather than imposing this one.
- Never delete or rewrite anything in it apart from today's own section.
- If no connector can write to the link, say so plainly and offer: a new Google Doc, a new Claude doc, or local only.

## Local only

`save_to = {"type": "local"}`. Nothing beyond `~/.my-standup/history/`. Mention once that they can switch to a doc anytime.

## Reading the log back

Carry-over reads the local history first. If the local history is empty (new computer, cleared folder) but `save_to` points at a doc, read the doc's newest section and use its **Today** list as the previous plan.
