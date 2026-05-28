import os
import re
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
USERNAME = "Emyre"
REPO_NAME = "leetcode-solutions"
# ---------------------

def parse_local_repo():
    """Scans LeetHub folders to extract solved dates, difficulties, and tags."""
    solved_problems = []
    current_dir = os.getcwd()
    
    # Regex to match LeetHub folder convention: e.g., "0001-two-sum"
    leethub_folder_pattern = re.compile(r"^\d{4}-")
    
    for folder in os.listdir(current_dir):
        if os.path.isdir(folder) and leethub_folder_pattern.match(folder):
            readme_path = os.path.join(folder, "README.md")
            if not os.path.exists(readme_path):
                continue
                
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract basic info from the markdown LeetHub creates
            difficulty = "Easy"
            if "Medium" in content: difficulty = "Medium"
            elif "Hard" in content: difficulty = "Hard"
            
            # Get the exact time the solution file was created/last updated by LeetHub
            # To fall back if Git timestamps aren't present locally
            stat = os.stat(readme_path)
            solved_date = datetime.fromtimestamp(stat.st_mtime)
            
            # Simple keyword matching to infer topics from LeetHub's problem text
            topics = []
            content_lower = content.lower()
            
            # EXTENDED KEYWORDS: Added complex data structures and algorithms
            keywords = {
                # --- Advanced Data Structures ---
                "Trie": ["trie", "prefix tree", "suffix tree", "suffix query", "suffix queries"],
                "Segment Tree / Fenwick": ["segment tree", "fenwick tree", "binary indexed tree", "bit", "range query"],
                "Union Find (DSU)": ["union find", "dsu", "disjoint set", "connected component"],
                "Heap / Priority Queue": ["heap", "priority queue", "pq", "min-heap", "max-heap"],
                "Monotonic Stack / Queue": ["monotonic stack", "monotonic queue", "next greater element"],
                "Graph": ["graph", "dfs", "bfs", "matrix", "topological", "dijkstra", "mst", "kruskal", "prim", "shortest path"],
                "Tree": ["tree", "binary tree", "bst", "node", "lowest common ancestor", "lca", "subtree"],
                
                # --- NEW: Linear Data Structures ---
                "Linked List": ["linked list", "listnode", "singly linked", "doubly linked", "dummy node"],
                
                # --- Advanced Algorithmic Paradigms ---
                "Dynamic Programming": ["dynamic programming", "dp", "memoization", "tabulation", "knapsack", "lcs", "lis", "kadane"],
                "Recursion / Backtracking": ["backtracking", "recursion", "permutations", "combinations", "subset"],
                "Divide and Conquer": ["divide and conquer", "merge sort", "quick sort"],
                "Greedy": ["greedy", "interval", "huffman"],
                
                # --- Intermediate Patterns ---
                "Sliding Window": ["sliding window", "longest substring without repeating"],
                "Two Pointers": ["two pointers", "two-pointer", "slow fast pointer", "meeting rooms"],
                "Binary Search": ["binary search", "bisect", "search in rotated"],
                "Bit Manipulation": ["bit manipulation", "bitwise", "xor", "and", "or", "shift"],
                
                # --- NEW: Structural Patterns ---
                "Prefix Sum": ["prefix sum", "suffix sum", "running sum", "cumulative sum"],
                "Design": ["lru cache", "lfu cache", "design", "oops", "system design", "instantiate", "iterator"],
                "Simulation": ["simulation", "simulate", "robot", "game of life"],
                
                # --- Basic Concepts ---
                "Hash Table": ["hash table", "hash map", "dictionary", "hashset", "counter", "frequency map"],
                "Sorting": ["sort", "sorting", "sorted"],
                "String": ["string", "char", "substring", "palindrome", "anagram"],
                "Array": ["array", "vector", "matrix", "subarray", "grid"],
                "Math": ["math", "geometry", "gcd", "lcm", "prime", "modulo", "combinatorics", "probability", "base-"]
            }
                        # ... (Inside your parse_local_repo() loop, right after content_lower = content.lower()) ...

            # 1. Classify which tags are considered "Noise/Basic"
            basic_noise_tags = {"Array", "String", "Math"}
            
            matched_topics = []
            for topic, keys in keywords.items():
                for key in keys:
                    # \b ensures we match standalone words/phrases only
                    pattern = r'\b' + re.escape(key.lower()) + r'\b'
                    if re.search(pattern, content_lower):
                        matched_topics.append(topic)
                        break  # Move to the next topic group
            
            # 2. Filtering Layer: Check if any advanced tag was found
            has_advanced_tag = any(tag not in basic_noise_tags for tag in matched_topics)
            
            if has_advanced_tag:
                # Keep only the advanced tags, dropping Array, String, and Math
                topics = [tag for tag in matched_topics if tag not in basic_noise_tags]
            else:
                # If NO advanced tags were found, fallback to the basic tags found
                topics = matched_topics

            if not topics:
                topics.append("General")
                
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
    for p in problems[:5]:
        date_str = p["date"].strftime("%b %d, %Y")
        diff_badge = f"🔴 {p['difficulty']}" if p['difficulty'] == "Hard" else (f"🟡 {p['difficulty']}" if p['difficulty'] == "Medium" else f"🟢 {p['difficulty']}")
        recent_rows += f"| {date_str} | [{p['title']}](./{p['folder']}) | {diff_badge} | {', '.join(p['topics'])} |\n"

    # Convert topic dicts to formatted markdown fragments
    def dict_to_md_list(d):
        if not d: return "None recorded yet."
        sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        return " ".join([f"`{topic} ({count})`" for topic, count in sorted_d])

    readme_content = f"""# 💻 LeetCode Engineering Portfolio

Welcome! This repository hosts my validated algorithmic solutions, automatically synced via LeetHub 2.0 and processed by an autonomous analytics dashboard workflow. It showcases my data structure expertise, consistency, and clean code optimization.

---

## 📊 Core Performance Metrics



| Metric | Overview Progress Summary |
| :--- | :--- |
| **Total Solved** | **{stats['total']}** problems completed |
| **Difficulty Mix** | 🟢 Easy: `{stats['easy']}` \| 🟡 Medium: `{stats['medium']}` \| 🔴 Hard: `{stats['hard']}` |
| **Weekly Velocity** | `{stats['week_count']}` problems solved in the last 7 days |
| **Monthly Velocity** | `{stats['month_count']}` problems solved in the last 30 days |

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
*Dashboard metrics updated automatically by GitHub Actions workflow container panel.*
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✔ README.md successfully updated with latest analytics.")

if __name__ == "__main__":
    problems_list = parse_local_repo()
    metrics = generate_analytics(problems_list)
    write_readme(metrics, problems_list)
