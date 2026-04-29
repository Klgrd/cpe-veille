import requests

urls = [
    "https://www.vousnousils.fr/feed",
    "https://www.education.gouv.fr/rss",
    "https://www.vie-publique.fr/rss"
]

for url in urls:
    try:
        r = requests.get(url, timeout=5)
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
