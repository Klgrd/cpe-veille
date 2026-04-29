import os
import requests
import json
from dotenv import load_dotenv
from notify import build_email_html

# Load local .env if exists
load_dotenv()

def test_new_design():
    api_key = os.environ.get("RESEND_API_KEY")
    from_email = os.environ.get("NOTIFY_FROM_EMAIL", "onboarding@resend.dev")
    to_email = "gaillardkylian@gmail.com"

    if not api_key:
        print("Erreur: RESEND_API_KEY manquante.")
        return

    # 1. Test avec des articles
    fake_posts = [
        {
            "title": "Nouveau décret sur le concours CPE 2026",
            "description": "Le ministère de l'Éducation nationale a publié ce matin les nouvelles modalités pour l'épreuve orale du concours externe de recrutement des CPE...",
            "source_name": "Légifrance",
            "link": "https://www.legifrance.gouv.fr"
        },
        {
            "title": "Analyse : L'évolution du métier de CPE en 2025",
            "description": "Un article passionnant du Café Pédagogique qui revient sur les enjeux de la vie scolaire et le rôle croissant du CPE dans l'accompagnement personnalisé.",
            "source_name": "Le Café Pédagogique",
            "link": "https://www.cafepedagogique.net"
        }
    ]

    print("--- Envoi du nouveau design (avec articles) ---")
    html_with_posts = build_email_html(fake_posts)
    send_mail(api_key, from_email, to_email, "Test Design : Nouveaux Articles", html_with_posts)

    # 2. Test sans articles (état vide)
    print("\n--- Envoi du nouveau design (vide / rien trouvé) ---")
    html_empty = build_email_html([])
    send_mail(api_key, from_email, to_email, "Test Design : Rien de neuf", html_empty)


def send_mail(api_key, from_addr, to_addr, subject, html):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": f"CPE Veille <{from_addr}>",
        "to": [to_addr],
        "subject": subject,
        "html": html
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    if resp.status_code in [200, 201]:
        print(f"Succes pour: {subject}")
    else:
        print(f"Echec ({resp.status_code}): {resp.text}")


if __name__ == "__main__":
    test_new_design()
