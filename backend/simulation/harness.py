import argparse
import random
import time
import requests

API = "http://localhost:8000/api/v1"

# tp = probability an alert is a true positive, as a function of (round, total_rounds)
PROFILES = {
    "SimReliable":  {"tp": lambda r, n: 0.90, "volume": 1},
    "SimNoisy":     {"tp": lambda r, n: 0.20, "volume": 1},
    "SimDegrading": {"tp": lambda r, n: 0.90 if r < n // 2 else 0.10, "volume": 1},
}

def post_alert(name, rnd, i):
    body = {
        "source_name": name,
        "ioc_type": "domain",
        "ioc_value": f"{name.lower()}-{rnd}-{i}.invalid",
        "mitre_ttp": "T1071",
    }
    r = requests.post(f"{API}/alerts", json=body, timeout=10)
    r.raise_for_status()
    return r.json()["id"]

def send_verdict(alert_id, is_tp):
    v = "true_positive" if is_tp else "false_positive"
    r = requests.post(f"{API}/feedback", json={"alert_id": alert_id, "verdict": v}, timeout=10)
    r.raise_for_status()
    return r.json()["source_trust_score"]

def main(rounds, delay, seed):
    random.seed(seed)
    for rnd in range(rounds):
        line = []
        for name, p in PROFILES.items():
            score = None
            for i in range(p["volume"]):
                aid = post_alert(name, rnd, i)
                score = send_verdict(aid, random.random() < p["tp"](rnd, rounds))
            line.append(f"{name}={score:.3f}")
        print(f"round {rnd:02d}  " + "  ".join(line))
        time.sleep(delay)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=30)
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    main(a.rounds, a.delay, a.seed)