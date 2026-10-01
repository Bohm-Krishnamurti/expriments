# Answering UK tax questions with this corpus

`corpus/*.txt` contains about 15–20M tokens of UK tax legislation (see README.md). Never
read a whole corpus file into context. Find the relevant provisions first and read only
those:

1. Locate: `python3 taxsearch.py search "<terms>"`. Narrow with `--act ITA2007,ITTOIA2005`
   or `--group core`. Use `define "<term>"` for statutory definitions and `toc <ACT> --grep`
   to browse the headings of one Act.
2. Read: `python3 taxsearch.py show <ACT> <label>`, e.g. `show ITA2007 s.35` or
   `show "FA2004 Sch.36 para.12"`. Follow cross-references ("see section 58") the same way.
3. Cite each claim with its provision label and the legislation.gov.uk URL from the
   provision's header.

Points to check:
- Consolidated Acts (`core`) state the law. Finance Acts (`finance`) set many annual rates
  and contain standalone regimes, and the rest of their content is mostly amendments to
  core Acts.
- A provision shown as `…` or flagged `[repealed]` has no current text. Look for the
  replacement provision.
- Each file's header gives the count of changes legislation.gov.uk hasn't applied yet.
  When that count is high, say the text may be out of date.
- Devolved rates (Scottish and Welsh income tax, LBTT, LTT) and HMRC guidance are not in
  the corpus.
