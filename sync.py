import os
import time
import requests
import difflib
from datetime import datetime

# Profile Settings
LEETCODE_USERNAME = "Emyre"
GRAPHQL_URL = "https://leetcode.com"

QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
    recentAcSubmissions(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
        lang
    }
}
"""

LANGUAGE_CONFIGS = {
    "python": {"ext": ".py", "comment": "#", "template": "class Solution:\n    def solve(self):\n        pass\n"},
    "python3": {"ext": ".py", "comment": "#", "template": "class Solution:\n    def solve(self):\n        pass\n"},
    "java": {"ext": ".java", "comment": "//", "template": "class Solution {\n    // Implementation\n}\n"},
    "cpp": {"ext": ".cpp", "comment": "//", "template": "class Solution {\npublic:\n    // Implementation\n};\n"},
    "javascript": {"ext": ".js", "comment": "//", "template": var solve = function() {\n};\n"},
    "typescript": {"ext": ".ts", "comment": "//", "template": "function solve(): void {}\n"},
    "kotlin": {"ext": ".kt", "comment": "//", "template": "class Solution {}\n"}
}

def fetch_recent_submissions():
    variables = {"username": LEETCODE_USERNAME, "limit": 20}
    try:
        response = requests.post(GRAPHQL_URL, json={"query": QUERY, "variables": variables})
        if response.status_code == 200:
            return response.json().get('data', {}).get('recentAcSubmissions', [])
    except Exception as e:
        print(f"API Error: {e}")
    return []

def calculate_similarity(old_file_path, new_template):
    """Calculates text variance against current file state."""
    try:
        with open(old_file_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
        # Using SequenceMatcher to gauge variance string limits
        matcher = difflib.SequenceMatcher(None, old_content, new_template)
        return matcher.ratio()
    except Exception:
        return 0.0

def run_versioned_sync():
    submissions = fetch_recent_submissions()
    if not submissions:
        print("No recent data fetched.")
        return

    current_time = time.time()
    one_day_ago = current_time - (24 * 3600)
    synced_any = False

    for sub in submissions:
        sub_time = int(sub['timestamp'])
        
        if sub_time >= one_day_ago:
            problem_slug = sub['titleSlug']
            problem_title = sub['title']
            leetcode_lang = sub['lang'].lower()
            
            lang_setup = LANGUAGE_CONFIGS.get(leetcode_lang, {"ext": ".txt", "comment": "#", "template": ""})
            os.makedirs(problem_slug, exist_ok=True)
            
            formatted_date = datetime.fromtimestamp(sub_time).strftime('%Y-%m-%d_%H-%M-%S')
            date_display = datetime.fromtimestamp(sub_time).strftime('%Y-%m-%d %H:%M:%S')
            comment_tag = lang_setup['comment']
            ext = lang_setup['ext']
            
            # Base text block initialization 
            file_body = f"{comment_tag} LeetCode Problem Title: {problem_title}\n"
            file_body += f"{comment_tag} Language: {sub['lang']}\n"
            file_body += f"{comment_tag} Reference: https://leetcode.com{problem_slug}/\n"
            file_body += f"{comment_tag} Synced: {date_display}\n\n"
            file_body += lang_setup['template']
            
            # Check for existing records matching this specific language extension
            existing_files = [f for f in os.listdir(problem_slug) if f.endswith(ext)]
            
            should_write = False
            target_filename = f"Solution{ext}"
            
            if not existing_files:
                # Scenario A: First time solving this problem in this programming language
                should_write = True
                target_filename = f"Solution{ext}"
            else:
                # Scenario B: Language exists. Check for codebase similarity updates
                # Target the latest historical version in that directory
                latest_existing_file = sorted(existing_files)[-1]
                full_old_path = os.path.join(problem_slug, latest_existing_file)
                
                similarity_score = calculate_similarity(full_old_path, file_body)
                
                # If variance is greater than 15% (similarity < 85%), trigger new version layout
                if similarity_score < 0.85:
                    should_write = True
                    target_filename = f"Solution_{formatted_date}{ext}"
                    print(f"Optimization detected for {problem_title} ({similarity_score:.2f} similarity). Saving version layer.")
            
            if should_write:
                final_path = os.path.join(problem_slug, target_filename)
                with open(final_path, "w", encoding="utf-8") as f:
                    f.write(file_body)
                print(f"Published solution tracking module: {final_path}")
                synced_any = True

    if not synced_any:
        print("No new problems or unique optimization profiles detected today.")

if __name__ == "__main__":
    run_versioned_sync()
