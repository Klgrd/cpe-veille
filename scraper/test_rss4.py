import requests

urls = [
    "https://eduscol.education.fr/rss.xml",
    "https://www.service-public.fr/rss/actualites.xml",
    "https://www.senat.fr/rss/commission/cult.xml",
    "https://www.assemblee-nationale.fr/dyn/flux-rss"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*'
}

for url in urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
