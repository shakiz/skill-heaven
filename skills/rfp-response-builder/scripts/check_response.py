#!/usr/bin/env python3
"""Validate response.json before building deliverables.

  check_response.py response.json [--library LIB] [--forbid NAME ...] [--report out.md]

Exit code 0 = no critical issues, 1 = critical issues (mandatory gaps, unknown sources, forbidden names).
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PLACEHOLDER_RE, load_response, parse_library, word_count  # noqa: E402

VALID_STATUS = {"answered", "partial", "gap", "not-applicable"}
VALID_COMPLIANCE = {"comply", "partial", "exception", "n/a", ""}
FILLER = ["best-in-class", "world-class", "cutting-edge", "synergy", "leverage", "state-of-the-art", "seamless"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("response")
    ap.add_argument("--library")
    ap.add_argument("--forbid", action="append", default=[], help="name that must not appear (other clients, competitors)")
    ap.add_argument("--report", help="also write the report to this markdown file")
    a = ap.parse_args()

    data = load_response(a.response)
    reqs = data["requirements"]
    lib = parse_library(a.library) if a.library else None
    critical, warn = [], []

    ids = Counter(r.get("id") for r in reqs)
    for i, c in ids.items():
        if c > 1:
            critical.append("Duplicate requirement id '{}' ({}x)".format(i, c))

    for r in reqs:
        rid = r.get("id", "?")
        st = r.get("status", "")
        ans = r.get("answer", "") or ""
        mand = bool(r.get("mandatory"))
        tag = "{}{}".format(rid, " (MANDATORY)" if mand else "")
        if st not in VALID_STATUS:
            critical.append("{}: invalid or missing status '{}'".format(tag, st))
        if r.get("compliance", "") not in VALID_COMPLIANCE:
            warn.append("{}: unknown compliance value '{}'".format(tag, r.get("compliance")))
        if st == "gap":
            (critical if mand else warn).append("{}: GAP - {}".format(tag, r.get("notes") or "no note on what is needed"))
            if not r.get("owner"):
                warn.append("{}: gap has no owner".format(tag))
        if st in ("answered", "partial") and not ans.strip():
            critical.append("{}: status '{}' but answer is empty".format(tag, st))
        if st == "answered" and ans.strip() and not r.get("sources"):
            warn.append("{}: answer has no sources - unverifiable claims?".format(tag))
        ph = PLACEHOLDER_RE.findall(ans)
        if ph:
            if st == "answered":
                warn.append("{}: status 'answered' but contains placeholders {} - should be 'partial'".format(tag, ph[:3]))
            else:
                warn.append("{}: placeholders to resolve {}".format(tag, ph[:3]))
        wl = r.get("word_limit")
        if wl:
            wc = word_count(ans)
            if wc > int(wl):
                critical.append("{}: {} words exceeds limit of {}".format(tag, wc, wl))
        if lib is not None:
            for s in r.get("sources") or []:
                if s == "USER":
                    continue
                e = lib.get(s)
                if not e:
                    critical.append("{}: source '{}' not found in library".format(tag, s))
                    continue
                if e["stale"]:
                    warn.append("{}: source {} is stale ({}) - confirm with {}".format(
                        tag, s, e["stale_reason"], e["meta"].get("owner", "owner")))
                if e["meta"].get("approved_for", "").startswith("internal"):
                    warn.append("{}: source {} is INTERNAL-ONLY - fine as guidance, but make sure none of its "
                                "wording or internal facts appear in the answer".format(tag, s))

    all_text = "\n".join([s.get("body", "") for s in data["sections"]] + [r.get("answer", "") or "" for r in reqs])
    for s in data["sections"]:
        for p in PLACEHOLDER_RE.findall(s.get("body", "")):
            warn.append("Section '{}': placeholder {}".format(s.get("title"), p))
    for name in a.forbid:
        hits = len(re.findall(re.escape(name), all_text, re.IGNORECASE))
        if hits:
            critical.append("Forbidden name '{}' appears {}x".format(name, hits))
    for w in FILLER:
        hits = len(re.findall(r"\b" + re.escape(w) + r"\b", all_text, re.IGNORECASE))
        if hits:
            warn.append("Filler phrase '{}' used {}x - replace with specifics".format(w, hits))
    if not data["sections"]:
        warn.append("No narrative sections (executive summary etc.)")

    by = Counter(r.get("status") for r in reqs)
    mand = [r for r in reqs if r.get("mandatory")]
    mand_ok = sum(1 for r in mand if r.get("status") in ("answered", "not-applicable"))
    lines = [
        "# Response check: {}".format(data["rfp"].get("title", "")),
        "",
        "Requirements: {} | answered {} | partial {} | gap {} | n/a {}".format(
            len(reqs), by.get("answered", 0), by.get("partial", 0), by.get("gap", 0), by.get("not-applicable", 0)),
        "Mandatory fully answered: {}/{}".format(mand_ok, len(mand)),
        "",
        "## Critical ({})".format(len(critical)),
    ] + ["- " + c for c in critical] + ["", "## Warnings ({})".format(len(warn))] + ["- " + w for w in warn]
    report = "\n".join(lines)
    print(report)
    if a.report:
        Path(a.report).write_text(report + "\n", encoding="utf-8")
    return 1 if critical else 0


if __name__ == "__main__":
    sys.exit(main())
