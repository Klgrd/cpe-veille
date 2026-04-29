KEYWORDS = [
    # Le métier et les acteurs
    "conseiller principal d'éducation", "CPE", "vie scolaire", "chef d'établissement", 
    "équipe éducative", "equipe educative", "AESH", "délégué", "delegue",
    
    # Le cadre
    "lycée", "lycee", "collège", "college", "secondaire", "éducation nationale", "education nationale", "EPLE",
    
    # Problématiques et thèmes
    "absentéisme", "absenteisme", "décrochage", "decrochage", "harcèlement", "harcelement", 
    "cyberharcèlement", "cyberharcelement", "exclusion", "sanctions", "handicape", "inclusion", 
    "psychologie", "autorité éducative", "autorite educative", "bien être", "bien etre", 
    "santé mental", "sante mental", "compétences psychosociales", "competences psychosociales",
    "citoyenneté", "citoyennete", "éducation moral", "education moral", "développement durable", 
    "developpement durable", "sociologie", "numérique", "numerique", "climat scolaire", 
    "prioritaire", "égalité", "egalite", "carte scolaire", "addiction", "inégalité", "inegalite", 
    "laïcité", "laicite", "internat", "allophone", "relation parents", "médiation", "mediation", 
    "surveillance", "droit à l'éducation", "droit a l'education", "valeurs de la république", 
    "valeurs de la republique", "politique éducative", "politique educative", "suivi éducatif", 
    "suivi educatif", "organisation des EPLE", "structure des EPLE", "apprentissage", 
    "accompagnement", "projet d'établissement", "projet d'etablissement",
    
    # Officiel / Légal
    "règlement intérieur", "reglement interieur", "décret", "decret", "circulaire", "arrêté", "arrete", 
    "lois", "note de service", "recommandation",
    
    # Droits, Devoirs et Conditions de travail (Fonction Publique)
    "fonction publique", "statut", "neutralité", "neutralite", "neutralit", "réserve", "reserve", 
    "droits et devoirs", "salaire", "rémunération", "remuneration", "remunerat", "grève", "greve", 
    "syndicat", "mouvement social", "conditions de travail",
    
    # Pédagogie & Examens
    "pédagogie", "pedagogie", "pedagogiq", "baccalauréat", "baccalaureat", "brevet", "orientation", 
    "parcoursup", "réforme", "reforme", "certification", "pix", "évaluation", "evaluation", 
    "niveau scolaire", "concours",
    
    # Grands Enjeux, Débats et Acteurs de l'éducation
    "école", "ecole", "élève", "eleve", "enseignant", "professeur", "enseignement", 
    "éducation", "education", "système éducatif", "systeme educatif", "intelligence artificielle", 
    "IA", "TDAH", "TSA", "troubles dys", "neuroatypique", "débat", "debat"
]

def is_relevant(title: str, description: str) -> bool:
    """Checks if the item contains any of the CPE keywords."""
    text = f"{title} {description}".lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)
