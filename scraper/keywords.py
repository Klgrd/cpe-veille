KEYWORDS = [
    "conseiller principal d'éducation", "CPE", "vie scolaire",
    "lycée", "collège", "secondaire", "absentéisme", "décrochage",
    "harcèlement", "règlement intérieur", "exclusion", "sanctions",
    "chef d'établissement", "équipe éducative", "AESH",
    "pédagogie", "décret", "circulaire", "arrêté", "éducation nationale",
    "baccalauréat", "brevet", "orientation", "parcoursup"
]

def is_relevant(title: str, description: str) -> bool:
    """Checks if the item contains any of the CPE keywords."""
    text = f"{title} {description}".lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)
