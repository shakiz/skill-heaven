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


LIST_KEYS = {"client_goals", "assumptions", "risks", "sources"}
INT_KEYS = {"page_limit", "word_limit", "score"}


def _value(key, raw):
    raw = raw.strip()
    if key in LIST_KEYS:
        return [x.strip() for x in re.split(r"[;,]" if key == "sources" else r";", raw) if x.strip()]
    if key in INT_KEYS:
        try:
            return int(raw)
        except ValueError:
            return None
    if key == "mandatory":
        return raw.lower() in ("yes", "true", "y", "1", "mandatory")
    if key == "evaluation_criteria":
        out = []
        for part in raw.split(";"):
            if "=" in part:
                name, w = part.rsplit("=", 1)
                try:
                    w = float(w.strip().rstrip("%"))
                    w = int(w) if w.is_integer() else w
                except ValueError:
                    w = w.strip()
                out.append({"name": name.strip(), "weight": w})
            elif part.strip():
                out.append({"name": part.strip(), "weight": None})
        return out
    return raw


def parse_response_md(text):
    """Parse the response.md authoring format (see references/response-format.md) into the response dict."""
    data = {"rfp": {}, "bid": {}, "win_themes": [], "sections": [], "requirements": []}
    blocks, cur = [], None
    for line in text.splitlines():
        if line.startswith("# "):
            cur = [line[2:].strip(), []]
            blocks.append(cur)
        elif cur is not None:
            cur[1].append(line)
    for head, lines in blocks:
        kind = head.lower()
        if kind.startswith("section:"):
            data["sections"].append({"title": head.split(":", 1)[1].strip(), "body": "\n".join(lines).strip()})
            continue
        if kind == "win themes":
            data["win_themes"] = [re.sub(r"^[-*]\s+", "", l).strip() for l in lines if l.strip()]
            continue
        meta, body, i = {}, [], 0
        while i < len(lines) and not lines[i].strip():
            i += 1
        while i < len(lines):
            m = META_RE.match(lines[i].strip())
            if not lines[i].strip() or not m:
                break
            meta[m.group(1)] = _value(m.group(1), m.group(2))
            i += 1
        body = "\n".join(lines[i:]).strip()
        if kind == "rfp":
            data["rfp"].update(meta)
        elif kind == "bid":
            data["bid"].update(meta)
            if body:
                data["bid"].setdefault("rationale", body)
        elif kind.startswith("requirement"):
            req = {"id": head.split(None, 1)[1].strip() if " " in head else ""}
            req.update(meta)
            req["answer"] = body
            req.setdefault("sources", [])
            data["requirements"].append(req)
    return data


def load_response(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    data = parse_response_md(raw) if str(path).lower().endswith(".md") else json.loads(raw)
    data.setdefault("rfp", {})
    data.setdefault("requirements", [])
    data.setdefault("sections", [])
    data.setdefault("win_themes", [])
    return data


def word_count(text):
    return len(re.findall(r"\b[\w'’-]+\b", text or ""))
