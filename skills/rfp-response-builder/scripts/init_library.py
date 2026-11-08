#!/usr/bin/env python3
"""Create a new, empty answer library in the user's own folder (never inside the skill).

  init_library.py ./rfp-library

Copies the starter structure (folders + README guides). Refuses to overwrite existing files.
"""
import shutil
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(__doc__)
src = Path(__file__).resolve().parent.parent / "assets" / "library-starter"
dst = Path(sys.argv[1]).resolve()
created = 0
for f in src.rglob("*"):
    if f.is_dir():
        continue
    target = dst / f.relative_to(src)
    if target.exists():
        continue
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, target)
    created += 1
print("Library ready at {} ({} starter files added). Next: add entries, e.g. by harvesting past proposals.".format(dst, created))
