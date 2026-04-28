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
    
    Réponds UNIQUEMENT au format JSON strict avec les clés "description" (string) et "tags" (liste de strings).
    Exemple: {{"description": "Un nouveau décret modifie les sanctions...", "tags": ["Décret", "Vie scolaire"]}}
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
            "tags": valid_result_tags[:3]
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "description": text[:200] + "..." if len(text) > 200 else text,
            "tags": ["Actualité"]
        }
