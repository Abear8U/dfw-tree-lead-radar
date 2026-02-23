import feedparser
from scoring import score_text

# Reddit RSS feeds (expanded)
REDDIT_FEEDS = [
    "https://www.reddit.com/r/FortWorth/new/.rss",
    "https://www.reddit.com/r/Dallas/new/.rss",
    "https://www.reddit.com/r/DFW/new/.rss",
    "https://www.reddit.com/r/Texas/new/.rss",
    "https://www.reddit.com/r/HomeImprovement/new/.rss",
    "https://www.reddit.com/r/DIY/new/.rss",
    "https://www.reddit.com/r/homeowners/new/.rss",
]

# Google search RSS feeds (big coverage)
GOOGLE_FEEDS = [
    "https://news.google.com/rss/search?q=tree+removal+fort+worth",
    "https://news.google.com/rss/search?q=fallen+tree+texas",
    "https://news.google.com/rss/search?q=tree+service+dallas",
]

ALL_FEEDS = REDDIT_FEEDS

def scan_all(limit_per_feed=100):
    leads = []
    for url in ALL_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries[:limit_per_feed]:
            title = e.get("title", "")
            summary = e.get("summary", "")
            link = e.get("link", "")

            text = f"{title}\n{summary}"
            score, city = score_text(text)

            if score <= 0:
                continue

            leads.append({
                "source": "multi",
                "title": title,
                "url": link,
                "score": score,
                "city": city
            })

    return leads
