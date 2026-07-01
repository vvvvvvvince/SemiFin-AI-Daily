import os
import sys
import json
import datetime
import argparse

try:
    import feedparser
except ImportError:
    print("Error: feedparser package is required. Install it using 'pip install feedparser'")
    sys.exit(1)

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

def filter_entry(title, summary, blacklist):
    text = (title + " " + (summary or "")).lower()
    for word in blacklist:
        if word.lower() in text:
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Dry run execution')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'config')
    reports_dir = os.path.join(base_dir, 'reports', 'raw')
    os.makedirs(reports_dir, exist_ok=True)

    feeds = load_config(os.path.join(config_dir, 'feeds.yaml'))
    blacklist = load_config(os.path.join(config_dir, 'blacklist.yaml')).get('blacklist', [])

    results = {}
    today_str = datetime.date.today().isoformat()

    if args.dry_run:
        print("Dry run mode: using mock feeds")
        feeds = {
            "official_labs": [{"name": "Mock Lab", "url": "mock"}]
        }

    for category, category_feeds in feeds.items():
        results[category] = []
        for feed in category_feeds:
            name = feed['name']
            url = feed['url']
            print(f"Fetching {name} ({url})...")
            
            if args.dry_run or url == 'mock':
                results[category].append({
                    "feed_name": name,
                    "title": "Mock Article about Document AI and OCR",
                    "link": "http://example.com/mock",
                    "summary": "This is a mock summary of a very interesting document AI development.",
                    "published": today_str
                })
                continue
                
            try:
                parsed = feedparser.parse(url)
                count = 0
                for entry in parsed.entries:
                    if count >= 5:
                        break
                    
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    link = entry.get('link', '')
                    published = entry.get('published', entry.get('updated', today_str))

                    if filter_entry(title, summary, blacklist):
                        print(f"  Filtered: {title}")
                        continue

                    results[category].append({
                        "feed_name": name,
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "published": published
                    })
                    count += 1
            except Exception as e:
                print(f"Error fetching {name}: {e}")

    output_path = os.path.join(reports_dir, f'rss_{today_str}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved RSS data to {output_path}")

if __name__ == '__main__':
    main()
