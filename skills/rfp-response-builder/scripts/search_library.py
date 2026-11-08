#!/usr/bin/env python3
"""Search the answer library.

  search_library.py --library LIB --query "data encryption at rest" [--top 5]
  search_library.py --library LIB --id ANS-SEC-004        # print one entry in full
  search_library.py --library LIB --list                  # list all entry IDs and titles
"""
import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import parse_library  # noqa: E402

STOP = set(
    "a an and are as at be by can do does for from has have how i in is it its of on or our "
    "please provide describe the their this to we what when where which who will with you your "
    "shall must should may any all".split()
)


def tokens(text):
    out = []
    for t in re.findall(r"[a-z0-9]+", text.lower()):
        if t in STOP or len(t) < 2:
            continue
        # crude stemming so "encrypt"/"encryption"/"encrypted" meet
        for suf in ("ation", "ions", "ing", "ed", "es", "s"):
            if len(t) > len(suf) + 3 and t.endswith(suf):
                t = t[: -len(suf)]
                break
        out.append(t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--library", required=True)
    ap.add_argument("--query")
    ap.add_argument("--id")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()

    lib = parse_library(a.library)
    if not lib:
        print("Library at '{}' is empty or missing. Draft with [VERIFY] markers.".format(a.library))
        return 1

    if a.list:
        for e in lib.values():
            flag = "  STALE({})".format(e["stale_reason"]) if e["stale"] else ""
            print("{:<14} {}  [{}]{}".format(e["id"], e["title"], e["file"], flag))
        return 0

    if a.id:
        e = lib.get(a.id)
        if not e:
            print("No entry with id {}".format(a.id))
            return 1
        print("## {}: {}".format(e["id"], e["title"]))
        for k, v in e["meta"].items():
            print("{}: {}".format(k, v))
        if e["stale"]:
            print("!! STALE: {} - confirm with owner before use".format(e["stale_reason"]))
        print()
        print(e["body"])
        return 0

    if not a.query:
        ap.error("give --query, --id or --list")

    docs = {}
    for e in lib.values():
        # title and tags count triple: they are curated summaries of the entry
        weighted = " ".join([e["title"]] * 3 + [e["meta"].get("tags", "")] * 3 + [e["body"]])
        docs[e["id"]] = Counter(tokens(weighted))
    n = len(docs)
    df = Counter(t for c in docs.values() for t in c)
    q = tokens(a.query)
    scores = []
    for eid, c in docs.items():
        length = sum(c.values()) or 1
        s = sum((1 + math.log(c[t])) * math.log(1 + n / df[t]) for t in set(q) if c[t])
        if s > 0:
            scores.append((s / math.sqrt(length) * 10, eid))
    scores.sort(reverse=True)
    if not scores:
        print("No matches for: {}  -> likely a GAP (status: gap, name an owner)".format(a.query))
        return 0
    for s, eid in scores[: a.top]:
        e = lib[eid]
        flag = "  STALE({})".format(e["stale_reason"]) if e["stale"] else ""
        internal = "  INTERNAL-ONLY" if e["meta"].get("approved_for", "").startswith("internal") else ""
        snippet = re.sub(r"\s+", " ", e["body"])[:160]
        print("{:5.2f}  {:<14} {}{}{}\n       {}…".format(s, eid, e["title"], flag, internal, snippet))
    return 0


if __name__ == "__main__":
    sys.exit(main())
