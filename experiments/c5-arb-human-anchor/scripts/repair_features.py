#!/usr/bin/env python3
"""C5 repair step (plumbing only): the feature CSV was corrupted by two concurrent
extractor processes (the previous runner session's extractor was still alive when the
resumed session launched its own; one file handle was in truncate mode, one in append
mode, so interleaved writes clobbered/duplicated rows). This script:
  1. strictly validates every row of data/trajectory_features.csv,
  2. drops corrupt rows and exact-duplicate keys (logging whether duplicates agree),
  3. re-fetches any keys still missing, single-threaded pool, single writer,
  4. rewrites the CSV atomically in filelist order and verifies 1,302 unique rows.
Feature definitions are untouched: re-fetching reuses extract_features.extract().
"""
import csv
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_features import FIELDS, FILELIST, OUT, fetch, extract  # noqa: E402

NUMERIC01 = ["error_rate", "repeat_rate", "max_consec_norm"]


def path_key(p):
    parts = p.split("/")
    return (parts[1], parts[-1][:-5], parts[2])


def valid(row, keyset):
    if set(row.keys()) != set(FIELDS) or any(v is None for v in row.values()):
        return False
    if (row["benchmark"], row["task_id"], row["model_name"]) not in keyset:
        return False
    try:
        if int(float(row["fetch_error"])) != 0:
            return False
        n_steps = float(row["n_steps"])
        if n_steps < 0 or n_steps != int(n_steps):
            return False
        for c in NUMERIC01:
            v = float(row[c])
            if not (0.0 <= v <= 1.0):
                return False
        nrec, nact = float(row["n_step_records"]), float(row["n_actions"])
        if nrec < nact or nact > n_steps + 1:
            return False
        if row["obs_tokens_per_step"] != "":
            float(row["obs_tokens_per_step"])
        int(float(row["obs_tokens_present"]))
        int(float(row["path_json_mismatch"]))
    except (ValueError, TypeError):
        return False
    return True


def main():
    paths = [l.strip() for l in open(FILELIST) if l.strip()]
    keyset = {path_key(p) for p in paths}
    assert len(keyset) == len(paths), "filelist keys not unique"

    by_key = {}
    n_raw = n_invalid = n_dup_identical = n_dup_conflict = 0
    with open(OUT) as f:
        for row in csv.DictReader(f):
            n_raw += 1
            if not valid(row, keyset):
                n_invalid += 1
                continue
            k = (row["benchmark"], row["task_id"], row["model_name"])
            if k in by_key:
                if by_key[k] == row:
                    n_dup_identical += 1
                else:
                    # conflicting duplicates: distrust both, refetch
                    n_dup_conflict += 1
                    del by_key[k]
            else:
                by_key[k] = row

    missing = [p for p in paths if path_key(p) not in by_key]
    print(f"raw rows: {n_raw}; invalid dropped: {n_invalid}; "
          f"identical dups dropped: {n_dup_identical}; "
          f"conflicting dups (refetch): {n_dup_conflict}; "
          f"valid unique: {len(by_key)}; to refetch: {len(missing)}", flush=True)

    def worker(path):
        return path, extract(path, fetch(path))

    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, (path, row) in enumerate(ex.map(worker, missing), 1):
            by_key[path_key(path)] = {k: str(v) for k, v in row.items()}
            if i % 25 == 0:
                print(f"refetched {i}/{len(missing)}", flush=True)

    assert len(by_key) == len(paths), f"still missing {len(paths) - len(by_key)} keys"
    tmp = OUT + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for p in paths:  # deterministic filelist order
            w.writerow(by_key[path_key(p)])
    os.replace(tmp, OUT)

    # final verification pass
    with open(OUT) as f:
        rows = list(csv.DictReader(f))
    keys = {(r["benchmark"], r["task_id"], r["model_name"]) for r in rows}
    assert len(rows) == 1302 and len(keys) == 1302, (len(rows), len(keys))
    print("repair complete: 1302 rows, 1302 unique keys, all valid", flush=True)


if __name__ == "__main__":
    main()
