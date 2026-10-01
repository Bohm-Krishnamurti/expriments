# UK tax code: local searchable copy

This folder holds the current revised text of UK tax legislation as plain text, taken from
[legislation.gov.uk](https://www.legislation.gov.uk). It also has a small CLI for searching
the text and citing it. The snapshot was taken in October 2026. Each file's header shows
the date its text is valid from.

## What's in it

| Group | Instruments | Provisions | Words | Est. tokens* |
|---|---:|---:|---:|---:|
| `core`: consolidated tax Acts (ITA 2007, ITEPA 2003, ITTOIA 2005, CTA 2009/2010, TIOPA 2010, TCGA 1992, CAA 2001, IHTA 1984, VATA 1994, TMA 1970, SSCBA 1992, customs/excise, stamp duty, …) | 22 | 23,152 | 4.35M | ~7–9M |
| `finance`: Finance Acts 1986, 1996, 2000–2026. These hold standalone regimes (SDLT, pensions, GAAR, ATED, DPT, DST, Pillar Two, penalties, HMRC powers, annual rate-setting) and the amending provisions. | 36 | 23,406 | 4.99M | ~8–11M |
| `si`: PAYE Regulations 2003, VAT Regulations 1995, Social Security (Contributions) Regulations 2001 | 3 | 1,514 | 0.31M | ~0.5–0.6M |
| **Total** | **61** | **48,072** | **9.65M** | **~15–20M** |

\*Token counts are estimates (characters ÷ 4 to characters ÷ 3). I haven't measured them
with a tokenizer. Per-instrument figures are in `stats.tsv` and `manifest.tsv` lists every
source.

The full set is far too big for one context window. A 1M-token window holds about 5–7% of
it, and the largest single Acts nearly fill a window on their own: CTA 2010 is about
0.8–1.1M tokens, ITA 2007 about 0.7–1.0M and CTA 2009 about 0.7–1.0M. The way to use it is
to **search it and pull in only the provisions you need**.

## Usage

```bash
python3 taxsearch.py search "annual exempt amount"            # ranked provisions with snippets
python3 taxsearch.py search 'loan "close company"' --act CTA2010 --full
python3 taxsearch.py search --regex "£[0-9,]+ for a tax year" --group core
python3 taxsearch.py show TCGA1992 s.1K                       # full text of a provision
python3 taxsearch.py show "FA2013 Sch.45 para.17"            # schedule paragraphs
python3 taxsearch.py define "connected"                       # where a term is defined
python3 taxsearch.py toc ITA2007 --grep "gift aid"            # headings for one Act
python3 taxsearch.py acts                                     # list instruments
```

Plain `grep`/`rg` also works. Every provision starts with two header lines:

```
§ ITA2007 s.35 — Personal allowance
@ https://www.legislation.gov.uk/ukpga/2007/3/section/35 | Part 3 Personal reliefs > Chapter 2 ...
(1) An individual who makes a claim is entitled to a personal allowance of £12,570 ...
```

`…` marks text that has been repealed or omitted. Header flags such as `[repealed]` and
`[not current]` come from the source XML.

## Rebuilding / extending

```bash
python3 build.py              # downloads to .cache/ (git-ignored), writes corpus/ + stats.tsv (~2 min)
python3 build.py --refresh    # re-download to pick up newer revisions
python3 build.py ITA2007      # rebuild one instrument
```

To add an instrument, add a line to `manifest.tsv` with its abbreviation, its
legislation.gov.uk path (for example `uksi/2006/964`), a group and a note. Then run
`build.py`. The script uses only the Python standard library.

## Caveats

- **Revised text can lag.** Each file's header gives the number of changes that
  legislation.gov.uk has recorded but not yet applied. Some files have a lot: TMA 1970 has
  243, SSCBA 1992 has 224, VAT Regs 1995 and FA 2026 have 122 each, and TCGA 1992 has 71.
  For anything that matters, check the provision's page online.
- **Many rates are set each year.** For example, the income tax rates for a tax year are
  set by a section of that year's Finance Act, so search the `finance` group as well.
- **Not included:**
  - HMRC manuals and other guidance
  - case law
  - most statutory instruments
  - devolved taxes (LBTT, LTT, Scottish and Welsh rate resolutions)
  - Budget resolutions and provisional collection
  - Northern Ireland-only legislation
- This is not legal or tax advice.

## Licence

Contains public sector information licensed under the
[Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
Source: legislation.gov.uk (The National Archives).
