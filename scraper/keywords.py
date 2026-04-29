KEYWORDS = [
    # Le métier et les acteurs
    "conseiller principal d'éducation", "CPE", "vie scolaire", "chef d'établissement", 
    "équipe éducative", "AESH", "délégué",
    
    # Le cadre
    "lycée", "collège", "secondaire", "éducation nationale", "EPLE",
    
    # Problématiques et thèmes
    "absentéisme", "décrochage", "harcèlement", "cyberharcèlement", "exclusion", 
    "sanctions", "handicape", "inclusion", "psychologie de l'adolescent", "psychologie de l'enfant",
    "autorité éducative", "bien être de l'enfant", "santé mental de l'ado", "santé mental de l'enfant",
    "compétences psychosociales", "éducation à la citoyenneté", "éducation moral et civique",
    "éducation développement durable", "sociologie de l'enfant", "sociologie de l'ado",
    "développement de l'enfant", "développement de l'ado", "éducation aux média et à l'information",
    "numérique à l'école", "climat scolaire", "éducation prioritaire", "égalité fille/garçon à l'école",
    "carte scolaire", "addiction à l'adolescence", "inégalité", "laïcité", "internat", 
    "élèves allophone", "relation parents école", "médiation entre pairs", "surveillance scolaire",
    "droit à l'éducation", "valeurs de la république", "politique éducative", "suivi éducatif",
    "organisation des EPLE", "structure des EPLE", "apprentissage", "accompagnement", "projet d'établissement", 
    "vie scolaire", "zone d'éducation prioritaire", "quartier prioritaire de la politique de la ville", "réseaux ambition réussite",
    "médiation", "parcours de formation", "réseaux de réussite scolaire", "contrat d'objectifs scolaire", "outil pédagogique", "outil éducatif",
    
    # Officiel / Légal
    "règlement intérieur", "décret", "circulaire", "arrêté", "lois", "note de service", 
    "recommandation officielle",
    
    # Droits, Devoirs et Conditions de travail (Fonction Publique)
    "fonction publique", "statut", "obligation de neutralité", "neutralit", "devoir de réserve", 
    "droits et devoirs", "salaire", "rémunération", "grève", "syndicat", 
    "mouvement social", "conditions de travail",
    
    # Pédagogie & Examens
    "pédagogie", "baccalauréat", "brevet", "orientation", "orientation scolaire", "parcoursup",
    "réforme du bac", "certification", "pix", "évaluation", "niveau scolaire", "concours",
    
    # Grands Enjeux, Débats et Acteurs de l'éducation
    "école", "ecole", "élève", "eleve", "enseignant", "professeur", "enseignement", 
    "éducation", "education", "système éducatif", "intelligence artificielle", "IA", 
    "TDAH", "TSA", "troubles dys", "neuroatypique", "débat"
]

def is_relevant(title: str, description: str) -> bool:
    """Checks if the item contains any of the CPE keywords."""
    text = f"{title} {description}".lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)
