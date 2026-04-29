import cloudscraper

scraper = cloudscraper.create_scraper()

print(scraper.get('https://www.education.gouv.fr/rss.xml').status_code)
print(scraper.get('https://www.legifrance.gouv.fr/api/rss').status_code)
