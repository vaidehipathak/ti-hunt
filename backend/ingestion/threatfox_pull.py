import os
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("URLHAUS_AUTH_KEY")
TF_API = "https://threatfox-api.abuse.ch/api/v1/"
ALERTS = "http://localhost:8000/api/v1/alerts"

TYPE_MAP = {"ip:port": "ip", "domain": "domain", "url": "url"}

def fetch(days=1):
    r = requests.post(TF_API, json={"query": "get_iocs", "days": days},
                      headers={"Auth-Key": KEY}, timeout=30)
    r.raise_for_status()
    return r.json().get("data") or []

def existing():
    r = requests.get(ALERTS, timeout=10)
    r.raise_for_status()
    return {a["ioc_value"] for a in r.json()}

def to_alert(ioc):
    t = TYPE_MAP.get(ioc["ioc_type"], ioc["ioc_type"])
    v = ioc["ioc"].split(":")[0] if ioc["ioc_type"] == "ip:port" else ioc["ioc"]
    return {"source_name": "ThreatFox", "ioc_type": t, "ioc_value": v}

def main(limit=20):
    seen = existing()
    sent = 0
    for ioc in fetch():
        a = to_alert(ioc)
        if a["ioc_value"] in seen:
            continue
        resp = requests.post(ALERTS, json=a, timeout=10)
        print(resp.status_code, a["ioc_value"])
        seen.add(a["ioc_value"])
        sent += 1
        if sent >= limit:
            break

if __name__ == "__main__":
    main()