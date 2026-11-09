"""Shared helpers for the contract review scripts. Python 3.9+.

- Text normalisation and tolerant matching (curly quotes, dashes, non-breaking spaces, spacing).
- A paragraph model over a .docx that understands runs split by Word, existing tracked changes,
  fields and auto-numbering, so text can be located and redlined exactly.
- Loading contracts in any format as a list of paragraphs (.docx, .pdf, .txt, .md).
- Parsers for review.md (the working file) and the playbook.
"""
import copy
import datetime as _dt
import re
from pathlib import Path

# --------------------------------------------------------------------------- normalisation

_CHARMAP = {
    "“": '"', "”": '"', "„": '"', "‟": '"', "«": '"', "»": '"',
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "–": "-", "—": "-", "‑": "-", "‐": "-", "−": "-",
    " ": " ", " ": " ", " ": " ", "\t": " ", "\n": " ", "\r": " ",
    "\u2026": "...",
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl", "\ufb05": "st", "\ufb06": "st",
}
LIGATURES = {k: v for k, v in _CHARMAP.items() if "\ufb00" <= k <= "\ufb06"}


def fix_ligatures(s):
    return "".join(LIGATURES.get(c, c) for c in s)
_DROP = set("​‌‍﻿­")


def normalize_with_map(s):
    """Return (normalised, index_map). index_map[i] is the index in s of normalised char i."""
    out, idx = [], []
    for i, ch in enumerate(s):
        if ch in _DROP:
            continue
        c = _CHARMAP.get(ch, ch)
        for cc in c:
            if cc.isspace():
                if out and out[-1] == " ":
                    continue
                cc = " "
            out.append(cc)
            idx.append(i)
    return "".join(out), idx


def normalize(s):
    return normalize_with_map(s or "")[0].strip()


def find_all(haystack, needle):
    """Find needle in haystack, tolerant of quote/dash/space differences.

    Returns (list of (start, end) spans in the ORIGINAL haystack, mode) where mode is
    'exact', 'normalised' or 'case-insensitive'."""
    if not needle or not needle.strip():
        return [], None
    spans, i = [], haystack.find(needle)
    while i >= 0:
        spans.append((i, i + len(needle)))
        i = haystack.find(needle, i + len(needle))
    if spans:
        return spans, "exact"
    hn, hmap = normalize_with_map(haystack)
    nn = normalize(needle)
    if not nn:
        return [], None
    for mode, h, n in (("normalised", hn, nn), ("case-insensitive", hn.lower(), nn.lower())):
        if len(h) != len(hn):
            continue
        res, j = [], h.find(n)
        while j >= 0:
            res.append((hmap[j], hmap[j + len(n) - 1] + 1))
            j = h.find(n, j + len(n))
        if res:
            return res, mode
    return [], None


# --------------------------------------------------------------------------- docx model

def _qn(tag):
    from docx.oxml.ns import qn
    return qn(tag)


def _local(el):
    t = el.tag
    return t.rsplit("}", 1)[-1] if isinstance(t, str) else ""


class Atom:
    """One piece of visible content: a run holding exactly one content child (after explode)."""
    __slots__ = ("run", "child", "kind", "text", "start", "locked")

    def __init__(self, run, child, kind, text, locked):
        self.run, self.child, self.kind, self.text, self.locked = run, child, kind, text, locked
        self.start = 0

    @property
    def end(self):
        return self.start + len(self.text)


class Para:
    """A paragraph of a .docx, seen in its ORIGINAL view for this session:
    text deleted by earlier reviewers is hidden, text inserted by earlier reviewers is shown,
    and edits made by this script (revision ids in the set `ours`) are ignored, so positions never shift."""

    def __init__(self, p, ours):
        self.p = p
        self.ours = ours
        self.rebuild()

    def _container_state(self, run):
        """('skip'|'locked'|'ok') for a run, from its ancestors up to the paragraph."""
        el = run.getparent()
        while el is not None and el is not self.p:
            name = _local(el)
            if name == "p":  # run belongs to a nested paragraph (text box)
                return "skip"
            if name in ("Fallback",):
                return "skip"
            if name in ("del", "moveFrom"):
                return "locked" if self._is_ours(el) else "skip"
            if name in ("ins", "moveTo") and self._is_ours(el):
                return "skip"
            el = el.getparent()
        return "ok"

    def _is_ours(self, el):
        return el.get(_qn("w:id")) in self.ours

    def rebuild(self):
        atoms = []
        for run in self.p.iter(_qn("w:r")):
            state = self._container_state(run)
            if state == "skip":
                continue
            locked = state == "locked"
            for child in run:
                name = _local(child)
                if name == "rPr":
                    continue
                if name in ("t", "delText"):
                    if name == "delText" and not locked:
                        continue
                    atoms.append(Atom(run, child, "text", child.text or "", locked))
                elif name == "tab":
                    atoms.append(Atom(run, child, "char", "\t", locked))
                elif name in ("br", "cr"):
                    atoms.append(Atom(run, child, "char", "\n", locked))
                elif name == "noBreakHyphen":
                    atoms.append(Atom(run, child, "char", "‑", locked))
                elif name == "softHyphen":
                    atoms.append(Atom(run, child, "char", "­", locked))
                elif name in ("sym", "drawing", "pict", "object"):
                    atoms.append(Atom(run, child, "object", "￼", locked))
                elif name in ("fldChar", "instrText", "delInstrText"):
                    atoms.append(Atom(run, child, "field", "", locked))
                else:
                    atoms.append(Atom(run, child, "other", "", locked))
        pos = 0
        for a in atoms:
            a.start = pos
            pos += len(a.text)
        self.atoms = atoms
        self.text = "".join(a.text for a in atoms)

    # ---- structural edits

    def explode(self):
        """Give every content child its own run (copying formatting) so any range can be isolated."""
        for run in list({id(a.run): a.run for a in self.atoms}.values()):
            kids = [c for c in run if _local(c) != "rPr"]
            if len(kids) <= 1:
                continue
            rpr = run.find(_qn("w:rPr"))
            parent = run.getparent()
            pos = parent.index(run)
            parent.remove(run)
            for i, k in enumerate(kids):
                nr = copy.deepcopy(run)
                for c in list(nr):
                    nr.remove(c)
                if rpr is not None:
                    nr.append(copy.deepcopy(rpr))
                nr.append(k)
                parent.insert(pos + i, nr)
        self.rebuild()

    def split_at(self, pos):
        """Make pos fall on a run boundary."""
        for a in self.atoms:
            if a.start < pos < a.end and a.kind == "text":
                k = pos - a.start
                r2 = copy.deepcopy(a.run)
                t2 = [c for c in r2 if _local(c) in ("t", "delText")][0]
                a.child.text, t2.text = a.text[:k], a.text[k:]
                for t in (a.child, t2):
                    t.set(_qn("xml:space"), "preserve")
                a.run.addnext(r2)
                self.rebuild()
                return

    def covered(self, a, b):
        """Atoms fully inside [a, b). Zero-length atoms are included only strictly inside."""
        out = []
        for at in self.atoms:
            if at.text:
                if at.start >= a and at.end <= b:
                    out.append(at)
            elif a < at.start < b:
                out.append(at)
        return out


def iter_paragraphs(doc):
    """Body paragraphs in document order, including table cells and text boxes (not headers)."""
    body = doc.element.body
    for p in body.iter(_qn("w:p")):
        el, skip = p.getparent(), False
        while el is not None:
            if _local(el) == "Fallback":
                skip = True
                break
            el = el.getparent()
        if not skip:
            yield p


def para_style_id(p):
    ps = p.find(_qn("w:pPr") + "/" + _qn("w:pStyle"))
    return ps.get(_qn("w:val")) if ps is not None else ""


# --------------------------------------------------------------------------- numbering

def _fmt_num(n, fmt):
    if fmt in ("decimal", "decimalZero", ""):
        return ("%02d" % n) if fmt == "decimalZero" else str(n)
    if fmt in ("lowerLetter", "upperLetter"):
        s, m = "", n
        while m > 0:
            m, r = divmod(m - 1, 26)
            s = chr(97 + r) + s
        return s if fmt == "lowerLetter" else s.upper()
    if fmt in ("lowerRoman", "upperRoman"):
        vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
                (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
        s, m = "", n
        for v, sym in vals:
            while m >= v:
                s, m = s + sym, m - v
        return s if fmt == "lowerRoman" else s.upper()
    if fmt == "none":
        return ""
    return None  # bullet and unknown formats


class Numbering:
    """Approximate Word auto-numbering, so extracted text shows clause numbers like '9.2'."""

    def __init__(self, doc):
        self.ok = False
        try:
            numbering = doc.part.numbering_part.element
        except Exception:
            return
        W = _qn
        self.abstract = {}
        for an in numbering.findall(W("w:abstractNum")):
            levels = {}
            for lvl in an.findall(W("w:lvl")):
                il = int(lvl.get(W("w:ilvl"), "0"))
                fmt = lvl.find(W("w:numFmt"))
                txt = lvl.find(W("w:lvlText"))
                st = lvl.find(W("w:start"))
                levels[il] = (
                    fmt.get(W("w:val")) if fmt is not None else "decimal",
                    txt.get(W("w:val")) if txt is not None else "",
                    int(st.get(W("w:val"))) if st is not None else 1,
                    lvl.find(W("w:isLgl")) is not None,
                )
            self.abstract[an.get(W("w:abstractNumId"))] = levels
        self.num = {}
        for n in numbering.findall(W("w:num")):
            a = n.find(W("w:abstractNumId"))
            if a is not None:
                self.num[n.get(W("w:numId"))] = a.get(W("w:val"))
        self.styles = {}
        try:
            for st in doc.styles.element.findall(W("w:style")):
                sid = st.get(W("w:styleId"))
                np_ = st.find(W("w:pPr") + "/" + W("w:numPr"))
                based = st.find(W("w:basedOn"))
                self.styles[sid] = (np_, based.get(W("w:val")) if based is not None else None)
        except Exception:
            pass
        self.counters = {}
        self.ok = True

    def _numpr(self, p):
        W = _qn
        np_ = p.find(W("w:pPr") + "/" + W("w:numPr"))
        sid, seen = para_style_id(p), set()
        while np_ is None and sid and sid not in seen:
            seen.add(sid)
            np_, sid = self.styles.get(sid, (None, None))
        if np_ is None:
            return None, None
        nid = np_.find(W("w:numId"))
        il = np_.find(W("w:ilvl"))
        return (nid.get(W("w:val")) if nid is not None else None,
                int(il.get(W("w:val"))) if il is not None else 0)

    def label(self, p):
        """Return the number label for p ('9.2', '(a)') or '' when not numbered."""
        if not self.ok:
            return ""
        nid, il = self._numpr(p)
        if not nid or nid == "0" or nid not in self.num:
            return ""
        aid = self.num[nid]
        levels = self.abstract.get(aid, {})
        if il not in levels:
            return ""
        c = self.counters.setdefault(aid, {})
        c[il] = c.get(il, levels[il][2] - 1) + 1
        for deeper in [k for k in c if k > il]:
            del c[deeper]
        fmt, text, _, _ = levels[il]
        if _fmt_num(1, fmt) is None:
            return ""

        def sub(m):
            k = int(m.group(1)) - 1
            if k not in levels:
                return ""
            f = "decimal" if levels[il][3] else levels[k][0]
            val = c.get(k, levels[k][2])
            return _fmt_num(val, f) or ""
        return re.sub(r"%(\d)", sub, text).strip()


def has_auto_number(doc_numbering, p):
    if not doc_numbering.ok:
        return False
    nid, _ = doc_numbering._numpr(p)
    return bool(nid) and nid != "0"


# --------------------------------------------------------------------------- loading contracts

CLAUSE_START_RE = re.compile(
    r"^\s*(?:(?:section|clause|article|schedule|annex|exhibit)\s+)?"
    r"(?:\(?[0-9]{1,3}(?:\.[0-9]{1,3})*[.)]?|\([a-z]{1,4}\)|[A-Z]\.)\s+\S", re.IGNORECASE)
SIGNATURE_START_RE = re.compile(r"^(signed|signature|for and on behalf|by:|name:|title:|date:)", re.IGNORECASE)
PAGE_RE = re.compile(r"^\s*(page\s+\d+(\s+of\s+\d+)?|\d+\s*/\s*\d+|-\s*\d+\s*-)\s*$", re.IGNORECASE)


def text_to_paragraphs(text):
    """Rebuild paragraphs from text whose lines were wrapped (PDF extraction, emails)."""
    paras, cur = [], []
    lines = text.replace("\r\n", "\n").split("\n")
    widths = sorted(len(l.strip()) for l in lines if l.strip())
    full = widths[int(len(widths) * 0.8)] if widths else 80

    def flush():
        if cur:
            joined = ""
            for s in cur:
                s = s.strip()
                if joined.endswith("-") and s[:1].islower() and not joined.endswith(" -"):
                    joined += s  # word hyphenated across a line break
                else:
                    joined = (joined + " " + s) if joined else s
            paras.append(joined)
            cur.clear()
    for line in lines:
        s = line.strip()
        if s.startswith("--- page ") or PAGE_RE.match(s):
            continue
        if not s:
            flush()
            continue
        if cur:
            prev = cur[-1].strip()
            new_clause = bool(CLAUSE_START_RE.match(s) or SIGNATURE_START_RE.match(s))
            prev_short = len(prev) < 0.7 * full and prev[-1:] in ".:;!?"
            heading = prev.isupper() and len(prev) < 80
            if new_clause or prev_short or heading:
                flush()
        cur.append(s)
    flush()
    return [p for p in paras if p]


def pdf_text(path):
    from pypdf import PdfReader
    r = PdfReader(str(path))
    if r.is_encrypted:
        try:
            r.decrypt("")
        except Exception:
            raise SystemExit("{} is password-protected. Ask the user for an unlocked copy.".format(path))
    return "\n\n".join("--- page {} ---\n{}".format(i, fix_ligatures(pg.extract_text() or ""))
                       for i, pg in enumerate(r.pages, 1))


def contract_paragraphs(path):
    """List of paragraph strings as the scripts see them (original view for .docx)."""
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".docx":
        from docx import Document
        doc = Document(str(p))
        return [Para(el, set()).text for el in iter_paragraphs(doc)]
    if ext == ".pdf":
        return text_to_paragraphs(pdf_text(p))
    if ext in (".txt", ".md", ".text", ""):
        return text_to_paragraphs(p.read_text(encoding="utf-8", errors="replace"))
    raise SystemExit("Unsupported format {}: save the contract as .docx (preferred), .pdf or .txt.".format(ext))


def locate(paragraphs, needle, occurrence=None):
    """Find needle in a list of paragraph strings.

    Returns dict(status=found|not-found|ambiguous|spans-paragraphs, hits=[(para_index, start, end)], mode, hint)."""
    hits, mode = [], None
    for i, t in enumerate(paragraphs):
        spans, m = find_all(t, needle)
        if spans:
            mode = mode or m
            hits.extend((i, a, b) for a, b in spans)
    if hits:
        if occurrence:
            if 1 <= occurrence <= len(hits):
                return {"status": "found", "hits": [hits[occurrence - 1]], "mode": mode, "hint": ""}
            return {"status": "not-found", "hits": [], "mode": None,
                    "hint": "occurrence {} requested but the text appears {} time(s)".format(occurrence, len(hits))}
        if len(hits) > 1:
            where = ", ".join("paragraph {}".format(h[0] + 1) for h in hits[:5])
            return {"status": "ambiguous", "hits": hits, "mode": mode,
                    "hint": "found {} times ({}); add surrounding words or set 'occurrence: N'".format(len(hits), where)}
        return {"status": "found", "hits": hits, "mode": mode, "hint": ""}
    # diagnostics
    n = normalize(needle)
    joined = " ".join(normalize(t) for t in paragraphs)
    if n and (n in joined or n.lower() in joined.lower()):
        return {"status": "spans-paragraphs", "hits": [], "mode": None,
                "hint": "the text runs across paragraphs; split it into one issue per paragraph"}
    hint = ""
    if re.match(r"^\s*(?:\d+(?:\.\d+)*[.)]?|\([a-z]+\))\s", needle):
        hint = "remove the clause number from 'find'; Word auto-numbering is not part of the text. "
    best = _closest(paragraphs, needle)
    if best:
        hint += "closest paragraph {}: \"{}\"".format(best[0] + 1, best[1][:160])
    return {"status": "not-found", "hits": [], "mode": None, "hint": hint.strip()}


def _closest(paragraphs, needle):
    import difflib
    n = normalize(needle).lower()
    words = set(n.split())
    best, score = None, 0.0
    for i, t in enumerate(paragraphs):
        tl = normalize(t).lower()
        if not tl:
            continue
        overlap = len(words & set(tl.split())) / (len(words) or 1)
        if overlap < 0.3:
            continue
        r = difflib.SequenceMatcher(None, n, tl[: len(n) * 2]).ratio() + overlap
        if r > score:
            best, score = (i, t), r
    return best


# --------------------------------------------------------------------------- review.md

META_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_ -]*?)\s*:\s*(.*)$")
VALID_RISK = ("high", "medium", "low")
VALID_ACTIONS = ("replace", "delete", "insert-after", "comment")


def parse_review(path):
    """Parse review.md into {'contract': {}, 'verdict': {}, 'sections': {name: text}, 'issues': [..]}."""
    text = Path(path).read_text(encoding="utf-8")
    blocks, cur = [], None
    for line in text.splitlines():
        if line.startswith("# "):
            cur = {"head": line[2:].strip(), "lines": []}
            blocks.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    out = {"contract": {}, "verdict": {}, "sections": {}, "issues": []}
    for b in blocks:
        head = b["head"]
        hl = head.lower()
        if hl == "contract" or hl == "verdict":
            meta, _ = _meta_and_subs(b["lines"])
            out[hl] = meta
            if hl == "verdict":
                out["verdict"]["_body"] = "\n".join(b["lines"]).strip()
        elif hl.startswith("issue"):
            m = re.match(r"issue\s+([A-Za-z0-9_.-]+)\s*[:\-–]?\s*(.*)$", head, re.IGNORECASE)
            meta, subs = _meta_and_subs(b["lines"])
            iss = {"id": m.group(1) if m else head, "title": (m.group(2) if m else "").strip()}
            iss.update({k.lower().replace(" ", "_"): v for k, v in meta.items()})
            for k, v in subs.items():
                iss[k] = v
            out["issues"].append(iss)
        else:
            out["sections"][head] = "\n".join(b["lines"]).strip()
    return out


def _meta_and_subs(lines):
    meta, subs, sub, in_meta = {}, {}, None, True
    for line in lines:
        if line.startswith("### "):
            sub = line[4:].strip().lower()
            subs[sub] = []
            in_meta = False
            continue
        if sub is not None:
            subs[sub].append(line)
            continue
        if in_meta:
            m = META_RE.match(line.strip())
            if m and line.strip():
                meta[m.group(1).strip().lower().replace(" ", "_")] = m.group(2).strip()
                continue
            if not line.strip() and meta:
                in_meta = False
    return meta, {k: "\n".join(v).strip() for k, v in subs.items()}


# --------------------------------------------------------------------------- playbook

ENTRY_RE = re.compile(r"^##\s+([A-Za-z0-9][A-Za-z0-9_.-]*)\s*:\s*(.+?)\s*$")
LABEL_RE = re.compile(r"^\*\*([A-Za-z][A-Za-z ()/'-]*?):?\*\*:?\s*(.*)$")
INTERNAL_LABELS = ("fallback", "walk", "internal")


def internal_texts(entry):
    """(label, text) pairs of a playbook entry that must never reach the counterparty."""
    return [(k, v) for k, v in entry["labels"].items() if v and k.startswith(INTERNAL_LABELS)]


def parse_playbook(folder):
    """Return {id: entry}; entry has meta (dict), labels (dict label->text) and body."""
    entries = {}
    root = Path(folder)
    if not root.exists():
        return entries
    files = [root] if root.is_file() else sorted(root.rglob("*.md"))
    for path in files:
        if path.name.lower() == "readme.md":
            continue
        current, in_meta, label = None, False, None
        for line in path.read_text(encoding="utf-8").splitlines():
            m = ENTRY_RE.match(line)
            if m:
                current = {"id": m.group(1), "title": m.group(2), "file": path.name,
                           "meta": {}, "labels": {}, "body": []}
                entries[current["id"]] = current
                in_meta, label = True, None
                continue
            if current is None:
                continue
            if line.startswith("# ") or line.startswith("## "):
                current = None
                continue
            if in_meta:
                mm = META_RE.match(line.strip())
                if mm and line.strip() and not line.strip().startswith("**"):
                    current["meta"][mm.group(1).strip().lower()] = mm.group(2).strip()
                    continue
                if not line.strip():
                    continue
                in_meta = False
            current["body"].append(line)
            lm = LABEL_RE.match(line.strip())
            if lm:
                label = lm.group(1).strip().lower()
                current["labels"][label] = lm.group(2).strip()
            elif label and line.strip():
                current["labels"][label] = (current["labels"][label] + " " + line.strip().lstrip("> ")).strip()
    for e in entries.values():
        e["body"] = "\n".join(e["body"]).strip()
    return entries


def applies(entry, contract_type, role):
    at = [x.strip().lower() for x in entry["meta"].get("applies_to", "all").split(",")]
    r = entry["meta"].get("role", "any").strip().lower()
    type_ok = "all" in at or (contract_type or "").lower() in at
    ours = (role or "").lower()
    role_ok = r in ("any", "both", "") or r == ours or (ours == "mutual" and r in ("discloser", "recipient"))
    return type_ok and role_ok


def utc_now():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug_initials(name):
    parts = re.findall(r"[A-Za-z0-9]+", name or "")
    return "".join(p[0] for p in parts[:3]).upper() or "R"


# --------------------------------------------------------------------------- what else a .docx carries
# Files sent to a counterparty carry more than the visible text: earlier comments (often internal notes from
# colleagues), document properties (author, comments, keywords) and hidden text. These helpers find and remove them.

META_FIELDS = ("author", "last_modified_by", "title", "subject", "comments", "keywords", "category", "content_status")


def existing_comments(doc):
    out = []
    for part in doc.part.package.iter_parts():
        if str(part.partname).endswith("/comments.xml") and hasattr(part, "element"):
            for c in part.element.findall(_qn("w:comment")):
                out.append({"id": c.get(_qn("w:id")), "author": c.get(_qn("w:author")) or "",
                            "text": " ".join("".join(t.text or "" for t in p.iter(_qn("w:t")))
                                             for p in c.iter(_qn("w:p"))).strip()})
    return out


def doc_metadata(doc):
    cp = doc.core_properties
    return {f: getattr(cp, f) for f in META_FIELDS if getattr(cp, f, None)}


def hidden_text(doc):
    """Text in runs formatted as hidden (w:vanish): invisible on screen, but sent with the file."""
    out = []
    for r in doc.element.body.iter(_qn("w:r")):
        rpr = r.find(_qn("w:rPr"))
        if rpr is not None and rpr.find(_qn("w:vanish")) is not None:
            v = rpr.find(_qn("w:vanish")).get(_qn("w:val"))
            if v in (None, "1", "true", "on"):
                t = "".join(x.text or "" for x in r.iter(_qn("w:t")))
                if t.strip():
                    out.append(t)
    return out


def _attr_endswith(el, name):
    return [v for k, v in el.attrib.items() if k.endswith("}" + name)]


def remove_comments(doc, ids):
    """Remove comments (by id) everywhere: anchors in the body, comments.xml and Word's companion parts."""
    from lxml import etree
    ids = {str(i) for i in ids}
    if not ids:
        return 0
    body = doc.element.body
    for el in list(body.iter(_qn("w:commentRangeStart"), _qn("w:commentRangeEnd"), _qn("w:commentReference"))):
        if el.get(_qn("w:id")) in ids:
            parent = el.getparent()
            if el.tag == _qn("w:commentReference") and parent.tag == _qn("w:r") and \
                    all(c.tag in (_qn("w:rPr"), _qn("w:commentReference")) for c in parent):
                parent.getparent().remove(parent)
            else:
                parent.remove(el)
    para_ids, removed_authors, n = set(), set(), 0
    parts = list(doc.part.package.iter_parts())
    for part in parts:
        if str(part.partname).endswith("/comments.xml") and hasattr(part, "element"):
            for c in list(part.element.findall(_qn("w:comment"))):
                if c.get(_qn("w:id")) in ids:
                    for p in c.iter(_qn("w:p")):
                        para_ids.update(_attr_endswith(p, "paraId"))
                    removed_authors.add(c.get(_qn("w:author")) or "")
                    part.element.remove(c)
                    n += 1
    remaining = {c["author"] for c in existing_comments(doc)}
    durable = set()
    for suffix in ("commentsIds.xml", "commentsExtended.xml", "commentsExtensible.xml", "people.xml"):
        for part in parts:
            if not str(part.partname).endswith("/" + suffix):
                continue
            is_xml = hasattr(part, "element")
            root = part.element if is_xml else etree.fromstring(part.blob)
            for child in list(root):
                pid = set(_attr_endswith(child, "paraId"))
                did = set(_attr_endswith(child, "durableId"))
                auth = set(_attr_endswith(child, "author"))
                if suffix == "commentsIds.xml" and pid & para_ids:
                    durable |= did
                drop = (pid & para_ids) or (did & durable) or \
                       (suffix == "people.xml" and auth & (removed_authors - remaining))
                if drop:
                    root.remove(child)
            if not is_xml:
                part._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    return n


def clean_metadata(doc, author):
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    for f in ("comments", "keywords", "subject", "category", "content_status"):
        setattr(cp, f, "")


def remove_hidden_text(doc):
    n = 0
    for r in list(doc.element.body.iter(_qn("w:r"))):
        rpr = r.find(_qn("w:rPr"))
        if rpr is not None and rpr.find(_qn("w:vanish")) is not None and \
                rpr.find(_qn("w:vanish")).get(_qn("w:val")) in (None, "1", "true", "on"):
            r.getparent().remove(r)
            n += 1
    return n
