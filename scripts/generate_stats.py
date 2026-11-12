#!/usr/bin/env python3
"""
Generate GitHub stats SVGs using GitHub API
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

GITHUB_USERNAME = "rafael-hsm"
OUTPUT_DIR = "dist"

def get_github_stats():
    """Fetch user stats from GitHub API"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # Get user profile
    user_url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    user_resp = requests.get(user_url, headers=headers)
    user_data = user_resp.json()
    
    # Get repositories
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    repos_resp = requests.get(repos_url, headers=headers)
    repos_data = repos_resp.json()
    
    # Calculate stats
    total_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)
    
    # Language stats
    languages = {}
    for repo in repos_data:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    # Sort languages
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:7]
    
    return {
        "total_repos": total_repos,
        "followers": followers,
        "following": following,
        "languages": sorted_langs
    }

def generate_stats_svg(stats):
    """Generate SVG with GitHub stats"""
    width, height = 400, 180
    
    svg = ET.Element("svg", {
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "xmlns": "http://www.w3.org/2000/svg"
    })
    
    # Background
    rect = ET.SubElement(svg, "rect", {
        "width": str(width),
        "height": str(height),
        "fill": "#282a36",
        "rx": "10"
    })
    
    # Title
    title = ET.SubElement(svg, "text", {
        "x": "20",
        "y": "30",
        "fill": "#f8f8f2",
        "font-family": "Arial, sans-serif",
        "font-size": "16",
        "font-weight": "bold"
    })
    title.text = f"GitHub Stats - @{GITHUB_USERNAME}"
    
    # Stats
    y_offset = 60
    stats_items = [
        f"Repositories: {stats['total_repos']}",
        f"Followers: {stats['followers']}",
        f"Following: {stats['following']}"
    ]
    
    for item in stats_items:
        text = ET.SubElement(svg, "text", {
            "x": "20",
            "y": str(y_offset),
            "fill": "#bd93f9",
            "font-family": "Arial, sans-serif",
            "font-size": "14"
        })
        text.text = item
        y_offset += 25
    
    return ET.tostring(svg, encoding="unicode")

def generate_languages_svg(stats):
    """Generate SVG with top languages"""
    width, height = 400, 180
    
    svg = ET.Element("svg", {
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "xmlns": "http://www.w3.org/2000/svg"
    })
    
    # Background
    rect = ET.SubElement(svg, "rect", {
        "width": str(width),
        "height": str(height),
        "fill": "#282a36",
        "rx": "10"
    })
    
    # Title
    title = ET.SubElement(svg, "text", {
        "x": "20",
        "y": "30",
        "fill": "#f8f8f2",
        "font-family": "Arial, sans-serif",
        "font-size": "16",
        "font-weight": "bold"
    })
    title.text = "Top Languages"
    
    # Languages
    y_offset = 60
    colors = ["#ff79c6", "#8be9fd", "#50fa7b", "#f1fa8c", "#ffb86c", "#bd93f9", "#ff5555"]
    
    for i, (lang, count) in enumerate(stats["languages"]):
        color = colors[i % len(colors)]
        
        # Language name
        text = ET.SubElement(svg, "text", {
            "x": "20",
            "y": str(y_offset),
            "fill": color,
            "font-family": "Arial, sans-serif",
            "font-size": "14"
        })
        text.text = f"{lang}: {count} repos"
        y_offset += 25
    
    return ET.tostring(svg, encoding="unicode")

def main():
    """Main function"""
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    stats = get_github_stats()
    
    # Generate stats SVG
    stats_svg = generate_stats_svg(stats)
    with open(f"{OUTPUT_DIR}/github-stats.svg", "w") as f:
        f.write(stats_svg)
    
    # Generate languages SVG
    langs_svg = generate_languages_svg(stats)
    with open(f"{OUTPUT_DIR}/github-languages.svg", "w") as f:
        f.write(langs_svg)
    
    print("✓ Generated GitHub stats SVGs")

if __name__ == "__main__":
    main()
