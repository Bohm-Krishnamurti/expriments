# STEPLOG — C5: Proxy validation against human burden-adjacent labels (AgentRewardBench)

Run date: 2026-06-10. Runner: Claude Code. SPEC.md read first and treated as binding.

## Step 1 — Data download

- Dataset: McGill-NLP/agent-reward-bench (HuggingFace, ungated, anonymous). API confirmed
  `gated: false`. Dataset sha at download time: b6d17e646009d6cb63d5dd7be78807b680693f61
  (lastModified 2025-04-21).
- `data/annotations.csv` downloaded via resolve URL: 1,408 data rows + header (matches SPEC's
  expected 1,408).
- Cleaned trajectory file list enumerated from the dataset API siblings: **1,302 JSONs** under
  `cleaned/<benchmark>/<agent>/<exp_name>/<task_id>.json` (matches SPEC's expected 1,302).
  Per-benchmark: workarena 472, webarena 398, visualwebarena 300, assistantbench 132.
  Per-agent: Qwen2.5-VL-72B 351, claude-3.7-sonnet 351, gpt-4o-2024-11-20 351,
  Llama-3.3-70B 249.
- **DEVIATION (plumbing only, forced by environment):** raw trajectory JSONs average ~17 MB
  (full AXTree/HTML observations per step); the full set is ~22 GB and the container disk
  filled at 876/1302 files (and the disk also hosts other agents' data that must not be
  touched). The initial bulk download was deleted and replaced by a **stream-and-extract**
  pipeline (`scripts/extract_features.py`): each JSON is fetched into memory from its public
  resolve URL, the frozen features are extracted, and the raw bytes are discarded. No raw
  trajectory files are persisted. This changes storage plumbing only; the features and the
  registered analysis are unchanged, and raw files remain regenerable from public URLs (per
  SPEC "Outputs"). `data/` is gitignored regardless (`experiments/*/data/`).
- Also freed: nothing outside this experiment's own downloads. A 13 GB leftover scout clone in
  /tmp could not be removed (permission denied by sandbox policy); the streaming design makes
  that unnecessary.

## Step 2 — Schema reconnaissance (one sample trajectory + annotations profile)

- Trajectory JSON top-level: benchmark, agent, model, experiment, goal, summary_info, steps[].
  `task_id` is NOT inside the JSON; it is the file stem of the path
  (`cleaned/<benchmark>/<agent>/<exp>/<task_id>.json`). `model_name` in annotations equals the
  `agent` path component / `agent` field (e.g. `GenericAgent-gpt-4o-2024-11-20`). Join keys
  therefore come from the file path; the in-file `benchmark`/`agent` fields are cross-checked
  during extraction. (Adaptation: SPEC said "join on (benchmark, task_id, model_name)"; the
  key construction from path is plumbing, the key itself is as registered.)
- `summary_info` has `n_steps` and FLATTENED stats keys (`stats.cum_n_token_axtree_txt`, ...)
  rather than a nested `summary_info.stats` dict. Adaptation: read the flattened keys.
- `steps` list has n_steps+1 records (terminal observation record has `action: null`).
  `last_action_error` at record t reports the error of the action taken at record t-1
  (record 0's is always empty).
- Annotation columns: `annotator_name` (SPEC said "annotator" — name plumbing),
  benchmark, task_id, model_name, exp_name, trajectory_success {Successful/Unsuccessful/Unsure},
  trajectory_side_effect {Yes/No/Unsure}, trajectory_optimality {1. Complete Failure /
  2. Suboptimal / 3. Somewhat Optimal / 4. Completely Optimal / Unsure},
  trajectory_looping {Yes/No}. One annotator value has a stray leading space (' H' → 'H',
  whitespace stripped). 106 rows are repeat-annotations of an already-annotated
  (benchmark, task_id, model_name) key.
- "Unsure" values (1 per label for success/side_effect/optimality) are not covered by the
  SPEC. Adaptation (logged, minimal): an "Unsure" vote is treated as a missing vote for that
  label only (excluded from the majority for that trajectory-label); counts reported below.

## Step 3 — Frozen feature operationalization (decisions logged before analysis)

All from trajectory JSON only; never from annotations, cum_reward, or model identity.
- `n_steps` := `summary_info['n_steps']`.
- error rate := (# step records with non-empty `last_action_error`) / n_steps. Because the
  steps list holds n_steps+1 records and record t's error describes action t-1, this is
  exactly the share of ACTIONS whose execution errored; capped at 1; 0 if n_steps == 0.
- action strings := `step['action']` for records where action is not null (n_steps of them);
  repeat rate := 1 - distinct(action strings)/n_steps (SPEC formula verbatim).
- max consecutive identical action strings, normalized: max run length / n_steps.
- mean observation tokens per step := (stats.cum_n_token_axtree_txt + stats.cum_n_token_dom_txt
  + stats.cum_n_token_pruned_html) / n_steps. Adaptation: SPEC said "from summary_info.stats";
  the dataset exposes flattened per-component token counters, and the page-observation
  components are the three above (url/goal/focused-element counters are not observation text;
  input_tokens would include the prompt and is not observation-only). Coverage rule (>=90% of
  joined trajectories else drop) applied as registered.
- z-scoring within training folds only (inside the CV loop).

## Step 4 — Registered analysis protocol: implementation decisions (logged BEFORE results)

All decisions below were fixed before any model was run or any AUC seen.
- sklearn LogisticRegression(penalty='l2', C=1/lambda, lbfgs, max_iter=2000); lambda grid
  {0.01, 0.1, 1, 10} verbatim from SPEC.
- Inner CV for lambda: grouped 5-fold by task_id WITHIN each training fold (group-respecting,
  consistent with the outer protocol); lambda chosen by pooled inner out-of-fold AUC.
- "Held-out AUC on the primary cross-validation" operationalized as the Mann-Whitney AUC on
  POOLED out-of-fold predictions from the 5 grouped folds (single registered number; per-fold
  averaging would be an alternative but pooled-OOF was fixed here first).
- Bootstrap CI: resample task_id clusters with replacement, 1,000 iterations, percentile 95%
  CI computed on pooled-OOF predictions.
- Leave-one-benchmark-out: train on 3 benchmarks / test on the 4th; reported pooled and
  per-benchmark; not decision-bearing (per SPEC).
- Labels with missing aggregated value (all votes Unsure) are dropped for that label only.
- Exploratory model-dummies sensitivity: same pipeline, features + 3 dummy columns (k-1
  coding over the 4 agents); exploratory only.
- Random seed fixed at 20260610 for the bootstrap.
- Tie-corrected Mann-Whitney (midranks) used for AUC.

## Step 5 — RUN RESUMED (2026-06-10, new runner session)

- The previous runner session ended mid-extraction: `data/trajectory_features.csv` held 450 of
  1,302 rows (0 fetch errors). State verified on resume: annotations.csv intact (1,408 data
  rows), cleaned_filelist.txt intact (1,302 entries), scripts present
  (extract_features.py / build_table.py / analyze.py — reviewed, consistent with the
  registered SPEC and the decisions in Steps 2–4 above; not modified).
- sklearn 1.9.0 available in this session (no pip install needed); pandas 3.0.3,
  numpy 2.4.6, scipy 1.17.1.
- Resumed `extract_features.py`, which skips already-extracted (benchmark, task_id,
  model_name) keys and appends — no completed work redone.
- **INCIDENT (plumbing only) + repair:** the previous session's extractor process was in
  fact still alive in the container and writing to the same CSV when the resumed extractor
  was launched; two concurrent writers (one truncate-mode handle, one append-mode handle)
  interleaved on `data/trajectory_features.csv`. Both processes finished (extract.log shows
  two "done" lines). Aftermath audited with `scripts/repair_features.py` (strict per-row
  validation against the filelist key set + field-level sanity checks): 1,394 raw rows ->
  1 corrupt row dropped, 91 byte-identical duplicate keys dropped, **0 conflicting
  duplicates**, 1,302 valid unique rows covering all 1,302 filelist keys; 0 re-fetches
  needed. CSV rewritten atomically in filelist order and re-verified (1,302 rows / 1,302
  unique keys / 0 fetch errors). Because duplicates were byte-identical and the corrupt
  row was dropped and re-validated, no feature values were affected. Feature definitions
  untouched; this was storage plumbing only.

## Step 6 — Join, aggregation, registered analysis (resumed session)

- `scripts/build_table.py` run on the repaired feature table. Counts logged: 1,408
  annotation rows over 1,302 unique (benchmark, task_id, model_name) keys; 106 keys with 2
  annotators (max 2); Unsure votes: side_effect 1, optimality 1, success 1, looping 0
  (treated as missing votes per Step 2). Ties at aggregation (resolved to positive per
  SPEC): side_effect 4, suboptimal 12, looping 11, success 12. Join: 1,302 joined, 0
  annotations without trajectory, 0 trajectories without annotation. obs_tokens coverage
  100% -> feature kept per the registered >=90% rule. 0 path/JSON metadata mismatches.
- Inter-annotator agreement (pooled pairwise, on the 106 doubly-annotated keys):
  side_effect 96.2% / kappa 0.65; suboptimal (binarized) 88.6% / kappa 0.74; looping
  89.6% / kappa 0.77; success 88.6% / kappa 0.76.
- `scripts/analyze.py` run exactly as registered (no changes to the analysis code in this
  session). sklearn 1.9.0 emitted a FutureWarning that `penalty=` is deprecated; behavior
  with penalty='l2' + C is unchanged in 1.9 (warning only), so the registered model is
  what ran. Outputs in `data/results.json`; registered numbers in RESULTS.md.
- Verdicts under the registered rules: H1 (side_effect) NOT supported (AUC 0.576 < 0.70;
  margin +0.098 did exceed 0.05). H2 (suboptimal) NOT supported (AUC 0.891 >= 0.70 but
  margin over length-only +0.009 < 0.05). The SPEC's null statement therefore applies.
  Looping (no decision weight): AUC 0.938, margin +0.049. Success (secondary): AUC 0.816,
  margin +0.015.
- RESULTS.md written: registered statistics and verdicts first, exploratory model-dummies
  sensitivity clearly separated, analytic do-nothing note included.
