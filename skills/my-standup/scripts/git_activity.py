#!/usr/bin/env python3
"""Collect your own git (and optionally GitHub PR) activity for a standup.

Usage:
  python3 git_activity.py [--roots DIR ...] [--since auto|YYYY-MM-DD|YYYY-MM-DDTHH:MM]
                          [--author EMAIL ...] [--workdays mon,tue,wed,thu,fri]
                          [--history DIR] [--gh] [--depth 3]

Prints JSON to stdout:
  {
    "window": {"since": ISO, "until": ISO, "reason": "..."},
    "authors": [...],
    "repos": [{"path", "name", "branch", "dirty_files", "commits": [...], "ticket_keys": [...]}],
    "pull_requests": [...] | null,        # only with --gh and a logged-in gh CLI
    "warnings": [...]
  }

Standard library only. Reads local repositories; the only network access is the
optional `gh` call, which uses the user's own GitHub CLI login.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
TICKET_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,9}-\d{1,6})\b")
NOISE_RE = re.compile(r"^(merge (branch|pull request|remote-tracking)|wip\b|fixup!|squash!)", re.I)
SKIP_DIRS = {"node_modules", ".venv", "venv", "vendor", "dist", "build", "target", ".cache", "Library"}


def run(cmd: list[str], cwd: str | None = None) -> str:
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout if out.returncode == 0 else ""


def parse_workdays(text: str) -> set[int]:
    days = {DAY_NAMES.index(d.strip()[:3].lower()) for d in text.split(",") if d.strip()[:3].lower() in DAY_NAMES}
    return days or {0, 1, 2, 3, 4}


def previous_workday(today: dt.date, workdays: set[int]) -> dt.date:
    d = today - dt.timedelta(days=1)
    for _ in range(14):
        if d.weekday() in workdays:
            return d
        d -= dt.timedelta(days=1)
    return today - dt.timedelta(days=1)


def last_history_time(history: Path | None, today: dt.date) -> tuple[dt.date, dt.datetime] | None:
    """Timestamp of the most recent saved standup before today, if any."""
    if not history or not history.is_dir():
        return None
    best = None
    for f in history.glob("*.md"):
        try:
            d = dt.date.fromisoformat(f.stem[:10])
        except ValueError:
            continue
        if d < today and (best is None or d > best[0]):
            best = (d, f)
    if not best:
        return None
    saved = dt.datetime.fromtimestamp(best[1].stat().st_mtime)
    # Saved later than its own day (copied, edited): fall back to the end of that day.
    if saved.date() != best[0]:
        saved = dt.datetime.combine(best[0], dt.time(23, 59))
    return best[0], saved


def resolve_window(since: str, workdays: set[int], history: Path | None) -> tuple[dt.datetime, str]:
    now = dt.datetime.now()
    today = now.date()
    if since != "auto":
        try:
            start = dt.datetime.fromisoformat(since)
        except ValueError:
            sys.exit(f"Bad --since value: {since!r} (use auto, YYYY-MM-DD or YYYY-MM-DDTHH:MM)")
        return start, "given explicitly"
    prev = previous_workday(today, workdays)
    prev_start = dt.datetime.combine(prev, dt.time.min)
    found = last_history_time(history, today)
    # A gap since the last saved standup (holiday, sick day) widens the window to cover it.
    if found and found[0] < prev:
        day, saved = found
        if (today - day).days <= 14:
            return saved, f"since the last saved standup ({day:%A %Y-%m-%d})"
    if found:
        return prev_start, f"start of the previous workday ({prev:%A %Y-%m-%d}); last saved standup was {found[0]:%A}"
    return prev_start, f"start of the previous workday ({prev:%A %Y-%m-%d})"


def find_repos(roots: list[str], depth: int) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        base = Path(root).expanduser().resolve()
        if not base.is_dir():
            continue
        if (base / ".git").exists():
            found.append(base)
            continue
        for dirpath, dirnames, _ in os.walk(base):
            rel_depth = len(Path(dirpath).relative_to(base).parts)
            if ".git" in dirnames:
                found.append(Path(dirpath))
                dirnames[:] = []  # don't descend into a repo
                continue
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS]
            if rel_depth >= depth:
                dirnames[:] = []
    return sorted(set(found))


def default_authors() -> list[str]:
    email = run(["git", "config", "--global", "user.email"]).strip()
    return [email] if email else []


def repo_activity(repo: Path, since: dt.datetime, authors: list[str]) -> dict | None:
    cwd = str(repo)
    if not authors:
        local = run(["git", "config", "user.email"], cwd).strip()
        authors = [local] if local else []
    if not authors:
        return None
    cmd = ["git", "log", "--all", "--no-merges", f"--since={since.isoformat(timespec='minutes')}",
           "--date=iso-strict", "--pretty=format:%H%x1f%ad%x1f%s%x1f%D"]
    for a in authors:
        cmd.append(f"--author={a}")
    raw = run(cmd, cwd)
    commits, keys = [], []
    seen = set()
    remotes = set(run(["git", "remote"], cwd).split())
    for line in raw.splitlines():
        parts = line.split("\x1f")
        if len(parts) < 3 or parts[0] in seen:
            continue
        seen.add(parts[0])
        subject = parts[2].strip()
        refs = parts[3] if len(parts) > 3 else ""
        branches = run(["git", "branch", "--all", "--contains", parts[0], "--format=%(refname:short)"], cwd).split()
        branches = [b for b in branches if b not in remotes and not b.endswith("/HEAD")]
        found = TICKET_RE.findall(subject + " " + " ".join(branches) + " " + refs)
        keys.extend(found)
        commits.append({
            "sha": parts[0][:9],
            "date": parts[1],
            "subject": subject,
            "branches": branches[:5],
            "ticket_keys": sorted(set(found)),
            "noise": bool(NOISE_RE.match(subject)),
        })
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd).strip()
    dirty = len([l for l in run(["git", "status", "--porcelain"], cwd).splitlines() if l.strip()])
    if not commits and not dirty:
        return None
    remote = run(["git", "config", "--get", "remote.origin.url"], cwd).strip()
    keys.extend(TICKET_RE.findall(branch))
    return {
        "path": cwd,
        "name": repo.name,
        "remote": remote or None,
        "branch": branch,
        "branch_ticket_keys": sorted(set(TICKET_RE.findall(branch))),
        "dirty_files": dirty,
        "commits": commits,
        "ticket_keys": sorted(set(keys)),
    }


def gh_pull_requests(since: dt.datetime, warnings: list[str]) -> list[dict] | None:
    if not shutil.which("gh"):
        warnings.append("gh CLI not installed: GitHub PRs skipped.")
        return None
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        warnings.append("gh CLI not logged in: GitHub PRs skipped (run `gh auth login`).")
        return None
    fields = "number,title,url,state,isDraft,repository,updatedAt,createdAt"
    results: dict[str, dict] = {}
    queries = [
        ("authored", ["gh", "search", "prs", "--author", "@me", "--updated", f">={since.date().isoformat()}"]),
        ("reviewed", ["gh", "search", "prs", "--reviewed-by", "@me", "--updated", f">={since.date().isoformat()}"]),
        ("open-authored", ["gh", "search", "prs", "--author", "@me", "--state", "open"]),
        ("review-requested", ["gh", "search", "prs", "--review-requested", "@me", "--state", "open"]),
    ]
    for role, cmd in queries:
        raw = run(cmd + ["--limit", "50", "--json", fields])
        try:
            items = json.loads(raw) if raw else []
        except json.JSONDecodeError:
            items = []
        for pr in items:
            entry = results.setdefault(pr["url"], {**pr, "roles": []})
            entry["roles"].append(role)
            entry["repository"] = (pr.get("repository") or {}).get("nameWithOwner")
            entry["ticket_keys"] = sorted(set(TICKET_RE.findall(pr.get("title", ""))))
    return sorted(results.values(), key=lambda p: p.get("updatedAt", ""), reverse=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", default=["."], help="repos or folders to scan for repos")
    ap.add_argument("--since", default="auto")
    ap.add_argument("--author", nargs="*", default=None, help="author emails/names (default: global git user.email)")
    ap.add_argument("--workdays", default="mon,tue,wed,thu,fri")
    home = os.environ.get("MY_STANDUP_HOME", "~/.my-standup")
    ap.add_argument("--history", default=str(Path(home, "history").expanduser()),
                    help="saved standups folder (default: $MY_STANDUP_HOME/history or ~/.my-standup/history)")
    ap.add_argument("--gh", action="store_true", help="also query GitHub PRs with the gh CLI")
    ap.add_argument("--depth", type=int, default=3, help="how deep to search roots for repos")
    args = ap.parse_args()

    warnings: list[str] = []
    workdays = parse_workdays(args.workdays)
    since, reason = resolve_window(args.since, workdays, Path(args.history).expanduser())
    authors = args.author if args.author else default_authors()
    if not authors:
        warnings.append("No author given and no global git user.email: using each repo's local user.email.")

    repos = []
    scanned = find_repos(args.roots, args.depth)
    if not scanned:
        warnings.append(f"No git repositories found under: {', '.join(args.roots)}")
    for repo in scanned:
        info = repo_activity(repo, since, authors)
        if info:
            repos.append(info)

    prs = gh_pull_requests(since, warnings) if args.gh else None
    print(json.dumps({
        "window": {"since": since.isoformat(timespec="minutes"),
                   "until": dt.datetime.now().isoformat(timespec="minutes"),
                   "reason": reason},
        "authors": authors,
        "repos_scanned": len(scanned),
        "repos": repos,
        "pull_requests": prs,
        "warnings": warnings,
    }, indent=2))


if __name__ == "__main__":
    main()
