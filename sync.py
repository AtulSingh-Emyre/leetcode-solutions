import os
import time
import requests
import difflib
from datetime import datetime

LEETCODE_USERNAME = "Emyre"
GRAPHQL_URL = "https://leetcode.com"

# Query 1: Get metadata for recent accepted submissions
SUBMISSIONS_QUERY = """
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

# Query 2: Fetch the actual source code text submitted for a specific submission ID
CODE_QUERY = """
query submissionDetails($submissionId: Int!) {
    submissionDetails(submissionId: $submissionId) {
        code
    }
}
"""

LANGUAGE_CONFIGS = {
    "python": {"ext": ".py", "comment": "#"},
    "python3": {"ext": ".py", "comment": "#"},
    "java": {"ext": ".java", "comment": "//"},
    "cpp": {"ext": ".cpp", "comment": "//"},
    "javascript": {"ext": ".js", "comment": "//"},
    "typescript": {"ext": ".ts", "comment": "//"},
    "kotlin": {"ext": ".kt", "comment": "//"}
}

def fetch_recent_submissions(csrf_token, session_token):
    print("\n--- [DEBUG LEVEL 1] SUBMISSIONS METADATA REQUEST ---")
    print(f"Target Username: '{LEETCODE_USERNAME}'")
    print(f"Target Endpoint: '{GRAPHQL_URL}'")
    
    variables = {"username": LEETCODE_USERNAME, "limit": 20}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/u/{LEETCODE_USERNAME}/",
        "Origin": "https://leetcode.com",
        "X-CSRFToken": csrf_token,
        "Cookie": f"csrftoken={csrf_token}; LEETCODE_SESSION={session_token};"
    }
    
    # Intentionally logging exactly what is being sent to verify malformations
    print(f"Constructed Header Referer: {headers['Referer']}")
    print(f"Sending metadata POST request now...")
    
    try:
        response = requests.post(GRAPHQL_URL, json={"query": SUBMISSIONS_QUERY, "variables": variables}, headers=headers, timeout=15)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✔ SUCCESS: Bypassed firewall for Metadata Query.")
            return response.json().get('data', {}).get('recentAcSubmissions', [])
        else:
            print(f"❌ 403 / BLOCK DETECTED ON METADATA FETCH")
            print(f"Full Response Header Dump: {dict(response.headers)}")
            print(f"Raw Server Response Body (First 500 chars):\n{response.text[:500]}")
    except Exception as e:
        print(f"💥 Network Layer Exception: {e}")
    return []

def fetch_submission_code(submission_id, csrf_token, session_token, problem_title):
    print(f"\n--- [DEBUG LEVEL 2] CODE PAYLOAD REQUEST FOR: {problem_title} ---")
    variables = {"submissionId": int(submission_id)}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/",
        "X-CSRFToken": csrf_token,
        "Cookie": f"csrftoken={csrf_token}; LEETCODE_SESSION={session_token};"
    }
    
    print(f"Sending code query POST request for ID {submission_id}...")
    try:
        response = requests.post(GRAPHQL_URL, json={"query": CODE_QUERY, "variables": variables}, headers=headers, timeout=15)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✔ SUCCESS: Bypassed firewall for Code Payload Query.")
            return response.json().get('data', {}).get('submissionDetails', {}).get('code', '')
        else:
            print(f"❌ 403 / BLOCK DETECTED ON CODE FETCH")
            print(f"Raw Server Response Body (First 500 chars):\n{response.text[:500]}")
    except Exception as e:
        print(f"💥 Network Layer Exception: {e}")
    return ""

def run_sync_pipeline():
    print("=== STARTING LEETCODE TO GITHUB SYNC PIPELINE ===")
    
    csrf_token = os.environ.get("LEETCODE_CSRF", "")
    session_token = os.environ.get("LEETCODE_SESSION", "")
    
    print(f"LEETCODE_CSRF present? {'Yes' if csrf_token else 'NO'}")
    print(f"LEETCODE_SESSION present? {'Yes' if session_token else 'NO'}")
    
    if not csrf_token or not session_token:
        print("Aborting: Environment variables missing.")
        return

    submissions = fetch_recent_submissions(csrf_token, session_token)
    if not submissions:
        return

    # Firewall checks pass if execution gets here; minimal logging below this line
    current_time = time.time()
    one_day_ago = current_time - (24 * 3600)
    processed_slugs = set()

    for sub in submissions:
        sub_time = int(sub['timestamp'])
        problem_slug = sub['titleSlug']
        
        if problem_slug in processed_slugs or sub_time < one_day_ago:
            continue
            
        actual_code = fetch_submission_code(sub['id'], csrf_token, session_token, sub['title'])
        if not actual_code:
            continue

        leetcode_lang = sub['lang'].lower()
        lang_setup = LANGUAGE_CONFIGS.get(leetcode_lang, {"ext": ".txt", "comment": "#"})
        os.makedirs(problem_slug, exist_ok=True)
        
        file_body = f"{lang_setup['comment']} LeetCode Problem Title: {sub['title']}\n\n{actual_code}"
        full_local_path = os.path.join(problem_slug, f"Solution{lang_setup['ext']}")
        
        with open(full_local_path, "w", encoding="utf-8") as f:
            f.write(file_body)
        
        processed_slugs.add(problem_slug)

if __name__ == "__main__":
    run_sync_pipeline()
