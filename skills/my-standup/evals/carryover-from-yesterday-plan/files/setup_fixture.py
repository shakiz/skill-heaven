#!/usr/bin/env python3
"""Build test git repos and a standup folder in the current directory.

Dates are relative to today, so the "since the previous workday" window
is exercised whatever day the test runs. Usage: python3 setup_fixture.py <scenario>
Scenarios: git-notes, carryover
"""
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ME = ("Dana Reyes", "dana@acme.test")
SAM = ("Sam Okafor", "sam@acme.test")


def prev_workday(today):
    d = today - dt.timedelta(days=1)
    while d.weekday() > 4:
        d -= dt.timedelta(days=1)
    return d


def git(repo, *args, env=None):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


def init(repo):
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", ME[0])
    git(repo, "config", "user.email", ME[1])
    git(repo, "config", "commit.gpgsign", "false")


def commit(repo, msg, when, who=ME, fname=None):
    f = repo / (fname or "log.txt")
    with f.open("a") as fh:
        fh.write(f"{when.isoformat()} {msg}\n")
    git(repo, "add", "-A")
    env = {**os.environ,
           "GIT_AUTHOR_NAME": who[0], "GIT_AUTHOR_EMAIL": who[1],
           "GIT_COMMITTER_NAME": who[0], "GIT_COMMITTER_EMAIL": who[1],
           "GIT_AUTHOR_DATE": when.isoformat(), "GIT_COMMITTER_DATE": when.isoformat()}
    git(repo, "commit", "-q", "-m", msg, env=env)


def at(day, h, m=0):
    return dt.datetime.combine(day, dt.time(h, m))


def config(home, **extra):
    home.mkdir(parents=True, exist_ok=True)
    (home / "history").mkdir(exist_ok=True)
    cfg = {
        "repo_roots": ["./repos"],
        "git_authors": [ME[1]],
        "github": False,
        "tracker": "none",
        "jira_base_url": "https://acme.atlassian.net",
        "calendar": False,
        "slack_search": False,
        "workdays": "mon,tue,wed,thu,fri",
        "link_style": "slack",
        "max_bullets": 5,
    }
    cfg.update(extra)
    (home / "config.json").write_text(json.dumps(cfg, indent=2))


def git_notes():
    today = dt.date.today()
    pw = prev_workday(today)
    old = today - dt.timedelta(days=12)

    pay = Path("repos/payments")
    init(pay)
    commit(pay, "Initial payments service", at(old, 9))
    commit(pay, "PAY-120 add refund audit log table", at(old, 15))  # outside window
    git(pay, "checkout", "-q", "-b", "feature/PAY-142-refund-retry")
    commit(pay, "PAY-142 exponential backoff for failed refund retries", at(pw, 10, 5))
    commit(pay, "WIP", at(pw, 11, 40))
    commit(pay, "fix tests", at(pw, 13, 15))
    commit(pay, "address review comments", at(pw, 15, 30))
    git(pay, "checkout", "-q", "main")
    commit(pay, "PAY-139 bump stripe sdk", at(pw, 9, 30), who=SAM, fname="deps.txt")  # someone else's
    git(pay, "merge", "-q", "--no-ff", "feature/PAY-142-refund-retry", "-m",
        "Merge branch 'feature/PAY-142-refund-retry'",
        env={**os.environ, "GIT_AUTHOR_DATE": at(pw, 16).isoformat(), "GIT_COMMITTER_DATE": at(pw, 16).isoformat()})

    web = Path("repos/web")
    init(web)
    commit(web, "Initial web app", at(old, 10))
    git(web, "checkout", "-q", "-b", "WEB-77-search-filters")
    commit(web, "WEB-77 add price range filter component", at(pw, 16, 45), fname="filters.tsx")
    (web / "filters.tsx").write_text("// half-done date filter\n")  # uncommitted work
    config(Path("standup-home"))


def carryover():
    today = dt.date.today()
    pw = prev_workday(today)
    old = today - dt.timedelta(days=12)

    pay = Path("repos/payments")
    init(pay)
    commit(pay, "Initial payments service", at(old, 9))
    git(pay, "checkout", "-q", "-b", "PAY-150-currency-rounding")
    commit(pay, "PAY-150 round JPY and KRW to zero decimals", at(pw, 10, 20))
    commit(pay, "PAY-150 add rounding tests for 3-decimal currencies", at(pw, 14, 50))
    (pay / "rounding.py").write_text("# TODO: banker's rounding for BHD\n")  # uncommitted

    home = Path("standup-home")
    config(home)
    (home / "history" / f"{pw.isoformat()}.md").write_text(
        "*Yesterday*\n"
        "• Shipped refund retry backoff PAY-142 https://acme.atlassian.net/browse/PAY-142\n"
        "*Today*\n"
        "• Finish currency rounding fix PAY-150 https://acme.atlassian.net/browse/PAY-150 and open PR\n"
        "• Write refund retries runbook PAY-155 https://acme.atlassian.net/browse/PAY-155\n"
        "*Blockers*\n"
        "• None\n")


if __name__ == "__main__":
    {"git-notes": git_notes, "carryover": carryover}[sys.argv[1]]()
    print("fixture ready")
