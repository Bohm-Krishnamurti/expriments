# RESULTS — C5: Proxy validation against human burden-adjacent labels (AgentRewardBench)

Pre-registration: `SPEC.md` (frozen before data download). Run log: `STEPLOG.md`.
Data: McGill-NLP/agent-reward-bench (HuggingFace, ungated), downloaded 2026-06-10.
Analysis run 2026-06-10. Everything in Part A is the registered analysis, exactly as
specified; Part B is exploratory and carries no decision weight.

## Part A — Registered results

### Verdicts (registered decision rules applied verbatim)

Decision rule (from SPEC): support requires held-out AUC >= 0.70 on the primary CV AND a
margin of >= 0.05 AUC over the length-only (n_steps) baseline; labels with < 5% positives
additionally require the 95% CI to exclude 0.5 (no label triggered this clause).

| Hypothesis | Label | Proxy AUC (95% CI) | Length-only AUC | Margin | AUC >= 0.70 | Margin >= 0.05 | Verdict |
|---|---|---|---|---|---|---|---|
| **H1** | side_effect | 0.576 [0.504, 0.648] | 0.478 | +0.098 | NO | yes | **NOT SUPPORTED** |
| **H2** | suboptimal | 0.891 [0.861, 0.915] | 0.882 | +0.009 | yes | NO | **NOT SUPPORTED** |
| (no decision weight) | looping | 0.938 [0.925, 0.952] | 0.890 | +0.049 | yes | no | flagged near-tautological in SPEC; reported only |
| (secondary) | success | 0.816 [0.786, 0.848] | 0.801 | +0.015 | yes | no | secondary, non-decision |

**Registered null statement applies.** Neither H1 nor H2 passes; per the SPEC: "the proxy
has no anchor in human judgment on this corpus beyond trajectory length." Concretely, the
two failure modes are complementary: for side effects the features carry too little signal
of any kind (AUC 0.58); for sub-optimality the features predict the human label well
(AUC 0.89) but almost all of that is trajectory length — the full proxy beats a bare
n_steps logistic by only 0.009 AUC. The proxy predicts human sub-optimality judgments, but
not beyond what a step counter already predicts; it does not usefully predict human
side-effect judgments at all. (Honest-verb note: throughout, "the proxy predicts the human
label"; burden itself was never measured here — these are human judgments of trajectories.)

### Data, join, and labels

- Trajectory files: 1,302 cleaned JSONs (matches expectation), 0 fetch errors, 0
  path-vs-JSON metadata mismatches. Annotations: 1,408 rows (matches expectation) over
  1,302 unique (benchmark, task_id, model_name) keys.
- Join on (benchmark, task_id, model_name): **1,302 joined; 0 annotation keys without a
  trajectory; 0 trajectories without an annotation.** Analyzed N = 1,302 trajectories,
  451 unique task_ids, 4 benchmarks (workarena 472, webarena 398, visualwebarena 300,
  assistantbench 132), 4 models.
- Multi-annotator handling (as registered): 106 keys had 2 annotators (max 2). Majority
  label; ties resolved to the positive (burden) class — tie counts: side_effect 4,
  suboptimal 12, looping 11, success 12. "Unsure" votes (1 each for side_effect,
  optimality, success) treated as missing votes for that label only (adaptation logged in
  STEPLOG before analysis).
- Inter-annotator agreement on the 106 doubly-annotated trajectories (pooled pairwise
  percent agreement; Cohen's kappa with chance from the marginal vote distribution):
  side_effect 96.2%, kappa 0.65; suboptimal (binarized) 88.6%, kappa 0.74; looping 89.6%,
  kappa 0.77; success 88.6%, kappa 0.76.
- H2 binarization as fixed in the SPEC before seeing distributions: "4. Completely
  Optimal" = 0, any lesser grade = 1.

### Prevalences (joined sample)

| Label | n non-missing | n positive | prevalence |
|---|---|---|---|
| side_effect | 1,301 | 87 | 6.7% |
| suboptimal | 1,302 | 1,078 | 82.8% |
| looping | 1,302 | 680 | 52.2% |
| success | 1,302 | 362 | 27.8% |

No label has < 5% positives, so the registered low-prevalence CI clause was not triggered
(side_effect at 6.7% is the closest; its CI [0.504, 0.648] is reported regardless).

### Features and model (as registered)

Features (from trajectory JSON only; never annotations, never cum_reward, never model
identity): n_steps; error rate (share of actions with non-empty last_action_error); repeat
rate (1 − distinct/total action strings); max consecutive identical action strings /
n_steps; mean observation tokens per step (axtree + dom + pruned-html token counters from
summary_info; coverage 100% of joined trajectories >= 90% threshold, so kept). Features
z-scored on training folds only.

Model: L2 logistic regression, lambda from {0.01, 0.1, 1, 10} by inner grouped CV on
training folds (sklearn 1.9.0). Primary CV: 5-fold grouped by task_id; AUC is the
tie-corrected Mann-Whitney statistic on pooled out-of-fold predictions; 95% CI from a
1,000-iteration bootstrap clustered by task_id (seed 20260610; all 1,000 iterations valid
for every label).

### Baselines (mandatory per SPEC)

1. **Majority class:** AUC 0.5 by construction; majority label is "No" for side_effect
   (93.3%), "suboptimal" for optimality (82.8%), "looping" slightly positive (52.2%),
   "Unsuccessful" for success (72.2%).
2. **Length-only logistic (n_steps):** AUCs in the verdict table. This baseline is the
   decisive one: it already achieves 0.882 (suboptimal), 0.890 (looping), 0.801 (success).
3. **Analytic do-nothing note (stated, not tested, per SPEC):** a zero-step trajectory has
   no errors and no repeats, so the proxy assigns it the lowest burden score. For
   side_effect this is the correct behavior — a do-nothing agent causes no side effects.
   The corpus contains only real runs, so this is an analytic property, not an empirical
   result.

### Secondary CV: leave-one-benchmark-out (reported only, not decision-bearing)

Pooled LOBO AUCs (proxy / length-only): side_effect 0.470 / 0.420; suboptimal 0.868 /
0.874; looping 0.931 / 0.894; success 0.794 / 0.785. Per-benchmark proxy AUCs:

| Label | assistantbench | visualwebarena | webarena | workarena |
|---|---|---|---|---|
| side_effect | 0.494 | 0.442 | 0.609 | 0.572 |
| suboptimal | 0.863 | 0.865 | 0.824 | 0.982 |
| looping | 0.821 | 0.943 | 0.969 | 0.926 |
| success | 0.751 | 0.809 | 0.769 | 0.876 |

The side_effect signal does not transfer across benchmarks at all (pooled LOBO below
chance), consistent with the primary-CV failure.

## Part B — Exploratory (no decision weight)

**Model-dummies sensitivity** (registered as exploratory): adding k−1 model-identity
dummies to the proxy features changes the primary AUCs only marginally — side_effect
0.576 → 0.610, suboptimal 0.891 → 0.896, looping 0.938 → 0.940, success 0.816 → 0.824.
The verdicts would be unchanged under every registered rule. The small side_effect gain
suggests a modest model-mix component in that label, but the dominant fact remains that
no feature set examined approaches the 0.70 bar for side effects.

## Scope and limitations (from SPEC; binding on interpretation)

- The labels are human judgments of trajectories, not measurements of human effort;
  nothing here measures burden.
- Web-domain corpus only; 4 models, none frontier-2026; no generalization claims.
- Looping is near-tautological with the repeated-action features and was excluded from
  decisions for that reason (its 0.938 AUC should not be read as validation).
- Annotation overlap is thin (106 of 1,302 trajectories double-annotated); kappa for
  side_effect (0.65) is moderate, so the H1 target label itself is noisy.

## Artifacts

- `joined_table.csv` — committed feature/label table (1,302 rows).
- `scripts/extract_features.py`, `scripts/repair_features.py`, `scripts/build_table.py`,
  `scripts/analyze.py` — full pipeline; raw downloads regenerable from public URLs.
- `data/results.json`, `data/labels_meta.json` — machine-readable statistics (gitignored
  data dir; numbers above are the registered ones).
- `STEPLOG.md` — run log, including the resumed-run note and the concurrent-writer
  incident and repair (plumbing only; no feature values affected).
