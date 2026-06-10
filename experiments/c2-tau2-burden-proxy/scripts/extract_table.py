#!/usr/bin/env python3
"""C2 extraction: build the task-by-submission table with the frozen variables
(SPEC.md, 'Variables (frozen)') from the raw trajectory files in data/raw/.

Outputs:
  task_by_submission.csv  — one row per (submission, domain, task)
  extract_log.json        — field-coverage numbers, exclusion counts, era notes

Frozen variables (per task t, submission m, trials k=1..4):
  p_hat     = (# trials with reward == 1) / 4 ; pass^1 = p_hat
  flakiness = p_hat * (1 - p_hat)
  effort    = log(1 + mean assistant-role message count per trial)
  retries   = mean hallucination_retries_used (only if field coverage >= 90% of
              included submissions; decided in analyze.py from extract_log.json)
  verification-type failure per failed trial: db_check pass AND
              (nl_assertions fail OR communicate_checks fail); trials lacking the
              fields are excluded from H3 and counted.

Solvable subset (decision-tree branch 2, recorded in STEPLOG before any statistic):
  do-nothing-passable iff the task's gold action set contains no state-changing
  (WRITE) action and no required (reward-basis-borne) communication assertion.
  Classified per submission from the task definitions embedded in that submission's
  own trajectory file (task versions differ across submission eras).
"""
import json, math, os, glob, csv, re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
OUT_CSV = os.path.join(HERE, "..", "task_by_submission.csv")
OUT_LOG = os.path.join(HERE, "..", "data", "extract_log.json")
TAU2 = "/tmp/tau2-bench"

DOMAINS = ["airline", "retail", "telecom"]

def write_tools():
    """tool name -> WRITE/READ/GENERIC per domain, parsed from tau2-bench source."""
    paths = {
        "airline": ["src/tau2/domains/airline/tools.py"],
        "retail": ["src/tau2/domains/retail/tools.py"],
        "telecom": ["src/tau2/domains/telecom/tools.py",
                     "src/tau2/domains/telecom/user_tools.py"],
    }
    out = {}
    for dom, ps in paths.items():
        tt = {}
        for p in ps:
            src = open(os.path.join(TAU2, p)).read()
            for m in re.finditer(r"@is_tool\(ToolType\.(\w+)\)\s+def\s+(\w+)\(", src):
                tt[m.group(2)] = m.group(1)
        out[dom] = tt
    return out

WRITE_TOOLS = write_tools()

def do_nothing_passable(task, dom):
    """Frozen branch-2 rule. Returns (passable, has_write, comm_required)."""
    ec = task.get("evaluation_criteria") or {}
    acts = ec.get("actions") or []
    rb = set(ec.get("reward_basis") or [])
    comm = ec.get("communicate_info") or []
    nla = ec.get("nl_assertions") or []
    has_write = any(WRITE_TOOLS[dom].get(a["name"]) == "WRITE" for a in acts)
    comm_required = (len(comm) > 0 and "COMMUNICATE" in rb) or \
                    (len(nla) > 0 and "NL_ASSERTION" in rb)
    return (not has_write) and (not comm_required), has_write, comm_required

def trial_fields(sim):
    ri = sim["reward_info"]
    if ri is None:
        # infrastructure_error trials: no reward, no messages. Not agent behavior;
        # excluded from all per-task means (deviation logged in STEPLOG).
        return None
    reward = ri.get("reward")
    passed = reward is not None and reward >= 1.0 - 1e-9
    n_assistant = sum(1 for m in sim["messages"] if m.get("role") == "assistant")
    retries = sim.get("hallucination_retries_used")  # None if legacy schema
    db = ri.get("db_check")
    nl = ri.get("nl_assertions")
    cc = ri.get("communicate_checks")
    h3_excluded = (db is None) or (nl is None and cc is None)
    vtype = False
    if not h3_excluded and not passed:
        db_pass = bool(db.get("db_match"))
        nl_fail = any(not a.get("met") for a in (nl or []))
        cc_fail = any(not a.get("met") for a in (cc or []))
        vtype = db_pass and (nl_fail or cc_fail)
    return passed, n_assistant, retries, h3_excluded, vtype

def main():
    rows = []
    log = {"submissions": {}, "h3_excluded_failed_trials": 0,
           "n_failed_trials": 0, "retries_coverage": {},
           "invalid_trials": 0, "tasks_dropped_no_valid_trials": []}
    files = sorted(glob.glob(os.path.join(RAW, "*__*.json")))
    subs = sorted({os.path.basename(f).split("__")[0] for f in files})
    for sub in subs:
        sub_log = {"domains": {}, "retries_field_present": True}
        for dom in DOMAINS:
            path = os.path.join(RAW, f"{sub}__{dom}.json")
            d = json.load(open(path))
            tasks = {t["id"]: t for t in d["tasks"]}
            by_task = {}
            for s in d["simulations"]:
                by_task.setdefault(s["task_id"], []).append(s)
            n_retry_present = n_trials_total = 0
            for tid, sims in sorted(by_task.items()):
                assert len(sims) == 4, (sub, dom, tid, len(sims))
                tf = [trial_fields(s) for s in sims]
                n_invalid = sum(1 for t in tf if t is None)
                tf = [t for t in tf if t is not None]
                n_valid = len(tf)
                log["invalid_trials"] += n_invalid
                if n_valid == 0:
                    log["tasks_dropped_no_valid_trials"].append([sub, dom, tid])
                    continue
                n_pass = sum(t[0] for t in tf)
                p_hat = n_pass / n_valid
                mean_amsg = sum(t[1] for t in tf) / n_valid
                retr = [t[2] for t in tf if t[2] is not None]
                n_retry_present += len(retr)
                n_trials_total += n_valid
                failed = [t for t in tf if not t[0]]
                h3_exc = sum(1 for t in failed if t[3])
                vty = sum(1 for t in failed if not t[3] and t[4])
                passable, has_write, comm_req = do_nothing_passable(tasks[tid], dom)
                rows.append({
                    "submission": sub, "domain": dom, "task_id": tid,
                    "n_trials": n_valid, "n_pass": n_pass, "p_hat": p_hat,
                    "flakiness": p_hat * (1 - p_hat),
                    "mean_assistant_msgs": mean_amsg,
                    "effort": math.log1p(mean_amsg),
                    "retries_mean": (sum(retr) / len(retr)) if retr else "",
                    "retries_n_present": len(retr),
                    "n_failed": len(failed),
                    "n_failed_vtype": vty,
                    "n_failed_h3_excluded": h3_exc,
                    "do_nothing_passable": int(passable),
                    "has_write_action": int(has_write),
                    "comm_required": int(comm_req),
                })
                log["h3_excluded_failed_trials"] += h3_exc
                log["n_failed_trials"] += len(failed)
            sub_log["domains"][dom] = {
                "n_tasks": len(by_task),
                "retries_field_coverage": n_retry_present / n_trials_total,
            }
            if n_retry_present < n_trials_total:
                sub_log["retries_field_present"] = False
        log["submissions"][sub] = sub_log
    n_with = sum(1 for s in log["submissions"].values() if s["retries_field_present"])
    log["retries_coverage"] = {
        "submissions_with_full_retries_field": n_with,
        "n_submissions": len(subs),
        "fraction": n_with / len(subs),
        "decision_rule": "include retries only if >= 0.90",
        "included": n_with / len(subs) >= 0.90,
    }
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT_LOG, "w") as f:
        json.dump(log, f, indent=1)
    print(f"rows={len(rows)} submissions={len(subs)}")
    print("retries coverage:", json.dumps(log["retries_coverage"]))
    print(f"failed trials={log['n_failed_trials']} h3-excluded={log['h3_excluded_failed_trials']}")

if __name__ == "__main__":
    main()
