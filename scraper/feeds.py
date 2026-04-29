import feedparser
import re
import requests
from typing import List, Dict, Any

FEEDS = [
    {
        "name": "Légifrance",
        "url": "https://www.legifrance.gouv.fr/api/rss",
    },
    {
        "name": "BOEN",
        "url": "https://www.education.gouv.fr/bo/rss.xml",
    },
    {
        "name": "Café Pédagogique",
        "url": "https://www.cafepedagogique.net/feed/",
    },
    {
        "name": "MEN",
        "url": "https://www.education.gouv.fr/rss.xml",
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
            # Use requests with a browser User-Agent to bypass government anti-bot filters
            response = requests.get(feed_info["url"], headers=HEADERS, timeout=15)
            response.raise_for_status()
            
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
