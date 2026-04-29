import requests

urls = [
    "https://www.senat.fr/rss/projets.xml",
    "https://www.senat.fr/rss/rapports.xml",
    "https://www.vie-publique.fr/rss",
    "https://www.snes.edu/feed/"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for url in urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
