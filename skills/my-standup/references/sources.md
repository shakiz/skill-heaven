# Sources: how to gather each one

Use the same time window (`since` → now) for every source. Run the independent calls in parallel. Connector tool names vary by host; look for a tool that does what is described, and skip the source if there isn't one.

## Contents
- Git and GitHub
- Jira
- Linear
- Calendar
- Slack
- Previous standup (history)
- Reading the user's notes

## Git and GitHub

```bash
python3 <skill-dir>/scripts/git_activity.py \
  --roots ~/code/payments ~/code/web \
  --author dana@acme.com dana@users.noreply.github.com \
  --workdays mon,tue,wed,thu,fri \
  --gh
```

- `--since auto` (default) picks the window from the workdays and `~/.my-standup/history/`. Pass `--since 2026-11-05` or `--since 2026-11-05T09:30` to override.
- `--roots` takes repos or parent folders; it searches 3 levels down by default (`--depth`).
- Without `--author` it uses the global git email. Users often commit under several emails (work, personal, GitHub noreply), so list them all in the config.

What the JSON gives you, and how to use it:
- `repos[].commits[]`: `subject`, `branches`, `ticket_keys`, `noise` (merge, WIP or fixup commits; ignore these). Group commits by `ticket_keys`, then by branch.
- `repos[].branch` + `dirty_files`: the branch currently checked out with uncommitted changes is almost always **today's** work.
- `pull_requests[].roles`: `authored`, `reviewed`, `open-authored` and `review-requested`.
  - `reviewed` → a Yesterday bullet ("Reviewed …").
  - `open-authored` that isn't a draft and hasn't been updated in over a day → a candidate blocker ("PR #881 waiting on review").
  - `review-requested` → a Today item ("Review Sam's PR #890").
- `warnings`: pass along anything relevant in the "Skipped" line.

If `gh` isn't available but a GitHub connector is, use it for the same four PR queries.

## Jira

Use the Atlassian connector's JQL search (e.g. `searchJiraIssuesUsingJql`). If it requires a cloud ID, get it from the accessible-resources tool first. Two queries:

1. Activity in the window:
   `assignee = currentUser() AND updated >= "<since yyyy-MM-dd HH:mm>" ORDER BY updated DESC`
   Add `AND (<jira_jql_extra>)` from the config if set. Also run
   `issuekey in issueHistory() AND updated >= "<since>"` only if the first query returns nothing. `issueHistory()` is the user's recently viewed issues, so treat these as hints (and include them only if git, Slack or the notes confirm the user worked on them), not as proof of work.
2. Current state:
   `assignee = currentUser() AND statusCategory = "In Progress" ORDER BY priority DESC`

Fields worth fetching: key, summary, status, statusCategory, priority, flagged, updated, and issue links of type "is blocked by".

- Status moved to Done in the window → shipped (Yesterday).
- In Progress / In Review → Today, or Yesterday if it moved.
- Status named like "Blocked", the Flagged field set, or an unresolved "is blocked by" link → Blocker evidence. Read the latest comment to name who or what it waits on.
- Link format: `<jira_base_url>/browse/<KEY>`. Get the base URL from the config or from the issue's `self` / site URL. Never guess it.

## Linear

Use the Linear connector: issues assigned to the user and updated since the window start, and issues in started states. "Blocked" comes from issue relations or a "Blocked" label. Use the issue's `url` field for links.

## Calendar

Google Calendar or Outlook connector:
- **Window** events: only to explain the day ("Ran the Q4 planning workshop"). Include a past meeting only if the user presented, ran it, or it produced a decision. Skip standups, 1:1s, focus blocks and declined events.
- **Today's** events: name 0–2 notable ones in Today, with the time ("Design review for search, 2pm"). Skip routine ones.
- Private events → treat as busy; never mention their title.
- Use the user's local timezone when showing times.

## Slack

Search messages **from the user** in the window (query like `from:@me after:<yyyy-mm-dd>`; adjust to the connector's syntax). Look for:
- a question the user asked that has no reply yet → possible blocker ("Waiting on @infra re: staging quota")
- the user answering someone or making a decision → possible Yesterday item, if significant
- incident or on-call channels → Yesterday item

Summarise; don't quote. Never include DM content, or other people's words, in the update.

## Previous standup (history)

`~/.my-standup/history/YYYY-MM-DD.md` holds each approved standup as plain text. Read the most recent one before today. Its **Today** section is the plan to check:
- done in the window → it should appear in Yesterday (as done)
- still in progress → carry over to Today
- no trace at all → carry over, and mention it under the draft so the user can drop it

Count carry-overs by looking back through the earlier files for the same item.

## Reading the user's notes

Notes beat tools. If the user says "today: finish PAY-150, blocked on creds from Dana", that's the Today and Blockers sections, with the tool data filling in links and details. If a note contradicts the data ("PAY-142 isn't done, it got reverted"), follow the note.
