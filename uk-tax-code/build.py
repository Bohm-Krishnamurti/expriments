#!/usr/bin/env python3
"""Download UK tax legislation from legislation.gov.uk and convert it to searchable text.

Usage:
    python3 build.py                # fetch (cached) + convert everything in manifest.tsv
    python3 build.py ITA2007 CTA2009  # only these abbreviations
    python3 build.py --refresh      # re-download even if cached

Raw XML goes to .cache/ (git-ignored); plain text goes to corpus/<ABBR>.txt and
per-act size statistics go to stats.tsv.

Each provision in corpus/*.txt starts with a header line, so the files work with
plain grep as well as with taxsearch.py:

    § ITA2007 s.6 — The basic rate, higher rate and additional rate
    @ https://www.legislation.gov.uk/ukpga/2007/3/section/6 | Part 2 ... > Chapter 2 ...
    (1) The main rates at which income tax is charged are—
        (b) the basic rate, ...
"""

import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
CORPUS = os.path.join(HERE, "corpus")
BASE = "https://www.legislation.gov.uk/"

NS = "{http://www.legislation.gov.uk/namespaces/legislation}"
UKM = "{http://www.legislation.gov.uk/namespaces/metadata}"
DC = "{http://purl.org/dc/elements/1.1/}"
DCT = "{http://purl.org/dc/terms/}"

# Containers that group provisions; their Number/Title become headings/breadcrumbs.
STRUCT = {"Body", "Schedules", "Part", "Chapter", "Pblock", "PsubBlock", "Schedule",
          "ScheduleBody", "EUPart", "EUTitle", "EUChapter", "EUSection", "EUSubsection",
          "Group", "Division"}
# Inline elements whose content is editorial noise.
SKIP_INLINE = {"CommentaryRef", "FootnoteRef", "MarginNoteRef", "Footnote"}
# Children that never carry legislative text.
SKIP_BLOCK = {"CommentaryRef", "FootnoteRef", "MarginNoteRef", "Footnote", "Reference",
              "SignedSection", "ExplanatoryNotes", "EarlierOrders", "Contents"}
# Inline children that should be separated by a space when flattened.
BLOCKISH = {"Text", "Para", "P", "td", "th", "ListItem", "P1", "P2", "P3", "P4", "P5", "P6",
            "Title", "Number", "mtd", "mtr"}
CHARS = {"emdash": "—", "endash": "–", "minus": "−", "LinePara": "\n", "NonBreakingSpace": " ",
         "ThinSpace": " ", "EnSpace": " ", "EmSpace": " ", "Ellipsis": "…"}
URI_ABBR = {"section": "s.", "schedule": "Sch.", "paragraph": "para.", "regulation": "reg.",
            "article": "art.", "rule": "r.", "part": "Pt.", "chapter": "Ch.", "annex": "Annex "}


def local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def norm(s):
    s = re.sub(r"[ \t\r\f\v\n]+", " ", s)
    s = re.sub(r"<?\b\w+ Ref=\"[^\"]*\"\s*/>", "", s)  # markup escaped into source text
    s = re.sub(r"\.(?:\s*\.){3,}", "…", s)  # ". . . . ." marks repealed/omitted text
    s = re.sub(r" ([,;:)])", r"\1", s)
    return s.strip()


def itext(e):
    """Flatten an element to a single line of text, dropping editorial markers."""
    out = []

    def rec(x):
        tag = local(x.tag)
        if tag in SKIP_INLINE:
            return
        if tag == "Character":
            out.append(CHARS.get(x.get("Name", ""), " "))
            return
        if tag in ("Image", "IncludedDocument"):
            out.append(" [image] ")
            return
        if tag in BLOCKISH:
            out.append(" ")
        if x.text:
            out.append(x.text)
        for c in x:
            rec(c)
            if c.tail:
                out.append(c.tail)
        if tag in BLOCKISH or tag in ("mo", "mi", "mn"):
            out.append(" ")

    rec(e)
    return norm("".join(out))


def heading(e):
    """Number + Title of a structural element (Title may sit inside a TitleBlock)."""
    num = e.find(NS + "Number")
    ttl = e.find(NS + "Title")
    if ttl is None:
        ttl = e.find(NS + "TitleBlock/" + NS + "Title")
    return " ".join(filter(None, (itext(num) if num is not None else "",
                                  itext(ttl) if ttl is not None else "")))


def pnum(e, default_before="(", default_after=")"):
    n = e.find(NS + "Pnumber")
    if n is None:
        return ""
    num = itext(n)
    if not num:
        return ""
    return n.get("PuncBefore", default_before) + num + n.get("PuncAfter", default_after)


class Renderer:
    """Turns block-level CLML into indented plain-text lines."""

    def block(self, e, depth):
        tag = local(e.tag)
        if tag in SKIP_BLOCK:
            return []
        ind = "    " * depth
        if tag in ("Text", "Title", "Number", "Subtitle", "Term", "Definition", "AppendText",
                   "TableText", "BlockText"):
            if tag == "BlockText":
                return self.children(e, depth)
            t = itext(e)
            return [ind + t] if t else []
        if re.fullmatch(r"P[1-9]", tag):
            before, after = ("", ".") if tag == "P1" else ("(", ")")
            return self.numbered(pnum(e, before, after), e, depth)
        if tag in ("P", "Para") or re.fullmatch(r"P[1-9]para", tag):
            return self.children(e, depth)
        if tag in ("BlockAmendment", "BlockExtract"):
            lines = self.children(e, depth + 1)
            if lines:
                lines[0] = re.sub(r"^(\s*)", r"\1“", lines[0], count=1)
                lines[-1] = lines[-1] + "”"
            return lines
        if tag in ("UnorderedList", "OrderedList"):
            lines = []
            for i, li in enumerate(e.findall(NS + "ListItem"), 1):
                mark = li.get("NumberOverride") or ("•" if tag == "UnorderedList" else f"{i}.")
                lines += self.numbered(mark, li, depth)
            return lines
        if tag == "Tabular":
            lines = []
            for c in e:
                ct = local(c.tag)
                if ct == "table":
                    for tr in c.iter():
                        if local(tr.tag) == "tr":
                            cells = [itext(td) for td in tr if local(td.tag) in ("td", "th")]
                            lines.append(ind + "| " + " | ".join(cells) + " |")
                else:
                    lines += self.block(c, depth)
            return lines
        if tag in ("Formula", "math"):
            t = itext(e)
            return [ind + "[formula] " + t] if t else []
        if tag in ("Figure", "Image"):
            return [ind + "[figure] " + itext(e)]
        if tag == "P1group":
            lines = []
            title = e.find(NS + "Title")
            if title is not None:
                lines.append(ind + itext(title))
            for c in e:
                if local(c.tag) != "Title":
                    lines += self.block(c, depth)
            return lines
        if tag in STRUCT:
            lines = []
            head = heading(e)
            if head:
                lines.append(ind + head)
            for c in e:
                if local(c.tag) not in ("Number", "Title", "TitleBlock"):
                    lines += self.block(c, depth)
            return lines
        if len(e):
            return self.children(e, depth)
        t = itext(e)
        return [ind + t] if t else []

    def children(self, e, depth):
        lines = []
        for c in e:
            if local(c.tag) not in ("Pnumber",):
                lines += self.block(c, depth)
        return lines

    def numbered(self, num, e, depth):
        lines = self.children(e, depth + 1)
        ind = "    " * depth
        if not num:
            return lines
        if lines and lines[0].startswith("    " * (depth + 1)) and not lines[0].strip().startswith("|"):
            lines[0] = ind + num + " " + lines[0].strip()
        else:
            lines.insert(0, ind + num)
        return lines


def label_from_uri(uri, act_path):
    if not uri:
        return ""
    tail = uri.split(act_path, 1)[-1].strip("/")
    toks = tail.split("/")
    parts, i = [], 0
    while i < len(toks):
        kind = toks[i]
        if kind in URI_ABBR:
            nxt = toks[i + 1] if i + 1 < len(toks) and toks[i + 1] not in URI_ABBR else ""
            if kind == "part" and parts and parts[0].startswith("Sch"):
                i += 2 if nxt else 1  # schedule part numbers aren't needed in a citation
                continue
            parts.append(URI_ABBR[kind] + nxt if nxt else URI_ABBR[kind].rstrip("."))
            i += 2 if nxt else 1
        else:
            i += 1
    return " ".join(parts)


class Converter:
    def __init__(self, abbr, act_path, root):
        self.abbr, self.act_path, self.root = abbr, act_path, root
        self.r = Renderer()
        self.out = []
        self.units = 0
        self.label_uri = {}
        self.seen = set()

    def emit_unit(self, label, title, uri, crumbs, flags, body_lines):
        key = (uri, label, tuple(body_lines))
        if key in self.seen:  # some source files repeat whole blocks verbatim
            return
        self.seen.add(key)
        head = f"§ {self.abbr} {label}".rstrip()
        if title:
            head += f" — {title}"
        if flags:
            head += " " + " ".join(f"[{f}]" for f in flags)
        url = (uri or "").replace("http://", "https://")
        self.out.append("")
        self.out.append(head)
        self.out.append(f"@ {url} | {' > '.join(crumbs)}")
        self.out.extend(body_lines)
        self.units += 1

    @staticmethod
    def flags(*els):
        f = []
        for e in els:
            if e is None:
                continue
            if e.get("Status") == "Repealed" and "repealed" not in f:
                f.append("repealed")
            if e.get("Status") == "Prospective" and "prospective" not in f:
                f.append("prospective")
            if e.get("Match") == "false" and "not current" not in f:
                f.append("not current")
        return f

    def unit_from_p1(self, p1, title, crumbs, group=None, ctx_label=""):
        uri = p1.get("DocumentURI", "")
        inner = p1.findall(NS + "P1")
        if not uri and inner:  # anonymous wrapper around real provisions
            for c in inner:
                self.unit_from_p1(c, title, crumbs, group, ctx_label)
            return
        label = label_from_uri(uri, self.act_path)
        if not label:
            n = pnum(p1, "", "")
            label = (ctx_label + " para." + n).strip() if ctx_label else n
        body = self.r.children(p1, 0)
        self.emit_unit(label, title, uri, crumbs, self.flags(group, p1), body)

    def walk(self, e, crumbs, ctx_label=""):
        tag = local(e.tag)
        if tag in STRUCT:
            head = heading(e)
            if tag == "Schedule":
                ctx_label = label_from_uri(e.get("DocumentURI", ""), self.act_path) or ctx_label
                self.label_uri.setdefault(ctx_label, e.get("DocumentURI", ""))
            sub = crumbs + [head] if head else crumbs
            loose = []
            for c in e:
                ct = local(c.tag)
                if ct in ("Number", "Title", "TitleBlock", "Reference") or ct in SKIP_BLOCK:
                    continue
                if ct in STRUCT or ct in ("P1group", "P1"):
                    if loose:
                        self.emit_loose(e, sub, ctx_label, loose)
                        loose = []
                    self.walk(c, sub, ctx_label)
                else:
                    loose += self.r.block(c, 0)
            if loose:
                self.emit_loose(e, sub, ctx_label, loose)
        elif tag == "P1group":
            title = itext(e.find(NS + "Title")) if e.find(NS + "Title") is not None else ""
            loose = []
            for c in e:
                ct = local(c.tag)
                if ct == "Title":
                    continue
                if ct == "P1":
                    self.unit_from_p1(c, title, crumbs, e, ctx_label)
                elif ct in STRUCT or ct == "P1group":
                    self.walk(c, crumbs + [title], ctx_label)
                else:
                    loose += self.r.block(c, 0)
            if loose:
                uri = e.get("DocumentURI", "")
                lab = label_from_uri(uri, self.act_path) or ctx_label
                self.emit_unit(lab, title, uri, crumbs, self.flags(e), loose)
        elif tag == "P1":
            self.unit_from_p1(e, "", crumbs, None, ctx_label)

    def emit_loose(self, e, crumbs, ctx_label, lines):
        if not any(l.strip() for l in lines):
            return
        uri = e.get("DocumentURI", "") or self.label_uri.get(ctx_label, "")
        lab = label_from_uri(uri, self.act_path) or ctx_label or "(unnumbered)"
        title = crumbs[-1] if crumbs else ""
        self.emit_unit(lab, title, uri, crumbs[:-1], self.flags(e), lines)

    def convert(self):
        r = self.root
        meta = r.find(UKM + "Metadata")
        title = meta.findtext(DC + "title") if meta is not None else self.abbr
        valid = meta.findtext(DCT + "valid") if meta is not None else ""
        modified = meta.findtext(DC + "modified") if meta is not None else ""
        unapplied = sum(1 for _ in r.iter(UKM + "UnappliedEffect"))
        doc = r.find(NS + "Primary")
        if doc is None:
            doc = r.find(NS + "Secondary")
        prelims = None
        if doc is not None:
            prelims = doc.find(NS + "PrimaryPrelims")
            if prelims is None:
                prelims = doc.find(NS + "SecondaryPrelims")
        long_title = ""
        if prelims is not None:
            lt = prelims.find(NS + "LongTitle")
            long_title = itext(lt) if lt is not None else ""
        self.out += [
            f"# {title}",
            f"# Source: {BASE}{self.act_path} (revised text; valid {valid}; modified {modified})",
            f"# Outstanding changes not yet applied by legislation.gov.uk: {unapplied}",
            "# Contains public sector information licensed under the Open Government Licence v3.0.",
        ]
        if long_title:
            self.out.append(f"# {long_title}")
        if doc is not None:
            for part in ("Body", "Schedules"):
                el = doc.find(NS + part)
                if el is not None:
                    self.walk(el, [])

        return title, valid, unapplied


def fetch(path, refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    dest = os.path.join(CACHE, path.replace("/", "_") + ".xml")
    if os.path.exists(dest) and not refresh:
        return dest
    url = BASE + path + "/data.xml"
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "uk-tax-code-corpus/1.0"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = resp.read()
            if not data.lstrip().startswith(b"<"):
                raise ValueError("not XML")
            with open(dest + ".part", "wb") as f:
                f.write(data)
            os.replace(dest + ".part", dest)
            return dest
        except Exception as exc:  # network hiccups / rate limiting
            wait = 2 ** (attempt + 1)
            print(f"  fetch {url} failed ({exc}); retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"could not fetch {url}")


def read_manifest():
    rows = []
    with open(os.path.join(HERE, "manifest.tsv"), encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            abbr, path, group, note = (line.rstrip("\n").split("\t") + [""] * 4)[:4]
            rows.append((abbr.strip(), path.strip(), group.strip(), note.strip()))
    return rows


def main(argv):
    refresh = "--refresh" in argv
    only = {a for a in argv if not a.startswith("--")}
    os.makedirs(CORPUS, exist_ok=True)
    stats = []
    for abbr, path, group, note in read_manifest():
        if only and abbr not in only:
            continue
        xml_path = fetch(path, refresh)
        root = ET.parse(xml_path).getroot()
        conv = Converter(abbr, path, root)
        title, valid, unapplied = conv.convert()
        text = "\n".join(conv.out) + "\n"
        with open(os.path.join(CORPUS, abbr + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
        words = len(re.findall(r"\S+", text))
        stats.append((abbr, group, title, path, valid, unapplied, conv.units, words, len(text)))
        print(f"{abbr:14} {group:8} units={conv.units:6} words={words:9,} chars={len(text):11,}  {title}")
    if not only:
        with open(os.path.join(HERE, "stats.tsv"), "w", encoding="utf-8") as f:
            f.write("abbr\tgroup\ttitle\tpath\tvalid_from\tunapplied_changes\tprovisions\twords\tchars\n")
            for row in stats:
                f.write("\t".join(str(x) for x in row) + "\n")
        tw = sum(s[7] for s in stats)
        tc = sum(s[8] for s in stats)
        print(f"TOTAL {len(stats)} instruments, {sum(s[6] for s in stats):,} provisions, "
              f"{tw:,} words, {tc:,} chars")


if __name__ == "__main__":
    main(sys.argv[1:])
