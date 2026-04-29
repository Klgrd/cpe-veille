import os
import requests
import json
from dotenv import load_dotenv
from notify import build_email_html

# Load local .env if exists
load_dotenv()

def test_brevo():
    api_key = os.environ.get("BREVO_API_KEY")
    # L'email que tu as verifie sur Brevo
    from_email = os.environ.get("NOTIFY_FROM_EMAIL", "gaillardkylian@gmail.com")
    # L'email destinataire (celui sans le .fr par exemple)
    to_email = "gaillardkylian@gmail.com"

    if not api_key:
        print("Erreur: BREVO_API_KEY manquante.")
        return

    print(f"--- Test Brevo : Envoi vers {to_email} ---")
    
    fake_posts = [
        {
            "title": "Brevo est operationnel !",
            "description": "Le systeme de veille a migre vers Brevo pour permettre l'envoi sans nom de domaine. Le design reste le meme.",
            "source_name": "SYSTEME",
            "link": "https://cpe-veille-k4oy.vercel.app"
        }
    ]

    html = build_email_html(fake_posts)
    
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "sender": {"name": "CPE Veille", "email": from_email},
        "to": [{"email": to_email}],
        "subject": "Test Brevo - CPE Veille",
        "htmlContent": html
    }

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if resp.status_code in [200, 201, 202]:
            print("Succes ! Le mail a ete envoye via Brevo.")
        else:
            print(f"Echec ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    test_brevo()
