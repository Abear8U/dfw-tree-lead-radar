import feedparser
import requests
from scoring import score_text

SEARCH_PAGES = [
    # Facebook public searches
    "https://www.facebook.com/search/posts?q=tree%20removal%20fort%20worth",
    "https://www.facebook.com/search/posts?q=tree%20service%20arlington",

    # OfferUp searches
    "https://offerup.com/search/?q=tree%20removal",
    "https://offerup.com/search/?q=tree%20service",
]

def scan_extra():
    leads = []

    for url in SEARCH_PAGES:
        try:
            r = requests.get(url, timeout=10)
            text = r.text.lower()

            # crude scan for phrases in page text
            phrases = [
                "need tree","looking for tree","tree removal",
                "tree service","fallen tree","trim tree"
            ]

            if any(p in text for p in phrases):
                score, city = score_text(text)
                if score > 0:
                    leads.append({
                        "source": "extra",
                        "title": "Possible lead on monitored page",
                        "url": url,
                        "score": score,
                        "city": city
                    })
        except:
            pass

    return leads


