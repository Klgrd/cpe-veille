import requests
import feedparser

FEEDS = [
    {"name": "Légifrance", "url": "https://www.legifrance.gouv.fr/api/rss"},
    {"name": "BOEN", "url": "https://www.education.gouv.fr/bo/rss.xml"},
    {"name": "Café Pédagogique", "url": "https://www.cafepedagogique.net/feed/"},
    {"name": "MEN", "url": "https://www.education.gouv.fr/rss.xml"}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*'
}

for feed_info in FEEDS:
    try:
        response = requests.get(feed_info["url"], headers=HEADERS, timeout=15) # removed verify=False to test default
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        print(f"{feed_info['name']}: {len(feed.entries)} entries")
    except Exception as e:
        print(f"{feed_info['name']} ERROR: {e}")
