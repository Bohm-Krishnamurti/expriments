# SPEC — C5: Proxy validation against human burden-adjacent labels (AgentRewardBench)

Pre-registered 2026-06-10, before any data download for this experiment. (A scout fetched
annotations.csv and one trajectory on 2026-06-09 to verify schema; no analysis was run.)
Grounding: experiments/AGENDA.md sections III, VI (behavioral proxies; validation list).
This experiment tests whether agent-observable trajectory signals predict EXISTING human
expert annotations of burden-adjacent failures. The annotations are human judgments of
trajectories, not measurements of human effort; no new human data is collected.

## Falsifiable predictions

H1 (side effects). A logistic model on agent-observable features predicts the human
side_effect label with held-out AUC >= 0.70 on the primary cross-validation, AND beats a
length-only (n_steps) baseline by >= 0.05 AUC. Both conditions required for support.

H2 (sub-optimality). Same two conditions for the optimality label (binarized: any
sub-optimality flagged vs none; if the field is graded, the binarization rule is "fully
optimal vs anything less", fixed here before seeing label distributions).

Looping is reported with the same pipeline but flagged near-tautological (repeated-action
features quasi-define it); it carries no decision weight. trajectory_success is a secondary,
non-decision outcome.

Null statement: if neither H1 nor H2 passes, the proxy has no anchor in human judgment on
this corpus beyond trajectory length; that is a result and will be reported as such.

## Data (verified accessible 2026-06-09)

McGill-NLP/agent-reward-bench on HuggingFace, ungated: cleaned trajectory JSONs (1,302; 4
models x WebArena / VisualWebArena / WorkArena / AssistantBench) and annotations.csv (1,408
human-labeled rows: annotator, benchmark, task_id, model_name, trajectory_success,
trajectory_side_effect, trajectory_optimality, trajectory_looping). Join on (benchmark,
task_id, model_name). Rows that fail to join are counted and logged. If multiple annotators
label the same trajectory: majority label; ties resolve to the positive (burden) class and
the tie count is reported; inter-annotator agreement (percent + Cohen's kappa) reported
where overlap exists.

## Features (frozen; agent-observable only)

From trajectory JSON only — never from annotations, never from benchmark reward
(cum_reward), never from model identity:
- n_steps;
- error rate: share of steps with non-empty last_action_error;
- repeat rate: 1 - (distinct action strings / n_steps);
- max consecutive identical action strings, normalized by n_steps;
- mean observation tokens per step (from summary_info.stats), if present for >= 90% of
  joined trajectories, else dropped (logged).
Features z-scored within the training fold.

## Model and evaluation (frozen)

L2-regularized logistic regression (lambda chosen by inner CV on the training folds from a
fixed grid {0.01, 0.1, 1, 10}); if sklearn is unavailable in the environment, a hand-rolled
implementation with the same spec. Primary CV: 5-fold grouped by task_id (a task never spans
train and test). Secondary (reported, not decision-bearing): leave-one-benchmark-out.
AUC computed as the Mann-Whitney statistic; 95% CI by 1,000-iteration bootstrap clustered by
task_id. Class prevalence reported per label; if a label has < 5% positives, the AUC is
still decision-bearing but the CI must exclude 0.5 for support.

## Degenerate baselines (mandatory)

(1) Majority-class predictor (AUC 0.5 floor, prevalence reported). (2) Length-only logistic
model (n_steps) — the proxy must beat it by >= 0.05 AUC; a proxy that is a step counter in
disguise fails. (3) Analytic do-nothing note: a zero-step trajectory has no errors and no
repeats, so the proxy assigns it the lowest burden score; this is correct behavior for
side_effect (a do-nothing agent causes none) and is stated in RESULTS.md rather than
tested, since the corpus contains only real runs.

## Primary validity threats

(1) Looping-feature circularity (excluded from decisions). (2) Web-domain-only corpus; 4
models, none frontier-2026; generalization claims out of bounds. (3) Annotation quality and
sparsity per cell. (4) Model-mix confound: features may proxy model identity; sensitivity
analysis with model dummies added is reported as exploratory only.

## What a result would let us claim

Support: agent-observable burden signals predict human judgments of side effects and/or
sub-optimality out of sample on web-agent trajectories, beyond trajectory length — a
construct-validity anchor for the burden proxy. NOT claimable: human-effort measurement;
DBR/HSS/SL levels; generalization beyond web agents or to 2026 frontier models.

## Outputs

experiments/c5-arb-human-anchor/: STEPLOG.md, joined feature/label table (committed, it is
small), analysis script(s), RESULTS.md with registered statistics first and exploratory
material clearly separated. Raw downloads regenerable from public URLs; large raw files stay
out of git.
