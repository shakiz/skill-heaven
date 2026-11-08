#!/usr/bin/env python3
"""Extract readable text from RFPs and past proposals: .docx, .xlsx, .pdf, .md, .txt, .csv.

  extract_text.py FILE [FILE ...] [-o OUT_DIR]

Prints the text (or writes OUT_DIR/<name>.txt per file). Word tables become pipe tables, spreadsheet
rows become "Sheet | Row n | cell | cell". PDF needs pypdf; if it is missing, read the PDF directly instead.
"""
import argparse
import sys
from pathlib import Path


def docx_text(p):
    from docx import Document
    from docx.oxml.ns import qn
    d = Document(p)
    out = []
    body = d.element.body
    for child in body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            t = "".join(n.text or "" for n in child.iter() if n.tag.endswith("}t"))
            style = child.find(".//{*}pStyle")
            sv = style.get(qn("w:val"), "") if style is not None else ""
            if t.strip():
                lvl = sv.replace("Heading", "").strip() if sv.startswith("Heading") else ""
                out.append(("#" * int(lvl) + " " if lvl.isdigit() else "") + t)
        elif tag == "tbl":
            for row in child.iter(qn("w:tr")):
                cells = []
                for c in row.iter(qn("w:tc")):
                    cells.append(" ".join("".join(n.text or "" for n in p.iter() if n.tag.endswith("}t"))
                                          for p in c.iter(qn("w:p"))).strip())
                out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def xlsx_text(p):
    from openpyxl import load_workbook
    wb = load_workbook(p, data_only=True)
    out = []
    for ws in wb:
        for i, row in enumerate(ws.iter_rows(values_only=True), 1):
            vals = ["" if v is None else str(v) for v in row]
            if any(v.strip() for v in vals):
                out.append("{} | Row {} | {}".format(ws.title, i, " | ".join(vals)))
    return "\n".join(out)


def pdf_text(p):
    try:
        from pypdf import PdfReader
    except ImportError:
        return "[pypdf not installed - read this PDF directly instead]"
    r = PdfReader(str(p))
    return "\n\n".join("--- page {} ---\n{}".format(i, pg.extract_text() or "") for i, pg in enumerate(r.pages, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out-dir")
    a = ap.parse_args()
    for f in a.files:
        p = Path(f)
        ext = p.suffix.lower()
        try:
            if ext == ".docx":
                t = docx_text(p)
            elif ext in (".xlsx", ".xlsm"):
                t = xlsx_text(p)
            elif ext == ".pdf":
                t = pdf_text(p)
            else:
                t = p.read_text(encoding="utf-8", errors="replace")
        except ImportError as e:
            t = "[missing library: {} - python3 -m pip install -r requirements.txt]".format(e.name)
        if a.out_dir:
            Path(a.out_dir).mkdir(parents=True, exist_ok=True)
            out = Path(a.out_dir) / (p.stem + ".txt")
            out.write_text(t, encoding="utf-8")
            print("{} -> {} ({} chars)".format(p, out, len(t)))
        else:
            print("===== {}\n{}".format(p, t))


if __name__ == "__main__":
    main()
