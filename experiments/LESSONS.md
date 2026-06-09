# LESSONS.md

One lesson per entry, one-line summary on top. Read this first on any new run.

## 2026-06-09 — Agenda file missing: the program brief referenced "[path to agenda file]" but the placeholder was never filled and the repo contains no agenda
The repository (`bohm-krishnamurti/expriments`, branch `claude/optimistic-bohr-3s1rzj`) contained only an AOI website redesign (index.html, variant-a/b/c) at program start. The formal framework and 70-work annotated bibliography are therefore not on hand. Phase 1 proceeded from the construct definitions given in the brief itself (DBR, HSS, SL, IDI as described); Phase 3a candidates were drafted from the brief's sketches and must be reconciled with the agenda once the user supplies it. Other unfilled FILL IN items: API keys / benchmark harnesses installed (none found in repo), compute budget for re-runs, paper format/length, citation style.

## 2026-06-09 — Repo working state: develop on branch claude/optimistic-bohr-3s1rzj; gh CLI unavailable, GitHub MCP tools scoped to this repo only
Remote execution environment; ephemeral container, so anything worth keeping must be committed and pushed.

## 2026-06-09 — MALT is gated and lacks the fields the family-2 design assumed: no success labels, no token counts, run_ids don't join to eval-analysis-public
HuggingFace metr-evals/malt-public: `gated: auto` (free account auto-approval); anonymous file listing works but data download returns HTTP 401. Records carry tool calls, branching (branch_id/parent_node_id), per-message timestamps, behavior labels (gives_up, hardcoded_solution, sabotage, refusals...), model and task ids — but NO success label, NO tokens, and an int64 run_id namespace incompatible with eval-analysis-public's warehouse_* ids. The "proxy vs headline success in MALT" experiment is not executable as originally specified; the design moved to tau2-bench (C2 in CANDIDATES.md). Note METR's own README labels malt-public as the ordered-message view and malt-transcripts-public as the graph view; third-party writeups sometimes reverse this.

## 2026-06-09 — METR eval-analysis-public is the open run-level panel; README references a LICENSE file that does not exist
Anonymous git clone works (43 MB); GitHub API calls were rate-limited but raw fetches and clone were fine. Two vintages that must not be pooled: reports/time-horizon-1-0/data/raw/runs.jsonl (41,629 runs, 170 tasks, 35 models) and time-horizon-1-1 (24,008 runs, 228 tasks, 21 models, Inspect reruns). Per-run fields incl. score_binarized, score_cont, human_minutes (+human_source: baseline 17,765 / estimate 6,243 in 1-1), tokens_count, generation_cost, scaffold, fatal_error_from (997 usageLimits runs to exclude). No transcripts. LICENSE file 404s, so reuse terms are formally unspecified — flag in any publication.

## 2026-06-09 — HCAST task specs: real repo is METR/hcast-public (METR/hcast is 404); ~60 public tasks across two repos, rest email-gated
hcast-public: 11 families / 29 tasks with full Task Standard code incl. score() functions, MIT. METR/public-tasks: 31 example tasks across 10 families; its suite manifest names 28 families / 186 tasks but names only. DVC asset remote is anonymously readable at production-task-assets-public.s3.amazonaws.com using the files/md5/ layout (the old /xx/yyy layout 403s). Human baseline minutes are NOT in these repos — they live in eval-analysis-public runs.jsonl.

## 2026-06-09 — tau2-bench is the richest free corpus: per-trial trajectories with per-message tokens/cost in-repo AND a publicly listable S3 bucket of frontier leaderboard submissions
In-repo data/tau2/results/final/ (577 MB, 26 files): 4 models x 3 domains x 4 trials, reward decomposition (db_check, action_checks, nl_assertions, communicate_checks), agent/user cost, seeds, full transcripts. Leaderboard S3: sierra-tau-bench-public.s3.amazonaws.com listable without credentials (?list-type=2&prefix=submissions/), ~49 submissions incl. Opus 4.5-4.7, GPT-5.x, Gemini 3; newer schema adds hallucination_retries_used, auth_classification. CRITICAL: in-repo paper results predate the v1.0.0 "75+ task fixes" — do not pool paper-era and leaderboard-era records. Old tau-bench repo ships historical_trajectories/ for only 2 models x 2 domains and its README marks the tasks outdated.

## 2026-06-09 — Do-nothing baseline numbers have a primary source: arXiv:2507.02825 (ABC paper), not the tau2 paper
Quotes verified by fetch: do-nothing agent passes 38% airline / 6.0% retail "for any k"; output-everything ("spamming") agent 40% / 9.6%. Mechanism: tau-bench counts unsolvable tasks as passed when the environment is left unchanged. Use these as published floors for C2's degenerate-baseline obligation.

## 2026-06-09 — TheAgentCompany data lives in TheAgentCompany/experiments (3.7 GB, anonymous clone), not HuggingFace; one run per task per model
19 submissions x ~175 tasks: results/eval_<task>.json gives checkpoint-array partial credit (final_score.total can exceed checkpoint sum via completion bonus); trajectories/traj_<task>.json.gz are OpenHands event streams with per-step actions and per-call token usage. Task id and model are encoded only in file/folder names. No trial replication, no pass^k. Re-running requires the full self-hosted stack (GitLab, ownCloud, Plane, RocketChat), an environment-LLM key, and the encrypted evaluator (public key: 'theagentcompany is all you need') — heavy; the do-nothing degenerate test is only partially dischargeable observationally. The experiments repo has no LICENSE (main repo MIT).

## 2026-06-09 — HAL traces: 113 GB, 11 benchmarks x ~25 models, ungated, but Fernet-encrypted with public password 'hal1234' (PBKDF2-HMAC-SHA256, 480,000 iterations — not the 100k in the decrypt.py docstring)
huggingface.co/datasets/agent-evals/hal_traces, anonymous download works. Per-run zip: config, per-task success labels, raw per-LLM-call Weave logs with token usage incl. cache and total_cost. Files suffixed 'slim' LACK transcripts. No license stated on dataset or harness repo.

## 2026-06-09 — Epoch AI Benchmarking Hub: CAPTCHA on the web viewer but raw Inspect .eval logs are plain public S3 URLs in the CSV bundle; CC-BY 4.0
epoch.ai/data/benchmark_data.zip → per-run CSV rows with a Logs column pointing at epoch-benchmarks-{staging,production}-public.s3.us-east-2.amazonaws.com. SWE-bench Verified: 31 model configs on identical tasks; per-sample fields include messages, events, explicit error_retries, model_usage (incl. cache and reasoning tokens), total_time/working_time. .eval = Zstd zip, ~65 MB each. Cleanest licensed ladder corpus found.

## 2026-06-09 — SWE-bench experiments S3 is anonymously readable despite README saying an AWS account is needed; use prefix verified/<submission>/{trajs,logs}/ (the README-implied evaluation/verified/ prefix 403s)
139 verified-split submissions; per-instance resolved labels already in git (results/results.json); trajectory formats are heterogeneous per team and generally lack token counts.

## 2026-06-09 — Other corpora: OSWorld-Verified 472 GB (use HTTP range/remotezip; all_result.json is Python-repr, not JSON; step-budget ablations 15/50/100 are unique); AgentRewardBench has the only human burden-adjacent labels (1,408 annotations: success, side_effect, optimality, looping; no license); GAIA gated tasks-only; TRAIL gated 401; AgentBench releases no eval trajectories
AgentRewardBench: McGill-NLP/agent-reward-bench, ungated, 4 models x 4 web benchmarks on shared tasks, cleaned trajectory JSONs with n_steps, last_action_error, per-component token stats. OSWorld MIT.

## 2026-06-09 — Judge monoculture constraint: this environment has Claude models only (no OpenAI/Google keys found), so C1's "inter-judge reliability across model judges" degrades to across-Claude-variants unless the user supplies external keys
State this limit in any IDI-scoring claim, or obtain keys at the gate.
