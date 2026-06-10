#!/usr/bin/env python3
"""C5 step 2: aggregate annotations (majority, ties->positive), agreement stats, join to
trajectory features. Outputs:
  - joined_table.csv (experiment root; committed — it is small)
  - data/labels_meta.json (tie counts, agreement, join diagnostics for RESULTS.md)
"""
import json
import os
from itertools import combinations

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")

KEY = ["benchmark", "task_id", "model_name"]
LABELS = ["side_effect", "suboptimal", "looping", "success"]


def code_labels(a):
    """Map raw annotation strings to {0,1,NaN}. Positive = burden class.

    side_effect: Yes=1, No=0, Unsure=NaN
    suboptimal (H2 binarization, fixed in SPEC before seeing distributions):
        '4. Completely Optimal' = 0, any lesser grade = 1, Unsure=NaN
    looping: Yes=1, No=0
    success: Successful=1, Unsuccessful=0, Unsure=NaN (secondary outcome; positive=success)
    """
    out = pd.DataFrame(index=a.index)
    yn = {"Yes": 1.0, "No": 0.0, "Unsure": np.nan}
    out["side_effect"] = a["trajectory_side_effect"].str.strip().map(yn)
    opt = a["trajectory_optimality"].str.strip()
    out["suboptimal"] = np.where(opt == "Unsure", np.nan,
                                 (opt != "4. Completely Optimal").astype(float))
    out["looping"] = a["trajectory_looping"].str.strip().map(yn)
    out["success"] = a["trajectory_success"].str.strip().map(
        {"Successful": 1.0, "Unsuccessful": 0.0, "Unsure": np.nan})
    return out


def pooled_pairwise_agreement(df, label):
    """Percent agreement + Cohen's kappa pooled over all unordered annotator pairs that
    labeled the same trajectory (chance agreement from the marginal vote distribution
    over all votes on overlapping items)."""
    pairs = []
    votes_on_overlap = []
    for _, g in df.groupby(KEY, sort=False):
        v = g[label].dropna().values
        if len(v) >= 2:
            votes_on_overlap.extend(v)
            pairs.extend(combinations(v, 2))
    if not pairs:
        return None
    po = float(np.mean([x == y for x, y in pairs]))
    p1 = float(np.mean(votes_on_overlap))
    pe = p1 ** 2 + (1 - p1) ** 2
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    return {"n_pairs": len(pairs), "percent_agreement": po, "kappa": kappa,
            "n_overlap_votes": len(votes_on_overlap)}


def main():
    a = pd.read_csv(os.path.join(DATA, "annotations.csv"))
    a["annotator_name"] = a["annotator_name"].str.strip()
    coded = code_labels(a)
    a = pd.concat([a[["annotator_name"] + KEY], coded], axis=1)

    meta = {"n_annotation_rows": int(len(a)),
            "n_unique_keys": int(a.groupby(KEY).ngroups),
            "n_unsure_votes": {l: int(coded[l].isna().sum()) for l in LABELS}}

    # multi-annotator overlap + agreement
    sizes = a.groupby(KEY).size()
    meta["keys_with_multiple_annotators"] = int((sizes > 1).sum())
    meta["max_annotators_per_key"] = int(sizes.max())
    meta["agreement"] = {l: pooled_pairwise_agreement(a, l) for l in LABELS}

    # majority aggregation; ties -> positive
    ties = {l: 0 for l in LABELS}
    rows = []
    for key, g in a.groupby(KEY, sort=False):
        rec = dict(zip(KEY, key))
        for l in LABELS:
            v = g[l].dropna()
            if len(v) == 0:
                rec[l] = np.nan
                continue
            pos, neg = int((v == 1).sum()), int((v == 0).sum())
            if pos > neg:
                rec[l] = 1.0
            elif neg > pos:
                rec[l] = 0.0
            else:
                rec[l] = 1.0  # tie -> positive (burden) class, per SPEC
                ties[l] += 1
        rows.append(rec)
    lab = pd.DataFrame(rows)
    meta["tie_counts"] = ties

    feats = pd.read_csv(os.path.join(DATA, "trajectory_features.csv"))
    meta["n_trajectory_files"] = int(len(feats))
    meta["n_fetch_errors"] = int(feats["fetch_error"].sum())
    meta["n_path_json_mismatch"] = int(feats["path_json_mismatch"].fillna(0).sum())
    feats = feats[feats["fetch_error"] == 0].drop(columns=["fetch_error"])

    j = lab.merge(feats, on=KEY, how="outer", indicator=True)
    meta["join"] = {
        "annotations_without_trajectory": int((j["_merge"] == "left_only").sum()),
        "trajectories_without_annotation": int((j["_merge"] == "right_only").sum()),
        "joined": int((j["_merge"] == "both").sum()),
    }
    meta["unjoined_annotation_keys"] = (
        j.loc[j["_merge"] == "left_only", KEY].to_dict("records"))
    joined = j[j["_merge"] == "both"].drop(columns=["_merge"]).reset_index(drop=True)

    # obs-token coverage rule (>=90% of joined else drop)
    cov = float(joined["obs_tokens_present"].mean())
    meta["obs_tokens_coverage_joined"] = cov
    meta["obs_tokens_feature_kept"] = bool(cov >= 0.90)

    meta["prevalence_joined"] = {
        l: {"n_nonmissing": int(joined[l].notna().sum()),
            "n_pos": int((joined[l] == 1).sum()),
            "prevalence": float(joined[l].mean())} for l in LABELS}

    joined.to_csv(os.path.join(ROOT, "joined_table.csv"), index=False)
    with open(os.path.join(DATA, "labels_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2)[:4000])


if __name__ == "__main__":
    main()
