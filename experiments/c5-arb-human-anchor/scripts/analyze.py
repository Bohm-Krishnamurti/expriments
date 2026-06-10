#!/usr/bin/env python3
"""C5 step 3: the registered analysis, exactly as in SPEC.md.

Model: L2 logistic regression; lambda from {0.01, 0.1, 1, 10} by inner CV (grouped by
task_id) on training folds; features z-scored using training-fold statistics only.
Primary CV: 5-fold grouped by task_id. Secondary (reported only): leave-one-benchmark-out.
AUC = Mann-Whitney on pooled out-of-fold predictions; 95% CI by 1,000-iteration bootstrap
clustered by task_id. Baselines: majority class; length-only (n_steps) logistic.
Exploratory: + model-identity dummies (sensitivity only).
Outputs data/results.json.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SEED = 20260610
LAMBDAS = [0.01, 0.1, 1, 10]  # sklearn C = 1/lambda
LABELS = ["side_effect", "suboptimal", "looping", "success"]


def auc_mann_whitney(y, s):
    """AUC as the Mann-Whitney statistic (tie-corrected via midranks)."""
    y = np.asarray(y, dtype=float)
    s = np.asarray(s, dtype=float)
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def zscore_fit(X):
    mu = X.mean(axis=0)
    sd = X.std(axis=0, ddof=0)
    sd = np.where(sd == 0, 1.0, sd)
    return mu, sd


def inner_select_lambda(X, y, groups, rng):
    """Pick lambda from the fixed grid by grouped inner CV (pooled inner-OOF AUC)."""
    n_grp = len(np.unique(groups))
    k = min(5, n_grp)
    if k < 2 or len(np.unique(y)) < 2:
        return 1.0
    best, best_auc = LAMBDAS[0], -np.inf
    for lam in LAMBDAS:
        oof = np.full(len(y), np.nan)
        for tr, te in GroupKFold(n_splits=k).split(X, y, groups):
            if len(np.unique(y[tr])) < 2:
                continue
            mu, sd = zscore_fit(X[tr])
            m = LogisticRegression(penalty="l2", C=1.0 / lam, solver="lbfgs",
                                   max_iter=2000)
            m.fit((X[tr] - mu) / sd, y[tr])
            oof[te] = m.predict_proba((X[te] - mu) / sd)[:, 1]
        ok = ~np.isnan(oof)
        a = auc_mann_whitney(y[ok], oof[ok]) if ok.any() else float("nan")
        if not np.isnan(a) and a > best_auc:
            best_auc, best = a, lam
    return best


def cv_oof(X, y, groups, splits, rng):
    """Out-of-fold predictions for a list of (train_idx, test_idx) splits."""
    oof = np.full(len(y), np.nan)
    lams = []
    for tr, te in splits:
        lam = inner_select_lambda(X[tr], y[tr], groups[tr], rng)
        lams.append(lam)
        mu, sd = zscore_fit(X[tr])
        m = LogisticRegression(penalty="l2", C=1.0 / lam, solver="lbfgs", max_iter=2000)
        m.fit((X[tr] - mu) / sd, y[tr])
        oof[te] = m.predict_proba((X[te] - mu) / sd)[:, 1]
    return oof, lams


def boot_ci(y, s, groups, n_boot=1000, seed=SEED):
    """95% percentile bootstrap CI for AUC, resampling task_id clusters."""
    rng = np.random.default_rng(seed)
    ug = np.unique(groups)
    idx_by_g = {g: np.where(groups == g)[0] for g in ug}
    aucs = []
    for _ in range(n_boot):
        gs = rng.choice(ug, size=len(ug), replace=True)
        idx = np.concatenate([idx_by_g[g] for g in gs])
        a = auc_mann_whitney(y[idx], s[idx])
        if not np.isnan(a):
            aucs.append(a)
    return [float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))], len(aucs)


def run_label(df, label, feat_cols, meta):
    d = df[df[label].notna()].reset_index(drop=True)
    y = d[label].astype(int).values
    groups = d["task_id"].values
    res = {"n": int(len(d)), "n_pos": int(y.sum()), "prevalence": float(y.mean())}
    rng = np.random.default_rng(SEED)

    specs = {"proxy": feat_cols, "length_only": ["n_steps"]}
    # exploratory model-dummies sensitivity
    dummy_cols = [c for c in d.columns if c.startswith("model_dummy_")]
    specs["proxy_plus_model_dummies_EXPLORATORY"] = feat_cols + dummy_cols

    primary = list(GroupKFold(n_splits=5).split(d, y, groups))
    benches = sorted(d["benchmark"].unique())
    lobo = [(np.where(d["benchmark"] != b)[0], np.where(d["benchmark"] == b)[0])
            for b in benches]

    for name, cols in specs.items():
        X = d[cols].astype(float).values
        oof, lams = cv_oof(X, y, groups, primary, rng)
        auc = auc_mann_whitney(y, oof)
        ci, n_eff = boot_ci(y, oof, groups)
        entry = {"auc_primary": auc, "ci95": ci, "boot_iters_valid": n_eff,
                 "lambdas_chosen": lams}
        # secondary: leave-one-benchmark-out (reported only)
        oof2, _ = cv_oof(X, y, groups, lobo, rng)
        entry["auc_lobo_pooled"] = auc_mann_whitney(y, oof2)
        entry["auc_lobo_per_benchmark"] = {
            b: auc_mann_whitney(y[d["benchmark"] == b], oof2[d["benchmark"] == b])
            for b in benches}
        res[name] = entry

    res["majority_class"] = {"auc": 0.5, "majority_label": int(y.mean() >= 0.5)}
    res["margin_over_length_only"] = (res["proxy"]["auc_primary"]
                                      - res["length_only"]["auc_primary"])
    # registered decision rule
    low_prev = res["prevalence"] < 0.05
    passes = (res["proxy"]["auc_primary"] >= 0.70
              and res["margin_over_length_only"] >= 0.05)
    if low_prev:
        passes = passes and (res["proxy"]["ci95"][0] > 0.5 or res["proxy"]["ci95"][1] < 0.5)
    res["low_prevalence_rule_applies"] = bool(low_prev)
    res["decision_rule_passes"] = bool(passes)
    return res


def main():
    df = pd.read_csv(os.path.join(ROOT, "joined_table.csv"))
    meta = json.load(open(os.path.join(ROOT, "data", "labels_meta.json")))

    feat_cols = ["n_steps", "error_rate", "repeat_rate", "max_consec_norm"]
    if meta["obs_tokens_feature_kept"]:
        feat_cols.append("obs_tokens_per_step")
        df = df[df["obs_tokens_present"] == 1].reset_index(drop=True)

    # exploratory model dummies (k-1 coding)
    models = sorted(df["model_name"].unique())
    for m in models[1:]:
        df[f"model_dummy_{m}"] = (df["model_name"] == m).astype(int)

    out = {"feat_cols": feat_cols,
           "n_joined_analyzed": int(len(df)),
           "n_unique_tasks": int(df["task_id"].nunique()),
           "labels": {}}
    for label in LABELS:
        print("running", label, flush=True)
        out["labels"][label] = run_label(df, label, feat_cols, meta)

    with open(os.path.join(ROOT, "data", "results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in
                          ("prevalence", "margin_over_length_only", "decision_rule_passes")}
                      for k, v in out["labels"].items()}, indent=2))


if __name__ == "__main__":
    main()
