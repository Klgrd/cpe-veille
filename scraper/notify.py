"""
notify.py — Send email notifications to subscribed users via Brevo (ex-Sendinblue).
"""

import os
import json
import requests
from datetime import datetime

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
# L'email de l'expéditeur DOIT être vérifié dans ton compte Brevo (Settings > Senders)
FROM_EMAIL = os.environ.get("NOTIFY_FROM_EMAIL", "gaillardkylian@gmail.com")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def get_subscribers() -> list[str]:
    """Fetch emails of users who opted in for notifications."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        return []

    url = f"{SUPABASE_URL}/rest/v1/notification_subscribers?select=email"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return [row["email"] for row in resp.json() if row.get("email")]
    except Exception:
        return []


def build_email_html(new_posts: list[dict]) -> str:
    """Build a FLASHY Neon-style HTML email body."""
    
    date_str = datetime.now().strftime("%d %B %Y").upper()
    
    if new_posts:
        header_title = f"{len(new_posts)} NOUVELLES ALERTES"
        header_subtitle = "Ton briefing quotidien est prêt. Découvre les dernières mises à jour du secteur."
        
        content_html = "".join(
            f"""
            <tr>
              <td style="padding:24px;background:rgba(255,255,255,0.03);border:1px solid rgba(161,255,0,0.2);border-radius:24px;margin-bottom:16px;display:block;">
                <p style="margin:0 0 8px;font-size:10px;font-weight:900;color:#a1ff00;text-transform:uppercase;letter-spacing:0.2em;">
                  {post.get('source_name', 'SOURCE OFFICIELLE')}
                </p>
                <a href="{post.get('link', '#')}"
                   style="font-size:19px;font-weight:800;color:#ffffff;text-decoration:none;line-height:1.3;display:block;">
                  {post.get('title', 'Sans titre')}
                </a>
                <p style="margin:12px 0 0;font-size:14px;color:#9ca3af;line-height:1.6;">
                   {post.get('description', '')[:180]}{'...' if len(post.get('description', '')) > 180 else ''}
                </p>
                <div style="margin-top:16px;">
                  <a href="{post.get('link', '#')}" style="font-size:12px;font-weight:700;color:#a1ff00;text-decoration:none;">LIRE LA SUITE →</a>
                </div>
              </td>
            </tr>
            <tr><td style="height:16px;line-height:16px;">&nbsp;</td></tr>
            """
            for post in new_posts
        )
    else:
        header_title = "VEILLE EN COURS"
        header_subtitle = "Aucune nouvelle alerte détectée ces dernières 24 heures. On reste sur le coup."
        
        content_html = """
        <tr>
          <td style="padding:60px 40px;text-align:center;background:rgba(255,255,255,0.03);border:1px dashed rgba(161,255,0,0.3);border-radius:32px;display:block;">
            <div style="font-size:50px;margin-bottom:20px;">🛰️</div>
            <h2 style="font-size:20px;font-weight:800;color:#ffffff;margin:0 0 10px;">Rien à signaler</h2>
            <p style="font-size:15px;color:#9ca3af;margin:0;line-height:1.5;">
              Le flux est calme. Profites-en pour réviser tes classiques sur la plateforme !
            </p>
          </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0;padding:0;background-color:#050505;font-family:-apple-system,BlinkMacSystemFont,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#050505;padding:40px 10px;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;">
              
              <!-- Logo -->
              <tr>
                <td style="padding-bottom:30px;text-align:center;">
                  <div style="display:inline-block;padding:8px 20px;background:#111;border:1px solid #333;border-radius:999px;">
                    <span style="font-size:14px;font-weight:900;color:#ffffff;letter-spacing:0.1em;">CPE VEILLE</span>
                  </div>
                </td>
              </tr>

              <!-- Card -->
              <tr>
                <td style="background:#0f0f0f;border:1px solid #1f1f1f;border-radius:40px;overflow:hidden;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding:50px 40px 40px;border-bottom:1px solid #1f1f1f;">
                        <p style="margin:0;font-size:11px;font-weight:900;letter-spacing:0.3em;color:#a1ff00;text-transform:uppercase;">
                          {date_str}
                        </p>
                        <h1 style="margin:16px 0 0;font-size:36px;font-weight:900;color:#ffffff;line-height:1.1;">
                          {header_title}
                        </h1>
                        <p style="margin:16px 0 0;font-size:16px;color:#9ca3af;line-height:1.6;">
                          {header_subtitle}
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:40px;">
                        <table width="100%" cellpadding="0" cellspacing="0">
                          {content_html}
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 40px 50px;text-align:center;">
                        <a href="https://cpe-veille-k4oy.vercel.app"
                           style="display:inline-block;width:100%;padding:18px 0;background:#a1ff00;color:#000000;font-weight:900;font-size:15px;text-transform:uppercase;border-radius:20px;text-decoration:none;">
                          Accéder au Dashboard
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding:40px 20px;text-align:center;">
                  <p style="margin:0;font-size:12px;color:#444;line-height:1.6;">
                    PROPULSÉ PAR L'IA • CPE VEILLE 2026<br>
                    <a href="https://cpe-veille-k4oy.vercel.app" style="color:#666;text-decoration:none;font-weight:700;">GÉRER MES ALERTES</a>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def send_notification_emails(new_posts: list[dict]) -> None:
    """Send flashy neon emails via Brevo API."""
    if not BREVO_API_KEY:
        print("[notify] BREVO_API_KEY missing.")
        return

    subscribers = get_subscribers()
    if not subscribers:
        print("[notify] No subscribers.")
        return

    html = build_email_html(new_posts)
    subject = f"⚡ {'ALERTES' if new_posts else 'VEILLE'} : CPE VEILLE — {datetime.now().strftime('%d/%m')}"

    # Brevo allows sending to multiple recipients in one call
    payload = {
        "sender": {"name": "CPE Veille", "email": FROM_EMAIL},
        "to": [{"email": email} for email in subscribers],
        "subject": subject,
        "htmlContent": html
    }

    try:
        resp = requests.post(
            BREVO_API_URL,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            data=json.dumps(payload),
            timeout=15
        )
        if resp.status_code in [200, 201]:
            print(f"[notify] ✓ Emails sent via Brevo to {len(subscribers)} subscribers.")
        else:
            print(f"[notify] ✗ Brevo error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[notify] ✗ Failed to send via Brevo: {e}")
