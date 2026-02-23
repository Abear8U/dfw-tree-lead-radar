# craigslist_scan.py
import feedparser
from scoring import score_text

CRAIGS_RSS = [
    # SERVICES + COMMUNITY + GIGS (better for homeowner requests)
    "https://dallas.craigslist.org/search/bbb?format=rss&query=tree%20removal",
    "https://dallas.craigslist.org/search/bbb?format=rss&query=tree%20trimming",
    "https://dallas.craigslist.org/search/bbb?format=rss&query=stump%20grinding",
    "https://dallas.craigslist.org/search/bbb?format=rss&query=fallen%20tree",
    "https://dallas.craigslist.org/search/bbb?format=rss&query=tree%20guy",

    "https://dallas.craigslist.org/search/cpg?format=rss&query=tree%20removal",
    "https://dallas.craigslist.org/search/cpg?format=rss&query=remove%20tree",
    "https://dallas.craigslist.org/search/cpg?format=rss&query=downed%20tree",

    "https://dallas.craigslist.org/search/cmm?format=rss&query=tree%20removal",
    "https://dallas.craigslist.org/search/cmm?format=rss&query=tree%20trimming",

    # keep for-sale as backup
    "https://dallas.craigslist.org/search/sss?format=rss&query=tree%20removal",
]

MIN_SCORE = 2

def scan_craigslist(limit_per_feed: int = 200):
    leads = []
    for rss_url in CRAIGS_RSS:
        feed = feedparser.parse(rss_url)
        for e in feed.entries[:limit_per_feed]:
            title = e.get("title", "")
            summary = e.get("summary", "")
            url = e.get("link", "")
            posted_at = e.get("published", "")

            text = f"{title}\n{summary}"
            score, city = score_text(text)

            if score < MIN_SCORE:
                continue

            leads.append({
                "source": "craigslist/dfw",
                "title": title,
                "content": summary,
                "url": url,
                "posted_at": posted_at,
                "score": score,
                "city": city
            })
    return leads
