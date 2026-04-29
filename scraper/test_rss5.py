import requests
import cloudscraper

urls = [
    "https://www.education.gouv.fr/rss.xml",
    "https://www.education.gouv.fr/rss"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

scraper = cloudscraper.create_scraper()

for url in urls:
    try:
        # Test with requests + User-Agent
        r1 = requests.get(url, headers=HEADERS, timeout=5)
        print(f"Requests {url}: {r1.status_code}")
        
        # Test with cloudscraper
        r2 = scraper.get(url, timeout=5)
        print(f"Cloudscraper {url}: {r2.status_code}")
        
        if r2.status_code == 200:
            print(f"Content snippet: {r2.text[:200]}")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
