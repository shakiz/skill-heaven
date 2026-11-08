#!/usr/bin/env python3
"""Build the proposal .docx from response.json.

  build_proposal.py response.json -o proposal.docx [--template house.docx] [--company "Name"] [--no-requirements]

Layout: cover page -> narrative sections (in order) -> "Response to requirements" in RFP order,
grouped by section. [VERIFY ...] placeholders are highlighted yellow so reviewers find them.
Requires python-docx.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PLACEHOLDER_RE, load_response  # noqa: E402

try:
    from docx import Document
    from docx.enum.text import WD_BREAK, WD_COLOR_INDEX
    from docx.shared import Pt, RGBColor
except ImportError:
    sys.exit("python-docx is required: pip install python-docx")

INLINE_RE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|" + PLACEHOLDER_RE.pattern + r")", re.IGNORECASE)


def add_inline(par, text):
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            par.add_run(text[pos:m.start()])
        tok = m.group(0)
        if tok.startswith("**"):
            par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*"):
            par.add_run(tok[1:-1]).italic = True
        else:
            run = par.add_run(tok)
            run.bold = True
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        pos = m.end()
    if pos < len(text):
        par.add_run(text[pos:])


def style_or(doc, name, fallback=None):
    try:
        doc.styles[name]
        return name
    except KeyError:
        return fallback


def add_markdown(doc, md, base_level=2):
    lines = (md or "").splitlines()
    i = 0
    para_buf = []

    def flush():
        if para_buf:
            add_inline(doc.add_paragraph(), " ".join(s.strip() for s in para_buf))
            para_buf.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            flush()
            i += 1
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            flush()
            lvl = min(base_level + len(h.group(1)) - 1, 9)
            doc.add_heading(h.group(2), level=lvl)
            i += 1
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1].strip()):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not re.match(r"^\|?\s*:?-{3,}", lines[i].strip()):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            ncol = max(len(r) for r in rows)
            t = doc.add_table(rows=len(rows), cols=ncol)
            st = style_or(doc, "Table Grid")
            if st:
                t.style = st
            for ri, r in enumerate(rows):
                for ci in range(ncol):
                    cell = t.cell(ri, ci)
                    cell.text = ""
                    add_inline(cell.paragraphs[0], r[ci] if ci < len(r) else "")
                    if ri == 0:
                        for run in cell.paragraphs[0].runs:
                            run.bold = True
            doc.add_paragraph()
            continue
        b = re.match(r"^[-*]\s+(.*)$", s)
        n = re.match(r"^\d+[.)]\s+(.*)$", s)
        if b or n:
            flush()
            indent = len(line) - len(line.lstrip())
            if b:
                style = "List Bullet 2" if indent >= 2 else "List Bullet"
            else:
                style = "List Number 2" if indent >= 2 else "List Number"
            add_inline(doc.add_paragraph(style=style_or(doc, style, None)), (b or n).group(1))
            i += 1
            continue
        para_buf.append(s)
        i += 1
    flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("response")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--template")
    ap.add_argument("--company", default="")
    ap.add_argument("--no-requirements", action="store_true", help="omit the per-requirement response chapter")
    a = ap.parse_args()

    data = load_response(a.response)
    rfp = data["rfp"]
    doc = Document(a.template) if a.template else Document()
    if not a.template:
        normal = doc.styles["Normal"]
        normal.font.name = "Calibri"
        normal.font.size = Pt(11)

    # cover
    doc.add_paragraph()
    title = doc.add_paragraph(style=style_or(doc, "Title"))
    title.add_run(rfp.get("title") or "Proposal")
    sub = doc.add_paragraph(style=style_or(doc, "Subtitle"))
    sub.add_run("Proposal to {}".format(rfp.get("client", "the client")))
    meta = []
    if rfp.get("reference"):
        meta.append("Reference: {}".format(rfp["reference"]))
    if a.company:
        meta.append("Submitted by: {}".format(a.company))
    meta.append("Date: {}".format(dt.date.today().isoformat()))
    for m in meta:
        p = doc.add_paragraph(m)
        p.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    for sec in data["sections"]:
        doc.add_heading(sec.get("title", ""), level=1)
        add_markdown(doc, sec.get("body", ""), base_level=2)

    reqs = [r for r in data["requirements"] if r.get("type") != "instruction"]
    if reqs and not a.no_requirements:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading("Response to requirements", level=1)
        current = None
        for r in reqs:
            if r.get("section") and r.get("section") != current:
                current = r["section"]
                doc.add_heading(current, level=2)
            doc.add_heading("{} {}".format(r.get("id", ""), _short(r.get("text", ""))), level=3)
            q = doc.add_paragraph()
            qr = q.add_run(r.get("text", ""))
            qr.italic = True
            qr.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            comp = r.get("compliance")
            if comp and comp != "n/a":
                cp = doc.add_paragraph()
                cp.add_run("Compliance: ").bold = True
                cp.add_run({"comply": "Fully compliant", "partial": "Partially compliant",
                            "exception": "Exception - see response"}.get(comp, comp))
            if r.get("status") == "gap" and not (r.get("answer") or "").strip():
                add_inline(doc.add_paragraph(), "[VERIFY: response pending - {}]".format(r.get("notes") or "input required"))
            else:
                add_markdown(doc, r.get("answer", ""), base_level=4)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    doc.save(a.out)
    print("Wrote {} ({} sections, {} requirement responses)".format(a.out, len(data["sections"]), len(reqs)))


def _short(text, n=70):
    t = re.sub(r"\s+", " ", text).strip()
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


if __name__ == "__main__":
    main()
