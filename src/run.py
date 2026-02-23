from craigslist_scan import scan_craigslist
from reddit_scan import scan_reddit

def main():
    leads = []
    leads += scan_craigslist()
    leads += scan_reddit()

    if not leads:
        print("No leads found right now.")
        return

    leads.sort(key=lambda x: x["score"], reverse=True)

    print(f"Found {len(leads)} possible leads:\n")
    for L in leads[:30]:
        print(f"[{L['score']}] {L.get('city') or 'unknown'} | {L['source']} | {L['title']}")
        print(L["url"])
        print("-" * 60)

if __name__ == "__main__":
    main()
