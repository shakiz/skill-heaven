#!/usr/bin/env python3
"""Create the user's contract playbook in their own folder (never inside the skill).

  init_playbook.py ./contract-playbook

Copies the starter playbook (standard positions for customers and vendors) for the user to adapt.
Never overwrites existing files.
"""
import shutil
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(__doc__)
src = Path(__file__).resolve().parent.parent / "assets" / "playbook-starter"
dst = Path(sys.argv[1]).resolve()
created = 0
for f in sorted(src.rglob("*")):
    if f.is_dir():
        continue
    target = dst / f.relative_to(src)
    if target.exists():
        continue
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, target)
    created += 1
print("Playbook ready at {} ({} files added). Edit the positions to match your company before relying on them."
      .format(dst, created))
