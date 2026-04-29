import feedparser
import re
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from typing import List, Dict, Any

FEEDS = [
    {
        "name": "Café Pédagogique",
        "url": "https://www.cafepedagogique.net/feed/",
    },
    {
        "name": "VousNousIls (L'e-mag de l'éducation)",
        "url": "https://www.vousnousils.fr/feed",
    },
    {
        "name": "Vie Publique",
        "url": "https://www.vie-publique.fr/rss",
    },
    {
        "name": "Sénat (Rapports)",
        "url": "https://www.senat.fr/rss/rapports.xml",
    },
    {
        "name": "SNES-FSU (Syndicat Éducation)",
        "url": "https://www.snes.edu/feed/",
    },
    {
        "name": "Google News (Faits divers école)",
        "url": "https://news.google.com/rss/search?q=%22fait+divers%22+(lyc%C3%A9e+OR+coll%C3%A8ge+OR+%C3%A9cole+OR+EPLE)&hl=fr&gl=FR&ceid=FR:fr",
    },
    {
        "name": "Bulletin Officiel (BOEN)",
        "url": "https://www.education.gouv.fr/le-bulletin-officiel-de-l-education-nationale-de-la-jeunesse-et-des-sports",
    }
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*'
}

def fetch_and_parse_feeds() -> List[Dict[str, Any]]:
    items = []
    for feed_info in FEEDS:
        try:
            if feed_info["name"] == "Bulletin Officiel (BOEN)":
                # Special HTML parsing for BOEN since they blocked RSS
                response = requests.get(feed_info["url"], impersonate="chrome120", timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                base_url = "https://www.education.gouv.fr"
                
                # Find latest BO link
                latest_bo_link = None
                for a in soup.find_all('a', href=True):
                    if re.search(r'/bo/\d+/Hebdo\d+', a['href']):
                        latest_bo_link = urljoin(base_url, a['href'])
                        break
                        
                if latest_bo_link:
                    r2 = requests.get(latest_bo_link, impersonate="chrome120", timeout=15)
                    soup2 = BeautifulSoup(r2.content, 'html.parser')
                    
                    for a in soup2.find_all('a', href=True):
                        if '/bo/' in a['href'] and a['href'] != latest_bo_link and len(a['href'].split('/')) > 4:
                            title = a.text.strip()
                            link = urljoin(base_url, a['href'])
                            if title:
                                items.append({
                                    "source_name": feed_info["name"],
                                    "title": title,
                                    "description": f"Nouvel article publié au Bulletin Officiel : {title}",
                                    "link": link,
                                    "source_id": link,
                                    "published_at": datetime.now().isoformat()
                                })
            else:
                # Standard RSS feed parsing using requests (curl_cffi) to bypass filters
                response = requests.get(feed_info["url"], impersonate="chrome120", headers=HEADERS, timeout=15)
                
                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    # Basic cleanup of title and description
                    title = entry.title if hasattr(entry, 'title') else ''
                    description = entry.description if hasattr(entry, 'description') else ''
                    link = entry.link if hasattr(entry, 'link') else ''
                    
                    # GUID or link as unique ID
                    source_id = entry.id if hasattr(entry, 'id') else link
    
                    items.append({
                        "source_name": feed_info["name"],
                        "title": title,
                        "description": re.sub(r'<[^>]+>', '', description), # Remove HTML tags
                        "link": link,
                        "source_id": source_id,
                        "published_at": entry.published if hasattr(entry, 'published') else None
                    })
        except Exception as e:
            print(f"Error parsing feed {feed_info['name']}: {e}")
    return items
