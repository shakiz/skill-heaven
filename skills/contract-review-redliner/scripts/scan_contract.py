#!/usr/bin/env python3
"""Read a contract and scan it for mechanical problems before the legal review.

  scan_contract.py CONTRACT [--markup] [-o contract.txt]

Prints the text with paragraph numbers and clause numbers (Word auto-numbering is reconstructed):
  para 12 [9.2] Supplier's total liability ...
then a SCAN section listing:
  - tracked changes and comments already in the file (use compare_versions.py --changes for detail)
  - unfilled blanks: [●], [insert ...], ____, TBD
  - number mismatches: "thirty (60) days"
  - cross-references to clauses that don't exist
  - defined terms never used, and terms defined twice
  - documents referenced but not included (schedules, exhibits, URLs, online terms)
  - paragraphs about renewal, notice periods and termination (for the key-dates table)
--markup shows existing tracked changes inline as {+inserted+} and [-deleted-] (default: accepted view).
Formats: .docx, .pdf, .txt, .md.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Numbering, contract_paragraphs, iter_paragraphs  # noqa: E402

UNITS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen".split())}
TENS = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "_"}
SCALES = {"hundred": 100, "thousand": 1000, "million": 1000000}


def words_to_int(words):
    total, cur, seen = 0, 0, False
    for w in words:
        if w in UNITS:
            cur += UNITS[w]
        elif w in TENS:
            cur += TENS[w]
        elif w == "hundred":
            cur = max(cur, 1) * 100
        elif w in SCALES:
            total += max(cur, 1) * SCALES[w]
            cur = 0
        elif w == "and" and seen:
            continue
        else:
            return None
        seen = True
    return total + cur if seen else None


NUMWORD_RE = re.compile(r"((?:[A-Za-z]+[\s-]+){0,5}[A-Za-z]+)\s*\(\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*%?\s*\)")
BLANK_RE = re.compile(r"\[\s*[●•■_.\s]*\]|\[(?:insert|date|name|amount|address|number|tbd|tbc|x{2,}|"
                      r"●)[^\]]{0,60}\]|_{4,}|\.{6,}|\bTB[DC]\b|<(?:insert|name|date)[^>]{0,40}>",
                      re.IGNORECASE)
XREF_RE = re.compile(r"\b(?:clauses?|sections?|articles?|paragraphs?)\s+(\d+(?:\.\d+)*)(?:\s*\(([a-z]{1,4})\))?",
                     re.IGNORECASE)
DEF_RE = re.compile(r"[“\"]([A-Z][\w&'’-]*(?:\s+(?:of|and|the|[A-Z][\w&'’-]*)){0,6})[”\"]")
DOCREF_RE = re.compile(r"\b(Schedule|Exhibit|Annex|Appendix|Attachment|Order Form|Statement of Work|SOW|"
                       r"SCHEDULE|EXHIBIT|ANNEX|APPENDIX)\b(?:\s+([A-Z0-9]{1,3})\b)?")
SIGNATURE_RE = re.compile(r"\b(signed|signature|by:|name:|title:|for and on behalf)", re.IGNORECASE)
URL_RE = re.compile(r"\b(?:[a-z]{4,5}:/{2}|www\.)\S+|\b[\w-]+\.(?:com|io|net|org|co|ai|app)(?:/\S*)?", re.IGNORECASE)
ONLINE_RE = re.compile(r"\b(?:as (?:amended|updated|modified) (?:by \w+ )?from time to time|available at|posted (?:at|on)|"
                       r"incorporated (?:herein )?by reference)\b", re.IGNORECASE)
DATE_CUES = re.compile(r"\b(renew\w*|auto-?renew\w*|notice period|days'? (?:prior )?(?:written )?notice|"
                       r"terminat\w+|expir\w+|initial term|minimum term|commitment period|price increase|"
                       r"increase the fees)\b", re.IGNORECASE)


def docx_paragraphs(path, markup):
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(str(path))
    num = Numbering(doc)
    out, revs, authors = [], 0, {}
    for p in iter_paragraphs(doc):
        label = num.label(p)
        parts = []
        for run in p.iter(qn("w:r")):
            el, state, nested = run.getparent(), "", False
            while el is not None and el is not p:
                name = el.tag.rsplit("}", 1)[-1]
                if name in ("p", "Fallback"):
                    nested = True
                    break
                if name in ("ins", "moveTo"):
                    state = state or "ins"
                if name in ("del", "moveFrom"):
                    state = "del"
                el = el.getparent()
            if nested:
                continue
            txt = "".join((c.text or "") if c.tag in (qn("w:t"), qn("w:delText")) else
                          "\t" if c.tag == qn("w:tab") else "\n" if c.tag in (qn("w:br"), qn("w:cr")) else ""
                          for c in run)
            if state == "del":
                if markup and txt:
                    parts.append("[-" + txt + "-]")
                continue
            parts.append("{+" + txt + "+}" if (state == "ins" and markup and txt) else txt)
        text = "".join(parts)
        if markup:
            text = re.sub(r"\+\}\{\+", "", re.sub(r"-\]\[-", "", text))
        style = p.find(qn("w:pPr") + "/" + qn("w:pStyle"))
        sv = style.get(qn("w:val")) if style is not None else ""
        out.append({"label": label, "text": text, "heading": sv.lower().startswith(("heading", "title"))})
    for el in doc.element.body.iter():
        name = el.tag.rsplit("}", 1)[-1] if isinstance(el.tag, str) else ""
        if name in ("ins", "del") and el.getparent() is not None and \
                el.getparent().tag.rsplit("}", 1)[-1] != "rPr":
            revs += 1
            a = el.get(qn("w:author")) or "?"
            authors[a] = authors.get(a, 0) + 1
    try:
        n_comments = len(list(doc.comments))
    except Exception:
        n_comments = 0
    return out, revs, authors, n_comments


def plain_paragraphs(path):
    return [{"label": "", "text": t, "heading": False} for t in contract_paragraphs(path)]


def typed_label(text):
    m = re.match(r"^\s*(?:(?:section|clause|article)\s+)?(\d{1,3}(?:\.\d{1,3})*)[.)]?\s", text, re.IGNORECASE)
    return m.group(1) if m else ""


def scan(paras):
    findings = []
    labels = set()
    for p in paras:
        for lab in (p["label"], typed_label(p["text"])):
            lab = lab.strip().rstrip(".)").lstrip("(")
            if lab:
                labels.add(lab)
                parts = lab.split(".")
                for k in range(1, len(parts)):
                    labels.add(".".join(parts[:k]))
    full = "\n".join(p["text"] for p in paras)

    for i, p in enumerate(paras, 1):
        t = p["text"]
        if not SIGNATURE_RE.search(t):
            for m in BLANK_RE.finditer(t):
                findings.append(("blank", i, "unfilled blank {!r}".format(m.group(0).strip())))
        for m in NUMWORD_RE.finditer(t):
            words = re.split(r"[\s-]+", m.group(1).lower())
            val, shown = None, ""
            for k in range(len(words)):
                v = words_to_int(words[k:])
                if v is not None:
                    val, shown = v, " ".join(words[k:])
                    break
            digits = m.group(2).replace(",", "")
            if val is not None and digits.replace(".", "").isdigit() and float(digits) != val:
                findings.append(("number-mismatch", i, "words and digits disagree: \"{} ({})\"".format(shown, m.group(2))))
        if labels:
            for m in XREF_RE.finditer(t):
                ref = m.group(1).rstrip(".")
                if ref not in labels:
                    findings.append(("xref", i, "refers to {} {} which was not found in this document".format(
                        m.group(0).split()[0].lower(), ref)))
        for m in URL_RE.finditer(t):
            findings.append(("external-doc", i, "refers to online terms or a link: {!r} (not reviewed; ask for a copy)"
                             .format(m.group(0).rstrip(".,;)"))))
        if ONLINE_RE.search(t):
            findings.append(("external-doc", i, "terms can change or live outside the contract: {!r}".format(
                ONLINE_RE.search(t).group(0))))
        if DATE_CUES.search(t) and len(t.strip()) > 40:
            findings.append(("dates", i, "renewal/notice/termination language: \"{}\"".format(
                t.strip()[:140] + ("..." if len(t.strip()) > 140 else ""))))

    # defined terms
    defs = {}
    for i, p in enumerate(paras, 1):
        for m in DEF_RE.finditer(p["text"]):
            term = m.group(1).strip()
            if len(term) < 2 or term.isupper() and len(term) > 25:
                continue
            defs.setdefault(term, []).append(i)
    for term, where in defs.items():
        uses = len(re.findall(r"(?<![\w“\"])" + re.escape(term) + r"(?![\w”\"])", full))
        if uses == 0:
            findings.append(("definition", where[0], "defined term \"{}\" is never used".format(term)))
        if len(set(where)) > 1:
            findings.append(("definition", where[0], "\"{}\" is defined more than once (paras {})".format(
                term, ", ".join(map(str, sorted(set(where)))))))

    # referenced documents present?
    headings = " ".join(p["text"] for p in paras if p["heading"] or len(p["text"]) < 80).lower()
    seen = set()
    for i, p in enumerate(paras, 1):
        for m in DOCREF_RE.finditer(p["text"]):
            name = (m.group(1) + (" " + m.group(2) if m.group(2) else "")).strip()
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            if key not in headings:
                findings.append(("external-doc", i, "{} is referred to but does not appear to be attached".format(name)))
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("contract")
    ap.add_argument("--markup", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    p = Path(a.contract)
    if not p.exists():
        sys.exit("Not found: {}".format(p))
    ext = p.suffix.lower()
    if ext in (".doc", ".rtf", ".odt", ".pages"):
        sys.exit("Save {} as .docx (or PDF) first.".format(p.name))
    revs, authors, n_comments = 0, {}, 0
    try:
        if ext == ".docx":
            paras, revs, authors, n_comments = docx_paragraphs(p, a.markup)
        else:
            paras = plain_paragraphs(p)
    except ImportError as e:
        sys.exit("Missing library {}: python3 -m pip install -r requirements.txt".format(e.name))
    lines = ["# {}".format(p.name), ""]
    words = sum(len(x["text"].split()) for x in paras)
    if not words:
        lines.append("NO TEXT FOUND. The file may be a scanned image: ask for a .docx or a text-based PDF.")
    for i, x in enumerate(paras, 1):
        if not x["text"].strip():
            continue
        lab = "[{}] ".format(x["label"]) if x["label"] else ""
        lines.append("para {} {}{}".format(i, lab, x["text"]))
    lines += ["", "# SCAN ({} paragraphs, {} words{})".format(
        len(paras), words, ", converted from " + ext if ext != ".docx" else "")]
    if revs or n_comments:
        lines.append("- tracked changes already in this file: {} ({}); comments: {}. "
                     "This is a marked-up draft: use compare_versions.py --changes.".format(
                         revs, ", ".join("{}: {}".format(k, v) for k, v in authors.items()) or "-", n_comments))
    order = ["blank", "number-mismatch", "xref", "definition", "external-doc", "dates"]
    findings = scan(paras)
    for kind in order:
        items = [f for f in findings if f[0] == kind]
        if items:
            lines.append("## {} ({})".format(kind, len(items)))
            lines += ["- para {}: {}".format(f[1], f[2]) for f in items]
    if not findings:
        lines.append("No mechanical issues found.")
    text = "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text, encoding="utf-8")
        print("Wrote {} ({} paragraphs, {} findings)".format(a.out, len(paras), len(findings)))
        print(text[text.index("# SCAN"):])
    else:
        print(text)


if __name__ == "__main__":
    main()
