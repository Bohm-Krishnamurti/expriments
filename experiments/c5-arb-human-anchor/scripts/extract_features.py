#!/usr/bin/env python3
"""C5 step 1/3: stream cleaned trajectory JSONs from HuggingFace, extract frozen features.

Raw JSONs (~17 MB each, ~22 GB total) are fetched into memory and discarded after feature
extraction (disk-constrained environment; see STEPLOG.md). Features are exactly the frozen
set in SPEC.md. Output: data/trajectory_features.csv (one row per trajectory file).
"""
import csv
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://huggingface.co/datasets/McGill-NLP/agent-reward-bench/resolve/main/"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FILELIST = os.path.join(DATA, "cleaned_filelist.txt")
OUT = os.path.join(DATA, "trajectory_features.csv")

FIELDS = [
    "benchmark", "task_id", "model_name",  # join keys (from path; cross-checked vs JSON)
    "n_steps", "error_rate", "repeat_rate", "max_consec_norm",
    "obs_tokens_per_step", "obs_tokens_present",
    "n_step_records", "n_actions", "path_json_mismatch", "fetch_error",
]


def fetch(path, retries=4):
    url = BASE + urllib.request.quote(path)
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))


def extract(path, raw):
    parts = path.split("/")
    benchmark, agent, task_id = parts[1], parts[2], parts[-1][:-5]
    row = {k: "" for k in FIELDS}
    row.update(benchmark=benchmark, task_id=task_id, model_name=agent)
    d = json.loads(raw)
    mismatch = int(d.get("benchmark") != benchmark or d.get("agent") != agent)
    si = d.get("summary_info") or {}
    steps = d.get("steps") or []
    n_steps = si.get("n_steps")
    if n_steps is None:
        n_steps = max(len(steps) - 1, 0)
    actions = [s.get("action") for s in steps if s.get("action") is not None]
    actions = [str(a) for a in actions]
    n_err = sum(1 for s in steps if (s.get("last_action_error") or "").strip())
    if n_steps > 0:
        error_rate = min(n_err / n_steps, 1.0)
        repeat_rate = max(0.0, 1.0 - len(set(actions)) / n_steps)
        max_run = 0
        cur = 0
        prev = object()
        for a in actions:
            cur = cur + 1 if a == prev else 1
            prev = a
            max_run = max(max_run, cur)
        max_consec_norm = max_run / n_steps
    else:
        error_rate = repeat_rate = max_consec_norm = 0.0
    tok_keys = ["stats.cum_n_token_axtree_txt", "stats.cum_n_token_dom_txt",
                "stats.cum_n_token_pruned_html"]
    present = all(si.get(k) is not None for k in tok_keys)
    obs_per_step = ""
    if present and n_steps > 0:
        obs_per_step = sum(float(si[k]) for k in tok_keys) / n_steps
    row.update(n_steps=n_steps, error_rate=error_rate, repeat_rate=repeat_rate,
               max_consec_norm=max_consec_norm, obs_tokens_per_step=obs_per_step,
               obs_tokens_present=int(present and n_steps > 0),
               n_step_records=len(steps), n_actions=len(actions),
               path_json_mismatch=mismatch, fetch_error=0)
    return row


def worker(path):
    try:
        raw = fetch(path)
        return extract(path, raw)
    except Exception as e:  # noqa: BLE001 - log and continue
        parts = path.split("/")
        row = {k: "" for k in FIELDS}
        row.update(benchmark=parts[1], task_id=parts[-1][:-5], model_name=parts[2],
                   fetch_error=1)
        sys.stderr.write(f"FAIL {path}: {e}\n")
        return row


def main():
    paths = [l.strip() for l in open(FILELIST) if l.strip()]
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as f:
            for r in csv.DictReader(f):
                done.add((r["benchmark"], r["task_id"], r["model_name"]))
    todo = [p for p in paths
            if (p.split("/")[1], p.split("/")[-1][:-5], p.split("/")[2]) not in done]
    print(f"{len(paths)} total, {len(done)} done, {len(todo)} to fetch", flush=True)
    mode = "a" if done else "w"
    with open(OUT, mode, newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if mode == "w":
            w.writeheader()
        n = 0
        with ThreadPoolExecutor(max_workers=12) as ex:
            for row in ex.map(worker, todo):
                w.writerow(row)
                n += 1
                if n % 50 == 0:
                    f.flush()
                    print(f"{n}/{len(todo)}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
