import feedparser
import re
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

def fetch_and_parse_feeds() -> List[Dict[str, Any]]:
    items = []
    for feed_info in FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
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
