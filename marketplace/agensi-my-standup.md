# Agensi listing: My Standup (my-standup)

Copy each field into the Agensi submission form (agensi.io/dashboard/submit).

## Logo
TODO: not made yet. Suggest the same family look as BidReady and RedlineReady: a speech bubble holding three short lines (yesterday / today / blockers) with a small check badge.

## Name (40 / 60 characters)
My Standup: Daily Updates From Your Work

## Summary (288 / 300 characters)
Your standup, written from what you actually did. Reads your commits, PRs, Jira or Linear tickets, calendar and Slack, groups it all by ticket, and gives you a short Yesterday / Today / Blockers update with links, ready for Slack or Teams. Remembers yesterday's plan. Free and open source (MIT).

## License
Open source, MIT. Free listing.

## Full description

### Stop rebuilding yesterday from memory at 9:58

Standup is in two minutes. You open GitHub, then Jira, then scroll Slack, trying to remember what you did after lunch yesterday. You end up posting "worked on PAY-142, continuing today", which is nothing like the day you actually had.

**My Standup reads your real activity and writes the update you'd write on a good day: short, specific, linked, and honest about blockers.**

### What it does

**🔎 Gathers from where your work already is.**
Your git commits and branches (including uncommitted work), GitHub PRs you opened, reviewed or need to review, Jira or Linear tickets you moved, today's meetings, and Slack threads where you're waiting on someone. It uses whichever of these you have and tells you which it skipped.

**🧩 Groups by ticket, not by tool.**
Six commits, a PR, a status change and a Slack thread about the same ticket become one line, named by the outcome rather than "fix tests" and "address review comments". Merge and WIP commits and routine meetings are dropped. Code reviews you did for others are kept, because people want to see them.

**🔗 Links everything.**
Every ticket and PR is linked, in Slack format, or markdown for Teams, Discord, GitHub and Notion. It never makes up a link.

**🗓️ Gets the window right.**
"Yesterday" means since your last standup, so on Monday it covers Friday and the weekend. Workdays are configurable for Sun–Thu teams.

**↩️ Remembers what you said you'd do.**
Yesterday's Today list is checked against what actually happened. Anything unfinished comes back, so plans don't quietly disappear.

**🚧 Honest blockers.**
A blocker shows up only when there's evidence: a blocked ticket, a PR waiting on review, an unanswered question, or you said so. Otherwise it says "None", because a made-up blocker sends real people chasing it.

**✅ You approve before anything is posted.**
You see the draft every time. It posts to your standup channel only after you say yes.

**📒 Keeps a standup log where you want it.**
The first time, it asks once where to keep your standups: a new Google Doc, a new Claude doc, or a doc you already have (Google Docs, Claude, Notion, Confluence). Every approved standup is added as a dated section, newest first, ready for your 1:1s and performance reviews.

### Also does
- A weekly or sprint summary (Shipped / In progress / Next week / Risks)
- A 30-second spoken version for video standups
- Turning messy notes into a clean update

### Who it's for
- **Developers** on teams with daily or async standups
- **Tech leads and EMs** who want a quick weekly summary of their own work
- **Remote teams** posting async updates in Slack or Teams

### Privacy
Runs locally with your own logins. It summarises your work only: it never quotes DMs or other people's messages. History is plain text in `~/.my-standup/`, plus the standup log doc you choose.

## Tags
standup, daily update, scrum, agile, git, github, jira, linear, slack, teams, productivity, developer tools, open source

## Category
Productivity / Developer tools
