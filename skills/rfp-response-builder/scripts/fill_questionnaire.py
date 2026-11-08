#!/usr/bin/env python3
"""Write answers from response.md into the client's own questionnaire spreadsheet.

  fill_questionnaire.py client.xlsx response.md -o filled.xlsx \
      --sheet "Questions" --id-col A --answer-col D [--compliance-col C] [--first-row 2]

Rows are matched by requirement id (the value in --id-col). Ids of the form R<n> match row n
when the sheet has no id column. Formatting and other cells of the client's file are preserved.
Rows with gaps or placeholders get a yellow fill in the answer cell.
Requires openpyxl.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PLACEHOLDER_RE, load_response  # noqa: E402

try:
    from openpyxl import load_workbook
    from openpyxl.styles import Alignment, PatternFill
    from openpyxl.utils import column_index_from_string
except ImportError:
    sys.exit("openpyxl is required: python3 -m pip install openpyxl")

YELLOW = PatternFill("solid", fgColor="FFEB9C")
COMPLIANCE_WORD = {"comply": "Yes", "partial": "Partial", "exception": "No", "n/a": "N/A"}


def plain(md):
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", md or "")
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"^\s*[-*]\s+", "• ", t, flags=re.M)
    return t.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("response")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--sheet")
    ap.add_argument("--id-col", default="A")
    ap.add_argument("--answer-col", required=True)
    ap.add_argument("--compliance-col")
    ap.add_argument("--first-row", type=int, default=2)
    a = ap.parse_args()

    data = load_response(a.response)
    by_id = {str(r.get("id", "")).strip(): r for r in data["requirements"]}
    wb = load_workbook(a.xlsx)
    ws = wb[a.sheet] if a.sheet else wb.active
    idc = column_index_from_string(a.id_col)
    ansc = column_index_from_string(a.answer_col)
    compc = column_index_from_string(a.compliance_col) if a.compliance_col else None

    filled, missing, flagged = 0, [], 0
    for row in range(a.first_row, ws.max_row + 1):
        raw = ws.cell(row=row, column=idc).value
        key = str(raw).strip() if raw is not None else ""
        r = by_id.get(key) or by_id.get("R{}".format(row))
        if r is None:
            if key:
                missing.append(key)
            continue
        ans = plain(r.get("answer", ""))
        if r.get("status") == "gap" and not ans:
            ans = "[VERIFY: {}]".format(r.get("notes") or "answer pending")
        cell = ws.cell(row=row, column=ansc)
        cell.value = ans
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if r.get("status") in ("gap", "partial") or PLACEHOLDER_RE.search(ans):
            cell.fill = YELLOW
            flagged += 1
        if compc and r.get("compliance"):
            ws.cell(row=row, column=compc).value = COMPLIANCE_WORD.get(r["compliance"], r["compliance"])
        filled += 1

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(a.out)
    print("Wrote {}: {} rows filled, {} flagged for review".format(a.out, filled, flagged))
    if missing:
        print("Rows with ids not in response.md ({}): {}".format(len(missing), ", ".join(missing[:20])))


if __name__ == "__main__":
    main()
