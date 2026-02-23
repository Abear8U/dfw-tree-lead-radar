import os, json
from dotenv import load_dotenv
from twilio.rest import Client

from reddit_scan import scan_reddit
from craigslist_scan import scan_craigslist

load_dotenv()

SEEN_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "seen.json")
MIN_SCORE_TO_TEXT = 6

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_seen(seen):
    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(list(seen))[-5000:], f)

def send_sms(body: str):
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_FROM_NUMBER")
    to_num = os.getenv("ALERT_TO_NUMBER")
    if not all([sid, token, from_num, to_num]):
        raise RuntimeError("Missing Twilio env vars")

    Client(sid, token).messages.create(body=body, from_=from_num, to=to_num)

def lead_id(l):
    return f"{l.get('source','')}-{l.get('url','')}"

def run_once():
    seen = load_seen()
    leads = scan_reddit(200) + scan_craigslist(200)

    new_hits = []
    for l in leads:
        if l.get("score", 0) < MIN_SCORE_TO_TEXT:
            continue
        lid = lead_id(l)
        if lid in seen:
            continue
        seen.add(lid)
        new_hits.append(l)

    if new_hits:
        new_hits.sort(key=lambda x: x["score"], reverse=True)
        top = new_hits[0]
        msg = f"🌳 Tree lead ({top['score']}): {top['title']}\n{top['url']}"
        send_sms(msg)

    save_seen(seen)

if __name__ == "__main__":
    run_once()
