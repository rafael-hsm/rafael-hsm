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
    width, height = 420, 200
    
    svg = ET.Element("svg", {
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "xmlns": "http://www.w3.org/2000/svg"
    })
    
    # Add style for dark/light mode support
    style = ET.SubElement(svg, "style")
    style.text = """
        @media (prefers-color-scheme: dark) {
            .bg { fill: #161b22; }
            .text { fill: #c9d1d9; }
            .stat { fill: #58a6ff; }
            .border { stroke: #30363d; }
        }
        @media (prefers-color-scheme: light) {
            .bg { fill: #ffffff; }
            .text { fill: #24292f; }
            .stat { fill: #0969da; }
            .border { stroke: #d0d7de; }
        }
    """
    
    # Background
    rect = ET.SubElement(svg, "rect", {
        "width": str(width),
        "height": str(height),
        "class": "bg",
        "rx": "12",
        "stroke-width": "1",
        "class": "bg border"
    })
    
    # Title
    title = ET.SubElement(svg, "text", {
        "x": "20",
        "y": "35",
        "class": "text",
        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
        "font-size": "18",
        "font-weight": "600"
    })
    title.text = f"📊 GitHub Stats"
    
    # Stats with icons
    y_offset = 70
    stats_items = [
        ("📦", f"Repositories", stats['total_repos']),
        ("👥", f"Followers", stats['followers']),
        ("👣", f"Following", stats['following'])
    ]
    
    for icon, label, value in stats_items:
        # Icon + label
        text = ET.SubElement(svg, "text", {
            "x": "20",
            "y": str(y_offset),
            "class": "text",
            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
            "font-size": "14"
        })
        text.text = f"{icon} {label}:"
        
        # Value
        value_text = ET.SubElement(svg, "text", {
            "x": "200",
            "y": str(y_offset),
            "class": "stat",
            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
            "font-size": "14",
            "font-weight": "600"
        })
        value_text.text = str(value)
        y_offset += 35
    
    return ET.tostring(svg, encoding="unicode")

def generate_languages_svg(stats):
    """Generate SVG with top languages"""
    width, height = 420, 220
    
    svg = ET.Element("svg", {
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "xmlns": "http://www.w3.org/2000/svg"
    })
    
    # Add style for dark/light mode support
    style = ET.SubElement(svg, "style")
    style.text = """
        @media (prefers-color-scheme: dark) {
            .bg { fill: #161b22; }
            .text { fill: #c9d1d9; }
            .border { stroke: #30363d; }
        }
        @media (prefers-color-scheme: light) {
            .bg { fill: #ffffff; }
            .text { fill: #24292f; }
            .border { stroke: #d0d7de; }
        }
    """
    
    # Background
    rect = ET.SubElement(svg, "rect", {
        "width": str(width),
        "height": str(height),
        "class": "bg",
        "rx": "12",
        "stroke-width": "1",
        "class": "bg border"
    })
    
    # Title
    title = ET.SubElement(svg, "text", {
        "x": "20",
        "y": "35",
        "class": "text",
        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
        "font-size": "18",
        "font-weight": "600"
    })
    title.text = "🔤 Top Languages"
    
    # Languages with GitHub colors
    lang_colors = {
        "Python": "#3572A5",
        "JavaScript": "#f1e05a",
        "HTML": "#e34c26",
        "CSS": "#563d7c",
        "TypeScript": "#2b7489",
        "Jupyter Notebook": "#F37626",
        "Java": "#b07219",
        "C++": "#f34b7d",
        "Go": "#00ADD8",
        "Rust": "#dea584",
        "PHP": "#4F5D95",
        "Ruby": "#701516",
        "Swift": "#F05138",
        "Kotlin": "#A97BFF",
        "Dart": "#00B4AB"
    }
    
    y_offset = 70
    
    for lang, count in stats["languages"][:7]:
        color = lang_colors.get(lang, "#58a6ff")
        
        # Language name
        text = ET.SubElement(svg, "text", {
            "x": "20",
            "y": str(y_offset),
            "class": "text",
            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
            "font-size": "14"
        })
        text.text = f"• {lang}"
        
        # Count
        count_text = ET.SubElement(svg, "text", {
            "x": "200",
            "y": str(y_offset),
            "class": "text",
            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
            "font-size": "14",
            "font-weight": "600"
        })
        count_text.text = f"{count} repos"
        
        # Color indicator
        circle = ET.SubElement(svg, "circle", {
            "cx": "350",
            "cy": str(y_offset - 5),
            "r": "6",
            "fill": color
        })
        
        y_offset += 28
    
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
