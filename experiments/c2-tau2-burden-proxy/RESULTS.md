# RESULTS — C2: Burden-proxy divergence on the tau2-bench frontier ladder

Run 2026-06-10 on branch claude/optimistic-bohr-3s1rzj. Pre-registration: SPEC.md
(2026-06-10, before data download). Full provenance: STEPLOG.md. Scripts:
scripts/{list_bucket,download_trajectories,extract_table,analyze}.py. Derived data:
task_by_submission.csv (4,170 rows), ladder.csv.

Scope reminder (SPEC): this experiment evaluates an agent-observable PREDICTOR of
delegation burden built from trajectory records. The proxy predicts or diverges from
headline success; no human governance effort, DBR, HSS, or SL was measured.

## Setup as executed

- Corpus: 15 leaderboard submissions on sierra-tau-bench-public with 4-trial trajectory
  files for airline, retail, and telecom (telecom included per the >= 10-submission
  rule; all 15 carry it). 31 other entries on the bucket were excluded for missing
  trajectories, single-trial data (incl. all 8 voice submissions), banking_knowledge-only
  coverage, or being templates — every exclusion is itemized in STEPLOG.md Step 2.
- Tasks: 50 airline + 114 retail + 114 telecom = 278 per submission; task-id sets are
  identical across all 15 submissions; coverage 100%.
- Solvable subset: decision-tree branch 2 fired (no explicit unsolvable annotations
  exist; gold action sets are recoverable). A task is do-nothing-passable iff its gold
  action set contains no WRITE-classified action and no reward-bearing communication
  assertion, classified per submission from that submission's own embedded task
  definitions (task versions differ across submission eras; STEPLOG Steps 4-5).
  Result: airline 19/50 (legacy era) or 23/50 (2026 era), retail 5/114 or 6/114,
  telecom 20/114 do-nothing-passable; solvable subset 229-234 tasks per submission
  (3,474 of 4,170 rows).
- Burden proxy B = mean of within-submission z-scores of {flakiness, effort}.
  The registered retries component was DROPPED by the frozen field-coverage rule:
  hallucination_retries_used is fully present for only 4/15 submissions (26.7% < 90%).
- Ladder = mean pass^1 across the three domains on the solvable subset; N = 15;
  top quartile = 4 submissions (gpt-5-2_sierra, glm-5-think_sierra,
  claude-opus-4-5_sierra, qwen3.5-397b-a17b-think_sierra).
- Forced deviation (logged): 132 of 16,680 simulations are infrastructure_error stubs
  (reward_info null, 0 messages) and were excluded from per-task means; denominators
  use valid trials. No task lost all 4 trials.

## Registered statistics (decision rules applied verbatim)

### H1 (divergence) — SUPPORTED

Top-quartile rho_m (Spearman between B and 1 - pass^1 across solvable tasks within
submission): 0.6715 (gpt-5-2), 0.4217 (glm-5-think), 0.6156 (claude-opus-4-5),
0.5542 (qwen3.5-397b-a17b-think).

Median top-quartile rho_m = 0.5849 < 0.7 -> not falsified; H1 SUPPORTED.
(Every individual top-quartile value is also below 0.7, so H1 holds even under the
stricter pre-correction reading.)

### H2 (persistence of divergence) — FALSIFIED

Spearman correlation between ladder rank and rho_m = +0.5179; one-sided permutation
test for a positive trend (10,000 permutations, seed 20260610): p = 0.0220 < 0.05.

The trend is significantly positive: rho_m RISES with capability, i.e. the
proxy-failure divergence narrows up the ladder. By the registered decision rule, H2 is
FALSIFIED. We report this plainly: on this corpus the registered burden proxy aligns
better, not worse, with headline failure as models get stronger.

### H3 (verification-type failure share) — SUPPORTED (sign rule)

Verification-type failure = failed trial with db_check passed AND (nl_assertions
failed OR communicate_checks failed). 298 of 3,992 failed trials lacked the required
decomposition and were excluded (counted in STEPLOG Step 6); per-submission failed-trial
counts on the solvable subset range 104-466.

Spearman correlation between ladder rank and verification-type failure share = +0.2857.
The point estimate is >= 0, so H3 is SUPPORTED under the registered rule. The
registered significance check applies only to a negative trend (one-sided p = 0.8525,
not significant). Note the registered support criterion is a sign condition only; see
exploratory for the (non-significant) positive-trend p-value.

### Registered robustness: proxy without flakiness (reported, not decision-bearing)

With B = z(effort) only: median top-quartile rho_m = 0.0002; trend of rho_m in ladder
rank = -0.7536, one-sided p(positive) = 0.9998. The H2 falsification under the
registered proxy is therefore carried by the flakiness component, which is mechanically
coupled to pass^1 (validity threat 2 in the SPEC). The registered verdicts above stand
as registered; this robustness result bounds their interpretation.

### Degenerate-baseline reporting (registered obligation)

Published floors (ABC paper, arXiv:2507.02825): a do-nothing agent passes 38% airline /
6.0% retail "for any k"; an output-everything agent passes 40% / 9.6%. Our structural
branch-2 classification yields 46.0% airline / 5.3% retail on the current (v1.0.0-fixed)
task definitions — retail matches the published floor closely; airline is higher, which
is conservative (a larger excluded set; the floors were measured on the pre-fix tasks).

Analytic do-nothing proxy signature: zero flakiness, minimal turns (one assistant
message, effort = log 2 = 0.693), zero retries. Against each submission's full-task
distributions this corresponds to z_effort between -4.4 and -8.2, z_flakiness between
-0.49 and -0.93, and B between -2.68 and -4.46: the proxy assigns the do-nothing policy
the extreme low-burden end of the scale while the benchmark would award it ~38-46% of
airline headline passes. This is precisely why the primary analysis is restricted to
the solvable subset.

With unsolvable (do-nothing-passable) tasks INCLUDED (artifact-contaminated, for
comparison only): H1 median top-quartile rho_m = 0.6185 (one submission, gpt-5-2,
reaches 0.7042); H2 trend rho = +0.6179, p = 0.0066 (falsified more strongly);
H3 rho = +0.2857, p(negative) = 0.8483. Contamination inflates the apparent
proxy-failure alignment, as expected.

## Per-submission ladder (solvable subset, registered proxy)

| rank | submission | ladder pass^1 | rho_m | vtype share |
|---|---|---|---|---|
| 1 | o4-mini_openai_2024-06-20 | 0.473 | 0.2202 | 0.0279 |
| 2 | gpt-4-1-mini_openai_2024-06-20 | 0.483 | 0.2826 | 0.0907 |
| 3 | gpt-4-1_openai_2024-06-20 | 0.490 | 0.4199 | 0.0444 |
| 4 | claude-3-7-sonnet_anthropic_2024-06-20 | 0.565 | 0.4715 | 0.0214 |
| 5 | gpt-5-2-none_sierra_2026-02-26 | 0.668 | 0.6094 | 0.0465 |
| 6 | claude-sonnet-4-5_sierra_2026-02-26 | 0.702 | 0.6254 | 0.0570 |
| 7 | gemini-3-flash_sierra_2026-03-02 | 0.723 | 0.4104 | 0.0489 |
| 8 | gpt-5_sierra_2025-08-09 | 0.750 | 0.4910 | 0.0182 |
| 9 | qwen3-max_qwen_2025-10-30 | 0.766 | 0.4765 | 0.0229 |
| 10 | qwen3-max_qwen_2026-01-23 | 0.774 | 0.4030 | 0.0395 |
| 11 | gemini-3-pro_sierra_2026-03-02 | 0.793 | 0.5734 | 0.0949 |
| 12 | gpt-5-2_sierra_2026-02-26 | 0.803 | 0.6715 | 0.0560 |
| 13 | glm-5-think_sierra_2026-03-02 | 0.810 | 0.4217 | 0.0400 |
| 14 | claude-opus-4-5_sierra_2026-02-26 | 0.815 | 0.6156 | 0.0902 |
| 15 | qwen3.5-397b-a17b-think_sierra_2026-03-02 | 0.850 | 0.5542 | 0.0769 |

## What this licenses (and does not)

The registered H1+H2 conjunction did NOT survive: the proxy diverges from headline
failure at the top of the ladder (H1), but the divergence narrows significantly as
capability rises (H2 falsified) — and the robustness check shows the narrowing is
attributable to the flakiness component rather than to conversational effort. H3's
sign condition holds: the share of verification-type failures (database state correct,
natural-language or communication checks failed) does not decline up the ladder; among
surviving failures, plausible-output/intent-unmet failures persist.

Not claimable (per SPEC): any level of DBR/HSS/SL; any statement about human effort;
generality beyond tau2's domains, scaffolds, and LLM-simulated users. Submissions
confound model and scaffold; turn counts partly reflect simulator chattiness.

## Exploratory (clearly separated; nothing here is a registered finding)

- Flakiness-only proxy: top-quartile rho_m median = 0.8428; trend in ladder rank
  rho = +0.9643, one-sided p = 0.0001 (seed 20260612). Together with the effort-only
  robustness above, this decomposes the registered H2 result: flakiness converges onto
  (1 - pass^1) almost perfectly as models strengthen (mostly mechanically), while the
  effort component's alignment with failure DECLINES with capability (trend -0.7536).
  A follow-up design should pre-register the effort-style and flakiness components as
  separate proxies with separate hypotheses.
- H3 positive trend: one-sided p = 0.1433 (seed 20260613) — positive but not
  significant; H3's registered support is the sign condition only and should be read
  as weak evidence.
- Era heterogeneity: 7/50 airline task definitions and the retail reward_basis differ
  between legacy-era and 2026-era submissions (STEPLOG Step 4); gemini-3-flash_sierra
  ran on legacy-style airline definitions. Classification per submission's own
  embedded definitions absorbs this for the solvable subset, but ladder comparisons
  across eras inherit whatever difficulty shift the v1.0.0 fixes introduced.
- Limitation of the frozen branch-2 rule: all 20 telecom do-nothing-passable tasks are
  (ACTION, ENV_ASSERTION)-graded tasks with read-only gold sets; a do-nothing agent
  would actually fail their ACTION check. Their exclusion shrinks the solvable subset
  (conservative); no contaminated task is retained by this error mode.
- The retries component (hallucination_retries_used) was unavailable for 11/15
  submissions; on the 4 submissions that have it, it remains unexamined here and is
  left to a future registered design.
