# STEPLOG — C2: Burden-proxy divergence on the tau2-bench frontier ladder

Run date: 2026-06-10. Runner: Claude (Fable 5), branch claude/optimistic-bohr-3s1rzj.
SPEC.md, LESSONS.md, AGENDA.md read before any data work. Steps in execution order.

## Step 0 — Environment

- python3 present; pandas 3.0.3, numpy 2.4.6, scipy 1.17.1 installed via pip.
- Disk incident at run start: / reported 936K free (stale thin-provisioning reading plus
  ~13G of leftover scout scratch in /tmp). After purging the pip cache this run created,
  df settled at 16G free; no pre-existing data was deleted. One early STEPLOG/.gitignore
  write was lost to ENOSPC and rewritten; no analysis output was affected.
- tau2-bench already cloned at /tmp/tau2-bench (HEAD 1746a25, 2026-06-01,
  "Update cascaded voice display (#339)") — used read-only for task definitions.

## Step 1 — Bucket listing (anonymous S3 ListObjectsV2)

- Tool: scripts/list_bucket.py (urllib, follows NextContinuationToken).
- Result: 12,099 keys under `submissions/` (data/bucket_listing.tsv, not committed).
- Bucket-level metadata: `submissions/manifest.json` partitions submissions into
  19 `submissions`, 8 `voice_submissions`, 16 `legacy_submissions`; plus 2 A_EXAMPLE
  templates, schema.json, README. manifest.json and schema.json downloaded to data/.

## Step 2 — Submission inventory and exclusions

SPEC rule: drop submissions missing trials or covering < 90% of a domain's tasks;
primary domains airline + retail; telecom included if >= 10 submissions carry it.

Candidate set: submissions WITH per-domain multi-trial trajectory files for airline AND
retail (15):

| submission | trajectory naming | nominal trials |
|---|---|---|
| claude-3-7-sonnet_anthropic_2024-06-20 | *_4trials.json | 4 |
| claude-opus-4-5_sierra_2026-02-26 | *_4trials.json | 4 |
| claude-sonnet-4-5_sierra_2026-02-26 | *_4trials.json | 4 |
| gemini-3-flash_sierra_2026-03-02 | geminiflash-(domain).json | verified in Step 4 |
| gemini-3-pro_sierra_2026-03-02 | geminipro-(domain).json | verified in Step 4 |
| glm-5-think_sierra_2026-03-02 | *_4trials.json | 4 |
| gpt-4-1-mini_openai_2024-06-20 | *_4trials.json | 4 |
| gpt-4-1_openai_2024-06-20 | *_4trials.json | 4 |
| gpt-5-2-none_sierra_2026-02-26 | *_4trials.json | 4 |
| gpt-5-2_sierra_2026-02-26 | *_4trials.json | 4 |
| gpt-5_sierra_2025-08-09 | *_4trials.json | 4 |
| o4-mini_openai_2024-06-20 | *_4trials.json | 4 |
| qwen3-max_qwen_2025-10-30 | (domain)_llm_agent_*.json | verified in Step 4 |
| qwen3-max_qwen_2026-01-23 | (domain)_llm_agent_*.json | verified in Step 4 |
| qwen3.5-397b-a17b-think_sierra_2026-03-02 | *_4trials.json | 4 |

EXCLUSIONS (every excluded submission, with reason):

1. No trajectory files on the bucket (submission.json only) — 11 submissions:
   claude-opus-4_anthropic_2025-05-22, claude-opus-4-1_anthropic_2025-01-15,
   claude-sonnet-4_anthropic_2025-05-22, claude-sonnet-4-5_anthropic_2025-10-02,
   kimi-k2_moonshot-ai_2025-07-11, o3_openai_2025-01-15, qwen3-max_qwen_2024_09_23,
   gemini-3-pro_google_2025-11-18, deepseek-v3.2_deepseek_2025-12-01,
   distyl-buttonagent_distyl_2026-03-25, raft-30b-a3b_neu_2026-04-29.
2. Single-trial submission — toolorchestra_nvidia_2025-12-02 (*_1trial.json): fails the
   4-trial requirement (p_hat/flakiness undefined as registered at k=1).
3. Voice submissions (8): gpt-realtime-1.5_sierra_2026-03-03,
   gemini-live-2.5-flash_sierra_2026-03-03, xai-realtime_sierra_2026-03-03,
   grok-voice-think-fast-1-0_xai_2026-04-21,
   gemini-3-1-flash-live-preview-thinking-high_google_2026-04-02,
   gemini-3-1-flash-live-preview-thinking-minimal_google_2026-04-13,
   gpt-realtime-1-0_openai_2026-04-13, livekit-cascaded_livekit_2026-05-19.
   Reason: per-domain simulation counts are exactly 50 airline / 114 retail / 114
   telecom = 1 simulation per task, i.e. single-trial; fails the 4-trial requirement.
   (Also a different modality — would confound the ladder.)
4. banking_knowledge-only submissions (no airline or retail trajectories) — 9:
   claude-opus-4-6_sierra_2026-05-05, claude-opus-4-7_sierra_2026-05-05,
   gemini-2-5-pro_sierra_2026-05-05, gemini-3-1-pro-preview_sierra_2026-05-05,
   gpt-5-4_sierra_2026-03-25, gpt-5-5_sierra_2026-05-05, grok-4-fast_sierra_2026-05-05,
   grok-4-1-fast_sierra_2026-05-05, grok-4-2_sierra_2026-05-05.
5. A_EXAMPLE_new-model, A_EXAMPLE_voice-model: documentation templates, not submissions.

Domain-variant handling (frozen before download): gpt-4-1_openai also ships
telecom_no-user-op (ablation) — only telecom_default used. o4-mini_openai also ships
telecom-workflow_no-user-op — only telecom_default used. gemini-3-flash/pro_sierra also
ship a `terminal` domain and several submissions ship banking_knowledge — both outside
the registered domain set (airline/retail/telecom), ignored.

Telecom decision: all 15 candidates carry telecom trajectories (>= 10 threshold), so
telecom is INCLUDED. Registered domain set for this run: {airline, retail, telecom}.

In-repo paper-era results (tau2-bench data/tau2/results/final/) NOT used anywhere, per
SPEC and LESSONS (pre-v1.0.0 task fixes; do not pool).

## Step 3 — Download

- scripts/download_trajectories.py: 45/45 files (15 submissions x 3 domains) downloaded
  anonymously from the bucket into data/raw/ (gitignored). 0 failures, ~1.1 GB.
- Verified per file: num_trials=4; airline 50 tasks x 4 = 200 sims; retail 114 x 4 = 456;
  telecom 114 x 4 = 456. Task-id sets identical across all 15 submissions in every domain;
  coverage 100% (>= 90% rule passed for all submissions; no coverage exclusions).
- Trial-count verification resolves the Step-2 "to verify" rows: gemini-3-flash_sierra,
  gemini-3-pro_sierra, qwen3-max_qwen_2025-10-30, qwen3-max_qwen_2026-01-23 all contain
  4 trials per task.

## Step 4 — Task-definition era check (before any statistic)

Embedded task definitions (each trajectory file carries the `tasks` array as run) were
hashed and compared across submissions and against /tmp/tau2-bench tasks.json (HEAD
1746a25):
- telecom: identical across all 15 submissions and the repo.
- airline: 7 of 50 tasks differ in decision-relevant features between the legacy-era
  submissions and the 2026 sierra-era submissions/repo (newer task version removed WRITE
  actions such as send_certificate / cancel_reservation from some gold sets).
  gemini-3-flash_sierra matches the LEGACY decision features despite being a 2026
  submission.
- retail: reward_basis changed era-to-era ((COMMUNICATE, DB) -> (DB, NL_ASSERTION)),
  communicate_info content moved into nl_assertions; qwen3-max_qwen_2025-10-30 is a
  third minor variant (2 tasks).
DECISION (frozen before statistics): do-nothing-passability is classified per submission
from that submission's OWN embedded task definitions — the task as actually evaluated —
not from a single canonical task file. Logged as a data-reality adaptation; the
registered rule itself is unchanged.

## Step 5 — Solvable-subset decision tree (resolved IN ORDER, branch recorded
## BEFORE any registered statistic was computed)

1. Branch 1 (explicit unsolvable/impossible annotation): NOT AVAILABLE. airline
   tasks.json has an `annotations` field but it is null for all 50 tasks; retail and
   telecom task objects carry no annotation field; grep for
   unsolvable/impossible/infeasible over data/tau2/domains/{airline,retail,telecom}
   matches nothing task-level. Branch 1 does not fire.
2. Branch 2 (gold action sets recoverable): FIRES. Every task definition carries
   evaluation_criteria.actions (gold action set), communicate_info, nl_assertions,
   reward_basis. Tool state-changing classification taken from tau2-bench source
   (@is_tool(ToolType.WRITE) decorators in src/tau2/domains/*/tools.py and
   telecom/user_tools.py — covers both assistant- and user-side actions).
   OPERATIONALIZATION of the frozen rule "no state-changing action and no required
   communication assertion": has_write = any gold action whose tool is WRITE;
   comm_required = (communicate_info non-empty AND COMMUNICATE in reward_basis) OR
   (nl_assertions non-empty AND NL_ASSERTION in reward_basis) — "required" read as
   reward-bearing. do-nothing-passable iff NOT has_write AND NOT comm_required.
   Branches 3 and 4 not reached.
- Sanity check against published floors (computed BEFORE any registered statistic, on
  the repo tasks.json): airline 23/50 = 46.0% do-nothing-passable, retail 6/114 = 5.3%.
  ABC floors (arXiv:2507.02825): 38% airline / 6.0% retail. Retail matches closely;
  airline is higher than the published floor — the ABC numbers predate the v1.0.0 task
  fixes, and the structural rule ignores NL-judge behavior on non-reward-bearing
  assertions. Direction of any misclassification is toward a SMALLER solvable subset
  (more exclusion), i.e. conservative w.r.t. the degenerate-floor artifact.
- Known limitation of the frozen branch-2 rule, noted before computing: telecom tasks
  graded by ENV_ASSERTION / ACTION reward bases are not addressed by the rule's two
  clauses; tasks with read-only gold sets under those bases are classified
  do-nothing-passable (excluded from the solvable subset) even though the evaluator
  might fail a do-nothing agent on them. Direction: smaller solvable subset
  (conservative). Counts reported in RESULTS.md.

## Step 6 — Extraction (scripts/extract_table.py -> task_by_submission.csv)

- 4,170 rows = 15 submissions x 278 tasks (50 airline + 114 retail + 114 telecom).
- DEVIATION (data reality, logged): 132 simulations across 4 submissions terminate with
  termination_reason=infrastructure_error and carry reward_info=null and 0 messages
  (gemini-3-pro_sierra: 3 airline / 20 retail / 2 telecom; glm-5-think_sierra: 4 retail /
  52 telecom; gpt-5-2-none_sierra: 51 retail). These are harness failures, not agent
  behavior; the SPEC's "trials k = 1..4" did not contemplate them. They are excluded
  from all per-task means; p_hat, flakiness, effort use the number of VALID trials as
  denominator (n_trials column records it). No task lost all 4 trials, so no task was
  dropped. The strict reward==1-of-4 reading would count infra failures against the
  model; rejected as misattribution.
- Pass definition: reward >= 1 - 1e-9 (rewards in the data are exactly 0.0 or 1.0 for
  telecom; airline/retail likewise binary checked during extraction).
- retries (hallucination_retries_used) FIELD-COVERAGE DECISION: field fully present for
  only 4/15 submissions (gemini-3-flash, gemini-3-pro, glm-5-think, qwen3.5 — all-sierra
  2026); partially present (airline/retail yes, telecom 25%) for claude-opus-4-5,
  claude-sonnet-4-5, gpt-5-2, gpt-5-2-none; absent for the 7 legacy-schema submissions.
  Coverage 4/15 = 26.7% < 90% -> retries component DROPPED, per the frozen rule.
  Burden proxy B = mean of z-scores of {flakiness, effort}.
- H3 field check: 3,992 failed trials total (all tasks); 298 failed trials lack the
  db_check/nl/communicate decomposition (db_check null or both nl_assertions and
  communicate_checks null) -> excluded from H3 and counted here, per SPEC.

## Step 7 — Registered statistics (scripts/analyze.py)

Run AFTER Steps 4-6 were logged. Ladder = submissions ordered by mean pass^1 across the
three included domains on the solvable subset (per-domain mean of p_hat over the
submission's solvable tasks, then unweighted mean over domains). Top quartile =
ceil(0.25 * 15) = 4 highest-ranked submissions. B standardized across tasks within
submission over the analysis task set (pooled domains). Permutation tests: 10,000
permutations, seeds 20260610 (H2) and 20260611 (H3), p = (count+1)/(N+1).

## Step 8 — Registered statistics: results (verbatim from scripts/analyze.py output)

Solvable subset: 3,474 / 4,170 rows. Do-nothing-passable per submission-era task
definitions: airline 19 (legacy-era, incl. gemini-3-flash) or 23 (2026-era) of 50;
retail 5 (legacy) or 6 (2026-era) of 114; telecom 20 of 114 for all submissions.
All 20 telecom do-nothing-passable tasks are reward_basis (ACTION, ENV_ASSERTION)
tasks with non-empty read-only gold sets (the Step-5 limitation; conservative
direction — a do-nothing agent would actually fail their ACTION check, so the
solvable subset is smaller than strictly necessary, never contaminated by them).

PRIMARY (B = mean z of {flakiness, effort}, solvable subset, n_tasks 229-234/submission):
- H1: top-quartile (4 of 15) rho_m = [0.6715, 0.4217, 0.6156, 0.5542];
  median = 0.5849 < 0.7 -> H1 SUPPORTED (every individual value also < 0.7).
- H2: Spearman(ladder_rank, rho_m) = +0.5179, one-sided permutation p = 0.0220 < 0.05
  -> significantly POSITIVE -> H2 FALSIFIED (divergence narrows up the ladder).
- H3: Spearman(ladder_rank, verification-type failure share) = +0.2857 >= 0
  -> H3 SUPPORTED under the registered sign rule (one-sided p for negative trend
  0.8525; n_failed trials per submission 104-466).

ROBUSTNESS (registered, not decision-bearing; B = z(effort) only):
- H1-analogue median top-quartile rho_m = 0.0002; H2-analogue trend rho = -0.7536,
  one-sided p(positive) = 0.9998. The positive H2 trend of the registered proxy is
  carried by the flakiness component.

COMPARISON (artifact-contaminated; all 278 tasks):
- H1 median top-quartile rho_m = 0.6185 (one submission, gpt-5-2, reaches 0.7042);
- H2 trend rho = +0.6179, p = 0.0066; H3 rho = +0.2857, p(neg) = 0.8483.

DEGENERATE BASELINE (analytic): do-nothing signature = zero flakiness, minimal turns
(1 assistant message -> effort = log 2 ~= 0.693), zero retries. Against each
submission's full-task distributions this gives z_effort -4.4 to -8.2, z_flakiness
-0.49 to -0.93, B between -2.68 and -4.46: the proxy places the do-nothing policy at
the extreme low-burden end, i.e. the registered statistics are stated net of the
degenerate floor only on the solvable subset (ABC floors cited: do-nothing 38%
airline / 6.0% retail; output-everything 40% / 9.6%; arXiv:2507.02825).

## Step 9 — Exploratory (computed after all registered statistics; seeds 20260612-13)

- Flakiness-only proxy: top-quartile rho_m median = 0.8428; trend rho = +0.9643,
  one-sided p(positive) = 0.0001 — direct demonstration of the mechanical
  flakiness <-> pass^1 coupling (registered validity threat 2).
- H3 positive-trend (not registered as decision-bearing): one-sided p = 0.1433.

## Script invocations (full list)

1. scripts/list_bucket.py data/bucket_listing.tsv
2. curl manifest.json, schema.json (data/)
3. scripts/download_trajectories.py  (45/45 OK)
4. scripts/extract_table.py  -> task_by_submission.csv, data/extract_log.json
5. scripts/analyze.py  -> ladder.csv, data/analyze_output.txt (stdout also in RESULTS.md)

## Step 10 — Finalization and commit

- Reproducibility check: scripts/analyze.py re-run end-to-end; all registered
  statistics identical to the recorded values (REPRODUCED).
- Committed outputs: STEPLOG.md, RESULTS.md, .gitignore, task_by_submission.csv,
  ladder.csv, scripts/{list_bucket,download_trajectories,extract_table,analyze}.py.
  Raw downloads (data/) excluded from git; download_trajectories.py regenerates them
  from public URLs.
- Provenance note: a concurrent orchestrator session made WIP snapshot commits on this
  branch while this run was in progress (e9efc05, cead50d) and swept the final C2
  outputs into commit 75a4e10 (whose message concerns the paper). This commit (message
  "C2: ...") marks the verified final state of the C2 run; the registered verdicts are
  H1 SUPPORTED, H2 FALSIFIED, H3 SUPPORTED (sign rule), as recorded in Step 8 and
  RESULTS.md.
