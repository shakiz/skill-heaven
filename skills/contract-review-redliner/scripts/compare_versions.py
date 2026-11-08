#!/usr/bin/env python3
"""See what changed in a contract: between two versions, or as tracked changes inside one .docx.

  compare_versions.py SENT RETURNED [-o diff.md]   # what the other side changed vs. what you sent
  compare_versions.py --changes FILE.docx [-o changes.md]   # list tracked changes and comments

Two-version mode reports:
  1. Proposed changes: everything that differs between your version (all changes accepted) and theirs.
  2. UNTRACKED changes: edits in their file that are NOT shown as tracked changes, i.e. silent edits.
     Tracked changes already in SENT are accepted and new ones rejected before comparing, so whatever
     still differs was changed without Track Changes (or one of your changes was removed without a trace).
  3. NEW tracked changes and comments in RETURNED, by author.
  4. What happened to the tracked changes you sent: accepted, still pending, or undone without tracking.
Any format works (.docx, .pdf, .txt, .md); tracked-change analysis needs .docx.
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Numbering, contract_paragraphs, iter_paragraphs, normalize  # noqa: E402

REV_INS = ("ins", "moveTo")
REV_DEL = ("del", "moveFrom")


def _local(el):
    return el.tag.rsplit("}", 1)[-1] if isinstance(el.tag, str) else ""


def _w(attr):
    from docx.oxml.ns import qn
    return qn("w:" + attr)


def para_view(p, keep):
    """Text of paragraph p, where keep(rev_el) says whether a revision is accepted.
    Returns (text, mark_present)."""
    out = []
    for run in p.iter(_w("r")):
        el, visible, nested = run.getparent(), True, False
        while el is not None and el is not p:
            name = _local(el)
            if name == "p" or name == "Fallback":
                nested = True
                break
            if name in REV_INS and not keep(el):
                visible = False
            if name in REV_DEL and keep(el):
                visible = False
            el = el.getparent()
        if nested or not visible:
            continue
        for c in run:
            n = _local(c)
            if n in ("t", "delText"):
                out.append(c.text or "")
            elif n == "tab":
                out.append("\t")
            elif n in ("br", "cr"):
                out.append("\n")
            elif n == "noBreakHyphen":
                out.append("-")
    mark = True
    rpr = p.find(_w("pPr") + "/" + _w("rPr"))
    if rpr is not None:
        for c in rpr:
            if _local(c) == "del" and keep(c):
                mark = False
            if _local(c) == "ins" and not keep(c):
                mark = False
    return "".join(out), mark


def docx_view(path, keep):
    from docx import Document
    doc = Document(str(path))
    num = Numbering(doc)
    paras = []
    for p in iter_paragraphs(doc):
        label = num.label(p)
        text, mark = para_view(p, keep)
        if not mark and not text.strip():
            continue
        paras.append((label, text))
    return paras


def rev_sig(el):
    kind = "ins" if _local(el) in REV_INS else "del"
    txt = "".join(t.text or "" for t in el.iter() if _local(t) in ("t", "delText"))
    return (kind, el.get(_w("author")) or "", (el.get(_w("date")) or "")[:19], txt)


def revision_sigs(path):
    """Signatures of every tracked change in a .docx (to recognise revisions carried over from it)."""
    from docx import Document
    doc = Document(str(path))
    return {rev_sig(el) for el in doc.element.body.iter() if _local(el) in REV_INS + REV_DEL}


def comment_sigs(path):
    from docx import Document
    try:
        return {(c.author, c.text.strip()) for c in Document(str(path)).comments}
    except Exception:
        return set()


def view(path, keep=None):
    if Path(path).suffix.lower() == ".docx":
        return docx_view(path, keep or (lambda el: True))
    return [("", t) for t in contract_paragraphs(path)]


def word_diff_md(a, b):
    from redline import word_diff
    out, pos = [], 0
    for o1, o2, new in word_diff(a, b):
        out.append(a[pos:o1])
        old = a[o1:o2]
        if old.strip():
            out.append("~~{}~~".format(old.strip()) + (" " if new.strip() else ""))
        if new.strip():
            out.append("**{}**".format(new.strip()))
        if (old + new)[-1:].isspace():
            out.append(" ")
        pos = o2
    out.append(a[pos:])
    return re.sub(r"[ \t]+", " ", "".join(out)).strip()


def diff_paras(A, B):
    """Yield change records between two paragraph lists of (label, text)."""
    na, nb = [normalize(t) for _, t in A], [normalize(t) for _, t in B]
    sm = difflib.SequenceMatcher(None, na, nb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        a_idx, b_idx = list(range(i1, i2)), list(range(j1, j2))
        pairs, used = [], set()
        for i in a_idx:
            best, score = None, 0.5
            for j in b_idx:
                if j in used:
                    continue
                r = difflib.SequenceMatcher(None, na[i], nb[j], autojunk=False).ratio()
                if A[i][0] and A[i][0] == B[j][0]:
                    r += 0.3  # same clause number: most likely the same clause, rewritten
                if r > score:
                    best, score = j, r
            if best is not None:
                used.add(best)
                pairs.append((i, best))
        paired_a = {i for i, _ in pairs}
        events = [(j, "changed", i) for i, j in pairs]
        events += [(None, "removed", i) for i in a_idx if i not in paired_a]
        events += [(j, "added", None) for j in b_idx if j not in used]
        for j, kind, i in sorted(events, key=lambda e: (e[0] if e[0] is not None else -1, e[2] or 0)):
            if kind == "changed":
                if na[i] == nb[j]:
                    continue
                yield {"kind": kind, "label": B[j][0] or A[i][0], "where": "para {}".format(j + 1),
                       "diff": word_diff_md(A[i][1], B[j][1]), "old": A[i][1], "new": B[j][1]}
            elif kind == "removed":
                if not na[i]:
                    continue
                yield {"kind": kind, "label": A[i][0], "where": "was para {}".format(i + 1),
                       "diff": "~~{}~~".format(A[i][1].strip()), "old": A[i][1], "new": ""}
            else:
                if not nb[j]:
                    continue
                yield {"kind": kind, "label": B[j][0], "where": "para {}".format(j + 1),
                       "diff": "**{}**".format(B[j][1].strip()), "old": "", "new": B[j][1]}


def earlier_changes_status(sent, ret, old_revs):
    """For each paragraph where SENT had tracked changes: were they accepted, still pending or undone?"""
    from docx import Document
    ret_sigs = revision_sigs(ret)
    base = view(ret, keep=lambda el: rev_sig(el) in old_revs or True)  # their proposal, everything accepted
    by_label = {}
    for lab, t in base:
        if lab:
            by_label.setdefault(lab, []).append(t)
    doc = Document(str(sent))
    num = Numbering(doc)
    rows = []
    for p in iter_paragraphs(doc):
        label = num.label(p)
        revs = [el for el in p.iter() if _local(el) in REV_INS + REV_DEL and el.getparent() is not None
                and _local(el.getparent()) != "rPr"]
        if not revs:
            continue
        mine = para_view(p, lambda el: True)[0] or para_view(p, lambda el: False)[0]
        cands = by_label.get(label) if label and len(by_label.get(label, [])) == 1 else None
        if cands:
            target = cands[0]
        else:
            target = max((t for _, t in base), key=lambda t: difflib.SequenceMatcher(
                None, normalize(mine), normalize(t), autojunk=False).ratio(), default="")
        nt = normalize(target)
        states = []
        for el in revs:
            sig = rev_sig(el)
            if not sig[3].strip():
                continue
            if sig in ret_sigs:
                states.append("pending")
            elif sig[0] == "ins" and any(r[0] == "del" and normalize(r[3]) == normalize(sig[3]) for r in ret_sigs):
                states.append("countered")  # they struck our insertion with their own tracked change
            elif sig[0] == "ins":
                states.append("accepted" if normalize(sig[3]) in nt else "undone")
            else:
                states.append("accepted" if normalize(sig[3]) not in nt else "undone")
        if not states:
            continue
        st = set(states)
        if st == {"accepted"}:
            verdict = "accepted"
        elif st == {"pending"}:
            verdict = "still pending (tracked, not yet accepted or rejected)"
        elif st == {"undone"}:
            verdict = "UNDONE without a tracked change"
        else:
            verdict = "mixed: " + ", ".join("{} {}".format(states.count(k), k) for k in ("accepted", "pending", "countered", "undone")
                                           if k in st)
        rows.append("- [{}] {}: \"{}\"".format(("\u00a7" + label) if label else "para", verdict,
                                              mine.strip()[:110] + ("..." if len(mine.strip()) > 110 else "")))
    return rows or ["(no tracked changes in the version you sent)"]


def fmt_changes(changes):
    lines = []
    for n, c in enumerate(changes, 1):
        lab = (" §" + c["label"]) if c["label"] else ""
        lines.append("{}. [{}{}] {}: {}".format(n, c["where"], lab, c["kind"], c["diff"]))
    return lines or ["(none)"]


def tracked_and_comments(path, skip_revs=frozenset(), skip_comments=frozenset()):
    """Tracked changes (grouped by author) and comments with the text they are anchored to.
    Revisions/comments whose signature is in skip_* (carried over from an earlier version) are left out."""
    from docx import Document
    doc = Document(str(path))
    num = Numbering(doc)
    changes = []
    for pi, p in enumerate(iter_paragraphs(doc), 1):
        label = num.label(p)
        context = para_view(p, lambda el: True)[0]
        for el in p.iter():
            n = _local(el)
            if n in REV_INS + REV_DEL and el.getparent() is not None and _local(el.getparent()) != "rPr":
                txt = "".join(t.text or "" for t in el.iter() if _local(t) in ("t", "delText"))
                if not txt or rev_sig(el) in skip_revs:
                    continue
                changes.append({"author": el.get(_w("author")) or "?", "date": (el.get(_w("date")) or "")[:10],
                                "type": "inserted" if n in REV_INS else "deleted", "text": txt,
                                "para": pi, "label": label, "context": context})
    comments = []
    try:
        anchors, active = {}, set()
        for el in doc.element.body.iter():
            n = _local(el)
            if n == "commentRangeStart":
                active.add(el.get(_w("id")))
                anchors.setdefault(el.get(_w("id")), "")
            elif n == "commentRangeEnd":
                active.discard(el.get(_w("id")))
            elif n in ("t", "delText") and active:
                for cid in active:
                    anchors[cid] += el.text or ""
        for c in doc.comments:
            if (c.author, c.text.strip()) in skip_comments:
                continue
            comments.append({"id": str(c.comment_id), "author": c.author, "text": c.text.strip(),
                             "anchor": anchors.get(str(c.comment_id), "").strip()})
    except Exception:
        pass
    return changes, comments


def fmt_tracked(changes, comments):
    lines = []
    if not changes:
        lines.append("No tracked changes.")
    by_author = {}
    for c in changes:
        by_author.setdefault(c["author"], []).append(c)
    for author, items in by_author.items():
        lines.append("### Tracked changes by {} ({})".format(author, len(items)))
        for c in items:
            lab = " §" + c["label"] if c["label"] else ""
            ctx = c["context"].strip()
            lines.append("- [para {}{}] {} \"{}\"  \n  in: \"{}\"".format(
                c["para"], lab, c["type"], c["text"].strip(), ctx[:220] + ("..." if len(ctx) > 220 else "")))
    lines.append("")
    lines.append("### Comments ({})".format(len(comments)))
    for c in comments:
        lines.append("- {} on \"{}\": {}".format(c["author"], c["anchor"][:120], c["text"]))
    if not comments:
        lines.append("(none)")
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--changes", action="store_true", help="list tracked changes and comments in one .docx")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    lines = []
    if a.changes:
        f = a.files[0]
        if Path(f).suffix.lower() != ".docx":
            sys.exit("--changes needs a .docx")
        ch, cm = tracked_and_comments(f)
        lines += ["# Tracked changes and comments: {}".format(Path(f).name), ""] + fmt_tracked(ch, cm)
    else:
        if len(a.files) != 2:
            sys.exit("Give two files: the version you sent, then the version you got back.")
        sent, ret = a.files
        is_docx = sent.lower().endswith(".docx")
        old_revs = revision_sigs(sent) if is_docx else set()
        old_comments = comment_sigs(sent) if is_docx else set()
        A = view(sent)  # what we proposed: all changes accepted
        B = view(ret)   # what they propose: all changes accepted
        proposed = list(diff_paras(A, B))
        lines += ["# Changes from {} to {}".format(Path(sent).name, Path(ret).name), ""]
        lines += ["## 1. Everything they changed vs. your version ({})".format(len(proposed)), ""]
        lines += fmt_changes(proposed)
        if ret.lower().endswith(".docx"):
            base = view(ret, keep=lambda el: rev_sig(el) in old_revs)
            silent = list(diff_paras(A, base))
            lines += ["", "## 2. UNTRACKED changes ({})".format(len(silent)), ""]
            if silent:
                lines.append("These edits are in their file but NOT marked as tracked changes. Raise every one.")
                lines.append("")
            lines += fmt_changes(silent)
            ch, cm = tracked_and_comments(ret, old_revs, old_comments)
            lines += ["", "## 3. NEW tracked changes and comments in {} (carried-over ones left out)".format(
                Path(ret).name), ""]
            lines += fmt_tracked(ch, cm)
            if old_revs:
                lines += ["", "## 4. What happened to your tracked changes", ""]
                lines += earlier_changes_status(sent, ret, old_revs)
        else:
            lines += ["", "(Their file is not .docx, so tracked and untracked changes can't be told apart: "
                          "treat every change above as needing review.)"]
    text = "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text, encoding="utf-8")
        print("Wrote {}".format(a.out))
    print(text)


if __name__ == "__main__":
    main()
