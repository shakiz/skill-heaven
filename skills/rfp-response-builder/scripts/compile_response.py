#!/usr/bin/env python3
"""Convert response.md (the authoring format) to response.json, e.g. for archiving or other tools.

  compile_response.py response.md -o response.json

All other scripts read response.md directly, so this step is optional.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_response  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("response")
ap.add_argument("-o", "--out", required=True)
a = ap.parse_args()
data = load_response(a.response)
Path(a.out).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Wrote {} ({} requirements, {} sections)".format(a.out, len(data["requirements"]), len(data["sections"])))
