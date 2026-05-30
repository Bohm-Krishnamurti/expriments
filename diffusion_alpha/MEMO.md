# Diffusion screen — tested against live data

*Universe: 47 names + SPY. Source of truth: Yahoo adjusted-close (total return, dividends
reinvested) for 1Y returns; yfinance trailing P/E & market cap. Run 2026-05-30.
Benchmark: S&P 500 +29.8% on the year — so "down 30%" means lagging the market by ~60 points.*

## 0. Data corrections (the memo's own methodology step)
| Name | Report | Live (1 source) | Verdict |
|---|---|---|---|
| Intuit (INTU) | −55.9% | **−55.6%** | report correct; the "−40%" correction was wrong |
| Accenture (ACN) | −39.6% | −40.2% | fine |
| FedEx (FDX) | +91.5% | +93.0% | fine |
| Oracle (ORCL) | +40.0% | +37.8% | fine |

The pasted critique's two "stale data" flags were themselves stale. INTU really is ~−56%.
(Note: a few P/Es are junk on one-off earnings — CI 2.4x, ALL 4.6x — so P/E is unusable
as a signal here; returns are clean.)

## 1. The result that breaks the thesis
Two axes, separated for the first time:
- **RL-exposure** — how automatable the workflow chains are (the report's axis)
- **Deployment friction** — regulation, unions, physical world, compliance, legacy
  integration (the axis from the RSI/diffusion essay)

```
corr(1Y return, RL-exposure) = -0.48   <- looks like the thesis works
corr(1Y return, friction)    = +0.62   <- but this is stronger
```

Quadrant grid (mean 1Y return):

|              | Low friction | High friction |
|---|---|---|
| **High RL-exposure** | **−34%** | **+17%** |
| **Low RL-exposure**  | −47% | +16% |

Returns sort by **column (friction)**, not row (exposure). Two baskets with *identical*
high RL-exposure are 51 points apart depending only on friction. OLS confirms it:

```
ret ~ rl + friction + rl*friction      (n=41, ex-builders, R²=0.39)
  friction   +1.15   (dominant)
  rl         +0.15   (flips POSITIVE once friction is controlled — i.e. ~zero)
```

**RL-exposure has no independent power to explain returns once friction is held constant.**
The raw −0.48 was a confound: in this universe "high RL-exposure" mostly means "low-friction
digital labor reseller." The screen is a deployment-friction screen wearing an AI costume —
which is exactly the essay's claim (friction is structural, not incidental) showing up in prices.

## 2. Why they're "doing badly" — they're not, and the cause isn't AI
- The split tracks **friction + a builder-vs-deployer rotation**, not exposure.
- AI infrastructure builders +56.4% vs deployers (resellers+platform) −32.2% = **89-point spread.**
  The market rewarded compute/supply and punished anything labelled "AI services/deployer,"
  fundamentals aside.
- The reseller losses are real but the *proximate* triggers are mundane: cut guidance (ACN),
  DOGE federal-contract cuts (ACN), a TurboTax/tax-season miss + securities probe (INTU).
  The exposure screen can't see any of this — it only has trailing return, which is the
  *residue* of those catalysts.

## 3. Where the alpha is NOT
- **Not in the buckets.** "Short BPO" is in the price: resellers lagged the market by **64 pts**
  and their within-bucket dispersion is tiny (spread 25 pts, σ=10) — the market treats every
  reseller as the same already-repriced beta. That's consensus, not edge.
- **Not in the headline control-layer names.** FDX (+93%, DRIVE cost program + freight spin)
  and CSX (+45%) already ran on self-help, not AI. NEE/CEG ran/lagged on power-demand and rates.

## 4. Where residual edge could actually live
1. **Within-bucket dispersion (pairs).** Where the taxonomy does work the bucket can't:
   - platform σ huge (spread 93 pts: ORCL +38% vs INTU −56%)
   - incumbent spread 102 pts (GS +73% vs PGR −29%)
   - control spread 99 pts
   Express the report's real insight — **long the workflow/data OWNER, short the labor RESELLER
   inside the same exposure bucket** — as relative value. The bucket is priced; the spread isn't.
2. **Friction-protected incumbents who internalize the gain.** Same automatable workflow volume
   as the resellers (rl ≈ 55) but a friction pass *and* they keep the productivity. They still
   only returned +12% (lagged market by 18 pts) and got no credit for margin upside. This is the
   report's "productivity beneficiary" bucket and it's the cleanest un-crowded long.
3. **The mean-reversion view (resellers over-punished)** has a *fundamental* basis from the
   essay — even digital deployment carries integration/trust/compliance friction, and resellers
   can pivot to AI-managed-services — but it's a crowded contrarian view, so size accordingly.

## 5. What would make this a signal (not in the table yet)
- Replace trailing return + trailing P/E with **forward** signals: earnings-revision breadth,
  margin trajectory, AI-revenue mix. Exposure says where the water is; revisions say when it
  floods the P&L — and the essay says that lag is long and jagged.
- Trade cross-sectional dispersion *inside* buckets, not the buckets.
- Add a real friction score (regulatory intensity, union %, capex cycle) as a first-class factor;
  in this run a crude ordinal version already out-explained the entire AI-exposure axis.

## Bottom line
As a labor-economics exposure map the RLFI lineage is sound. As an alpha screen it is *right and
late*: it rediscovered (a) a friction factor and (b) the builder>deployer rotation, both already
in the price. The one genuinely tradable idea is the report's own firm-level taxonomy —
**owner vs reseller** — run as within-bucket relative value, plus the friction-protected
incumbents the market has not yet paid for the productivity it's about to internalize.

*Not investment advice. Ordinal exposure/friction scores are judgmental; n per bucket is small;
single-vendor data, 1Y window — directional, not a backtest.*
