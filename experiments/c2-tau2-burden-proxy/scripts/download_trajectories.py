#!/usr/bin/env python3
"""Download the per-domain multi-trial trajectory JSONs for the 15 candidate C2
submissions from the public sierra-tau-bench-public S3 bucket (anonymous HTTPS).

Regenerates data/raw/ from public URLs; raw files stay out of git.
"""
import os, sys, urllib.request

BASE = "https://sierra-tau-bench-public.s3.amazonaws.com/submissions/"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# (submission, domain, key-relative-path)
FILES = []
def add(sub, dom, rel): FILES.append((sub, dom, f"{sub}/trajectories/{rel}"))

for dom in ["airline", "retail", "telecom"]:
    add("claude-3-7-sonnet_anthropic_2024-06-20", dom,
        f"claude-3-7-sonnet-20250219_{dom}_default_gpt-4.1-2025-04-14_4trials.json")
    add("claude-opus-4-5_sierra_2026-02-26", dom, f"claude-opus-4-5_high_{dom}_gpt-5.2_4trials.json")
    add("claude-sonnet-4-5_sierra_2026-02-26", dom, f"claude-sonnet-4-5_enabled_{dom}_gpt-5.2_4trials.json")
    add("gemini-3-flash_sierra_2026-03-02", dom, f"geminiflash-{dom}.json")
    add("gemini-3-pro_sierra_2026-03-02", dom, f"geminipro-{dom}.json")
    add("glm-5-think_sierra_2026-03-02", dom, f"glm-5_enabled_{dom}_gpt-5.2_4trials.json")
    add("gpt-4-1-mini_openai_2024-06-20", dom,
        f"gpt-4.1-mini-2025-04-14_{dom}_base_gpt-4.1-2025-04-14_4trials.json")
    add("gpt-4-1_openai_2024-06-20", dom,
        f"gpt-4.1-2025-04-14_{dom}_default_gpt-4.1-2025-04-14_4trials.json")
    add("gpt-5-2-none_sierra_2026-02-26", dom, f"gpt-5.2_none_{dom}_gpt-5.2_4trials.json")
    add("gpt-5-2_sierra_2026-02-26", dom, f"gpt-5.2_high_{dom}_gpt-5.2_4trials.json")
    add("gpt-5_sierra_2025-08-09", dom, f"gpt-5_{dom}_default_gpt-4.1-2025-04-14_4trials.json")
    add("o4-mini_openai_2024-06-20", dom, f"o4-mini-2025-04-16_{dom}_default_gpt-4.1-2025-04-14_4trials.json")
    add("qwen3-max_qwen_2025-10-30", dom,
        f"{dom}_llm_agent_qwen3-max-2025-10-30_user_simulator_gpt-4.1-2025-04-14.json")
    add("qwen3-max_qwen_2026-01-23", dom,
        f"{dom}_llm_agent_qwen3-max-2026-01-23_user_simulator_gpt-4.1-2025-04-14.json")
    add("qwen3.5-397b-a17b-think_sierra_2026-03-02", dom, f"qwen3.5-397b-a17b_enabled_{dom}_gpt-5.2_4trials.json")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ok = skip = fail = 0
    for sub, dom, key in FILES:
        dest = os.path.join(OUT, f"{sub}__{dom}.json")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skip += 1
            continue
        url = BASE + urllib.request.quote(key)
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"OK   {sub} {dom} {os.path.getsize(dest)/1e6:.1f} MB", flush=True)
            ok += 1
        except Exception as e:
            print(f"FAIL {sub} {dom}: {e}", flush=True)
            if os.path.exists(dest):
                os.remove(dest)
            fail += 1
    print(f"downloaded={ok} skipped={skip} failed={fail} of {len(FILES)}")
