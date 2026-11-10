---
name: my-standup
description: Writes the user's daily standup update (yesterday / today / blockers) from their real activity, so they don't have to reconstruct it from memory. Pulls their own git commits and GitHub PRs, Jira or Linear tickets, calendar meetings, Slack threads and any rough notes they type, merges everything about the same ticket into one line, and returns a short Slack-ready update with ticket and PR links, then optionally posts it to their standup channel and logs it to a Google Doc, Claude doc or existing doc of their choice. Remembers yesterday's plan so unfinished items carry over. Use this skill whenever the user asks for their standup, daily update, daily status, scrum update, async check-in, "what did I do yesterday", "write my update for #standup", or pastes messy notes and wants them turned into a standup, even if they don't say the word "standup". Also use it for weekly/sprint status summaries of their own work.
---

# My Standup

Turn the user's actual activity into the update they'd write themselves on a good day: short, specific, linked, and honest about blockers. The user should be able to read it in ten seconds, fix one word, and post it.

The hard part isn't formatting. It is **choosing**: a day produces 30 commits, 6 Jira transitions, 4 meetings and a dozen Slack threads, and a standup has room for about 3–6 bullets. Group by outcome, drop the noise, and keep the link.

## Workflow

### 1. Load the config (or set it up)

The standup folder is `$MY_STANDUP_HOME` if set, otherwise `~/.my-standup`. If the user names a different folder, use that, and pass `--history <folder>/history` to the script. Below, `~/.my-standup` means whichever folder applies.

Read `~/.my-standup/config.json`. Relative paths in it are relative to the folder the user is working in. If it doesn't exist, run first-time setup (below) **unless** the user has already given you everything you need in the message (e.g. they pasted notes and just want them shaped). Never block a first standup on setup; produce it from what's available and offer setup afterwards.

Config fields (all optional; `assets/config.example.json` is the template):

| Field | Meaning | Default |
|---|---|---|
| `repo_roots` | folders to scan for git repos | current directory |
| `git_authors` | emails/names the user commits as | global `git config user.email` |
| `github` | query PRs with the `gh` CLI | `true` if `gh` is logged in |
| `tracker` | `jira`, `linear` or `none` | whichever connector exists |
| `jira_jql_extra` | extra JQL, e.g. `project = PAY` | none |
| `jira_base_url` | e.g. `https://acme.atlassian.net` for links | from the connector |
| `calendar` | include meetings | `true` if a calendar connector exists |
| `slack_channel` | where to post, e.g. `#team-standup` | none (draft only) |
| `slack_search` | include the user's own Slack threads | `true` if Slack connector exists |
| `workdays` | e.g. `sun,mon,tue,wed,thu` | `mon,tue,wed,thu,fri` |
| `link_style` | `slack`, `markdown` or `plain` | `slack` |
| `sections` | headings to use | `["Yesterday", "Today", "Blockers"]` |
| `max_bullets` | per section | `5` |
| `tone` | `terse`, `normal` or `detailed` | `terse` |
| `save_to` | where approved standups are logged: `{"type": "google_doc" \| "claude_doc" \| "notion" \| "confluence" \| "local", "url": "...", "title": "..."}` | not set → ask once (see below) |

**First-time setup**: ask at most one compact question round. Infer what you can first (git email, repos with recent commits under the working directory or `~/code`, `~/Projects`, `~/src`, which connectors are available) and ask only to confirm or fill gaps: repo folders, Jira project, Slack channel, workdays, and where to save standups (below). Write the file, then continue to the standup.

**Where to save standups (asked once, ever)**: if `save_to` is missing from the config, ask the user one question, as part of first-time setup, or at the first approval if setup was skipped: "Where should I keep your standups?" Offer only options that can actually work here:
- **A new Google Doc**: if a Google Docs or Drive connector is available.
- **A new Claude doc**: if a Claude Docs connector (or a docs skill) is available. The doc lives in their Claude account.
- **An existing doc**: they paste a link (Google Doc, Claude doc/artifact, Notion page, Confluence page). Accept it only if a connector here can write to that kind of link; otherwise say so and offer the other options.
- **Just this computer**: the local history files only.

Store the answer in `save_to` straight away, and include the URL once a new doc is created, so the question is never asked again. Only ask again if the user asks to change it ("save my standups somewhere else"). The local history in `~/.my-standup/history/` is kept whatever they choose, because it's what the window and carry-over steps read.

### 2. Work out the time window

"Yesterday" means **since the last standup**, not the last 24 hours. On the first workday of the week it covers the previous workday plus the weekend; after a holiday it covers the gap. `scripts/git_activity.py --since auto --workdays <workdays>` computes this from the workdays and the saved history; use the same window for every source. If the user says "since Thursday" or "for this week", honour that instead.

### 3. Gather from every available source, in parallel

Read `references/sources.md` for the exact calls per source. In short:

- **Git + GitHub**: run `python3 scripts/git_activity.py --roots <repo_roots> --author <git_authors> --workdays <workdays> --gh`. It returns commits (with ticket keys parsed from messages and branch names), current branches, uncommitted work, and PRs authored, reviewed or awaiting the user's review.
- **Tracker** (Jira via the Atlassian connector, or Linear): issues assigned to the user that were updated, transitioned or commented on in the window, plus everything currently In Progress / In Review / Blocked.
- **Calendar**: yesterday's meetings (for context only) and today's meetings (for the Today section).
- **Slack**: messages the user sent in the window, to find threads where they unblocked someone, made a decision, or are waiting on an answer.
- **Previous standup**: the latest file in `~/.my-standup/history/`, for yesterday's **Today** plan.
- **The user's own notes** in the message: always highest priority. They know things no tool can see.

A missing or unauthenticated source is not an error. Skip it, keep going, and mention the gap in one short line under the draft ("Skipped: calendar (not connected)"). Don't ask the user to connect things in the middle of their standup.

### 4. Build items, then merge them

Turn raw activity into **work items**, one per ticket or piece of work:

1. Key everything by ticket ID (`PAY-142`), PR URL, or, when neither exists, by repo plus branch/topic.
2. Merge: the commits, the PR, the Jira transition and the Slack thread about `PAY-142` are **one** bullet, not four.
3. Name each item by its outcome, in the user's words where possible: use the ticket title or PR title rather than commit messages. "Refund retries now back off exponentially" beats "fix tests, address review, rename var".
4. Give each item a state: done/merged, in review, in progress, started, or blocked.

**Drop**: merge commits, WIP/fixup commits, formatting and lint-only changes, routine recurring meetings (standup, 1:1s) unless something came out of them, and Slack chatter with no outcome. Group 3+ small related fixes as one bullet ("Cleaned up 4 flaky checkout tests").

**Keep, even if small**: code reviews done for others (people value seeing these), incidents and on-call work, unblocking someone, decisions made, and anything the user mentioned in their notes.

### 5. Fill the sections

- **Yesterday**: items that moved in the window, most significant first. Shipped/merged items before in-progress items.
- **Today**: the user's notes first; then yesterday's unfinished plan items (carry-over: see below); then In Progress tickets, open PRs needing follow-up, and meetings worth naming (a demo, a design review; not the daily standup). Be realistic: 2–4 items.
- **Blockers**: only real ones. Evidence that counts: a ticket in a Blocked/flagged state, a PR waiting on review for more than one working day, an unanswered question the user asked in Slack, or the user saying so. Name **who or what** is needed: "Waiting on @dana for staging DB creds". If there's nothing, write "None". **Never invent a blocker**, because a fake blocker triggers real people to act on it.

**Carry-over**: compare the previous standup's Today list against what actually happened. An item that wasn't completed goes into Today again, unless the activity shows it was dropped. Don't silently lose things the user said they'd do. If it's been carried over three or more times, keep it but mention it to the user privately below the draft (not in the update).

### 6. Write it

Read `references/format.md` for link syntax and examples. The default is Slack style, shown here as posted through the Slack connector. If the user will paste the update by hand, use the paste-safe form in format.md, because Slack doesn't render `<url|text>` in pasted text:

```
*Yesterday*
• Merged retry backoff for failed refunds <https://acme.atlassian.net/browse/PAY-142|PAY-142> (<https://github.com/acme/pay/pull/881|PR #881>)
• Reviewed Sam's webhook signature PR <https://github.com/acme/pay/pull/877|#877>
*Today*
• Finish currency rounding fix <https://acme.atlassian.net/browse/PAY-150|PAY-150>, then open PR
• Demo refunds flow to support team (2pm)
*Blockers*
• None
```

Writing rules:
- First person is implied: no "I", start bullets with a verb or the outcome.
- Every bullet about a ticket or PR carries its link. Never make up a URL or ticket key. If you don't have the real link, use the plain key.
- Keep `max_bullets` per section. If there's more, merge further rather than truncating important work.
- No internal jargon from commit messages, no SHAs, no file paths, no time-tracking numbers.
- Don't include private content: DMs, other people's messages, or anything from a calendar event marked private beyond "busy". Summarise what the *user* did.

### 7. Show, then post only on a clear yes

Show the draft in a code block so it's copy-pasteable, followed by at most two short lines: skipped sources, and anything you were unsure of ("Not sure whether PAY-150 is still yours; it was reassigned yesterday").

- If `slack_channel` is set and a Slack connector is available, ask: "Post to #team-standup?" Post **only after the user says yes**, because a message in a team channel can't really be taken back. Post with Slack mrkdwn links (`<url|text>`).
- Otherwise, the draft is the deliverable.

When the user approves (posts, or says it's good, or edits it), save the final text. If they edited it, save their version: that's what tomorrow's carry-over must compare against.

1. **Local history, always**: write `~/.my-standup/history/YYYY-MM-DD.md`.
2. **The standup log doc**, per `save_to` (if `save_to` isn't set yet, ask the one-time question first). Read `references/saving.md` for how to create and update each kind of doc. In short: add a dated section (`## Tue 10 Nov 2026`) holding that day's standup, newest at the top, with links as normal markdown links (never Slack `<url|text>`). Running it twice on the same day replaces that day's section instead of adding a second one.

If writing to the doc fails (connector down, access revoked), the local copy still stands. Say so in one line and offer to retry, but don't ask the where-to-save question again. Confirm the save in a few words, with the doc link: "Saved to your Standup log."

## Variations

- **Notes only** ("turn this into my standup: …"): skip gathering if the user clearly just wants their notes shaped, but still look up ticket links if a tracker connector is available and the notes mention ticket keys.
- **Weekly or sprint summary**: same pipeline with a longer window. Sections become *Shipped*, *In progress*, *Next week*, *Risks*. Allow up to 8 bullets in Shipped.
- **Spoken version** ("I'm on a call, give me something to say"): 3–5 plain sentences, no links, under 45 seconds read aloud.
- **Different format requested** (Teams, Discord, GitHub, Linear comment): use `markdown` link style.
- **Edits** ("drop the review, make it shorter"): change only what was asked, keep the links, re-show.
