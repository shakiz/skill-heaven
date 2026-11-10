# My Standup

Your daily standup, written from what you actually did. It reads your commits, PRs, tickets, calendar and Slack, groups everything by ticket, and gives you a short Yesterday / Today / Blockers update with links, ready to post.

## What you get

- **A ready-to-post update.** Slack format by default, with Jira/Linear tickets and GitHub PRs linked. Markdown for Teams, Discord, GitHub or Notion, or plain text to read aloud.
- **Outcomes, not commit messages.** Six commits, a PR, a Jira transition and a Slack thread about `PAY-142` become one line: *Shipped refund retry backoff PAY-142 (PR #881)*. Merge, WIP and fixup commits are dropped.
- **The right window.** "Yesterday" means since your last standup, so Monday covers Friday and the weekend. Workdays are configurable (e.g. Sun–Thu).
- **Carry-over.** Yesterday's plan is remembered. Anything you said you'd do that didn't happen comes back in Today, so it doesn't quietly disappear.
- **Honest blockers.** Only real ones: a blocked or flagged ticket, a PR waiting on review for more than a day, an unanswered question, or you said so. Otherwise "None".
- **Posts only when you say yes.** You see the draft first, every time.

## Quick start

> "Write my standup."

> "Standup for #payments-standup, and I'm blocked on staging creds from Dana."

> "Turn these notes into my standup for Teams: …"

> "Give me a weekly summary of what I shipped."

The first time, it asks one short round of setup questions (which repo folders, which Jira project, which Slack channel, your workdays) and saves them to `~/.my-standup/config.json`. See `assets/config.example.json` for every option. Set `MY_STANDUP_HOME` to keep the config and history somewhere else.

## Sources

| Source | How | Needed? |
|---|---|---|
| Git commits, branches, uncommitted work | `scripts/git_activity.py` reads your local repos | Recommended |
| GitHub PRs authored, reviewed, awaiting your review | `gh` CLI (your own login) | Optional |
| Jira or Linear tickets | Atlassian or Linear connector | Optional |
| Meetings | Google Calendar or Outlook connector | Optional |
| Your Slack threads | Slack connector | Optional |
| Your notes | type them in | Always wins |

Use whichever sources you have. The draft says which ones it skipped.

## Privacy

- Everything runs on your machine with your own logins. The bundled script uses only the Python standard library; its only network access is the optional `gh` call.
- The update summarises **your** work. It doesn't quote DMs or other people's messages, and private calendar events are treated as "busy".
- Approved standups are saved as plain text in `~/.my-standup/history/`, and only there. Delete the folder whenever you like.

## Requirements

Python 3.8+ and git. Optional: the `gh` CLI and the Jira/Linear, calendar and Slack connectors in your Claude client.

## License

MIT. See `LICENSE`. Contributions welcome.
