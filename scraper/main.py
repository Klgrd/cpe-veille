import os
from dotenv import load_dotenv
from feeds import fetch_and_parse_feeds
from keywords import is_relevant
from llm import generate_summary_and_tags
from supabase_client import get_existing_source_ids, insert_post
from notify import send_notification_emails

def main():
    # Load env vars for local development
    load_dotenv()
    
    print("Starting CPE Veille scraper...")
    
    # Diagnostic des variables d'environnement
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    gemini = os.environ.get("GEMINI_API_KEY")
    
    missing = []
    if not url: missing.append("SUPABASE_URL")
    if not key: missing.append("SUPABASE_SERVICE_ROLE_KEY")
    if not gemini: missing.append("GEMINI_API_KEY")
    
    if missing:
        print(f"🛑 ERREUR CRITIQUE : Variables manquantes : {', '.join(missing)}")
        print("Vérifiez vos secrets GitHub (Settings > Secrets and variables > Actions)")
        return

    # Initialize connection check
    try:
        existing_ids = get_existing_source_ids()
        print(f"Found {len(existing_ids)} existing posts in database.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return

    # Fetch feeds
    items = fetch_and_parse_feeds()
    print(f"Fetched {len(items)} items from RSS feeds.")
    
    new_posts_count = 0
    added_items = []
    ignored_items = []
    failed_items = []
    skipped_existing = 0
    faits_divers_count = 0
    
    for item in items:
        # Check if already processed
        if item["source_id"] in existing_ids:
            skipped_existing += 1
            continue
            
        # Check relevance based on keywords
        if not is_relevant(item["title"], item["description"]):
            ignored_items.append(item)
            continue
            
        print(f"\nFound relevant new item: {item['title']}")
        
        # Generate summary and tags via LLM
        enriched_data = generate_summary_and_tags(item["title"], item["description"])
        
        # Fait divers logic
        if enriched_data.get("is_fait_divers"):
            if not enriched_data.get("is_relevant_fait_divers"):
                print(f"Ignoré: Fait divers non pertinent ({item['title']})")
                ignored_items.append(item)
                continue
                
            if faits_divers_count >= 1:
                print(f"Ignoré: Quota de 1 fait divers atteint ({item['title']})")
                ignored_items.append(item)
                continue
                
            faits_divers_count += 1
            
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
            # Ensure it's in a format Postgres likes (ISO)
            post_data["published_at"] = item["published_at"]
            
        # Insert into DB
        success, error_msg = insert_post(post_data)
        if success:
            print(f"Successfully inserted: {item['title']}")
            new_posts_count += 1
            added_items.append(item)
            existing_ids.add(item["source_id"]) # Prevent duplicate in same run
        else:
            print(f"FAILED to insert: {item['title']} - {error_msg}")
            item["error"] = error_msg
            failed_items.append(item)
            
    print(f"\nScraping complete. Added {new_posts_count} new posts.")

    # Send daily briefing email to subscribers
    send_notification_emails(added_items)
    
    # Write to GitHub Step Summary if running in GitHub Actions
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write("### 🤖 Rapport de Scraping CPE Veille\n\n")
                f.write(f"- **Total d'articles récupérés (RSS) :** {len(items)}\n")
                f.write(f"- **Articles ignorés (déjà en base) :** {skipped_existing}\n")
                
                if new_posts_count == 0:
                    f.write("- **Résultat :** 🛑 Aucun nouvel article pertinent ajouté aujourd'hui.\n\n")
                else:
                    f.write(f"- **Résultat :** ✅ **{new_posts_count}** nouveaux articles ajoutés.\n\n")
                
                if failed_items:
                    f.write(f"- **⚠️ Erreurs :** {len(failed_items)} articles n'ont pas pu être insérés en base.\n\n")
                    
                if added_items:
                    f.write("#### ✨ Nouveaux articles publiés :\n")
                    for it in added_items:
                        f.write(f"- [{it['title']}]({it['link']})\n")
                    f.write("\n")
                    
                if failed_items:
                    f.write("#### ❌ Articles en erreur (Échec insertion) :\n")
                    # Show the first few errors specifically
                    for it in failed_items[:10]:
                        f.write(f"- {it['title']} : `{it.get('error')}`\n")
                    if len(failed_items) > 10:
                        f.write(f"- ... et {len(failed_items) - 10} autres articles.\n")
                    f.write("\n")

                if ignored_items:
                    f.write("<details><summary>🔍 Voir les articles analysés mais ignorés (hors-sujet)</summary>\n\n")
                    for it in ignored_items:
                        f.write(f"- [{it['title']}]({it['link']})\n")
                    f.write("\n</details>\n")
                    
        except Exception as e:
            print(f"Could not write to GitHub Step Summary: {e}")

if __name__ == "__main__":
    main()
