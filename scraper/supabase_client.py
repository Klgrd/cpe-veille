import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        
    return create_client(url, key)

def get_existing_source_ids(supabase: Client) -> set:
    """Fetches all existing source_ids from the database to avoid duplicates."""
    try:
        response = supabase.table("posts").select("source_id").execute()
        return {item["source_id"] for item in response.data if item["source_id"]}
    except Exception as e:
        print(f"Error fetching existing IDs: {e}")
        return set()

def insert_post(supabase: Client, post_data: dict) -> bool:
    """Inserts a single post into the database."""
    try:
        supabase.table("posts").insert(post_data).execute()
        return True
    except Exception as e:
        print(f"Error inserting post {post_data.get('title')}: {e}")
        return False
