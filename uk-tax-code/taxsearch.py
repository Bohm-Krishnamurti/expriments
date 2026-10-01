#!/usr/bin/env python3
"""Search and read the UK tax legislation corpus built by build.py.

    python3 taxsearch.py search "annual investment allowance"      # ranked provisions
    python3 taxsearch.py search 'residence "sufficient ties"' --act FA2013
    python3 taxsearch.py search --regex "personal allowance.{0,40}£" --group core
    python3 taxsearch.py show ITA2007 s.35                          # full text of a provision
    python3 taxsearch.py show "FA2013 Sch.45 para.17"
    python3 taxsearch.py define "connected"                          # where a term is defined
    python3 taxsearch.py toc CTA2010 --grep "group relief"           # list provision headings
    python3 taxsearch.py acts                                        # what's in the corpus

Search terms are ANDed (falls back to "most terms matched" if nothing has them all);
"double quotes" keep a phrase together. Repealed/empty provisions are hidden unless
--all is given.
"""

import argparse
import math
import os
import re
import signal
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus")
STOP = {"the", "a", "an", "of", "and", "or", "to", "in", "for", "on", "is", "be", "by", "as",
        "at", "with", "what", "how", "does", "do", "which", "that", "this", "are", "it", "from"}
HEAD = re.compile(r"^§ (\S+) (.*?)(?: — (.*?))?((?: \[[^\]]+\])*)$")


class Provision:
    __slots__ = ("abbr", "label", "title", "flags", "url", "crumbs", "body", "low", "group")

    def __init__(self, block, group):
        lines = block.split("\n")
        m = HEAD.match(lines[0])
        self.abbr, self.label = m.group(1), m.group(2).strip()
        self.title = (m.group(3) or "").strip()
        self.flags = re.findall(r"\[([^\]]+)\]", m.group(4) or "")
        meta = lines[1][2:] if len(lines) > 1 and lines[1].startswith("@ ") else ""
        self.url, _, self.crumbs = meta.partition(" | ")
        self.url = self.url.strip()
        self.body = "\n".join(lines[2:] if meta else lines[1:]).strip("\n")
        self.low = (self.title + "\n" + self.body).lower()
        self.group = group

    @property
    def cite(self):
        return f"{self.abbr} {self.label}".strip()

    @property
    def empty(self):
        """Repealed, or nothing left but numbering and "…" markers."""
        if "repealed" in self.flags:
            return True
        rest = re.sub(r"^\s*(?:\([0-9A-Za-z]+\)\s*)+", "", self.body, flags=re.M).replace("…", "")
        return not re.search(r"[A-Za-z]{2,}", rest)

    def header(self):
        h = f"§ {self.cite}"
        if self.title:
            h += f" — {self.title}"
        if self.flags:
            h += " " + " ".join(f"[{f}]" for f in self.flags)
        return h


def load(acts=None, groups=None):
    manifest = {}
    with open(os.path.join(HERE, "manifest.tsv"), encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                cols = line.rstrip("\n").split("\t")
                manifest[cols[0]] = (cols[2], cols[3] if len(cols) > 3 else "")
    provs = []
    for abbr, (group, _) in manifest.items():
        if acts and abbr.upper() not in acts:
            continue
        if groups and group not in groups:
            continue
        path = os.path.join(CORPUS, abbr + ".txt")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for block in text.split("\n§ ")[1:]:
            provs.append(Provision("§ " + block, group))
    if not provs:
        sys.exit("No provisions loaded - run build.py first, or check --act/--group.")
    return provs, manifest


def parse_query(q):
    terms = [p.lower() for p in re.findall(r'"([^"]+)"', q)]
    rest = re.sub(r'"[^"]+"', " ", q)
    terms += [w.lower() for w in re.findall(r"[\w£%'’-]+", rest) if w.lower() not in STOP]
    return terms


def snippet(p, terms=None, rx=None, width=220, max_lines=3):
    out = []
    for line in p.body.split("\n"):
        low = line.lower()
        hit = rx.search(line) if rx else next((t for t in terms if t in low), None)
        if not hit:
            continue
        s = line.strip()
        if len(s) > width:
            pos = hit.start() if rx else s.lower().find(hit)
            start = max(0, pos - width // 3)
            s = ("…" if start else "") + s[start:start + width] + "…"
        out.append("    " + s)
        if len(out) >= max_lines:
            break
    return out


def cmd_search(args):
    provs, _ = load(args.act, args.group)
    if not args.all:
        provs = [p for p in provs if not p.empty]
    if args.regex:
        rx = re.compile(args.query, re.I)
        hits = [(len(rx.findall(p.title + "\n" + p.body)), p) for p in provs]
        hits = [(s, p) for s, p in hits if s]
        hits.sort(key=lambda x: -x[0])
        show_hits(hits, args, rx=rx)
        return
    terms = parse_query(args.query)
    if not terms:
        sys.exit("empty query")
    n = len(provs)
    df = {t: sum(1 for p in provs if t in p.low) for t in terms}
    idf = {t: math.log(1 + n / (1 + df[t])) for t in terms}
    scored = []
    for p in provs:
        matched = [t for t in terms if t in p.low]
        if not matched:
            continue
        s = 0.0
        tl = p.title.lower()
        for t in matched:
            tf = p.low.count(t)
            s += (1 + math.log(tf)) * idf[t] * (2.0 if t in tl else 1.0)
        phrase = " ".join(terms)
        if tl == phrase:
            s *= 3.0
        elif phrase in tl:
            s *= 1.5
        s /= math.sqrt(1 + len(p.body) / 4000)  # don't let giant schedules win on volume
        if p.group != "finance":
            s *= 1.25  # consolidated Acts state the law; Finance Acts often just amend it
        scored.append((len(matched), s, p))
    full = [x for x in scored if x[0] == len(terms)]
    if not full and scored:
        print(f"(no provision contains all of {terms}; showing best partial matches)\n")
        full = scored
    full.sort(key=lambda x: (-x[0], -x[1]))
    show_hits([(s, p) for _, s, p in full], args, terms=terms)


def show_hits(hits, args, terms=None, rx=None):
    total = len(hits)
    for s, p in hits[: args.limit]:
        print(p.header())
        print(f"    {p.url}")
        if p.crumbs:
            print(f"    in: {p.crumbs}")
        if args.full:
            print("\n".join("    " + l for l in p.body.split("\n")))
        else:
            for l in snippet(p, terms=terms, rx=rx):
                print(l)
        print()
    print(f"[{min(total, args.limit)} of {total} matching provisions shown]")


def norm_label(s):
    s = s.lower().replace(" ", "")
    s = re.sub(r"^(section|sec)\.?", "s.", s)
    s = re.sub(r"^s(?=\d)", "s.", s)
    s = re.sub(r"(schedule|sch)\.?", "sch.", s)
    s = re.sub(r"(paragraph|para)\.?", "para.", s)
    s = re.sub(r"^(regulation|reg)\.?", "reg.", s)
    return s


def cmd_show(args):
    spec = " ".join(args.ref).strip()
    m = re.match(r"(\S+)\s+(.+)", spec)
    if not m:
        sys.exit('usage: show ACT LABEL   e.g. show ITA2007 s.35   or   show "FA2013 Sch.45 para.17"')
    abbr, label = m.group(1).upper(), norm_label(m.group(2))
    provs, _ = load({abbr})
    found = [p for p in provs if norm_label(p.label) == label]
    if not found:  # e.g. "s.35" given loosely, or a whole schedule "Sch.45"
        found = [p for p in provs if norm_label(p.label).startswith(label)
                 and not norm_label(p.label)[len(label):len(label) + 1].isalnum()]
    if not found:
        sys.exit(f"{abbr} {m.group(2)}: not found (try: toc {abbr} --grep ...)")
    for p in found[: args.limit]:
        print(p.header())
        print(f"{p.url}")
        if p.crumbs:
            print(f"in: {p.crumbs}")
        print()
        print(p.body)
        print()
    if len(found) > args.limit:
        print(f"[{args.limit} of {len(found)} provisions shown; raise --limit]")


def cmd_define(args):
    term = args.term.strip().lower()
    provs, _ = load(args.act, args.group)
    q = re.escape(term)
    rx = re.compile(r"[“\"]" + q + r"[”\"]\s*(?:\([^)]*\)\s*)?(?:means|has the meaning|includes|is|are|"
                    r"shall|,? in relation to)\b", re.I)
    rx2 = re.compile(r"(?:(?:meaning of|definition of)\s*[“\"]" + q + r"[”\"]|^[“\"]" + q + r"[”\"]\s*$)", re.I)
    hits = []
    for p in provs:
        if p.empty:
            continue
        n = len(rx.findall(p.body))
        if rx2.search(p.title) or rx2.search(p.crumbs.rsplit(" > ", 1)[-1]):
            n += 5
        if n:
            hits.append((n + (1 if p.group != "finance" else 0), p))
    hits.sort(key=lambda x: -x[0])
    args.full = False
    show_hits(hits, args, rx=re.compile(re.escape(term), re.I))


def cmd_toc(args):
    provs, _ = load({args.act.upper()})
    rx = re.compile(args.grep, re.I) if args.grep else None
    for p in provs:
        line = p.header()
        if rx and not (rx.search(line) or rx.search(p.crumbs)):
            continue
        if not args.all and p.empty:
            continue
        print(line)


def cmd_acts(args):
    stats = os.path.join(HERE, "stats.tsv")
    with open(stats, encoding="utf-8") as f:
        rows = [l.rstrip("\n").split("\t") for l in f][1:]
    for r in rows:
        print(f"{r[0]:14} {r[1]:8} {int(r[7]):>9,} words  {r[2]}  (valid {r[4]})")
    print(f"{'TOTAL':14} {'':8} {sum(int(r[7]) for r in rows):>9,} words")


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet when piped into head
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--act", type=lambda s: {a.strip().upper() for a in s.split(",")},
                       help="comma-separated abbreviations, e.g. ITA2007,TCGA1992")
        p.add_argument("--group", type=lambda s: set(s.split(",")), help="core, finance, si")
        p.add_argument("--limit", type=int, default=10)
        p.add_argument("--all", action="store_true", help="include repealed/empty provisions")

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--regex", action="store_true")
    p.add_argument("--full", action="store_true", help="print whole provisions, not snippets")
    common(p)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("show")
    p.add_argument("ref", nargs="+")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("define")
    p.add_argument("term")
    common(p)
    p.set_defaults(fn=cmd_define)

    p = sub.add_parser("toc")
    p.add_argument("act")
    p.add_argument("--grep")
    p.add_argument("--all", action="store_true")
    p.set_defaults(fn=cmd_toc)

    p = sub.add_parser("acts")
    p.set_defaults(fn=cmd_acts)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
