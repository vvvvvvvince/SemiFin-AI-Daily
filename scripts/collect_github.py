import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
import re
import argparse

try:
    import yaml
except ImportError:
    print("Error: pyyaml package is required. Install it using 'pip install pyyaml'")
    sys.exit(1)

def load_config(config_path):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def fetch_latest_release(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/releases/latest"
    print(f"Fetching GitHub Release for {repo_name}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Antigravity AI Daily Client',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return {
                "repo": repo_name,
                "tag_name": data.get("tag_name"),
                "name": data.get("name"),
                "published_at": data.get("published_at"),
                "html_url": data.get("html_url"),
                "body": data.get("body", "")[:2000]
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  No release found for {repo_name} (404)")
        else:
            print(f"  HTTP error for {repo_name}: {e}")
    except Exception as e:
        print(f"  Error fetching {repo_name}: {e}")
    return None

def fetch_github_trending():
    url = "https://github.com/trending"
    print("Fetching GitHub Daily Trending...")
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html'
            }
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        articles = html.split('<article class="Box-row">')[1:]
        trending = []
        for i, article in enumerate(articles):
            if '<h2 class="h3 lh-condensed">' not in article:
                continue
            
            h2_section = article.split('<h2 class="h3 lh-condensed">')[1].split('</h2>')[0]
            href_match = re.search(r'href="([^"]+)"', h2_section)
            if not href_match:
                continue
            repo_path = href_match.group(1).strip('/')
            
            desc_match = re.search(r'<p class="col-9 color-fg-muted[^"]*">\s*(.*?)\s*</p>', article, re.DOTALL)
            desc = desc_match.group(1).strip() if desc_match else "No description"
            desc = re.sub(r'<[^>]*>', '', desc).replace('\n', ' ').strip()
            
            trending.append({
                "rank": len(trending) + 1,
                "repo": repo_path,
                "url": f"https://github.com/{repo_path}",
                "description": desc
            })
            if len(trending) >= 10:
                break
        return trending
    except Exception as e:
        print(f"Error fetching GitHub Trending: {e}")
        return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Dry run execution')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'config')
    reports_dir = os.path.join(base_dir, 'reports', 'raw')
    os.makedirs(reports_dir, exist_ok=True)

    watch_repos = load_config(os.path.join(config_dir, 'watch_repos.yaml')).get('watch_repos', [])
    today_str = datetime.date.today().isoformat()

    releases = []
    trending = []

    if args.dry_run:
        print("Dry run mode: using mock releases and trending")
        releases.append({
            "repo": "modelcontextprotocol/specification",
            "tag_name": "v0.5.0",
            "name": "MCP Specification Update",
            "published_at": today_str,
            "html_url": "https://github.com/modelcontextprotocol/specification/releases/tag/v0.5.0",
            "body": "### Breaking Changes\n- Updated authentication scheme in security spec.\n### New Capabilities\n- Added layout-parsing schema support."
        })
        trending.append({
            "rank": 1,
            "repo": "browser-use/video-use",
            "url": "https://github.com/browser-use/video-use",
            "description": "Edit videos with coding agents"
        })
    else:
        for repo in watch_repos:
            release = fetch_latest_release(repo)
            if release:
                releases.append(release)
        trending = fetch_github_trending()

    output = {
        "releases": releases,
        "trending": trending
    }

    output_path = os.path.join(reports_dir, f'github_{today_str}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Saved GitHub release and trending data to {output_path}")

if __name__ == '__main__':
    main()
