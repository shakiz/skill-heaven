#!/usr/bin/env python3
"""Validate review.md before anything is built or sent.

  check_review.py REVIEW_MD [--contract FILE] [--playbook DIR] [--email email-draft.md]

ERRORS (exit 1) - fix before building the redline:
  - missing contract facts (file, type, our_role, counterparty) or verdict
  - an issue with a bad risk/action, or whose `find` text is not found exactly once in the contract
  - LEAKS: counterparty-facing text (### replace, ### comment, the email) that reveals internal positions:
    fallback / walk-away wording, text copied from ### internal or from the playbook's Fallback/Walk-away,
    playbook IDs, placeholders
WARNINGS - review, then fix or accept:
  - redline text using capitalised terms the contract never uses ("Vendor" when the contract says "Supplier")
  - redline text referring to clauses that don't exist, or with words/digits that disagree
  - playbook topics for this contract type that the checklist doesn't cover
  - high-risk issues without a comment, too many issues for a readable redline
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (VALID_ACTIONS, VALID_RISK, applies, contract_paragraphs, internal_texts, locate,  # noqa: E402
                     normalize, parse_playbook, parse_review)
from scan_contract import NUMWORD_RE, XREF_RE, docx_paragraphs, typed_label, words_to_int  # noqa: E402

VALID_TYPES = ("nda", "msa", "saas", "sow", "dpa", "services", "consulting", "freelance", "supply", "vendor",
               "reseller", "partnership", "licence", "license", "employment", "lease", "loan", "other")
VALID_ROLES = ("customer", "vendor", "discloser", "recipient", "mutual", "employer", "employee", "licensor",
               "licensee", "landlord", "tenant", "partner", "other")
VALID_VERDICTS = ("sign", "sign-with-changes", "negotiate", "escalate", "do-not-sign", "summary-only")

LEAK_RE = re.compile(
    r"\b(walk[- ]?away|fall[- ]?back|bottom[- ]line|our (?:minimum|maximum|limit|floor|ceiling|red line)|"
    r"we (?:can|could|would|will|may) (?:still )?(?:accept|live with|agree to|concede|go (?:up|down) to)|"
    r"(?:internal|confidential) (?:note|only|position)|BATNA|don'?t (?:tell|mention|reveal)|"
    r"(?:negotiat\w+|trading) (?:room|chip|position)|last resort|if (?:they|the other side|[A-Z]\w+) "
    r"(?:push(?:es)? back|insists?)|our real|they don'?t (?:need to )?know)\b", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"\[(?:VERIFY|TBD|TODO|CHECK)[^\]]*\]|\bTODO\b|\{\{[^}]*\}\}|<insert[^>]*>", re.IGNORECASE)
PB_ID_RE = re.compile(r"\bPB-[A-Z0-9-]+\b")
COMMON_CAPS = set("""I A The This That These Those Each Either Neither Any All No Not If In On At By For Of To
With Without Upon Unless Where When While Such Its It Our We You Your Please Party Parties Agreement
January February March April May June July August September October November December Monday Tuesday
Wednesday Thursday Friday Saturday Sunday Clause Clauses Section Sections Schedule Exhibit Annex Appendix
Article Paragraph EU UK US USA GDPR""".split())


def ngrams(text, n=6):
    w = re.findall(r"[a-z0-9%]+", normalize(text).lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def leaks(text, internal_texts):
    found = []
    for m in LEAK_RE.finditer(text):
        found.append("internal wording \"{}\"".format(m.group(0)))
    for m in PLACEHOLDER_RE.finditer(text):
        found.append("placeholder \"{}\"".format(m.group(0)))
    for m in PB_ID_RE.finditer(text):
        found.append("playbook ID \"{}\"".format(m.group(0)))
    grams = ngrams(text)
    for label, itext in internal_texts:
        common = grams & ngrams(itext)
        if common:
            found.append("repeats {} text: \"{}...\"".format(label, sorted(common)[0]))
    return found


def contract_model(path):
    p = Path(path)
    if p.suffix.lower() == ".docx":
        paras, _, _, _ = docx_paragraphs(p, markup=False)
        texts = [x["text"] for x in paras]
        labels = {x["label"].strip().rstrip(".)").lstrip("(") for x in paras if x["label"]}
    else:
        texts = contract_paragraphs(p)
        labels = set()
    for t in texts:
        lab = typed_label(t)
        if lab:
            labels.add(lab)
    full = set()
    for lab in labels:
        parts = lab.split(".")
        for k in range(1, len(parts) + 1):
            full.add(".".join(parts[:k]))
    return texts, full


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("review")
    ap.add_argument("--contract")
    ap.add_argument("--playbook")
    ap.add_argument("--email", help="draft email to the counterparty, checked for leaks")
    a = ap.parse_args()
    rv = parse_review(a.review)
    c, v = rv["contract"], rv["verdict"]
    errors, warns = [], []

    for k in ("file", "type", "our_role", "counterparty", "our_party"):
        if not c.get(k):
            errors.append("# Contract: missing '{}:'{}".format(
                k, " (which side are we on? ask the user if unclear)" if k == "our_role" else ""))
    if c.get("type") and c["type"].lower() not in VALID_TYPES:
        warns.append("# Contract: type '{}' is not one of {}".format(c["type"], ", ".join(VALID_TYPES)))
    if c.get("our_role") and c["our_role"].lower() not in VALID_ROLES:
        warns.append("# Contract: our_role '{}' is not one of {}".format(c["our_role"], ", ".join(VALID_ROLES)))
    if not v.get("overall"):
        errors.append("# Verdict: missing 'overall:' ({})".format(" | ".join(VALID_VERDICTS)))
    elif v["overall"].lower() not in VALID_VERDICTS:
        errors.append("# Verdict: overall '{}' must be one of {}".format(v["overall"], ", ".join(VALID_VERDICTS)))

    contract = a.contract or c.get("file")
    texts, labels, full_text = None, set(), ""
    if contract:
        cp = Path(contract)
        if not cp.exists():
            alt = Path(a.review).resolve().parent / contract
            cp = alt if alt.exists() else cp
        if cp.exists():
            texts, labels = contract_model(cp)
            full_text = "\n".join(texts)
        else:
            errors.append("Contract file not found: {}".format(contract))

    playbook = {}
    pb_path = a.playbook or c.get("playbook")
    if pb_path and pb_path.strip().lower() in ("starter", "default", "starter defaults"):
        pb_path = str(Path(__file__).resolve().parent.parent / "assets" / "playbook-starter")
    if pb_path and not Path(pb_path).exists():
        warns.append("Playbook not found at {}: checklist coverage not checked".format(pb_path))
    if pb_path and Path(pb_path).exists():
        playbook = parse_playbook(pb_path)
    internal_pb = []
    for e in playbook.values():
        for lab, txt in internal_texts(e):
            internal_pb.append(("playbook {} {}".format(e["id"], lab), txt))

    new_terms = set()
    for iss in rv["issues"]:
        for m in re.finditer(r"[\u201c\"]([A-Z][\w'-]*(?:\s+[A-Z][\w'-]*){0,4})[\u201d\"]", iss.get("replace", "")):
            new_terms.update(m.group(1).split())
    topics_seen = set()
    issues = rv["issues"]
    seen_ids, spans = set(), {}
    for iss in issues:
        iid = iss["id"]
        pre = "Issue {}".format(iid)
        if iid in seen_ids:
            errors.append("{}: duplicate issue ID".format(pre))
        seen_ids.add(iid)
        risk = (iss.get("risk") or "").lower()
        action = (iss.get("action") or "").lower()
        if risk not in VALID_RISK:
            errors.append("{}: risk must be high, medium or low".format(pre))
        if action not in VALID_ACTIONS:
            errors.append("{}: action must be one of {}".format(pre, ", ".join(VALID_ACTIONS)))
        for t in re.split(r"[,\s]+", iss.get("topic", "")):
            if t:
                topics_seen.add(t)
                if playbook and t not in playbook:
                    warns.append("{}: topic {} is not in the playbook".format(pre, t))
        find = iss.get("find", "")
        if not find.strip():
            errors.append("{}: missing ### find (exact contract text to anchor on)".format(pre))
        elif texts is not None:
            occ = iss.get("occurrence")
            loc = locate(texts, find, int(occ) if occ and occ.strip().isdigit() else None)
            if loc["status"] != "found":
                errors.append("{}: find text {}: {}".format(pre, loc["status"], loc["hint"]))
        rep = iss.get("replace", "")
        if action == "replace" and rep.strip() and normalize(rep) == normalize(find):
            errors.append("{}: ### replace is identical to ### find".format(pre))
        if action in ("replace", "delete") and texts is not None and find.strip():
            occ = iss.get("occurrence")
            loc = locate(texts, find, int(occ) if occ and occ.strip().isdigit() else None)
            if loc["status"] == "found":
                pi, s0, e0 = loc["hits"][0]
                for other, (opi, os0, oe0) in spans.items():
                    if opi == pi and s0 < oe0 and os0 < e0:
                        errors.append("{}: edits the same text as Issue {}; merge them into one issue".format(pre, other))
                spans[iid] = (pi, s0, e0)
        if action in ("replace", "insert-after") and not rep.strip():
            errors.append("{}: action {} needs ### replace".format(pre, action))
        if action == "comment" and not iss.get("comment", "").strip():
            errors.append("{}: action comment needs ### comment".format(pre))
        if risk == "high" and not iss.get("comment", "").strip():
            warns.append("{}: high risk but no ### comment explaining the change to the counterparty".format(pre))
        if not iss.get("internal", "").strip():
            warns.append("{}: no ### internal note (why it matters, fallback) for your own team".format(pre))

        internal = [("### internal", iss.get("internal", ""))] + internal_pb
        for field in ("replace", "comment"):
            txt = iss.get(field, "")
            if not txt:
                continue
            for lk in leaks(txt, internal):
                errors.append("{} ### {}: LEAK, {}".format(pre, field, lk))

        if rep and full_text:
            body = rep.replace("’", "'")
            for m in re.finditer(r"\b([A-Z][a-z][A-Za-z-]+)\b", body):
                w = m.group(1)
                if w in COMMON_CAPS or w in new_terms:
                    continue
                before = body[:m.start()].rstrip()
                if not before or before[-1] in ".!?:;(\n\"\u201c":
                    # sentence start: only a party-like subject ("Vendor shall", "Vendor's") is checked
                    if not re.match(r"(?:'s|\u2019s)?\s+(?:shall|may|must|will|agrees|warrants|is|has)\b|'s|\u2019s",
                                    body[m.end():m.end() + 12]):
                        continue
                stem = w[:-1] if w.endswith("s") else w
                if not re.search(r"\b" + re.escape(stem) + r"s?\b", full_text):
                    warns.append("{}: \"{}\" in ### replace never appears in the contract; use the contract's "
                                 "own defined terms and party names".format(pre, w))
            if labels:
                for m in XREF_RE.finditer(rep):
                    after = rep[m.end():m.end() + 30].lower()
                    if re.match(r"\s*(?:\([a-z0-9]+\)\s*)?of (?:the )?(?:gdpr|uk gdpr|regulation|directive|act)\b", after) \
                            or re.match(r"\s*(?:gdpr|eu)\b", after):
                        continue  # a reference to legislation, not to this contract
                    if m.group(1).rstrip(".") not in labels:
                        warns.append("{}: ### replace refers to {} which does not exist in the contract".format(
                            pre, m.group(0)))
            for m in NUMWORD_RE.finditer(rep):
                words = re.split(r"[\s-]+", m.group(1).lower())
                for k in range(len(words)):
                    val = words_to_int(words[k:])
                    if val is not None:
                        d = m.group(2).replace(",", "")
                        if d.replace(".", "").isdigit() and float(d) != val:
                            errors.append("{}: ### replace words and digits disagree: \"{} ({})\"".format(
                                pre, " ".join(words[k:]), m.group(2)))
                        break

    if len(issues) > 25:
        warns.append("{} issues: a redline this heavy reads as a rewrite. Keep must-haves and important points "
                     "as redlines; turn minor points into comments or drop them.".format(len(issues)))

    checklist = rv["sections"].get("Checklist", "")
    if not checklist:
        warns.append("No # Checklist section: list every playbook topic for this contract as ok / issue / missing / n/a")
    if playbook and c.get("type"):
        needed = [e for e in playbook.values() if applies(e, c.get("type"), c.get("our_role"))]
        missing = [e for e in needed if e["id"] not in checklist and e["id"] not in topics_seen]
        for e in missing:
            warns.append("Checklist: playbook topic {} ({}) not covered".format(e["id"], e["title"]))

    if a.email:
        et = Path(a.email).read_text(encoding="utf-8")
        internal_all = internal_pb + [("issue {} internal".format(i["id"]), i.get("internal", "")) for i in issues]
        for lk in leaks(et, internal_all):
            errors.append("Email {}: LEAK, {}".format(Path(a.email).name, lk))

    for e in errors:
        print("ERROR  " + e)
    for w in warns:
        print("WARN   " + w)
    high = sum((i.get("risk") or "").lower() == "high" for i in issues)
    print("\n{} issues ({} high). {} errors, {} warnings.".format(len(issues), high, len(errors), len(warns)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
