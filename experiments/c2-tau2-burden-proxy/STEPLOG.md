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
