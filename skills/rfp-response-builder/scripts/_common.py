"""Shared helpers: library parsing and response.json loading. Python 3.9+, stdlib only."""
import datetime as _dt
import json
import re
from pathlib import Path

ENTRY_RE = re.compile(r"^##\s+([A-Za-z0-9][A-Za-z0-9_.-]*)\s*:\s*(.+?)\s*$")
META_RE = re.compile(r"^([a-z_]+)\s*:\s*(.*)$")
PLACEHOLDER_RE = re.compile(
    r"\[(?:VERIFY|TBD|TODO)[^\]]*\]|\bXXX\b|\{\{[^}]*\}\}|<insert[^>]*>", re.IGNORECASE
)
STALE_DAYS = 365


def parse_library(library_dir):
    """Return {id: entry} for every '## ID: title' entry in library_dir/**/*.md (README.md skipped)."""
    entries = {}
    root = Path(library_dir)
    if not root.exists():
        return entries
    for path in sorted(root.rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        current = None
        in_meta = False
        for line in path.read_text(encoding="utf-8").splitlines():
            m = ENTRY_RE.match(line)
            if m:
                current = {
                    "id": m.group(1),
                    "title": m.group(2),
                    "file": str(path.relative_to(root)),
                    "meta": {},
                    "body": [],
                }
                entries[current["id"]] = current
                in_meta = True
                continue
            if current is None:
                continue
            if line.startswith("## ") or line.startswith("# "):
                current = None
                continue
            if in_meta:
                mm = META_RE.match(line.strip())
                if mm and line.strip():
                    current["meta"][mm.group(1)] = mm.group(2).strip()
                    continue
                if not line.strip():
                    continue
                in_meta = False
            current["body"].append(line)
    for e in entries.values():
        e["body"] = "\n".join(e["body"]).strip()
        e["stale"], e["stale_reason"] = staleness(e["meta"])
    return entries


def _date(s):
    try:
        return _dt.date.fromisoformat(s.strip()[:10])
    except (ValueError, AttributeError):
        return None


def staleness(meta, today=None):
    today = today or _dt.date.today()
    exp = _date(meta.get("expires", ""))
    if exp and exp < today:
        return True, "expired {}".format(exp)
    rev = _date(meta.get("last_reviewed", ""))
    if rev is None:
        return True, "no last_reviewed date"
    if (today - rev).days > STALE_DAYS:
        return True, "last reviewed {}".format(rev)
    return False, ""


def load_response(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("rfp", {})
    data.setdefault("requirements", [])
    data.setdefault("sections", [])
    data.setdefault("win_themes", [])
    return data


def word_count(text):
    return len(re.findall(r"\b[\w'’-]+\b", text or ""))
