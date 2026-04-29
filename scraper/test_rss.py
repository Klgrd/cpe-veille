import feedparser
import urllib.request

urls = [
    "https://www.legifrance.gouv.fr/api/rss",
    "https://www.education.gouv.fr/bo/rss.xml",
    "https://www.cafepedagogique.net/feed/",
    "https://www.education.gouv.fr/rss.xml"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        print(f"{url}: {res.status}")
        
        feed = feedparser.parse(url)
        print(f"  Entries: {len(feed.entries)}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
