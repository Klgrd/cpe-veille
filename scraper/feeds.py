import feedparser
import re
import time
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
    },
    {
        "name": "OZP",
        "url": "https://www.ozp.fr/spip.php?page=backend",
    },
    {
        "name": "Eduscol",
        "url": "https://eduscol.education.gouv.fr/",
    },
    {
        "name": "Réseau Canopé",
        "url": "https://www.reseau-canope.fr/actualites.html",
    },
    {
        "name": "IH2EF",
        "url": "https://www.ih2ef.gouv.fr/actualites",
    },
    {
        "name": "Centre Alain Savary",
        "url": "https://ife.ens-lyon.fr/presentation/equipes/centre-alain-savary",
    }
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*'
}

FRENCH_MONTHS = {
    'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06',
    'juillet': '07', 'août': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12',
    'janv.': '01', 'févr.': '02', 'avr.': '04', 'sept.': '09', 'oct.': '10', 'nov.': '11', 'déc.': '12'
}

def parse_french_date(date_str: str) -> str:
    """Converts a French date like 'Mis à jour le 18 mai 2026' into ISO format."""
    try:
        clean_str = date_str.lower().strip()
        clean_str = clean_str.replace("mis à jour le", "").replace("publié le", "").strip()
        
        match = re.search(r'(\d+)\s+([a-zéû\.]+)\s+(\d{4})', clean_str)
        if match:
            day, month_str, year = match.groups()
            month = FRENCH_MONTHS.get(month_str, '01')
            day = f"{int(day):02d}"
            return f"{year}-{month}-{day}T00:00:00"
    except Exception as e:
        print(f"Error parsing French date '{date_str}': {e}")
    return datetime.now().isoformat()

def fetch_and_parse_feeds() -> List[Dict[str, Any]]:
    items = []
    for feed_info in FEEDS:
        try:
            name = feed_info["name"]
            url = feed_info["url"]
            print(f"Parsing feed/site: {name} ({url})...")
            
            if name == "Bulletin Officiel (BOEN)":
                # Special HTML parsing for BOEN since they blocked RSS
                response = requests.get(url, impersonate="chrome120", timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                base_url = "https://www.education.gouv.fr"
                
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
                                    "source_name": name,
                                    "title": title,
                                    "description": f"Nouvel article publié au Bulletin Officiel : {title}",
                                    "link": link,
                                    "source_id": link,
                                    "published_at": datetime.now().isoformat()
                                })
                                
            elif name == "Eduscol":
                response = requests.get(url, impersonate="chrome120", timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.find_all('div', class_='fr-card')
                
                seen_links = set()
                for card in cards:
                    title_el = card.find('h3', class_='fr-card__title')
                    if not title_el:
                        continue
                    a = title_el.find('a')
                    if not a:
                        continue
                    
                    title = a.text.strip()
                    link = urljoin(url, a['href'])
                    
                    if link in seen_links:
                        continue
                    seen_links.add(link)
                    
                    desc_el = card.find('p', class_='fr-card__desc') or card.find('p')
                    description = desc_el.text.strip() if desc_el else f"Article d'actualité sur Éduscol : {title}"
                    
                    items.append({
                        "source_name": name,
                        "title": title,
                        "description": description,
                        "link": link,
                        "source_id": link,
                        "published_at": datetime.now().isoformat()
                    })
                    
            elif name == "Réseau Canopé":
                response = requests.get(url, impersonate="chrome120", timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.find_all('div', class_=lambda c: c and 'card' in str(c) and 'article' in str(c))
                
                seen_links = set()
                for card in cards:
                    a = card.find('a', class_='card__link')
                    if not a:
                        continue
                    
                    title = a.text.strip()
                    if not title:
                        span = a.find('span', itemprop='headline')
                        if span:
                            title = span.text.strip()
                    if not title:
                        continue
                        
                    link = urljoin(url, a['href'])
                    if link in seen_links:
                        continue
                    seen_links.add(link)
                    
                    desc_el = card.find('div', itemprop='description')
                    description = desc_el.text.strip() if desc_el else f"Actualité Réseau Canopé : {title}"
                    
                    pub_date = None
                    time_el = card.find('time', itemprop='datePublished')
                    if time_el and time_el.get('datetime'):
                        pub_date = time_el['datetime'] + "T00:00:00"
                    else:
                        date_el = card.find('span', class_='news-list-date')
                        if date_el:
                            pub_date = parse_french_date(date_el.text)
                    if not pub_date:
                        pub_date = datetime.now().isoformat()
                        
                    items.append({
                        "source_name": name,
                        "title": title,
                        "description": description,
                        "link": link,
                        "source_id": link,
                        "published_at": pub_date
                    })
                    
            elif name == "IH2EF":
                response = requests.get(url, impersonate="chrome120", timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.find_all('div', class_='item bg-white')
                
                seen_links = set()
                for card in cards:
                    label_div = card.find('div', class_='label')
                    if not label_div:
                        continue
                    a = label_div.find('a')
                    if not a:
                        continue
                        
                    title = a.text.strip()
                    link = urljoin(url, a['href'])
                    
                    if link in seen_links:
                        continue
                    seen_links.add(link)
                    
                    desc_div = card.find('div', class_='description')
                    description = desc_div.text.strip() if desc_div else f"Actualité IH2EF : {title}"
                    
                    pub_date = None
                    date_p = card.find('p', class_='date')
                    if date_p:
                        pub_date = parse_french_date(date_p.text)
                    if not pub_date:
                        pub_date = datetime.now().isoformat()
                        
                    items.append({
                        "source_name": name,
                        "title": title,
                        "description": description,
                        "link": link,
                        "source_id": link,
                        "published_at": pub_date
                    })
                    
            elif name == "Centre Alain Savary":
                response = requests.get(url, impersonate="chrome120", timeout=15)
                soup = BeautifulSoup(response.content, 'html.parser')
                view = soup.find('div', class_='block-views-blockdernieres-ressources-p-block-1')
                
                if view:
                    view_content = view.find('div', class_='view-content')
                    if view_content:
                        rows = [c for c in view_content.children if c.name == 'div']
                        seen_links = set()
                        for row in rows:
                            title_div = row.find('div', class_='views-field-title')
                            if not title_div:
                                continue
                            a = title_div.find('a')
                            if not a:
                                continue
                                
                            title = a.text.strip()
                            link = urljoin(url, a['href'])
                            
                            if link in seen_links:
                                continue
                            seen_links.add(link)
                            
                            description = f"Nouvelle ressource publiée par le Centre Alain Savary : {title}"
                            
                            pub_date = None
                            date_div = row.find('div', class_='cartouche-content-type-absolute')
                            if date_div:
                                try:
                                    date_str = date_div.text.strip()
                                    dt = datetime.strptime(date_str, "%d/%m/%Y")
                                    pub_date = dt.isoformat()
                                except Exception as e:
                                    print(f"Error parsing date {date_div.text}: {e}")
                            if not pub_date:
                                pub_date = datetime.now().isoformat()
                                
                            items.append({
                                "source_name": name,
                                "title": title,
                                "description": description,
                                "link": link,
                                "source_id": link,
                                "published_at": pub_date
                            })
                            
            else:
                # Standard RSS feed parsing using requests (curl_cffi) to bypass filters
                response = requests.get(url, impersonate="chrome120", headers=HEADERS, timeout=15)
                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    title = entry.title if hasattr(entry, 'title') else ''
                    description = entry.description if hasattr(entry, 'description') else ''
                    link = entry.link if hasattr(entry, 'link') else ''
                    source_id = entry.id if hasattr(entry, 'id') else link
    
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime.fromtimestamp(time.mktime(entry.published_parsed)).isoformat()
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime.fromtimestamp(time.mktime(entry.updated_parsed)).isoformat()
                    elif hasattr(entry, 'published'):
                        pub_date = entry.published
                    elif hasattr(entry, 'updated'):
                        pub_date = entry.updated
                    else:
                        pub_date = datetime.now().isoformat()

                    items.append({
                        "source_name": name,
                        "title": title,
                        "description": re.sub(r'<[^>]+>', '', description), # Remove HTML tags
                        "link": link,
                        "source_id": source_id,
                        "published_at": pub_date
                    })
        except Exception as e:
            print(f"Error parsing feed/site {feed_info['name']}: {e}")
    return items
