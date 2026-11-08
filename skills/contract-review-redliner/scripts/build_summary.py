#!/usr/bin/env python3
"""Build the INTERNAL review summary (.docx) from review.md.

  build_summary.py REVIEW_MD -o review-summary.docx [--reviewer "Name"]

Contains: verdict, key terms, an issues table coloured by risk, each issue with the contract text, our
proposal, the comment sent to the counterparty and the internal note, then any other sections of review.md
(key dates, checklist, open questions, next steps). Marked internal in the page header: it holds fallbacks.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import parse_review  # noqa: E402

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor
except ImportError:
    sys.exit("python-docx is missing: python3 -m pip install -r requirements.txt")

RISK_FILL = {"high": "F8D7DA", "medium": "FFF3CD", "low": "D1E7DD"}
VERDICT_TEXT = {"sign": "OK TO SIGN", "sign-with-changes": "SIGN WITH MINOR CHANGES", "negotiate": "NEGOTIATE BEFORE SIGNING",
                "escalate": "ESCALATE TO A LAWYER", "do-not-sign": "DO NOT SIGN AS DRAFTED",
                "summary-only": "SIGNED CONTRACT SUMMARY"}
NAVY = RGBColor(0x14, 0x21, 0x3D)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), fill)
    tcpr.append(sh)


def add_inline(par, text):
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|~~[^~]+~~)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            par.add_run(part[2:-2]).bold = True
        elif part.startswith("~~") and part.endswith("~~"):
            par.add_run(part[2:-2]).font.strike = True
        elif part.startswith("`") and part.endswith("`"):
            r = par.add_run(part[1:-1])
            r.font.name = "Consolas"
        else:
            par.add_run(part)


def render_md(doc, md):
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                n = max(len(r) for r in rows)
                t = doc.add_table(rows=len(rows), cols=n)
                t.style = "Table Grid"
                for r, row in enumerate(rows):
                    for k in range(n):
                        cell = t.cell(r, k)
                        cell.text = ""
                        add_inline(cell.paragraphs[0], row[k] if k < len(row) else "")
                        if r == 0:
                            for run in cell.paragraphs[0].runs:
                                run.bold = True
                doc.add_paragraph()
            continue
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            doc.add_heading(m.group(2), level=min(len(m.group(1)), 3))
        elif re.match(r"^\s*[-*]\s+", line):
            add_inline(doc.add_paragraph(style="List Bullet"), re.sub(r"^\s*[-*]\s+", "", line))
        elif re.match(r"^\s*\d+[.)]\s+", line):
            add_inline(doc.add_paragraph(style="List Number"), re.sub(r"^\s*\d+[.)]\s+", "", line))
        elif line.startswith(">"):
            p = doc.add_paragraph()
            add_inline(p, line.lstrip("> "))
            p.paragraph_format.left_indent = Pt(18)
        else:
            add_inline(doc.add_paragraph(), line)
        i += 1


def label_value(doc, label, value):
    if not value:
        return
    p = doc.add_paragraph()
    p.add_run(label + ": ").bold = True
    add_inline(p, re.sub(r"\s*\n\s*", " ", value))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("review")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--reviewer")
    a = ap.parse_args()
    rv = parse_review(a.review)
    c, v, issues = rv["contract"], rv["verdict"], rv["issues"]

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    hdr = doc.sections[0].header.paragraphs[0]
    hdr.text = "INTERNAL: contains negotiation positions. Do not send to the counterparty."
    hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in hdr.runs:
        r.font.size, r.font.color.rgb, r.bold = Pt(8), RGBColor(0xB0, 0x1E, 0x2F), True

    title = c.get("title") or " ".join(x for x in ((c.get("type") or "").upper(), "with " + c["counterparty"]
                                                   if c.get("counterparty") else "") if x) or "Contract"
    h = doc.add_heading("Contract review: " + title, 0)
    for r in h.runs:
        r.font.color.rgb = NAVY
    meta = [c.get("counterparty"), (c.get("type") or "").upper(), "we are " + c["our_role"] if c.get("our_role") else "",
            "reviewed " + dt.date.today().isoformat(), ("by " + a.reviewer) if a.reviewer else ""]
    doc.add_paragraph(" · ".join(x for x in meta if x))

    overall = (v.get("overall") or "").lower()
    t = doc.add_table(rows=1, cols=1)
    cell = t.cell(0, 0)
    fill = {"sign": "D1E7DD", "sign-with-changes": "D1E7DD", "negotiate": "FFF3CD",
            "escalate": "F8D7DA", "do-not-sign": "F8D7DA"}.get(overall, "E9ECEF")
    shade(cell, fill)
    p = cell.paragraphs[0]
    r = p.add_run(VERDICT_TEXT.get(overall, overall.upper() or "VERDICT MISSING"))
    r.bold, r.font.size = True, Pt(14)
    summary = v.get("summary") or ""
    if summary:
        add_inline(cell.add_paragraph(), summary)
    counts = {k: sum((i.get("risk") or "").lower() == k for i in issues) for k in ("high", "medium", "low")}
    cell.add_paragraph("{} issues: {} high, {} medium, {} low.".format(len(issues), counts["high"], counts["medium"],
                                                                     counts["low"]))
    lawyer = [i["id"] for i in issues if (i.get("lawyer") or "").lower() in ("yes", "true")]
    if lawyer:
        cell.add_paragraph("Lawyer review recommended for: " + ", ".join(lawyer) + ".")
    doc.add_paragraph()

    for name in ("Key terms", "Key dates"):
        if rv["sections"].get(name):
            doc.add_heading(name, 1)
            render_md(doc, rv["sections"][name])

    if issues:
        doc.add_heading("Issues", 1)
        tbl = doc.add_table(rows=1, cols=6)
        tbl.style = "Table Grid"
        for k, head in enumerate(("ID", "Clause", "Risk", "Issue", "Our position", "Priority")):
            tbl.rows[0].cells[k].text = head
            tbl.rows[0].cells[k].paragraphs[0].runs[0].bold = True
        order = {"high": 0, "medium": 1, "low": 2}
        for iss in sorted(issues, key=lambda i: order.get((i.get("risk") or "").lower(), 3)):
            row = tbl.add_row().cells
            risk = (iss.get("risk") or "").lower()
            action = (iss.get("action") or "").lower()
            pos = {"replace": "Amend", "delete": "Delete", "insert-after": "Add clause",
                   "comment": "Raise in comment"}.get(action, action)
            vals = (iss["id"], iss.get("clause", ""), risk, iss.get("title", ""),
                    pos + (": " + iss.get("position", "") if iss.get("position") else ""),
                    iss.get("priority", ""))
            for k, val in enumerate(vals):
                row[k].text = val
            if risk in RISK_FILL:
                shade(row[2], RISK_FILL[risk])
        doc.add_paragraph()
        doc.add_heading("Issue details", 1)
        for iss in issues:
            doc.add_heading("{}: {}".format(iss["id"], iss.get("title", "")), 2)
            label_value(doc, "Clause", iss.get("clause"))
            label_value(doc, "Risk", "{}{}".format(iss.get("risk", ""), (", " + iss["priority"]) if iss.get("priority") else ""))
            label_value(doc, "Contract says", iss.get("find"))
            if (iss.get("action") or "").lower() == "delete":
                label_value(doc, "We propose", "delete this text")
            else:
                label_value(doc, "We propose", iss.get("replace"))
            label_value(doc, "Comment to counterparty", iss.get("comment"))
            label_value(doc, "Internal", iss.get("internal"))

    for name, body in rv["sections"].items():
        if name in ("Key terms", "Key dates") or not body:
            continue
        doc.add_heading(name, 1)
        render_md(doc, body)

    foot = doc.add_paragraph()
    r = foot.add_run("First-pass review to support your decision. It is not legal advice; have a qualified lawyer "
                     "review high-risk, regulated or jurisdiction-specific points before signing.")
    r.italic, r.font.size = True, Pt(8.5)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    doc.save(a.out)
    print("Saved {} ({} issues, verdict: {})".format(a.out, len(issues), overall or "missing"))


if __name__ == "__main__":
    main()
