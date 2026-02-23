import feedparser
from scoring import score_text

REDDIT_FEEDS = [
    "https://www.reddit.com/r/FortWorth/new/.rss",
    "https://www.reddit.com/r/Dallas/new/.rss",
    "https://www.reddit.com/r/DFW/new/.rss",
    "https://www.reddit.com/r/Arlington/new/.rss",
    "https://www.reddit.com/r/HomeImprovement/new/.rss",
    "https://www.reddit.com/r/Landscaping/new/.rss",
]

MIN_SCORE = 2

def scan_reddit(limit_per_feed: int = 200):
    leads = []
    for url in REDDIT_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries[:limit_per_feed]:
            title = e.get("title", "")
            summary = e.get("summary", "")
            link = e.get("link", "")
            posted = e.get("published", "")

            text = f"{title}\n{summary}"
            score, city = score_text(text)

            if score < MIN_SCORE:
                continue

            leads.append({
                "source": "reddit/rss",
                "title": title,
                "content": summary,
                "url": link,
                "posted_at": posted,
                "score": score,
                "city": city
            })

    return leads
