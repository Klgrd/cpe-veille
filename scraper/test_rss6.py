import requests
import feedparser

urls = [
    "https://www.snes.edu/feed/",
    "https://www.enseignementsup-recherche.gouv.fr/rss.xml",
    "https://www.aefinfo.fr/rss/depeches/education"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

for url in urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        print(f"{url}: {r.status_code}")
        if r.status_code == 200:
            feed = feedparser.parse(r.content)
            print(f"  Entries: {len(feed.entries)}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
