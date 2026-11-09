#!/usr/bin/env python3
"""Apply the issues in review.md to the contract as real Word tracked changes and margin comments.

  redline.py REVIEW_MD -o OUT.docx [--contract FILE] [--author NAME] [--no-track] [--strict]

- The contract is read from --contract or the `file:` line of the `# Contract` block. It is never modified.
- .docx keeps its formatting. .pdf/.txt/.md are first rebuilt as a plain .docx (formatting is not kept).
- Redlines are surgical: only the words that change are struck through and inserted.
- Only the `### comment` text goes into Word. `### internal` never leaves review.md.
- Exit code 1 when an issue could not be applied (not found, ambiguous, overlapping): fix review.md and rerun.
"""
import argparse
import copy
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (VALID_ACTIONS, CLAUSE_START_RE, Numbering, Para, _CHARMAP, clean_metadata,  # noqa: E402
                     contract_paragraphs, doc_metadata, existing_comments, has_auto_number, hidden_text,
                     iter_paragraphs, locate, parse_review, remove_comments, remove_hidden_text, slug_initials,
                     utc_now)

try:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("python-docx is missing: python3 -m pip install -r requirements.txt")


# --------------------------------------------------------------------------- helpers

class Ctx:
    def __init__(self, doc, author):
        self.doc, self.author, self.date = doc, author, utc_now()
        self.initials = slug_initials(author)
        ids = [int(v) for el in doc.element.iter() for k, v in el.attrib.items()
               if k == qn("w:id") and v.lstrip("-").isdigit()]
        self.next_id = max(ids + [0]) + 1000
        self.ours = set()
        self.numbering = Numbering(doc)

    def rev(self, kind):
        el = OxmlElement("w:" + kind)
        el.set(qn("w:id"), str(self.next_id))
        el.set(qn("w:author"), self.author)
        el.set(qn("w:date"), self.date)
        self.ours.add(str(self.next_id))
        self.next_id += 1
        return el


def clean_rpr(rpr):
    if rpr is None:
        return None
    rpr = copy.deepcopy(rpr)
    for c in list(rpr):
        if c.tag in (qn("w:rPrChange"), qn("w:ins"), qn("w:del"), qn("w:vanish")):
            rpr.remove(c)
    return rpr


def make_run(text, rpr):
    r = OxmlElement("w:r")
    if rpr is not None:
        r.append(clean_rpr(rpr))
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    r.append(t)
    return r


def top_in_para(el):
    while el.getparent() is not None and el.getparent().tag != qn("w:p"):
        el = el.getparent()
    return el


def add_comment(ctx, first_el, last_el, text):
    c = ctx.doc.comments.add_comment(text=text, author=ctx.author, initials=ctx.initials)
    try:
        c._comment_elm.set(qn("w:date"), ctx.date)
    except Exception:
        pass
    cid = str(c.comment_id)
    a, b = top_in_para(first_el), top_in_para(last_el)
    start = OxmlElement("w:commentRangeStart")
    start.set(qn("w:id"), cid)
    a.addprevious(start)
    end = OxmlElement("w:commentRangeEnd")
    end.set(qn("w:id"), cid)
    b.addnext(end)
    ref_run = OxmlElement("w:r")
    ref = OxmlElement("w:commentReference")
    ref.set(qn("w:id"), cid)
    ref_run.append(ref)
    end.addnext(ref_run)


def para_rpr(p):
    """Return the paragraph-mark rPr element, creating pPr/rPr when needed."""
    ppr = p.find(qn("w:pPr"))
    if ppr is None:
        ppr = OxmlElement("w:pPr")
        p.insert(0, ppr)
    rpr = ppr.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        succ = [c for c in ppr if c.tag in (qn("w:sectPr"), qn("w:pPrChange"))]
        if succ:
            succ[0].addprevious(rpr)
        else:
            ppr.append(rpr)
    return rpr


def is_last_in_container(p):
    nxt = p.getnext()
    while nxt is not None:
        if nxt.tag in (qn("w:p"), qn("w:tbl"), qn("w:sdt")):
            return False
        nxt = nxt.getnext()
    return True


# --------------------------------------------------------------------------- word diff

TOKEN_RE = re.compile(r"\w+|\s+|[^\w\s]", re.UNICODE)


def _norm_tok(t):
    if t.isspace():
        return " "
    return "".join(_CHARMAP.get(c, c) for c in t)


def word_diff(old, new):
    """Return ops [(old_start, old_end, new_text)] turning old into new, at word granularity."""
    a, b = TOKEN_RE.findall(old), TOKEN_RE.findall(new)
    sm = difflib.SequenceMatcher(None, [_norm_tok(t) for t in a], [_norm_tok(t) for t in b], autojunk=False)
    offs = [0]
    for t in a:
        offs.append(offs[-1] + len(t))
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            ops.append(["equal", i1, i2, j1, j2])
        else:
            ops.append(["change", i1, i2, j1, j2])
    # merge changes separated by a tiny equal gap (whitespace or one short word) for readable redlines
    merged = []
    for op in ops:
        if (op[0] == "change" and len(merged) >= 2 and merged[-1][0] == "equal"
                and merged[-2][0] == "change"):
            gap = a[merged[-1][1]:merged[-1][2]]
            if all(t.isspace() for t in gap) or (len(gap) <= 3 and sum(len(t) for t in gap) <= 4):
                eq = merged.pop()
                prev = merged.pop()
                merged.append(["change", prev[1], op[2], prev[3], op[4]])
                continue
        if op[0] == "change" and merged and merged[-1][0] == "change":
            prev = merged.pop()
            op = ["change", prev[1], op[2], prev[3], op[4]]
        merged.append(op)
    out = []
    for tag, i1, i2, j1, j2 in merged:
        if tag == "change":
            out.append((offs[i1], offs[i2], "".join(b[j1:j2])))
    return out


# --------------------------------------------------------------------------- edits

class Skip(Exception):
    def __init__(self, status, detail):
        super().__init__(detail)
        self.status, self.detail = status, detail


def precheck(para, x, y):
    atoms = [a for a in para.atoms if (a.start < y and a.end > x) or (a.text == "" and x < a.start < y)]
    if any(a.locked for a in atoms):
        raise Skip("overlap", "overlaps text another issue already changed; merge the two issues")
    if any(a.kind in ("field", "object") for a in atoms):
        raise Skip("fallback", "contains a field or object")
    parents = {id(a.run.getparent()) for a in atoms}
    if len(parents) > 1:
        raise Skip("fallback", "crosses a hyperlink, content control or earlier tracked change")


def delete_range(ctx, para, x, y):
    para.split_at(x)
    para.split_at(y)
    atoms = para.covered(x, y)
    if not atoms:
        return None
    runs = []
    for a in atoms:
        if a.run not in runs:
            runs.append(a.run)
    parent = runs[0].getparent()
    i1, i2 = parent.index(runs[0]), parent.index(runs[-1])
    moving = list(parent)[i1:i2 + 1]
    d = ctx.rev("del")
    parent.insert(i1, d)
    for el in moving:
        d.append(el)
        for t in el.iter(qn("w:t")):
            t.tag = qn("w:delText")
        for t in el.iter(qn("w:instrText")):
            t.tag = qn("w:delInstrText")
    para.rebuild()
    return d


def insert_at(ctx, para, x, text, after_el=None, rpr_from=None):
    ins = ctx.rev("ins")
    rpr = None
    if rpr_from is not None:
        rpr = rpr_from.find(qn("w:rPr"))
    if after_el is not None:
        after_el.addnext(ins)
    else:
        para.split_at(x)
        prev =[a for a in para.atoms if a.text and a.end == x]
        nxt = [a for a in para.atoms if a.text and a.start == x]
        if prev:
            anchor = prev[-1].run
            if anchor.getparent().tag == qn("w:del"):
                anchor = anchor.getparent()
            anchor.addnext(ins)
            rpr = rpr if rpr is not None else prev[-1].run.find(qn("w:rPr"))
        elif nxt:
            nxt[0].run.addprevious(ins)
            rpr = rpr if rpr is not None else nxt[0].run.find(qn("w:rPr"))
        else:
            para.p.append(ins)
    ins.append(make_run(text, rpr))
    para.rebuild()
    return ins


def do_replace(ctx, para, a, b, new_text, whole_delete=False):
    old = para.text[a:b]
    ops = word_diff(old, new_text)
    if not ops:
        raise Skip("no-change", "replacement text is the same as the contract text")
    for o1, o2, _ in ops:
        precheck(para, a + o1, a + o2)
    para.explode()
    touched = []
    # right to left keeps the visual order of del/ins pairs simple; positions are stable anyway
    for o1, o2, txt in reversed(ops):
        x, y = a + o1, a + o2
        first_run = next((at.run for at in para.atoms if at.text and at.start >= x), None)
        d = delete_range(ctx, para, x, y) if y > x else None
        i = None
        if txt:
            i = insert_at(ctx, para, y, txt, after_el=d,
                          rpr_from=first_run if d is not None else None)
        touched.extend(e for e in (d, i) if e is not None)
    if whole_delete and not para.text[:a].strip() and not para.text[b:].strip() \
            and not is_last_in_container(para.p):
        para_rpr(para.p).insert(0, ctx.rev("del"))
    order = sorted(touched, key=lambda e: list(para.p.iter()).index(e))
    return order[0], order[-1]


def strip_number(text):
    m = CLAUSE_START_RE.match(text)
    if not m:
        return text, False
    stripped = re.sub(r"^\s*(?:(?:section|clause|article)\s+)?(?:\(?[0-9]{1,3}(?:\.[0-9]{1,3})*[.)]?|\([a-z]{1,4}\))\s+",
                      "", text, count=1, flags=re.IGNORECASE)
    return stripped, stripped != text


def do_insert_after(ctx, para, text, numbered=True):
    p = para.p
    auto = has_auto_number(ctx.numbering, p)
    notes = []
    blocks = [re.sub(r"\s*\n\s*", " ", blk).strip() for blk in re.split(r"\n\s*\n", text.strip())]
    blocks = [blk for blk in blocks if blk]
    tmpl_run = next((a.run for a in para.atoms if a.kind == "text" and a.text.strip()), None)
    rpr = tmpl_run.find(qn("w:rPr")) if tmpl_run is not None else None
    last, created = p, []
    for blk in blocks:
        if auto and numbered:
            blk, did = strip_number(blk)
            if did:
                notes.append("removed a typed clause number (the paragraph is auto-numbered)")
        np_ = OxmlElement("w:p")
        ppr = p.find(qn("w:pPr"))
        if ppr is not None:
            ppr = copy.deepcopy(ppr)
            for c in list(ppr):
                if c.tag in (qn("w:sectPr"), qn("w:pPrChange")):
                    ppr.remove(c)
            prpr = ppr.find(qn("w:rPr"))
            if prpr is not None:
                for c in list(prpr):
                    if c.tag in (qn("w:ins"), qn("w:del"), qn("w:rPrChange")):
                        prpr.remove(c)
            if not numbered:
                old = ppr.find(qn("w:numPr"))
                if old is not None:
                    ppr.remove(old)
                if auto:
                    numpr = OxmlElement("w:numPr")
                    il = OxmlElement("w:ilvl")
                    il.set(qn("w:val"), "0")
                    nid = OxmlElement("w:numId")
                    nid.set(qn("w:val"), "0")
                    numpr.append(il)
                    numpr.append(nid)
                    ps = ppr.find(qn("w:pStyle"))
                    (ps.addnext(numpr) if ps is not None else ppr.insert(0, numpr))
            np_.append(ppr)
        last.addnext(np_)
        para_rpr(np_).insert(0, ctx.rev("ins"))
        ins = ctx.rev("ins")
        ins.append(make_run(blk, rpr))
        np_.append(ins)
        created.append(ins)
        last = np_
    if not created:
        raise Skip("invalid", "nothing to insert")
    return created[0], created[-1], "; ".join(sorted(set(notes)))


def do_comment_only(ctx, para, a, b):
    para.explode()
    para.split_at(a)
    para.split_at(b)
    atoms = [x for x in para.covered(a, b) if x.text]
    if not atoms:
        return None, None
    return atoms[0].run, atoms[-1].run


# --------------------------------------------------------------------------- source loading

def load_source(path):
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".docx":
        return Document(str(p)), None
    if ext in (".doc", ".rtf", ".odt", ".pages", ".wpd"):
        sys.exit("{} is {}: open it and 'Save As' .docx (or run: soffice --headless --convert-to docx), "
                 "then rerun.".format(p.name, ext))
    paras = contract_paragraphs(p)
    if not paras:
        sys.exit("No text found in {}. It may be a scanned image: ask for a .docx or a text PDF.".format(p.name))
    doc = Document()
    for t in paras:
        short = len(t) < 90 and not t.rstrip().endswith((".", ";", ","))
        heading = short and (t.isupper() or re.match(r"^(?:\d{1,2}\.?|[A-Z]\.)\s+[A-Z]", t))
        doc.add_paragraph(t, style="Heading 2" if heading else None)
    return doc, "rebuilt from {} as a plain Word document (original layout not kept)".format(ext)


def enable_tracking(doc):
    settings = doc.settings.element
    if settings.find(qn("w:trackRevisions")) is not None:
        return
    succ = ("doNotTrackMoves doNotTrackFormatting documentProtection autoFormatOverride styleLockTheme "
            "styleLockQFSet defaultTabStop autoHyphenation consecutiveHyphenLimit hyphenationZone "
            "doNotHyphenateCaps showEnvelope summaryLength clickAndTypeStyle defaultTableStyle "
            "evenAndOddHeaders bookFoldRevPrinting bookFoldPrinting bookFoldPrintingSheets "
            "drawingGridHorizontalSpacing drawingGridVerticalSpacing displayHorizontalDrawingGridEvery "
            "displayVerticalDrawingGridEvery doNotUseMarginsForDrawingGridOrigin drawingGridHorizontalOrigin "
            "drawingGridVerticalOrigin doNotShadeFormData noPunctuationKerning characterSpacingControl "
            "printTwoOnOne strictFirstAndLastChars noLineBreaksAfter noLineBreaksBefore savePreviewPicture "
            "doNotValidateAgainstSchema saveInvalidXml ignoreMixedContent alwaysShowPlaceholderText "
            "doNotDemarcateInvalidXml saveXmlDataOnly useXSLTWhenSaving saveThroughXslt showXMLTags "
            "alwaysMergeEmptyNamespace updateFields hdrShapeDefaults footnotePr endnotePr compat docVars "
            "rsids mathPr attachedSchema themeFontLang clrSchemeMapping doNotIncludeSubdocsInStats "
            "doNotAutoCompressPictures forceUpgrade captions readModeInkLockDown smartTagType schemaLibrary "
            "shapeDefaults doNotEmbedSmartTags decimalSymbol listSeparator").split()
    tr = OxmlElement("w:trackRevisions")
    for name in succ:
        el = settings.find(qn("w:" + name))
        if el is not None:
            el.addprevious(tr)
            return
    settings.append(tr)


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("review")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--contract")
    ap.add_argument("--author")
    ap.add_argument("--no-track", action="store_true", help="do not switch on Track Changes in the output")
    ap.add_argument("--strict", action="store_true", help="do not write the file if any issue fails")
    ap.add_argument("--remove-comments-by", nargs="+", default=[], metavar="AUTHOR",
                    help="remove existing comments by these authors (e.g. colleagues' internal notes)")
    ap.add_argument("--remove-all-comments", action="store_true", help="remove every comment already in the file")
    ap.add_argument("--keep-metadata", action="store_true",
                    help="keep document properties as they are (default: author set to --author; comments, "
                         "keywords, subject and category cleared)")
    ap.add_argument("--remove-hidden-text", action="store_true", help="delete text formatted as hidden")
    a = ap.parse_args()

    rv = parse_review(a.review)
    c = rv["contract"]
    src = a.contract or c.get("file")
    if not src:
        sys.exit("No contract: pass --contract or add 'file:' to the # Contract block.")
    srcp = Path(src)
    if not srcp.exists():
        alt = Path(a.review).resolve().parent / src
        if alt.exists():
            srcp = alt
        else:
            sys.exit("Contract file not found: {}".format(src))
    out = Path(a.out)
    if out.resolve() == srcp.resolve():
        sys.exit("Refusing to overwrite the original contract. Choose another output name.")
    author = a.author or c.get("author") or c.get("our_party") or "Reviewer"

    doc, note = load_source(srcp)
    hygiene = []
    old_comments = existing_comments(doc)
    if old_comments:
        drop = [c["id"] for c in old_comments if a.remove_all_comments or c["author"] in a.remove_comments_by]
        n = remove_comments(doc, drop)
        if n:
            hygiene.append("removed {} existing comment(s)".format(n))
        kept = [c for c in old_comments if c["id"] not in drop]
        for c in kept:
            hygiene.append("WARNING: kept existing comment by {}: \"{}\" (it will be sent; remove with "
                           "--remove-comments-by if internal)".format(c["author"] or "?", c["text"][:90]))
    meta = doc_metadata(doc)
    if not a.keep_metadata:
        clean_metadata(doc, author)
        dropped = {k: v for k, v in meta.items() if k in ("comments", "keywords", "subject", "category", "content_status")
                   or (k in ("author", "last_modified_by") and v != author)}
        if dropped:
            hygiene.append("document properties cleaned: " + "; ".join("{}={!r}".format(k, str(v)[:60])
                                                                      for k, v in dropped.items()))
    hid = hidden_text(doc)
    if hid:
        if a.remove_hidden_text:
            hygiene.append("removed {} hidden-text run(s)".format(remove_hidden_text(doc)))
        else:
            hygiene.append("WARNING: hidden text in the file will be sent: \"{}\" (use --remove-hidden-text)".format(
                " ".join(hid)[:120]))
    ctx = Ctx(doc, author)
    paras = [Para(p, ctx.ours) for p in iter_paragraphs(doc)]
    texts = [pa.text for pa in paras]

    results = []
    for iss in rv["issues"]:
        iid = iss["id"]
        action = (iss.get("action") or "").strip().lower()
        find = iss.get("find", "")
        comment = iss.get("comment", "").strip()
        try:
            if action not in VALID_ACTIONS:
                raise Skip("invalid", "action must be one of " + ", ".join(VALID_ACTIONS))
            if not find.strip():
                raise Skip("invalid", "missing ### find")
            occ = iss.get("occurrence")
            loc = locate(texts, find, int(occ) if occ and occ.strip().isdigit() else None)
            if loc["status"] != "found":
                raise Skip(loc["status"], loc["hint"])
            pi, s, e = loc["hits"][0]
            para = paras[pi]
            detail = "matched ({})".format(loc["mode"]) if loc["mode"] != "exact" else ""
            if action in ("replace", "delete"):
                new = "" if action == "delete" else re.sub(r"\s*\n\s*", " ", iss.get("replace", "")).strip()
                if action == "delete" and s > 0 and para.text[s - 1] == " " and (e == len(para.text) or para.text[e] in " .,;"):
                    s -= 1  # take the space before a removed sentence with it
                if action == "replace" and not new:
                    raise Skip("invalid", "replace needs a ### replace section (use action: delete to remove text)")
                try:
                    first, last = do_replace(ctx, para, s, e, new, whole_delete=(action == "delete"))
                    status = "applied"
                except Skip as sk:
                    if sk.status != "fallback":
                        raise
                    first, last = do_comment_only(ctx, para, s, e)
                    comment = ("Proposed change: " + (("replace with \"{}\"".format(new)) if new else "delete this text")
                               + (". " + comment if comment else ""))
                    status, detail = "comment-fallback", sk.detail
            elif action == "insert-after":
                if not iss.get("replace", "").strip():
                    raise Skip("invalid", "insert-after needs the new text under ### replace")
                numbered = (iss.get("numbered", "yes").strip().lower() not in ("no", "false"))
                first, last, n = do_insert_after(ctx, para, iss["replace"], numbered)
                status, detail = "applied", "; ".join(x for x in (detail, n) if x)
            else:
                if not comment:
                    raise Skip("invalid", "comment action needs a ### comment section")
                first, last = do_comment_only(ctx, para, s, e)
                status = "applied"
            if comment and first is not None:
                add_comment(ctx, first, last, comment)
            results.append((iid, action, status, detail))
        except Skip as sk:
            results.append((iid, action or "?", sk.status, sk.detail))

    failed = [r for r in results if r[2] not in ("applied", "comment-fallback")]
    print("Redline of {} by '{}'{}".format(srcp.name, author, " ({})".format(note) if note else ""))
    w = max([len(r[0]) for r in results] + [5])
    for iid, action, status, detail in results:
        print("  {:<{w}}  {:<12}  {:<16} {}".format(iid, action, status, detail, w=w))
    if not results:
        print("  No issues in review.md.")
    for h in hygiene:
        print("  " + h)
    if failed and a.strict:
        sys.exit("{} issue(s) failed; nothing written (--strict).".format(len(failed)))
    if not a.no_track:
        enable_tracking(doc)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print("Saved {}: {} applied, {} as comment only, {} failed.".format(
        out, sum(r[2] == "applied" for r in results), sum(r[2] == "comment-fallback" for r in results), len(failed)))
    if failed:
        print("Fix the failed issues in review.md (see hints) and run again on the ORIGINAL contract.")
        sys.exit(1)


if __name__ == "__main__":
    main()
