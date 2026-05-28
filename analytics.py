import os
import re
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
USERNAME = "Emyre"
REPO_NAME = "leetcode-solutions"
# ---------------------

def parse_local_repo():
    """Scans local folders and matches clean, context-filtered tags entirely offline."""
    solved_problems = []
    current_dir = os.getcwd()
    leethub_folder_pattern = re.compile(r"^\d{4}-")
    
    # Advanced vs Basic tag configuration for the filtering engine
    basic_noise_tags = {"Array", "String", "Math", "Sorting"}

    for folder in os.listdir(current_dir):
        if os.path.isdir(folder) and leethub_folder_pattern.match(folder):
            readme_path = os.path.join(folder, "README.md")
            if not os.path.exists(readme_path):
                continue
                
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            difficulty = "Easy"
            if "Medium" in content: difficulty = "Medium"
            elif "Hard" in content: difficulty = "Hard"
            
            stat = os.stat(readme_path)
            solved_date = datetime.fromtimestamp(stat.st_mtime)
            
            # --- INTELLIGENT OFFLINE HEURISTIC ---
            # Isolate the title slug (e.g. 'longest-common-suffix-queries')
            title_slug = folder.split("-", 1)[1].lower().replace("-", " ")
            
            matched_topics = set()
            
            # 1. Structural Rules (Matches full conceptual phrases inside the problem description)
            structural_rules = {
                "Trie": ["trie", "prefix tree", "suffix tree", "suffix query", "suffix queries", "common suffix"],
                "Linked List": ["linked list", "list node", "reverse list", "palindrome list"],
                "Segment Tree": ["segment tree", "fenwick", "binary indexed tree", "range query"],
                "Union Find": ["union find", "disjoint set", "connected components"],
                "Heap / Priority Queue": ["priority queue", "kth largest", "merge k sorted"],
                "Monotonic Stack": ["monotonic stack", "next greater element", "daily temperatures"],
                "Sliding Window": ["sliding window", "longest substring without", "subarrays with k"],
                "Two Pointers": ["two pointers", "two pointer", "container with most water", "3sum"],
                "Binary Search": ["binary search", "search in rotated", "find first and last"],
                "Bit Manipulation": ["bit manipulation", "bitwise", "number of 1 bits", "single number"],
                "Dynamic Programming": ["dynamic programming", "coin change", "longest common subsequence", "knapsack"],
                "Graph": ["graph", "shortest path", "bipartite", "course schedule", "clone graph", "number of islands"],
                "Tree": ["binary tree", "lowest common ancestor", "tree diameter", "bst", "binary search tree"],
                "Prefix Sum": ["prefix sum", "subarray sum equals k", "running sum"],
                "Design": ["lru cache", "lfu cache", "design hit counter", "implement stack using"],
                # Fallback Basic Concepts
                "String": ["string", "palindrome", "anagram", "substring"],
                "Array": ["array", "matrix", "vector", "subarray", "grid"],
                "Math": ["math", "gcd", "lcm", "prime factor", "pow(x, n)"]
            }

            # Map concepts based on text patterns found in the title slug or description content
            for topic, keywords in structural_rules.items():
                for keyword in keywords:
                    # Look for standalone keywords inside the problem text context
                    if keyword in title_slug or f" {keyword} " in f" {content.lower()} ":
                        matched_topics.add(topic)
                        break

            # 2. Smart Filtering Layer
            has_advanced_tag = any(tag not in basic_noise_tags for tag in matched_topics)
            if has_advanced_tag:
                # If an advanced tag is found, strip out basic container keywords like Array/String
                topics = [tag for tag in matched_topics if tag not in basic_noise_tags]
            else:
                topics = list(matched_topics) if matched_topics else ["General"]
            
            # Clean up title rendering securely
            clean_title = folder.split("-", 1)[1].replace("-", " ").title()
            
            solved_problems.append({
                "title": clean_title,
                "folder": folder,
                "difficulty": difficulty,
                "date": solved_date,
                "topics": topics
            })
            
    return solved_problems

def generate_analytics(problems):
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    stats = {
        "total": len(problems), "easy": 0, "medium": 0, "hard": 0,
        "week_count": 0, "month_count": 0,
        "week_topics": {}, "month_topics": {}
    }
    
    for p in problems:
        # Global counts
        if p["difficulty"] == "Easy": stats["easy"] += 1
        elif p["difficulty"] == "Medium": stats["medium"] += 1
        elif p["difficulty"] == "Hard": stats["hard"] += 1
        
        # Weekly Analytics
        if p["date"] >= week_ago:
            stats["week_count"] += 1
            for t in p["topics"]:
                stats["week_topics"][t] = stats["week_topics"].get(t, 0) + 1
                
        # Monthly Analytics
        if p["date"] >= month_ago:
            stats["month_count"] += 1
            for t in p["topics"]:
                stats["month_topics"][t] = stats["month_topics"].get(t, 0) + 1
                
    return stats

def write_readme(stats, problems):
    # Sort recent problems to show on the dashboard
    problems.sort(key=lambda x: x["date"], reverse=True)
    recent_rows = ""
    
    # Helper to clean labels for Shields.io URL compatibility
    def clean_label(text):
        text = str(text)
        text = text.replace("-", "--")      # Shields.io format for literal dash
        text = text.replace("%", "%25")     # URL encode percent sign
        text = text.replace(" ", "%20")     # URL encode space
        text = text.replace("/", "%2F")     # URL encode slash
        return text
    
    for p in problems[:5]:
        date_str = p["date"].strftime("%b %d, %Y")
        
        # --- DYNAMIC DIFFICULTY BADGES ---
        if p['difficulty'] == "Hard":
            diff_badge = '<img src="https://img.shields.io/badge/Hard-🔴-red?style=flat-square" alt="Hard">'
        elif p['difficulty'] == "Medium":
            diff_badge = '<img src="https://img.shields.io/badge/Medium-🟡-yellow?style=flat-square" alt="Medium">'
        else:
            diff_badge = '<img src="https://img.shields.io/badge/Easy-🟢-green?style=flat-square" alt="Easy">'
            
        # --- HTML TAG CLOUD FOR CORE CONCEPTS ---
        tag_badges = []
        for tag in p['topics']:
            safe_tag = clean_label(tag)
            tag_badges.append(f'<img src="https://img.shields.io/badge/{safe_tag}-blue?style=flat-square" alt="{tag}">')
        tag_str = " ".join(tag_badges)
        
        recent_rows += f"| {date_str} | [{p['title']}](./{p['folder']}) | {diff_badge} | {tag_str} |\n"

    # Convert topic dicts to formatted markdown fragments
    def dict_to_md_list(d):
        if not d: return "None recorded yet."
        sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        return " ".join([f"📈 `{topic} ({count})`" for topic, count in sorted_d])

    # --- PROGRESS CALCULATION FOR SHIELD BARS ---
    total = stats['total'] if stats['total'] > 0 else 1
    easy_pct = round((stats['easy'] / total) * 100)
    med_pct = round((stats['medium'] / total) * 100)
    hard_pct = round((stats['hard'] / total) * 100)

    # Sanitize the header badge values to prevent bad URLs - don't encode for display text
    safe_easy_lbl = clean_label(f"Easy ({easy_pct}%)")
    safe_med_lbl = clean_label(f"Medium ({med_pct}%)")
    safe_hard_lbl = clean_label(f"Hard ({hard_pct}%)")
    safe_week_vel = clean_label(f"{stats['week_count']} problems / wk")
    safe_month_vel = clean_label(f"{stats['month_count']} problems / mo")
    safe_total = clean_label(f"{stats['total']}")

    # Create readable display versions without encoding
    display_easy = f"Easy ({easy_pct}%)"
    display_med = f"Medium ({med_pct}%)"
    display_hard = f"Hard ({hard_pct}%)"
    display_week_vel = f"{stats['week_count']} problems / wk"
    display_month_vel = f"{stats['month_count']} problems / mo"

    readme_content = f"""# 💻 LeetCode Engineering Portfolio

Welcome! This repository hosts my validated algorithmic solutions, automatically synced via LeetHub 2.0 and processed by an autonomous analytics dashboard workflow. It showcases my data structure expe[...]

---

## 📊 Core Performance Metrics

<p align="left">
  <img src="https://img.shields.io/badge/Total%20Solved-{safe_total}-7A1FA2?style=for-the-badge&logo=leetcode" alt="Total Solved">
  <img src="https://img.shields.io/badge/{safe_easy_lbl}-{stats['easy']}-2E7D32?style=for-the-badge" alt="{display_easy}">
  <img src="https://img.shields.io/badge/{safe_med_lbl}-{stats['medium']}-F57C00?style=for-the-badge" alt="{display_med}">
  <img src="https://img.shields.io/badge/{safe_hard_lbl}-{stats['hard']}-C62828?style=for-the-badge" alt="{display_hard}">
</p>


| Metric | Overview Progress Summary |
| :--- | :--- |
| **Weekly Velocity** | <img src="https://img.shields.io/badge/{safe_week_vel}-blue?style=flat-square" alt="{display_week_vel}"> |
| **Monthly Velocity** | <img src="https://img.shields.io/badge/{safe_month_vel}-blue?style=flat-square" alt="{display_month_vel}"> |

---

## ⏱️ Time-Frame Analytics (Recruiter Dashboard)

### 📅 Past 7 Days (Velocity: {stats['week_count']} Problems)
* **Core Topics Mastered This Week:** {dict_to_md_list(stats['week_topics'])}

### 📅 Past 30 Days (Velocity: {stats['month_count']} Problems)
* **Core Topics Mastered This Month:** {dict_to_md_list(stats['month_topics'])}

---

## 🕒 Recent Submissions Activity Log


| Date | Problem Title | Difficulty | Core Concept Tags |
| :--- | :--- | :--- | :--- |
{recent_rows}

---
<p align="center">
  <img src="https://img.shields.io/badge/Last%20Updated-{datetime.now().strftime('%Y%m%d')}-blue" alt="Workflow Status">
</p>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✔ README.md successfully updated with high-end, escaped Shields.io badges.")

if __name__ == "__main__":
    problems_list = parse_local_repo()
    metrics = generate_analytics(problems_list)
    write_readme(metrics, problems_list)
