#!/usr/bin/env python3
"""Build the compliance matrix .xlsx from response.json.

  build_matrix.py response.json -o compliance-matrix.xlsx

Sheets: Summary, Compliance matrix (every requirement), Gaps (what experts must supply).
Requires openpyxl.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PLACEHOLDER_RE, load_response  # noqa: E402

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl")

FILL = {
    "answered": "C6EFCE", "partial": "FFEB9C", "gap": "FFC7CE", "not-applicable": "EDEDED",
}
HEAD = PatternFill("solid", fgColor="1F3864")


def header(ws, cols, widths):
    ws.append(cols)
    for i, w in enumerate(widths, 1):
        c = ws.cell(row=1, column=i)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = HEAD
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def plain(md, n=400):
    t = re.sub(r"[*#|`]", "", md or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("response")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    data = load_response(a.response)
    rfp, reqs = data["rfp"], data["requirements"]

    wb = Workbook()
    s = wb.active
    s.title = "Summary"
    by = Counter(r.get("status") for r in reqs)
    mand = [r for r in reqs if r.get("mandatory")]
    rows = [
        ("Client", rfp.get("client", "")), ("RFP", rfp.get("title", "")), ("Reference", rfp.get("reference", "")),
        ("Deadline", rfp.get("deadline", "")), ("Bid decision", "{} ({})".format(
            data.get("bid", {}).get("decision", ""), data.get("bid", {}).get("score", ""))),
        ("", ""), ("Total requirements", len(reqs)), ("Answered", by.get("answered", 0)),
        ("Partial / to verify", by.get("partial", 0)), ("Gaps", by.get("gap", 0)),
        ("Not applicable", by.get("not-applicable", 0)), ("Mandatory", len(mand)),
        ("Mandatory not fully answered", sum(1 for r in mand if r.get("status") not in ("answered", "not-applicable"))),
    ]
    for k, v in rows:
        s.append([k, v])
        s.cell(row=s.max_row, column=1).font = Font(bold=True)
    s.column_dimensions["A"].width = 30
    s.column_dimensions["B"].width = 60

    m = wb.create_sheet("Compliance matrix")
    cols = ["ID", "Section", "Requirement", "Mandatory", "Compliance", "Status", "Response summary",
            "Sources", "Confidence", "Owner", "Notes"]
    header(m, cols, [9, 22, 50, 11, 13, 13, 60, 22, 12, 18, 35])
    for r in reqs:
        m.append([
            r.get("id", ""), r.get("section", ""), r.get("text", ""), "Yes" if r.get("mandatory") else "No",
            r.get("compliance", ""), r.get("status", ""), plain(r.get("answer", "")),
            ", ".join(r.get("sources") or []), r.get("confidence", ""), r.get("owner", ""), r.get("notes", ""),
        ])
        row = m.max_row
        color = FILL.get(r.get("status"))
        if color:
            m.cell(row=row, column=6).fill = PatternFill("solid", fgColor=color)
        for c in range(1, len(cols) + 1):
            m.cell(row=row, column=c).alignment = Alignment(vertical="top", wrap_text=True)
    m.auto_filter.ref = "A1:{}{}".format(get_column_letter(len(cols)), m.max_row)

    g = wb.create_sheet("Gaps")
    header(g, ["ID", "Mandatory", "Requirement", "What is needed", "Owner", "Status"], [9, 11, 50, 55, 20, 12])
    ngap = 0
    for r in reqs:
        ph = PLACEHOLDER_RE.findall(r.get("answer", "") or "")
        if r.get("status") in ("gap", "partial") or ph:
            need = r.get("notes") or "; ".join(ph) or "Confirm content"
            g.append([r.get("id", ""), "Yes" if r.get("mandatory") else "No", r.get("text", ""), need,
                      r.get("owner", ""), r.get("status", "")])
            for c in range(1, 7):
                g.cell(row=g.max_row, column=c).alignment = Alignment(vertical="top", wrap_text=True)
            ngap += 1

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(a.out)
    print("Wrote {} ({} requirements, {} gap/verify rows)".format(a.out, len(reqs), ngap))


if __name__ == "__main__":
    main()
