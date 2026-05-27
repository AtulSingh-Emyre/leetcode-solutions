import requests
from datetime import datetime

LEETCODE_USERNAME = "Emyre"
GRAPHQL_URL = "https://leetcode.com"

ANALYTICS_QUERY = """
query userProfileUserQuestionProgressByDifficulty($username: String!) {
    matchedUser(username: $username) {
        submitStats {
            acSubmissionNum { difficulty count }
        }
        tagProblemCounts {
            advanced { tagName tagSlug problemsSolved }
            intermediate { tagName tagSlug problemsSolved }
            fundamental { tagName tagSlug problemsSolved }
        }
    }
}
"""

def generate_visual_bar(percentage, length=20):
    filled = int(round(length * (percentage / 100)))
    return "█" * filled + "░" * (length - filled)

def run_analytics_pipeline():
    print("Executing native GraphQL analytics dashboard compiler...")
    variables = {"username": LEETCODE_USERNAME}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{LEETCODE_USERNAME}/",
        "Origin": "https://leetcode.com"
    }
    try:
        resp = requests.post(GRAPHQL_URL, json={"query": ANALYTICS_QUERY, "variables": variables}, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"GraphQL Query blocked by server dashboard context. Status: {resp.status_code}")
            return
        
        data = resp.json().get('data', {}).get('matchedUser', {})
        if not data:
            print("Profile payload execution resolved to an empty container.")
            return

        stats = data['submitStats']['acSubmissionNum']
        solved_map = {item['difficulty']: item['count'] for item in stats}
        total_solved = solved_map.get('All', 0)
        
        tags = data['tagProblemCounts']
        all_tags = tags['advanced'] + tags['intermediate'] + tags['fundamental']
        sorted_tags = sorted(all_tags, key=lambda x: x['problemsSolved'], reverse=True)[:10]

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md = f"""# 📊 Algorithmic Metrics & Progress Dashboard
*Last automated sync: {now_str}*

## 📈 High-Level Vitals
- **Total Solved Problems:** {total_solved}
- **LeetCode Target Rank:** Top 1% Global Tier (Peak Rating: 2009 / Knight Badge)

### 🎯 Difficulty Distribution
"""
        for diff in ['Easy', 'Medium', 'Hard']:
            count = solved_map.get(diff, 0)
            pct = (count / total_solved * 100) if total_solved > 0 else 0
            bar = generate_visual_bar(pct)
            md += f"- **{diff}:** {count} solutions ({pct:.1f}%) | `{bar}`\n"

        md += "\n## 🏷️ Top 10 Problem-Solving Topic Allocations\n"
        md += "| Topic Category | Problems Resolved | Depth Graph |\n| :--- | :---: | :--- |\n"
        
        max_tag_solved = sorted_tags['problemsSolved'] if sorted_tags else 1
        for t in sorted_tags:
            t_count = t['problemsSolved']
            depth_pct = (t_count / max_tag_solved * 100)
            depth_bar = generate_visual_bar(depth_pct, length=10)
            md += f"| **{t['tagName']}** | {t_count} | `{depth_bar}` |\n"

        with open("analytics.md", "w", encoding="utf-8") as f:
            f.write(md)
        print("Successfully compiled and output native analytics.md file.")
    except Exception as e:
        print(f"Error compiling analytics dashboard dashboard: {e}")

if __name__ == "__main__":
    run_analytics_pipeline()
