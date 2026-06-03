# Diffusion Public-Market Research — v2 (empirically tested)

*Rewritten with live market data and a statistical test of the thesis.
Universe: 47 listed names + S&P 500. Source of truth: Yahoo adjusted-close for 1Y total
return (dividends reinvested); yfinance for trailing P/E and market cap. Run 2026-05-30.
Benchmark: **S&P 500 +29.8%** on the trailing year — the single most important number in this
document, because it means "down 30%" is really "lagging the market by ~60 points," and "up 8%"
is really a 22-point underperformance.*

---

## What changed from v1

v1 was an **exposure map**: it identified where AI *could* bite (digital, verifiable, chainable
work) and observed that the exposed names had sold off. v2 tests whether that exposure actually
explains the sell-off. **It does not.** Once you add the axis the original report was missing —
**deployment friction** — AI-exposure loses all independent power to explain returns. The screen
turns out to be a friction screen, and the cross-section is a builder-vs-deployer rotation plus
idiosyncratic catalysts. The genuinely tradable idea is not the buckets; it is the firm-level
owner-vs-reseller distinction run as relative value, and the friction-protected incumbents the
market has not yet paid for the productivity they are about to internalize.

---

## 1. Paper selection (unchanged)

Two papers answer different halves of the question.

- **RL exposure / post-trainability (RLFI lineage).** Scores all 17,951 O\*NET task-occupation
  pairs across 894 occupations by how feasible it is to improve an LLM on that task via RL-style
  post-training. Uses O\*NET 30.0 task descriptions, a physical-feasibility gate, eight
  RL-feasibility dimensions, and O\*NET task-importance weights to aggregate to occupations.
  *Answers: which tasks/jobs are post-trainable?*
- **NBER chaining paper.** Models production as a sequence of steps (manual / AI-augmented /
  fully automated) inside contiguous AI-executed "chains." Key point: AI exposure matters more
  when exposed steps are **adjacent and chainable**, not merely present. *Answers: when do
  trainable tasks become automatable workflows?*

The eight RL-scoring dimensions: verification method, environment simulability, state
observability, task variability, sequential decision depth, feedback density/decomposability,
tool/interface accessibility, output tangibility/gradeability.

### 1b. The axis both papers imply but v1 omitted: deployment friction

The RSI/diffusion argument is that **being automatable and being automated-in-practice are
different things**, separated by friction that is *structural, not incidental*: regulation,
unions, liability, physical-world interfaces, compliance/explainability, legacy-system
integration, and capex cycles. A task can score maximally on RL-feasibility and still take years
to hit a P&L. This is the same logic as the NBER chaining filter, extended past the firm's
workflow into its regulatory and physical environment. v2 makes friction a first-class variable —
and it turns out to be *the* variable.

---

## 2. Exposed occupations (unchanged)

- **Absolute high-RL occupations:** data-entry keyers, correspondence clerks, proofreaders,
  credit clerks, payroll/timekeeping clerks, statistical assistants, brokerage clerks, order
  clerks, insurance claims/policy clerks, bookkeeping/accounting/auditing clerks. Digital,
  rule-governed, verifiable, gradeable.
- **Hidden high-RL / low-standard-LLM-exposure occupations:** aircraft cargo-handling
  supervisors, power distributors/dispatchers, railroad conductors/yardmasters, gas-plant
  operators, chemical-plant operators. Less text-centric, but instrumented and
  outcome-verifiable — so more RL-trainable than text-based screens suggest. **(These are also
  the highest-friction occupations of all — flag this; it matters in §6.)**

---

## 3. Occupation → industry mapping (unchanged)

- **Direct:** payroll clerks → payroll/HCM; claims clerks → insurance; brokerage clerks →
  brokerage/financial ops; credit clerks → banks/cards/credit bureaus; order clerks →
  logistics/wholesale/e-commerce.
- **Paper-based sector tilt:** Finance & Insurance, Information, Professional & Technical
  Services, Management of Companies, Wholesale Trade, Utilities, Administrative & Waste Services,
  Manufacturing.
- **NBER filter:** prioritize industries where exposed tasks form contiguous chains — claims,
  payroll, KYC, credit authorization, brokerage ops, order management, routing, dispatch,
  reconciliation, correspondence.

---

## 4. Firm selection (unchanged criteria) + the taxonomy that turned out to matter

Selection criteria: scale, purity of exposure, workflow ownership, public comparability.

The decisive lens, stated in v1 and confirmed in v2, is **what the firm *is* relative to the
workflow**:

| Type | Definition | AI sign |
|---|---|---|
| **Reseller** | sells labor *into* the workflow | loses if it automates |
| **Platform** | owns the software / system-of-record rails | ambiguous |
| **Incumbent** | internalizes both the workflow and the productivity gain | beneficiary |
| **Control** | instrumented physical/ops control layer ("hidden" RL) | beneficiary, but slow |
| **Builder** | AI infrastructure (added in v2 as a control group) | the rotation winner |

---

## 5. Live market data

*Trailing-year total return, trailing P/E, market cap. P/E flagged N/M where earnings are
negative or distorted by one-offs (e.g. CI, ALL, DOW — do not read P/E as a signal here).*

| Cluster | Co | Tkr | Tax | RL | Friction | Mcap | 1Y total ret | P/E |
|---|---|---|---|---:|---:|---:|---:|---:|
| BPO/IT | Accenture | ACN | reseller | 70 | 35 | $115B | **−40.2%** | 15.3 |
| BPO/IT | Cognizant | CTSH | reseller | 78 | 30 | $26B | −29.7% | 12.1 |
| BPO/F&A | Genpact | G | reseller | 90 | 25 | $5.6B | −22.5% | 10.1 |
| Customer ops | Concentrix | CNXC | reseller | 92 | 20 | $1.7B | −47.6% | N/M |
| Analytics BPO | EXLService | EXLS | reseller | 88 | 28 | $4.4B | −36.9% | 18.5 |
| Digital ops | TaskUs | TASK | reseller | 90 | 18 | $0.6B | −41.5% | 5.6 |
| BPO | Conduent | CNDT | reseller | 85 | 30 | $0.3B | −22.8% | N/M |
| Payroll/HCM | ADP | ADP | platform | 60 | 45 | $89B | −30.1% | 20.7 |
| Payroll/HCM | Paychex | PAYX | platform | 60 | 45 | $35B | −36.1% | 21.4 |
| HCM sw | Workday | WDAY | platform | 45 | 50 | $36B | −41.0% | 45.5 |
| Payroll sw | Paycom | PAYC | platform | 55 | 45 | $6.5B | −45.6% | 16.1 |
| Tax/SMB sw | Intuit | INTU | platform | 58 | 40 | $90B | **−55.6%** | 20.2 |
| Enterprise sw | Oracle | ORCL | platform | 40 | 55 | $649B | **+37.8%** | 40.5 |
| Enterprise sw | SAP | SAP | platform | 40 | 55 | $214B | −38.9% | 25.0 |
| Banking | JPMorgan | JPM | incumbent | 55 | 75 | $802B | +15.6% | 14.3 |
| Banking | Bank of America | BAC | incumbent | 55 | 75 | $366B | +19.6% | 12.8 |
| Banking | Wells Fargo | WFC | incumbent | 55 | 78 | $237B | +6.0% | 12.0 |
| Cards | American Express | AXP | incumbent | 55 | 70 | $216B | +8.8% | 19.8 |
| Brokerage | Schwab | SCHW | incumbent | 58 | 68 | $152B | +0.1% | 17.4 |
| Brokerage | Morgan Stanley | MS | incumbent | 50 | 70 | $328B | **+66.4%** | 18.8 |
| Brokerage | Goldman Sachs | GS | incumbent | 50 | 70 | $302B | **+73.5%** | 18.7 |
| Health ins | UnitedHealth | UNH | incumbent | 60 | 80 | $345B | +29.5% | 28.7 |
| Health ins | Elevance | ELV | incumbent | 60 | 80 | $85B | +4.6% | 16.7 |
| Health ins | Cigna | CI | incumbent | 58 | 80 | $73B | −10.5% | N/M |
| P&C ins | Progressive | PGR | incumbent | 58 | 65 | $111B | −28.8% | 9.7 |
| P&C ins | Allstate | ALL | incumbent | 55 | 65 | $53B | +0.1% | N/M |
| P&C ins | Chubb | CB | incumbent | 52 | 68 | $121B | +5.6% | 11.0 |
| P&C ins | Travelers | TRV | incumbent | 52 | 68 | $62B | +7.6% | 8.7 |
| Insurance | AIG | AIG | incumbent | 50 | 70 | $39B | −10.3% | 13.1 |
| Insurance | MetLife | MET | incumbent | 50 | 70 | $53B | +8.4% | 16.0 |
| Utility/grid | NextEra | NEE | control | 45 | 88 | $181B | +26.8% | 22.1 |
| Utility/grid | Duke Energy | DUK | control | 42 | 88 | $96B | +7.9% | 18.9 |
| Utility/grid | Southern Co | SO | control | 42 | 88 | $104B | +5.6% | 23.5 |
| Utility/power | Constellation | CEG | control | 45 | 85 | $104B | −5.5% | 25.0 |
| Rail | Union Pacific | UNP | control | 48 | 82 | $156B | +21.2% | 21.6 |
| Rail | CSX | CSX | control | 48 | 82 | $84B | +45.3% | 27.8 |
| Rail | Norfolk Southern | NSC | control | 48 | 82 | $68B | +25.7% | 25.7 |
| Parcel | UPS | UPS | control | 55 | 60 | $90B | +16.9% | 17.3 |
| Parcel | FedEx | FDX | control | 55 | 60 | $98B | **+93.0%** | 22.0 |
| Industrial gas | Linde | LIN | control | 40 | 80 | $230B | +7.9% | 33.0 |
| Chemicals | Dow | DOW | control | 40 | 78 | $24B | +28.0% | N/M |
| AI infra | Nvidia | NVDA | builder | 10 | 30 | $5.1T | +56.3% | 32.4 |
| AI infra | Microsoft | MSFT | builder | 15 | 35 | $3.3T | −1.4% | 26.8 |
| AI infra | Alphabet | GOOGL | builder | 15 | 35 | $4.6T | **+122.2%** | 29.0 |
| AI infra | Broadcom | AVGO | builder | 10 | 30 | $2.1T | +86.1% | 86.9 |
| AI deployer | Palantir | PLTR | builder | 20 | 40 | $375B | +18.8% | 175.9 |
| Benchmark | S&P 500 | SPY | — | — | — | — | **+29.8%** | 28.4 |

**Data corrections vs the v1 narrative.** Against one source: Intuit is −55.6% (v1 said −55.9% —
correct; a later "it's really −40%" correction was itself wrong). ACN −40.2% vs −39.6%, FDX
+93.0% vs +91.5%, ORCL +37.8% vs +40.0% — all fine. P/E is unusable on several names (CI 2.4x,
ALL 4.6x are one-off-distorted); returns are clean.

---

## 6. The test

### 6.1 Friction beats exposure
```
corr(1Y return, RL-exposure) = -0.48     # looks like the thesis works...
corr(1Y return, friction)    = +0.62     # ...but friction is stronger
```

### 6.2 The quadrant grid (mean 1Y return)
|  | Low friction | High friction |
|---|---:|---:|
| **High RL-exposure** | **−34%** | **+17%** |
| **Low RL-exposure** | −47% | +16% |

Returns sort by **column (friction)**, not row (exposure). Two baskets with *identical* high
RL-exposure are 51 points apart on friction alone.

### 6.3 Regression
```
ret1y ~ rl + friction + rl*friction      (n=41, ex-builders, R² = 0.39)
   friction     +1.15   (dominant)
   rl           +0.15   (flips POSITIVE once friction is controlled ≈ zero effect)
   rl*friction  -0.001
```
**RL-exposure has no independent power to explain returns once friction is held constant.** The
raw −0.48 was a confound: in this universe "high RL-exposure" mostly means "low-friction digital
labor reseller." The screen is a deployment-friction screen wearing an AI costume — exactly what
the RSI/diffusion argument predicts (friction is structural, and it is what gets priced).

### 6.4 The rotation
```
AI infrastructure builders : +56.4%
AI deployers (resel+platf) : -32.2%
spread                     :  88.6 points
```
The market rewarded compute/supply and punished anything labelled "AI services / deployer,"
fundamentals aside.

### 6.5 Within-bucket dispersion (where relative value lives)
| Bucket | spread | best | worst | σ |
|---|---:|---|---|---:|
| reseller | 25 pts | G −22% | CNXC −48% | 10 |
| platform | 93 pts | ORCL +38% | INTU −56% | 31 |
| incumbent | 102 pts | GS +73% | PGR −29% | 26 |
| control | 99 pts | FDX +93% | CEG −6% | 26 |

The reseller bucket is **tight** — the market treats every reseller as one repriced beta.
Platform / incumbent / control are **wide** — that is where the owner-vs-reseller taxonomy does
work the bucket cannot.

---

## 7. Interpretation

**1. The market is pricing friction, not AI.** The clean read of §6 is that the sell-off in
resellers and process software is a *low-friction* sell-off; the pass given to banks, insurers,
utilities, rails and gases is a *high-friction* pass. AI-exposure is incidental to both. This is
the RSI/diffusion thesis made empirical: capability is necessary but not sufficient; deployment
runs through structural friction; and equity prices are already discounting that gap.

**2. "Doing badly" is mostly lagging a +30% market, for mundane reasons.** Resellers fell on cut
guidance (ACN), federal-contract cuts (ACN/DOGE), and a tax-season miss + securities probe (INTU)
— not on demonstrated workflow cannibalization. Trailing return is the residue of those
catalysts, which is why an exposure screen built on trailing return can't distinguish them.

**3. The headline control-layer names already ran for non-AI reasons.** FDX +93% (DRIVE cost
program + freight spin), CSX +45%, NEE +27% (data-center power demand). The "hidden RL" thesis
did not drive these; and because control-layer work is the *highest-friction* of all (§2), the RL
exposure there will not convert to P&L for years — the essay's point precisely.

**4. Platforms and incumbents are the under-priced beneficiaries.** Platforms own the workflow
rails; incumbents internalize both the cost base and the productivity gain. Incumbents returned
only +12% (lagged the market by 18 pts) despite carrying the same automatable workflow volume as
the resellers *and* keeping the margin. They have received no credit for productivity they are
positioned to internalize behind a friction moat.

---

## 8. Where the alpha is

**Not in the buckets.** "Short BPO" is consensus: resellers lagged the market by 64 pts and their
within-bucket dispersion is tiny. Finding stocks that already fell on your thesis is selecting on
the dependent variable.

**1. Owner-vs-reseller, as relative value.** Long the firm that owns the system-of-record / data,
short the one that resells headcount, *inside the same exposure bucket*. The bucket is priced; the
spread (platform 93 pts, incumbent 102, control 99) is not. This is v1's real intellectual content.

**2. Friction-protected incumbents who internalize the gain.** Same workflow volume as resellers,
a friction pass, and they keep the margin — yet still trailing the market with no credit for the
productivity. Cleanest un-crowded long, and the trade the diffusion essay most supports: the gain
is coming, friction delays it, the market hasn't paid for it.

**3. Mean-reversion in over-punished resellers** has a *fundamental* basis (even digital
deployment carries integration/trust/compliance friction; resellers can pivot to AI-managed
services) — but it is a crowded contrarian view. Size accordingly; it is not undiscovered.

---

## 9. What would turn this into a signal (roadmap, not yet built)

1. **Forward signals over trailing.** Replace trailing return + trailing P/E (backward-looking;
   P/E meaningless on collapsing/negative E — CNXC, CI, ALL are tells) with earnings-revision
   breadth, margin trajectory, and AI-revenue mix. Exposure says where the water is; revisions say
   when it floods the P&L — and the essay says that lag is long and jagged.
2. **A real friction factor.** Build regulatory intensity, unionization %, and capex cycle into a
   proper friction score; a crude ordinal version already out-explained the entire AI axis (§6).
3. **Trade the dispersion, not the bucket.** Construct the owner-vs-reseller pairs explicitly and
   measure the spread's history.
4. **Decompose realized returns** against guidance/sector/rate factors to confirm AI-exposure adds
   nothing beyond friction — §6 strongly suggests it doesn't.

---

## 10. Bottom line

As a labor-economics exposure map, the RLFI lineage is sound and v1 should not apologize for it.
As an alpha screen it is **right and late**: it rediscovered a friction factor and the
builder-over-deployer rotation, both already in the price. The one genuinely tradable idea is v1's
own firm-level taxonomy — **owner vs reseller** — expressed as within-bucket relative value, plus
the friction-protected incumbents the market has not yet paid for the productivity they are about
to internalize. The cleanest one-line thesis is no longer "AI automates jobs." It is:

> **AI exposure is priced through deployment friction. The losers are low-friction labor resellers
> the market has already repriced; the edge is in distinguishing workflow owners from labor
> resellers, and in friction-protected incumbents who will internalize the gain before the market
> credits it.**

*Not investment advice. Exposure and friction scores are judgmental ordinal inputs; n per bucket
is small; single-vendor data over a single 1Y window — directional, not a backtest. Refresh
figures before any use.*
