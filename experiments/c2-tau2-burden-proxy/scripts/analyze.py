#!/usr/bin/env python3
"""C2 registered analysis (SPEC.md, 'Statistics and decision rules (frozen)').

Inputs: task_by_submission.csv, data/extract_log.json
Outputs: ladder.csv (per-submission registered quantities) and printed statistics
consumed verbatim by RESULTS.md.

Registered statistics:
  H1: median rho_m over the top quartile of the capability ladder, vs 0.7.
  H2: Spearman trend of rho_m in ladder rank; one-sided permutation test
      (10,000 perms, alpha 0.05) for POSITIVE trend. H2 supported if not
      significantly positive.
  H3: Spearman trend of verification-type failure share in ladder rank;
      supported if point estimate >= 0; unsupported if negative and significant
      (one-sided permutation test for negative trend); weak/inconclusive otherwise.
Robustness (registered, not decision-bearing): proxy without flakiness.
Degenerate baseline: analytic do-nothing proxy signature; results with
unsolvable (do-nothing-passable) tasks included, labelled artifact-contaminated.

Proxy components after the field-coverage decision (extract_log.json:
hallucination_retries_used present for 4/15 = 26.7% < 90% -> retries DROPPED):
  B(t, m) = mean of z-scores of {flakiness, effort}, standardized across tasks
  within submission over the analysis task set.
"""
import json, os, sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "..", "task_by_submission.csv")
LOG = os.path.join(HERE, "..", "data", "extract_log.json")
OUT = os.path.join(HERE, "..", "ladder.csv")

N_PERMS = 10_000
SEED = 20260610
DOMAINS = ["airline", "retail", "telecom"]

def zscore(x):
    x = np.asarray(x, dtype=float)
    sd = x.std(ddof=0)
    if sd == 0:
        return np.zeros_like(x)
    return (x - x.mean()) / sd

def proxy_B(g, components):
    zs = [zscore(g[c].values) for c in components]
    return np.mean(zs, axis=0)

def per_submission(df, components):
    """Per submission: ladder score (mean over domains of mean pass^1),
    rho_m = Spearman(B, 1-pass^1) across pooled tasks, verification share."""
    recs = []
    for sub, g in df.groupby("submission"):
        dom_pass = g.groupby("domain")["p_hat"].mean()
        ladder = float(np.mean([dom_pass[d] for d in DOMAINS]))
        B = proxy_B(g, components)
        rho, _ = spearmanr(B, 1.0 - g["p_hat"].values)
        n_fail_eval = (g["n_failed"] - g["n_failed_h3_excluded"]).sum()
        vshare = g["n_failed_vtype"].sum() / n_fail_eval if n_fail_eval > 0 else np.nan
        recs.append({"submission": sub, "ladder_score": ladder,
                     "rho_m": float(rho), "n_tasks": len(g),
                     "n_failed_trials_h3": int(n_fail_eval),
                     "vtype_share": float(vshare)})
    out = pd.DataFrame(recs).sort_values("ladder_score").reset_index(drop=True)
    out["ladder_rank"] = np.arange(1, len(out) + 1)  # higher = better
    return out

def perm_test_spearman(x, y, alternative, rng):
    """One-sided permutation p-value for Spearman rho of y against x."""
    obs, _ = spearmanr(x, y)
    y = np.asarray(y, dtype=float)
    count = 0
    for _ in range(N_PERMS):
        r, _ = spearmanr(x, rng.permutation(y))
        if alternative == "greater" and r >= obs - 1e-12:
            count += 1
        elif alternative == "less" and r <= obs + 1e-12:
            count += 1
    return float(obs), (count + 1) / (N_PERMS + 1)

def analyze(df, label, components):
    print(f"\n===== {label} | components={components} =====")
    lad = per_submission(df, components)
    n = len(lad)
    q = int(np.ceil(0.25 * n))
    top = lad.tail(q)
    med = float(top["rho_m"].median())
    print(lad.to_string(index=False))
    print(f"\nN submissions={n}; top quartile = {q} submissions: "
          f"{', '.join(top['submission'])}")
    print(f"H1: top-quartile rho_m values: {[round(v,4) for v in top['rho_m']]}")
    print(f"H1: MEDIAN top-quartile rho_m = {med:.4f}  (threshold 0.7; "
          f"falsified if >= 0.7) -> {'FALSIFIED' if med >= 0.7 else 'SUPPORTED'}")
    rng = np.random.default_rng(SEED)
    rho2, p2 = perm_test_spearman(lad["ladder_rank"], lad["rho_m"], "greater", rng)
    print(f"H2: Spearman(ladder_rank, rho_m) = {rho2:.4f}, one-sided p (positive) = "
          f"{p2:.4f} ({N_PERMS} perms) -> "
          f"{'FALSIFIED (significantly positive)' if p2 < 0.05 else 'SUPPORTED (not significantly positive)'}")
    rng = np.random.default_rng(SEED + 1)
    lad3 = lad.dropna(subset=["vtype_share"])
    rho3, p3neg = perm_test_spearman(lad3["ladder_rank"], lad3["vtype_share"], "less", rng)
    if rho3 >= 0:
        verdict3 = "SUPPORTED (point estimate >= 0)"
    elif p3neg < 0.05:
        verdict3 = "UNSUPPORTED (negative and significant)"
    else:
        verdict3 = "WEAK/INCONCLUSIVE (negative, not significant)"
    print(f"H3: Spearman(ladder_rank, vtype_share) = {rho3:.4f}, one-sided p (negative) = "
          f"{p3neg:.4f} -> {verdict3}")
    return lad

def main():
    df = pd.read_csv(CSV)
    log = json.load(open(LOG))
    cov = log["retries_coverage"]
    print(f"retries field coverage: {cov['submissions_with_full_retries_field']}/"
          f"{cov['n_submissions']} = {cov['fraction']:.3f} -> retries "
          f"{'INCLUDED' if cov['included'] else 'DROPPED'}")
    components = ["flakiness", "effort"] + (["retries_mean"] if cov["included"] else [])

    # do-nothing-passable counts per domain (modal across submissions, plus range)
    print("\nDo-nothing-passable counts per (submission, domain):")
    cnt = df.groupby(["domain", "submission"])["do_nothing_passable"].sum().unstack(0)
    print(cnt.to_string())

    solv = df[df["do_nothing_passable"] == 0].copy()
    print(f"\nSolvable-subset rows: {len(solv)} / {len(df)}")

    lad = analyze(solv, "PRIMARY: solvable subset", components)
    lad.to_csv(OUT, index=False)

    # Registered robustness: proxy without flakiness
    analyze(solv, "ROBUSTNESS: proxy without flakiness", ["effort"])

    # Degenerate-baseline comparison: all tasks (artifact-contaminated)
    analyze(df, "COMPARISON (artifact-contaminated): all tasks incl. do-nothing-passable",
            components)

    # Analytic do-nothing proxy signature (against full-task distributions)
    print("\n===== Analytic do-nothing proxy signature =====")
    full = df.groupby("submission").agg(mean_eff=("effort", "mean"),
                                        sd_eff=("effort", "std"),
                                        mean_fl=("flakiness", "mean"),
                                        sd_fl=("flakiness", "std"))
    e0 = np.log1p(1.0)  # one assistant message, zero retries, zero flakiness
    full["z_eff_do_nothing"] = (e0 - full["mean_eff"]) / full["sd_eff"]
    full["z_fl_do_nothing"] = (0.0 - full["mean_fl"]) / full["sd_fl"]
    full["B_do_nothing"] = (full["z_eff_do_nothing"] + full["z_fl_do_nothing"]) / 2
    print(full.round(3).to_string())

if __name__ == "__main__":
    main()
