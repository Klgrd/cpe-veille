"""
notify.py — Send email notifications to subscribed users via Resend.

Required env vars:
  RESEND_API_KEY         — Your Resend API key (https://resend.com)
  SUPABASE_URL           — Supabase project URL
  SUPABASE_SERVICE_KEY   — Supabase service role key (to read notification_subscribers)
  NOTIFY_FROM_EMAIL      — Sender email address (must be verified on Resend)
"""

import os
import json
import requests

RESEND_API_URL = "https://api.resend.com/emails"
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("NOTIFY_FROM_EMAIL", "noreply@cpe-veille.fr")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def get_subscribers() -> list[str]:
    """Fetch emails of users who opted in for notifications via Supabase."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("[notify] Missing Supabase credentials — skipping subscriber fetch.")
        return []

    url = f"{SUPABASE_URL}/rest/v1/notification_subscribers?select=email"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [row["email"] for row in data if row.get("email")]
    except Exception as e:
        print(f"[notify] Could not fetch subscribers: {e}")
        return []


def build_email_html(new_posts: list[dict]) -> str:
    """Build a clean HTML email body with the list of new posts."""
    items_html = "".join(
        f"""
        <tr>
          <td style="padding:12px 0;border-bottom:1px solid #e5e5e5;">
            <a href="{post.get('link', '#')}"
               style="font-size:15px;font-weight:600;color:#111;text-decoration:none;">
              {post.get('title', 'Sans titre')}
            </a>
            <p style="margin:4px 0 0;font-size:13px;color:#666;">
              {post.get('source_name', 'CPE Veille')}
            </p>
          </td>
        </tr>
        """
        for post in new_posts
    )

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;background:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:40px 20px;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0"
                   style="background:#fff;border-radius:20px;overflow:hidden;border:1px solid #e5e5e5;">

              <!-- Header -->
              <tr>
                <td style="padding:32px 36px 24px;border-bottom:1px solid #e5e5e5;">
                  <p style="margin:0;font-size:13px;font-weight:700;letter-spacing:0.05em;color:#888;text-transform:uppercase;">
                    CPE Veille
                  </p>
                  <h1 style="margin:8px 0 0;font-size:24px;font-weight:800;color:#111;">
                    {len(new_posts)} nouveau{'x' if len(new_posts) > 1 else ''} article{'s' if len(new_posts) > 1 else ''} publié{'s' if len(new_posts) > 1 else ''}
                  </h1>
                </td>
              </tr>

              <!-- Articles list -->
              <tr>
                <td style="padding:16px 36px 8px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    {items_html}
                  </table>
                </td>
              </tr>

              <!-- CTA -->
              <tr>
                <td style="padding:24px 36px 32px;text-align:center;">
                  <a href="https://cpe-veille.vercel.app"
                     style="display:inline-block;padding:14px 32px;background:#a1ff00;color:#000;font-weight:700;font-size:14px;border-radius:999px;text-decoration:none;">
                    Voir sur CPE Veille →
                  </a>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding:16px 36px 24px;border-top:1px solid #e5e5e5;text-align:center;">
                  <p style="margin:0;font-size:11px;color:#aaa;">
                    Tu reçois cet email car tu as activé les alertes sur CPE Veille.<br>
                    Tu peux les désactiver depuis ton profil.
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
    """Main entry point: fetch subscribers and send them an email."""
    if not new_posts:
        print("[notify] No new posts — no email to send.")
        return

    if not RESEND_API_KEY:
        print("[notify] RESEND_API_KEY not set — skipping email notifications.")
        return

    subscribers = get_subscribers()
    if not subscribers:
        print("[notify] No subscribers found.")
        return

    print(f"[notify] Sending notifications to {len(subscribers)} subscriber(s)...")

    html = build_email_html(new_posts)
    subject = (
        f"📰 {len(new_posts)} nouvel article CPE Veille"
        if len(new_posts) == 1
        else f"📰 {len(new_posts)} nouveaux articles CPE Veille"
    )

    success = 0
    for email in subscribers:
        payload = {
            "from": f"CPE Veille <{FROM_EMAIL}>",
            "to": [email],
            "subject": subject,
            "html": html,
        }
        try:
            resp = requests.post(
                RESEND_API_URL,
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(payload),
                timeout=15,
            )
            resp.raise_for_status()
            success += 1
            print(f"[notify] ✓ Email sent to {email}")
        except Exception as e:
            print(f"[notify] ✗ Failed to send to {email}: {e}")

    print(f"[notify] Done. {success}/{len(subscribers)} emails sent.")
