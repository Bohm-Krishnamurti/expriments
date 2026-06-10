# SPEC — C2: Burden-proxy divergence on the tau2-bench frontier ladder

Pre-registered 2026-06-10, before any data download for this experiment. (A scout sampled
one S3 trajectory file on 2026-06-09 to verify schema; its contents were not analyzed.)
Grounding: experiments/AGENDA.md sections I.4, III (pass@k row), VI (behavioral proxies),
XI. This experiment builds an agent-observable PREDICTOR of delegation burden. It does not
measure human governance effort, DBR, HSS, or SL.

## Falsifiable predictions

H1 (divergence). For frontier models, a task-level burden proxy B and task-level headline
failure (1 - pass^1) are imperfectly aligned: Spearman rho_m between B and (1 - pass^1)
across tasks is below 0.7 for every submission in the top quartile of the capability ladder.
Falsified if any top-quartile submission has rho_m >= 0.7... CORRECTION (fixed before data):
falsified if the MEDIAN top-quartile rho_m >= 0.7 (single-submission noise should not decide;
median rule frozen here).

H2 (persistence). Divergence does not close as capability rises: the Spearman correlation
between ladder rank (better models = higher rank) and rho_m is not significantly positive at
one-sided alpha = 0.05. Falsified if significantly positive (divergence closing).

H3 (verification-type failure share). Among failed trials on the solvable subset, define a
verification-type failure as: database state check passed but natural-language or
communication checks failed (output plausible, intent unmet). H3 supported if the point
estimate of the Spearman correlation between ladder rank and verification-type failure share
is >= 0; reported as unsupported if negative and significantly so at one-sided alpha = 0.05;
"weak/inconclusive" otherwise.

## Data (verified accessible 2026-06-09)

Primary: leaderboard-era 4-trial trajectory files on the public S3 bucket
sierra-tau-bench-public.s3.amazonaws.com (listable, no auth), all submissions with 4-trial
files for airline and retail (telecom included if present for >= 10 submissions). Excluded:
in-repo paper-era results in tau2-bench data/tau2/results/final/ (predate the v1.0.0 task
fixes; do not pool). Exclusion rule: drop submissions missing trials or covering < 90% of a
domain's tasks; log every exclusion in STEPLOG.md.

## Variables (frozen)

Per task t, submission m, trials k = 1..4, from trajectory records only:
- p_hat = (number of trials with reward == 1) / 4; pass^1 = p_hat; flakiness F = p_hat(1 - p_hat).
- effort E = log(1 + mean assistant-role message count per trial).
- retries R = mean hallucination_retries_used, included only if the field is present for
  >= 90% of included submissions; otherwise dropped (decision recorded in STEPLOG.md).
- Burden proxy B(t, m) = mean of z-scores (standardized across tasks within submission) of
  the included components.
- Verification-type failure indicator per failed trial from reward_info: db_check pass AND
  (nl_assertions fail OR communicate_checks fail). Trials lacking these fields are excluded
  from H3 and counted in STEPLOG.md.

Ladder: submissions ordered by mean pass^1 across included domains on the solvable subset.

## Solvable subset (degenerate-baseline obligation)

Published floors (ABC paper, arXiv:2507.02825, fetched and quoted 2026-06-09): do-nothing
agent passes 38% airline / 6.0% retail "for any k"; output-everything agent 40% / 9.6%.
A proxy a do-nothing agent satisfies is not measuring delegation, so the primary analysis
runs on the solvable subset: tasks a do-nothing policy does NOT pass. Operationalization
decision tree, frozen; the runner records which branch fired BEFORE computing any statistic:
1. If tau2 task definitions carry an explicit unsolvable/impossible annotation, use it.
2. Else if gold action sets are recoverable from task definitions: a task is do-nothing-
   passable iff its gold action set contains no state-changing action and no required
   communication assertion.
3. Else if tau2's evaluator can score an empty transcript offline cheaply, compute
   do-nothing reward per task directly.
4. Else restrict the primary analysis to retail (6% contamination) and report airline as
   sensitivity only.
Additionally: the do-nothing policy's proxy signature is computed analytically (zero
flakiness, minimal turns, zero retries) and reported, demonstrating the proxy is stated net
of the degenerate floor; headline results are also reported with unsolvable tasks included,
for comparison, labelled as artifact-contaminated.

## Statistics and decision rules (frozen)

Exactly the tests in H1-H3; alpha = 0.05; permutation-based p-values (10,000 permutations)
for trend tests given small ladder N. No other test is promoted to a headline finding;
anything else is labelled exploratory. Robustness (reported, not decision-bearing): proxy
recomputed without the flakiness component, because flakiness mechanically relates to pass^1
(maximal at p_hat = 0.5).

## Primary validity threats

(1) The tau2 user is an LLM simulator: turn counts partly reflect simulator chattiness, not
task burden. (2) Flakiness-success mechanical coupling (robustness check above). (3)
Submissions confound model and scaffold. (4) Reward design itself has known artifacts (the
reason for the solvable-subset restriction). Claim language must stay inside: "the proxy
predicts / diverges"; never "burden was measured."

## What a result would let us claim

Supported H1+H2: an agent-observable burden proxy diverges from headline success on a
customer-service corpus across the frontier ladder, and the divergence persists up the
ladder; H3 locates surviving failures in verification-type checks. NOT claimable: any level
of DBR/HSS/SL; any statement about human effort; generality beyond tau2's domains/scaffolds.

## Outputs

experiments/c2-tau2-burden-proxy/: STEPLOG.md (every step, every exclusion), derived
task-by-submission CSV (committed), analysis script(s) (committed), RESULTS.md (statistics
exactly as registered + exploratory section). Raw downloads stay out of git (data/ is
gitignored); the derivation script must regenerate them from public URLs.
