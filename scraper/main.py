import os
from dotenv import load_dotenv
from feeds import fetch_and_parse_feeds
from keywords import is_relevant
from llm import generate_summary_and_tags
from supabase_client import get_supabase_client, get_existing_source_ids, insert_post

def main():
    # Load env vars for local development
    load_dotenv()
    
    print("Starting CPE Veille scraper...")
    
    # Initialize Supabase
    try:
        supabase = get_supabase_client()
        existing_ids = get_existing_source_ids(supabase)
        print(f"Found {len(existing_ids)} existing posts in database.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return

    # Fetch feeds
    items = fetch_and_parse_feeds()
    print(f"Fetched {len(items)} items from RSS feeds.")
    
    new_posts_count = 0
    
    for item in items:
        # Check if already processed
        if item["source_id"] in existing_ids:
            continue
            
        # Check relevance based on keywords
        if not is_relevant(item["title"], item["description"]):
            continue
            
        print(f"\nFound relevant new item: {item['title']}")
        
        # Generate summary and tags via LLM
        enriched_data = generate_summary_and_tags(item["title"], item["description"])
        
        # Prepare post object for database
        post_data = {
            "title": item["title"],
            "description": enriched_data["description"],
            "source_url": [item["link"]],
            "tags": enriched_data["tags"],
            "source_name": item["source_name"],
            "source_id": item["source_id"]
        }
        
        # Use published date from RSS if available, otherwise Supabase uses NOW()
        if item.get("published_at"):
            post_data["published_at"] = item["published_at"]
            
        # Insert into DB
        if insert_post(supabase, post_data):
            print(f"Successfully inserted: {item['title']}")
            new_posts_count += 1
            existing_ids.add(item["source_id"]) # Prevent duplicate in same run
            
    print(f"\nScraping complete. Added {new_posts_count} new posts.")

if __name__ == "__main__":
    main()
