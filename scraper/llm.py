import os
import json
from google import genai
from google.genai import types

# Supported tags in the frontend
VALID_TAGS = [
    'Décret', 'Circulaire', 'Arrêté', 'Pédagogie', 'Vie scolaire',
    'Actualité', 'Harcèlement', 'Absentéisme', 'Formation',
    'Numérique', 'Inclusion', 'Orientation'
]

def generate_summary_and_tags(title: str, text: str) -> dict:
    """Uses Gemini API to generate a concise summary and select appropriate tags."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Fallback if no API key is provided
        return {
            "description": text[:200] + "..." if len(text) > 200 else text,
            "tags": ["Actualité"]
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Tu es un assistant spécialisé pour les Conseillers Principaux d'Éducation (CPE).
    Analyse l'article suivant et fournis un résumé concis (2-3 phrases maximum) 
    qui met en évidence l'intérêt pour un CPE ou un candidat au concours CPE.
    Sélectionne également 1 à 3 tags pertinents parmi cette liste stricte : {", ".join(VALID_TAGS)}.
    
    Titre: {title}
    Contenu: {text[:1500]}
    
    IMPORTANT : Tu dois aussi déterminer si cet article est un "fait divers" (un incident, accident, délit ou fait de société spécifique qui s'est produit dans un établissement).
    Si c'est un fait divers, tu dois évaluer s'il est PERTINENT pour un CPE (c'est-à-dire s'il est lié aux problématiques comme le harcèlement, la violence, le handicap, l'inclusion, la santé mentale, la laïcité, etc.). Un simple fait divers sans enjeu éducatif ou de climat scolaire (ex: fuite d'eau, accident de la route sans lien avec l'école) n'est PAS pertinent.
    
    Réponds UNIQUEMENT au format JSON strict avec les clés "description" (string), "tags" (liste de strings), "is_fait_divers" (boolean) et "is_relevant_fait_divers" (boolean).
    Exemple: {{"description": "...", "tags": ["Harcèlement"], "is_fait_divers": true, "is_relevant_fait_divers": true}}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        
        result = json.loads(response.text)
        
        # Ensure tags are valid
        valid_result_tags = [tag for tag in result.get("tags", []) if tag in VALID_TAGS]
        if not valid_result_tags:
            valid_result_tags = ["Actualité"]
            
        return {
            "description": result.get("description", text[:200] + "..."),
            "tags": valid_result_tags[:3],
            "is_fait_divers": result.get("is_fait_divers", False),
            "is_relevant_fait_divers": result.get("is_relevant_fait_divers", False)
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "description": text[:200] + "..." if len(text) > 200 else text,
            "tags": ["Actualité"],
            "is_fait_divers": False,
            "is_relevant_fait_divers": False
        }
