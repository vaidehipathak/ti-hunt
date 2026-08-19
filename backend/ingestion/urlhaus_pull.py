"""
URLhaus ingestion connector.

Pulls recent malicious URLs from the URLhaus API and injects them into
ti-hunt as real alerts, using the exact same POST /api/v1/alerts endpoint
the demo panel uses. This means trust scoring, EXP3 weight updates, and
the CUSUM watchdog all fire exactly as they would for any other alert --
no DB logic is duplicated here.

Usage:
    python urlhaus_pull.py

Requires:
    URLHAUS_AUTH_KEY env var (or hardcode below for tonight's demo)
    Backend running locally on port 8000
"""

import os
import time
import requests

URLHAUS_AUTH_KEY = os.environ.get("URLHAUS_AUTH_KEY", "PUT_YOUR_KEY_HERE")
URLHAUS_ENDPOINT = "https://urlhaus-api.abuse.ch/v1/urls/recent/limit/20/"
BACKEND_ALERTS_ENDPOINT = "http://localhost:8000/api/v1/alerts"
SOURCE_NAME = "URLhaus"


def fetch_recent_urls():
    resp = requests.get(
        URLHAUS_ENDPOINT,
        headers={"Auth-Key": URLHAUS_AUTH_KEY},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    if data.get("query_status") != "ok":
        raise RuntimeError(f"URLhaus returned non-ok status: {data.get('query_status')}")

    return data.get("urls", [])


def push_alert(url_entry):
    payload = {
        "source_name": SOURCE_NAME,
        "ioc_type": "url",
        "ioc_value": url_entry["url"],
        "mitre_ttp": None,
    }
    resp = requests.post(BACKEND_ALERTS_ENDPOINT, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    print("Fetching recent URLs from URLhaus...")
    urls = fetch_recent_urls()
    print(f"Got {len(urls)} entries.")

    success, failed = 0, 0
    for entry in urls:
        try:
            result = push_alert(entry)
            print(f"  [ok] alert id={result['id']} url={entry['url'][:60]}")
            success += 1
        except Exception as e:
            print(f"  [fail] {entry.get('url', '?')[:60]} -> {e}")
            failed += 1
        time.sleep(0.1)  # be polite to your own local backend

    print(f"\nDone. {success} inserted, {failed} failed.")


if __name__ == "__main__":
    main()