# Phase 1 — Candidate experiments (SELECTION GATE)

All dataset-access claims below were verified on 2026-06-09 by actually fetching the data
(clone, curl, or sample download), not assumed from papers. Access quirks are logged in
LESSONS.md. Ranking criterion: evidential value for the delegation-cost program times
feasibility. No candidate measures human governance effort; every deliverable is a
predictor, a proxy, a map, or a simulation, and is named as such.

Verified corpus inventory (summary):
- METR eval-analysis-public (GitHub, open, no auth): run-level panel; v1-0 41,629 runs /
  170 tasks / 35 models, v1-1 24,008 runs / 228 tasks / 21 models; per run: binary +
  continuous score, human_minutes with provenance, tokens, cost, model, scaffold,
  wall-clock, fatal-error field. No transcripts. No LICENSE file despite README reference.
- HCAST public specs (METR/hcast-public + METR/public-tasks, MIT): ~60 tasks across ~21
  families with full task code and scoring functions; remainder email-gated.
- MALT (HuggingFace, GATED auto-approve; anonymous download = 401): 7,179 transcript-level
  runs, 169 tasks, ~19 models, tool calls, branching, behavior labels; NO success labels,
  NO token counts. MIT.
- tau-bench / tau2-bench (GitHub + public S3, no auth): per-trial records with full
  transcripts; tau2 in-repo paper results (4 models x 3 domains x 4 trials, per-message
  tokens and cost, reward decomposition) plus ~49 leaderboard submissions on a publicly
  listable S3 bucket covering the frontier ladder (Opus 4.5-4.7, GPT-5.x, Gemini 3, ...),
  4 trials each. MIT. Degenerate-baseline numbers are published: arXiv:2507.02825 reports
  a do-nothing agent passes 38% (airline) / 6% (retail) and an output-everything agent
  40% / 9.6%.
- TheAgentCompany/experiments (GitHub, open, no auth, ~3.7 GB): 19 agent/model submissions
  x 175 tasks; per-task checkpoint-level partial credit (position = checkpoint index) plus
  full gzipped trajectories (per-step actions, per-call token usage). One run per
  task/model, so no pass^k. No LICENSE on the experiments repo.
- HAL traces (HuggingFace agent-evals/hal_traces, open, 113 GB across 380 zips): 11
  benchmarks x ~25 models; per-task success, full LLM-call logs, tokens incl. cache, cost.
  Files Fernet-encrypted with public hardcoded password "hal1234" (PBKDF2, 480k
  iterations). No license stated.
- Epoch AI Benchmarking Hub (CC-BY 4.0): raw Inspect .eval logs on public S3; SWE-bench
  Verified covers 31 model configs on identical tasks with per-sample messages, events,
  explicit error_retries, model_usage, timing.
- SWE-bench/experiments (GitHub + public S3, no auth despite README): 139 verified-split
  submissions, per-instance resolved labels in git; trajectories in S3 with heterogeneous
  formats, generally no tokens.
- OSWorld-Verified trajectories (HuggingFace xlangai, MIT, 472 GB; use HTTP range reads):
  ~30 models x 361 tasks, per-step actions with raw reasoning, partial credit, and
  step-budget ablations (15/50/100 max steps) for the same model.
- AgentRewardBench (HuggingFace McGill-NLP, open): 1,302 trajectories, 4 models x 4 web
  benchmarks on shared tasks, WITH human expert annotations per trajectory: success, side
  effects, optimality, looping. No license stated.
- Negative findings: GAIA gated and tasks-only; TRAIL gated (401 without HF token);
  WebArena original and AgentBench release no usable multi-model eval trajectories.

---

## C2. Burden-proxy divergence on the tau2-bench frontier ladder  [RANK 1]

Falsifiable prediction: a delegation-burden proxy built from agent-observable signals
(cross-trial flakiness from pass^k at k=1..4, turn counts, per-trial token cost,
hallucination_retries_used, and which reward component failed: db_check vs action_checks vs
nl_assertions) orders tasks differently from headline pass^1, and the divergence does not
close as capability rises. If proxy and headline orderings converge to rank correlation
> 0.9 at the top of the ladder, the program's "headline success hides surviving burden"
claim is wrong on this corpus.

Dataset, verified: sierra-research/tau2-bench in-repo results (data/tau2/results/final/,
577 MB, 26 files) plus the public S3 leaderboard bucket
(sierra-tau-bench-public.s3.amazonaws.com, listable without credentials, ~49 submissions,
4 trials per task, per-message usage). Fetched and schema confirmed this session.

Analysis and decision rule (to be frozen in SPEC.md before data touch): per model, compute
task-level proxy and task-level pass^1; statistic = Spearman rank correlation between proxy
and (1 - pass^1) across tasks, and the trend of that correlation across the capability
ladder (ladder ordered by overall pass^1). Pre-registered decision: the program's claim is
supported if proxy-vs-headline rank correlation stays below 0.7 for the top quartile of the
ladder AND the share of failures attributable to verification-type checks (nl_assertions,
communicate_checks) does not decline monotonically up the ladder.

Degenerate baselines: published do-nothing (38%/6%) and output-everything (40%/9.6%)
numbers from arXiv:2507.02825 give the floor; additionally compute the proxy's value ON
those degenerate policies analytically (a do-nothing agent has zero retries and zero
flakiness, so the proxy must NOT rank do-nothing as low-burden on tasks it "passes" — the
proxy must be reported net of this artifact, e.g. by restricting to tasks where the
do-nothing reward is 0, the solvable subset).

Primary validity threat: tau2's user is an LLM simulator, so turn counts partly reflect
simulator chattiness, not task burden; and the in-repo paper trajectories predate the v1.0
task fixes (75+ task changes), so paper-era and leaderboard-era records must not be pooled.
Mitigation: leaderboard-era S3 data only for the ladder analysis.

Would let me CLAIM: an agent-observable burden proxy diverges from headline success on a
customer-service agent corpus across the frontier ladder, and the divergence locates where
verification-type failures concentrate. Would NOT let me claim: anything about human
supervision effort, DBR, HSS, or SL levels; the proxy is a predictor, unvalidated against
human-effort data.

Feasibility: high. No auth, schemas confirmed, ~1-2 GB of targeted downloads, pure
secondary analysis. Est. 1-2 days of compute-light work.

## C1. IDI construct validation on the METR task corpus  [RANK 2]

Falsifiable prediction: an IDI scored by LLM judges from task specs alone (dimensions per
the agenda: context specificity, verifiability, failure externality, etc.) predicts
task-level agent reliability in METR's run panel BEYOND log human_minutes (the
time-horizon variable). If IDI adds no incremental signal over task length, IDI as a
structural predictor is not supported on this corpus.

Dataset, verified: METR/hcast-public + METR/public-tasks give full task specs and scoring
code for ~60 public tasks; METR/eval-analysis-public runs.jsonl gives per-task per-model
success, human_minutes, tokens. Join is on task_id/task_family; join coverage must be
confirmed in SPEC.md before registration (the public-spec subset may not all appear in the
run panel — this is the candidate's main unknown).

Analysis and decision rule: 3+ LLM judges score each public task spec on each IDI
dimension; report inter-judge reliability (Krippendorff's alpha per dimension; dimensions
below a pre-set alpha, e.g. 0.5, are dropped before the predictive test). Statistic:
partial Spearman correlation of composite IDI with task-level mean success (per model
tier), controlling log human_minutes; pre-registered threshold on coefficient and a
permutation p-value. Degenerate baseline: a "spec length + family dummy" regressor — IDI
must beat surface features of the spec, not just exist.

Primary validity threat: judge contamination (METR tasks are publicly discussed; judges
may recognize tasks and recall published difficulty) and judge monoculture (only Claude
judges are available in this environment without extra API keys, so "inter-judge
reliability across model judges" shrinks to across Claude variants unless the user
supplies an OpenAI/Google key). Both must be stated in the claim language.

Would let me CLAIM: IDI dimensions are scoreable from task structure with stated
reliability, and the index predicts (or fails to predict) where agents fail beyond task
length, on ~60 tasks. Would NOT let me claim: that IDI predicts human governance burden;
the criterion variable here is agent reliability, not human effort.

Feasibility: medium-high. Data open; the binding constraints are join coverage (N may be
~30-60 tasks, so power is limited) and judge diversity. Est. 2-3 days.

## C5. Proxy validation against human burden-adjacent labels (AgentRewardBench)  [RANK 3]

Falsifiable prediction: agent-observable signals (n_steps, repeated-action/looping
patterns, last_action_error counts, token counts per step) predict the EXISTING human
expert annotations of trajectory looping, side effects, and sub-optimality. If AUC fails
the pre-set threshold, the burden proxy has no anchor in human judgment on this corpus.

Dataset, verified: McGill-NLP/agent-reward-bench on HuggingFace, ungated; 1,302 cleaned
trajectories (4 models x WebArena/VisualWebArena/WorkArena/AssistantBench) plus
annotations.csv with 1,408 human-labeled rows (trajectory_success, side_effect,
optimality, looping). Sample fetched, schema confirmed.

Analysis and decision rule: pre-registered logistic model / AUC per label, trained and
evaluated with task-family-level cross-validation to prevent leakage; decision threshold
on held-out AUC (e.g. 0.70) fixed in SPEC.md. Degenerate baselines: predict-majority-class
and a trajectory-length-only classifier; the proxy must beat length alone, otherwise it is
a step counter.

Primary validity threat: these are human judgments OF trajectories, not measurements of
human effort, and the annotation set is small and web-domain-only; also looping labels are
near-definitionally related to repeated-action features (risk of validating a tautology —
the side_effect and optimality labels are the non-circular targets and must be reported
separately).

Would let me CLAIM: the burden proxy's components predict human judgments of
burden-adjacent trajectory failures (side effects, sub-optimality) out of sample on web
agents. This is the strongest construct-validity anchor available without collecting human
data. Would NOT let me claim: human effort measurement; generalization beyond web tasks.

Feasibility: high. Small download, no auth. Est. 1 day. Pairs naturally with C2 (same
proxy, second corpus, human-label criterion).

## C7. Effort-signature divergence on the Epoch SWE-bench Verified ladder  [RANK 4]

Falsifiable prediction: across 31 model configs on identical SWE-bench Verified tasks, the
"effort signature" (error_retries, working_time, token usage conditional on resolution
outcome) per task diverges from the resolution-rate ordering, and tasks that stay
expensive-conditional-on-success up the ladder are predicted by task descriptors. If
effort collapses onto success rate at the top of the ladder, surviving-burden structure is
absent here.

Dataset, verified: Epoch AI Benchmarking Hub, CC-BY 4.0; raw Inspect .eval logs on public
S3 (URLs in the Logs column of the CSV bundle at epoch.ai/data/benchmark_data.zip); sample
.eval opened, per-sample schema confirmed (messages, events, error_retries, model_usage,
total_time, scores). 31 SWE-bench Verified model configs.

Analysis and decision rule: per task x model, extract retries, tokens, time; statistic =
rank correlation of task-level mean effort-conditional-on-success with task-level
resolution rate, and its trend up the ladder; thresholds frozen in SPEC.md. Degenerate
baseline: SWE-bench has known weak-test artifacts (resolved label can overstate success);
report results both on all tasks and excluding tasks flagged by the ABC paper
(arXiv:2507.02825) as having inadequate tests, if that flag list is recoverable.

Primary validity threat: scaffold heterogeneity — Epoch's runs use one harness, which aids
comparability, but conclusions then attach to that scaffold; token/time also reflect
provider serving speed, not burden. Licensing is the cleanest of all candidates (CC-BY).

Would let me CLAIM: on identical software tasks under one harness, effort signatures
diverge (or not) from success across the ladder. Would NOT: human effort; cross-scaffold
generality. Feasibility: high but data-heavy (each .eval is ~65 MB; 31 configs x ~500
tasks). Est. 2 days.

## C3. Failure-position dynamics in TheAgentCompany checkpoints  [RANK 5]

Falsifiable prediction: as model capability rises across the 19 submissions, the first
failed checkpoint moves later in task structure (failures migrate from early execution to
late verification/integration stages), so remediation exposure per failure RISES over part
of the ladder even as failure rate falls. A flat or random failure-position distribution
across the ladder falsifies the burden-concentration map.

Dataset, verified: TheAgentCompany/experiments (GitHub, ~3.7 GB), 19 submissions x 175
tasks, checkpoint-level results (position = array index, partial credit) plus full
trajectories with per-step actions and per-call tokens. Sample fetched, schema confirmed.
One run per task/model; no trial replication.

Analysis and decision rule: ordinal regression of first-failed-checkpoint index (normalized
by checkpoint count) on overall submission score; pre-registered sign and significance
threshold. Degenerate baselines: this is the weak point — checkpoint rubrics may award
points for trivial initial states, and the evaluator is encrypted (key is public:
'theagentcompany is all you need') but scoring a do-nothing trajectory requires standing
up the full service stack (GitLab, ownCloud, RocketChat...), which is heavy. Fallback
degenerate test: compute what share of checkpoints are earned at trajectory step 0 or with
zero tool calls in the released runs, an observational lower bound on rubric slack; if the
full do-nothing run is infeasible, the SPEC must say the degenerate test is partial.

Primary validity threat: one run per cell (no within-task variance), submissions differ in
scaffold AND model simultaneously, and checkpoint granularity varies by task. Claims must
be about position distributions, not rates.

Would let me CLAIM: a map of where in multi-stage office tasks failures concentrate and
how the position shifts with capability. Would NOT: pass^k-style reliability, human
effort. Feasibility: medium (data open and confirmed; the degenerate-baseline obligation
is only partially dischargeable). Est. 2-3 days.

## C4. Wasted-work curve on the METR run panel  [RANK 6]

Falsifiable prediction: the share of total agent token spend incurred on runs that end in
failure ("wasted work", a remediation-exposure proxy) declines more slowly than failure
rate across the model ladder, i.e. failures get individually more expensive as they get
rarer. Proportional decline falsifies.

Dataset, verified: eval-analysis-public runs.jsonl v1-1 (24,008 runs with tokens_count,
score_binarized, model, human_minutes; fatal_error_from lets us exclude infra failures —
997 usageLimits runs must be excluded or sensitivity-tested).

Analysis and decision rule: per model, wasted-token share vs failure rate; statistic =
slope in log-log space against the ladder, threshold pre-set. Degenerate baseline: a
constant-cost-per-run null (if all runs cost the same, wasted share = failure rate
mechanically; the test is against that null). Threat: token counts conflate reasoning
styles across model families; scaffold differences (1-0 vs 1-1 vintages must not be
pooled). Claims: about agent-side waste structure only. Feasibility: very high (single
open JSONL, est. half a day) — but evidential value is moderate, since it uses no
within-task failure structure. Natural add-on to C1 on the same corpus.

## C8. Adoption-model simulation under threshold heterogeneity  [RANK 7]

Falsifiable prediction (internal to the model): under the T1 threshold structure (see
THEORY_CANDIDATES.md), heterogeneity in task-level IDI generates an adoption curve whose
shape (long upper tail of non-delegated work) differs qualitatively from a homogeneous
capability-only model; calibrating the capability axis to METR's measured time-horizon
distribution makes the difference quantitative.

Dataset: none — this is simulation, labelled as such throughout; the only empirical input
is the published METR time-horizon distribution (open, verified above). Decision rule:
pre-registered qualitative signature (which moments distinguish the two models).

Threat: a simulation cannot support empirical claims; its value is generating testable
signatures for C2/C7 and figures for the paper. CLAIM verbs restricted to "the simulation
shows". Feasibility: very high. Est. 1 day. Ranked low on evidential value by design.

## C6. MALT behavior-label and self-correction analysis  [RANK 8 — BLOCKED]

Falsifiable prediction: burden-relevant behavior rates (gives_up, hardcoded_solution,
bypass_constraints, refusals) and branching/self-correction counts do not decline
proportionally with capability across MALT's ~19 models.

Dataset, verified: metr-evals/malt-public on HuggingFace — GATED (auto-approve): file
listing works anonymously but data download returns 401. Needs a (free) HuggingFace
account token from you. Also verified: MALT records contain NO success labels and NO token
counts, and MALT run_ids do not join to eval-analysis-public run_ids, so the original
"divergence from headline success rate in MALT" design is NOT executable as stated — the
outcome variable would have to be behavior labels, not success. This is why the family-2
design moved to tau2 (C2).

Feasibility: blocked on an HF token; analysis itself is medium effort (~4 GB download,
transcript parsing). Ranked last until unblocked.

---

## Ranked list (evidential value x feasibility)

1. C2 tau2-bench burden-proxy divergence (frontier ladder, per-trial, free, published degenerate baselines)
2. C1 IDI construct validation on METR tasks (validates the program's own index; N-limited)
3. C5 AgentRewardBench human-label anchor (only human burden-adjacent labels available anywhere)
4. C7 Epoch SWE-bench effort signatures (cleanest license and ladder; data-heavy)
5. C3 TheAgentCompany failure positions (unique checkpoint structure; degenerate test only partial)
6. C4 METR wasted-work curve (cheap add-on to C1)
7. C8 adoption simulation (paper input, not evidence)
8. C6 MALT behaviors (blocked on HF token; original design not executable as specified)

Suggested portfolio if you want one anchor + one validator: C2 + C5 (same proxy, two
corpora, one with human labels), with C1 as the IDI-specific companion and C4 as a cheap
add-on. Selection is yours.
