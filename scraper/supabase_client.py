import os
import requests

def get_headers() -> dict:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

def get_supabase_url() -> str:
    url = os.environ.get("SUPABASE_URL")
    if not url:
        return ""
    # Ensure no trailing slash
    return url.rstrip('/')

def get_existing_source_ids(client=None) -> set:
    """Fetches all existing source_ids from the database to avoid duplicates."""
    # We ignore the `client` argument now, it was used for the Supabase SDK
    try:
        url = f"{get_supabase_url()}/rest/v1/posts?select=source_id"
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        
        data = response.json()
        return {item["source_id"] for item in data if item.get("source_id")}
    except Exception as e:
        print(f"Error fetching existing IDs: {e}")
        return set()

def insert_post(post_data: dict) -> tuple[bool, str]:
    """Inserts a single post into the database. Returns (success, error_message)."""
    try:
        url = f"{get_supabase_url()}/rest/v1/posts"
        response = requests.post(url, headers=get_headers(), json=post_data)
        if response.status_code >= 400:
            return False, f"HTTP {response.status_code}: {response.text}"
        return True, ""
    except Exception as e:
        return False, str(e)
